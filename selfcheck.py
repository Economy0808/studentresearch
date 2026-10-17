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
    bad = {"is_error": True, "result": "Failed to authenticate: OAuth session expired"}
    try:
        llm._raise_if_error(bad)
    except llm.StopRun:
        pass
    else:
        raise AssertionError("auth error must raise StopRun")


CHECKS = [check_store, check_llm_dry]


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
