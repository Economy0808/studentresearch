"""The one runnable check for the pipeline. `python selfcheck.py` exits non-zero on failure."""
import shutil
import sys
import tempfile
from pathlib import Path

from store import append_jsonl, new_id, read_jsonl, write_jsonl


def check_store(tmp: Path, data: Path) -> None:
    p = tmp / "x.jsonl"
    append_jsonl(p, {"a": 1, "k": "한글"})
    append_jsonl(p, {"a": 2})
    assert read_jsonl(p) == [{"a": 1, "k": "한글"}, {"a": 2}], read_jsonl(p)
    assert "한글" in p.read_text(encoding="utf-8"), "must not escape non-ASCII"
    write_jsonl(p, [{"a": 3}])
    assert read_jsonl(p) == [{"a": 3}]
    assert read_jsonl(tmp / "missing.jsonl") == []
    i = new_id("P")
    assert i.startswith("P-") and len(i) == 8, i


CHECKS = [check_store]


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
