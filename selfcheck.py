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
    assert row["source"] == "human" and row["id"].startswith("P-h"), row
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


CHECKS = [check_store, check_llm_dry, check_llm_errors, check_cli_offline, check_prompts, check_gen]


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
