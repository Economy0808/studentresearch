"""CLI for the experiment pipeline. Usage: python run.py [--data-dir data] [--dry-run] [--models a,b] <cmd> ..."""
import argparse
import json
import sys
from pathlib import Path

import llm
import pipeline

PROBE_SCHEMA = {"type": "object",
                "properties": {"ok": {"type": "boolean"}, "model_name": {"type": "string"},
                               "saw_other_instructions": {"type": "boolean"}, "other_instructions_summary": {"type": "string"}},
                "required": ["ok", "model_name", "saw_other_instructions", "other_instructions_summary"]}
PROBE_PROMPT = ("Return ok=true, model_name=the model you are, saw_other_instructions=true if you received any "
                "instructions, personas, skills or project notes besides the short system prompt and this message, "
                "and summarize them in other_instructions_summary (empty string if none).")


def probe(models: list[str], data_dir: Path, dry_run: bool = False) -> None:
    for m in models:
        raw = data_dir / "raw" / "probe" / f"{m}.json"
        try:
            out = llm.call(m, pipeline.system(), PROBE_PROMPT, PROBE_SCHEMA, raw, dry_run)
            print(f"{m}: {json.dumps(out, ensure_ascii=False)}")
        except llm.CallFailed as e:
            print(f"{m}: FAILED {e}")
        if raw.exists():  # token counts expose context injected beyond the system prompt (CLAUDE.md, skills, memory)
            cli = json.loads(raw.read_text(encoding="utf-8"))["cli_output"]
            u = cli.get("usage") or {}
            print(f"  modelUsage={list(cli.get('modelUsage') or {})} input_tokens={u.get('input_tokens')} "
                  f"cache_read_input_tokens={u.get('cache_read_input_tokens')} "
                  f"cache_creation_input_tokens={u.get('cache_creation_input_tokens')}")


def report(a, n: int) -> None:
    print(f"{a.cmd}: {n} new record(s) in {a.data_dir}")
    fails = a.data_dir / "failures.jsonl"
    if fails.exists():
        print(f"note: failures were recorded in {fails}; rerunning retries them")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="AI problem generation / solving / evaluation pipeline")
    ap.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parent / "data")
    ap.add_argument("--dry-run", action="store_true", help="use the fake model; no CLI calls")
    ap.add_argument("--models", default=",".join(llm.MODELS), help="comma-separated model aliases")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen", help="generate problems: context × models × n")
    g.add_argument("--context", type=Path, required=True)
    g.add_argument("--kind", choices=["open", "checkable"], required=True)
    g.add_argument("--n", type=int, default=5)
    sv = sub.add_parser("solve", help="every problem (incl. human_problems.jsonl) × every model")
    sv.add_argument("--only", help="comma-separated problem ids: solve just these, in this order")
    sub.add_parser("eval", help="AI raters score every problem and solution, one item per call")
    sub.add_parser("verify", help="run REVIEWED checkers on submitted candidates")
    e = sub.add_parser("export-human", help="write data/blind.json (+ eval_page/index.html if template exists)")
    e.add_argument("--extra-data-dir", type=Path, action="append", default=[],
                   help="also mix this data folder (e.g. the high-context one) into the same blind export")
    e.add_argument("--raters", default="R1,R2,R3,R4,R5", help="allowed evaluator codes")
    i = sub.add_parser("import-human", help="merge a JSON file downloaded from the evaluation page")
    i.add_argument("file", type=Path)
    sub.add_parser("probe", help="one tiny live call per model; checks auth, aliases and leaked context")
    sub.add_parser("selfcheck", help="run the offline self-check")
    return ap


def main(argv=None) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # the console may be cp949; model text is UTF-8
    ap = build_parser()
    a = ap.parse_args(argv)
    models = [m.strip() for m in a.models.split(",") if m.strip()]
    bad = [m for m in models if m not in llm.GRADE]
    if bad:
        ap.error(f"unknown model alias(es) {bad}; allowed: {list(llm.GRADE)}")
    if a.dry_run and a.data_dir.resolve().parent == Path(__file__).resolve().parent:
        ap.error("--dry-run must not touch the real dataset or its sibling folders: use --data-dir tmp_dry/data")
    hp = a.data_dir.resolve().parent / "human_problems.jsonl"
    if a.cmd in ("solve", "eval", "export-human") and not hp.exists():
        print(f"warning: {hp} not found; no human control problems will be included")
    try:
        if a.cmd == "gen":
            report(a, pipeline.gen(a.data_dir, a.context, a.kind, a.n, models, a.dry_run))
        elif a.cmd == "solve":
            only = [x.strip() for x in a.only.split(",") if x.strip()] if a.only is not None else None
            report(a, pipeline.solve(a.data_dir, models, a.dry_run, only))
        elif a.cmd == "eval":
            report(a, pipeline.eval_ai(a.data_dir, models, a.dry_run))
        elif a.cmd == "verify":
            report(a, pipeline.verify(a.data_dir))
        elif a.cmd == "export-human":
            print(pipeline.export_human(a.data_dir, [r.strip() for r in a.raters.split(",") if r.strip()], a.extra_data_dir))
        elif a.cmd == "import-human":
            report(a, pipeline.import_human(a.data_dir, a.file))
        elif a.cmd == "probe":
            probe(models, a.data_dir, a.dry_run)
        elif a.cmd == "selfcheck":
            import selfcheck
            selfcheck.main()
    except llm.StopRun as e:
        raise SystemExit(f"STOPPED: {e}\n"
                         "If this is a login or usage-limit problem: run `claude` and /login, or wait for the usage "
                         "window, then rerun the same command; finished items are kept.")


if __name__ == "__main__":
    main()
