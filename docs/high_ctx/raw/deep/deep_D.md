# 정독 보고 D: K19(2508.18586, 2503.09121), K1(2406.12290), K18(2610.25271, 2610.35819)

기준일 2026-11-06. 다섯 편 모두 본문 텍스트를 처음부터 끝까지 읽었습니다. 수식이 깨진 곳은 PDF를 직접 그림으로 열어 확인했습니다(2508.18586 48쪽, 2503.09121 3·4쪽). 쪽 표시는 논문 자체의 쪽 번호입니다. 열린 질문의 인용은 15단어 이내로 줄였고, "내 해석"이라고 적은 것은 본문에 없는 제 추론입니다.

---

### 2406.12290 — Elsholtz, Hunter, Proske, Sauermann, Improving Behrend's construction: Sets without arithmetic progressions in integers and over finite fields (15쪽, 읽은 범위: 전체. 단 §4의 도형 계산은 구조 위주로 읽음)

**주정리.**
- **정리 1.1.** N이 클 때 {1..N} 안에서 세 수가 등차를 이루는 일이 없는 부분집합의 최대 크기 r_3(N)은 N·2^{−(C+o(1))√(log₂N)} 이상이다. C = 2√(log₂(24/7)) ≈ 2.667로 Behrend(1946)의 2√2 ≈ 2.828보다 작다. 쉬운 말: 80년간 안 바뀌던 "얼마나 큰 집합이 가능한가"의 아래쪽 기록을 처음으로 지수의 상수까지 올렸다(준다항식 개선).
- **정리 1.2.** 소수 p를 고정하고 n이 충분히 크면 F_p^n(p를 법으로 하는 n차원 벡터 공간)에서 r_3(F_p^n) ≥ (cp)^n인 절대상수 c > 1/2가 있다. 정리 1.3에서 c < √(7/24) ≈ 0.540까지 되며 본문 예는 c = 0.54. (추출 텍스트에는 √가 빠져 "c < 7/24"로 보이나, 정리 1.3의 (7/24)^{n/2}에서 √(7/24)가 맞습니다.) 쉬운 말: 1940년대부터 c = 1/2에서 막혀 있던 벽을 처음 넘었다.
- **정리 1.3.** 2 ≤ m_i ≤ m인 임의의 순환군들의 곱 Z_{m1}×…×Z_{mn}에서 r_3 ≥ (7/24)^{n/2}/(10^6 m² n³)·m_1⋯m_n. 소수가 아닌 모듈러스, 짝수 모듈러스도 포함(짝수는 기존 ((m+2)/2)^n을 넘음). 쉬운 말: 어떤 아벨군이든 같은 방법이 통하는 일반형.
- 범위 주의: 정리 1.1은 {1..N}, 정리 1.2는 p 고정·n→∞, 정리 1.3은 n이 m과 c에 비해 충분히 클 때.

**증명의 뼈대.**
- §2(개요). 정수/군을 높은 차원의 원환(토러스 [0,1)^n)에 무작위로 넣는다. 원환 안에서는 3항 등차가 없는 집합이 측도 0이라서(본문 p.3), 첫째 항과 셋째 항이 "멀리 떨어진" 등차만 금지한다.
- **명제 2.1**(핵심 난관): x+z ≡ 2y (mod 1)이면 모든 좌표에서 |x_i−z_i| < δ가 되는 집합 S ⊆ [0,1)^n의 측도가 ≥ 10^{−5}δ²n^{−3}(7/24)^{n/2}. 옛 방식의 그릇은 (1/2)^n = (1/4)^{n/2}.
- **명제 2.2**(새 아이디어): 2차원 판 T ⊆ [0,1)²와 함수 f: T → [0, 100/ε²]가 있어 x+z ≡ 2y이면 f(x)+f(z) ≥ 2f(y) + (x_1−z_1)² + (x_2−z_2)². 면적 μ(T) ≥ 7/24 − ε. 이 판의 n/2제곱 곱에서 f의 합이 좁은 구간에 있는 "얇은 조각"을 잡으면 명제 2.1이 나온다(§2 끝 증명, 합산 부등식 한 줄).
- §3. 명제 2.1 → 정리 1.3(원환으로의 무작위 넣기 φ_a + 평균 논증 + 보조정리 3.2 곱군 부분군), → 정리 1.2(m=p), → 정리 1.1(처음 n개의 소수의 거듭제곱들의 곱으로 Z_{m1⋯mn} ≅ 곱군이라는 중국인의 나머지 정리 이용; 또 Green–Wolf식 직접 증명도 소개).
- §4. T를 정의 4.1로 다각형 3개(T_1,T_2,T_3)의 합집합으로 명시하고(면적 합 = 7/24 − O(ε)), f를 만들어 부등식을 사건 분석(보조정리 4.4, 4.6, 따름정리 4.5, 4.7)으로 증명한다. 핵심 새 아이디어는 §2의 명제 2.2와 §4의 T 자체에 있다.

**방법이 막히는 곳.**
1. "토러스에서 3항 등차가 없는 집합은 측도 0"이라 순수 토러스 구성은 불가능, 먼 항만 금지해야 한다(§2, p.3).
2. 전통 구성은 [0,(p−1)/2]^n에 갇혀 wrap-around를 피하므로 ((p+1)/2)^n을 넘을 수 없다: "so c = 1/2 is a significant barrier"(§1, p.3).
3. 결론은 x−z 좌표로 써야 하고 x−y로는 "analogous statement ... would be false"(§2, p.4). 첫째·셋째 항 차이만 통제된다.
4. 7/24는 "somewhat ad-hoc"한 구성에서 나온 숫자이고 최적이라는 주장이 없다(§2, p.4).
5. 정리 1.1의 낮은 차수 항: 본문 증명은 (log N)^{3/2} 꼴 손실을 낳는다(§3 끝). Elkin(2010)이 개선한 (log₂N)^{1/4} 이득 요인과의 비교는 본문에 없다(내 해석: 이 논문은 지수의 상수만 올렸고 낮은 차수 항은 겨루지 않음).
6. 상한과의 간격: F_p^n에서 상한 상수 ≈ 0.841(Ellenberg–Gijswijt), 하한 ≈ 0.540, "there is still a large gap"(§1, p.2).

**본문 전체에서 나온 열린 질문.** 저자가 번호 붙은 추측을 적지 않았고 아래는 모두 본문 문장에서 읽은 것입니다.
1. 2차원 판의 면적 7/24를 더 큰 값으로: "an improved choice ... larger area would automatically carry over"(§1, p.3). 곧 C와 7/24의 개선.
2. 같은 문제의 확인: "it seems plausible that the constant 7/24 ... can be improved"(§2, p.4).
3. F_p^n 하한 상수 c(≈0.54)와 상한 상수(≈0.841) 사이 간격 전체(§1, p.2). 작은 소수는 소수별 구성이 일반 c보다 낫다(F_3^n 2.2202^n, F_5^n 35^{1/3·n}, §1 p.3). 일반 구성과 소수별 최적의 관계는 본문이 묻지 않은 암묵적 틈이다.
4. (내 해석, 본문 명시 없음) 판의 차원을 2에서 더 올리면 더 큰 면적 비율이 나오는가. 본문은 2차원 블록만 쓴다.
5. 상한 쪽 배경: Kelley–Meka 지수 1/12, Bloom–Sisask 1/9 대 Behrend 지수 1/2의 간격(§1, p.1–2). 이 논문의 질문은 아니고 배경.

**1차 조사와 다른 점.**
- 일치: C, c < √(7/24), "7/24는 개선될 법함" 모두 본문과 맞다.
- 1차 조사는 선행 논문 2401.12802(Elsholtz–Proske–Sauermann), 2401.16106(Hunter)이 "합쳐졌다"고 적었으나 이 본문(v1)에는 두 논문 언급이 없다. 확인 불가.
- 1차 조사의 "2.2208(Naslund) 근거 원고 확인 불가"에 대해: 이 본문은 "Naslund informed us about forthcoming work"라며 2.2208^{n−o(n)}를 전해 들은 예고로 적고, 공개 값으로는 FunSearch(Romera-Paredes et al., Nature 2024)의 2.2202를 적는다. 1차 조사의 2.2203은 이 본문에 없고(다른 논문 2508.07932 값) 모순은 아니다.
- 1차 조사의 "기존 1차원 방식의 (1/2)²=1/4"는 본문 표현으로는 (1/2)^n = (1/4)^{n/2}이고 2차원 한 조각당 1/4 대 7/24라는 뜻이라 맞다.

**팩 적합도.**
- (a) 재료: §1의 정리 세 개, §2 명제 2.2의 부등식 조건, 정의 4.1의 T. 컴퓨터로 확인 가능한 문제를 만들기 쉽다(T의 면적 계산, 조건 f(x)+f(z) ≥ 2f(y)+|x−z|²를 격자점으로 점검, 더 큰 면적 T를 탐색).
- (b) 뺄 것: Kelley–Meka, Bloom–Sisask 상한 서술은 이미 알려진 것이므로 배경 한 줄로 충분. 대조군 #28 #30 #36 #39 #52 #66 #200 #241 #324에 관한 서술은 본문에 없음.
- (c) 15쪽. §1–§2는 쉽게 읽히고(철학 전공자도 흐름 파악 가능) §4는 도형 사건 분석이라 분량이 많다. 팩에는 §1–§2와 정의 4.1/명제 2.2만 넣는 구성을 권한다.
- (d) AI 관여 서술: 본문과 감사의 글에는 없음(감사의 글은 토론 상대만). 다만 선행 결과로 인용한 F_3^n 2.2202가 AI(FunSearch)가 찾은 값이라고 본문이 밝힌다.
- **판정: 상.** 하한 쪽 최전선이고 구체적 숫자(7/24)가 개선 대상으로 명시되어 문제 만들기에 좋음.

**필요한 선행 논문.**
1. Behrend, On sets of integers which contain no three terms in arithmetical progression, 1946 (참고문헌 [2]). `[arXiv 없음]`
2. Green–Wolf, A note on Elkin's improvement of Behrend's construction, Additive Number Theory(Springer) 2010 ([22]). 본문에 arXiv 번호 없음.
3. Elsholtz–Pach, Caps and progression-free sets in Z_m^n, Des. Codes Cryptogr. 88 (2020) ([17]). 본문에 arXiv 번호 없음.
4. Bloom–Sisask, An improvement to the Kelley-Meka bounds on three-term arithmetic progressions, 2023, arXiv:2309.02353 ([5]). 위쪽 최전선 짝.
5. Romera-Paredes et al., Mathematical discoveries from program search with large language models, Nature 625 (2024) ([32]). AI가 찾은 F_3^n 하한의 출처. `[arXiv 없음]`(Nature 게재, 본문에 번호 없음. 확실하지는 않음)

---

### 2503.09121 — Ouyang, On restricted sumsets with bounded degree relations (14쪽, v3 2025-09-04, 읽은 범위: 전체)

**주정리.** 기호: p는 소수, A, B ⊆ F_p, R ⊆ A×B는 "금지할 짝"의 목록, A +_R B = {a+b : (a,b) ∉ R}.
- **정리 1.5(정수판).** A, B ⊆ Z, |B| ≤ |A|. R의 최대 차수(한 원소가 R에서 몇 번 나오는지)가 B쪽에서 ≤ Δ이면 |A+_R B| ≥ |A|+|B|−3Δ, 양쪽에서 ≤ Δ이면 ≥ |A|+|B|−1−2Δ(후자는 최적, Remark 3.2). 쉬운 말: 금지한 짝이 적으면 합집합이 별로 줄지 않는다.
- **정리 1.6(F_p판).** 임의의 ε > 0, Δ ≥ 1에 대해 상수 c_ε, p_0가 있어, |B| ≤ |A|, |A|+|B| ≤ (1−ε)p, |B| ≤ c_ε p일 때(p > p_0 또는 |A| ≥ 10Δ) (i) B쪽 차수 ≤ Δ이면 ≥ |A|+|B|−3Δ, (ii) 양쪽 차수 ≤ Δ이면 ≥ |A|+|B|−1−2Δ. c_ε는 ε에 대해 이중지수보다 훨씬 작은 값이고 α = 2^{−18}·3.1·10^{−1549}ε, p_0 = 4^{10Δ}.
- **정리 1.7.** 양쪽 차수 ≤ Δ이고 |A|+|B| ≤ (1−ε)p이면 |B| ≤ c_ε p 조건 없이 ≥ |A|+|B|−1−2Δ(|A| ≥ β∆ 또는 p > p_0 = exp(O_ε(Δ))).
- **따름정리 1.8.** (i) 임의 함수 f: B→A, |A|+|B| ≤ (1−ε)p, |B| ≤ c_ε p이면 |{a+b : a ≠ f(b)}| ≥ |A|+|B|−3. (ii) R이 대응(차수 ≤ 1, 양쪽)이고 |A|+|B| ≤ (1−ε)p, p > p_0(ε)이면 ≥ |A|+|B|−3. (ii)가 Lev 추측의 (1−ε)p 범위 확인.
- **정리 1.9(정수에서의 반례 구성).** 정수에서 |A|=|B|=n, B쪽 차수 ≤ Δ인데 |A+_R B| = |A|+|B|−1−⌊5Δ/2⌋가 되는 예. 쉬운 말: B쪽만 차수를 제한하면 "−2Δ"는 안 되고 최소 ⌊5Δ/2⌋만큼 줄 수 있다.
- **정리 1.11.** (i) |A| = p−(k−1)ℓ−k+1, |B| = kℓ+2, 함수 R: B→A로 |A+_R B| = p−k(Lev 구성의 일반화). (ii) A ⊆ F_p, |A| = 6⌊p/11⌋−3, R ⊆ A×A가 대칭이고 차수 1(대응)인데 |A+_R A| = p−3. (iii) 임의 ε에 대해 |A|+|B| > (1+δ)p−O(1), |B| ≤ εp, 차수 1인 R로 |A+_R B| = p−3.
- **정리 1.14.** |A|+|B| ≥ ⌊2kp/(2k−1)⌋+1이면 어떤 함수 R: B→A에도 |A+_R B| ≥ p−k+1. 따름정리 1.12(i)의 구성이 k−2 정도의 덧셈 오차까지 최적.

**증명의 뼈대.**
- §2. Plünnecke–Ruzsa 부등식, "rectifiability"(F_p의 부분집합을 합 관계를 보존하며 정수로 "펴는" 사상), 그리고 BLT25(Bollobás–Leader–Tiba) 정리 25·26·27을 도구로 가져온다(정리 2.3–2.6, 증명은 부록 A에 정리 2.4만).
- §3. |B| ≥ α|A|이면 Plünnecke–Ruzsa로 |(A∪B)+(A∪B)|가 작음을 보이고 Green–Ruzsa(정리 2.6)로 A∪B를 정수로 펴서 정리 1.5로 넘긴다(Case 1). |B| < α|A|이면 BLT25의 "B에서 원소 세 개만 골라도 Cauchy–Davenport 하한을 달성"(정리 2.4)과 등차수열 구조(정리 2.3)를 쓴다(Case 2). 정리 1.7은 정리 2.5로 A가 등차수열 근처임을 얻고 구간 논증으로 마무리. 핵심 새 아이디어는 "차수 제한이 있는 관계"에서도 위 BLT25 도구가 통하게 하고 두 크기가 비슷한 경우를 Green–Ruzsa로 처리한 점이다(§1 p.3 "our main objective is to improve the O(Δ) term").
- §4. 구성: 정리 1.9는 구간 두 개에서 양 끝 근처와 중간 구간을 지움. 정리 1.11(i)은 A = {0,k,2k,…}∪(꼬리 구간), B = 음수 구간. (ii)(iii)는 보조정리 4.1(주기 11, 밀도 6/11, {0,1,4}의 평행이동이 A와 한 점에서만 만나는 집합 {0,1,2,3,5,6}+11Z)로 만든다.

**방법이 막히는 곳.**
1. 정리 1.6(i)의 "−3Δ" 항: "The bottleneck of the current method ... lies in the case A,B ⊆ Z after applying the rectifiability argument"(§1, p.4). 정수판 정리 1.5(i)가 개선되면 1.6(i)은 상수 변경 없이 개선된다.
2. 상수가 ε에 선형이 아니다: "parameter c_ε is not linear in ε", 그래서 |A|+c|B| < p 꼴 가정에서 −3을 못 얻는다(§1, p.4, 추측 1.13 앞).
3. |A|+|B| ≥ p 쪽은 방법 밖이다. 정리 1.11(ii)(iii)와 따름정리 1.12(ii)(|A| = (1−2ε)p, |B| = εp인데 |A|+|B|−4)가 구성으로 가로막는다. 따라서 따름정리 1.8(i)의 |B| ≤ c_ε p 조건은 필요하다(§1, p.4).
4. p_0와 c_ε는 상상하기 어려운 크기(10^{−1549}, 10^{6400}/ε⁴ 꼴)이고 정리 1.7의 β, p_0는 "determining their explicit forms requires a more detailed examination"이라며 명시하지 않았다(§1, p.3). 상수는 BLT25 정리 25에서 상속한 것이다.
5. 구성이 |A|+|B| > p에서만 이득을 보는 이유: "if the initial value of |A|+|B|−p were negative, this approach would offer no advantage"(§4, p.11).

**본문 전체에서 나온 열린 질문.**
1. 추측 1.2(Lev): |A|+|B| ≤ p이면 ≥ |A|+|B|−3. 본문은 (1−ε)p까지만 증명하고 ε 손실 없는 증명은 열림(§1, p.2, 따름정리 1.8 아래).
2. 추측 1.10: 정수에서 B쪽 차수 ≤ Δ이면 |A+_R B| ≥ |A|+|B|−1−⌊5Δ/2⌋. "We believe the above theorem is tight"(§1, p.3–4). 지금 증명된 것은 −3Δ.
3. 추측 1.13: 임의의 함수 R: B→A, |A|+2|B| ≤ p이면 ≥ |A|+|B|−3(§1, p.4).
4. 추측 1.2의 세 번째 가지(|A|+|B| ≥ p+2이면 ≥ p−2)의 올바른 임계값: "a stronger assumption |A|+|B| ≥ (1+δ)p is necessary"(§1, p.4). 정확한 문턱은 열림.
5. 따름정리 1.12(i) 구성의 최적성: 정리 1.14가 "tight up to an additive term of k−2"(§1, p.5)라고 하므로 남은 k−2의 틈.
6. 보조정리 4.1을 {0,1,4} 대신 크기 ≥ 4인 집합으로 바꿔 A의 상한 밀도를 1/2 위로 유지하면 구성이 p−4까지 개선된다: "If we could replace the set {0,1,4} ... keeping the upper density ... greater than 1/2"(Remark 4.2, p.11). 그런 집합이 있는가.
7. 회피 집합 F = F_p \ (A+_R B)는 시돈 집합이고 |F| < √p+1/2: "Any construction achieving |F| = ω(1), or any improvement proving |F| = o(√p), would be of interest"(§5, p.12).
8. (암묵) 정리 1.6/1.7의 상수 p_0, c_ε의 명시적이고 합리적인 크기.

**1차 조사와 다른 점.**
- 일치: (1−ε)p, 6p/11, p−3, v3 날짜, BLT·Green–Ruzsa 기반.
- **빠진 것 1.** 1차 조사는 Lev 추측을 한 가지(|A|+|B| ≤ p ⇒ ≥ |A|+|B|−3)로만 적었다. 본문의 추측 1.2는 세 가지다(≤ p이면 −3 / = p+1이면 p−3 / ≥ p+2이면 p−2).
- **빠진 것 2(내 해석, 전문가 확인 필요).** 정리 1.11(ii)의 R은 A 전체를 덮는 대칭 대응이고(i가 −t+1..t−1, −t..t−1을 지나며 모든 원소를 덮음) |A|+|B| = 12⌊p/11⌋−6이 p+2를 훌쩍 넘는데 |A+_R B| = p−3이다. 이는 본문이 적은 추측 1.2의 셋째 줄과 모순되어 보인다. 본문은 "반례"라는 낱말을 쓰지 않고 "we should be more cautious"(§1, p.2)와 위 4번 질문으로 표현한다. 1차 조사의 "Lev 추측의 반례가 아니다"는 첫째 가지(≤ p)에 대해서는 맞고, 셋째 가지에는 해당하지 않을 수 있다. 팩에 쓸 때 "반례가 아님"이라고 단정하지 말고 "Lev 추측의 셋째 가지를 수정해야 함을 보이는 구성"이라는 본문 취지를 함께 적는 편이 안전하다.
- 1차 조사에 없는 열린 질문: 위 2, 3, 5, 6, 7번.
- 1차 조사가 쓴 "남은 경계 1"(ε 없이)은 본문에서 명시적으로는 "confirm the conjecture whenever ≤ (1−ε)p"라는 서술에서 읽힌 것이며 저자가 별도 문장으로 "ε을 없애라"고 쓰지는 않았다(내 해석).

**팩 적합도.**
- (a) 재료: 추측 1.10과 1.13은 문장이 짧고 정수 또는 작은 p에서 컴퓨터로 확인할 수 있어 checkable 문제로 만들기 쉽다(작은 p, 작은 |A|, |B|, Δ를 전수 탐색해 최소 |A+_R B| 계산). 정리 1.9의 구성과 보조정리 4.1의 6/11 집합도 확인 가능.
- (b) 뺄 것: 정리 1.5(정수판, 본문이 "quite straightforward"라고 적음), 추측 1.2의 (1−ε) 범위(이미 증명), 위 "반례" 서술. 회피 집합 F가 시돈 집합이고 |F| < √p+1/2라는 §5의 서술은 대조군 #30(시돈 집합 최대 크기) 주변 주제여서 직접 겹치지는 않지만 팩에 넣을 때 확인이 필요하다(내 해석).
- (c) 14쪽. 증명은 BLT25의 정리 25–27에 크게 의존해 독립적으로 이해하기 어렵다. 정리와 열린 질문 서술은 쉽게 읽힌다. 팩에는 §1과 §4 구성 부분, §5를 넣고 §3은 요약만 권한다.
- (d) AI 관여 서술: 없음. 감사의 글은 Lev, Bukh, Dong와의 토론과 IBS 프로그램.
- **판정: 상.** 최전선 위치가 숫자로 분명하고 열린 추측이 3개 명시되어 있음. 단 BLT25 없이는 증명 이해가 어렵다.

**필요한 선행 논문.**
1. Bollobás–Leader–Tiba, Large sumsets from small subsets, Israel J. Math. 2025 ([BLT25]). 본문에 arXiv 번호 없음(1차 조사는 2204.07559로 적었으나 검색 요약 기준이라 미확인).
2. Lev, Restricted set addition in groups II. A generalization of the Erdős–Heilbronn conjecture, Electron. J. Combin. 7 (2000) R4 ([Lev00b]). 추측 1.2와 F의 시돈성의 출처. 본문에 arXiv 번호 없음.
3. Green–Ruzsa, Sets with small sumset and rectification, Bull. London Math. Soc. 38 (2006) ([GR06]). 본문에 arXiv 번호 없음.
4. Alon–Nathanson–Ruzsa, The polynomial method and restricted sums of congruence classes, J. Number Theory 56 (1996) ([ANR96]). `[arXiv 없음]`(1996년 논문, 본문 번호 없음. 확실하지 않음)
5. Dias da Silva–Hamidoune, Cyclic spaces for Grassmann derivatives and additive theory, Bull. London Math. Soc. 26 (1994) ([DdSH94]). `[arXiv 없음]`

---

### 2508.18586 — Conlon, Lim, Sums of algebraic dilates (PDF 49쪽, 본문 48쪽, v1 2025-08-26, 읽은 범위: 전체. §4·§6·§7의 보조정리 증명은 구조 위주로 읽고 세부 계산은 확인하지 않음)

**주정리.** 기호: K = Q(λ_1..λ_k)는 수체, d = [K:Q], σ_1..σ_d는 K의 복소수 내장(embedding), D는 분모 아이디얼 {x ∈ O_K : xλ_l ∈ O_K 모든 l}, N(D) = [O_K : D].
- **정리 1.2.** λ_1..λ_k가 대수적 수이면 복소수의 모든 유한 부분집합 A에 대해 |A+λ_1A+…+λ_kA| ≥ H(λ_1..λ_k)|A| − o(|A|), H = N(D)·∏_{i=1}^d (1+|σ_i(λ_1)|+…+|σ_i(λ_k)|). 점근적으로 최선(명제 3.3: 오차 O(|A|^{(d−1)/d})로 상계 달성). 쉬운 말: 대수적 수 배수 합집합의 최소 크기를 "정확한 상수"로 알아냈다.
- **추측 1.1(Krachun–Petrov)**은 k=1에서 이 정리로 완전히 해결된다(H(λ) = 최소다항식의 ∏(|a_i|+|b_i|)).
- **정리 1.7.** L_0..L_k ∈ Mat_d(Z)가 pre-commuting(어떤 P ∈ GL_d(Q)로 PL_i가 서로 가환), 기약(irreducible), 서로소(coprime)이면 |L_0A+…+L_kA| ≥ H(L)|A| − o(|A|), H(L) = ∏(|a_{0i}|+…+|a_{ki}|), det(x_0L_0+…+x_kL_k) = ∏(a_{0i}x_0+…+a_{ki}x_k).
- **따름정리 1.8.** k=1(두 변환)이면 pre-commuting 조건이 자동이므로 L_0, L_1 기약·서로소에서 점근적 최적 하한(Bukh 추측의 교정판 1.3의 k=1을 이전 논문 [7]이 해결, 이번엔 최적 상수).
- **정리 3.1(연속판).** 동시에 대각화 가능한 L_1..L_k와 콤팩트 A ⊂ R^d에 대해 μ(ΣL_lA) ≥ ∏_{i}Σ_l|λ_{li}|·μ(A), 등호 가능.
- **정리 1.9 = 정리 4.14.** 합집합이 |A|의 C배 이하이면 A는 크기 ≤ F|A|, 차원 ≤ n인 "p-proper O_K-GAP"에 들어간다(Freiman 정리의 대수적 변형).

**증명의 뼈대.**
- §2. A ⊂ K로 줄이고(보조정리 2.1), O_K ≅ Z^d로 옮겨 곱셈을 정수 행렬 L_l의 작용으로 바꾼다. 보조정리 2.3: M_l이 모두 C 위에서 대각화됨.
- §3. 연속판(정리 3.1): 고유공간마다 Steiner 대칭화를 하고 Brunn–Minkowski를 쓴다(보조정리 3.2). §3.1에서 하한이 최선임을 구성.
- §4–§5. 대수적 Minkowski 제2정리(보조정리 4.7), 존 정리(4.10), 차원 낮추기(4.11)로 정리 4.14. 이로써 일반 A를 박스 [0,N)^d의 조밀한 부분집합으로 보내는 Freiman 동형 사상을 얻는다(§5).
- §6–§8(핵심 새 아이디어). 격자 밀도(lattice density) LD(A;F)를 정의한다(주기 집합 A와 격자의 flag F에 대해, 콤팩트 하향집합 ⊂ [0,1]^k). A를 R^{d+k+1}의 콤팩트 집합 "밑면 ≈ A, 섬유 = 국소 격자 밀도"로 표현한다. 정리 6.5(합의 격자 밀도가 성분별 max를 포함), 보조정리 7.1–7.2(flag 가족 F_n, G_n이 사영을 보존), 정규성 보조정리 7.4–7.5(유계 개수의 부분 정육면체로 쪼개 대부분의 A를 정규 정육면체에 넣음). §8 주장 8.2: L_0′X+…+L_k′X ⊆ Y를 보이고 정리 3.1을 적용한다.
- §9. 정리 1.7을 정리 1.2로 환원: 정리 9.1(분모 아이디얼의 노름 = 노름 다항식의 분모, Gauss 보조정리의 O_K판 9.3), 정리 9.4(pre-commuting + 기약 + 서로소이면 어떤 수체의 곱셈과 동치).

**방법이 막히는 곳.**
1. 정수 λ용 관찰 1.10("A+LA의 국소 밀도가 A 이상")은 λ가 정수가 아니면 너무 약하다. 밀도가 1/|det L_1|배로만 보장됨. 그래서 비대칭 합 L_1A_1+L_2A_2와 "ηη′ ≥ σ_1σ_2"(관찰 1.11)로 우회(§1.1, p.6).
2. 모든 l에 동시에 맞는 flag 쌍은 없다: "there are no pairs of flags ... that simultaneously satisfy Lemmas 7.1 and 7.2 for all l"(§7.1, p.35). 그래서 n→∞의 안정성(정규성)에 의존. 격자 밀도 자체의 수렴은 "we make no attempt to formally prove"(p.35).
3. 정리 3.1은 동시 대각화(고유공간 분해와 Steiner 대칭화)에 의존하므로 pre-commuting이 아니면 쓸 수 없다(§3 첫머리, §10).
4. 오차항: 논증을 따라가면 o(|A|)는 O(|A|/√log_(k)|A|)(k번 겹친 로그의 제곱근)로 "clearly not best possible"(§10, p.48). (내 해석: 정규성 보조정리 7.4–7.5를 k번 반복하고 R_0 = M^d/(εδ²) 꼴 상수가 쌓이는 구조와 Freiman 정리의 정량적이지 않은 상수 n, F가 이런 약한 오차의 원천으로 보이나 저자가 원인을 명시하지는 않았다.)
5. 이전 논문 [7]의 k=1, λ = (p/q)^{1/d} 경우에는 O(|A|^{1−σ}) 오차를 얻었으나 "the methods of that paper and this one are quite orthogonal"(§10, p.48).

**본문 전체에서 나온 열린 질문.**
1. 오차항을 O(|A|^{1−1/d})로: 구성(§3.1)이 이 값을 시사하나 "likely to be difficult"(§10, p.48).
2. 적어도 λ_1..λ_k에만 의존하는 σ > 0으로 O(|A|^{1−σ}): "it would already be interesting"(§10, p.48). 새 방법이 필요할 것이라고 적음.
3. pre-commuting이 아닌 L_0..L_k: "The main problem left open by this paper"(§10, p.48).
4. 구체적 예: L_0 = [[0,1,0],[−1,0,0],[0,0,0]], L_1 = [[0,0,1],[0,0,0],[−1,0,0]], L_2 = [[0,0,0],[0,0,1],[0,−1,0]]. 기약·서로소이나 pre-commuting이 아니다. 추측: |L_0A+L_1A+L_2A| ≥ 8|A|−o(|A|)이고 박스 [0,N)^3이 최적을 보인다. 저자는 "unable to even prove that there is some C > 0 such that |L_0A+L_1A+L_2A| ≥ C|A|"(§10, p.48). 정수 격자 Z^3의 부분집합에 관한 유한 질문이라 컴퓨터 탐색이 가능하다.
5. 추측 1.3(교정된 Bukh 추측): L_i ∈ Mat_d(Z) 기약·서로소일 때 |ΣL_iA| ≥ (Σ|det L_i|^{1/d})^d|A|−o(|A|). 본문은 k=1은 [7]이 해결, 이번 논문은 pre-commuting에서 다른(더 강한) 상수 H(L)를 줌. 일반 k에서 참값은 열림(§1, p.3–4).

**1차 조사와 다른 점.**
- 일치: 정리 1.2의 H, 오차 O(|A|/√log_(k)|A|), 열린 문제 두 가지(오차항, 비pre-commuting 3×3 예), 3×3 예 존재. 쪽수는 PDF 49쪽(본문 48쪽)이며 1차 조사 지시문의 50쪽과 약간 다름.
- 1차 조사에 없는 것: 오차 목표값 O(|A|^{1−1/d}), "C|A|조차 못 보임", 추측 8|A|(본문에서 나온 숫자), 교정된 Bukh 추측 1.3이 일반 k에서 열려 있다는 점.
- 1차 조사는 Shakan(2014)이라 적었으나 본문 참고문헌은 Combin. Probab. Comput. 25 (2016)이다(arXiv 판 연도는 다를 수 있음).
- 1차 조사가 표에 적은 Conlon–Lim 2409.17112(소수 위수군에서)는 이 본문의 참고문헌에 없다. 이 논문의 선행 계보는 [6]=초월 확대(2023), [7]=선형변환의 합, [12][13]=Krachun–Petrov.
- 1차 조사는 정리 1.7의 pre-commuting 가정을 "응용" 서술에서 따로 적지 않았다.

**팩 적합도.**
- (a) 재료: §1(정리 1.2, 1.7, 추측 1.1, 1.3), §3.1 구성, §10 전체. checkable 문제로는 (i) 구체적 대수적 수(예: 1+√2, (1+√5)/2, 2^{1/3})의 H 계산과 Z[λ] ≅ Z^d에서 작은 집합의 |A+λA|/|A| 점검, (ii) §10의 3×3 예에서 작은 A ⊂ Z^3의 |L_0A+L_1A+L_2A|/|A|를 최소화하는 탐색(8 미만이 나오는지)을 만들기 쉽다.
- (b) 뺄 것: 추측 1.1(해결됨), 대수적 정수 λ의 Krachun–Petrov 결과(해결됨), 유리수 λ의 Bukh 결과, k=1 L_0, L_1 결과(해결됨). 대조군 #28 #30 #36 #39 #52 #66 #200 #241 #324 관련 서술은 본문에 없음. 곱셈은 λ_i로 곱하는 상수배뿐이라 합-곱(#52)과는 다름.
- (c) 49쪽으로 가장 길다. 대수적 수론(수체, 정수환, 아이디얼 노름), 측도(Brunn–Minkowski, Steiner), Freiman 정리를 모두 요구해 철학 전공자가 읽기엔 어렵다. 팩에는 §1(약 8쪽: 정리와 증명 스케치)과 §10(약 1쪽)만 발췌하기를 권한다. §4–§8은 팩에서 빼도 열린 질문을 이해하는 데 지장이 없다.
- (d) AI 관여 서술: 없음. 감사의 글은 Singhal 교수의 도움과 NSF 연구비.
- **판정: 중.** 최전선의 위치와 열린 질문은 선명하지만 분량·난이도가 커서 발췌가 필수. 열린 질문(3×3 예)은 구체적이라 문제 재료로는 좋음.

**필요한 선행 논문.**
1. Krachun–Petrov, Tight lower bound on |A+λA| for algebraic integer λ, arXiv:2311.09399 ([13]). 이번 논문의 3단계 뼈대의 직접 선행.
2. Conlon–Lim, Sums of linear transformations, Trans. Amer. Math. Soc.(to appear) ([7]). 본문에 arXiv 번호 없음. 교정된 Bukh 추측 1.3의 출처이자 k=1 결과.
3. Krachun–Petrov, On the size of A+λA for algebraic λ, Mosc. J. Comb. Number Theory 12 (2023) ([12]). 추측 1.1의 출처. 본문에 arXiv 번호 없음.
4. Bukh, Sums of dilates, Combin. Probab. Comput. 17 (2008) ([4]). 유리수 λ의 결과. 본문에 arXiv 번호 없음.
5. Bruch–Jing–Mudgal, Brunn–Minkowski type estimates for certain discrete sumsets, arXiv:2409.05638 ([3]). 이산 Brunn–Minkowski 계열 최신.

---

### 2610.25271 — Wang, Zeng, Inverse zero-sum problems of Erdős–Ginzburg–Ziv constant: Property C and Property D conjectures (7쪽, v2 2026-10-25, 읽은 범위: 전체)

**주정리.** 기호: C_n^r은 Z/nZ의 r개 곱(각 원소는 n으로 나눈 나머지 r개짜리 벡터). "수열"은 원소의 중복을 허용하는 목록. s(G)는 "길이 n(= G의 지수)인 영합(합이 0인) 부분수열이 반드시 생기려면 필요한 최소 길이", η(G)는 "길이 n 이하의 비어 있지 않은 영합 부분수열". T^{n−1}은 T의 각 원소를 n−1번씩 반복한 수열.
- **정리 1.1.** r ≥ 4이고 n ≥ 2가 짝수이면 C_n^r이 Property D를 가질 필요충분조건은 n이 2의 거듭제곱이다. 더 정확히 n = 2^a m(a ≥ 1, m ≥ 3 홀수)이면 s(C_n^r) ≥ 2^r(n−1) + 2^{r−3}(m−1) + 1, 또 η(C_n^r) ≥ (2^r−1)(n−1) + 2^{r−3}(m−1) + 1.
- **따름정리 3.6.** 같은 조건에서 Property C도 n이 2의 거듭제곱일 때만 성립.
- 쉬운 말: "가장 긴 영합 회피 수열은 한 가지 규칙적인 모양(같은 원소를 똑같이 n−1번씩)이다"라는 2006·2007년의 추측(Property D, C)이 짝수이면서 2의 거듭제곱이 아닌 n(예: 6, 10, 12)에서 틀린다. 4차원 이상에서만 보였다.
- 범위: n 짝수만, r ≥ 4만. 홀수 n과 r ≤ 3은 다루지 않음. n이 2의 거듭제곱이면 s = 2^r(n−1)+1과 Property D는 이전 결과(명제 3.3, Harborth 1973과 Gao–Thangadurai 2003).

**증명의 뼈대.**
- 보조정리 3.1: n이 짝수이면 Property D가 있을 때 s(C_n^r) = 2^r(n−1)+1이다(T가 mod 2로 단사여야 하므로 |T| ≤ 2^r). 따라서 Harborth 하한 2^r(n−1)+1을 한 번이라도 넘는 수열이 있으면 Property D가 틀린다(수치 조건이 곧 구조 반례).
- 보조정리 3.2: 랭크를 올릴 때 {0,1}^{r−d}의 각 점마다 복사해 길이를 2^{r−d}배로 늘린다.
- **구성(§3)**: n = km(k = 2^a, m 홀수)에 대해 C_n^4 안에 18개 점(표 1: 9개 라벨 P=(x,y,z), 각 행에 t 값)을 잡는다. 16개는 n−1번, 2개는 m−1번 반복. 점 g(P,t) = (y, x−z, q(P,t), t), q는 중국인의 나머지 정리로 정함. 길이 16(n−1)+2(m−1).
- **명제 3.5(핵심)**: 이 수열은 길이 n의 영합 부분수열이 없다. 3단계 증명: (1) 평균 (y/n, (x−z)/n)가 라벨 삼각형 안의 격자점이어야 해 모든 항이 한 변에 있다. (2) 각 변에서 mod k, mod m 합동으로 모든 항의 라벨이 같음. (3) 네 번째 좌표로 n−1 복사본 한계에 걸린다.
- 정리 1.1과 따름정리 3.6은 보조정리 3.2, 3.4(η 하한)로 마무리. 새 아이디어는 구성(표 1과 명제 3.5)에 있다.

**방법이 막히는 곳.** 저자가 "이 방법으로는 안 된다"고 쓴 곳은 없다. 구조상 한계:
1. 방법은 짝수 n에서만 작동한다. Property D가 짝수에서 "Harborth 하한과의 등식"을 강제하는 짝수성(parity) 논증(보조정리 3.1)에 기대기 때문(§1, p.2).
2. 구성이 4차원이라 r ≥ 4만 얻는다(랭크 올림은 보조정리 3.2).
3. 결과는 하한이고 참값 s(C_n^r)는 모른다.

**본문 전체에서 나온 열린 질문.** 저자가 질문 문장으로 적은 것은 없다. 본문에서 읽히는 경계:
1. 홀수 n에서 Property C, D가 성립하는가(본문은 짝수에만 정리, 서론 p.2: "every even exponent with an odd prime divisor").
2. r = 2, 3에서 짝수이고 2의 거듭제곱이 아닌 n(예 C_6^2, C_6^3)의 Property C, D. 본문 §1 p.2는 r=2에서 Schlage-Puchta가 "C_p^2 has Property D for every sufficiently large prime p"(p.2)를 증명했다고만 적는다. 구성이 r ≥ 4에서만 나오므로 r ≤ 3은 이 논문이 말하지 않는다(내 해석).
3. Gao의 추측 s(G) = η(G)+exp(G)−1(§1, p.2, [8, Conjecture 6.5]). Property D는 이 등식을 함의하지만 Property D가 틀렸다고 해서 등식이 틀린 것은 아니다. 본문은 이 추측의 진위를 다루지 않는다.
4. 참값 s(C_n^r)(짝수, 2의 거듭제곱 아님): 하한만 있음.
5. Property B(C_n^2의 길이 2n−1 최소 영합 수열이 n−1번 반복되는 원소를 가짐)와 랭크 2의 성질들(§1, p.2): 본문 문헌 소개로만 언급.

**1차 조사와 다른 점.**
- 일치: 정리 1.1, 따름정리 3.6, v1(Wang 단독, n=6)과 v2(Zeng 공저) 이력, 홀수 n 미언급.
- 1차 조사가 적지 않은 것: **r ≥ 4 조건에서 r ≤ 3이 빠진다**는 점(특히 C_6^2, C_6^3). 1차 조사는 "모든 r ≥ 4"로 썼으나 r ≤ 3의 열린 상태를 경계에 올리지 않았다.
- 1차 조사 지적대로 이 본문에는 저자가 직접 적은 열린 질문이 없고 "남은 경계"는 읽는 쪽이 만든 것이다.

**팩 적합도.**
- (a) 재료: 표 1과 명제 3.5(18점 구성, n = 6이면 컴퓨터로 확인 가능), 보조정리 3.1의 수치 조건, r < 4와 홀수 n의 미해결 상태. checkable로 만들기 쉽다: 작은 n에서 길이 > 2^r(n−1)인 영합 회피 수열의 존재 확인, 명제 3.5를 n = 6, 10에서 전수 확인.
- (b) 뺄 것: 추측 A(Property C)와 B(Property D)는 반증된 사실이므로 팩에서 "열린 추측"으로 소개하면 안 된다. 서론의 s(C_n^2) = 4n−3(Reiher)과 Schlage-Puchta의 랭크 2 결과는 참고용. 대조군 관련 서술 없음.
- (c) 가장 짧다(7쪽). 영합 이론 용어(수열, 짧은 영합, 보조 군) 설명이 필요하나 구성은 구체적. 표 1이 텍스트 추출에서 깨져 있으므로 팩에는 PDF나 직접 옮긴 표가 필요하다.
- (d) AI 관여 서술: 없음. 감사의 글은 중국 국가자연과학기금 번호뿐.
- **판정: 상.** 짧고 구체적이며 컴퓨터 확인이 쉬움. 약점은 저자가 열린 질문을 직접 쓰지 않았다는 점이라 열린 질문은 팩 작성자가 정리해야 한다. 2610.35819와 함께 읽는 구성이 자연스럽다.

**필요한 선행 논문.**
1. Gao–Geroldinger, Zero-sum problems in finite abelian groups: a survey, Expo. Math. 24 (2006) ([8]). Property D와 Conjecture 7.2의 출처. 본문에 arXiv 번호 없음.
2. Gao–Hou–Schmid–Thangadurai, On short zero-sum subsequences II, Integers 7 (2007) A21 ([11]). Property C 질문(Open Problems 1.2)의 출처. 본문에 arXiv 번호 없음.
3. Elsholtz, Lower bounds for multidimensional zero sums, Combinatorica 24 (2004) ([4]). 표 1의 9개 라벨 배치의 출처(p.354). 본문에 arXiv 번호 없음.
4. Schlage-Puchta, All large primes have Property D, arXiv:2509.02436 ([16]). 랭크 2의 최근 결과.
5. Edel–Elsholtz–Geroldinger–Kubertin–Rackham, Zero-sum problems in finite abelian groups and affine caps, Q. J. Math. 58 (2007) ([3]). 영합 수열과 affine cap의 연결. 본문에 arXiv 번호 없음.

---

### 2610.35819 — Elsholtz, The Erdős–Ginzburg–Ziv constant of C_n^r for even n: rigid sequences, products, and growth beyond Harborth's bound (14쪽, v2 2026-10-27, 읽은 범위: 전체. 부록 표 4의 210개 증명서는 구조만 보고 개별 검산은 하지 않음)

**주정리.** 기호는 2610.25271과 같고 n = 2^a m(a ≥ 1, m ≥ 3 홀수). "무거운(heavy) 항"은 n−1번 반복되는 항, "가벼운(light) 항"은 m−1번 이하 반복되는 항.
- **정리 1.3.** r ≥ 4이면 s(C_n^r) ≥ 2^r(n−1) + (m−1)·2^{r−3}·⌊r/4⌋ + 1, η(C_n^r) ≥ (2^r−1)(n−1) + (m−1)·2^{r−3}·⌊r/4⌋ + 1. 4 ≤ r ≤ 7에서는 Wang–Zeng(정리 1.2)과 같고 r ≥ 8부터 더 강하다. 쉬운 말: 위반 크기(Harborth 하한 초과분)가 2^r의 고정 배수가 아니라 r·2^r 규모로 자란다(따름정리 1.5: ≥ (m−1)·r·2^r/64).
- **정리 1.4(n ≡ 2 mod 4, 곧 n = 2m).** (a) s(C_n^5) ≥ 32(n−1)+8(m−1)+1 (Wang–Zeng의 초과분 4(m−1)을 개선), η도 대응. (b) r ≥ 5에서 초과분 (m−1)·2^{r−2}·⌊r/5⌋. (c) 4차원 블록과 5차원 블록을 섞으면 (m−1)·2^r·μ(r), μ(r) = max{a/4+b/8 : 5a+4b ≤ r}.
- **정리 4.3(곱 정리).** "견고한(rigid) 수열" S_1..S_t의 텐서곱 S_1⊗…⊗S_t는 길이 n의 영합 부분수열이 없다. 명제 5.1: Wang–Zeng 수열은 견고하다.
- **명제 3.3과 따름정리 3.4.** Property D의 재정식화: 임계 길이 L = (m−1)M_m(r)에서 구조가 T^{m−1}꼴이 아닌 수열이 하나라도 있으면 s의 참값에 상관없이 Property D가 틀린다.
- **추측 8.1과 명제 8.2.** 길이 s(G)−1인 영합 회피 수열의 n항 부분수열 합들은 G의 0이 아닌 모든 원소를 덮는다(추측). 한 항이 n−1번 반복되면(극대 수열에서) 이것이 성립(명제 8.2, 따름정리 8.3).

**증명의 뼈대.**
- §2–§3. 도구: 배가 보조정리 2.3(점마다 {0,1}을 붙여 랭크 +1, 길이 ×2), 약수 보조정리 3.1(d | m이면 mod d 사영이 단사이고 M_m(r) ≤ M_d(r)), 따름정리 3.2(M_m(3)=9, M_m(4)=20 등, 3 | m인 홀수 m).
- §4. 정의 4.1(견고) → 곱 정리 4.3: 곱의 영합을 각 블록에 사영하면 x^n 꼴이거나 h^a ℓ^{n−a} 꼴이고, 모순을 만든다. Remark 4.4: 견고한 수열의 곱이 다시 견고한 것은 아니라서 반복하지 않고 직접 곱한다.
- §5. Wang–Zeng의 18점 수열이 견고함을 증명(명제 5.1: 삼각형 논증 + 한 행 논증 + 행 내부). j개 곱으로 정리 1.3.
- §6–§7(새 아이디어). n = 2m에 대해 "glued 수열"(라벨 ∈ F_2^r는 무거운 항마다 서로 다르고 mod m 지지집합이 m-good) 개념과 곱 정리 6.4. 5차원 블록 S_5(n): C_5의 V_4 = {−1,0,1}^4의 20점 원뿔과 {0,1}의 곱 40점(표 3: 32개 무거움, 8개 가벼움). 정리 7.2: S_5(2m)은 길이 2m의 영합 부분수열이 없다. 증명은 4개의 합동식과 210개 벡터에 대한 증명서(표 4)로 경우를 나눈다.
- §8. 추측 8.1과 명제 8.2.
- §9. 모든 정리는 구성에 의한 하한이며 컴퓨터는 구성과 증명서를 찾는 데만 쓰였고, 분석적 정리와 "explicit case study"(정리 7.2)와 증명에 쓰이지 않는 검산을 구분해 적는다.

**방법이 막히는 곳.** 이 논문은 막힌 곳을 구체적으로 많이 적었다(§10과 본문 곳곳).
1. 견고함의 곱은 견고하지 않다: a+b ≥ n이면 반례(Remark 4.4, p.5).
2. 5차원 블록은 견고함을 확인할 수 없고(§6 첫머리, p.7) n = 2m인 경우에만 glued 경로가 있다. n ≡ 0 mod 4에서는 4차원 블록뿐. 5차원 블록 S_5의 직접 유사물(C_4^5에서 0/1 라벨)은 n = 12, 20에서 영합이 생긴다(§10(3), p.11).
3. 최대 cap은 지지집합으로 쓸 수 없다: 20점 cap과 Edel의 42점, 96점 집합에는 "가벼운 항을 붙일 쌍"이 없다(Remark 7.4, p.10).
4. n = 2q(q 홀수 소수)에서 s(C_q^4) = 20q−19, s(C_q^5) = 42q−41이 **추측대로라고 가정하면** 부분군 상계와 하한 사이가 2(q−1) 벌어진다. 4차원에서 좁히려면 지지집합이 ≥ 20점이어야 하고 Wang–Zeng 수열은 확장 불가, 20점 집합들에는 m = 3, 5, 7에서 가벼운 항을 붙일 수 없음(전수 계산)(§10(2), p.11).
5. 3차원: 부분군 상계 17q−9가 Harborth 16q−8보다 가벼운 항 하나만큼 크지만 n = 6, 10에서 탐색해도 못 찾음(§10(2)).
6. 5차원에서 42점 지지집합: q = 5, 7에서 "modifying, doubling and twisting the 20-point sets"로도 못 찾음(§10(2)).
7. 6차원: 가벼움 밀도 1/4은 5차원 블록의 곱보다 나을 게 없다(§10(4), p.11).
8. 홀수 n: 반례가 없다. C_9^3 등에서 "한 무거운 항을 h^a ℓ^{n−1−a}로 바꾸기"는 전수 탐색에서 불가능, C_135에서 길이 126 수열을 simulated annealing으로 탐색해도 실패: "this is evidence about these searches, not about Property D"(§10(5), p.12).
9. 정리 1.4의 증명은 컴퓨터가 찾은 210개 증명서에 의존하고 기계 판독 가능한 표는 "available from the author"(§7, p.10)라 독립 재검토가 쉽지 않다.

**본문 전체에서 나온 열린 질문.**
1. 추측 8.1: 길이 s(G)−1인 영합 회피 수열의 n항 합들이 0 아닌 모든 원소를 덮는다(§8, p.10).
2. 약한 Property D: 길이 s(C_n^r)−1 수열이 항상 n−1번 반복되는 항을 갖는가. "which is open for all groups C_n^r with r ≥ 2 where Property D is not known"(§8, p.10).
3. §10(1): 초과분의 참값. 하한은 (m−1)·r·2^r 규모, 부분군 상계 s(C_{2^r m'}) ≤ m'2^r+s(C_{m'}^r)는 "exponentially larger"(§10(1), p.11). 그 사이의 간격 전체.
4. §10(2): n = 2q에서 rank 4의 2(q−1) 간격과 rank 5의 2(q−1) 간격. 4차원 ≥ 20점 지지집합, 5차원 42점 지지집합, 3차원에서 가벼운 항 하나(n = 6, 10)를 찾아라.
5. §10(3): n ≡ 0 mod 4에서 가벼움 밀도 1/4인 5차원 블록: "A rank-five block with light density 1/4 would improve Theorem 1.3"(p.11).
6. §10(4): 5차원 블록 곱(밀도 r/20)을 넘는 더 큰 블록: "Better rates would need blocks of light density larger than r/20"(p.11).
7. §10(5): 홀수 n에서 Property C, D가 성립하는가. 특히 C_135 = C_15^3: "whether Property D holds for C_135"(p.12). s(C_135) = 127은 알려져 있어 길이 126 수열의 구조 문제.
8. 3 | m인 홀수 m의 3, 4차원: Property D는 임계 길이 9(m−1), 20(m−1)에서의 유일성 문제가 된다(§3 끝, p.4).
9. 랭크 2: Property D는 n ∈ {2,3,5,7}과 충분히 큰 소수에서만 알려짐, 랭크 3에서 C_2^{3a}, C_3^{3a}, C_5^{3a}만(§1, p.1).

**1차 조사와 다른 점.**
- 1차 조사 "남은 경계 5"는 (가) rank 4 간격 2(q−1), (나) n ≡ 0 mod 4용 rank-5 블록, (다) 42점 지지집합. 맞다. 단 (가)(다)는 **s(C_q^4) = 20q−19, s(C_q^5) = 42q−41이 추측대로라는 가정 아래**의 간격이고 n = 2q(q 홀수 소수) 한정이다(1차 조사에는 조건이 빠져 있음).
- 1차 조사에 빠진 열린 질문: 추측 8.1, 약한 Property D, §10(1) 상·하한 간격, §10(2) 3차원, §10(4) 더 큰 블록, §10(5) C_135의 Property D.
- 1차 조사는 Han–Zhang(2610.40095)의 s(C_n^r) ≤ 4^r n을 "참값의 위쪽 끝"으로 적었다. 이 본문(2610.35819)에는 Han–Zhang도 4^r n도 나오지 않는다. 본문이 말하는 상계는 부분군 상계(§10(1))뿐이다. 4^r n은 Han–Zhang 원문에서 따로 확인해야 한다.
- AI 관여는 일치("Use of AI tools": Claude(Anthropic, Opus 5.5)와 ChatGPT, 접근 논의·컴퓨터 탐색 작성과 실행·원고 초안, 초안은 ChatGPT와 저자가 점검). 추가: 정리 1.4의 증명은 컴퓨터가 찾은 210개 증명서에 의존한다(§9 분류 "By an explicit case study").
- v1이 Wang–Zeng v2를 보지 못한 상태에서 n ≡ 2 mod 4, r ≥ 4에 대해 초과분 2^{r−2}를 18점 구성으로 얻었다는 점은 일치("A note on the versions", p.2). Wang의 첫 수열은 C_6^4에서 길이 81(p.2).

**팩 적합도.**
- (a) 재료: §10 전체(질문 7개), 추측 8.1과 약한 Property D, 정의 4.1–정리 4.3, 표 3. checkable로 만들기 가장 쉬운 본문이다(작은 n, r에서 추측 8.1 점검, 표 3의 S_5(6)에서 영합 부분수열 부재 확인, n = 12에서 C_4^5 직접 유사물에 영합이 있는지, 4차원에서 20점 cap에 가벼운 항을 붙일 수 있는지).
- (b) 뺄 것: 표 4와 부록(210개 증명서, 개별로는 읽을 필요 없음, 분량 큼), 2610.25271이 이미 해결한 Property C/D의 반증(정리 1.2는 인용이므로 중복), 서론의 Property D 이력.
- (c) 14쪽이지만 본문은 실질 약 10쪽, 부록 3쪽이 표. 영합 용어와 정의 4.1의 "견고"를 쉬운 말로 풀어야 한다. 2610.25271을 먼저 읽는 순서가 필요.
- (d) **AI 관여 서술이 있다.** 본문 끝 "Use of AI tools"에 Claude(Anthropic, 모델 Opus 5.5)가 접근법 논의, 컴퓨터 탐색 코드, 원고 초안에 쓰였다고 적힘. Opus는 이 실험의 피험 모델 계열이므로 팩에 넣을지는 연구자가 정할 설계 판단이다(1차 조사와 같은 지적). 팩에 넣는다면 이 문단을 남길지 지울지도 같은 판단에 속한다.
- **판정: 상(내용). 단 피험 모델 관여로 설계 판단이 선행되어야 함.** 열린 질문이 가장 풍부하고 컴퓨터 확인이 쉬우나 Claude 관여 때문에 조건부.

**필요한 선행 논문.**
1. Wang–Zeng, arXiv:2610.25271 (이 목록에서 별도 논문으로 이미 있음, [20]). Wang의 v1([19])도 같은 번호의 v1.
2. Edel–Elsholtz–Geroldinger–Kubertin–Rackham, Zero-sum problems in finite abelian groups and affine caps, Q. J. Math. 58 (2007) ([3]). 위 논문과 공통. 본문에 arXiv 번호 없음.
3. Edel, Sequences in abelian groups G of odd order without zero-sum subsequences of length exp(G), Des. Codes Cryptogr. 47 (2008) ([1]). 42점·96점 집합의 출처. 본문에 arXiv 번호 없음.
4. Elsholtz, Lower bounds for multidimensional zero sums, Combinatorica 24 (2004) ([5]). 9점 집합 T_0의 출처. 본문에 arXiv 번호 없음.
5. Gao, Two zero sum problems and multiple properties, J. Number Theory 81 (2000) ([8]). Property D의 도입. 본문에 arXiv 번호 없음. (참고: Elsholtz [6] An alternative proof on four-dimensional zero-sums, RMS Lecture Notes 23 (2016)는 20점 집합의 출처이나 5편 한도로 뺌)

---

## 부록: 선행 논문 중 arXiv 번호가 본문에 없는 것 (arXiv 존재 여부는 이번에 조회하지 않음)

- arXiv에 없을 것이 확실한 것: Behrend 1946, Dias da Silva–Hamidoune 1994, Alon–Nathanson–Ruzsa 1996, Gao 2000(J. Number Theory), Harborth 1973, van Emde Boas 1969(Mathematisch Centrum 보고서), Tao–Vu 교재.
- 번호가 본문에 없어 조회가 필요한 것: Green–Wolf 2010, Elsholtz–Pach 2020, Bollobás–Leader–Tiba 2025(1차 조사는 2204.07559), Lev 2000(EJC), Green–Ruzsa 2006, Conlon–Lim "Sums of linear transformations", Krachun–Petrov "On the size of A+λA for algebraic λ", Bukh 2008, Gao–Geroldinger 2006, Gao–Hou–Schmid–Thangadurai 2007, Elsholtz 2004, Edel 2008, Edel et al. 2007.
- 번호가 본문에 있는 것: Bloom–Sisask 2309.02353, Krachun–Petrov 2311.09399, Bruch–Jing–Mudgal 2409.05638, Schlage-Puchta 2509.02436.
- 확실히 arXiv 밖인 AI 관련 선행: Romera-Paredes et al.(Nature 2024)은 arXiv에 없을 것으로 보이나 확인하지 않음.
