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
temperature 고정 불가(CLI), 타사 모델 자동 호출 불가(수동 입력은 `source` 자유 텍스트로), Lean 4 미지원. 분석의 `success` 판정에서 풀이 정확성 평균은 풀이한 모델 자신의 평가도 포함한다(자기편애 표 참조). Kendall's W는 평가자 2명일 때 (1+평균 ρ)/2이므로 0.5는 일치 없음에 해당한다.
