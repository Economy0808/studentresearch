"""Model call layer: one function, two backends (Claude Code CLI or a deterministic fake)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

from store import now

MODELS = ["sonnet", "opus", "fable"]
GRADE = {"sonnet": 1, "opus": 2, "fable": 3}
STOP_MARKERS = ("limit", "authenticate", "oauth", "quota", "log in", "login", "credit")


class StopRun(Exception):
    """Auth or usage-limit failure: abort the whole run instead of burning the queue."""


class CallFailed(Exception):
    """One call failed; the caller records it in failures.jsonl and moves on."""


def claude_exe() -> str:
    found = shutil.which("claude")
    if not found:
        raise StopRun("claude CLI not found on PATH")
    native = Path(found).parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    return str(native) if native.exists() else found


def call(model: str, system: str, prompt: str, schema: dict, raw_path: Path, dry_run: bool = False) -> dict:
    started = now()
    if dry_run:
        out = fake(model, schema, prompt)
    else:
        out = _cli(model, system, prompt, schema, raw_path.parent.parent / "_cwd")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps({"model": model, "system": system, "prompt": prompt, "schema": schema,
                                    "started_at": started, "finished_at": now(), "cli_output": out},
                                   ensure_ascii=False, indent=1), encoding="utf-8")
    _raise_if_error(out)
    data = out.get("structured_output")
    if data is None:
        try:
            data = json.loads(out.get("result") or "")
        except (TypeError, json.JSONDecodeError):
            raise CallFailed("no structured_output and result is not JSON")
    return data


def _raise_if_error(out: dict) -> None:
    if not out.get("is_error"):
        return
    msg = str(out.get("result", out))
    if any(m in msg.lower() for m in STOP_MARKERS):
        raise StopRun(msg)
    raise CallFailed(msg)


def _cli(model: str, system: str, prompt: str, schema: dict, cwd: Path) -> dict:
    cwd.mkdir(parents=True, exist_ok=True)
    cmd = [claude_exe(), "-p", "--model", model, "--output-format", "json",
           "--json-schema", json.dumps(schema), "--tools", "", "--system-prompt", system,
           "--setting-sources", "project", "--no-session-persistence"]
    try:
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                           cwd=cwd, timeout=1800)
    except subprocess.TimeoutExpired:
        return {"is_error": True, "result": "timeout after 1800s"}
    if not p.stdout.strip():
        return {"is_error": True, "result": f"empty stdout; stderr: {p.stderr[-800:]}"}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"is_error": True, "result": f"non-JSON stdout: {p.stdout[:800]}"}


def _gen_grade(prompt: str) -> int:
    """Fake problems carry '[fake <model>]' in their statement; recover the generator's grade from it."""
    m = re.search(r"\[fake (\w+)\]", prompt)
    return GRADE.get(m.group(1), 2) if m else 2


def fake(model: str, schema: dict, prompt: str) -> dict:
    """Deterministic schema-shaped answers. Higher generator grade → longer richness list; a solver
    succeeds only on problems from a strictly lower grade. analyze() has an order to check."""
    g = GRADE[model]
    gen = _gen_grade(prompt)
    props = schema.get("properties", {})
    if "statement" in props:
        data = {"statement": f"[fake {model}] Is f(n) bounded for all n?", "grounding": "fake grounding",
                "why_hard": "fake", "why_important": "fake", "resembles_known": None, "novelty_confidence": 0.5}
        if "checker_code" in props:
            data |= {"finite_form": "Give a list of 3 distinct positive integers.",
                     "candidate_format": "JSON array of 3 integers",
                     "checker_code": "def check(candidate):\n    return isinstance(candidate, list) and len(set(candidate)) == 3\n"}
    elif "claimed_status" in props:
        data = {"text": f"[fake {model}] proof sketch", "claimed_status": "solved" if g >= 2 else "partial",
                "candidate": [1, 2, 3] if g > gen else [1, 1]}
    elif "richness_list" in props:
        data = {"clarity": 3, "difficulty": 3, "want_to_solve": 3,
                "richness_list": ["derived question"] * gen, "known_problem": False}
    else:
        data = {"correctness": min(5, 2 + g), "clarity_sol": 3, "understandable": True}
    return {"is_error": False, "structured_output": data, "result": json.dumps(data), "fake": True}
