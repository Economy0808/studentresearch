"""Progress snapshot for the dashboard: data/progress.json, one row per (stage, item, model)."""
import json
import sys
from pathlib import Path

import llm
from pipeline import all_problems, is_budget_error
from store import now, read_jsonl

ROOT = Path(__file__).resolve().parent
D = ROOT / "data"


def main() -> None:
    probs = all_problems(D)
    kind = {p["id"]: p["kind"] for p in probs}
    sols = [s for s in read_jsonl(D / "solutions.jsonl") if s["problem_id"] in kind]  # all_problems already dropped EXCLUDED_PROBLEMS
    fails = read_jsonl(D / "failures.jsonl")
    ratings = read_jsonl(D / "ratings.jsonl")
    vers = read_jsonl(D / "verifications.jsonl")
    fail_by: dict[tuple, list] = {}
    for f in fails:
        fail_by.setdefault((f["stage"], f["target_id"], f["model"]), []).append(f)
    snap = now()
    rows = []

    def add(**r):
        rows.append({"snapshot_at": snap, "budget_tries": 0, "note": "", "at": "", **r})

    for p in probs:  # gen: every generated problem is a finished cell
        if p["source"] in llm.MODELS:
            add(stage="gen", item=p["id"], kind=p["kind"], source=p["source"], model=p["source"],
                status="done", attempts=1, at=p["created_at"])

    done = {(s["problem_id"], s["solver"]): s for s in sols}
    for p in probs:
        for m in llm.MODELS:
            s = done.get((p["id"], m))
            fl = fail_by.get(("solve", p["id"], m), [])
            if s and s.get("budget_exceeded"):
                st, note, at = "budget", "예산 초과(두 번 소진)", s["created_at"]
            elif s:
                st, note, at = "done", s["claimed_status"], s["created_at"]
            elif fl:
                st, note, at = "retry", fl[-1]["error"][:90], fl[-1]["created_at"]
            else:
                st, note, at = "pending", "", ""
            add(stage="solve", item=p["id"], kind=p["kind"], source=p["source"], model=m, status=st,
                attempts=len(fl) + (1 if st == "done" else 0),
                budget_tries=sum(is_budget_error(f["error"]) for f in fl), note=note, at=at)

    rated = {(r["rater"], r["target_id"]) for r in ratings if r.get("rater_type") == "ai"}
    targets = [("problem", p["id"], p["kind"], p["source"]) for p in probs] + \
              [("solution", s["id"], kind[s["problem_id"]], s["solver"]) for s in sols if not s.get("budget_exceeded")]
    for tt, tid, k, src in targets:
        for m in llm.MODELS:
            fl = fail_by.get(("eval", tid, m), [])
            st = "done" if (m, tid) in rated else ("retry" if fl else "pending")
            add(stage="eval", item=f"{tt}:{tid}", kind=k, source=src, model=m, status=st,
                attempts=len(fl) + (st == "done"), note=fl[-1]["error"][:90] if fl and st != "done" else "",
                at=fl[-1]["created_at"] if fl and st != "done" else "")

    reviewed = {f.stem for f in (ROOT / "checkers").glob("P-*.py")
                if f.read_text(encoding="utf-8-sig").startswith("# REVIEWED")}
    vd = {v["solution_id"]: v for v in vers}
    for s in sols:
        if kind[s["problem_id"]] == "checkable" and s["problem_id"] in reviewed and not s.get("budget_exceeded"):
            v = vd.get(s["id"])
            add(stage="verify", item=s["id"], kind="checkable", source=s["problem_id"], model=s["solver"],
                status="done" if v else "pending", attempts=1 if v else 0,
                note=str(v.get("verdict")) if v else "", at=v.get("created_at", "") if v else "")

    (D / "progress.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    for stage in ("gen", "solve", "eval", "verify"):
        per = {m: sum(1 for r in rows if r["stage"] == stage and r["model"] == m and r["status"] in ("done", "budget"))
               for m in llm.MODELS}
        tot = sum(1 for r in rows if r["stage"] == stage)
        print(f"{stage:6} {sum(per.values())}/{tot} {per}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
