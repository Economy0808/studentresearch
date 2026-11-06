"""The one runnable check for the pipeline. `python selfcheck.py` exits non-zero on failure."""
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path

from store import append_jsonl, new_id, read_jsonl, write_jsonl


def check_store(tmp: Path, data: Path) -> None:
    p = data / "nested" / "x.jsonl"  # parent does not exist yet: exercises mkdir
    append_jsonl(p, {"a": 1, "k": "한글"})
    append_jsonl(p, {"a": 2, "sep": "a b c\u0085d"})  # line separators must survive a round trip
    assert read_jsonl(p) == [{"a": 1, "k": "한글"}, {"a": 2, "sep": "a b c\u0085d"}], read_jsonl(p)
    assert b"\r\n" not in p.read_bytes(), "JSONL must use LF on every platform"
    assert "한글" in p.read_text(encoding="utf-8"), "must not escape non-ASCII"
    write_jsonl(p, [{"a": 3}])
    assert read_jsonl(p) == [{"a": 3}]
    assert not list(p.parent.glob("*.tmp")), "write_jsonl must leave no temp file behind (atomic replace)"
    assert read_jsonl(tmp / "missing.jsonl") == []
    bom = tmp / "bom.jsonl"  # PowerShell/Notepad "UTF-8" files start with a BOM
    bom.write_bytes(b"\xef\xbb\xbf" + '{"a": "한글"}\n{"a": 2}\n'.encode("utf-8"))
    assert read_jsonl(bom) == [{"a": "한글"}, {"a": 2}], read_jsonl(bom)
    i = new_id("P")
    assert i.startswith("P-") and len(i) == 8, i


def check_llm_dry(tmp: Path, data: Path) -> None:
    import llm
    schema = {"type": "object", "properties": {"clarity": {}, "richness_list": {}}, "required": []}
    raw = tmp / "raw" / "t" / "x.json"
    out = llm.call("fable", "sys", "rate this: [fake sonnet] q", schema, raw, dry_run=True)
    assert out["richness_list"] == ["derived question"], out  # generator grade 1 → one item
    saved = __import__("json").loads(raw.read_text(encoding="utf-8"))
    assert saved["model"] == "fable" and saved["cli_output"]["structured_output"] == out
    assert llm.GRADE == {"sonnet": 1, "opus": 2, "fable": 3}
    assert llm.fake("sonnet", {"properties": {"saw_other_instructions": {}}}, "")["structured_output"]["saw_other_instructions"] is False
    bad = {"is_error": True, "result": "Failed to authenticate: OAuth session expired"}
    try:
        llm._raise_if_error(bad)
    except llm.StopRun:
        pass
    else:
        raise AssertionError("auth error must raise StopRun")


def check_llm_errors(tmp: Path, data: Path) -> None:
    import llm
    llm._consecutive_failures = 0
    for msg in ("timeout after 1800s",
                "empty stdout (exit 1); stderr tail: (node) MaxListenersExceededWarning: use setMaxListeners() to increase limit",
                "non-JSON stdout (exit 0): <html>", "input length and max_tokens exceed context limit"):
        try:
            llm._raise_if_error({"is_error": True, "result": msg})
        except llm.CallFailed:
            pass
        else:
            raise AssertionError(f"{msg!r} must raise CallFailed")
    try:  # four failures so far: the fifth in a row stops the run
        llm._raise_if_error({"is_error": True, "result": "timeout after 1800s"})
    except llm.StopRun as e:
        assert "5 consecutive failures" in str(e), e
    else:
        raise AssertionError("the fifth consecutive failure must raise StopRun")
    llm._consecutive_failures = 0
    for msg in ("Failed to authenticate: OAuth session expired", "You've hit your usage limit",
                "Rate limit reached for this plan", "Not logged in. Run /login",
                "You've hit your session limit · resets 3pm",
                "You've hit your Fable limit · continuing on Opus uses usage credits",
                "You're out of usage credits", "You're out of extra usage",
                "Invalid API key · Fix external API key", "Authentication error · Try again",
                "rate_limit_error", "authentication_error"):
        try:
            llm._raise_if_error({"is_error": True, "result": msg})
        except llm.StopRun:
            pass
        else:
            raise AssertionError(f"{msg!r} must raise StopRun")


def check_cli_offline(tmp: Path, data: Path) -> None:
    """Exercise _cli with subprocess.run patched: exact flags, stdin prompt, cwd, error mapping, raw log."""
    import json
    import os
    import llm
    seen = {}
    opus_ok = {"is_error": False, "structured_output": {"ok": True}, "modelUsage": {"claude-opus-5-5": {}}}

    class Done:
        def __init__(self, out, err="", rc=0):
            self.stdout, self.stderr, self.returncode = out, err, rc

    def fake_run(cmd, **kw):
        seen["cmd"], seen["kw"] = cmd, kw
        return Done(seen.pop("stdout_next", json.dumps(opus_ok)))

    def must_stop(raw_name, reply, want):
        seen["stdout_next"] = json.dumps(reply)
        try:
            llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {}}, tmp / "raw" / "t" / raw_name)
        except llm.StopRun as e:
            assert want in str(e), e
        else:
            raise AssertionError(f"{raw_name}: an answer not from opus must raise StopRun")

    real_run, real_exe, real_ver = llm.subprocess.run, llm.claude_exe, llm._CLI_VERSION
    llm.subprocess.run, llm.claude_exe, llm._CLI_VERSION = fake_run, lambda: "claude.exe", "claude 9.9.9"
    real_key = os.environ.get("ANTHROPIC_API_KEY")
    os.environ["ANTHROPIC_API_KEY"] = "sk-selfcheck"
    try:
        out = llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {"ok": {"type": "boolean"}}},
                       tmp / "raw" / "t" / "live.json")
        assert out == {"ok": True}, out
        assert "ANTHROPIC_API_KEY" not in seen["kw"]["env"], "the API key must not reach the CLI (Max plan, not API billing)"
        assert json.loads((tmp / "raw" / "t" / "live.json").read_text(encoding="utf-8"))["cli_version"] == "claude 9.9.9"
        cmd = seen["cmd"]
        assert cmd[:4] == ["claude.exe", "-p", "--model", "opus"], cmd
        for flag, val in (("--output-format", "json"), ("--tools", ""), ("--system-prompt", "SYS"),
                          ("--setting-sources", "project")):
            assert cmd[cmd.index(flag) + 1] == val, (flag, cmd)
        assert "--no-session-persistence" in cmd and "--strict-mcp-config" in cmd
        assert cmd[cmd.index("--mcp-config") + 1] == '{"mcpServers":{}}', cmd
        assert json.loads(cmd[cmd.index("--json-schema") + 1])["type"] == "object"
        assert seen["kw"]["input"] == "PROMPT" and seen["kw"]["encoding"] == "utf-8"
        assert seen["kw"]["errors"] == "replace" and seen["kw"]["timeout"] == llm.CALL_TIMEOUT == 3600, seen["kw"]
        neutral = Path(tempfile.gettempdir()) / "claude_cli_cwd"  # outside the repo: no project memory attaches
        assert Path(seen["kw"]["cwd"]) == neutral and neutral.is_dir()
        seen["stdout_next"] = "not json"
        try:
            llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {}}, tmp / "raw" / "t" / "bad.json")
        except llm.CallFailed:
            pass
        else:
            raise AssertionError("non-JSON stdout must raise CallFailed")
        logged = json.loads((tmp / "raw" / "t" / "bad.json").read_text(encoding="utf-8"))["cli_output"]
        assert logged["stdout"] == "not json" and logged["is_error"] is True, logged
        # a fallback to another model stops the whole run (live path only): wrong model, mixed, or no modelUsage at all
        must_stop("wrong.json", {"is_error": False, "structured_output": {"ok": True},
                                 "modelUsage": {"claude-sonnet-5-5": {"inputTokens": 1}}}, "not opus")
        must_stop("mixed.json", {"is_error": False, "structured_output": {"ok": True},
                                 "modelUsage": {"claude-opus-5-5": {}, "claude-sonnet-5-5": {}}}, "not opus")
        must_stop("nousage.json", {"is_error": False, "structured_output": {"ok": True}}, "unknown model")
        seen["stdout_next"] = json.dumps({"is_error": False, "structured_output": {"ok": True},
                                          "modelUsage": {"claude-opus-5-5": {"inputTokens": 1}}})
        assert llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {}}, tmp / "raw" / "t" / "right.json") == {"ok": True}
        seen["stdout_next"] = json.dumps({"is_error": False, "structured_output": {"nope": 1},
                                          "modelUsage": {"claude-opus-5-5": {}}})
        try:
            llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {"ok": {}}, "required": ["ok"]}, tmp / "raw" / "t" / "invalid.json")
        except llm.CallFailed as e:
            assert "missing required keys" in str(e), e
        else:
            raise AssertionError("output missing a required key must raise CallFailed")
    finally:
        llm.subprocess.run, llm.claude_exe, llm._CLI_VERSION = real_run, real_exe, real_ver
        if real_key is None:
            os.environ.pop("ANTHROPIC_API_KEY", None)
        else:
            os.environ["ANTHROPIC_API_KEY"] = real_key
        llm._consecutive_failures = 0


def check_prompts(tmp: Path, data: Path) -> None:
    root = Path(__file__).resolve().parent
    expected = {"system.md": set(), "gen_open.md": {"context", "focus"}, "gen_checkable.md": {"context", "focus"},
                "solve.md": {"statement", "finite_form", "candidate_format"},
                "eval_problem.md": {"rubric", "statement", "finite_form"},
                "eval_solution.md": {"rubric", "statement", "finite_form", "text", "candidate"},
                "rubric.md": set()}
    for name, want in expected.items():
        text = (root / "prompts" / name).read_text(encoding="utf-8")
        found = set(re.findall(r"\{([a-z_]+)\}", text))
        assert found == want, f"{name}: placeholders {found} != {want}"
    assert "checker_code" in (root / "prompts" / "gen_checkable.md").read_text(encoding="utf-8")
    rubric = (root / "prompts" / "rubric.md").read_text(encoding="utf-8")
    for key in ("(clarity,", "(difficulty,", "(richness_list)", "(want_to_solve,", "(known_problem,",
                "(correctness,", "(clarity_sol,", "(understandable)"):
        assert key in rubric, f"rubric.md lacks {key}"
    for name in ("solve.md", "eval_problem.md", "eval_solution.md"):
        text = (root / "prompts" / name).read_text(encoding="utf-8")
        for leak in ("source", "solver", "grounding", "why_hard", "gen_key"):
            assert "{" + leak + "}" not in text, f"{name} must not reveal {leak}"
    row = json.loads((root / "human_problems.example.jsonl").read_text(encoding="utf-8").strip())
    assert row["source"] == "human" and re.fullmatch(r"P-[0-9a-f]{6}", row["id"]), row
    assert "note" in row


CONTEXT = """# Fake pack

## Definitions
fake

## Result: A
fake a

## Result: B
fake b

## Format examples
fake
"""


def check_gen(tmp: Path, data: Path) -> None:
    import pipeline
    ctx = tmp / "ctx.md"
    ctx.write_text(CONTEXT, encoding="utf-8")
    assert pipeline.parse_context(ctx)[1] == ["Result: A", "Result: B"]
    n1 = pipeline.gen(data, ctx, "open", 2, dry_run=True)
    n2 = pipeline.gen(data, ctx, "checkable", 1, dry_run=True)
    assert (n1, n2) == (6, 3), (n1, n2)
    assert pipeline.gen(data, ctx, "open", 2, dry_run=True) == 0, "gen must be idempotent"
    probs = read_jsonl(data / "problems.jsonl")
    assert len(probs) == 9
    assert {p["focus"] for p in probs if p["kind"] == "open"} == {"Result: A", "Result: B"}
    assert all(p["id"].startswith("P-") and p["source"] in ("sonnet", "opus", "fable") for p in probs)
    assert all(p["checker_code"] is None for p in probs if p["kind"] == "open")
    checkers = sorted((tmp / "checkers").glob("P-*.py"))
    assert len(checkers) == 3, checkers
    first = checkers[0].read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("# UNREVIEWED"), first
    raws = list((data / "raw" / "gen").glob("*.json"))
    assert len(raws) == 9, len(raws)
    assert pipeline.fill("a {x} b {y}", x="1", y=None) == "a 1 b "
    assert pipeline.fill("{text}", text="see {candidate}") == "see {candidate}", "inserted text must not be rescanned"
    assert pipeline.fill("{a_{n}} {z}", z="1") == "{a_{n}} 1", "unknown tokens stay untouched"
    fenced =tmp / "fenced.md"
    fenced.write_text("# README\n\n```\n## Result: <x>\n```\n", encoding="utf-8")
    try:
        pipeline.parse_context(fenced)
    except SystemExit:
        pass
    else:
        raise AssertionError("a '## Result:' line inside a code fence must not count as a section")
    mixed = tmp / "mixed.md"
    mixed.write_text("## Result: Real\nx\n\n```\n## Result: Fenced\n```\n\n~~~\n## Result: Tilde\n~~~\n\n## Result: Real2\ny\n", encoding="utf-8")
    assert pipeline.parse_context(mixed)[1] == ["Result: Real", "Result: Real2"]
    try:
        pipeline.parse_context(Path(__file__).resolve().parent / "context" / "README.md")
    except SystemExit:
        pass
    else:
        raise AssertionError("context/README.md has only fenced Result headings and must be rejected")
    cid = "ctx-" + hashlib.sha256(ctx.read_text(encoding="utf-8").encode("utf-8")).hexdigest()[:8]
    assert {p["context_id"] for p in probs} == {cid}, "context_id carries a hash of the pack text"
    assert [p["source"] for p in probs[:6]] == ["sonnet", "opus", "fable"] * 2, "generation is item-major: a partial run stays balanced"
    prompts = {json.loads((data / "raw" / "gen" / f"{cid}_open_{m}_0.json").read_text(encoding="utf-8"))["prompt"] for m in ("sonnet", "opus", "fable")}
    assert len(prompts) == 1, "the three models must receive byte-identical prompts"
    for p in probs:
        if p["kind"] == "checkable":
            assert p["finite_form"] and p["checker_code"] and p["candidate_format"], p
    # a failed call is recorded and retried on the next run (own data dir: the shared one must keep exactly 9 problems)
    d2 = tmp / "flaky" / "data"
    real_call = pipeline.llm.call
    calls = {"n": 0}

    def flaky(*a, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            raise pipeline.llm.CallFailed("boom")
        return real_call(*a, **kw)

    pipeline.llm.call = flaky
    try:
        assert pipeline.gen(d2, ctx, "open", 1, dry_run=True) == 2, "one of the 3 calls fails"
        fails = read_jsonl(d2 / "failures.jsonl")
        assert len(fails) == 1 and fails[0]["stage"] == "gen" and fails[0]["error"] == "boom", fails
        assert pipeline.gen(d2, ctx, "open", 1, dry_run=True) == 1, "the failed item is retried"
    finally:
        pipeline.llm.call = real_call
    assert len(read_jsonl(data / "problems.jsonl")) == 9, "shared data dir must still hold exactly 9 problems"


def check_solve(tmp: Path, data: Path) -> None:
    import pipeline
    assert pipeline.solve(data, dry_run=True) == 27
    assert pipeline.solve(data, dry_run=True) == 0, "solve must be idempotent"
    sols = read_jsonl(data / "solutions.jsonl")
    assert len(sols) == 27 and all(s["id"].startswith("S-") for s in sols)
    assert {s["solver"] for s in sols} == {"sonnet", "opus", "fable"}
    raw = next((data / "raw" / "solve").glob("*.json")).read_text(encoding="utf-8")
    for leak in ('"source"', "grounding", "gen_key"):
        assert leak not in __import__("json").loads(raw)["prompt"], f"solve prompt leaks {leak}"
    # a claimed_status outside the enum is a recorded failure, not a solution row (own data dir)
    d = tmp / "badsolve" / "data"
    append_jsonl(d / "problems.jsonl", {"id": "P-0e0e0e", "statement": "s"})
    real_call = pipeline.llm.call
    pipeline.llm.call = lambda *a, **kw: {"text": "t", "claimed_status": "maybe", "candidate": None}
    try:
        assert pipeline.solve(d, ["sonnet"], dry_run=True) == 0
    finally:
        pipeline.llm.call = real_call
    fails = read_jsonl(d / "failures.jsonl")
    assert len(fails) == 1 and "claimed_status out of range" in fails[0]["error"], fails
    assert not (d / "solutions.jsonl").exists()


def check_time_budget(tmp: Path, data: Path) -> None:
    import pipeline, llm
    d3 = tmp / "budget" / "data"
    p = {"id": "P-b0d9e7", "source": "sonnet", "kind": "open", "context_id": "x", "focus": "Result: A", "gen_key": "x:open:sonnet:0",
         "statement": "[fake sonnet] budget test", "grounding": "g", "why_hard": "h", "why_important": "w", "resembles_known": None,
         "novelty_confidence": 0.5, "finite_form": None, "candidate_format": None, "checker_code": None, "created_at": "2026-10-18T00:00:00+00:00"}
    append_jsonl(d3 / "problems.jsonl", p)
    for _ in range(2):
        append_jsonl(d3 / "failures.jsonl", {"stage": "solve", "target_id": p["id"], "model": "fable", "error": f"timeout after {llm.CALL_TIMEOUT}s", "created_at": "2026-10-18T00:00:00+00:00"})
    append_jsonl(d3 / "failures.jsonl", {"stage": "solve", "target_id": p["id"], "model": "opus", "error": f"timeout after {llm.CALL_TIMEOUT}s", "created_at": "2026-10-18T00:00:00+00:00"})
    assert pipeline.solve(d3, dry_run=True) == 3, "sonnet and opus are solved by the fake; fable gets a budget row"
    sols = read_jsonl(d3 / "solutions.jsonl")
    fab = next(s for s in sols if s["solver"] == "fable")
    assert fab["budget_exceeded"] is True and fab["claimed_status"] == "unsolved" and fab["candidate"] is None and "[pipeline]" in fab["text"], fab
    assert all(not s.get("budget_exceeded") for s in sols if s["solver"] != "fable"), "one timeout must not trigger the budget"
    assert not (d3 / "raw" / "solve" / f"{p['id']}_fable.json").exists(), "the model must not be called for a budget row"
    assert pipeline.solve(d3, dry_run=True) == 0, "idempotent"
    assert pipeline.eval_ai(d3, dry_run=True) == 3 + 2 * 3, "problem x 3 raters + 2 real solutions x 3 raters; the budget row is not rated"
    blind = json.loads(pipeline.export_human(d3, ["R1"]).read_text(encoding="utf-8"))
    assert len(blind["problems"][0]["solutions"]) == 2, "budget row is not exported"


def check_eval(tmp: Path, data: Path) -> None:
    import pipeline
    assert pipeline.eval_ai(data, dry_run=True) == 9 * 3 + 27 * 3
    assert pipeline.eval_ai(data, dry_run=True) == 0, "eval must be idempotent"
    ratings = read_jsonl(data / "ratings.jsonl")
    probs = {p["id"]: p for p in read_jsonl(data / "problems.jsonl")}
    grade = {"sonnet": 1, "opus": 2, "fable": 3}
    for r in ratings:
        assert r["rater_type"] == "ai" and r["rater"] in grade
        if r["target_type"] == "problem":
            assert len(r["richness_list"]) == grade[probs[r["target_id"]]["source"]], r
        else:
            assert r["correctness"] == min(5, 2 + grade[r["rater"]]), r
    raw = next((data / "raw" / "eval").glob("*.json")).read_text(encoding="utf-8")
    prompt = __import__("json").loads(raw)["prompt"]
    assert "채점표" in prompt and '"source"' not in prompt and "grounding" not in prompt
    # AI ratings are stored cleaned, like human ones: out-of-range or wrongly typed values become null (own data dir)
    d = tmp / "badeval" / "data"
    append_jsonl(d / "problems.jsonl", {"id": "P-0e0e0e", "statement": "s", "why_important": "WHYSENTINEL"})
    real_call = pipeline.llm.call
    seen = []
    pipeline.llm.call = lambda *a, **kw: seen.append(a[2]) or {"clarity": 9, "difficulty": 3, "want_to_solve": True,
                                          "richness_list": ["x", 3, " y "], "known_problem": "no"}
    try:
        assert pipeline.eval_ai(d, ["sonnet"], dry_run=True) == 1
        assert "WHYSENTINEL" not in seen[0], "raters must not see why_important"
    finally:
        pipeline.llm.call = real_call
    r = read_jsonl(d / "ratings.jsonl")[0]
    assert (r["clarity"], r["difficulty"], r["want_to_solve"], r["richness_list"], r["known_problem"]) == (None, 3, None, ["x", "y"], None), r


def check_verify(tmp: Path, data: Path) -> None:
    import pipeline
    probs = {p["source"]: p for p in read_jsonl(data / "problems.jsonl") if p["kind"] == "checkable"}
    for src in ("sonnet", "fable"):  # review two of the three checkers; leave opus unreviewed
        f = tmp / "checkers" / f"{probs[src]['id']}.py"
        lines = f.read_text(encoding="utf-8").splitlines()
        lines[0] = "# REVIEWED"
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert pipeline.verify(data) == 6, "2 reviewed problems × 3 solvers"
    assert pipeline.verify(data) == 0, "verify must be idempotent"
    sols = {s["id"]: s for s in read_jsonl(data / "solutions.jsonl")}
    verdicts = {(probs_src(sols[v["solution_id"]], probs), sols[v["solution_id"]]["solver"]): v["verdict"]
                for v in read_jsonl(data / "verifications.jsonl")}
    assert verdicts[("sonnet", "opus")] == "pass" and verdicts[("sonnet", "fable")] == "pass"
    assert verdicts[("sonnet", "sonnet")] == "fail"
    assert all(verdicts[("fable", m)] == "fail" for m in ("sonnet", "opus", "fable")), verdicts
    assert ("opus", "opus") not in verdicts, "unreviewed checker must be skipped"


def probs_src(sol: dict, probs: dict) -> str:
    return next(src for src, p in probs.items() if p["id"] == sol["problem_id"])


def check_verify_errors(tmp: Path, data: Path) -> None:
    """Own data dir: a crashing/hanging/missing checker is recorded as 'error' (never raises); no candidate → 'na'."""
    import pipeline
    d = tmp / "verr" / "data"
    (tmp / "verr" / "checkers").mkdir(parents=True)
    for pid, body in (("P-crash", "raise RuntimeError('한글 boom')"), ("P-slow", "__import__('time').sleep(30)"),
                      ("P-pexit", "print('PASS')\n    raise SystemExit(1)")):  # prints PASS, then a non-zero exit: must not count as pass
        (tmp / "verr" / "checkers" / f"{pid}.py").write_text(f"# REVIEWED\ndef check(c):\n    {body}\n", encoding="utf-8")
    (tmp / "verr" / "checkers" / "P-empty.py").write_bytes(b"")  # zero bytes: no first line → not REVIEWED → skipped, never raises
    for pid in ("P-crash", "P-slow", "P-miss", "P-na", "P-pexit", "P-empty"):
        append_jsonl(d / "problems.jsonl", {"id": pid, "kind": "checkable"})
        append_jsonl(d / "solutions.jsonl", {"id": "S-" + pid, "problem_id": pid, "candidate": None if pid == "P-na" else [1]})
    assert pipeline.verify(d, timeout=3) == 5, "P-empty is skipped, the other five get a row"
    got = {v["problem_id"]: v["verdict"] for v in read_jsonl(d / "verifications.jsonl")}
    assert got == {"P-crash": "error", "P-slow": "error", "P-miss": "error", "P-na": "na", "P-pexit": "error"}, got
    log = next(v["log"] for v in read_jsonl(d / "verifications.jsonl") if v["problem_id"] == "P-crash")
    assert "한글 boom" in log, log  # child tracebacks are UTF-8 (-X utf8), not the console code page


def check_roundtrip(tmp: Path, data: Path) -> None:
    import contextlib
    import io
    import json
    import pipeline
    HP = "P-ab12cd"  # a human control problem: it has no solutions and its note names the source
    write_jsonl(data.parent / "human_problems.jsonl", [
        {"id": HP, "source": "human", "kind": "open", "context_id": None, "focus": None,
         "statement": "Human control problem $x$", "grounding": None, "why_hard": None,
         "why_important": "Would settle a basic question.", "resembles_known": None, "novelty_confidence": None,
         "finite_form": None, "candidate_format": None, "checker_code": None,
         "note": "Erdős problem #1, erdosproblems.com/1", "created_at": "2026-10-18T00:00:00+00:00"}])
    out = pipeline.export_human(data, ["R1", "R2"])
    text = out.read_text(encoding="utf-8")
    blind = json.loads(text)
    assert len(blind["problems"]) == 10 and all(len(p["solutions"]) == 3 for p in blind["problems"] if p["id"] != HP)
    assert all([s["id"] for s in p["solutions"]] == sorted(s["id"] for s in p["solutions"]) for p in blind["problems"]), "solutions must be ordered by opaque id, not solver"
    for leak in ('"source"', '"solver"', '"grounding"', '"why_hard"', '"why_important"', '"gen_key"', '"kind"', '"note"', "erdosproblems"):
        assert leak not in text, f"blind.json leaks {leak}"
    assert "채점표" in blind["rubric_md"] and blind["raters"] == ["R1", "R2"]
    rows = [{"rater": "R1", "target_type": "problem", "target_id": p["id"], "clarity": 4, "difficulty": None,
             "want_to_solve": 2, "richness_list": ["x"], "known_problem": False, "source_guess": "ai_mid"}
            for p in blind["problems"]]
    rows[0]["clarity"] = True  # JSON true is not a score
    rows[2]["richness_list"] = ["x", 3, None, " y "]  # only strings survive, trimmed
    rows.append(dict(rows[1], clarity=5))  # same (rater, type, id) twice in one file: the last one wins
    rows.append({"rater": "R9", "target_type": "problem", "target_id": blind["problems"][0]["id"], "clarity": 1})
    first_sol = next(p for p in blind["problems"] if p["solutions"])["solutions"][0]["id"]
    rows.append({"rater": "R1", "target_type": "solution", "target_id": first_sol,
                 "correctness": 9, "clarity_sol": 3, "understandable": None})
    f = tmp / "human.json"
    f.write_text(json.dumps(rows), encoding="utf-8")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert pipeline.import_human(data, f) == 11, "10 problem rows (the duplicate collapsed) + 1 solution row; R9 skipped"
    assert "import-human: 11 new, 0 replaced" in buf.getvalue(), buf.getvalue()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert pipeline.import_human(data, f) == 11
    assert "import-human: 0 new, 11 replaced" in buf.getvalue(), buf.getvalue()
    human =[r for r in read_jsonl(data / "ratings.jsonl") if r["rater_type"] == "human"]
    assert len(human) == 11, "re-import must overwrite, not duplicate"
    by_id = {r["target_id"]: r for r in human if r["target_type"] == "problem"}
    assert by_id[blind["problems"][0]["id"]]["clarity"] is None, "JSON true must not count as score 1"
    assert by_id[blind["problems"][1]["id"]]["clarity"] == 5, "last duplicate row wins"
    assert by_id[blind["problems"][2]["id"]]["richness_list"] == ["x", "y"]
    sol = next(r for r in human if r["target_type"] == "solution")
    assert sol["correctness"] is None, "out-of-range score becomes null"
    assert all(r["source_guess"] in ("ai_mid", None) for r in human)
    assert len([r for r in read_jsonl(data / "ratings.jsonl") if r["rater_type"] == "ai"]) == 108
    # export refuses anything that could reveal a source (own data dirs)
    cases = {"hid": ({"id": "P-h00001", "statement": "s"}, None),
             "dup": ({"id": "P-0a0a0a", "statement": "s"}, None),
             "sid": ({"id": "P-0c0c0c", "statement": "s"}, {"id": "S-opus", "problem_id": "P-0c0c0c", "text": "t"}),
             "sdup": ({"id": "P-0d0d0d", "statement": "s"}, {"id": "S-0a0a0a", "problem_id": "P-0d0d0d", "text": "t"})}
    for name, (prob, sol_row) in cases.items():
        d = tmp / "leak" / name / "data"
        append_jsonl(d / "problems.jsonl", prob)
        if name == "dup":
            append_jsonl(d / "problems.jsonl", prob)
        if sol_row:
            append_jsonl(d / "solutions.jsonl", sol_row)
        if name == "sdup":
            append_jsonl(d / "solutions.jsonl", sol_row)
        try:
            pipeline.export_human(d, ["R1"])
        except SystemExit:
            assert not (d / "blind.json").exists(), f"{name}: a refused export must not write blind.json"
        else:
            raise AssertionError(f"export_human must refuse case {name!r}")
    # a row whose target is not in blind.json (stale export) is kept but warned about
    d = tmp / "stale" / "data"
    append_jsonl(d / "problems.jsonl", {"id": "P-0e0e0e", "statement": "s"})
    pipeline.export_human(d, ["R1"])
    g = tmp / "stale.json"
    g.write_text(json.dumps([{"rater": "R1", "target_type": "problem", "target_id": i, "clarity": 3}
                             for i in ("P-0e0e0e", "P-ffffff")]), encoding="utf-8")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert pipeline.import_human(d, g) == 2
    assert "'P-ffffff'" in buf.getvalue() and "'P-0e0e0e'" not in buf.getvalue(), buf.getvalue()
    assert len(read_jsonl(d / "ratings.jsonl")) == 2
    # the page template gets the JSON with every '<' escaped, so no payload text can close the script tag
    d = tmp / "tpl" / "data"
    append_jsonl(d / "problems.jsonl", {"id": "P-0d0d0d", "statement": "x </script><!-- y"})
    (tmp / "tpl" / "eval_page").mkdir(parents=True)
    (tmp / "tpl" / "eval_page" / "template.html").write_text("<script>const B = /*BLIND_JSON*/;</script>", encoding="utf-8")
    pipeline.export_human(d, ["R1"])
    page = (tmp / "tpl" / "eval_page" / "index.html").read_text(encoding="utf-8")
    payload = page[len("<script>const B = "):-len(";</script>")]
    assert "<" not in payload and json.loads(payload)["problems"][0]["statement"] == "x </script><!-- y", page


def check_analyze(tmp: Path, data: Path) -> None:
    import json
    import analyze
    import pipeline
    blind = json.loads((data / "blind.json").read_text(encoding="utf-8"))
    r2 = [{"rater": "R2", "target_type": "problem", "target_id": p["id"], "clarity": 4, "difficulty": 2,
           "want_to_solve": 3, "richness_list": ["a", "b"], "known_problem": None} for p in blind["problems"]]
    f2 = tmp / "human_r2.json"
    f2.write_text(json.dumps(r2), encoding="utf-8")
    assert pipeline.import_human(data, f2) == len(blind["problems"])
    # the human control problem (written by check_roundtrip) is now solved and rated like any other
    assert pipeline.solve(data, dry_run=True) == 3
    assert pipeline.eval_ai(data, dry_run=True) == 3 + 9, "1 human problem x 3 raters + 3 new solutions x 3 raters"
    hp = next(p for p in pipeline.all_problems(data) if p["source"] == "human")
    for stage in ("solve", "eval"):
        files = sorted((data / "raw" / stage).glob(f"{hp['id']}_*.json"))
        assert len(files) == 3, files
        assert len({json.loads(f.read_text(encoding="utf-8"))["prompt"] for f in files}) == 1, \
            f"{stage}: the three models must receive byte-identical prompts for one problem"
    opus_checkable = next(p for p in read_jsonl(data / "problems.jsonl") if p["kind"] == "checkable" and p["source"] == "opus")
    some_sol = next(s for s in read_jsonl(data / "solutions.jsonl") if s["problem_id"] == opus_checkable["id"])
    for log in ("fixture", "fixture, written twice"):  # a duplicated verification row must not break analysis (load keeps the last)
        append_jsonl(data / "verifications.jsonl", {"solution_id": some_sol["id"], "problem_id": opus_checkable["id"], "verdict": "error", "log": log, "created_at": "2026-10-18T00:00:00+00:00"})
    t = analyze.main(data, tmp / "results")
    ai = t["q_g"].loc["ai"]
    assert [ai.loc[s, "richness"] for s in ("sonnet", "opus", "fable")] == [1.0, 2.0, 3.0], ai
    lad = t["ladder_ceiling"].set_index(["generator", "kind"])
    nan = lambda x: x != x
    assert lad.loc[("sonnet", "checkable"), "ladder"] == 1.0 and int(lad.loc[("sonnet", "checkable"), "n_verified"]) == 3, lad
    assert lad.loc[("sonnet", "open"), "ladder"] == 0.5, "opus 4.0 (success) and fable 3.5 (not), solver's own rating excluded"
    assert nan(lad.loc[("fable", "checkable"), "ladder"]), "fable has no upper model → NaN"
    assert int(lad.loc[("fable", "checkable"), "n_verified"]) == 3 and int(lad.loc[("opus", "checkable"), "n_verified"]) == 0, lad
    sp = t["self_preference"]
    assert set(sp["rater"]) == {"sonnet", "opus", "fable"}
    assert (sp.filter(like="bias_").fillna(0).abs() < 1e-9).all().all(), sp  # fake raters score alike, so no self-preference
    assert (tmp / "results" / "metrics.md").exists() and (tmp / "results" / "q_g.csv").exists()
    assert not t["cannot_judge"].empty, "human ratings from check_roundtrip must appear"
    kw = t["kendall_w"]
    assert not kw.empty and kw["n_raters"].eq(2).all() and kw["kendall_W"].dropna().between(0, 1).all(), kw
    cj = t["cannot_judge"]
    assert "cj_difficulty" in cj and cj[cj.target_type == "problem"]["cj_difficulty"].eq(0.5).all(), cj  # R1 null, R2 = 2
    assert cj[cj.target_type == "problem"]["cj_known_problem"].eq(0.5).all(), cj  # R1 false, R2 null
    assert "actor" in cj and "source" not in cj, cj
    kr = t["kruskal"]
    assert kr[kr.rater_type == "ai"]["n_problems"].eq(9).all(), kr


def check_mixed_export(tmp: Path, data: Path) -> None:
    import pipeline
    d3, d4 = tmp / "budget" / "data", tmp / "mixed_high" / "data"  # d3 comes from check_time_budget
    p = dict(read_jsonl(d3 / "problems.jsonl")[0], id="P-4a1c3e", gen_key="y:open:sonnet:0", statement="[fake sonnet] high-context test")
    append_jsonl(d4 / "problems.jsonl", p)
    assert pipeline.solve(d4, models=["sonnet"], dry_run=True) == 1
    blind_path = pipeline.export_human(d3, ["R1"], [d4])
    blind = json.loads(blind_path.read_text(encoding="utf-8"))
    assert {q["id"] for q in blind["problems"]} == {"P-b0d9e7", "P-4a1c3e"}, "both folders in one export"
    assert str(d4) not in blind_path.read_text(encoding="utf-8"), "the rating page must not see which folder a problem came from"
    s4 = read_jsonl(d4 / "solutions.jsonl")[0]["id"]
    sub = tmp / "mixed_ratings.json"
    sub.write_text(json.dumps([{"rater": "R1", "target_type": "problem", "target_id": i, "clarity": 3} for i in ("P-b0d9e7", "P-4a1c3e")]
                              + [{"rater": "R1", "target_type": "solution", "target_id": s4, "correctness": 2}]), encoding="utf-8")
    assert pipeline.import_human(d3, sub) == 3
    hum = lambda d: {r["target_id"] for r in read_jsonl(d / "ratings.jsonl") if r["rater_type"] == "human"}
    assert hum(d3) == {"P-b0d9e7"} and hum(d4) == {"P-4a1c3e", s4}, "each rating goes to the folder that owns its target"
    assert pipeline.import_human(d3, sub) == 3 and len(hum(d4)) == 2, "re-import replaces, never duplicates"
    pipeline.export_human(d3, ["R1"])
    assert not (d3 / "blind_sources.json").exists(), "a plain export drops a stale routing file"


CHECKS = [check_store, check_llm_dry, check_llm_errors, check_cli_offline, check_prompts, check_gen, check_solve,
          check_time_budget, check_mixed_export, check_eval, check_verify, check_verify_errors, check_roundtrip, check_analyze]


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="selfcheck_"))
    data = tmp / "data"
    try:
        for fn in CHECKS:
            fn(tmp, data)
            print(f"ok  {fn.__name__}")
        print("selfcheck OK")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
