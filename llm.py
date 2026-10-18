"""Model call layer: one function, two backends (Claude Code CLI or a deterministic fake)."""
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from store import now

MODELS = ["sonnet", "opus", "fable"]
GRADE = {"sonnet": 1, "opus": 2, "fable": 3}
# Phrases meaning "stop the whole run" (login or plan usage limit). Matched only against the CLI's `result` text.
STOP_MARKERS = ("usage limit", "rate limit", "you've hit your", "you've reached your", "usage credits", "extra usage",
                "spend limit", "credit balance", "authenticate", "authentication error", "oauth", "/login",
                "not logged in", "invalid api key")


class StopRun(Exception):
    """Auth or usage-limit failure: abort the whole run instead of burning the queue."""


class CallFailed(Exception):
    """One call failed; the caller records it in failures.jsonl and moves on."""


# ponytail: crude breaker; per-model counters if one alias flaps
_consecutive_failures = 0
_CLI_VERSION = None


def cli_version() -> str:
    global _CLI_VERSION
    if _CLI_VERSION is None:
        try:
            _CLI_VERSION = subprocess.run([claude_exe(), "--version"], capture_output=True, text=True, encoding="utf-8",
                                          errors="replace", timeout=60).stdout.strip()
        except Exception as e:  # noqa: BLE001 - diagnostic only
            _CLI_VERSION = f"unknown ({e})"
    return _CLI_VERSION


def claude_exe() -> str:
    found = shutil.which("claude")
    if not found:
        raise StopRun("claude CLI not found on PATH")
    native = Path(found).parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    if native.exists():
        return str(native)
    if Path(found).suffix.lower() != ".exe":
        raise StopRun(f"claude CLI at {found} is a shell shim and no native claude.exe was found next to it; "
                      "arguments cannot be passed safely through cmd.exe")
    return found


def call(model: str, system: str, prompt: str, schema: dict, raw_path: Path, dry_run: bool = False) -> dict:
    global _consecutive_failures
    started = now()
    if dry_run:
        out = fake(model, schema, prompt)
    else:
        out = _cli(model, system, prompt, schema, Path(tempfile.gettempdir()) / "claude_cli_cwd")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps({"model": model, "system": system, "prompt": prompt, "schema": schema,
                                    "started_at": started, "finished_at": now(),
                                    "cli_version": None if dry_run else cli_version(), "cli_output": out},
                                   ensure_ascii=False, indent=1), encoding="utf-8")
    _raise_if_error(out)
    used = list(out.get("modelUsage") or {})
    if not dry_run:
        others = [k for k in used if any(m != model and m in k.lower() for m in GRADE)]
        if others or not any(model in k.lower() for k in used):
            raise StopRun(f"answered by {used or 'unknown model'}, not {model}; the CLI fell back or the alias is wrong — "
                          "wait for the limit window or fix --models, then rerun")
    data = out.get("structured_output")
    if data is None:
        try:
            data = json.loads(out.get("result") or "")
        except (TypeError, json.JSONDecodeError):
            raise CallFailed("no structured_output and result is not JSON")
    if not isinstance(data, dict):
        raise CallFailed(f"output is {type(data).__name__}, not an object")
    missing = [k for k in schema.get("required", []) if k not in data]
    if missing:
        raise CallFailed(f"output missing required keys {missing}")
    _consecutive_failures = 0
    return data


def _raise_if_error(out: dict) -> None:
    global _consecutive_failures
    if not out.get("is_error"):
        return
    msg = str(out.get("result") or "")
    low = msg.lower().replace("_", " ")  # API error types arrive as rate_limit_error, authentication_error
    if any(m in low for m in STOP_MARKERS):
        raise StopRun(msg)
    _consecutive_failures += 1
    if _consecutive_failures >= 5:
        raise StopRun(f"5 consecutive failures; last: {msg}")
    raise CallFailed(msg or "CLI reported an error without a message")


def _text(b) -> str:
    return b.decode("utf-8", "replace") if isinstance(b, bytes) else (b or "")


def _cli(model: str, system: str, prompt: str, schema: dict, cwd: Path) -> dict:
    # Hidden context: auto-memory attaches from a project cwd (so cwd is a neutral temp folder), and MCP
    # instructions come from account connectors (so --strict-mcp-config with an empty server list).
    cwd.mkdir(parents=True, exist_ok=True)
    cmd = [claude_exe(), "-p", "--model", model, "--output-format", "json",
           "--json-schema", json.dumps(schema), "--tools", "", "--system-prompt", system,
           "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           "--no-session-persistence"]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # bill the Max plan, never the API
    try:
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=cwd, timeout=1800, env=env)
    except subprocess.TimeoutExpired as e:
        return {"is_error": True, "result": "timeout after 1800s", "stdout": _text(e.stdout), "stderr": _text(e.stderr)}
    except OSError as e:
        return {"is_error": True, "result": f"could not start claude CLI: {e}"}
    if not p.stdout.strip():
        return {"is_error": True, "result": f"empty stdout (exit {p.returncode}); stderr tail: {p.stderr[-300:]}",
                "stdout": p.stdout, "stderr": p.stderr, "returncode": p.returncode}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"is_error": True, "result": f"non-JSON stdout (exit {p.returncode}): {p.stdout[:300]}",
                "stdout": p.stdout, "stderr": p.stderr, "returncode": p.returncode}


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
    if "saw_other_instructions" in props:
        data = {"ok": True, "model_name": f"fake-{model}", "saw_other_instructions": False, "other_instructions_summary": ""}
    elif "statement" in props:
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
    return {"is_error": False, "structured_output": data, "result": json.dumps(data, ensure_ascii=False), "fake": True}
