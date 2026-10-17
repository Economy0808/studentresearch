"""The one runnable check for the pipeline. `python selfcheck.py` exits non-zero on failure."""
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
    for msg in ("timeout after 1800s",
                "empty stdout (exit 1); stderr tail: (node) MaxListenersExceededWarning: use setMaxListeners() to increase limit",
                "non-JSON stdout (exit 0): <html>", "input length and max_tokens exceed context limit"):
        try:
            llm._raise_if_error({"is_error": True, "result": msg})
        except llm.CallFailed:
            pass
        else:
            raise AssertionError(f"{msg!r} must raise CallFailed")
    for msg in ("Failed to authenticate: OAuth session expired", "You've hit your usage limit",
                "Rate limit reached for this plan", "Not logged in. Run /login",
                "You've hit your session limit · resets 3pm",
                "You've hit your Fable limit · continuing on Opus uses usage credits",
                "You're out of usage credits", "You're out of extra usage",
                "Invalid API key · Fix external API key", "Authentication error · Try again"):
        try:
            llm._raise_if_error({"is_error": True, "result": msg})
        except llm.StopRun:
            pass
        else:
            raise AssertionError(f"{msg!r} must raise StopRun")


def check_cli_offline(tmp: Path, data: Path) -> None:
    """Exercise _cli with subprocess.run patched: exact flags, stdin prompt, cwd, error mapping, raw log."""
    import json
    import llm
    seen = {}

    class Done:
        def __init__(self, out, err="", rc=0):
            self.stdout, self.stderr, self.returncode = out, err, rc

    def fake_run(cmd, **kw):
        seen["cmd"], seen["kw"] = cmd, kw
        return Done(seen.pop("stdout_next", json.dumps({"is_error": False, "structured_output": {"ok": True}})))

    real_run, real_exe = llm.subprocess.run, llm.claude_exe
    llm.subprocess.run, llm.claude_exe = fake_run, lambda: "claude.exe"
    try:
        out = llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {"ok": {"type": "boolean"}}},
                       tmp / "raw" / "t" / "live.json")
        assert out == {"ok": True}, out
        cmd = seen["cmd"]
        assert cmd[:4] == ["claude.exe", "-p", "--model", "opus"], cmd
        for flag, val in (("--output-format", "json"), ("--tools", ""), ("--system-prompt", "SYS"),
                          ("--setting-sources", "project")):
            assert cmd[cmd.index(flag) + 1] == val, (flag, cmd)
        assert "--no-session-persistence" in cmd
        assert json.loads(cmd[cmd.index("--json-schema") + 1])["type"] == "object"
        assert seen["kw"]["input"] == "PROMPT" and seen["kw"]["encoding"] == "utf-8"
        assert seen["kw"]["errors"] == "replace" and seen["kw"]["timeout"] == 1800, seen["kw"]
        assert Path(seen["kw"]["cwd"]) == tmp / "raw" / "_cwd" and (tmp / "raw" / "_cwd").is_dir()
        seen["stdout_next"] = "not json"
        try:
            llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {}}, tmp / "raw" / "t" / "bad.json")
        except llm.CallFailed:
            pass
        else:
            raise AssertionError("non-JSON stdout must raise CallFailed")
        logged = json.loads((tmp / "raw" / "t" / "bad.json").read_text(encoding="utf-8"))["cli_output"]
        assert logged["stdout"] == "not json" and logged["is_error"] is True, logged
        seen["stdout_next"] = json.dumps({"is_error": False, "structured_output": {"ok": True},
                                          "modelUsage": {"claude-sonnet-5-5": {"inputTokens": 1}}})
        try:
            llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {}}, tmp / "raw" / "t" / "wrong.json")
        except llm.CallFailed as e:
            assert "not opus" in str(e), e
        else:
            raise AssertionError("an answer from another model must raise CallFailed")
        seen["stdout_next"] = json.dumps({"is_error": False, "structured_output": {"ok": True},
                                          "modelUsage": {"claude-opus-5-5": {"inputTokens": 1}}})
        assert llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {}}, tmp / "raw" / "t" / "right.json") == {"ok": True}
        seen["stdout_next"] = json.dumps({"is_error": False, "structured_output": {"nope": 1}})
        try:
            llm.call("opus", "SYS", "PROMPT", {"type": "object", "properties": {"ok": {}}, "required": ["ok"]}, tmp / "raw" / "t" / "invalid.json")
        except llm.CallFailed as e:
            assert "missing required keys" in str(e), e
        else:
            raise AssertionError("output missing a required key must raise CallFailed")
    finally:
        llm.subprocess.run, llm.claude_exe = real_run, real_exe


def check_prompts(tmp: Path, data: Path) -> None:
    root = Path(__file__).resolve().parent
    expected = {"system.md": set(), "gen_open.md": {"context", "focus"}, "gen_checkable.md": {"context", "focus"},
                "solve.md": {"statement", "finite_form", "candidate_format"},
                "eval_problem.md": {"rubric", "statement", "finite_form", "why_important"},
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
    assert "erd" not in row["why_important"].lower() and "http" not in row["why_important"].lower(), "why_important must not name the source"
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
    fenced = tmp / "fenced.md"
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
    prompts = {json.loads((data / "raw" / "gen" / f"ctx_open_{m}_0.json").read_text(encoding="utf-8"))["prompt"] for m in ("sonnet", "opus", "fable")}
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
    for pid, body in (("P-crash", "raise RuntimeError('boom')"), ("P-slow", "__import__('time').sleep(30)"),
                      ("P-pexit", "print('PASS')\n    raise SystemExit(1)")):  # prints PASS, then a non-zero exit: must not count as pass
        (tmp / "verr" / "checkers" / f"{pid}.py").write_text(f"# REVIEWED\ndef check(c):\n    {body}\n", encoding="utf-8")
    (tmp / "verr" / "checkers" / "P-empty.py").write_bytes(b"")  # zero bytes: no first line → not REVIEWED → skipped, never raises
    for pid in ("P-crash", "P-slow", "P-miss", "P-na", "P-pexit", "P-empty"):
        append_jsonl(d / "problems.jsonl", {"id": pid, "kind": "checkable"})
        append_jsonl(d / "solutions.jsonl", {"id": "S-" + pid, "problem_id": pid, "candidate": None if pid == "P-na" else [1]})
    assert pipeline.verify(d, timeout=3) == 5, "P-empty is skipped, the other five get a row"
    got = {v["problem_id"]: v["verdict"] for v in read_jsonl(d / "verifications.jsonl")}
    assert got == {"P-crash": "error", "P-slow": "error", "P-miss": "error", "P-na": "na", "P-pexit": "error"}, got


def check_roundtrip(tmp: Path, data: Path) -> None:
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
    for leak in ('"source"', '"solver"', '"grounding"', '"why_hard"', '"gen_key"', '"kind"', '"note"', "erdosproblems"):
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
    assert pipeline.import_human(data, f) == 11, "10 problem rows (the duplicate collapsed) + 1 solution row; R9 skipped"
    assert pipeline.import_human(data, f) == 11
    human = [r for r in read_jsonl(data / "ratings.jsonl") if r["rater_type"] == "human"]
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
             "src": ({"id": "P-0b0b0b", "statement": "s", "why_important": "See Problem #12 on the site."}, None),
             "sid": ({"id": "P-0c0c0c", "statement": "s"}, {"id": "S-opus", "problem_id": "P-0c0c0c", "text": "t"})}
    for name, (prob, sol_row) in cases.items():
        d = tmp / "leak" / name / "data"
        append_jsonl(d / "problems.jsonl", prob)
        if name == "dup":
            append_jsonl(d / "problems.jsonl", prob)
        if sol_row:
            append_jsonl(d / "solutions.jsonl", sol_row)
        try:
            pipeline.export_human(d, ["R1"])
        except SystemExit:
            assert not (d / "blind.json").exists(), f"{name}: a refused export must not write blind.json"
        else:
            raise AssertionError(f"export_human must refuse case {name!r}")
    # the page template gets the JSON with every '<' escaped, so no payload text can close the script tag
    d = tmp / "tpl" / "data"
    append_jsonl(d / "problems.jsonl", {"id": "P-0d0d0d", "statement": "x </script><!-- y"})
    (tmp / "tpl" / "eval_page").mkdir(parents=True)
    (tmp / "tpl" / "eval_page" / "template.html").write_text("<script>const B = /*BLIND_JSON*/;</script>", encoding="utf-8")
    pipeline.export_human(d, ["R1"])
    page = (tmp / "tpl" / "eval_page" / "index.html").read_text(encoding="utf-8")
    payload = page[len("<script>const B = "):-len(";</script>")]
    assert "<" not in payload and json.loads(payload)["problems"][0]["statement"] == "x </script><!-- y", page


CHECKS = [check_store, check_llm_dry, check_llm_errors, check_cli_offline, check_prompts, check_gen, check_solve,
          check_eval, check_verify, check_verify_errors, check_roundtrip]


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
