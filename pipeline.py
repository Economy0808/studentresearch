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
