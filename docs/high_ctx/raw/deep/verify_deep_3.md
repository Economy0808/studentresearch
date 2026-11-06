# 정독 노트 검증: deep_G.md, deep_H1.md, deep_H2.md (2026-11-06)

기준: `src/<arXiv>.tex`(LaTeX 원본)를 우선으로 보고, 쪽수는 `fulltext/<arXiv>.txt`의 쪽 나눔(\f)으로 확인했습니다. 판 번호는 arXiv 메타데이터(`v34/*.xml`)로 확인했습니다: 2512.11217 v2, 2404.02244 v2, 2604.25893 v1, 2506.20813 v2, 2406.18798 v4(2026-03-31), 2605.28781 v1, 2602.23282 v2, 2607.11351 v2.

| arXiv | 판정 | 고칠 내용(한 줄) |
|---|---|---|
| 2512.11217 | 수정 필요 | 초록은 본문과 "어긋난" 것이 아니라 더 약한 서술(정리 1.4에서 따라 나옴). 가우시안 계산이 log d 손실의 "본질성을 보인다"는 표현은 과장 |
| 2404.02244 | 확인 | "of some independent interest" 위치는 부록 A가 아니라 서론(4쪽) |
| 2604.25893 | 수정 필요 | 반례 A₁의 결론은 "정리 1.2의 밀도를 가진 P·Q에 A 전체가 들어갈 수 없다"로 한정해야 함. 16쪽 오탈자 지적은 맞음 |
| 2506.20813 | 확인 | §8은 #52 "인접"이 아니라 정수 합-곱 추측(#52)을 직접 서술 |
| 2606.02541 | 확인 | 없음 |
| 2609.31798 | 확인 | 없음 |
| 2605.28781 | 수정 필요 | 정수 Z 서술이 없는 곳은 §3·§4·§5도 포함. §6·§7.1·§7.2는 §3–§4의 보조정리에 기대므로 단독으로 분리되지 않음 |
| 2406.18798 | 확인 | 추측 18의 max는 LaTeX 원본에도 있는 저자 오타(추출 문제 아님). min이 맞음 |
| 2605.03181 | 확인 | 없음 |
| 2602.23282 | 확인 | "코드 초안도 AI가 작성"은 원문의 "초안 생성을 도왔다"로 약하게 고칠 것 |
| 2607.11351 | 수정 필요 | 1.2절 첫 문장은 "점근 기저" 정의라 남겨야 함. 노트가 지운다고 한 "Clearly…"는 둘째 문장 |
| 2609.08706 | 확인 | 없음 |

집계: 확인 8, 수정 필요 4, 중대 오류 0.

---

## 지정 쟁점

### 쟁점 1. 2605.28781: 정수 Z·대조군 #52와 분리 가능한 범위, AI 단락의 원문 범위

**정수 Z를 직접 말하는 곳(원본 전체 검색, `\bbz`·`\mathbb Z`).** 노트의 "제거 대상" 목록은 빠짐없이 맞습니다.
- 1절 본문(1–2쪽): Erdős가 Z·R·C에 대해 물었고 주된 관심은 Z였다는 문장(`main interest was for A⊂\bbz`). R에서 4/3+c, Cushman c=10/4407(1쪽). "(1.1)은 유계 차수, 특히 원래 환경인 Z에서는 여전히 참일 수 있다"(2쪽).
- 1.1절(2–3쪽): 괄호 속 "원래 A⊂Z에 대한 것"(2쪽). Pálvölgyi–Zhelezov가 Z에서 같은 의존성을 달성(3쪽).
- 2절(5–6쪽): "Instead of working in Z…"(5쪽). Balog–Wooley 1차원 예(5쪽). 마지막 문단의 "d→∞가 필요"(6쪽).
- 6절의 Γ≤Q^× 문장(13쪽)은 Z 합-곱이 아니라 인접 서술입니다. 같은 절 앞부분의 Erdős–Stewart–Tijdeman 구성(Γ≤Q^×)도 같은 성격입니다.
- §7.1의 `\mathbb Z_p`(p진 정수), 보조정리 7.1 증명의 `(\mathbb Z/2)^{|S|}`(갈루아 군)는 정수 Z와 무관합니다.

**"분리 가능한 것은 1.2절, 1.3절, 6절, 7절뿐"이라는 판정은 두 방향으로 고쳐야 합니다.**
1. *더 넓습니다.* §3(대수적 정수론), §4(구성, 보조정리 4.1·4.2), §5(수치 추정, c≥0.00000087) 본문에는 Z 문장이 하나도 없습니다. 원문 그대로 넣을 수 있습니다. 노트가 "§4를 2–3문단으로 요약해 붙여야 하고, 그 요약은 새로 쓴 글"이라고 한 것은 맞지 않습니다. §3–§4 원문을 그대로 두면 됩니다.
2. *더 좁습니다.* §6·§7.1·§7.2는 혼자 서지 못합니다.
   - 정리 6.2 증명: "A를 Lemma `lem-mainmult`처럼 구성", Theorem `th-tower` 사용.
   - 정리 6.3 증명: Lemma `lem-regbound`, `lem-ball-mult`, `lem-ball` 사용.
   - §7.1: "Lemma `lem-main`의 K가 p를 완전분해하면…".
   - §7.2(정리 7.2) 증명: Lemma `lem-main`과 그 증명 속 부등식(|σ(α)|≤2Xe^Y)을 직접 씀.
   - §7.3(함수체)만 "complete rewrite"라 거의 독립입니다. 다만 595행의 유비 문단은 수체 구성을 가리킵니다.
   - 따라서 분리할 묶음의 최소 단위는 "§1.2·§1.3 + §3 + §4 + §6 + §7"(필요하면 §5 포함)입니다. 원문에서 빼야 할 것은 위 Z 문장들(1절 본문 일부, 1.1절 두 문장, 2절 첫·끝 문단)과 정리 1.1–1.3 진술의 처리 방식입니다.
3. *남는 위험(노트 판단 유지).* Z를 말하지 않아도 보조정리 4.1의 X^d ≤ |A| ≤ (XY/c)^d와 정리 1.2의 "무한히 많은 d"가 "차수 d→∞가 필요하다"를 그대로 드러냅니다. 모델이 "유계 차수·정수에서는?"을 묻게 될 위험은 남습니다. 이것은 연구자가 판단할 일입니다.

**"The role of AI in this proof" 원문 범위.**
- 1절 끝, 1.3절 다음, Acknowledgements 앞에 있는 번호 없는 소절(`\subsection*`, 4쪽)입니다. 네 문장으로 되어 있습니다.
  1. 저자들은 OpenAI의 단위거리 추측 반례(참고문헌 ABGLSSTWW2026)에 자극받아 큰 차수 수체로 합-곱 반증을 다시 시도했습니다.
  2. 최종 구성에는 그 반례보다 훨씬 적은 정수론이 필요했습니다.
  3. GPT-5.5 Pro를 초기 단계의 "sounding board"로 썼습니다. 최종 증명과 주요 아이디어는 거의 전부 사람의 것이고, 예외는 Lemma `lem-unitsep`의 제안(Schinzel 결과를 짧은 초등 논증으로 대체)입니다.
  4. 글은 모두 저자가 썼습니다.
- 노트 요약은 이와 일치합니다.
- 추가 위치:
  - §3.2 단위 격자 소절, 8쪽: Lemma `lem-unitsep` 앞 문장 "(suggested by GPT-5.5 Pro)". 노트가 적었습니다.
  - §5 둘째 문단(11쪽)과 §7.3(17쪽, 583행): "단위거리 반증 논증"(곧 OpenAI 결과)의 작은 분해 소수를 언급합니다. AI가 직접 관여했다는 서술은 아니지만, AI 관련 서술을 걷어낸다면 함께 볼 곳입니다.
- 노트가 적은 참고문헌 [2](Alon–Bloom–Gowers–Litt–Sawin–Shankar–Tsimerman–Wang–Wood, arXiv 2605.20695)는 PDF 참고문헌에서 확인했습니다.

### 쟁점 2. 2406.18798: 추측 18의 max/min, 추측 14·15의 상태

- **max는 원본 LaTeX에 그대로 있습니다**(1188–1190행 `\max\bigl( \AA\{X\}, \MM\{X\}\bigr) \le (3-\eps+o(1))\Eta\{X\}`, PDF 26쪽). 인쇄나 추출의 오류가 아니라 **저자의 표기 오타**로 판정합니다. 의도된 형태는 min{A{X},M{X}} ≤ (3−ε+o(1))H{X}입니다. 근거는 셋입니다.
  1. i.i.d.일 때 A{X}=4H(X)−H(X+X′)이므로 max ≤ (3−ε)H는 "합과 곱의 엔트로피가 둘 다 (1+ε)H 이상"이라는 뜻이 됩니다. 정수 구간 위 균등분포에서는 A{X}=3H−O(1)이라 어떤 ε>0에서도 거짓입니다(노트의 계산과 같음).
  2. 같은 쪽 다음 문장(이 추측이 참이면 고전 합-곱 부등식이 따름)과 추측 14의 형태("M이 크면 A는 작다", 곧 min형)에 맞는 것은 min입니다.
  3. 2506.20813 §8(식 (59) 부근, 2637행)이 Goh의 추측을 max{H(X+X′),H(XX′)} ≥ (1+ε−o(1))H(X)로 다시 적었습니다. 이것은 min{A,M} ≤ (3−ε+o(1))H와 동치입니다. "ε≤1/3이어야 한다"는 결론도 min형에서만 의미가 있습니다.
  - 노트에 "원본 .tex에도 max(저자 오타)"를 덧붙이면 됩니다.
- **추측 14·15는 v4 시점에 열려 있습니다.**
  - 원본 1037행 "We were unable to prove the entropic version of the Bourgain–Katz–Tao theorem"(22쪽). 추측 15(1043행 이하)는 추측으로만 제시되고, 증명된 것은 "추측 15 ⇒ 추측 14"뿐입니다.
  - 26쪽 개정 문단("Following the initial preprint release…")은 추측 18에 대한 ε≤1/3만 반영했고, 추측 14·15의 해결은 언급하지 않습니다.
  - v4(2026-03-31) 이후의 해결 여부는 이 원본으로는 판정할 수 없습니다.
- 노트가 "1차 조사에 따르면 Li(2607.29042)가 8/7 증명"이라고 한 것은 이 폴더에 원본이 없어 검증하지 못했습니다(노트도 미검증으로 표시).

### 쟁점 3. 2607.11351: #30·#39 서술 위치와 남겨야 할 정의 문장

원본 1절 구조는 1.1절 Sidon sets(세 문단), 1.2절 Asymptotic Sidon bases, 1.3절 구성 안내이고, 6절이 Remarks and open problems입니다.

- **1.1절 둘째 문단(1쪽 하단~2쪽, 262–274행)이 #30 문단**입니다. f(n)~n^{1/2}, Erdős 추측 f(n)=n^{1/2}+O_ε(n^ε), 상계의 역사(Lindström, Ruzsa, Graham, Cilleruelo, Balogh–Füredi–Roy, O'Bryant), "See Erdős Problem #30"이 들어 있습니다. 노트와 같습니다.
- **1.1절 셋째 문단(2쪽, 276–300행)은 한 문단**입니다. 앞부분은 #39(그리디 x^{1/3}, AKS, Ruzsa x^{√2−1+o(1)}, "major open problem", "See Erdős Problem #39")이고, 뒷부분은 limsup ≥ 1/2, 식 (1.2) liminf, Krückeberg, #329입니다. 노트는 이를 "셋째 문단"과 "이어지는 문장"으로 나눴지만 원본에서는 같은 문단입니다. 빼는 범위는 노트와 같습니다.
- **1.2절 첫 문장은 노트가 잘못 짚었습니다.**
  - 원본 303행의 첫 문장은 "A set A⊂N is called an asymptotic basis of order k≥1 if every sufficiently large integer can be written as the sum of k elements of A."입니다. 이것은 **점근 기저의 정의**이고, 문제 1.1·1.2와 정리 1.1이 모두 이 정의를 씁니다. **남겨야 합니다.**
  - 노트가 "1.2절 첫 문장"이라며 빼라고 한 "Clearly, it follows from (1.2) that no Sidon set can be an asymptotic basis of order 2"는 **둘째 문장**입니다. 이 문장을 빼는 판단 자체는 맞습니다. 식 (1.2)를 잃고, 무한 Sidon 집합의 밀도 상계를 가리키므로 #39 배경입니다.
- **Problem 6.1 뒤 문장(21쪽, 1615–1618행)**: "The range a+b>1 is the natural necessary condition suggested by the classical upper bound S(x)≪x^{1/2}… And the range a+b>√2 may be a more realistic first target from Ruzsa's exponent √2−1 for dense infinite Sidon sequences [Ru98]."
  - 둘째 문장(Ruzsa 지수)은 #39의 현재 기록이므로 빼야 합니다. 노트와 같습니다.
  - 원본은 `a+b>\sqrt{2}`입니다. 노트의 복원이 맞습니다. 계수 논법으로 c(a+b+1)≥1, c=√2−1이면 a+b≥√2입니다.
  - 첫 문장(S(x)≪x^{1/2})은 연구자 판단 사항이라는 노트 의견을 유지합니다.
- **본문 2–5절과 초록**에는 Ruzsa, Erdős Problem, x^{1/2}가 다시 나오지 않습니다(검색 확인). 남는 흔적은 노트가 적은 대로 Lemma 4.4(c=0.3393)와 6절 첫 문단의 c<(3−√5)/2, 마지막 문단의 B_h[1] 크기 N^{1/h}뿐입니다.
- **남겨야 할 정의 문장(최종).**
  1. 1.1절 첫 문단 첫 문장: Sidon 집합의 정의(257행).
  2. 1.1절 셋째 문단 둘째 문장: "For any subset A⊂N, let A(x) denote the number of elements of A not exceeding x"(276행). Lemma 4.4의 S(x)와 6절 문제들이 씁니다.
  3. **1.2절 첫 문장: 점근 기저의 정의(303행).** 노트에서 빠졌습니다.
  - f(n) 표기(262행)는 이후 절에서 쓰이지 않으므로 함께 빼도 됩니다.

### 쟁점 4. 2602.23282: "Declaration of AI usage" 원문 범위

- 위치: Acknowledgements 바로 뒤, 참고문헌 앞의 굵은 머리 문단 "Declaration of AI usage."(1248–1252행, 14쪽)입니다. 네 문장으로 되어 있습니다.
  1. AI 보조 도구를 Lemma `lem:base-block`(A_base)의 구성 탐색에 썼습니다.
  2. AI 보조 탐색이 먼저 12점 예(c*≤7/12)를 냈고, 여러 차례 다듬어 14점 A_base(c*≤4/7)가 되었습니다.
  3. AI가 Lemma `lem:base-block`의 전수 확인 코드 초안 생성을 도왔습니다.
  4. Lemma `lem:base-block` 관련 작업을 빼면 모든 증명과 서술은 사람 저자가 했습니다.
- 노트 요약은 대체로 맞습니다. 다만 "전수 확인 코드 초안도 AI가 작성"은 원문 "helped generate an initial draft"보다 강합니다. "초안 작성을 도움"으로 고치는 것이 맞습니다.
- 다른 곳에 AI 서술은 없습니다. Lemma 증명은 저자 GitHub 저장소(`ep757-45set-base-block-verification`)를 인용합니다.

### 쟁점 5. 2604.25893: 4쪽 반례 A₁, "이산에서는 A 전체가 구조에 들어갈 수 없다", 16쪽 오탈자

- **A₁ 수식은 원본과 같습니다**(252–253행, 4쪽). A₁={0,10N,2^N}+[N], N≥100, |A₁+A₁|=6(2N−1) ≤ 4|A₁|−6. 직접 계산하면 |A₁|=3N이고 합집합은 서로 겹치지 않는 평행이동 6개(각 2N−1개)이므로 12N−6=4|A₁|−6으로, 실제로는 등호입니다.
- **판정 문장은 한정이 필요합니다.**
  - 원문은 "it is not possible to have the entirety of A contained in P or Q **in Theorem 1.2**"입니다. 곧 정리 1.2의 밀도 조건(P에서 ≥1/2−ε′, 진짜 2차원 Q에서 ≥1−ε′)을 갖는 P나 Q에 A 전체가 들어갈 수 없다는 뜻입니다.
  - 노트의 "이산에서는 A 전체가 구조에 들어갈 수 없다"는 너무 넓습니다. 실제로 A₁은 Q={l₁+l₂·2^N : 1≤l₁≤11N, l₂∈{0,1}}(진짜 2차원, 2^N>11N이므로 proper, |Q|=22N≈7.3|A₁|)에 통째로 들어갑니다. 다만 밀도가 3/22로 낮습니다.
  - 원문의 다음 문장 "A₁ is not contained in any 2-dimensional progression Q such that |Q|≪|A₁|"도 Vinogradov 기호를 글자 그대로 읽으면 이 Q 때문에 성립하지 않습니다. "|Q|가 |A₁|과 거의 같은 크기"라는 뜻으로 읽어야 합니다.
  - 따라서 노트와 1차 조사 정정문을 "정리 1.2 수준의 밀도로 A 전체를 담는 1·2차원 진행은 없다(반례 A₁)"로 고칠 것을 권합니다.
  - 1차 조사의 "남은 경계 2"를 열린 질문에서 빼라는 노트의 결론은 유지합니다.
- **16쪽 오탈자 지적은 맞습니다**(699행). "let (a₀,i₀) ∈ E be such that α(a₀,i₀) is maximal"에서 E는 Lemma `exceptionlemma`의 예외 집합(|E|≤ε⁴qM)입니다. 바로 뒤에서 (a₀,i₀)는 J={(a,i)∉E : α≥10ε′}의 원소로 쓰이고(J′ 정의), (tree1) α(a₀,i₀) ≥ α−ε−10ε′는 "|J|≤qM"에서 J 위 최댓값으로 나옵니다. 따라서 "∉ E"(또는 "∈ J")가 맞습니다. 노트의 근거 문구("뒤에서 α가 크다는 것을 쓰므로")는 "J의 원소로 쓰이므로"로 바꾸면 더 정확합니다.
- 덧붙임: Question 1.1의 출처는 **Green의 100 open problems 중 Problem 30**이고 **Erdős Problem #30(대조군)과는 다른 문제**입니다. 노트는 바르게 구분했지만, 팩 구성 때 번호가 겹쳐 헷갈리지 않게 표시해 둘 것을 권합니다.

### 쟁점 6. 2512.11217: 초록(v2)과 정리 1.4, §5 장벽 서술

- **초록**(74–76행): "for any ε>0… exp(C_ε log(2K)^{1+ε})… dimension at most C_ε log(2K)^{1+ε}"입니다. 정리 1.4(104행)는 f(K)=O(log(3K)·loglog(3K))입니다.
  - log·loglog ≤ C_ε log^{1+ε}이므로 초록은 정리 1.4에서 곧바로 따라 나오는 **더 약한(그러나 참인) 서술**입니다. 모순은 아닙니다.
  - 감사의 글(148행)에 따르면 앞선 판은 log·loglog·logloglog였고, Fredy Yip의 제안으로 logloglog가 빠졌습니다. 초록은 어느 판 기준으로도 본문보다 약하게 적혀 있습니다.
  - 노트의 "초록과 본문의 불일치 → 고치거나 빼야"는 "초록이 본문 최강 결과를 반영하지 않음 → 팩에는 정리 1.4를 기준으로 쓸 것"으로 표현을 바꾸는 것이 맞습니다.
- **§5(16–18쪽)는 노트 요약이 대체로 맞고, 두 곳만 고칩니다.**
  1. 노트는 가우시안 계산이 log d 손실이 "본질적임을 보인다"고 썼습니다. 원문(486행)은 "This observation does not, on its own, prohibit the possibility of using almost-periods as part of a proof of Conjecture 1.5"라고 먼저 한정합니다. 그다음 "without any new ideas… unlikely to yield a bound better than Theorem 1.4"라는 저자의 **믿음**을 적습니다. "본질적임을 보인다"는 과장이므로 "이 방법의 한계를 보여 주는 예"로 고칠 것.
  2. 장벽 2: Courtade–Fathi–Pananjady 반례(무거운 꼬리 가우시안 혼합)는 W₂ 거리에서 가우시안과 멀지만, 원문은 "they are still close to Gaussians in Ruzsa distance"라고 덧붙입니다. 노트는 이 단서를 뺐습니다. 한계는 "Shannon–Stam 안정성 증명 방법의 일반적 한계"이지, Ruzsa 거리 프로그램이 반증된 것이 아닙니다.
- 장벽 1(끝마무리; 이산 가우시안의 배가 Θ(d), 합·섬유 연산에 닫힘, Z^d에서의 근사 최소화는 d=1만 알려짐), 프로그램 (1)(2), "(1) may be within reach", Kac–Bernstein "we do not see at present how to discretize", 절 머리의 "speculative"·"known to experts"는 원문과 일치합니다. 쪽도 맞습니다(장벽 16–17쪽, Kac–Bernstein 18쪽).

---

## 논문별 세부

**2512.11217 (deep_G).** 정리 1.4, 추측 1.5, Prop 2.11(η=1/438, d=O(log 3K), 규모 Cd⁵, d[X;U_A]≤30d log d), Theorem 1.8(홀수 위수, 부록 C 스케치)은 원본과 일치합니다. 열린 질문 2(§1.1 "perform even more poorly", 3쪽), 4(Prendiville, 4쪽), 5(Croot–Sisask, 8–9쪽)의 위치도 맞습니다. AI 서술은 없습니다(감사의 글: Yip, Tao, Leng, Green, NSF). 고칠 곳은 쟁점 6의 두 가지뿐입니다.

**2404.02244 (deep_G).** 정리 1.1(“Moreover, H⊆ℓA−ℓA, ℓ≪(2+m log K)^{O(m³ log m)}”), 정리 1.3, 따름정리 1.2(p 홀수, η≤1/2, η^{O(p³)}), "unable to achieve this even in the m=2 case"(2쪽), "can probably be improved with additional effort"(2쪽), 각주의 Liao 2K^{11}→2K^9(참고문헌 jjl = arXiv 2404.09639)는 모두 일치합니다. 다만 노트의 열린 질문 4 위치 "(부록 A, Lemma A.3 앞 p.4)"는 서론의 증명 개요 문단(202행, 4쪽)입니다. AI 서술은 없습니다(Zach Hunter 감사만).

**2604.25893 (deep_G).** 정리 1.2, 따름정리 1.3·1.4, 보조정리 2.3(|P|≥12, >1/2, 5X−4X), 2.4(|X|≥100, 최소 진행, >2/5, 9X−8X), 2.5(c<1/10, 41X−40X), 날카로움 예(P=[2l], X=2·[l])는 원본과 일치합니다. 열린 질문 2의 "does not seem to follow even conditionally"(4쪽)도 맞습니다. AI 서술은 없습니다(연구비만). 고칠 곳은 쟁점 5의 A₁ 판정 한정과 오탈자 근거 문구입니다.

**2506.20813 (deep_G).** Theorem 7.2(h(XY−ZW) ≤ 5h(XY)+2h(X+Y)−6h(X)−4E log|X|), §5 "Open problem"(f(C,D), 1866행), §1.3의 "We do not present any positive results", Example 8.1(4/3, ε≤1/3)은 모두 일치합니다. 대조군 판정을 하나 고칩니다. §8은 정수(N) 값 확률변수의 합-곱과 "널리 추측되는 ε≤1"(정수 합-곱 추측 자체)을 다루므로 #52 "인접"이 아니라 #52를 직접 서술합니다(제외 판단은 그대로). 각주의 "INFORMED-AI project"는 연구비 이름일 뿐 AI 사용 서술이 아닙니다(노트의 "없음" 유지).

**2606.02541 (deep_H1).** 정리 1(w(k;3) > 2^{k(log* k)/4}), "not aware of any way to construct… [r^{(1+Ω(1))k log k}]"(3쪽), 서론의 "roughly (log* k)/2 steps"와 증명의 b=⌊(log* k)/3.5⌋(노트의 내부 불일치 지적이 맞음), Disclosure(ChatGPT Pro 5.5, 퇴고용 copyediting, 수학은 사람)는 원본과 일치합니다.

**2609.31798 (deep_H1).** 초록·서론의 Green "reasonable to believe w(3,k)≤k^{O(log k)}", "perhaps gives some evidence that k^{Θ(log k)}", Raghavan의 (log n)^{1/6}/loglog n에서 나온 상계 exp(O((log k)^6(loglog k)^6)), s-공식은 원본과 일치합니다. 감사의 글 7명에 AI 서술은 없습니다. 노트가 "제 계산/추정"이라고 표시한 부분은 원문에 없는 해석이라고 바르게 표시되어 있습니다.

**2605.28781 (deep_H1).** 정리 1.1–1.8, 6.2(exp((C^{-1}k log k)d)), 7.2(p^{fδ}<|A|<p^δ), §5의 c≥0.00000087과 "작은 분해 소수" 문단, §6의 Q^× 문장(13쪽), Niklasch exp(d^{2/3+o(1)})(14쪽), Cushman 10/4407은 원본과 일치합니다(4/3+10/4407=1962/1469도 맞음). 고칠 곳은 쟁점 1입니다.

**2406.18798 (deep_H1).** 쟁점 2 외에는 일치합니다. "No originality is claimed"(13쪽), Hegarty 집합 {−7,−5,−4,−3,0,4,5,7}, {0,1,2} Sidon 변수, Bloom 4/3+2/951과 Rudnev–Stevens 4/3+2/1167(26쪽), 두 심사자 감사를 확인했습니다. AI 서술은 없습니다.

**2605.03181 (deep_H2).** "remains open" 문장이 원본에 없다는 지적, 제곱수 경우의 "stronger bounds… known; see [LefmannThiele, §6]", Mian–Chowla n^{1/3}, KSS 0.0000305, Abbott 0.0805, 식 (1)(2)(Erdős–Turán, Lindström, Carter–Hunter–O'Bryant 0.98183)의 위치가 모두 맞습니다. 참고문헌 [27] "Tao" 항목이 1952년 C. R. Acad. Sci. 논문으로 인쇄된 오류도 확인했습니다(원문 126행 `\cite{TaoDistance}`). f(c)=(c−1)/(2c√c)의 최댓값이 c=3에서 1/(3√3)임도 직접 확인했습니다.

**2602.23282 (deep_H2).** 정리 1.2·1.3(g(n)=⌈(n+1)/2⌉), Problem 1.4(#757), Gyárfás–Lehel 1/2+1/(141·76)≤c*≤3/5, 정리 1.6(9/17≤c*≤4/7), A_base 14점, Henning–Yeo 17τ≤5n+3m, 비선형 예 {1,2,3,5}는 원본과 일치합니다. 쟁점 4의 문구 하나만 고칩니다.

**2607.11351 (deep_H2).** Theorem 1.1(η<0.0527), 매개변수(α²=0.9473, c=0.3393; (α²−c)(α⁴−c)=0.339311>c, c(2+α²)=1.00001889)를 다시 계산해 일치를 확인했습니다. 6절 첫 문단(c<(3−√5)/2, 삭제 방법의 어려움), Problem 6.1–6.4, "cannot force all three summands…", B_h[1] N^{1/h} 문장도 원본과 같습니다. 열린 문제 5개(1.1은 해결됨) 판정도 맞습니다. 고칠 곳은 쟁점 3의 1.2절 첫 문장입니다.

**2609.08706 (deep_H2).** Erdős–Nathanson (0,1/(2h−2)), h=2는 (0,1/2], Nathanson–Sárközy d_L≤1/h, "Erdős–Nathanson's Problem"(h≥3, (0,1/h))을 이 논문이 해결한다는 점, 새 열린 질문이 없다는 점이 원본과 일치합니다. AI 서술은 없습니다.
