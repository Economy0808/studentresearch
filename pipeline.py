"""The experiment stages as pure functions over a data_dir. Project files hang off data_dir.parent."""
import json
import re
import subprocess
import sys
from pathlib import Path

import llm
from store import append_jsonl, new_id, now, read_jsonl, write_jsonl

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"

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
    """Replace {key} tokens one by one; str.format is avoided because LaTeX uses braces."""
    for k, v in values.items():
        template = template.replace("{" + k + "}", "" if v is None else str(v))
    return template


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
    return read_jsonl(data_dir / "problems.jsonl") + read_jsonl(data_dir.parent / "human_problems.jsonl")


def record_failure(data_dir: Path, stage: str, target_id: str, model: str, err: Exception) -> None:
    append_jsonl(data_dir / "failures.jsonl", {"stage": stage, "target_id": target_id, "model": model,
                                               "error": str(err)[:1000], "created_at": now()})


def gen(data_dir: Path, context_path: Path, kind: str, n: int, models=llm.MODELS, dry_run: bool = False) -> int:
    if kind not in ("open", "checkable"):
        raise ValueError(kind)
    text, results = parse_context(context_path)
    context_id = context_path.stem
    template = load_prompt(f"gen_{kind}.md")
    schema = _schema(GEN_PROPS | (CHECKABLE_PROPS if kind == "checkable" else {}))
    problems_path = data_dir / "problems.jsonl"
    done = {p.get("gen_key") for p in read_jsonl(problems_path)}
    made = 0
    for model in models:
        for i in range(n):
            key = f"{context_id}:{kind}:{model}:{i}"
            if key in done:
                continue
            focus = results[i % len(results)]
            prompt = fill(template, context=text, focus=focus)
            raw = data_dir / "raw" / "gen" / (key.replace(":", "_") + ".json")
            try:
                out = llm.call(model, system(), prompt, schema, raw, dry_run)
            except llm.CallFailed as e:
                record_failure(data_dir, "gen", key, model, e)
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


def solve(data_dir: Path, models=llm.MODELS, dry_run: bool = False) -> int:
    template = load_prompt("solve.md")
    schema = _schema(SOLVE_PROPS)
    sol_path = data_dir / "solutions.jsonl"
    done = {(s["problem_id"], s["solver"]) for s in read_jsonl(sol_path)}
    made = 0
    for p in all_problems(data_dir):
        for model in models:
            if (p["id"], model) in done:
                continue
            prompt = fill(template, statement=p["statement"], finite_form=p.get("finite_form"),
                          candidate_format=p.get("candidate_format"))
            raw = data_dir / "raw" / "solve" / f"{p['id']}_{model}.json"
            try:
                out = llm.call(model, system(), prompt, schema, raw, dry_run)
            except llm.CallFailed as e:
                record_failure(data_dir, "solve", p["id"], model, e)
                continue
            append_jsonl(sol_path, {"id": new_id("S"), "problem_id": p["id"], "solver": model,
                                    **{k: out[k] for k in SOLVE_PROPS}, "created_at": now()})
            made += 1
    return made


def eval_ai(data_dir: Path, models=llm.MODELS, dry_run: bool = False) -> int:
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
        try:
            out = llm.call(model, system(), prompt, _schema(props), raw, dry_run)
        except llm.CallFailed as e:
            record_failure(data_dir, "eval", target_id, model, e)
            return
        append_jsonl(ratings_path, {"rater": model, "rater_type": "ai", "target_type": target_type,
                                    "target_id": target_id, **{k: out[k] for k in props}, "created_at": now()})
        made += 1

    for p in problems.values():
        prompt = fill(t_prob, statement=p["statement"], finite_form=p.get("finite_form"),
                      why_important=p.get("why_important"))
        for model in models:
            if (model, "problem", p["id"]) not in done:
                rate(model, "problem", p["id"], prompt, EVAL_PROBLEM_PROPS)
    for s in read_jsonl(data_dir / "solutions.jsonl"):
        p = problems.get(s["problem_id"])
        if p is None:
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
        if s["id"] in done:
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
                r = subprocess.run([sys.executable, "-I", str(runner), str(checker), str(cand)],
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


def export_human(data_dir: Path, raters: list[str]) -> Path:
    problems = all_problems(data_dir)
    ids = [p["id"] for p in problems]
    bad = [i for i in ids if not re.fullmatch(r"P-[0-9a-f]{6}", str(i))]
    if bad or len(set(ids)) != len(ids):
        raise SystemExit(f"export-human refused: problem ids must be unique and look like P-xxxxxx (6 hex); offending: {bad or 'duplicates'}. "
                         "Generate ids with: python -c \"from store import new_id; print(new_id('P'))\"")
    leaky = [p["id"] for p in problems if re.search(r"erdosproblems|https?://|problem\s*#?\s*\d+", p.get("why_important") or "", re.I)]
    if leaky:
        raise SystemExit(f"export-human refused: why_important names a source (erdosproblems/URL/'problem #N') in {leaky}; move it to the note field")
    sols_all = read_jsonl(data_dir / "solutions.jsonl")
    bad_s = [s["id"] for s in sols_all if not re.fullmatch(r"S-[0-9a-f]{6}", str(s["id"]))]
    if bad_s:
        raise SystemExit(f"export-human refused: solution ids must look like S-xxxxxx; offending: {bad_s}")
    sols: dict[str, list[dict]] = {}
    for s in sols_all:
        sols.setdefault(s["problem_id"], []).append({"id": s["id"], "text": s["text"], "candidate": s.get("candidate")})
    for v in sols.values():
        v.sort(key=lambda x: x["id"])  # file order is solver order; blind.json must not carry it
    blind = {"generated_at": now(), "raters": raters, "rubric_md": load_prompt("rubric.md"),
             "problems": sorted([{"id": p["id"], "statement": p["statement"],
                                  "why_important": p.get("why_important") or "",
                                  "finite_form": p.get("finite_form"),
                                  "solutions": sols.get(p["id"], [])}
                                 for p in problems], key=lambda x: x["id"])}
    out = data_dir / "blind.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(blind, ensure_ascii=False, indent=1), encoding="utf-8")
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
    allowed = set(json.loads(blind_path.read_text(encoding="utf-8"))["raters"])
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
        clean[(row["rater"], row["target_type"], row["target_id"])] = row
    keys = set(clean)
    clean = list(clean.values())
    ratings_path = data_dir / "ratings.jsonl"
    kept = [e for e in read_jsonl(ratings_path)
            if not (e["rater_type"] == "human" and (e["rater"], e["target_type"], e["target_id"]) in keys)]
    write_jsonl(ratings_path, kept + clean)
    return len(clean)
