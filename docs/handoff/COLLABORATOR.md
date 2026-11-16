# 협업자 인수인계: 실험을 이어서 돌리는 법

2026-11-16 기준입니다. 이 문서는 데스크톱 PC가 아닌 곳에서 실험을 이어 돌릴 협업자를 위한 것입니다. 숫자는 `python status.py`로 다시 확인하세요.

## 1. 이 실험이 묻는 것

연구 주제는 「AI는 지식폭발을 야기할 것인가」입니다. 세 모델(Sonnet < Opus < Fable 순의 성능 등급)이 가법 조합론 자료를 읽고 문제를 내고, 모든 문제를 풀고, 서로 채점합니다. 사람 평가자도 같은 채점표로 채점합니다. 계획서의 가설 셋을 반증 가능한 형태로 검증합니다.

- **H-P2:** 등급이 올라가도 문제의 "풍요로움"(풀리면 따라오는 다른 문제의 수)은 유의하게 오르지 않는다.
- **H-P3:** 낸 모델은 못 풀고 상위 모델은 푸는 문제가 존재한다.
- **H-P4:** 등급이 오를수록 사람 평가자의 "판단 불가" 비율이 오르고, 사람과 AI 평가의 일치도는 떨어진다.

자세한 설계는 `docs/handoff/hakjayeon_guide.html`(브라우저로 열기)과 설계서 `docs/superpowers/specs/2026-10-17-experiment-environment-design.md`에 있습니다.

## 2. 지금 어디까지 왔나 (2026-11-16)

| 단계 | 진행 |
|---|---|
| 문제 생성 | 끝남. 유효 31개(모델 22 + 사람이 낸 Erdős 대조군 9) |
| 풀이 | 87/93칸. 남은 6칸은 모두 Fable |
| AI 평가 | 230/345건. Sonnet, Opus 끝남. Fable 0건 |
| 체커 판정 | 16건(통과 3, 모두 `P-d6bfbe`) |
| 고컨텍스트 조건 | 설계 승인, **아직 한 번도 안 돌림**(`high_ctx2/` 폴더 없음) |
| 사람 평가 | 0건. 평가 자료 내보내기 전 |
| 사전 지정 문서 | 초안만 있음. 승인 대기 14개. 커밋 확정 전 |

**일정이 밀렸습니다.** `docs/plan/2026-11-10-7day-plan.md`의 7일 계획은 11-11에 고컨텍스트 출제와 Fable 4칸을 돌리고 11-17에 끝내는 것이었는데, 11-11 이후 실행된 것이 없습니다. 새 일정은 연구자(설계자)와 정한 뒤 시작하세요.

## 3. 처음 한 번 준비

1. **저장소 접근:** 비공개 저장소입니다. 연구자가 GitHub에서 협업자로 초대해야 받을 수 있습니다.
   ```bash
   git clone https://github.com/Economy0808/studentresearch.git
   ```
2. **파이썬:** 3.11 이상. `pip install -r requirements.txt`(pandas, scipy, matplotlib).
3. **Claude Code CLI:** 모델은 이 도구로 부릅니다. API 키가 아니라 Claude 구독 플랜(Max)으로 로그인해야 합니다(`claude` 실행 후 `/login`). 코드는 환경변수 `ANTHROPIC_API_KEY`를 일부러 지우고 부릅니다.
   - 지금까지의 호출은 모두 CLI 2.1.302였습니다. 자동 업데이트는 끄기를 권합니다(실행 창에서 `DISABLE_AUTOUPDATER=1`).
4. **자체 점검(모델 호출 없음):** `python -X utf8 selfcheck.py` → 마지막 줄 `selfcheck OK`.
5. **모델 확인(짧은 실제 호출 3번):** `python -X utf8 run.py probe`. 세 줄에 `claude-sonnet-5-5`, `claude-opus-5-5`, `claude-fable-5-1`이 찍혀야 합니다. 협업자 계정에서 `claude-fable-5-1`을 쓸 수 없으면 **실행하지 말고** 연구자에게 알리세요. 다른 버전으로 바꾸면 이미 끝난 칸과 비교할 수 없게 됩니다.

## 4. 꼭 지킬 규칙

- **한 번에 한 곳에서만 돌립니다.** 실험 원본이 두 곳에서 동시에 돌면 데이터가 갈라집니다. 돌리기 전에 연구자에게 "지금부터 내가 돌린다"고 알리고, 시작 전에 `git pull`, 끝나면 바로 커밋하고 `git push`합니다.
- **한 데이터 폴더에는 한 번에 명령 하나.** `data/`와 `high_ctx2/data/`는 서로 다른 폴더라 동시에 돌려도 됩니다.
- **설계 판단은 혼자 정하지 않습니다.** 숫자, 기준, 범위, 실행 조건을 바꾸는 일은 연구자에게 먼저 묻습니다. 결정 목록은 `docs/plan/2026-11-10-7day-plan.md`와 `docs/preregistration_2026-11-11.md`에 있습니다.
- **사전 지정 문서를 커밋하기 전에는 아래 5절의 실행을 시작하지 않습니다.** 결과를 보기 전에 판정 규칙을 적어 두는 문서라 순서가 중요합니다.
- **고컨텍스트 팩 `context/additive_comb_high_v2.md`는 한 글자도 고치지 않습니다.** 고치면 문제 생성이 처음부터 다시 돕니다.
- **남은 칸의 실행 조건을 바꾸지 않습니다.** 프롬프트, 모델, 60분 제한, 도구 없음, 기회 횟수(예산 초과 2번이면 "못 풂")는 그대로입니다.
- **`P-c2d5cd`의 Fable 풀이는 다시 돌리지 않습니다.** 안전 필터에 막혀 결측으로 닫기로 했습니다. 그래서 Fable 풀이는 늘 `--only`로 문제를 지정합니다. `--only` 없이 `solve`를 돌리면 이 칸이 다시 시도됩니다.
- **사람 평가 내보내기(`export-human`)는 한 번만.** 다시 하면 평가자 진행이 초기화됩니다.
- **한도:** Fable 주간 한도가 가장 빠듯합니다. 대화 세션을 Fable 모델로 두지 마세요(실험 몫이 줄어듭니다). 한도가 모자랄 때 자르는 순서는 ① `P-c2d5cd` ② `P-cbca09` ③ Fable의 풀이 평가 ④ 고컨텍스트 Fable 풀이입니다.
- **인용 금지:** 자기 평가를 뺀 난이도 p=0.035는 인용하지 않습니다.

## 5. 승인된 실행 순서와 명령

연구자가 11-10에 승인한 순서입니다. 날짜는 새 일정에 맞추세요.

```bash
# 1) 고컨텍스트 출제: 모델당 open 3문제, 모두 9문제 (새 폴더 high_ctx2/data가 생김)
python -X utf8 run.py --data-dir high_ctx2/data gen --context context/additive_comb_high_v2.md --kind open --n 3

# 2) H-P3를 가르는 Fable 풀이 4칸, 이 순서로 (한 칸 최대 60분)
python -X utf8 run.py --models fable solve --only P-5d88c3,P-e1102e,P-09b1eb,P-fd59f2

# 3) 체커 판정, 새 풀이에 대한 Sonnet·Opus 평가
python -X utf8 run.py verify
python -X utf8 run.py --models sonnet,opus eval

# 4) 고컨텍스트 풀이와 평가 (한도가 허락할 때)
python -X utf8 run.py --data-dir high_ctx2/data solve
python -X utf8 run.py --data-dir high_ctx2/data eval

# 5) Fable 평가 (문제 먼저 평가하고 풀이를 나중에 평가함. 한도가 모자라면 문제 평가가 끝난 뒤 Ctrl+C)
python -X utf8 run.py --models fable eval
```

- 모든 명령은 끝난 칸을 건너뛰므로, 중간에 끊겨도 같은 명령을 다시 돌리면 이어집니다.
- "5 consecutive failures"나 한도 메시지로 멈추면, 원인(인터넷, 로그인, 한도)을 확인하고 같은 명령을 다시 돌립니다. 인터넷 끊김은 기회 횟수에 들어가지 않습니다.
- 진행 확인: `python -X utf8 status.py`. 분석: `python -X utf8 analyze.py`.

**사람 평가:** 평가 묶음(결정 10)이 아직 정해지지 않았고, 내보낼 항목을 고르는 기능과 평가 페이지 수정이 아직 코드에 없습니다. 연구자와 정한 뒤 진행하세요. 추천안은 계획 문서의 "사람 평가 묶음"에 있습니다.

## 6. 파일 지도

| 파일 | 내용 |
|---|---|
| `run.py` | 명령 입구(gen, solve, eval, verify, export-human, import-human, probe) |
| `pipeline.py`, `llm.py`, `store.py` | 단계 실행, 모델 호출(정확한 모델 이름 고정), 기록 |
| `analyze.py`, `status.py`, `selfcheck.py` | 분석, 진행 현황, 자체 점검 |
| `prompts/` | 출제·풀이·평가 프롬프트와 채점표 |
| `context/` | 컨텍스트 팩(저컨텍스트 `additive_comb.md`, 고컨텍스트 `additive_comb_high_v2.md`) |
| `checkers/` | checkable 문제의 정답 확인 코드 |
| `data/` | 원자료(`*.jsonl`)와 호출 원본(`raw/`) |
| `human_problems.jsonl` | 사람이 낸 Erdős 대조군 9문제 |
| `eval_page/template.html` | 사람 평가 페이지 틀 |
| `CLAUDE.md` | Claude Code 세션이 자동으로 읽는 인계 규칙. 이 폴더에서 Claude Code를 열면 실험 내용을 바로 물어볼 수 있습니다 |
| `docs/plan/`, `docs/preregistration_2026-11-11.md` | 7일 계획과 결정 목록, 사전 지정 문서 초안 |

## 7. 알아 둘 것

- `data/raw/probe/fable*.json`에는 연구자 계정의 이메일이 모델 응답 속에 기록돼 있습니다. 밖으로 공유하지 마세요.
- 협업자 계정으로 돌리면 한도도 협업자 계정 기준입니다. Fable 한도 사용률을 실행 전후로 적어 두면 연구자가 일정을 잡기 쉽습니다.
- 출력 상한: Fable은 한 번에 64,000토큰까지 쓰고 잘리면 같은 호출 안에서 최대 3번 이어 써서 합계 256,000토큰까지 씁니다. Sonnet·Opus는 한 번에 128,000토큰입니다. "Fable만 절반 분량"이라고 쓰지 마세요.
