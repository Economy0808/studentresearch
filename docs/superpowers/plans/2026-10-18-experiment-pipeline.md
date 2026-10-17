# Experiment Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Model roles (user instruction):** planning = Fable (done), implementation subagents = `model: "sonnet"`, review/verification subagents = `model: "opus"`.

**Goal:** Build the tool environment that runs the research plan's three-stage experiment (generate problems → solve → evaluate) across Sonnet/Opus/Fable through the Claude Code CLI, plus a blind human-evaluation web page and the metric analysis.

**Architecture:** A handful of small Python modules under the project root: `store.py` (JSONL I/O), `llm.py` (one `call()` with a CLI backend and a deterministic fake), `pipeline.py` (stages as pure functions over a `data_dir`), `run.py` (argparse CLI), `analyze.py` (pandas/scipy metrics), one growing `selfcheck.py`. Prompts are markdown files. The human page is one static HTML template into which `export-human` injects the blinded dataset.

**Tech Stack:** Python 3.14 stdlib for everything except `analyze.py` (pandas, scipy, matplotlib). Claude Code CLI 2.1.x (`claude.exe`, Max plan OAuth). Vanilla HTML/JS + KaTeX (cdnjs) for the page.

Spec: `docs/superpowers/specs/2026-10-17-experiment-environment-design.md` (read §4–§11 before starting any task).

## Global Constraints

- Project root: `C:\Users\user\Desktop\학자연`. All paths via `pathlib.Path`; every file read/write passes `encoding="utf-8"`; every `json.dumps` of data passes `ensure_ascii=False`.
- Model aliases are exactly `sonnet`, `opus`, `fable`; `GRADE = {"sonnet": 1, "opus": 2, "fable": 3}` lives in `llm.py` and nowhere else.
- IDs: problems `"P-" + 6 hex`, solutions `"S-" + 6 hex` (from `store.new_id`). Timestamps: `store.now()` = ISO 8601 UTC with seconds.
- Prompts live in `prompts/*.md`; the three models receive byte-identical prompts. Solve and eval prompts never contain `source`, `solver`, `grounding`, `why_hard`, `gen_key`.
- Every CLI call is logged whole to `data/raw/<stage>/<id>.json` before parsing. Every stage is idempotent (skips existing results) so a rerun continues after a usage-limit stop.
- Headless CLI invocation (exact flags): `claude.exe -p --model <alias> --output-format json --json-schema <json> --tools "" --system-prompt <text> --setting-sources project --no-session-persistence`, prompt on **stdin**, `cwd` = `data/raw/_cwd/` (empty dir). Parse `structured_output`; fall back to `json.loads(result)`.
- Everything hangs off `data_dir.parent` (= project root by default): `checkers/`, `human_problems.jsonl`, `eval_page/`. `selfcheck.py` uses a temp dir so it never touches real data.
- No new dependencies beyond `requirements.txt` (pandas, scipy, matplotlib). No test framework: the single check is `python selfcheck.py` (also `python run.py selfcheck`).
- Git identity is configured globally. Commit after every task with the message given; end each commit message with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Model-written checker code is never executed unless the file's first line is exactly `# REVIEWED`.
- Each task's implementer must run `python selfcheck.py` as the last check before committing; it must print `selfcheck OK`.

---

### Task 1: Skeleton, JSONL store, selfcheck harness

**Files:**
- Create: `store.py`, `selfcheck.py`, `requirements.txt`, `.gitignore`, `README.md`

**Interfaces:**
- Produces: `store.now() -> str`, `store.new_id(prefix: str) -> str`, `store.read_jsonl(path: Path) -> list[dict]`, `store.append_jsonl(path: Path, row: dict) -> None`, `store.write_jsonl(path: Path, rows: list[dict]) -> None`. `selfcheck.main()` runs every `check_*` function in order inside a fresh temp dir and prints `selfcheck OK`.

- [ ] **Step 1: Write the failing check**

Create `selfcheck.py`:

```python
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
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py`
Expected: `ModuleNotFoundError: No module named 'store'`

- [ ] **Step 3: Implement store.py**

```python
"""JSONL storage helpers shared by every stage."""
import datetime as _dt
import json
import secrets
from pathlib import Path


def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}-{secrets.token_hex(3)}"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    # split("\n"), not splitlines(): ensure_ascii=False writes U+2028/U+2029/U+0085 raw and splitlines() would cut rows there
    return [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line.strip()]


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
```

- [ ] **Step 4: Add the support files**

`requirements.txt`:
```
pandas
scipy
matplotlib
```

`.gitignore`:
```
__pycache__/
data/raw/_cwd/
results/*.png
```

`README.md` (stub; Task 11 completes it):
```markdown
# 학자연 실험 환경

「AI는 지식폭발을 야기할 것인가」 본 실험(생성 → 풀이 → 평가) 도구. 설계: `docs/superpowers/specs/`.

## 점검
```bash
python selfcheck.py
```
```

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py`
Expected: `ok  check_store` then `selfcheck OK`

- [ ] **Step 6: Commit**

```bash
git add store.py selfcheck.py requirements.txt .gitignore README.md
git commit -m "Add JSONL store and selfcheck harness

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Model call layer (CLI + fake) and `run.py probe`

**Files:**
- Create: `llm.py`, `run.py`
- Modify: `selfcheck.py` (add `check_llm_dry`)

**Interfaces:**
- Consumes: `store.now`.
- Produces: `llm.MODELS`, `llm.GRADE`, `llm.StopRun`, `llm.CallFailed`, `llm.call(model, system, prompt, schema, raw_path, dry_run=False) -> dict` (returns the schema-shaped object), `llm.fake(model, schema, prompt) -> dict` (CLI-output-shaped dict with `structured_output`), `llm._raise_if_error(out)`. `run.main(argv=None)` with subcommands `probe`, `selfcheck` (more added later).

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` (before `CHECKS`), and add `check_llm_dry` to `CHECKS`:

```python
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
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py`
Expected: `ModuleNotFoundError: No module named 'llm'`

- [ ] **Step 3: Implement llm.py**

```python
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
```

- [ ] **Step 4: Implement run.py (probe + selfcheck only for now)**

```python
"""CLI for the experiment pipeline. Usage: python run.py [--data-dir data] [--dry-run] [--models a,b] <cmd> ..."""
import argparse
import json
from pathlib import Path

import llm

PROBE_SCHEMA = {"type": "object",
                "properties": {"ok": {"type": "boolean"}, "model_name": {"type": "string"},
                               "saw_other_instructions": {"type": "boolean"}, "other_instructions_summary": {"type": "string"}},
                "required": ["ok", "model_name", "saw_other_instructions", "other_instructions_summary"]}
PROBE_PROMPT = ("Return ok=true, model_name=the model you are, saw_other_instructions=true if you received any "
                "instructions, personas, skills or project notes besides the short system prompt and this message, "
                "and summarize them in other_instructions_summary (empty string if none).")


def probe(models: list[str], data_dir: Path, dry_run: bool = False) -> None:
    for m in models:
        try:
            out = llm.call(m, "You are a research mathematician. Respond only in the requested JSON.",
                           PROBE_PROMPT, PROBE_SCHEMA, data_dir / "raw" / "probe" / f"{m}.json", dry_run)
            print(f"{m}: {json.dumps(out, ensure_ascii=False)}")
        except llm.CallFailed as e:
            print(f"{m}: FAILED {e}")


def report(a, n: int) -> None:
    print(f"{a.cmd}: {n} new record(s) in {a.data_dir}")
    fails = a.data_dir / "failures.jsonl"
    if fails.exists():
        print(f"note: failures were recorded in {fails}; rerunning retries them")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="AI problem generation / solving / evaluation pipeline")
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--dry-run", action="store_true", help="use the fake model; no CLI calls")
    ap.add_argument("--models", default=",".join(llm.MODELS), help="comma-separated model aliases")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe", help="one tiny live call per model; checks auth, aliases and leaked context")
    sub.add_parser("selfcheck", help="run the offline self-check")
    return ap


def main(argv=None) -> None:
    ap = build_parser()
    a = ap.parse_args(argv)
    models = [m.strip() for m in a.models.split(",") if m.strip()]
    try:
        if a.cmd == "probe":
            probe(models, a.data_dir, a.dry_run)
        elif a.cmd == "selfcheck":
            import selfcheck
            selfcheck.main()
    except llm.StopRun as e:
        raise SystemExit(f"STOPPED (auth or usage limit): {e}\n"
                         "Fix it (run `claude` and /login, or wait for the usage window) and rerun the same command; "
                         "finished items are kept.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py`
Expected: `ok  check_store`, `ok  check_llm_dry`, `selfcheck OK`

Also run: `python run.py --help` → lists `probe` and `selfcheck`.

Do **not** run `python run.py probe` in this task unless the user has re-logged in; if you do run it and see `Failed to authenticate`, that is the known expired-OAuth state, not a bug.

- [ ] **Step 6: Commit**

```bash
git add llm.py run.py selfcheck.py
git commit -m "Add model call layer with CLI and fake backends, probe command

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: Prompts, rubric, context-pack spec, human-problem example

**Files:**
- Create: `prompts/system.md`, `prompts/gen_open.md`, `prompts/gen_checkable.md`, `prompts/solve.md`, `prompts/eval_problem.md`, `prompts/eval_solution.md`, `prompts/rubric.md`, `context/README.md`, `human_problems.example.jsonl`
- Modify: `selfcheck.py` (add `check_prompts`)

**Interfaces:**
- Produces: placeholder names used by `pipeline.fill` in Task 4–6: `{context}`, `{focus}` (gen); `{statement}`, `{finite_form}`, `{candidate_format}` (solve); `{rubric}`, `{statement}`, `{finite_form}`, `{why_important}` (eval_problem); `{rubric}`, `{statement}`, `{finite_form}`, `{text}`, `{candidate}` (eval_solution).

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS`:

```python
def check_prompts(tmp: Path, data: Path) -> None:
    root = Path(__file__).resolve().parent / "prompts"
    need = {"system.md": [], "gen_open.md": ["{context}", "{focus}"],
            "gen_checkable.md": ["{context}", "{focus}", "checker_code"],
            "solve.md": ["{statement}", "{finite_form}", "{candidate_format}"],
            "eval_problem.md": ["{rubric}", "{statement}", "{finite_form}", "{why_important}"],
            "eval_solution.md": ["{rubric}", "{statement}", "{finite_form}", "{text}", "{candidate}"],
            "rubric.md": ["clarity", "difficulty", "richness_list", "want_to_solve", "known_problem",
                          "correctness", "clarity_sol", "understandable"]}
    for name, tokens in need.items():
        text = (root / name).read_text(encoding="utf-8")
        for t in tokens:
            assert t in text, f"{name} lacks {t}"
    for name in ("solve.md", "eval_problem.md", "eval_solution.md"):
        text = (root / name).read_text(encoding="utf-8")
        for leak in ("{source}", "{solver}", "{grounding}", "{why_hard}"):
            assert leak not in text, f"{name} must not reveal {leak}"
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py`
Expected: `FileNotFoundError` for `prompts/system.md`

- [ ] **Step 3: Write the prompt files**

`prompts/system.md`:
```
You are a research mathematician working alone, with no tools and no internet access. Answer only in the requested JSON format. Write mathematics in English, using LaTeX ($...$) for formulas.
```

`prompts/gen_open.md`:
```
Below is a context pack summarizing recent results in one area of mathematics.

<context>
{context}
</context>

Task: pose ONE problem in this area that you believe is currently unsolved, grounded in the context above. Focus on the section titled "{focus}": start from a gap, a boundary case, or a natural extension that the results in that section leave open.

Requirements
- statement: a precise, self-contained problem statement of at most 150 words. Define every symbol you use.
- grounding: which results in the context the problem extends, and exactly where the gap is (cite section titles).
- why_hard: the obvious approaches and the specific reason each one fails.
- why_important: what would follow if it were solved, and why it is more than a routine exercise.
- resembles_known: the name of any well-known conjecture or theorem this problem resembles or specializes, or null if none.
- novelty_confidence: your probability (0 to 1) that the problem is genuinely open rather than a known result.

Do not restate a named conjecture (an Erdős problem by number, Goldbach, twin primes, and so on). Prefer a problem a specialist would recognize as natural and would want to attack.
```

`prompts/gen_checkable.md`:
```
Below is a context pack summarizing recent results in one area of mathematics.

<context>
{context}
</context>

Task: pose ONE problem in this area that you believe is currently unsolved, grounded in the context above, of the form "find a construction, counterexample, or extremal object", so that a proposed answer can be checked mechanically. Focus on the section titled "{focus}": start from a gap, a boundary case, or a natural extension that the results in that section leave open.

Requirements
- statement: the general (infinite-family) problem, precise and self-contained, at most 150 words. Define every symbol.
- grounding: which results in the context the problem extends, and exactly where the gap is (cite section titles).
- why_hard: the obvious approaches and the specific reason each one fails.
- why_important: what would follow if it were solved.
- resembles_known: the name of any well-known conjecture or theorem this resembles, or null.
- novelty_confidence: your probability (0 to 1) that the general problem is genuinely open.
- finite_form: one concrete finite instance (fix the parameters, e.g. n = 12) whose solution is a finite object (a set, a sequence, a graph, a coloring) and which you believe is still hard at that size, not solvable by a quick brute-force search.
- candidate_format: the exact JSON shape a solver must submit, e.g. "a JSON array of distinct positive integers at most 100".
- checker_code: a complete Python function `def check(candidate) -> bool` returning True exactly when the candidate solves finite_form. Standard library only, deterministic, finishes within 10 seconds on any input of the stated shape, and returns False (never raises) on malformed input.

Do not restate a named conjecture. The checker must test the finite_form you stated, nothing else.
```

`prompts/solve.md`:
```
Solve the following problem as completely as you can.

<problem>
{statement}
</problem>

<finite_instance>
{finite_form}
</finite_instance>

<required_candidate_format>
{candidate_format}
</required_candidate_format>

Return
- text: your full solution or best partial progress: definitions, the argument, and a clear final answer. If you cannot solve it, state exactly what you proved and what remains.
- claimed_status: "solved" only if you believe the problem (or, when given, the finite instance) is fully solved; "partial" for real progress; "unsolved" otherwise.
- candidate: if a finite instance is given, the object you propose, exactly in the required JSON shape; otherwise null.
```

`prompts/rubric.md`:
```
# 채점표 (문제·풀이 공통)

모든 항목에 "판단 불가"를 선택할 수 있다. 확신이 없으면 추측하지 말고 판단 불가를 택한다.

## 문제 평가
- 명확성 (clarity, 1~5): 1 = 뜻이 통하지 않거나 정의가 빠짐 · 3 = 뜻은 통하지만 모호한 부분이 있음 · 5 = 모든 기호와 조건이 정의되어 한 가지로만 읽힘
- 난이도 (difficulty, 1~5): 1 = 학부 연습문제 수준 · 3 = 대학원생이 며칠 걸릴 수준 · 5 = 현재 알려진 방법으로는 접근이 보이지 않는 수준
- 풍요로움 (richness_list): "이 문제가 풀리면 쉬워지거나 자연스럽게 따라오는 다른 문제"를 생각나는 만큼 적는다. 한 줄에 하나. 없으면 비워 둔다. 점수는 그 개수다.
- 풀고 싶은 정도 (want_to_solve, 1~5): 1 = 전혀 · 3 = 시간이 있으면 · 5 = 지금 바로 붙잡고 싶다
- 이미 알려진 문제 (known_problem): 이 문제가 이미 알려진 문제·정리와 사실상 같다면 체크한다.

## 풀이 평가
- 정확성 (correctness, 1~5): 1 = 틀렸거나 핵심 단계가 없음 · 3 = 방향은 맞지만 빈틈이 있음 · 5 = 완전하고 올바름
- 명료성 (clarity_sol, 1~5): 1 = 따라갈 수 없음 · 3 = 노력하면 따라갈 수 있음 · 5 = 한 번 읽고 따라갈 수 있음
- 이해 가능 여부 (understandable): 이 풀이의 핵심 아이디어를 자기 말로 다시 설명할 수 있으면 "예", 없으면 "아니오", 모르겠으면 "판단 불가"
```

`prompts/eval_problem.md`:
```
You are one evaluator on a panel. Score the problem below using exactly the rubric that follows (the rubric is written in Korean; score items are the English keys in parentheses). Use null for any item you cannot judge. Do not try to guess who wrote the problem.

<rubric>
{rubric}
</rubric>

<problem>
{statement}
</problem>

<finite_instance>
{finite_form}
</finite_instance>

<stated_importance>
{why_important}
</stated_importance>

Return clarity, difficulty, want_to_solve as integers 1–5 or null; richness_list as an array of strings, one derived problem per string (may be empty); known_problem as a boolean.
```

`prompts/eval_solution.md`:
```
You are one evaluator on a panel. Score the solution below to the given problem using exactly the rubric that follows (the rubric is written in Korean; score items are the English keys in parentheses). Use null for any item you cannot judge. Do not try to guess who wrote the solution.

<rubric>
{rubric}
</rubric>

<problem>
{statement}
</problem>

<finite_instance>
{finite_form}
</finite_instance>

<solution>
{text}
</solution>

<submitted_candidate>
{candidate}
</submitted_candidate>

Return correctness and clarity_sol as integers 1–5 or null; understandable as true, false, or null.
```

- [ ] **Step 4: Write context/README.md and the human example**

`context/README.md`:
```markdown
# 컨텍스트 팩 작성 규격

`run.py gen --context context/<이름>.md`가 읽는 마크다운 한 파일. `## ` 2단계 헤더가 섹션이다.

1. `## Definitions` — 핵심 정의 1쪽.
2. `## Result: <짧은 제목>` × 8~12개 — 정리 진술 + 한 줄 증명 아이디어 + 출처(저자, 연도, arXiv 번호).
   2023~2026년에 풀린 Erdős 문제와 arXiv 최신 결과 위주로 고른다(학습 데이터 오염 통제).
3. `## Format examples` — 문제 진술 형식 예시 2~3개(Erdős 스타일).
   **대조군으로 쓸 open 문제(`human_problems.jsonl`)는 절대 넣지 않는다.**

`gen --n k`는 i번째 호출에 `Result:` 섹션 중 i번째(개수를 넘으면 순환)를 초점으로 준다.
세 모델에 동일하게 적용된다. 파일 상단에 `DRAFT` 표시가 있으면 연구자 검토 전이다.

## 최소 예시

```
# DRAFT — additive combinatorics pack

## Definitions
A set A ⊂ ℕ is a Sidon set if all pairwise sums a+b (a ≤ b) are distinct. ...

## Result: Sidon sets in [N] have size ≤ √N + N^{1/4} + 1/2
Statement. ... Proof idea. ... Source: Balogh–Füredi–Roy, 2023, arXiv:2103.15850.

## Result: ...

## Format examples
Erdős-style: "Let A ⊂ {1,…,N} be ... Is it true that |A| ≤ ...?"
```
```

`human_problems.example.jsonl` (one line; researchers copy to `human_problems.jsonl` and replace the content):
```
{"id": "P-h00001", "source": "human", "kind": "open", "context_id": null, "focus": null, "statement": "EXAMPLE, REPLACE ME. Let $A \\subset \\{1,\\dots,N\\}$ be a Sidon set. Is it true that $|A| \\le \\sqrt{N} + O(1)$?", "grounding": null, "why_hard": null, "why_important": "Erdős problem, see erdosproblems.com (replace with the actual number and text).", "resembles_known": null, "novelty_confidence": null, "finite_form": null, "candidate_format": null, "checker_code": null, "created_at": "2026-10-18T00:00:00+00:00"}
```

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py`
Expected: `ok  check_prompts` and `selfcheck OK`

- [ ] **Step 6: Commit**

```bash
git add prompts context human_problems.example.jsonl selfcheck.py
git commit -m "Add prompts, rubric, context pack spec and human problem example

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: `gen` stage with checker file output

**Files:**
- Create: `pipeline.py`
- Modify: `run.py` (add `gen` subcommand), `selfcheck.py` (add `check_gen`)

**Interfaces:**
- Consumes: `llm.call`, `llm.MODELS`, `llm.CallFailed`, `store.*`, prompt files from Task 3.
- Produces: `pipeline._schema(props) -> dict`, `pipeline.GEN_PROPS`, `pipeline.CHECKABLE_PROPS`, `pipeline.SOLVE_PROPS`, `pipeline.EVAL_PROBLEM_PROPS`, `pipeline.EVAL_SOLUTION_PROPS`, `pipeline.load_prompt(name) -> str`, `pipeline.fill(template, **values) -> str`, `pipeline.system() -> str`, `pipeline.parse_context(path) -> tuple[str, list[str]]`, `pipeline.all_problems(data_dir) -> list[dict]`, `pipeline.record_failure(data_dir, stage, target_id, model, err)`, `pipeline.gen(data_dir, context_path, kind, n, models=llm.MODELS, dry_run=False) -> int`. Problem rows carry `gen_key` = `"<context_id>:<kind>:<model>:<i>"` for idempotency. Checkers go to `data_dir.parent / "checkers" / f"{problem_id}.py"`.

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS`:

```python
CONTEXT = """# Fake pack

## Definitions
fake

## Result: A
fake a

## Result: B
fake b

## Format examples
fake
"""


def check_gen(tmp: Path, data: Path) -> None:
    import pipeline
    ctx = tmp / "ctx.md"
    ctx.write_text(CONTEXT, encoding="utf-8")
    assert pipeline.parse_context(ctx)[1] == ["Result: A", "Result: B"]
    n1 = pipeline.gen(data, ctx, "open", 2, dry_run=True)
    n2 = pipeline.gen(data, ctx, "checkable", 1, dry_run=True)
    assert (n1, n2) == (6, 3), (n1, n2)
    assert pipeline.gen(data, ctx, "open", 2, dry_run=True) == 0, "gen must be idempotent"
    probs = read_jsonl(data / "problems.jsonl")
    assert len(probs) == 9
    assert {p["focus"] for p in probs if p["kind"] == "open"} == {"Result: A", "Result: B"}
    assert all(p["id"].startswith("P-") and p["source"] in ("sonnet", "opus", "fable") for p in probs)
    assert all(p["checker_code"] is None for p in probs if p["kind"] == "open")
    checkers = sorted((tmp / "checkers").glob("P-*.py"))
    assert len(checkers) == 3, checkers
    first = checkers[0].read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("# UNREVIEWED"), first
    raws = list((data / "raw" / "gen").glob("*.json"))
    assert len(raws) == 9, len(raws)
    assert pipeline.fill("a {x} b {y}", x="1", y=None) == "a 1 b "
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py`
Expected: `ModuleNotFoundError: No module named 'pipeline'`

- [ ] **Step 3: Implement pipeline.py (gen part)**

```python
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
    results = [m.group(1).strip() for m in re.finditer(r"^## (Result:.*)$", text, flags=re.M)]
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
            row = {"id": new_id("P"), "source": model, "kind": kind, "context_id": context_id,
                   "focus": focus, "gen_key": key}
            row.update({k: None for k in CHECKABLE_PROPS})
            row.update(out)
            row["created_at"] = now()
            append_jsonl(problems_path, row)
            if kind == "checkable":
                _write_checker(data_dir, row)
            made += 1
    return made


def _write_checker(data_dir: Path, p: dict) -> None:
    cdir = data_dir.parent / "checkers"
    cdir.mkdir(parents=True, exist_ok=True)
    one_line = lambda s: (s or "").replace("\n", " ")[:300]
    header = ("# UNREVIEWED: read this file; if it correctly tests finite_form, replace this first line with exactly '# REVIEWED'.\n"
              f"# problem {p['id']} (generated by {p['source']}): {one_line(p['statement'])}\n"
              f"# finite_form: {one_line(p['finite_form'])}\n"
              f"# candidate_format: {one_line(p['candidate_format'])}\n\n")
    (cdir / f"{p['id']}.py").write_text(header + p["checker_code"], encoding="utf-8")
```

- [ ] **Step 4: Wire `gen` into run.py**

In `run.py`: add `import pipeline` after `import llm`. In `build_parser()`, before `sub.add_parser("probe", ...)`:

```python
    g = sub.add_parser("gen", help="generate problems: context × models × n")
    g.add_argument("--context", type=Path, required=True)
    g.add_argument("--kind", choices=["open", "checkable"], required=True)
    g.add_argument("--n", type=int, default=5)
```

In `main()`, inside the `try`, before the `probe` branch (and change the existing `if a.cmd == "probe":` to `elif`):

```python
        if a.cmd == "gen":
            report(a, pipeline.gen(a.data_dir, a.context, a.kind, a.n, models, a.dry_run))
        elif a.cmd == "probe":
```

- [ ] **Step 5: Run the check and a dry-run from the CLI**

Run: `python selfcheck.py` → `ok  check_gen`, `selfcheck OK`.

Run: `python run.py --dry-run --data-dir %TEMP%\gen_try gen --context context\README.md --kind open --n 1`
Expected: exits with `context\README.md: no '## Result:' sections` (the README's example is inside a code fence, so this is the right error). This confirms the error path; delete `%TEMP%\gen_try` afterwards.

- [ ] **Step 6: Commit**

```bash
git add pipeline.py run.py selfcheck.py
git commit -m "Add problem generation stage with checker file output

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: `solve` stage

**Files:**
- Modify: `pipeline.py` (add `solve`), `run.py` (add `solve`), `selfcheck.py` (add `check_solve`)

**Interfaces:**
- Consumes: `pipeline.all_problems`, `pipeline.fill`, `pipeline.SOLVE_PROPS`, `llm.call`.
- Produces: `pipeline.solve(data_dir, models=llm.MODELS, dry_run=False) -> int`; rows in `solutions.jsonl` with `id, problem_id, solver, text, claimed_status, candidate, created_at`; raw files `data/raw/solve/<problem_id>_<model>.json`.

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS` (after `check_gen`; it relies on the 9 problems gen left in `data`):

```python
def check_solve(tmp: Path, data: Path) -> None:
    import pipeline
    assert pipeline.solve(data, dry_run=True) == 27
    assert pipeline.solve(data, dry_run=True) == 0, "solve must be idempotent"
    sols = read_jsonl(data / "solutions.jsonl")
    assert len(sols) == 27 and all(s["id"].startswith("S-") for s in sols)
    assert {s["solver"] for s in sols} == {"sonnet", "opus", "fable"}
    raw = next((data / "raw" / "solve").glob("*.json")).read_text(encoding="utf-8")
    for leak in ('"source"', "grounding", "gen_key"):
        assert leak not in __import__("json").loads(raw)["prompt"], f"solve prompt leaks {leak}"
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py`
Expected: `AttributeError: module 'pipeline' has no attribute 'solve'`

- [ ] **Step 3: Implement solve in pipeline.py**

Append:

```python
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
```

- [ ] **Step 4: Wire into run.py**

In `build_parser()`: `sub.add_parser("solve", help="every problem (incl. human_problems.jsonl) × every model")`.
In `main()`: `elif a.cmd == "solve": report(a, pipeline.solve(a.data_dir, models, a.dry_run))`.

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py` → `ok  check_solve`, `selfcheck OK`

- [ ] **Step 6: Commit**

```bash
git add pipeline.py run.py selfcheck.py
git commit -m "Add solve stage

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: `eval` stage (AI raters)

**Files:**
- Modify: `pipeline.py` (add `eval_ai`), `run.py` (add `eval`), `selfcheck.py` (add `check_eval`)

**Interfaces:**
- Produces: `pipeline.eval_ai(data_dir, models=llm.MODELS, dry_run=False) -> int`; rows in `ratings.jsonl` with `rater, rater_type="ai", target_type, target_id, <rubric fields>, created_at`; raw files `data/raw/eval/<target_id>_<model>.json`.

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS` after `check_solve`:

```python
def check_eval(tmp: Path, data: Path) -> None:
    import pipeline
    assert pipeline.eval_ai(data, dry_run=True) == 9 * 3 + 27 * 3
    assert pipeline.eval_ai(data, dry_run=True) == 0, "eval must be idempotent"
    ratings = read_jsonl(data / "ratings.jsonl")
    probs = {p["id"]: p for p in read_jsonl(data / "problems.jsonl")}
    grade = {"sonnet": 1, "opus": 2, "fable": 3}
    for r in ratings:
        assert r["rater_type"] == "ai" and r["rater"] in grade
        if r["target_type"] == "problem":
            assert len(r["richness_list"]) == grade[probs[r["target_id"]]["source"]], r
        else:
            assert r["correctness"] == min(5, 2 + grade[r["rater"]]), r
    raw = next((data / "raw" / "eval").glob("*.json")).read_text(encoding="utf-8")
    prompt = __import__("json").loads(raw)["prompt"]
    assert "채점표" in prompt and '"source"' not in prompt and "grounding" not in prompt
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py` → `AttributeError: module 'pipeline' has no attribute 'eval_ai'`

- [ ] **Step 3: Implement eval_ai in pipeline.py**

Append:

```python
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
```

- [ ] **Step 4: Wire into run.py**

`sub.add_parser("eval", help="AI raters score every problem and solution, one item per call")` and
`elif a.cmd == "eval": report(a, pipeline.eval_ai(a.data_dir, models, a.dry_run))`.

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py` → `ok  check_eval`, `selfcheck OK`

- [ ] **Step 6: Commit**

```bash
git add pipeline.py run.py selfcheck.py
git commit -m "Add AI evaluation stage

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: `verify` stage with isolated checker runner

**Files:**
- Create: `checker_runner.py`
- Modify: `pipeline.py` (add `verify`), `run.py` (add `verify`), `selfcheck.py` (add `check_verify`)

**Interfaces:**
- Produces: `pipeline.verify(data_dir, timeout=60) -> int`; rows in `verifications.jsonl`: `solution_id, problem_id, verdict ∈ {pass, fail, error, na}, log, created_at`. `checker_runner.py <checker.py> <candidate.json>` prints `PASS` or `FAIL` on its last stdout line.

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS` after `check_eval`:

```python
def check_verify(tmp: Path, data: Path) -> None:
    import pipeline
    probs = {p["source"]: p for p in read_jsonl(data / "problems.jsonl") if p["kind"] == "checkable"}
    for src in ("sonnet", "fable"):  # review two of the three checkers; leave opus unreviewed
        f = tmp / "checkers" / f"{probs[src]['id']}.py"
        lines = f.read_text(encoding="utf-8").splitlines()
        lines[0] = "# REVIEWED"
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert pipeline.verify(data) == 6, "2 reviewed problems × 3 solvers"
    assert pipeline.verify(data) == 0, "verify must be idempotent"
    sols = {s["id"]: s for s in read_jsonl(data / "solutions.jsonl")}
    verdicts = {(probs_src(sols[v["solution_id"]], probs), sols[v["solution_id"]]["solver"]): v["verdict"]
                for v in read_jsonl(data / "verifications.jsonl")}
    assert verdicts[("sonnet", "opus")] == "pass" and verdicts[("sonnet", "fable")] == "pass"
    assert verdicts[("sonnet", "sonnet")] == "fail"
    assert all(verdicts[("fable", m)] == "fail" for m in ("sonnet", "opus", "fable")), verdicts
    assert ("opus", "opus") not in verdicts, "unreviewed checker must be skipped"


def probs_src(sol: dict, probs: dict) -> str:
    return next(src for src, p in probs.items() if p["id"] == sol["problem_id"])
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py` → `AttributeError: module 'pipeline' has no attribute 'verify'`

- [ ] **Step 3: Create checker_runner.py**

```python
"""Run one checker on one candidate in an isolated interpreter.
Usage: python -I checker_runner.py <checker.py> <candidate.json>  → prints PASS or FAIL."""
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location("checker", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
with open(sys.argv[2], encoding="utf-8") as f:
    candidate = json.load(f)
print("PASS" if mod.check(candidate) is True else "FAIL")
```

- [ ] **Step 4: Implement verify in pipeline.py**

Append:

```python
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
        elif checker.read_text(encoding="utf-8").splitlines()[0].strip() != "# REVIEWED":
            print(f"skip {s['id']}: {checker.name} is not marked '# REVIEWED'")
            continue
        else:
            cand = data_dir / "raw" / "verify" / f"{s['id']}_candidate.json"
            cand.parent.mkdir(parents=True, exist_ok=True)
            cand.write_text(json.dumps(s["candidate"]), encoding="utf-8")
            try:
                r = subprocess.run([sys.executable, "-I", str(runner), str(checker), str(cand)],
                                   capture_output=True, text=True, encoding="utf-8",
                                   timeout=timeout, cwd=cand.parent)
                last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
                verdict = {"PASS": "pass", "FAIL": "fail"}.get(last, "error")
                log = (r.stdout + r.stderr)[-2000:]
            except subprocess.TimeoutExpired:
                verdict, log = "error", f"timeout after {timeout}s"
        append_jsonl(ver_path, {"solution_id": s["id"], "problem_id": p["id"], "verdict": verdict,
                                "log": log, "created_at": now()})
        made += 1
    return made
```

- [ ] **Step 5: Wire into run.py and run the check**

`sub.add_parser("verify", help="run REVIEWED checkers on submitted candidates")` and
`elif a.cmd == "verify": report(a, pipeline.verify(a.data_dir))`.

Run: `python selfcheck.py` → `ok  check_verify`, `selfcheck OK`

- [ ] **Step 6: Commit**

```bash
git add checker_runner.py pipeline.py run.py selfcheck.py
git commit -m "Add machine verification stage with isolated checker runner

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: `export-human` and `import-human`

**Files:**
- Modify: `pipeline.py` (add `export_human`, `import_human`), `run.py`, `selfcheck.py` (add `check_roundtrip`)

**Interfaces:**
- Produces: `pipeline.export_human(data_dir, raters: list[str]) -> Path` writing `data/blind.json` = `{"generated_at", "raters": [...], "rubric_md", "problems": [{"id", "statement", "why_important", "finite_form", "solutions": [{"id", "text", "candidate"}]}]}` and, when `data_dir.parent/eval_page/template.html` exists, `eval_page/index.html` with the literal token `/*BLIND_JSON*/` replaced by the JSON (with `</` escaped as `<\/`). `pipeline.import_human(data_dir, path) -> int` accepts a JSON array of rating rows or `{"ratings": [...]}`; each row `{rater, target_type, target_id, <fields>, source_guess?, created_at?}`.

- [ ] **Step 1: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS` after `check_verify`:

```python
def check_roundtrip(tmp: Path, data: Path) -> None:
    import json
    import pipeline
    out = pipeline.export_human(data, ["R1", "R2"])
    text = out.read_text(encoding="utf-8")
    blind = json.loads(text)
    assert len(blind["problems"]) == 9 and all(len(p["solutions"]) == 3 for p in blind["problems"])
    for leak in ('"source"', '"solver"', '"grounding"', '"why_hard"', '"gen_key"', '"kind"'):
        assert leak not in text, f"blind.json leaks {leak}"
    assert "채점표" in blind["rubric_md"] and blind["raters"] == ["R1", "R2"]
    rows = [{"rater": "R1", "target_type": "problem", "target_id": p["id"], "clarity": 4, "difficulty": None,
             "want_to_solve": 2, "richness_list": ["x"], "known_problem": False, "source_guess": "ai_mid"}
            for p in blind["problems"]]
    rows.append({"rater": "R9", "target_type": "problem", "target_id": blind["problems"][0]["id"], "clarity": 1})
    rows.append({"rater": "R1", "target_type": "solution", "target_id": blind["problems"][0]["solutions"][0]["id"],
                 "correctness": 9, "clarity_sol": 3, "understandable": None})
    f = tmp / "human.json"
    f.write_text(json.dumps(rows), encoding="utf-8")
    assert pipeline.import_human(data, f) == 10, "9 problem rows + 1 solution row; R9 skipped"
    assert pipeline.import_human(data, f) == 10
    human = [r for r in read_jsonl(data / "ratings.jsonl") if r["rater_type"] == "human"]
    assert len(human) == 10, "re-import must overwrite, not duplicate"
    sol = next(r for r in human if r["target_type"] == "solution")
    assert sol["correctness"] is None, "out-of-range score becomes null"
    assert all(r["source_guess"] in ("ai_mid", None) for r in human)
    assert len([r for r in read_jsonl(data / "ratings.jsonl") if r["rater_type"] == "ai"]) == 108
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python selfcheck.py` → `AttributeError: module 'pipeline' has no attribute 'export_human'`

- [ ] **Step 3: Implement export_human and import_human**

Append to `pipeline.py`:

```python
def export_human(data_dir: Path, raters: list[str]) -> Path:
    sols: dict[str, list[dict]] = {}
    for s in read_jsonl(data_dir / "solutions.jsonl"):
        sols.setdefault(s["problem_id"], []).append({"id": s["id"], "text": s["text"], "candidate": s.get("candidate")})
    blind = {"generated_at": now(), "raters": raters, "rubric_md": load_prompt("rubric.md"),
             "problems": sorted([{"id": p["id"], "statement": p["statement"],
                                  "why_important": p.get("why_important") or "",
                                  "finite_form": p.get("finite_form"),
                                  "solutions": sols.get(p["id"], [])}
                                 for p in all_problems(data_dir)], key=lambda x: x["id"])}
    out = data_dir / "blind.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(blind, ensure_ascii=False, indent=1), encoding="utf-8")
    tpl = data_dir.parent / "eval_page" / "template.html"
    if tpl.exists():
        payload = json.dumps(blind, ensure_ascii=False).replace("</", "<\\/")
        (tpl.parent / "index.html").write_text(tpl.read_text(encoding="utf-8").replace("/*BLIND_JSON*/", payload),
                                               encoding="utf-8")
    return out


HUMAN_FIELDS = {"problem": ("clarity", "difficulty", "want_to_solve", "richness_list", "known_problem"),
                "solution": ("correctness", "clarity_sol", "understandable")}
SCORE_FIELDS = {"clarity", "difficulty", "want_to_solve", "correctness", "clarity_sol"}
GUESSES = {"human", "ai_low", "ai_mid", "ai_high", "unknown"}


def _clean_field(k: str, v):
    if k in SCORE_FIELDS:
        return v if isinstance(v, int) and 1 <= v <= 5 else None
    if k == "richness_list":
        return [str(x).strip() for x in v if str(x).strip()] if isinstance(v, list) else []
    if k in ("known_problem", "understandable"):
        return v if isinstance(v, bool) else None
    return v


def import_human(data_dir: Path, path: Path) -> int:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("ratings", [])
    allowed = set(json.loads((data_dir / "blind.json").read_text(encoding="utf-8"))["raters"])
    clean = []
    for r in rows:
        if r.get("rater") not in allowed:
            print(f"skip: rater {r.get('rater')!r} is not in blind.json raters")
            continue
        if r.get("target_type") not in HUMAN_FIELDS or not r.get("target_id"):
            print(f"skip: malformed row {str(r)[:120]}")
            continue
        row = {"rater": r["rater"], "rater_type": "human", "target_type": r["target_type"], "target_id": r["target_id"]}
        for k in HUMAN_FIELDS[r["target_type"]]:
            row[k] = _clean_field(k, r.get(k))
        row["source_guess"] = r.get("source_guess") if r.get("source_guess") in GUESSES else None
        row["created_at"] = r.get("created_at") or now()
        clean.append(row)
    ratings_path = data_dir / "ratings.jsonl"
    keys = {(c["rater"], c["target_type"], c["target_id"]) for c in clean}
    kept = [e for e in read_jsonl(ratings_path)
            if not (e["rater_type"] == "human" and (e["rater"], e["target_type"], e["target_id"]) in keys)]
    write_jsonl(ratings_path, kept + clean)
    return len(clean)
```

- [ ] **Step 4: Wire into run.py**

```python
    e = sub.add_parser("export-human", help="write data/blind.json (+ eval_page/index.html if template exists)")
    e.add_argument("--raters", default="R1,R2,R3,R4,R5", help="allowed evaluator codes")
    i = sub.add_parser("import-human", help="merge a JSON file downloaded from the evaluation page")
    i.add_argument("file", type=Path)
```
and in `main()`:
```python
        elif a.cmd == "export-human":
            print(pipeline.export_human(a.data_dir, [r.strip() for r in a.raters.split(",") if r.strip()]))
        elif a.cmd == "import-human":
            report(a, pipeline.import_human(a.data_dir, a.file))
```

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py` → `ok  check_roundtrip`, `selfcheck OK`

- [ ] **Step 6: Commit**

```bash
git add pipeline.py run.py selfcheck.py
git commit -m "Add blind export and human rating import

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: Human evaluation page (`eval_page/template.html`)

**Files:**
- Create: `eval_page/template.html`
- Test: manual, in the built-in browser pane, on a dry-run `index.html`

**Interfaces:**
- Consumes: `/*BLIND_JSON*/` token replaced by Task 8's `export_human` with the blind.json object.
- Produces: downloaded file `ratings_<rater>.json` = `{"rater", "exported_at", "ratings": [rows]}` where each row matches Task 8's `import_human` input (`rater, target_type, target_id, clarity, difficulty, want_to_solve, richness_list, known_problem` for problems; `rater, target_type, target_id, correctness, clarity_sol, understandable` for solutions; `source_guess` set on both at the guess screen; `created_at`).

Before writing, the implementer loads the `artifact-design` skill (page contract: `<title>` of 2–4 words, color tokens on `:root` with dark-mode overrides, explicit `body` background, phone-width layout with 16px gutters, scripts only from cdnjs/jsdelivr/unpkg with pinned versions).

- [ ] **Step 1: Produce a dry-run dataset to test against**

Create `selfcheck_ctx.md` in the project root with the `CONTEXT` string from `selfcheck.py` (the text between the triple quotes). Then:
```bash
python run.py --dry-run --data-dir %TEMP%\page_try\data gen --context selfcheck_ctx.md --kind open --n 2
python run.py --dry-run --data-dir %TEMP%\page_try\data gen --context selfcheck_ctx.md --kind checkable --n 1
python run.py --dry-run --data-dir %TEMP%\page_try\data solve
```
Expected: 9 problems, 27 solutions. Delete `selfcheck_ctx.md` before committing.

- [ ] **Step 2: Write the template**

`eval_page/template.html`. Required behaviour (spec §9); implement all of it:

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>문제·풀이 평가</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/contrib/auto-render.min.js"></script>
<style>
:root{--bg:#faf9f6;--fg:#1d1c1a;--muted:#6b6862;--line:#dcd9d2;--accent:#2f5d8a;--card:#ffffff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17181a;--fg:#ecebe7;--muted:#9a978f;--line:#34373b;--accent:#7fb0e0;--card:#1f2124}}
:root[data-theme="dark"]{--bg:#17181a;--fg:#ecebe7;--muted:#9a978f;--line:#34373b;--accent:#7fb0e0;--card:#1f2124}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:24px 16px 80px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px;margin:12px 0}
.math{white-space:pre-wrap;overflow-x:auto}
.muted{color:var(--muted);font-size:14px}
fieldset{border:0;padding:0;margin:14px 0}
legend{font-weight:600;margin-bottom:4px}
.scale label{display:inline-block;margin-right:10px}
textarea{width:100%;min-height:90px;box-sizing:border-box;font:inherit;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px}
button{font:inherit;padding:10px 16px;border-radius:6px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer}
button.secondary{background:transparent;color:var(--accent)}
.bar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
details pre{white-space:pre-wrap;font:inherit}
.err{color:#b4232c}
</style>
</head>
<body>
<main id="app"></main>
<script id="blind" type="application/json">/*BLIND_JSON*/</script>
<script>
(() => {
  let BLIND = null;
  try { BLIND = JSON.parse(document.getElementById('blind').textContent); } catch (e) { BLIND = null; }
  const app = document.getElementById('app');
  const $ = (tag, attrs = {}, ...kids) => { const el = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) { if (k === 'class') el.className = v; else if (k.startsWith('on')) el.addEventListener(k.slice(2), v); else el.setAttribute(k, v); } for (const kid of kids) el.append(kid); return el; };
  const mathBlock = (text) => { const d = $('div', { class: 'math' }); d.textContent = text || ''; queueMicrotask(() => { if (window.renderMathInElement) renderMathInElement(d, { delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }, { left: '\\(', right: '\\)', display: false }, { left: '\\[', right: '\\]', display: true }], throwOnError: false }); }); return d; };

  // deterministic shuffle seeded by the rater code (mulberry32 over a string hash)
  const seeded = (str) => { let h = 1779033703 ^ str.length; for (const c of str) { h = Math.imul(h ^ c.charCodeAt(0), 3432918353); h = (h << 13) | (h >>> 19); } return () => { h = Math.imul(h ^ (h >>> 16), 2246822507); h = Math.imul(h ^ (h >>> 13), 3266489909); return ((h ^= h >>> 16) >>> 0) / 4294967296; }; };
  const shuffle = (arr, rnd) => { for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [arr[i], arr[j]] = [arr[j], arr[i]]; } return arr; };
  const buildSteps = (code) => { const rnd = seeded(code); const steps = []; for (const p of shuffle([...BLIND.problems], rnd)) { steps.push({ type: 'problem', p }); for (const s of shuffle([...p.solutions], rnd)) steps.push({ type: 'solution', p, s }); } steps.push({ type: 'guess' }); steps.push({ type: 'done' }); return steps; };

  // state: {rater, idx, ratings: {"problem:P-x": row, "solution:S-y": row}}
  const KEY = (code) => 'hakja:' + code;
  const load = (code) => { try { return JSON.parse(localStorage.getItem(KEY(code))) || null; } catch (e) { return null; } };
  const save = (state) => { try { localStorage.setItem(KEY(state.rater), JSON.stringify(state)); } catch (e) { /* storage unavailable: the download is the record */ } };
  let dbp = null; // best-effort mirror; the JSON download is the record
  const mirror = async (row) => { try { if (!dbp) dbp = (window.claude && window.claude.use) ? window.claude.use('db') : Promise.resolve(null); const db = await dbp; if (db) await db.doc('ratings/' + row.rater + ':' + row.target_id).set(row); } catch (e) { /* ignore */ } };

  let state = null, steps = [];
  const nowIso = () => new Date().toISOString();
  const download = () => { const rows = Object.values(state.ratings); const blob = new Blob([JSON.stringify({ rater: state.rater, exported_at: nowIso(), ratings: rows }, null, 1)], { type: 'application/json' }); const a = $('a', { href: URL.createObjectURL(blob), download: 'ratings_' + state.rater + '.json' }); document.body.append(a); a.click(); a.remove(); };

  const scale = (name, labelText) => { const fs = $('fieldset', { class: 'scale' }, $('legend', {}, labelText)); for (const v of [1, 2, 3, 4, 5, 'na']) fs.append($('label', {}, $('input', { type: 'radio', name, value: String(v), required: '' }), ' ' + (v === 'na' ? '판단 불가' : v))); return fs; };
  const readScale = (form, name) => { const v = form.elements[name].value; return v === 'na' ? null : Number(v); };

  const header = (title) => $('div', { class: 'bar' }, $('h2', {}, title), $('div', {}, $('span', { class: 'muted' }, state ? `${state.rater} · ${Math.min(state.idx + 1, steps.length)}/${steps.length} ` : ''), state ? $('button', { class: 'secondary', onclick: download }, '내 응답 JSON 다운로드') : ''));
  const rubric = () => $('details', {}, $('summary', {}, '채점 기준 보기'), $('pre', {}, BLIND.rubric_md));

  const render = () => {
    app.replaceChildren();
    if (!BLIND || !BLIND.problems) { app.append($('p', { class: 'err' }, '평가 데이터가 없습니다. 연구자가 run.py export-human을 다시 실행해야 합니다.')); return; }
    if (!state) return renderStart();
    const step = steps[state.idx];
    if (step.type === 'problem') return renderProblem(step);
    if (step.type === 'solution') return renderSolution(step);
    if (step.type === 'guess') return renderGuess();
    return renderDone();
  };

  const renderStart = () => {
    const form = $('form', { onsubmit: (e) => { e.preventDefault(); const code = form.elements.code.value.trim(); if (!BLIND.raters.includes(code)) { form.querySelector('.err').textContent = '등록되지 않은 평가자 코드입니다.'; return; } steps = buildSteps(code); state = load(code) || { rater: code, idx: 0, ratings: {} }; if (state.idx >= steps.length) state.idx = steps.length - 1; render(); } },
      $('p', {}, '연구자에게 받은 평가자 코드를 입력하세요. 같은 브라우저에서 다시 열면 이어서 할 수 있습니다.'),
      $('input', { name: 'code', autocomplete: 'off', required: '' }), ' ', $('button', { type: 'submit' }, '시작'), $('p', { class: 'err' }));
    app.append($('h1', {}, '문제·풀이 블라인드 평가'), $('div', { class: 'card' }, form), rubric());
  };

  const commit = (row) => { state.ratings[row.target_type + ':' + row.target_id] = row; state.idx += 1; save(state); mirror(row); render(); window.scrollTo(0, 0); };

  const renderProblem = ({ p }) => {
    const prev = state.ratings['problem:' + p.id];
    const form = $('form', { onsubmit: (e) => { e.preventDefault(); commit({ rater: state.rater, target_type: 'problem', target_id: p.id, clarity: readScale(form, 'clarity'), difficulty: readScale(form, 'difficulty'), want_to_solve: readScale(form, 'want_to_solve'), richness_list: form.elements.richness.value.split('\n').map(s => s.trim()).filter(Boolean), known_problem: form.elements.known.value === 'na' ? null : form.elements.known.value === 'yes', created_at: nowIso() }); } },
      scale('clarity', '명확성 (1~5)'), scale('difficulty', '난이도 (1~5)'),
      $('fieldset', {}, $('legend', {}, '풍요로움: 이 문제가 풀리면 쉬워지거나 따라오는 다른 문제 (한 줄에 하나, 없으면 비움)'), $('textarea', { name: 'richness' })),
      scale('want_to_solve', '풀고 싶은 정도 (1~5)'),
      $('fieldset', { class: 'scale' }, $('legend', {}, '이미 알려진 문제·정리와 사실상 같은가'), ...[['yes', '예'], ['no', '아니오'], ['na', '판단 불가']].map(([v, t]) => $('label', {}, $('input', { type: 'radio', name: 'known', value: v, required: '' }), ' ' + t))),
      $('button', { type: 'submit' }, '저장하고 다음'));
    app.append(header('문제 평가'), $('div', { class: 'card' }, $('h3', {}, '문제'), mathBlock(p.statement), p.finite_form ? $('div', {}, $('h4', {}, '유한 인스턴스'), mathBlock(p.finite_form)) : '', $('h4', {}, '제시된 중요성'), mathBlock(p.why_important)), rubric(), $('div', { class: 'card' }, form));
    if (prev) { for (const k of ['clarity', 'difficulty', 'want_to_solve']) form.elements[k].value = prev[k] === null ? 'na' : String(prev[k]); form.elements.richness.value = (prev.richness_list || []).join('\n'); form.elements.known.value = prev.known_problem === null ? 'na' : (prev.known_problem ? 'yes' : 'no'); }
  };

  const renderSolution = ({ p, s }) => {
    const prev = state.ratings['solution:' + s.id];
    const form = $('form', { onsubmit: (e) => { e.preventDefault(); const u = form.elements.understandable.value; commit({ rater: state.rater, target_type: 'solution', target_id: s.id, correctness: readScale(form, 'correctness'), clarity_sol: readScale(form, 'clarity_sol'), understandable: u === 'na' ? null : u === 'yes', created_at: nowIso() }); } },
      scale('correctness', '정확성 (1~5)'), scale('clarity_sol', '명료성 (1~5)'),
      $('fieldset', { class: 'scale' }, $('legend', {}, '이해 가능 여부: 핵심 아이디어를 자기 말로 다시 설명할 수 있는가'), ...[['yes', '예'], ['no', '아니오'], ['na', '판단 불가']].map(([v, t]) => $('label', {}, $('input', { type: 'radio', name: 'understandable', value: v, required: '' }), ' ' + t))),
      $('button', { type: 'submit' }, '저장하고 다음'));
    app.append(header('풀이 평가'), $('div', { class: 'card' }, $('details', {}, $('summary', {}, '문제 다시 보기'), mathBlock(p.statement), p.finite_form ? mathBlock(p.finite_form) : ''), $('h3', {}, '풀이'), mathBlock(s.text), s.candidate != null ? $('div', {}, $('h4', {}, '제출된 답(candidate)'), $('pre', { class: 'math' }, JSON.stringify(s.candidate))) : ''), rubric(), $('div', { class: 'card' }, form));
    if (prev) { for (const k of ['correctness', 'clarity_sol']) form.elements[k].value = prev[k] === null ? 'na' : String(prev[k]); form.elements.understandable.value = prev.understandable === null ? 'na' : (prev.understandable ? 'yes' : 'no'); }
  };

  const renderGuess = () => {
    const sel = (opts) => { const s = $('select', {}); for (const [v, t] of opts) s.append($('option', { value: v }, t)); return s; };
    const P_OPTS = [['unknown', '모름'], ['human', '사람'], ['ai_low', 'AI(하위 등급)'], ['ai_mid', 'AI(중위 등급)'], ['ai_high', 'AI(상위 등급)']];
    const S_OPTS = P_OPTS.filter(([v]) => v !== 'human');
    const rows = [];
    const list = $('div', {});
    for (const p of BLIND.problems) { const sp = sel(P_OPTS); rows.push(['problem', p.id, sp]); list.append($('div', { class: 'card' }, $('div', { class: 'muted' }, '문제 ' + p.id), mathBlock(p.statement.slice(0, 240)), $('label', {}, '출처 추측: ', sp), ...p.solutions.map(s => { const ss = sel(S_OPTS); rows.push(['solution', s.id, ss]); return $('div', {}, $('span', { class: 'muted' }, '풀이 ' + s.id + ' '), $('label', {}, '출처 추측: ', ss)); }))); }
    const finish = (apply) => { if (apply) for (const [tt, id, s] of rows) { const r = state.ratings[tt + ':' + id]; if (r) r.source_guess = s.value; } state.idx += 1; save(state); render(); window.scrollTo(0, 0); };
    app.append(header('출처 추측 (선택)'), $('p', {}, '각 문제와 풀이를 누가 만들었을지 추측해 주세요. 건너뛰어도 됩니다.'), list, $('div', { class: 'bar' }, $('button', { onclick: () => finish(true) }, '저장하고 완료'), $('button', { class: 'secondary', onclick: () => finish(false) }, '건너뛰기')));
  };

  const renderDone = () => { app.append(header('완료'), $('div', { class: 'card' }, $('p', {}, '수고하셨습니다. 아래 버튼으로 응답 파일을 내려받아 연구자에게 보내 주세요.'), $('button', { onclick: download }, '내 응답 JSON 다운로드'), ' ', $('button', { class: 'secondary', onclick: () => { state.idx = 0; save(state); render(); } }, '처음부터 다시 보기'))); };

  render();
})();
</script>
</body>
</html>
```

- [ ] **Step 3: Render the page from dry-run data and check it in the browser**

Copy `eval_page/template.html` to `%TEMP%\page_try\eval_page\template.html` (export looks for the template at `data_dir.parent/eval_page/`), then:
```bash
python run.py --data-dir %TEMP%\page_try\data export-human --raters R1,R2
```
Expected: prints the blind.json path and writes `%TEMP%\page_try\eval_page\index.html`.

Open that `index.html` with the built-in browser (`preview_start` or `navigate` with a `file:///` URL). Verify, and fix anything that fails:
1. Wrong code → error text; `R1` → first problem screen; header shows `R1 · 1/N`.
2. Submitting a problem requires all three scales; textarea lines become `richness_list`.
3. Reload the page, enter `R1` again → resumes at the same step.
4. Entering `R2` yields a different problem order than `R1`.
5. After the last solution the guess screen appears; "건너뛰기" leads to the done screen; the download produces `ratings_R1.json` whose rows import cleanly:
```bash
python run.py --data-dir %TEMP%\page_try\data import-human <downloads>\ratings_R1.json
```
Expected: `import-human: <k> new record(s)`.
6. A statement containing `$x^2$` renders as math (edit one statement in `%TEMP%\page_try\data\problems.jsonl`, re-export, reload). At 375px width there is no horizontal scroll.

- [ ] **Step 4: Commit**

```bash
git add eval_page/template.html
git commit -m "Add blind human evaluation page template

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 10: `analyze.py`

**Files:**
- Create: `analyze.py`
- Modify: `selfcheck.py` (add `check_analyze`)

**Interfaces:**
- Consumes: `pipeline.all_problems`, `store.read_jsonl`, `llm.GRADE`.
- Produces: `analyze.main(data_dir=Path("data"), out=Path("results")) -> dict[str, DataFrame]` with keys `q_g, kruskal, ladder_ceiling, cannot_judge, human_ai_agreement, kendall_w, self_preference`; files `results/<key>.csv`, `results/metrics.md`, `results/richness_by_source.png`.

- [ ] **Step 1: Install the analysis dependencies**

```bash
python -m pip install -r requirements.txt
```

- [ ] **Step 2: Write the failing check**

Append to `selfcheck.py` and add to `CHECKS` after `check_roundtrip`:

```python
def check_analyze(tmp: Path, data: Path) -> None:
    import analyze
    t = analyze.main(data, tmp / "results")
    ai = t["q_g"].loc["ai"]
    assert [ai.loc[s, "richness"] for s in ("sonnet", "opus", "fable")] == [1.0, 2.0, 3.0], ai
    lad = t["ladder_ceiling"].set_index("generator")
    assert lad.loc["sonnet", "ladder"] == 1.0, lad
    assert lad.loc["fable", "ladder"] != lad.loc["fable", "ladder"], "fable has no upper model → NaN"
    assert set(t["self_preference"]["rater"]) == {"sonnet", "opus", "fable"}
    assert (tmp / "results" / "metrics.md").exists() and (tmp / "results" / "q_g.csv").exists()
    assert not t["cannot_judge"].empty, "human ratings from check_roundtrip must appear"
```

- [ ] **Step 3: Run it to verify it fails**

Run: `python selfcheck.py` → `ModuleNotFoundError: No module named 'analyze'`

- [ ] **Step 4: Implement analyze.py**

```python
"""Metrics from spec §11. Usage: python analyze.py [--data-dir data] [--out results]"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

import llm
import pipeline
from store import now, read_jsonl

PROBLEM_ITEMS = ["clarity", "difficulty", "richness", "want_to_solve"]
SOLUTION_ITEMS = ["correctness", "clarity_sol"]
NULLABLE = {"problem": ["clarity", "difficulty", "want_to_solve"],
            "solution": ["correctness", "clarity_sol", "understandable"]}


def load(data_dir: Path):
    P = pd.DataFrame(pipeline.all_problems(data_dir))
    S = pd.DataFrame(read_jsonl(data_dir / "solutions.jsonl"))
    R = pd.DataFrame(read_jsonl(data_dir / "ratings.jsonl"))
    V = pd.DataFrame(read_jsonl(data_dir / "verifications.jsonl"))
    if R.empty:
        raise SystemExit("no ratings yet; run eval or import-human first")
    R["richness"] = R["richness_list"].apply(lambda x: len(x) if isinstance(x, list) else None) if "richness_list" in R else None
    psrc = P.set_index("id")["source"]
    actor = psrc.copy()
    if not S.empty:
        S["source"] = S["problem_id"].map(psrc)
        psrc = pd.concat([psrc, S.set_index("id")["source"]])
        actor = pd.concat([actor, S.set_index("id")["solver"]])
    R["source"] = R["target_id"].map(psrc)   # generator of the problem behind the target
    R["actor"] = R["target_id"].map(actor)   # who wrote the target itself (generator or solver)
    R["grade"] = R["source"].map(llm.GRADE)
    return P, S, R, V


def q_g(R):
    prob = R[R.target_type == "problem"]
    return prob.groupby(["rater_type", "source"])[PROBLEM_ITEMS].mean().round(2)


def kruskal(R):
    rows = []
    prob = R[(R.target_type == "problem") & R.grade.notna()]
    for rt, sub in prob.groupby("rater_type"):
        for item in PROBLEM_ITEMS:
            groups = [g[item].dropna().astype(float).values for _, g in sub.groupby("grade")]
            groups = [g for g in groups if len(g)]
            if len(groups) < 2:
                continue
            try:
                h, p = stats.kruskal(*groups)
            except ValueError:  # all values identical
                h, p = float("nan"), float("nan")
            rows.append({"rater_type": rt, "item": item, "H": round(h, 3), "p": round(p, 4),
                         "medians_by_grade": [float(pd.Series(g).median()) for g in groups]})
    return pd.DataFrame(rows)


def success(S, V, R):
    """Per solution: 1.0/0.0/NaN. Verified → pass==1; otherwise claimed solved and mean correctness ≥ 4."""
    S = S.copy()
    v = V.set_index("solution_id")["verdict"] if not V.empty else pd.Series(dtype=object)
    corr = R[R.target_type == "solution"].groupby("target_id")["correctness"].mean()

    def f(s):
        if s["id"] in v.index and v[s["id"]] in ("pass", "fail"):
            return float(v[s["id"]] == "pass")
        c = corr.get(s["id"], float("nan"))
        if pd.isna(c):
            return float("nan")
        return float(s.get("claimed_status") == "solved" and c >= 4)

    S["success"] = S.apply(f, axis=1)
    S["verified"] = S["id"].isin(v.index)
    return S


def ladder_ceiling(S):
    S = S[S["source"].isin(llm.GRADE)].copy()
    S["solver_grade"] = S["solver"].map(llm.GRADE)
    rows = []
    for g, grp in S.groupby("source"):
        gg = llm.GRADE[g]
        own = grp[grp.solver == g].success.mean()
        upper = grp[grp.solver_grade > gg].success.mean()
        lower = grp[grp.solver_grade < gg].success.mean()
        rows.append({"generator": g, "self_success": own, "upper_success": upper, "lower_success": lower,
                     "ladder": upper - own, "ceiling": lower, "n_verified": int(grp.verified.sum())})
    return pd.DataFrame(rows).round(3)


def cannot_judge(R):
    hum = R[R.rater_type == "human"]
    rows = []
    for tt, cols in NULLABLE.items():
        sub = hum[hum.target_type == tt]
        for src, grp in sub.groupby("source"):
            rows.append({"target_type": tt, "source": src, "n_ratings": len(grp),
                         "cannot_judge_rate": round(float(grp[cols].isna().values.mean()), 3)})
    df = pd.DataFrame(rows)
    rho = None
    if not df.empty:
        t = df[df["source"].isin(llm.GRADE)]
        if len(t) >= 3:
            rho = stats.spearmanr(t["source"].map(llm.GRADE), t["cannot_judge_rate"])
    return df, rho


def human_ai_agreement(R):
    rows = []
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = R[R.target_type == tt]
        h = sub[sub.rater_type == "human"].groupby("target_id")[items].mean()
        a = sub[sub.rater_type == "ai"].groupby("target_id")[items].mean()
        j = h.join(a, lsuffix="_h", rsuffix="_a", how="inner")
        for it in items:
            pair = j[[f"{it}_h", f"{it}_a"]].dropna()
            if len(pair) >= 3:
                rho, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
                rows.append({"target_type": tt, "item": it, "n": len(pair), "spearman_rho": round(rho, 3), "p": round(p, 4)})
    return pd.DataFrame(rows)


def kendall_w(R):
    rows = []
    hum = R[R.rater_type == "human"]
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = hum[hum.target_type == tt]
        for it in items:
            if sub.empty or it not in sub:
                continue
            m = sub.pivot_table(index="target_id", columns="rater", values=it, aggfunc="first").dropna()
            n, k = m.shape
            if k >= 2 and n >= 2:
                rsum = m.rank().sum(axis=1)
                ssq = float(((rsum - rsum.mean()) ** 2).sum())
                rows.append({"target_type": tt, "item": it, "n_items": n, "n_raters": k,
                             "kendall_W": round(12 * ssq / (k ** 2 * (n ** 3 - n)), 3)})
    return pd.DataFrame(rows)


def self_preference(R):
    ai = R[(R.rater_type == "ai") & R["actor"].isin(llm.GRADE)]
    rows = []
    for rater, grp in ai.groupby("rater"):
        for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
            sub = grp[grp.target_type == tt]
            if sub.empty:
                continue
            own, other = sub[sub.actor == rater][items].mean(), sub[sub.actor != rater][items].mean()
            rows.append({"rater": rater, "target_type": tt, **{f"bias_{it}": round(own[it] - other[it], 3) for it in items}})
    return pd.DataFrame(rows)


def main(data_dir: Path = Path("data"), out: Path = Path("results")) -> dict:
    P, S, R, V = load(data_dir)
    out.mkdir(parents=True, exist_ok=True)
    S = success(S, V, R) if not S.empty else S
    cj, rho = cannot_judge(R)
    tables = {"q_g": q_g(R), "kruskal": kruskal(R),
              "ladder_ceiling": ladder_ceiling(S) if not S.empty else pd.DataFrame(),
              "cannot_judge": cj, "human_ai_agreement": human_ai_agreement(R),
              "kendall_w": kendall_w(R), "self_preference": self_preference(R)}
    md = ["# Metrics", f"generated {now()}", "",
          "success for unverified solutions = claimed_status solved AND mean correctness >= 4 (see n_verified).", ""]
    for name, df in tables.items():
        df.to_csv(out / f"{name}.csv", encoding="utf-8")
        md += [f"## {name}", df.to_string() if not df.empty else "_no data_", ""]
    if rho is not None:
        md += [f"grade vs cannot_judge_rate: spearman rho={rho.statistic:.3f}, p={rho.pvalue:.4f}", ""]
    (out / "metrics.md").write_text("\n".join(md), encoding="utf-8")
    prob = R[(R.target_type == "problem") & R.richness.notna()]
    if not prob.empty:
        ax = prob.boxplot(column="richness", by="source")
        ax.set_title("richness by generator"); plt.suptitle("")
        plt.savefig(out / "richness_by_source.png", dpi=120, bbox_inches="tight"); plt.close("all")
    return tables


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--out", type=Path, default=Path("results"))
    a = ap.parse_args()
    main(a.data_dir, a.out)
    print(f"wrote {a.out / 'metrics.md'}")
```

- [ ] **Step 5: Run the check**

Run: `python selfcheck.py` → `ok  check_analyze`, `selfcheck OK`. If an assertion fails, inspect the returned table and fix the function, not the assertion.

- [ ] **Step 6: Commit**

```bash
git add analyze.py selfcheck.py
git commit -m "Add metric analysis with nonparametric tests

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 11: README and end-to-end dry run

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Write the full README**

```markdown
# 학자연 실험 환경

「AI는 지식폭발을 야기할 것인가」 본 실험(생성 → 풀이 → 평가) 도구. 설계 문서: `docs/superpowers/specs/`, 구현 계획: `docs/superpowers/plans/`.

## 0. 준비
- Python 3.14, `python -m pip install -r requirements.txt` (분석용 pandas·scipy·matplotlib)
- Claude Code CLI 로그인(Max 플랜): 터미널에서 `claude` 실행 후 `/login`
- `python run.py probe` → 세 모델이 각각 `ok: true`를 내고 `saw_other_instructions: false`여야 한다.

## 1. 자료 준비
- `context/<이름>.md` — 컨텍스트 팩. 규격은 `context/README.md`.
- `human_problems.jsonl` — 인간 대조군 문제. `human_problems.example.jsonl`을 복사해 내용을 바꾼다. 컨텍스트 팩과 겹치지 않게.
  - id는 평가자에게 보이므로 모델 문제와 같은 불투명 id를 쓴다: `python -c "from store import new_id; print(new_id('P'))"`.
  - `why_important`도 평가자에게 보인다. 출처·문제 번호·URL은 쓰지 말고 `note` 필드에 적는다(`note`는 내보내지 않음). `export-human`이 위반을 발견하면 거부한다.

## 2. 실행 (모든 명령은 재실행 시 끝난 항목을 건너뜀)
```bash
python run.py gen --context context/additive_comb.md --kind open --n 5
python run.py gen --context context/additive_comb.md --kind checkable --n 3
python run.py solve
python run.py eval
```
사용량 한도로 `STOPPED`가 뜨면 기다렸다가 같은 명령을 다시 친다.

## 3. 기계 검증
`checkers/P-xxxxxx.py`를 열어 읽고, 맞으면 첫 줄을 `# REVIEWED`로 바꾼다. 그 뒤:
```bash
python run.py verify
```
체커를 고친 뒤 다시 검증하려면 `data/verifications.jsonl`에서 그 풀이의 행을 지우고 다시 실행한다(판정은 자동으로 갱신되지 않음). 검토한 체커는 외부 프로세스를 띄우지 않아야 한다.

## 4. 인간 평가
```bash
python run.py export-human --raters R1,R2,R3
```
→ `eval_page/index.html`을 Artifact로 게시(또는 파일을 그대로 전달). 평가자는 코드를 입력해 평가하고 마지막에 `ratings_R1.json`을 내려받아 보낸다.
배포 전에 export를 고정한다: `export-human`을 다시 돌리면 `generated_at`이 바뀌어 평가자의 진행 상태가 처음으로 돌아간다. 평가 중에는 다시 내보내지 않는다.
```bash
python run.py import-human ratings_R1.json
```

## 5. 분석
```bash
python analyze.py
```
→ `results/metrics.md`, CSV, `richness_by_source.png`.

## 6. 점검·시험 가동
```bash
python selfcheck.py
python run.py --dry-run --data-dir tmp_dry gen --context context/additive_comb.md --kind open --n 1
```
`--dry-run`은 모델 대신 가짜 응답을 쓴다.

## 데이터 파일
`data/problems.jsonl`, `solutions.jsonl`, `ratings.jsonl`, `verifications.jsonl`, `failures.jsonl`, `raw/<stage>/*.json`(호출 원본). 필드 정의는 설계 문서 5절.

## 한계
temperature 고정 불가(CLI), 타사 모델 자동 호출 불가(수동 입력은 `source` 자유 텍스트로), Lean 4 미지원.
```

- [ ] **Step 2: Full dry run through the CLI**

```bash
python selfcheck.py
python run.py --help
```
Expected: `selfcheck OK`; help lists `gen solve eval export-human import-human verify probe selfcheck`.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Write README with the end-to-end procedure

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 12: Context pack draft (research content, not code)

**Files:**
- Create: `context/additive_comb.md` (marked `DRAFT`), `human_problems.jsonl`

**Roles:** a Sonnet subagent with web access drafts; an Opus subagent verifies every statement against its cited source and checks that no `human_problems.jsonl` problem appears in the pack.

- [ ] **Step 1: Collect sources**

Use `https://www.erdosproblems.com/tags/additive combinatorics`, `/tags/sidon sets`, `/tags/additive basis`, `/tags/arithmetic progressions` (tag pages; the site lists 1221 problems; per-problem pages are `/<number>`). Collect (a) 8–12 problems marked solved in 2023–2026 with the solving paper (arXiv id) and (b) 6–10 problems still open in the same tags. For each solved one, fetch the arXiv abstract to state the theorem precisely.

- [ ] **Step 2: Write `context/additive_comb.md`**

Format exactly as `context/README.md` specifies: `# DRAFT — ...`, `## Definitions`, 8–12 `## Result: <title>` sections each with `Statement.`, `Proof idea.` (one or two sentences), `Source: <authors>, <year>, arXiv:<id>, Erdős #<n>`, then `## Format examples` with 2–3 Erdős-style statements that are **not** in `human_problems.jsonl`.

- [ ] **Step 3: Write `human_problems.jsonl`**

One line per open problem from Step 1(b), following `human_problems.example.jsonl` (ids are opaque hex like model ids — generate each with `python -c "from store import new_id; print(new_id('P'))"`, never a readable prefix such as `P-h…`, because evaluators see ids; `source: "human"`; the statement in English with LaTeX, copied faithfully and briefly). **Blinding rule:** `why_important` is shown to evaluators, so write it in the same register as the gen prompt asks of models (what would follow if solved, why it is not routine) and never name the source, problem number or URL there; put `"Erdős problem #<n>, erdosproblems.com/<n>"` in the `note` field, which `export_human` never exports.

<!-- moved to Amendments: Task 3 (review round 1, plan decisions) -->
<!-- original text follows for the record -->
<!-- **Task 3 (review round 1, plan decisions):** `rubric.md` — "판단 불가" applies to the 1–5 items and to `known_problem` (예/아니오/판단 불가); an empty `richness_list` means 0, not "cannot judge"; correctness is judged against the finite instance when one is given. `eval_problem.md` — `known_problem` is true/false/null; the "do not guess the author" sentence is dropped from both eval prompts. `human_problems.example.jsonl` — generic placeholder statement, `why_important` in consequence register, new `note` field for the source (never exported). `context/README.md` — generic example without a specific (and possibly misattributed) theorem. `check_prompts` asserts the exact placeholder set per prompt and that the example's `why_important` names no source. Downstream: `EVAL_PROBLEM_PROPS.known_problem` is `["boolean","null"]` (Task 4), `_clean_field` keeps bool-or-null (Task 8), the page's known_problem control is 예/아니오/판단 불가 radios (Task 9). -->

- [ ] **Step 4: Check**

```bash
python -c "import pipeline,pathlib; t,r=pipeline.parse_context(pathlib.Path('context/additive_comb.md')); print(len(r),'results')"
python -c "import re; from store import read_jsonl; from pathlib import Path; rows=read_jsonl(Path('human_problems.jsonl')); ids=[r['id'] for r in rows]; assert len(set(ids))==len(ids) and all(re.fullmatch(r'P-[0-9a-f]{6}', r['id']) and r['source']=='human' and 'erdosproblems' not in r['why_important'].lower() and 'http' not in r['why_important'].lower() and not re.search(r'problem\s*#?\s*\d+', r['why_important'], re.I) and r.get('note') for r in rows); print(len(rows),'human problems, blinding ok')"
```
Expected: 8–12 results, 6–10 human problems. Opus review: every `Result:` statement matches its source; no overlap between pack and human problems; no open problem leaked into `## Format examples`.

- [ ] **Step 5: Commit**

```bash
git add context/additive_comb.md human_problems.jsonl
git commit -m "Add draft additive combinatorics context pack and human control problems

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 13: Publish the evaluation page and first live run (Fable, in the main session)

- [ ] **Step 1:** User runs `claude` → `/login` in a terminal. Then `python run.py probe`; confirm `ok: true` for all three aliases and `saw_other_instructions: false`. If `fable` is rejected as an alias, ask the user for the exact model id to put in `--models`.
- [ ] **Step 2:** `python run.py gen --context context/additive_comb.md --kind open --n 1` as a smoke test; read the three problems with the user; adjust prompts if the output is off, then run the full `--n`.
- [ ] **Step 3:** `python run.py export-human --raters R1,R2,R3,R4,R5`; publish `eval_page/index.html` with the Artifact tool (`capabilities: {db: {}}`, icon `clipboard`); record the URL in `README.md` §4; commit.

---

## Amendments during execution

- **Task 2 (review round 1):** `STOP_MARKERS` narrowed to phrases ("usage limit", "rate limit", "authenticate", "oauth", "/login", "not logged in", "credit balance") and matched only against the CLI `result` text; `_cli` catches `OSError`, uses `errors="replace"`, and keeps `stdout`/`stderr`/`returncode` in the error dict; `claude_exe()` refuses a `.cmd`/extensionless shim when the native exe is missing; `fake()` answers the probe schema; `run.py` reconfigures stdout to UTF-8, validates `--models` against `llm.GRADE`, and its STOPPED message no longer assumes an auth cause; `selfcheck.py` gains `check_llm_errors` (negative/positive marker cases) and `check_cli_offline` (patched `subprocess.run` asserting the exact flags, stdin prompt, `_cwd`, and error mapping). The committed files are the source of truth for Task 2.
- **Task 2 (review round 2):** `STOP_MARKERS` extended with the installed CLI's real strings ("you've hit your", "you've reached your", "usage credits", "extra usage", "spend limit", "invalid api key", "authentication error"); `llm.call` raises `CallFailed("answered by <ids>, not <alias>")` when `cli_output.modelUsage` names a model that does not contain the requested alias (the CLI can fall back to another model when a per-model limit is hit; such answers must never enter the data); `check_cli_offline` pins `errors="replace"`, `timeout`, and the mismatch guard.
- **Task 3 (review round 1, plan decisions):** `rubric.md` — "판단 불가" applies to the 1–5 items and to `known_problem` (예/아니오/판단 불가) and to `understandable`; an empty `richness_list` means 0; correctness is judged against the finite instance when one is given. `eval_problem.md` — `known_problem` is true/false/null; the "do not guess the author" sentence is dropped from both eval prompts. `human_problems.example.jsonl` — generic placeholder statement, `why_important` in consequence register, new `note` field for the source (never exported). `context/README.md` — generic example. `check_prompts` asserts the exact placeholder set per prompt and that the example's `why_important` names no source. Downstream: `EVAL_PROBLEM_PROPS.known_problem` is `["boolean","null"]` (Task 4), `_clean_field` keeps bool-or-null (Task 8), the page's known_problem control is 예/아니오/판단 불가 radios (Task 9), Task 12's check asserts blinding on the real `human_problems.jsonl`. Task 3's body in this plan is superseded by the committed files.
- **Task 4 (review round 1):** `llm.call` validates the parsed output against the schema (must be a dict containing every `required` key; otherwise `CallFailed`), so no stage ever merges unvalidated model output; `gen` copies only `schema["properties"]` keys into the row (never `id`/`source`/`gen_key`), writes the checker file **before** appending the row, and `one_line` collapses all whitespace (a lone `\r` could otherwise break out of the header comment); `parse_context` strips whole-line ``` and ~~~ fences before scanning headings (the brief's regex matched the README's fenced example). Tasks 5–6 copy only their schema keys (`**{k: out[k] for k in PROPS}`), already edited above. `check_gen` also asserts: real sections survive next to a fenced example, `context/README.md` is rejected, the three index-0 prompts are byte-identical, a `CallFailed` is recorded and retried, checkable rows have non-null `finite_form`/`checker_code`; `check_cli_offline` asserts a schema-invalid output raises `CallFailed`. (Round 2) the retry check runs in its own `tmp/flaky/data` dir so the shared `data` keeps exactly 9 problems for Tasks 5–8; `gen` records a failure instead of crashing when a checkable output's `finite_form`/`candidate_format`/`checker_code` is not a non-empty string.
- **Task 7 (review round 1):** `verify` maps to `pass`/`fail` only when the runner's return code is 0 (a checker that prints PASS then crashes is `error`); the gate line is read with `encoding="utf-8-sig", errors="replace"` and an empty file is treated as unreviewed; the candidate file is written with `ensure_ascii=False`; the subprocess decodes with `errors="replace"` (cp949 tracebacks); `check_verify_errors` (implementer-added, own data dir) also covers the PASS-then-crash case. Known limit, documented in code: on Windows a grandchild process can hold the pipes past the timeout. README (Task 11) documents that verdicts are not recomputed when a checker is edited: delete that solution's rows from `verifications.jsonl` to re-verify.
- **Task 8 (review round 1):** human problem ids were `P-h…`, which sorted last and showed on the guess screen — a source leak. Decision: every problem id is `P-` + 6 hex (human rows too, via `store.new_id`); `export_human` raises `SystemExit` naming the offending row if any problem id does not match `^P-[0-9a-f]{6}$`, any solution id `^S-[0-9a-f]{6}$`, ids are not unique, or a `why_important` contains `erdosproblems`, `http`, or `problem #N`; the example row id becomes hex and `check_prompts` asserts the hex pattern. Also: `_clean_field` uses `type(v) is int` (JSON `true` is not a score) and keeps only `str` items in `richness_list`; `import_human` dedupes rows within one file (last wins), skips non-dict rows, exits with a message when `blind.json` is missing, and accepts `created_at` only as a string; the template injection escapes every less-than sign as the JSON escape `<` (six ASCII characters: backslash, u, 0, 0, 3, c); `store.write_jsonl` writes a temp file then `os.replace` (atomic). `check_roundtrip` adds a human problem with a `note`, asserts `note` is absent from blind.json, and covers the bool-score and duplicate-key cases.
- **Task 9 (review round 1):** the guess screen listed each problem's solutions in export order, which is solver order (sonnet, opus, fable) — a solver leak. Decisions: `export_human` sorts each problem's `solutions` by id (opaque hex), asserted in `check_roundtrip`; the guess screen is built from the rater's shuffled `steps` and shows a 160-character excerpt of each solution; `commit` preserves an existing `source_guess`, and the guess selects are prefilled from stored rows; the localStorage key is `hakja:<code>:<BLIND.generated_at>` so a re-export starts fresh (README: freeze the export before distributing); a `load` listener re-renders the current screen when KaTeX finishes loading; the PRNG comment is corrected (xmur3-style hash iterated, not mulberry32). CSS additions by the implementer (`color-scheme`, `--on-accent`, `--err`) are kept.
- **Task 10 (review round 1, statistics corrections):** Kendall's W uses the tie-corrected denominator `k²(n³−n) − kΣT_j` (NaN when 0); Kruskal–Wallis runs on per-problem means (one observation per `target_id`, not per rating) and reports `{grade: median}` plus the median range and `n_problems`, p formatted `.3g`; the cannot-judge table adds per-item `cj_<item>` columns and the grade-vs-null-share Spearman is computed per `target_type` over rating rows; `n_verified` counts only `pass`/`fail` verdicts; ladder/ceiling report `n_self`/`n_upper`/`n_lower`; `success` and agreement functions `reindex` missing columns so partial data (no solutions yet) does not crash; CSVs write the index only for `q_g`; the boxplot uses AI ratings only; `metrics.md` notes that mean correctness includes the solver's own rater; scipy constant-input warnings are silenced around the test calls. `check_analyze` adds a second human rater (R2) so Kendall's W is exercised, an `error` verification row so `n_verified` excludes it, and asserts `n_verified` per generator (sonnet 3, opus 0, fable 3).

## Self-review (done by the plan author)

- **Spec coverage:** §4 call layer → Task 2; §5 data model → Tasks 4–8 (fields match; `problems` has the extra `gen_key`, documented in Task 4's interface); §6 commands → Tasks 4–8 plus `probe`, `selfcheck`; §7 prompts → Task 3; §8 context pack → Tasks 3 (README) and 12; §9 page → Task 9 (db best-effort per the amended spec); §10 verify → Task 7; §11 analysis → Task 10; §12 error handling → `StopRun` in Task 2, `record_failure` in Task 4, import skips in Task 8, verify `error` verdicts in Task 7; §13 selfcheck → grows across Tasks 1–10; §14 limits → README in Task 11.
- **Type consistency:** `pipeline.system()` used in Tasks 4–6; `record_failure(data_dir, stage, target_id, model, err)` everywhere; `import_human` returns a count, `export_human` returns a Path; `analyze.main` returns the dict of DataFrames the check reads; `check_verify` relies on `probs_src` defined right after it; `report(a, n)` defined in Task 2 and used from Task 4 on.
- **Placeholders:** none; every step has its content or its exact command.
