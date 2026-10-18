# 학자연 실험 환경

「AI는 지식폭발을 야기할 것인가」 본 실험(생성 → 풀이 → 평가) 도구. 설계 문서: `docs/superpowers/specs/`, 구현 계획: `docs/superpowers/plans/`.

## 0. 준비
- Python 3.14, `python -m pip install -r requirements.txt` (분석용 pandas·scipy·matplotlib)
- Claude Code CLI 로그인(Max 플랜): 터미널에서 `claude` 실행 후 `/login`
- `ANTHROPIC_API_KEY` 환경변수가 설정돼 있으면 안 된다(API 과금; 스크립트가 서브프로세스에서 제거하지만 셸에서도 비워 둘 것). 모든 명령은 프로젝트 폴더에서 실행한다.
- `python run.py probe` → 세 모델이 각각 `ok: true`를 내야 한다. `saw_other_instructions`는 아래 환경 정보 때문에만 `true`일 수 있다. probe 출력의 other_instructions_summary에는 Claude Code 고유의 환경 정보(OS, 작업 폴더, 날짜, 모델 이름)와 계정 이메일 식별 문구만 보여야 한다. 메모리·프로젝트 설명·MCP 안내가 보이면 호출 폴더나 플래그가 잘못된 것이다.

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
사용량 한도로 `STOPPED`가 뜨면 기다렸다가 같은 명령을 다시 친다. 시간 예산: 한 (문제, 모델) 쌍이 30분 제한에 두 번 걸리면 다음 실행에서 모델을 다시 부르지 않고 "시간 초과로 미해결" 행을 기록한다. 이 행은 평가·평가자 페이지에서 제외되고 분석에서는 실패(0)로 센다.

- 한 데이터 폴더에서는 한 번에 하나의 명령만 실행한다(`eval`과 `import-human`을 동시에 돌리면 평가 행이 사라질 수 있다).
- 단계가 읽는 입력(`context/*.md`, `prompts/`, `human_problems.jsonl`)은 그 단계가 끝날 때까지 고정한다. 컨텍스트 팩을 고치면 `context_id`가 바뀌어 모든 모델의 생성이 처음부터 다시 시작된다.
- `STOPPED: answered by …`는 모델 한도로 다른 모델이 대신 답한 경우다. 한도가 풀릴 때까지 기다리거나 `--models`로 나머지 모델만 계속 돌린다(`--models`는 하위 명령 앞에 쓴다: `python run.py --models sonnet,opus gen …`). `STOPPED: 5 consecutive failures`는 연속 5회 실패이므로 원인(로그인·네트워크·한도)을 해결한 뒤 다시 친다.
- 같은 항목이 계속 실패하면 `data/failures.jsonl`과 `data/raw/`의 원본을 본다.
- 손으로 고친 JSONL은 UTF-8이어야 하고, 비정상 종료 뒤에는 마지막 줄이 잘렸는지 확인한다.

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
(자동 검사는 사람 문제의 why_important에 대해 URL·erdosproblems·"problem #N"·"#N"만 본다.)
→ `eval_page/index.html`을 Artifact로 게시(또는 파일을 그대로 전달). 평가자는 코드를 입력해 평가하고 마지막에 `ratings_R1.json`을 내려받아 보낸다.
배포 전에 export를 고정한다: `export-human`을 다시 돌리면 `generated_at`이 바뀌어 평가자의 진행 상태가 처음으로 돌아간다. 평가 중에는 다시 내보내지 않는다.
```bash
python run.py import-human ratings_R1.json
```
새로 들어온 행과 덮어쓴 행의 수를 출력하고, `data/blind.json`에 없는 id의 행은 경고와 함께 그대로 둔다(오래된 export로 평가했는지 확인).

## 5. 분석
```bash
python analyze.py
```
→ `results/metrics.md`, CSV, `richness_by_source.png`.

## 6. 점검·시험 가동
```bash
python selfcheck.py
python run.py --dry-run --data-dir tmp_dry/data gen --context context/additive_comb.md --kind open --n 1
```
`--dry-run`은 모델 대신 가짜 응답을 쓴다. 진짜 데이터와 `checkers/`·`eval_page/` 같은 옆 폴더를 건드리지 않도록, 프로젝트 폴더 바로 아래의 데이터 폴더(기본 `data/`)에는 `--dry-run`이 거부된다. 시험이 끝나면 `tmp_dry/`는 지워도 된다.

## 데이터 파일
`data/problems.jsonl`, `solutions.jsonl`, `ratings.jsonl`, `verifications.jsonl`, `failures.jsonl`, `blind.json`(`export-human`이 쓰는 평가자용 내보내기), `raw/<stage>/*.json`(호출 원본). 필드 정의는 설계 문서 5절.

## 한계
temperature 고정 불가(CLI), 타사 모델 자동 호출 불가(수동 입력은 `source` 자유 텍스트로), Lean 4 미지원. 분석의 `success` 판정에서 풀이 정확성 평균은 풀이한 모델 자신을 뺀 AI 평가자들의 평균이다(자기편애 표는 같은 대상을 평가한 다른 AI 평가자 평균과의 편차). Kendall's W는 평가자 2명일 때(동점 없을 때) (1+평균 ρ)/2이므로 0.5는 일치 없음에 해당한다.
