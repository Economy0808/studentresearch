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
