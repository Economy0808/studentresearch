"""The experiment stages as pure functions over a data_dir. Project files hang off data_dir.parent."""
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import llm
from store import append_jsonl, new_id, now, read_jsonl, write_jsonl

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"
TIME_BUDGET_ATTEMPTS = 2  # exhausted solve attempts (timeout or output-token overflow) per (problem, solver) before the cell is recorded as unsolved
# Excluded 2026-10-29: the finite instances of these two generated checkable problems were found provably impossible.
# Their rows stay in the data files; every stage, status.py and analyze.py skip them (all_problems drops them).
EXCLUDED_PROBLEMS = {"P-fdf0ff", "P-2e0477"}


def is_budget_error(error) -> bool:
    """A failure that counts as an exhausted solve attempt: our per-call timeout, or the API's output-token overflow."""
    e = str(error or "")
    return e.startswith(llm.TIMEOUT_PREFIX) or "output token maximum" in e


_STR = {"type": "string"}
_SCORE = {"type": ["integer", "null"], "minimum": 1, "maximum": 5}
GEN_PROPS = {"statement": _STR, "grounding": _STR, "why_hard": _STR, "why_important": _STR,
             "resembles_known": {"type": ["string", "null"]},
             "novelty_confidence": {"type": "number", "minimum": 0, "maximum": 1}}
CHECKABLE_PROPS = {"finite_form": _STR, "candidate_format": _STR, "checker_code": _STR}
SOLVE_PROPS = {"text": _STR,
               "claimed_status": {"type": "string", "enum": ["solved", "partial", "unsolved"]},
               "candidate": {"type": ["array", "object", "string", "number", "null"]}}
EVAL_PROBLEM_PROPS = {"clarity": _SCORE, "difficulty": _SCORE, "want_to_solve": _SCORE,
                      "richness_list": {"type": "array", "items": _STR},
                      "known_problem": {"type": ["boolean", "null"]}}
EVAL_SOLUTION_PROPS = {"correctness": _SCORE, "clarity_sol": _SCORE,
                       "understandable": {"type": ["boolean", "null"]}}


def _schema(props: dict) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def load_prompt(name: str) -> str:
    return (PROMPTS / name).read_text(encoding="utf-8")


def fill(template: str, **values) -> str:
    """Replace {key} tokens in one pass (inserted text is never rescanned); unknown tokens stay; str.format is avoided because LaTeX uses braces."""
    return re.sub(r"\{([a-z_]+)\}", lambda m: ("" if values.get(m.group(1)) is None else str(values[m.group(1)]))
                  if m.group(1) in values else m.group(0), template)


def system() -> str:
    return load_prompt("system.md").strip()


def parse_context(path: Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    scan = re.sub(r"^(```|~~~)[^`\n]*$.*?^\1[ \t]*$", "", text, flags=re.M | re.S)  # fenced examples (see context/README.md) are not sections
    results = [m.group(1).strip() for m in re.finditer(r"^## (Result:.*)$", scan, flags=re.M)]
    if not results:
        raise SystemExit(f"{path}: no '## Result:' sections; see context/README.md")
    return text, results


def all_problems(data_dir: Path) -> list[dict]:
    rows = read_jsonl(data_dir / "problems.jsonl") + read_jsonl(data_dir.parent / "human_problems.jsonl")
    ids = [p["id"] for p in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"duplicate problem ids across problems.jsonl and human_problems.jsonl: {dup}")
    return [p for p in rows if p["id"] not in EXCLUDED_PROBLEMS]


def check_one_row_per_cell(data_dir: Path) -> None:
    cells = Counter((s["problem_id"], s.get("solver")) for s in read_jsonl(data_dir / "solutions.jsonl"))
    dup = sorted((c for c, n in cells.items() if n > 1), key=str)
    if dup:
        raise SystemExit(f"solutions.jsonl has more than one row for the same (problem_id, solver): {dup}; fix the file first")


def record_failure(data_dir: Path, stage: str, target_id: str, model: str, err: Exception) -> None:
    append_jsonl(data_dir / "failures.jsonl", {"stage": stage, "target_id": target_id, "model": model,
                                               "error": str(err)[:1000], "created_at": now()})


def call_recorded(data_dir: Path, stage: str, target_id: str, model: str, *args):
    """llm.call that writes every failure to failures.jsonl; a single failure returns None, a StopRun still propagates."""
    try:
        return llm.call(model, *args)
    except llm.CallFailed as e:
        record_failure(data_dir, stage, target_id, model, e)
    except llm.StopRun as e:
        if e.last_error:  # the breaker's 5th failure: record the underlying error, not the wrapper text
            record_failure(data_dir, stage, target_id, model, llm.CallFailed(e.last_error))
        raise


def gen(data_dir: Path, context_path: Path, kind: str, n: int, models=llm.MODELS, dry_run: bool = False) -> int:
    if kind not in ("open", "checkable"):
        raise ValueError(kind)
    text, results = parse_context(context_path)
    context_id = f"{context_path.stem}-{hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]}"  # editing the pack restarts generation
    template = load_prompt(f"gen_{kind}.md")
    schema = _schema(GEN_PROPS | (CHECKABLE_PROPS if kind == "checkable" else {}))
    problems_path = data_dir / "problems.jsonl"
    done = {p.get("gen_key") for p in read_jsonl(problems_path)}
    made = 0
    for i in range(n):  # item-major, so a partial run stays balanced across models
        for model in models:
            key = f"{context_id}:{kind}:{model}:{i}"
            if key in done:
                continue
            focus = results[i % len(results)]
            prompt = fill(template, context=text, focus=focus)
            raw = data_dir / "raw" / "gen" / (key.replace(":", "_") + ".json")
            out = call_recorded(data_dir, "gen", key, model, system(), prompt, schema, raw, dry_run)
            if out is None:
                continue
            if kind == "checkable" and not all(isinstance(out.get(k), str) and out[k].strip() for k in CHECKABLE_PROPS):
                record_failure(data_dir, "gen", key, model, ValueError("checkable fields must be non-empty strings"))
                continue
            row = {"id": new_id("P"), "source": model, "kind": kind, "context_id": context_id,
                   "focus": focus, "gen_key": key}
            row.update({k: None for k in CHECKABLE_PROPS})
            row.update({k: out[k] for k in schema["properties"]})
            row["created_at"] = now()
            if kind == "checkable":
                _write_checker(data_dir, row)  # before the row: a crash here leaves a stray file, never a row without a checker
            append_jsonl(problems_path, row)
            made += 1
    return made


def _write_checker(data_dir: Path, p: dict) -> None:
    cdir = data_dir.parent / "checkers"
    cdir.mkdir(parents=True, exist_ok=True)
    one_line = lambda s: " ".join(str(s or "").split())[:300]
    header = ("# UNREVIEWED: read this file; if it correctly tests finite_form, replace this first line with exactly '# REVIEWED'.\n"
              f"# problem {p['id']} (generated by {p['source']}): {one_line(p['statement'])}\n"
              f"# finite_form: {one_line(p['finite_form'])}\n"
              f"# candidate_format: {one_line(p['candidate_format'])}\n\n")
    (cdir / f"{p['id']}.py").write_text(header + p["checker_code"], encoding="utf-8")


def solve(data_dir: Path, models=llm.MODELS, dry_run: bool = False, only: list[str] | None = None) -> int:
    template = load_prompt("solve.md")
    schema = _schema(SOLVE_PROPS)
    sol_path = data_dir / "solutions.jsonl"
    done = {(s["problem_id"], s["solver"]) for s in read_jsonl(sol_path)}
    timeouts = Counter((f["target_id"], f["model"]) for f in read_jsonl(data_dir / "failures.jsonl")
                       if f.get("stage") == "solve" and is_budget_error(f.get("error")))
    probs = all_problems(data_dir)
    if only is not None:  # --only: just these problems, in the order given (and no re-sorting below)
        by_id = {p["id"]: p for p in probs}
        unknown = [i for i in only if i not in by_id]
        if unknown:
            raise SystemExit(f"--only has problem id(s) not among the valid problems: {unknown}")
        probs = [by_id[i] for i in dict.fromkeys(only)]
    cells = [(p, m) for p in probs for m in models if (p["id"], m) not in done]
    # untried cells first (stable sort keeps problem order); cells that already owe a budget row go first because they cost no call
    if only is None:
        cells.sort(key=lambda c: n if (n := timeouts[(c[0]["id"], c[1])]) < TIME_BUDGET_ATTEMPTS else -1)
    made = 0
    for p, model in cells:
        if timeouts[(p["id"], model)] >= TIME_BUDGET_ATTEMPTS:
            # budget rule: after 2 exhausted attempts (timeout / output-token overflow) the cell is recorded as unsolved and never retried
            append_jsonl(sol_path, {"id": new_id("S"), "problem_id": p["id"], "solver": model,
                                    "text": f"[pipeline] No answer within the budget ({TIME_BUDGET_ATTEMPTS} attempts, each ending in a {llm.CALL_TIMEOUT} s timeout or an output-token overflow). This row was written by the pipeline, not by the model.",
                                    "claimed_status": "unsolved", "candidate": None, "budget_exceeded": True,
                                    "created_at": now()})
            made += 1
            continue
        prompt = fill(template, statement=p["statement"], finite_form=p.get("finite_form"),
                      candidate_format=p.get("candidate_format"))
        raw = data_dir / "raw" / "solve" / f"{p['id']}_{model}.json"
        out = call_recorded(data_dir, "solve", p["id"], model, system(), prompt, schema, raw, dry_run)
        if out is None:
            continue
        if out["claimed_status"] not in SOLVE_PROPS["claimed_status"]["enum"]:
            record_failure(data_dir, "solve", p["id"], model, ValueError("claimed_status out of range"))
            continue
        append_jsonl(sol_path, {"id": new_id("S"), "problem_id": p["id"], "solver": model,
                                **{k: out[k] for k in SOLVE_PROPS}, "created_at": now()})
        made += 1
    return made


def eval_ai(data_dir: Path, models=llm.MODELS, dry_run: bool = False) -> int:
    check_one_row_per_cell(data_dir)
    rubric = load_prompt("rubric.md")
    t_prob = fill(load_prompt("eval_problem.md"), rubric=rubric)
    t_sol = fill(load_prompt("eval_solution.md"), rubric=rubric)
    ratings_path = data_dir / "ratings.jsonl"
    done = {(r["rater"], r["target_type"], r["target_id"])
            for r in read_jsonl(ratings_path) if r["rater_type"] == "ai"}
    problems = {p["id"]: p for p in all_problems(data_dir)}
    made = 0

    def rate(model: str, target_type: str, target_id: str, prompt: str, props: dict) -> None:
        nonlocal made
        raw = data_dir / "raw" / "eval" / f"{target_id}_{model}.json"
        out = call_recorded(data_dir, "eval", target_id, model, system(), prompt, _schema(props), raw, dry_run)
        if out is None:
            return
        append_jsonl(ratings_path, {"rater": model, "rater_type": "ai", "target_type": target_type,
                                    "target_id": target_id, **{k: _clean_field(k, out[k]) for k in props}, "created_at": now()})
        made += 1

    for p in problems.values():
        prompt = fill(t_prob, statement=p["statement"], finite_form=p.get("finite_form"))
        for model in models:
            if (model, "problem", p["id"]) not in done:
                rate(model, "problem", p["id"], prompt, EVAL_PROBLEM_PROPS)
    for s in read_jsonl(data_dir / "solutions.jsonl"):
        p = problems.get(s["problem_id"])
        if p is None or s.get("budget_exceeded"):  # pipeline-written rows are not solutions: nothing to rate
            continue
        cand = s.get("candidate")
        prompt = fill(t_sol, statement=p["statement"], finite_form=p.get("finite_form"), text=s["text"],
                      candidate=json.dumps(cand, ensure_ascii=False) if cand is not None else None)
        for model in models:
            if (model, "solution", s["id"]) not in done:
                rate(model, "solution", s["id"], prompt, EVAL_SOLUTION_PROPS)
    return made


def verify(data_dir: Path, timeout: int = 60) -> int:
    problems = {p["id"]: p for p in all_problems(data_dir)}
    ver_path = data_dir / "verifications.jsonl"
    done = {v["solution_id"] for v in read_jsonl(ver_path)}
    cdir = data_dir.parent / "checkers"
    runner = ROOT / "checker_runner.py"
    made = 0
    for s in read_jsonl(data_dir / "solutions.jsonl"):
        if s["id"] in done or s.get("budget_exceeded"):  # pipeline-written rows are not solutions (same rule as eval)
            continue
        p = problems.get(s["problem_id"])
        if not p or p.get("kind") != "checkable":
            continue
        checker = cdir / f"{p['id']}.py"
        if s.get("candidate") is None:
            verdict, log = "na", "solution submitted no candidate"
        elif not checker.exists():
            verdict, log = "error", f"checker file missing: {checker}"
        elif (checker.read_text(encoding="utf-8-sig", errors="replace").splitlines() or [""])[0].strip() != "# REVIEWED":
            print(f"skip {s['id']}: {checker.name} is not marked '# REVIEWED'")
            continue
        else:
            cand = data_dir / "raw" / "verify" / f"{s['id']}_candidate.json"
            cand.parent.mkdir(parents=True, exist_ok=True)
            cand.write_text(json.dumps(s["candidate"], ensure_ascii=False), encoding="utf-8")
            try:
                # ponytail: on Windows a grandchild process can hold the pipes past the timeout; reviewed checkers must not spawn processes
                r = subprocess.run([sys.executable, "-I", "-X", "utf8", str(runner), str(checker), str(cand)],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   timeout=timeout, cwd=cand.parent)
                last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
                verdict = {"PASS": "pass", "FAIL": "fail"}.get(last, "error") if r.returncode == 0 else "error"
                log = (r.stdout + r.stderr)[-2000:]
            except subprocess.TimeoutExpired:
                verdict, log = "error", f"timeout after {timeout}s"
        append_jsonl(ver_path, {"solution_id": s["id"], "problem_id": p["id"], "verdict": verdict,
                                "log": log, "created_at": now()})
        made += 1
    return made


def export_human(data_dir: Path, raters: list[str], extra_dirs: list[Path] = ()) -> Path:
    """extra_dirs (e.g. the high-context data folder) are mixed into the same blind export; the folder of each target
    goes to blind_sources.json, which import-human uses to route ratings and which the rating page never sees."""
    dirs = [data_dir, *extra_dirs]
    for d in dirs:
        check_one_row_per_cell(d)
    problems = [p for d in dirs for p in all_problems(d)] if extra_dirs else all_problems(data_dir)
    ids = [p["id"] for p in problems]
    bad = [i for i in ids if not re.fullmatch(r"P-[0-9a-f]{6}", str(i))]
    if bad or len(set(ids)) != len(ids):
        raise SystemExit(f"export-human refused: problem ids must be unique and look like P-xxxxxx (6 hex); offending: {bad or 'duplicates'}. "
                         "Generate ids with: python -c \"from store import new_id; print(new_id('P'))\"")
    sols_all = [s for d in dirs for s in read_jsonl(d / "solutions.jsonl")]
    if len(set(s["id"] for s in sols_all)) != len(sols_all):
        raise SystemExit("export-human refused: duplicate solution ids")
    bad_s = [s["id"] for s in sols_all if not re.fullmatch(r"S-[0-9a-f]{6}", str(s["id"]))]
    if bad_s:
        raise SystemExit(f"export-human refused: solution ids must look like S-xxxxxx; offending: {bad_s}")
    sols: dict[str, list[dict]] = {}
    for s in sols_all:
        if s.get("budget_exceeded"):  # pipeline-written row, not a solution: raters never see it
            continue
        sols.setdefault(s["problem_id"], []).append({"id": s["id"], "text": s["text"], "candidate": s.get("candidate")})
    for v in sols.values():
        v.sort(key=lambda x: x["id"])  # file order is solver order; blind.json must not carry it
    blind = {"generated_at": now(), "raters": raters, "rubric_md": load_prompt("rubric.md"),
             "problems": sorted([{"id": p["id"], "statement": p["statement"],
                                  "finite_form": p.get("finite_form"),
                                  "solutions": sols.get(p["id"], [])}
                                 for p in problems], key=lambda x: x["id"])}
    out = data_dir / "blind.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(blind, ensure_ascii=False, indent=1), encoding="utf-8")
    src_path = data_dir / "blind_sources.json"
    if extra_dirs:
        owner = {p["id"]: d for d in dirs for p in all_problems(d)}  # controls come from data_dir's parent, so data_dir owns them
        owner |= {s["id"]: d for d in dirs for s in read_jsonl(d / "solutions.jsonl")}
        src_path.write_text(json.dumps({i: str(d.resolve()) for i, d in owner.items()}, indent=1), encoding="utf-8")
    elif src_path.exists():
        src_path.unlink()
    tpl = data_dir.parent / "eval_page" / "template.html"
    if tpl.exists():
        payload = json.dumps(blind, ensure_ascii=False).replace("<", "\\u003c")
        (tpl.parent / "index.html").write_text(tpl.read_text(encoding="utf-8").replace("/*BLIND_JSON*/", payload),
                                               encoding="utf-8")
    return out


HUMAN_FIELDS = {"problem": ("clarity", "difficulty", "want_to_solve", "richness_list", "known_problem"),
                "solution": ("correctness", "clarity_sol", "understandable")}
SCORE_FIELDS = {"clarity", "difficulty", "want_to_solve", "correctness", "clarity_sol"}
GUESSES = {"human", "ai_low", "ai_mid", "ai_high", "unknown"}


def _clean_field(k: str, v):
    if k in SCORE_FIELDS:
        return v if type(v) is int and 1 <= v <= 5 else None
    if k == "richness_list":
        return [x.strip() for x in v if isinstance(x, str) and x.strip()] if isinstance(v, list) else []
    if k in ("known_problem", "understandable"):
        return v if isinstance(v, bool) else None
    return v


def import_human(data_dir: Path, path: Path) -> int:
    blind_path = data_dir / "blind.json"
    if not blind_path.exists():
        raise SystemExit("run export-human first: data/blind.json not found")
    rows = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("ratings", [])
    blind = json.loads(blind_path.read_text(encoding="utf-8"))
    allowed = set(blind["raters"])
    known = {p["id"] for p in blind["problems"]} | {s["id"] for p in blind["problems"] for s in p["solutions"]}
    clean: dict[tuple, dict] = {}  # keyed so a duplicate row inside one file collapses; the last one wins
    for r in rows:
        if not isinstance(r, dict):
            print("skip: row is not an object")
            continue
        if not isinstance(r.get("rater"), str) or r["rater"] not in allowed:
            print(f"skip: rater {r.get('rater')!r} is not in blind.json raters")
            continue
        if (not isinstance(r.get("target_type"), str) or r["target_type"] not in HUMAN_FIELDS
                or not isinstance(r.get("target_id"), str) or not r["target_id"]):
            print(f"skip: malformed row {str(r)[:120]}")
            continue
        row = {"rater": r["rater"], "rater_type": "human", "target_type": r["target_type"], "target_id": r["target_id"]}
        for k in HUMAN_FIELDS[r["target_type"]]:
            row[k] = _clean_field(k, r.get(k))
        row["source_guess"] = r["source_guess"] if isinstance(r.get("source_guess"), str) and r["source_guess"] in GUESSES else None
        row["created_at"] = r.get("created_at") if isinstance(r.get("created_at"), str) and r.get("created_at") else now()
        if row["target_id"] not in known:
            print(f"warning: target_id {row['target_id']!r} is not in blind.json (stale export?); row kept")
        clean[(row["rater"], row["target_type"], row["target_id"])] = row
    src_path = data_dir / "blind_sources.json"
    owner = {i: Path(d) for i, d in json.loads(src_path.read_text(encoding="utf-8")).items()} if src_path.exists() else {}
    by_dir: dict[Path, dict] = {}
    for k, row in clean.items():  # each rating goes to the folder that owns its target (export-human --extra-data-dir)
        by_dir.setdefault(owner.get(row["target_id"], data_dir), {})[k] = row
    replaced = 0
    for d, part in by_dir.items():
        ratings_path = d / "ratings.jsonl"
        old = read_jsonl(ratings_path)
        replaced += len(set(part) & {(e["rater"], e["target_type"], e["target_id"]) for e in old if e["rater_type"] == "human"})
        kept = [e for e in old if not (e["rater_type"] == "human" and (e["rater"], e["target_type"], e["target_id"]) in part)]
        write_jsonl(ratings_path, kept + list(part.values()))
    print(f"import-human: {len(clean) - replaced} new, {replaced} replaced")
    return len(clean)
