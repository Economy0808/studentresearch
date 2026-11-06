# 실험 환경 설계: AI 문제 생성–풀이–평가 파이프라인

- 날짜: 2026-10-17
- 연구: 경기 조(이경재·박슬기), 「AI는 지식폭발을 야기할 것인가」 학생자율연구
- 대상: 계획서 2.2 본 실험(P2·P3·P4), 2.3 지표, 2.5 통제 사항을 실행하는 도구 환경

## 1. 목적과 범위

계획서의 3단계 실험(생성 → 풀이 → 평가)을 재현 가능하게 실행하고, 모든 원본 응답을 파일로 남기며, 계획서 2.3의 지표를 자동 계산한다.

포함:
- 세 등급 모델(Sonnet, Opus, Fable)로 문제 생성·풀이·AI 평가를 돌리는 명령줄 도구
- 인간 평가자용 블라인드 웹 평가 페이지(지금 구축, 평가자 섭외 후 접속)
- 기계 검증(Python 체커)
- 지표 계산과 비모수 통계

제외(14절): Lean 4 검증, 2.4 이해 실험, 타사 모델 자동 호출.

## 2. 확정된 결정

| 항목 | 결정 | 이유 |
|---|---|---|
| 모델 호출 | Claude Code CLI 헤드리스(`claude -p`), Max 플랜 | 계획서 예산이 Max x5 플랜. API 키 없음 |
| 인간 평가 양식 | 웹 페이지 1장(Claude Artifact, db 기능) | 순서 무작위·자동 수집·링크 하나로 배포 |
| 수학 분야 | 조합론·가법 정수론(Erdős 문제 밀집 영역) | 대조군(Erdős open 문제)과 최근 결과를 한 출처에서 확보, 유한 구성 문제로 변환 용이 |
| 산출물 언어 | 문제·풀이는 영어, 평가 UI는 한국어 | 수학 문헌 관례, 평가자는 영어 수학을 읽음 |
| 생성 문제 종류 | `open`(미해결 믿음) / `checkable`(유한 구성+체커) 두 종 | 진짜 난제만 있으면 P3 지표가 전부 0. checkable 종이 등급 경계 난이도를 제공 |

## 3. 구조

```
학자연/
  run.py                 # gen | solve | eval | export-human | import-human | verify | selfcheck
  analyze.py             # 지표 + 통계 → results/
  prompts/
    system.md            # 모든 호출에 공통인 짧은 시스템 프롬프트
    gen_open.md, gen_checkable.md, solve.md
    eval_problem.md, eval_solution.md
    rubric.md            # 채점표 원문. AI 평가 프롬프트와 인간 페이지가 같은 파일을 쓴다
  context/
    README.md            # 컨텍스트 팩 작성 규격(8절)
    additive_comb.md     # 컨텍스트 팩 초안(연구자 검토 대상)
  human_problems.jsonl   # 인간 대조군 문제(연구자가 채움). problems와 같은 스키마, source="human"
  checkers/
    <problem_id>.py      # gen이 자동 생성. 연구자가 검토 후 `# REVIEWED` 줄을 추가해야 verify가 실행
  data/
    problems.jsonl, solutions.jsonl, ratings.jsonl, verifications.jsonl, failures.jsonl
    raw/<stage>/<id>.json  # 호출별 원본(보낸 프롬프트 + CLI 출력 전체)
    blind.json           # export-human 산출물. 출처 제거된 평가용 데이터
  eval_page/index.html   # 인간 평가 페이지(blind.json 삽입 후 Artifact로 게시)
  results/               # analyze.py 산출물(CSV, PNG, metrics.md)
  docs/superpowers/specs/ # 이 문서
```

## 4. 모델 호출 레이어

모든 호출은 아래 한 형태다. `cwd`는 **프로젝트 밖의** 빈 임시 디렉터리(`%TEMP%/claude_cli_cwd/`)로 둔다: 프로젝트 안의 폴더에서 호출하면 Claude Code가 그 프로젝트의 자동 메모리(연구 설명이 들어 있음)를 첫 메시지에 붙인다(2026-10-18 probe로 확인). `--strict-mcp-config --mcp-config '{"mcpServers":{}}'`로 계정 수준 MCP 커넥터 안내도 제거한다. 남는 것은 Claude Code 고유의 환경 블록(OS, 작업 폴더, 날짜, 모델 이름)과 계정 이메일 식별 문구이며, 세 모델에 동일하고 실험 정보를 담지 않는다. `probe`가 매번 이를 보여 준다.

```
claude -p <user prompt> --model <sonnet|opus|fable> --output-format json
       --json-schema <단계별 스키마> --tools "" --system-prompt <prompts/system.md 내용>
       --no-session-persistence
```

- `--tools ""`: 파일 읽기·웹 검색 차단. 학습 데이터 오염 통제(2.5-4)에도 기여.
- `--json-schema`: 출력이 스키마를 따르므로 파싱 실패가 거의 없다. 실패 시 raw만 저장하고 `failures.jsonl`에 기록.
- 원본 저장: `data/raw/<stage>/<id>.json` = `{prompt, system, model, cli_version, started_at, cli_output}`.
- 멱등성: 이미 결과가 있는 (단계, 대상, 모델) 조합은 건너뛴다. 사용량 한도로 중단돼도 같은 명령을 다시 치면 이어진다.
- 한도 감지: CLI 응답이 `is_error`이고 메시지가 한도·인증 관련이면 그 자리에서 실행을 멈추고 이유를 출력한다(남은 호출을 실패로 태우지 않음).
- 등급 매핑: `GRADE = {sonnet: 1, opus: 2, fable: 3}` (run.py 상단 상수).
- 한계: temperature 조절 불가. 대신 `--n`으로 독립 호출을 반복한다. 모델 버전은 CLI가 가리키는 최신 alias이며 raw에 `modelUsage`가 남아 사후 확인 가능.

## 5. 데이터 모델 (JSONL, 한 줄 = 한 레코드)

**problems**
```
id            "P-" + 6자리 hex
source        "sonnet" | "opus" | "fable" | "human" | 기타 자유 텍스트(타사 모델 수동 입력용)
kind          "open" | "checkable"
context_id    컨텍스트 팩 파일명 + "-" + 내용 SHA-256 앞 8자리 (예: additive_comb-3fa9c1e2). 팩을 고치면 모든 모델의 생성 키가 새로 시작된다. human은 null 가능
focus         초점을 준 컨텍스트 섹션 제목 (8절)
statement, grounding, why_hard, why_important     문자열(영어, LaTeX 허용)
resembles_known        닮은 알려진 추측/정리 이름 또는 null
novelty_confidence     0~1
finite_form, candidate_format, checker_code       checkable만, 아니면 null
created_at    ISO 8601 UTC
```

**solutions**
```
id            "S-" + 6자리 hex
problem_id, solver
text          풀이 본문(영어)
claimed_status  "solved" | "partial" | "unsolved"
candidate     checkable 문제일 때 체커 입력(JSON), 아니면 null
created_at
```

**ratings** (AI·인간 공통)
```
rater         AI: 모델 alias, 인간: 평가자 코드(R1, R2, …)
rater_type    "ai" | "human"
target_type   "problem" | "solution"
target_id
# problem 항목
clarity, difficulty, want_to_solve     1~5 정수 또는 null(=판단 불가)
richness_list                           문자열 목록("이 문제가 풀리면 쉬워지는 다른 문제")
known_problem                           bool ("이미 알려진 문제와 동일")
# solution 항목
correctness, clarity_sol               1~5 또는 null
understandable                         true | false | null
# 인간만
source_guess   "human" | "ai_low" | "ai_mid" | "ai_high" | "unknown" | null
created_at
```
풍요로움 점수는 `len(richness_list)`. 판단 불가율은 null 비율.

**verifications**
```
solution_id, verdict  "pass" | "fail" | "error" | "na", log, created_at
```

**failures**: `{stage, target_id, model, error, created_at}`.

## 6. 파이프라인 명령

| 명령 | 입력 | 출력 | 비고 |
|---|---|---|---|
| `gen --context <file> --kind open\|checkable --n 5 [--models ...]` | 컨텍스트 팩 | problems, checkers/ | 모델 × n 호출. i번째 호출은 i번째 섹션에 초점 |
| `solve` | problems + human_problems | solutions | 모든 문제 × 3 모델. 풀이자는 출처를 받지 않음 |
| `eval` | problems, solutions | ratings(rater_type=ai) | 항목 하나당 호출 하나, 3 평가 모델. 출처 미포함 → 순서 효과 없음 |
| `export-human` | problems, solutions | data/blind.json | source·solver·grounding 제거. 평가 페이지에 삽입 |
| `import-human <json>` | 페이지에서 내려받은 JSON(5절 ratings 레코드의 배열) | ratings(rater_type=human) | 같은 (rater, target_id)는 최신으로 덮어씀 |
| `verify` | solutions(candidate), checkers/ | verifications | `# REVIEWED` 없는 체커는 건너뛰고 경고 |
| `selfcheck` | 없음 | 콘솔 | 13절 |

공통 옵션: `--dry-run`(가짜 모델), `--data-dir`(기본 `data/`).

## 7. 프롬프트 설계

세 모델에 **글자 하나까지 같은 프롬프트**를 준다. 파일은 `prompts/`에 두어 코드 수정 없이 고친다. `{placeholders}`는 run.py가 채운다.

**system.md**: "You are a research mathematician. You have no tools and no internet access. Respond only in the requested JSON." 수준의 짧은 고정 문장.

**gen_open.md** 요구 항목(=스키마 필드): `statement`(≤150 words, self-contained), `grounding`(컨텍스트의 어떤 결과를 확장하며 어디가 빈틈인지), `why_hard`(뻔한 접근과 그것이 막히는 이유), `why_important`, `resembles_known`, `novelty_confidence`. 지시: 컨텍스트에 있는 결과의 빈틈에서 문제를 끌어낼 것, 이름 붙은 유명 추측을 재진술하지 말 것, `{focus}` 섹션에 초점을 둘 것.

**gen_checkable.md**: 위 항목 + `finite_form`(유한 매개변수 n 등으로 구체화한 진술), `candidate_format`(풀이자가 제출할 JSON 형태 설명), `checker_code`(`def check(candidate) -> bool` 하나, 표준 라이브러리만, 10초 내 종료). 문제는 "풀리면 구성·반례를 제시하는 형태"로 한정.

**solve.md**: 문제 `statement`(checkable이면 `finite_form`, `candidate_format`도)만 준다. 출력: `text`, `claimed_status`, `candidate`(checkable만). 출처·생성 모델·grounding은 주지 않는다.

**eval_problem.md / eval_solution.md**: `rubric.md` 원문을 그대로 삽입하고 대상 하나를 준다. 모든 항목에 null(판단 불가) 허용을 명시. `known_problem` 체크 포함. 풀이 평가 시 문제 진술도 함께 제시.

**rubric.md**: 계획서 3단계 항목 그대로. 문제: 명확성·난이도·풍요로움(목록)·풀고 싶은 정도. 풀이: 정확성·명료성·이해 가능 여부. 각 1~5 척도의 기준 문장을 적는다. AI 프롬프트와 인간 페이지가 같은 파일을 읽어 "두 집단은 동일한 채점표"를 보장한다.

## 8. 컨텍스트 팩 규격 (`context/README.md`)

마크다운 한 파일. `## ` 2단계 헤더가 섹션이며 gen의 초점 로테이션 단위다.

1. `## Definitions` — 핵심 정의 1쪽
2. `## Result: <짧은 제목>` × 8~12개 — 정리 진술 + 한 줄 증명 아이디어 + 출처(연도). 2023~2026년 풀린 Erdős 문제와 arXiv 최신 결과 위주(오염 통제 2.5-4)
3. `## Format examples` — 문제 진술 형식 예시 2~3개(Erdős 스타일). **대조군으로 쓸 open 문제는 넣지 않는다.**

`gen --n k`는 i번째 호출에 `Result:` 섹션 중 i번째(개수 초과 시 순환)를 `{focus}`로 넣는다. 세 모델에 동일하게 적용되어 공정하고 문제 다양성을 확보한다.

초안 `context/additive_comb.md`는 erdosproblems.com과 arXiv에서 모아 작성하되 연구자 검토 전까지 "DRAFT" 표시를 유지한다. `human_problems.jsonl`에는 같은 분야의 open Erdős 문제를 넣는다(컨텍스트 팩과 겹치지 않게).

## 9. 인간 평가 페이지

단일 HTML(Artifact, `db` 기능). `blind.json`을 페이지에 삽입해 게시한다.

흐름:
1. 시작 화면: 평가자 코드 입력(허용 코드 목록은 페이지 상단 설정 상수). 코드가 순서 무작위화의 시드.
2. 문제 화면(한 문제씩): 진술 + why_important → 루브릭 4항목(각 "판단 불가"), `known_problem` 체크 → 이어서 그 문제의 풀이 3개를 섞인 순서로 한 풀이씩: 루브릭 3항목(각 "판단 불가").
3. 모든 문제 종료 후 출처 추측 화면: 각 문제 `human/ai_low/ai_mid/ai_high/unknown`, 각 풀이 `ai_low/ai_mid/ai_high/unknown`. 건너뛰기 허용(본 자료 손실 방지).
4. 완료 화면.

저장: 항목마다 즉시 브라우저 localStorage에 저장(같은 브라우저로 재접속 시 이어서). 완료 화면과 모든 화면 상단에 "내 응답 JSON 다운로드" 버튼 → 평가자가 파일을 연구자에게 보냄 → `run.py import-human`. Artifact db는 **보조**로만 쓴다: db 타입 정의상 공개 링크로 들어온 외부 평가자(연구자 개인 플랜 밖)는 db에 쓸 수 없으므로, `claude.use("db")`가 null이 아니고 쓰기가 성공할 때만 같은 레코드를 `ratings/<rater>:<target_id>`에 복제한다. 실패는 무시한다. 수집의 정본은 JSON 파일이다.

렌더링: KaTeX(cdnjs)로 LaTeX 표시. 휴대폰 폭에서도 읽히는 단일 열 레이아웃.

평가자 섭외 전: 페이지는 지금 게시하고, 섭외 후 `export-human`을 다시 돌려 최신 데이터로 재게시한다.

## 10. 기계 검증

- gen이 checkable 문제의 `checker_code`를 `checkers/<problem_id>.py`로 저장한다(헤더에 문제 진술 주석).
- 연구자가 코드를 읽고 맞다고 판단하면 첫 줄에 `# REVIEWED`를 추가한다. 이 줄이 없으면 verify는 그 체커를 실행하지 않는다(모델이 쓴 코드를 검토 없이 실행하지 않기 위한 유일한 안전장치).
- verify는 체커를 `python -I` 서브프로세스로, 60초 타임아웃으로, 풀이의 `candidate`에 대해 실행한다. 결과: pass / fail / error(예외·타임아웃) / na(candidate 없음).
- 계획서 2.5-1: verify 결과는 평가자 정확성 점수와 대조하는 기준값이 된다(analyze).

## 11. 분석 (`analyze.py`)

입력은 data/*.jsonl, 출력은 `results/metrics.md`(표), CSV, PNG.

| 지표 | 계산 | 전제 |
|---|---|---|
| Q(G) | source별 문제 항목(명확성·난이도·풍요로움 개수·풀고 싶은 정도) 평균. 인간·AI 평가자 분리 표시 | P2 |
| 사다리 | 생성 모델 g의 문제에 대해 success(상위 모델) − success(g). success는 checkable: verify pass율, open: `claimed_status=solved`이고 평가자 정확성 평균 ≥ 4 | P3 |
| 천장 | 상위 모델 문제에 대한 하위 모델 success율 | P3 |
| 판단 불가율 | source 등급별, 인간 평가자의 null 비율(항목별·전체) | P4 |
| 인간–AI 일치도 | 같은 대상에 대한 인간 평균 점수 vs AI 평균 점수 Spearman ρ | P4 |
| 인간 간 일치도 | Kendall's W (항목별) | P4 |
| 자기편애 | AI 평가자 r에 대해 mean(score | source==r) − mean(score | source≠r) | 2.5-2 |

검정: Q(G) 항목별 Kruskal–Wallis(등급 3군), 등급 vs 판단 불가율 Spearman. 표본이 작으므로 p값과 함께 효과 크기(중앙값 차)를 같이 적는다. 라이브러리: pandas, scipy, matplotlib.

## 12. 오류 처리

- CLI 비정상 종료·스키마 불일치: raw 저장, failures 기록, 다음 항목으로. 종료 시 실패 요약 출력. 재실행 시 실패 항목만 다시 시도.
- 한도·인증 오류: 즉시 중단(4절).
- import-human: 스키마 검증 후 병합. 허용되지 않은 rater 코드는 경고하고 건너뜀.
- verify: 체커 예외는 error로 기록하고 로그 보존. 풀이 실패로 간주하지 않음.

## 13. 테스트

`python run.py selfcheck` 하나:
1. 임시 data-dir에 `--dry-run`으로 gen(open 2 + checkable 1) → solve → eval을 돌린다. 가짜 모델은 스키마에 맞는 결정적 응답을 등급에 따라 다르게 낸다(예: 상위 등급이 richness를 하나 더 냄).
2. export-human → import-human 왕복이 레코드를 보존하는지 확인.
3. verify가 `# REVIEWED` 없는 체커를 건너뛰고, 있는 체커는 pass/fail을 내는지 확인.
4. analyze를 돌려 Q(G) 풍요로움 평균이 등급 순서대로 나오는지 `assert`.

실패하면 비영 종료. 그 외 단위 테스트 없음.

## 14. 범위 밖과 한계

- Lean 4: 미설치. `verifications`에 추가 verdict 종류를 넣을 자리만 둔다.
- 2.4 이해 실험(재설명·파생 문제 생성): 평가 페이지 틀을 재사용해 나중에 추가.
- 타사 모델: Max 플랜으로 호출 불가. `source` 자유 텍스트로 수동 입력 경로만 제공. 계열 효과는 계획서대로 한계로 명시.
- temperature 고정 불가, 모델 alias가 가리키는 버전이 기간 중 바뀔 수 있음(raw의 `modelUsage`로 추적).
- 헤드리스 CLI 로그인이 만료된 상태. 실행 전 터미널에서 `claude` → `/login` 필요(연구자가 직접).

## 15. 실행 순서

1. run.py의 호출 레이어 + gen + selfcheck(dry-run) → 컨텍스트 팩 초안 → 실제 `gen` 1회(10/19 생성 구간 안에)
2. solve, eval, verify
3. 평가 페이지 제작·게시(평가자 섭외 전 데이터로 미리 점검)
4. analyze

## 16. 추가 조건: 고컨텍스트 P2 가지 실험 (2026-11-04 추가)

배경: 2026-10 OpenAI의 준리만가설 결과(원고 722편 공개)는 사람이 고른 난제를 에이전트가 최전선 선행 연구(Dunn–Radziwiłł 2021 등) 위에서 평균 3시간 풀어 낸 것으로, 새 개념 없는 "알려진 아이디어의 종합"이었다. AI가 스스로 문제를 제기한 사례는 없다. 본 실험의 생성 단계는 1,558단어 초안 컨텍스트 팩으로 돌았으므로, P2에서 등급 차이가 나타나지 않을 때 그것이 모델 능력 때문인지 입력 때문인지 가릴 수 없다.

설계 (2026-11-06 사용자 승인으로 개정. 11-04 초안의 "저팩 + 초록 추가" 방식과 그 팩 `context/additive_comb_high.md`는 사용자 지시로 폐기·삭제했다. 그 팩으로 먼저 실행된 `high_ctx/` 폴더(문제 4개, 평가 8건)도 사용자 지시로 삭제했다):
- 기존 실행은 **저컨텍스트 조건**으로 명명한다. 데이터는 그대로 둔다.
- **고컨텍스트 팩**: `context/additive_comb_high_v2.md`(원본 `docs/high_ctx/2026-11-06-additive-comb-high-pack-draft.md`, 약 5,200단어). 저팩에 덧붙인 것이 아니라 세 문제 줄기를 기원부터 2026-11 최전선까지 요약한 독립 팩이다. Result 절 3개 = 줄기 3개: (1) 3항 등차수열 없는 집합(정수, 캡 세트), (2) 배가가 작은 집합의 구조(Freiman→PFR→배가 4+δ), (3) 제한 합집합(Erdős–Heilbronn→Lev→Ouyang 2025). 논문 조사와 팩 작성은 사용자가 별도 세션에서 진행했고 근거는 `docs/high_ctx/`에 있다.
- 팩에서 뺀 것: AI·회사·모델 이름, 실험·평가 언급, 대조군 주제(시돈 집합, 표현 함수, 합-곱, 최소 겹침, 소수 등차수열), 최전선에 AI가 관여한 결과. 확정되지 않은 상수는 값을 단정하지 않는 중립 문장으로 쓴다. 각 줄기의 "알려진 열린 질문" 목록은 두되 "다시 내지 말 것" 지시는 붙이지 않는다(저팩에 없는 과제 지시가 고조건에만 생기므로).
- 모델·출제 프롬프트·시스템 프롬프트·평가자·채점표는 저컨텍스트와 같다. 팩은 출제할 때만 보여 주고 풀이할 때는 보여 주지 않는다(저컨텍스트와 같음).
- 규모: 모델당 open 3개(총 9개, `gen --kind open --n 3`이라 모델마다 줄기 1·2·3에서 하나씩) → 3모델 풀이(27칸) → AI 평가(문제 27건, 풀이 81건). 성공 판정은 저컨텍스트 open과 같은 기준이다. 데이터는 새 폴더 `high_ctx2/data`에 쓴다.
- 순서: 본 실험 Fable 마무리 → 고컨텍스트 출제·풀이·AI 평가 → 사람 평가 내보내기 한 번(`export-human --extra-data-dir high_ctx2/data`로 저·고 문제를 표시 없이 섞어 한 번에 내보내고, `import-human`이 평가를 각 폴더로 되돌린다).
- 유출 통제: 고컨텍스트 문제마다 저컨텍스트와 같은 문헌 대조(웹 검색)를 하고, 필드 `pack_list_match`(그대로 옮김 / 변형 / 목록 밖 + 해당 목록 항목 번호)를 더한다. 9문제라 Opus 1회 판정 + 사용자 확인으로 한다.
- 사전 지정 짝(결과 보기 전 2026-11-06 기록): 저컨텍스트에서 Result 1("Strong bounds for 3-term progressions")을 초점으로 받은 open 문제 P-e7ee71(sonnet), P-0ec34a(opus), P-afca8b(fable)를 고컨텍스트 줄기 1의 open 3개와 짝지어 같은 주제·다른 깊이의 서술 비교를 한다.
- 가설 H-ctx: 컨텍스트를 두껍게 하면 Q(G)와 성립률은 오르지만 등급 순서는 바뀌지 않는다. 등급 효과가 고컨텍스트에서만 나타나면 P2는 모델이 아니라 입력에 의존한다.
- 분석: 조건 × 등급 표(기술통계, 중앙값 차). n이 작으므로 검정은 보조.
- 한계: 줄기 2·3은 저팩과 주제가 달라 깊이 효과와 주제 효과가 섞인다(줄기 1만 같은 주제). 사람 평가는 섞어 제시해도 주제만 보고 조건을 짐작할 수 있어 블라인드가 약하다. 팩의 최전선 결과 일부는 모델 학습 시점 무렵이거나 이후이며, 결과마다 연도와 arXiv 번호가 있어 나중에 grounding과 대조할 수 있다(별도 지표는 두지 않음).
- 대조군은 여전히 인간이 낸 Erdős 문제다. 고컨텍스트 조건은 대조군이 아니라 두 번째 조건이다.
- 보고: 2.5-5(계열 효과) 옆에 "체제 효과"(도구 없는 60분 단일 호출 vs 에이전트·도구·수시간)를 한계로 추가한다. P3의 "사다리 없음"은 이 체제 안의 관찰로만 해석한다.

