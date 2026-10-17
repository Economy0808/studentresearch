"""The one runnable check for the pipeline. `python selfcheck.py` exits non-zero on failure."""
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
                "Rate limit reached for this plan", "Not logged in. Run /login"):
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
    finally:
        llm.subprocess.run, llm.claude_exe = real_run, real_exe


CHECKS = [check_store, check_llm_dry, check_llm_errors, check_cli_offline]


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
