# 정독 결과 H2 (K13 두 편, K14 두 편)

작성일 2026-11-06. 맡은 논문 4편을 `fulltext/<번호>.txt`로 처음부터 끝까지 읽었습니다(본문, 부록 없음, 참고문헌 포함). 수식이 깨진 곳은 문맥과 직접 계산으로 확인했고, PDF 쪽수 렌더러(pdftoppm)가 없어 PDF 이미지는 보지 못했습니다. 아래 `[추론]` 표시는 본문에 그대로 적혀 있지 않고 제가 본문 내용에서 이끌어 낸 해석입니다.

---

### 2605.03181 — Alexandre Bailleul, Robin Riblet, On the largest Sidon subset in a finite subset of R^N (11쪽, 읽은 범위: 전체)

**주정리.**
- Theorem 2.2: n개 정수 집합 E 중 가장 불리한 것을 잡아도 그 안에 크기 (1/(3√3) + o(1))√n ≳ 0.19√n 인 시돈 부분집합이 있습니다. 즉 H(n) ≥ (1/(3√3)+o(1))√n. 여기서 H(n)은 n개 정수 집합 전체에 대한 min over E, max over S⊂E 시돈입니다(식 (3)). 쉬운 말로: 아무 정수 n개를 줘도 그 안에서 "합이 모두 다른" 수를 √n의 약 19%만큼은 반드시 고를 수 있습니다.
- Theorem 2.1: R^N의 n개 점에서도 같은 하한이며 차원 N에 의존하지 않습니다(F_N(n) ≥ (1/(3√3)+o(1))√n). Lemma 2.6과 2.7이 F_N(n) = F_1(n) = H(n)을 보입니다. 따라서 평면 점 n개에서 평행사변형이 없는 ⌊0.19√n⌋개, 실수 n개에서 서로 다른 거리만 만드는 ⌊0.19√n⌋개, 중점이 모두 다른 점들을 뽑을 수 있습니다(쪽 2).
- Theorem 3.3: 고정된 N, g ≥ 1에 대해 B_2[g] 집합(어떤 합이든 표현이 g개 이하)으로 바꾸면 F_{g,N}(n) ≥ (√g/(3√3) + o(1))√n ≳ 0.19√(gn).
- 이전 기록(본문 쪽 2): Mian–Chowla c·n^{1/3}, Komlós–Sulyok–Szemerédi (0.0000305+o(1))√n, Abbott 1990 (0.0805+o(1))√n. 상계는 Erdős–Turán의 s(1,n) < √n + O(n^{1/4})에서 바로 나옵니다. 즉 현재 H(n)은 0.19√n ≲ H(n) ≲ √n 사이에 있고, Erdős 추측은 H(n) ~ √n입니다.

**증명의 뼈대.**
- 2.1절 Lemma 2.3(핵심 새 아이디어, "압축 보조정리"): 유한 A ⊂ Z와 m에 대해, |C| ≥ |A|/2 − |A|²/(2m)인 C ⊆ A와 C에서 Z/mZ로 가는 단사 Freiman 2-사상(x+y=z+t이면 φ(x)+φ(y)=φ(z)+φ(t))이 존재합니다. 만드는 법: 무작위 θ∈[0,1)를 잡고 φ_θ(a) = ⌊amθ⌋ mod m, B_θ = {a : {amθ} < 1/2}로 정의하면 B_θ에서는 올림이 생기지 않아 φ_θ가 합을 보존합니다. θ에 대해 평균을 내어 |B_θ|의 기댓값 ≥ n/2, 충돌 쌍의 기댓값 ≤ n²/(2m)를 얻고, 충돌마다 한 원소씩 지워 단사로 만듭니다. 측도 보존은 Lemma 2.4(x→kx mod 1이 르베그 측도를 보존).
- Lemma 2.5(Singer): q가 소수 거듭제곱이면 Z/(q²+q+1)Z는 크기 q+1인 시돈 집합 q+1개로 덮입니다. 쪽 3의 이 보조정리는 인용이며 증명은 Singer 1938에 있습니다.
- Theorem 2.2의 증명: m = p²+p+1 ≈ cn으로 잡고(c>1, 소수 정리로 이런 소수 p가 있음) Lemma 2.3으로 |C| ≈ (1/2 − 1/(2c))n을 얻고, Singer의 p+1개 시돈 집합 중 비둘기집 원리로 하나가 φ(C)를 (c−1)/(2c√c)·√n 이상 포함합니다. 이를 φ⁻¹로 끌어올리면 시돈입니다(단사 Freiman 사상이므로). f(c) = (c−1)/(2c√c)는 c=3에서 최대이고 f(3) = 1/(3√3)입니다(쪽 6~7).
- 2.2절(R^N으로 확장): Lemma 2.6은 점들을 서로 다르게 보내는 직선 위로 사영, Lemma 2.7은 디리클레 근사로 실수를 공통 분모 정수로 바꾸면서 시돈성을 유지(M>4 조건이 4/M<1을 보장).
- 3절: Lemma 3.1은 Singer 덮개를 Z/gNZ로 끌어올려 크기 g(q+1)인 B_2[g] 집합 q+1개로 덮는 일반화이고, 나머지는 같은 증명입니다(x = cn/g로 근사). 3.2절은 x_1+…+x_k = y_1+…+y_k 꼴로 확장하는 방법의 스케치(B_θ(k) = {a : {amθ} < 1/k}, Freiman k-사상)입니다.

**방법이 막히는 곳.**
- 이전 방법: 쪽 2 "The need to discard some residues at each step is what causes the losses in the constant." 단계마다 잔여류를 버리는 데서 상수 손실이 생겼고, 이 논문은 그것을 한 번의 압축으로 바꿨다고 합니다.
- 이 방법의 남은 손실(쪽 6, 증명 직전 문단): m을 너무 크게 하면 Singer 덮개가 퍼져 압축된 원소의 집중이 줄고, 너무 작으면 충돌이 늘어 "the right choice is to take m of order |A|." 그 결과 상수는 c=3에서 1/(3√3). [추론] 즉 {amθ}<1/2로 절반을 버리는 것과 Singer 덮개 p+1개 중 하나를 고르는 것이 0.19의 원인이며, 이 두 단계를 유지하는 한 f(c)의 최댓값이 한계입니다. 본문은 "최적"이라고 선언하지는 않고 미분으로 c=3을 찾았다고만 적습니다.
- Remark 3.4(쪽 9): g=2일 때는 √g·√m보다 나은 B_2[2] 구성이 알려져 있지만(Habsieger–Plagne [15]) {1,…,m}에서의 구성이라 Z/mZ가 아니며, 큰 순환군에 넣고 이동 논법(Komlós–Sulyok–Szemerédi Lemma 6)을 써도 "weaker bound"가 나온다고 적습니다.
- 3.2절(쪽 9~10): 일반 선형 구성에는 Singer 덮개 같은 것이 보통 없어서 이동 논법으로 바꿔야 하고, 얇은 B_θ(k)를 쓰므로 상수가 더 약해집니다. "We do not pursue here the optimization of the constants for these more general equations."

**본문 전체에서 나온 열린 질문.**
1. Erdős 추측 H(n) ~ √n (쪽 2, "he conjectured that H(n) ∼ √n"). 본문은 Komlós–Sulyok–Szemerédi가 "partially proved the conjecture"(옳은 차수)라고 적고 "열려 있다"는 문장은 쓰지 않습니다.
2. 쪽 1~2 "Beyond these cases, little seems to be known." 도미노 n/2개 안, 처음 n개 소수 안, 처음 n개 제곱수 안의 최대 시돈 집합 크기는? 제곱수 경우는 "stronger bounds than the one obtained in the present article are known; see [20, Section 6]"(Lefmann–Thiele).
3. Remark 3.4: B_2[g], 특히 g=2에서 하한을 개선할 수 있는가(알려진 구성이 Z/mZ가 아니라 바로 못 쓴다).
4. 3.2절: x_1+…+x_k = y_1+…+y_k와 양의 정수 계수의 균형 선형방정식에서 상수 최적화는 미해결(본문이 하지 않았다고 명시).
5. 본문에 번호 붙은 Problem/Question은 없음.

**1차 조사와 다른 점.**
- 1차 조사는 "논문이 'Erdős's conjecture ... remains open'으로 정리"라고 인용했으나 본문에 그 문장은 없습니다(전체 검색 확인). 본문은 "he conjectured that H(n) ∼ √n"과 Komlós–Sulyok–Szemerédi가 "partially proved the conjecture"라고만 적습니다.
- 남은 경계 2번(도미노, 소수, 제곱수)을 "little seems to be known"으로만 옮겼으나, 같은 문장에서 제곱수는 Lefmann–Thiele가 더 좋은 결과를 갖고 있다고 밝힙니다. 따라서 제곱수 경우를 팩의 "모르는 영역"으로 쓰면 안 됩니다.
- 1차 조사가 빠뜨린 이전 기록: Komlós–Sulyok–Szemerédi (0.0000305)와 Mian–Chowla (n^{1/3}).
- 서론(쪽 1)에 수식 (1)~(2)가 Erdős–Turán, Lindström, Carter–Hunter–O'Bryant의 s(1,n) < √n + 0.98183 n^{1/4} + O(1)을 적습니다. 1차 조사는 "대조군 아님"으로 판정했지만 이 두 줄은 #30(구간 안 최대 시돈 집합 크기)의 배경 정보입니다.
- 참고문헌 [27] 오류: 서론이 "Tao [27] solved one of Erdős's favourite problems on distinct distances"라고 쓰는데 [27]은 1952년 C. R. Acad. Sci. Paris 논문으로 인쇄되어 있어 최근 Tao 결과를 식별할 수 없습니다.

**팩 적합도.**
- (a) 문제 재료: Theorem 2.2의 증명에서 c의 선택(쪽 6~7)과 Lemma 2.3의 두 손실 항; Remark 3.4(B_2[2]); 3.2절의 다른 균형 방정식(예: k=3, B_3류 압축); 쪽 2의 도미노·소수·제곱수 질문; Lemma 2.3의 Z/mZ 압축은 작은 n에서 유한 계산으로 검증하기 쉬움(체커 문제 가능). 이전에 풀린 부분집합 문제(제곱수)는 제외해야 합니다.
- (b) 빼야 할 부분: 쪽 1 하단~쪽 2 상단 식 (1), (2)와 "Thus, equations (1) and (2) imply that s(n) ~ √n" 부근(#30 관련 s(1,n) 상계 진행 상황). 제곱수 문장의 "stronger bounds ... known"은 그대로 둘지 결정 필요(둘 경우 제곱수는 열린 영역이 아님이 분명해짐). 대조군 #28 #36 #39 #52 #66 #200 #241 #324 관련 서술은 본문에 없습니다.
- (c) 난이도와 분량: 11쪽, 측도 보존과 Singer 덮개 외에 고급 도구가 없어 철학 전공자도 구조를 따라갈 수 있는 가장 읽기 쉬운 편입니다. Lemma 2.3 증명이 가장 기술적입니다.
- (d) AI 관여 서술: 없음(감사의 글이 아예 없고 각주에도 없음).

**필요한 선행 논문.**
1. H. L. Abbott, "Sidon sets", Canad. Math. Bull. 33 (1990) — 이전 기록 0.0805 (참고문헌 [1]) [arXiv 없음]
2. J. Komlós, M. Sulyok, E. Szemerédi, "Linear problems in combinatorial number theory", Acta Math. Acad. Sci. Hungar. 26 (1975) ([19]) — 이동 논법의 출처 [arXiv 없음]
3. H. Lefmann, T. Thiele, "Point sets with distinct distances", Combinatorica 15 (1995) ([20], 6절) — 제곱수에서 더 좋은 결과 [arXiv 없음]
4. R. Riblet, "Sidon sets in a union of intervals", Acta Math. Hungar. 167 (2022) ([24]) — 구간 두 개의 경우 0.876 (참고문헌에 arXiv 번호 없음, 존재 여부 미확인)
5. 서론의 "Tao [27]" 최근 결과 — 참고문헌이 잘못 인쇄되어 식별 불가 (arXiv 번호 미상)

---

### 2602.23282 — Jie Ma, Quanyu Tang, Largest Sidon subsets in weak Sidon sets (15쪽, 읽은 범위: 전체)

**주정리.** 정의: 유한 집합이 Sidon이면 x≤y인 모든 합이 서로 다르고, weak Sidon이면 x<y인 합만 서로 다릅니다(x+x는 제외). h(A)는 A 안의 최대 시돈 부분집합 크기입니다.
- Theorem 1.3: weak Sidon 집합 A⊂R, |A|=n에 대해 g(n) := min h(A) = ⌈(n+1)/2⌉ (모든 n≥1). Theorem 1.2: lim g(n)/n = 1/2. Sárközy–Sós(2013, Problem 12)의 물음을 완전히 해결합니다. 쉬운 말로: "거의 시돈인" 집합 안에는 항상 절반 이상을 시돈으로 뽑을 수 있고, 정확히 절반에서 끝나는 집합이 있습니다.
- (4,5)-집합: 네 원소를 어떻게 잡아도 6개의 차이의 절댓값이 최소 5종류. f(n) := min h(A) over (4,5)-집합. Theorem 1.5: lim f(n)/n이 존재하고 Erdős의 최적 상수 c*와 같으며 c* = inf_n f(n)/n. Theorem 1.6: 9/17 ≤ c* ≤ 4/7. 이전 Gyárfás–Lehel(1995): 1/2 + 1/(141·76) ≤ c* ≤ 3/5. c*는 아직 모릅니다. 이 문제는 Bloom 사이트의 Erdős Problem #757입니다(쪽 2, 대조군 아님).
- 포함 관계(Prop. 2.1, 2.2): Sidon ⊊ (4,5)-집합 ⊊ weak Sidon.

**증명의 뼈대.**
- 2절 A.P.-하이퍼그래프 H(A): 꼭짓점이 A, 변이 3항 등차수열인 3-균등 하이퍼그래프. Lemma 2.3: weak Sidon이면 "Sidon 부분집합 = 3항 등차수열을 포함하지 않는 부분집합", 따라서 h(A) = α(H(A)). Lemma 2.4: 각 변의 가운데 원소를 대응시키는 사상이 단사이므로 변의 수 m_H ≤ n_H − 2. Lemma 2.5: (4,5)-집합이면 H(A)가 선형(두 변이 한 점 이하 공유). Lemma 5.2([5]): F7을 부분하이퍼그래프로 갖지 않음. 이 세 보조정리는 Gyárfás–Lehel이 증명 없이 적은 것을 증명하면서 Lemma 2.3, 2.4는 weak Sidon 전체로 가정을 약화했다고 합니다(쪽 5).
- 3절: g와 f가 부분가법(Lemma 3.3, 3.6: 두 집합을 아주 다른 크기로 붙여 새 충돌이 없게 함, q를 비율 집합 R 밖에서 잡음)이라 Fekete 보조정리로 극한 존재.
- 4절 하한 g(n) ≥ ⌈(n+1)/2⌉: Chvátal–McDiarmid·Tuza(Theorem 4.6, 4τ ≤ n+m)와 m_H ≤ n_H − 2를 합쳐 τ ≤ n/2 − 1/2. 상한: A_{2n+1} = {X_i = 2^{n−i}3^i} ∪ {Y_i = 2^{n−i+1}3^i}를 만들어 weak Sidon임을 3진 값매김(v_3)으로 증명(Lemma 4.1, 4.2, Prop. 4.3), 등차수열이 정확히 2n−1개(Lemma 4.4), h(A_{2n+1}) = n+1(Theorem 4.5). 짝수 크기는 한 원소를 지워서.
- 5절: 상한 c* ≤ 4/7은 14점 (4,5)-집합 A_base = {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}이 h=8임을 컴퓨터 전수 확인(Lemma 5.1)하고 c* = inf f(n)/n 때문에 f(14)/14 ≤ 8/14. 하한 9/17은 Henning–Yeo의 17τ ≤ 5n + 3m(3-균등 선형 F7-free 하이퍼그래프, Theorem 5.3)에 m ≤ n − 2를 넣어 τ ≤ 8n/17.
- 핵심 새 아이디어 위치: (i) g(n)의 정확한 값은 Lemma 2.4와 Theorem 4.6의 결합(4절), 구성은 Prop 4.3과 Theorem 4.5; (ii) c*의 개선은 Theorem 1.5(극한이 inf이므로 유한 예 하나가 상계)와 Theorem 5.3.

**방법이 막히는 곳.**
- 쪽 5 (Lemma 2.5 뒤): "(4,5)" 가정을 weak Sidon으로 약화하면 선형성이 깨집니다(예 A={1,2,3,5}에서 변 {1,2,3}과 {1,3,5}가 두 점 공유). 그래서 Henning–Yeo 방식이 weak Sidon에는 안 통합니다.
- 쪽 2 각주 1: Gyárfás–Lehel의 결과는 weak Sidon 문제에 직접 도움이 안 됨("a weak Sidon set need not be a (4, 5)-set").
- 쪽 3: "any single finite (4, 5)-set A with a small enough ratio ... immediately yields an upper bound on c∗." 상계는 이제 유한 예 탐색 문제입니다.
- [추론] 하한 9/17은 m ≤ n − 2라는 weak Sidon 일반 부등식만 쓰고 (4,5)-집합에 특유한 더 강한 구조는 쓰지 않으므로 거기가 개선 여지이지만, 저자들이 그렇게 쓰지는 않았습니다. 상한은 14점 탐색에서 왔고, 12점 예가 7/12를 주었다는 점(AI 선언)으로 보아 더 큰 점수의 예가 상수를 더 낮출 수 있는지 불명.

**본문 전체에서 나온 열린 질문.**
1. c*의 정확한 값은? 현재 9/17 ≤ c* ≤ 4/7 (Theorem 1.6; Problem 1.4 = Erdős #757, 쪽 2). "Find the best constant c∗ > 0"라는 원문 질문이 해결되지 않은 상태.
2. 쪽 3: c* = inf f(n)/n이므로 더 작은 f(n)/n을 주는 유한 (4,5)-집합이 있는가(위 인용). 저자들은 14점이 최선이라고 주장하지 않습니다.
3. 본문에 번호 붙은 새 Problem은 없고, Problem 1.1(Sárközy–Sós)은 이 논문에서 해결됨.
4. 암시적 질문: weak Sidon에 대한 선형성이 깨져도 사용할 하이퍼그래프 성질이 있는지(쪽 5 설명). 본문이 질문 형태로 쓰지는 않음.

**1차 조사와 다른 점.**
- 1차 조사 서술(g(n)=⌈(n+1)/2⌉, 9/17≤c*≤4/7, Gyárfás–Lehel 1/2+1/10716≤c*≤3/5)은 모두 본문과 일치합니다.
- 1차 조사가 빠뜨린 것: 상한 c*≤4/7이 AI의 도움으로 얻은 14점 집합에서 나왔다는 선언(쪽 14, 아래 (d)), 컴퓨터 전수 확인에 의존함, 그리고 Theorem 1.5(c*=inf f(n)/n)가 상계의 핵심이라는 점. 또 "유한 판으로 체커로 채점하기 좋다"는 평가는 맞습니다: (4,5) 성질과 h(A) 모두 유한 집합에서 전수 확인 가능(Lemma 5.1의 절차).
- 1차 조사는 "문제가 풀린 부분(g)"과 "열린 부분(c*)"을 같은 줄에 두었는데, g(n)은 완전히 닫혔으므로 팩에서 g를 열린 문제로 쓰면 안 됩니다.

**팩 적합도.**
- (a) 문제 재료: c*의 구간 [9/17, 4/7] 자체(Problem 1.4); 14점 A_base와 다른 크기의 (4,5)-집합 탐색(체커 문제); Lemma 2.4/Theorem 4.6의 조합에서 어떤 하이퍼그래프 구조를 더 이용할 수 있는가; weak Sidon vs (4,5) 사이의 중간 개념.
- (b) 빼야 할 부분: g(n)=⌈(n+1)/2⌉ 부분은 이미 풀렸으므로 "결과"로만 남기고 열린 질문으로 쓰지 말 것. 대조군(#28 #30 #36 #39 #52 #66 #200 #241 #324) 관련 서술은 본문에 없습니다. 참고: #757은 대조군이 아닙니다.
- (c) 난이도와 분량: 15쪽. 하이퍼그래프의 독립수와 횡단수(transversal number), 3진 값매김만 알면 됩니다. Fekete 보조정리와 선형 하이퍼그래프의 횡단수 상계를 인용한 증명이라 읽기 쉬운 편입니다.
- (d) AI 관여 서술: 있음. "Declaration of AI usage"(쪽 14): "An AI assistant was used in the search for a construction of the set Abase", 처음 12점 예(c*≤7/12)를 만들고 여러 번 다듬어 14점(c*≤4/7)이 되었으며 전수 확인 코드 초안도 AI가 작성. 나머지 증명과 서술은 사람이 했다고 명시. 팩에 넣을 때 이 선언을 함께 보여 줄지 정해야 합니다(AI가 만든 구성이 최전선의 일부라는 점이 실험 주제와 직접 관련).

**필요한 선행 논문.**
1. A. Gyárfás, J. Lehel, "Linear sets with five distinct differences among any four elements", J. Combin. Theory Ser. B 64 (1995) ([5]) — c*의 이전 구간과 A.P.-하이퍼그래프 [arXiv 없음, 참고문헌에 번호 없음]
2. M. A. Henning, A. Yeo, "Affine Planes and Transversals in 3-Uniform Linear Hypergraphs", Graphs and Combinatorics 37 (2021) ([6]) — Theorem 5.3의 출처 (참고문헌에 arXiv 번호 없음, 존재 여부 미확인)
3. A. Sárközy, V. T. Sós, "On additive representative functions", in The Mathematics of Paul Erdős I, Springer 2013 ([11]) — Problem 12의 출처 [arXiv 없음]
4. P. Erdős, "Some old and new problems in various branches of combinatorics", Discrete Math. 165/166 (1997) ([4]) — Problem 1.4의 출처 [arXiv 없음]

---

### 2607.11351 — Wei Niu, An asymptotic Sidon basis of order 3 − η (24쪽, 읽은 범위: 전체)

**주정리.**
- Theorem 1.1: 0 < η < 0.0527인 모든 η에 대해, 모든 충분히 큰 정수 m이 m = s_1+s_2+s_3 (s_i ∈ S)이면서 min{s_1,s_2,s_3} ≤ m^{1−η}로 쓰이는 무한 시돈 집합 S ⊂ N이 존재합니다("order 3−η 점근 기저"). 쉬운 말로: Pilatte(2024)가 시돈 집합이 3개의 합으로 모든 큰 수를 만들 수 있음을 보였는데, 이 논문은 세 항 중 하나를 m보다 훨씬 작게(m^{0.947} 이하) 제한해도 된다는 것입니다.
- 본문은 S를 무작위로 만들어 확률 1로 성립함을 보입니다(5.2절). 즉 존재 증명이며 명시적 구성이 아닙니다.
- 부수 결과 Lemma 4.4: 구성된 S는 S(x) = x^{c+o(1)}이고 c = 0.3393 (밀도 지수).
- 이전 기록(쪽 2~3): Deshouillers–Plagne 차수 7, Kiss 5, Kiss–Rozgonyi–Sándor 4, Cilleruelo 3+ε, 최종 Pilatte 3(Problem 1.1, Erdős–Sárközy–Sós 1994 해결).

**증명의 뼈대.**
- 2절: Cilleruelo-Pilatte의 일반화된 진법 b(b_{2i−1}=q^{2i−1}−1, b_{2i}=p)와 Lemma 2.2: Sawin의 함수체 F_q[t] 정리(제곱근 상쇄)에서, 서로 다른 차수 d_0, d, d의 기약다항식 3개의 곱이 법 g의 잉여류에 고르게 분포한다는 형태. Lemma 2.3(Pilatte): 소수 p마다 A ⊂ [1, p/2) 가 있어 A+A+A가 연속 p+2개 정수를 담고 A ∩ (A+A+{0,1}) = ∅.
- 3절(핵심 새 아이디어, "truncated construction"): 각 기약다항식 f에 정수 n_f를 대응시켜 S = {n_f}. n_f의 자릿수는 f의 법 g_i(차수 2i−1)에 대한 이산로그 e_i(f)(i ≤ αk), 나머지 자리는 무작위(자리 r_i는 A에서, 위쪽 자리 R_i는 W={0..p−1}에서). Pilatte와의 차이: 세 항 중 하나(f_0)를 더 낮은 차수 d_0 < d의 다항식에서 뽑아 b-전개가 일찍 끝나게 하고(합의 한 항이 작아짐), 그에 맞춰 A-값 자리를 W-값 자리로 바꿉니다(쪽 8).
- 4절: 시돈성. 네 원소의 합 등식을 아래쪽 2L자리에서 읽어 f_1f_2 ≡ f_3f_4 (mod G)와 f_1 ≡ f_3 (mod H)를 얻고, 차수 비교로 세 경우(Case I–III)를 처리. Case III가 불가능한 이유가 모수 조건 (α²−c)(α⁴−c) > c(식 3.1)입니다. 이 단계에서 A∩(A+A+{0,1})=∅가 쓰입니다.
- 5절: 점근 기저성. Lemma 5.1: m을 y_i ∈ A+A+A (i ≤ ℓ*), A+A+W (ℓ* < i ≤ k*), W+W (k* < i ≤ k) 꼴로 전개. Lemma 5.2~5.3: 후보 세 쌍 C_m'을 서로 소가 되게 골라 |C_m'| = q^{βk²+O(k)}, β = c(2+α²) − α⁴. Lemma 5.4: 각 세 쌍이 m을 만들 확률 ≥ q^{−(1−α⁴)k²−O(k)}. 기댓값 q^{γk²}, γ = c(2+α²) − 1 > 0이므로 Borel–Cantelli로 확률 1.
- 모수(3.1~3.3): α² = 0.9473, c = 0.3393일 때 α⁴ = 0.89737729, c(2+α²) = 1.00001889. η < 1 − α² = 0.0527이 여기서 나옵니다.

**방법이 막히는 곳.**
- 6절 첫 문단(쪽 21): Pilatte의 Lemma 4.1처럼 c < (3−√5)/2 ≈ 0.382이어야 하고 η의 범위는 α²의 범위로 정해지며, c(2+α²) > 1 때문에 "the restriction on c forces η to be small". c의 범위를 넓히면 η도 커지지만 방법은 막혀 있습니다: Cilleruelo의 삭제 방법을 쓰면 c를 개선할 수 있을 법하나 "such a deletion may remove some triples from C_m', and it seems difficult to obtain a sufficiently precise estimate" (쪽 21).
- [추론] 직접 계산으로 확인한 점: 제약 (α²−c)(α⁴−c) > c, α⁴ > 2c, c(2+α²) > 1을 동시에 만족하는 α²의 하한은 약 0.9473이어서 본문의 0.9472873…와 일치합니다. 조건 c(2+α²)>1은 "세 항의 가능한 조합 수 ≥ m"이라는 단순 계수 조건과 같은 모양이므로, S의 밀도 지수 c가 작은 한 η를 크게 못 잡습니다.
- 쪽 22 Problem 6.2 뒤: "Unfortunately, our present construction cannot force all three summands to lie in short intervals around m/3."
- 쪽 22 마지막 문단: B_h[1] 집합의 점근 기저 차수 k(h) ≤ 2h−1을 더 줄이는 것은 "challenging" (B_h[1]의 최대 크기가 N^{1/h}이기 때문).
- 6절 Problem 6.1 뒤: "applying our truncated construction should give a result for a small range of a and b" (좁은 범위만 가능).

**본문 전체에서 나온 열린 질문.**
1. Problem 1.1(Erdős–Sárközy–Sós 1994): 시돈 집합이면서 3차 점근 기저인 무한 집합이 있는가. 이미 Pilatte가 긍정으로 해결(본문이 명시). 열린 질문이 아님.
2. Problem 1.2 (3−η, 쪽 3): "Find an admissible constant η > 0, as large as possible"; 현재 η < 0.0527 (Ping Xi의 제안). 최적화형 질문.
3. Problem 6.1 (a+b+1 판, 쪽 21, Csaba Sándor의 제안): 0≤a≤b≤1, a+b>1이면 모든 큰 m = s_1+s_2+s_3, s_1 ≪ m^a, s_2 ≪ m^b, s_3 ≍ m인 시돈 집합이 있는가. 본문은 a+b>1이 고전적 상계 S(x) ≪ x^{1/2}가 시사하는 필요조건이고, a+b>√2가 Ruzsa의 지수 √2−1에서 나오는 "더 현실적인 첫 목표"라고 적습니다(원문의 √ 기호가 추출에서 깨졌고 계수 논법으로 a+b>√2가 맞는 해석임).
4. Problem 6.2 (거의 같은 항 판, 쪽 22): 어떤 θ<1과 무한 시돈 집합에서 모든 큰 m이 |s_i − m/3| ≪ m^θ인 세 항의 합이 되는가. 더 일반적으로 허용되는 최소 θ는?
5. Problem 6.3 (쪽 22, Kiss–Sándor): B_h[1] 집합이 점근 기저가 되는 최소 차수 k(h) ≥ h를 구하라. 알려진 것: k(h) ≤ 2h (Kiss–Sándor 2025), Pilatte 언급으로 k(h) ≤ 2h−1.
6. Problem 6.4 (쪽 22, Kiss–Sándor): (h+1)차 점근 기저인 B_h[g] 집합의 최소 g(h)를 구하라.
7. 6절 첫 문단: c의 허용 범위를 넓히는 방법(삭제 방법)과 그에 따른 η 개선은 미해결(위 인용).

**1차 조사와 다른 점.**
- 열린 문제 개수: 1차 조사 표는 "열린 문제 6개"라 적었으나 본문에서 번호 붙은 문제는 Problem 1.1(이미 해결), 1.2, 6.1, 6.2, 6.3, 6.4로, 열린 것은 5개입니다. 팩 추천 문단이 "Problem 1.2, 6.1–6.4"라 쓴 것은 맞습니다.
- 1차 조사 서술의 Problem 1.2, 6.2, 6.3, 6.4 내용은 본문과 일치. 6.1의 a+b>1, 그리고 Ruzsa 지수에서 나오는 a+b>√2라는 보조 서술은 1차 조사에 없었습니다.
- 1차 조사는 "1.1절 전체를 빼면 된다"고 했습니다. 본문 전체 기준 #30/#39 서술 범위는 아래 "팩 적합도 (b)"에 정확히 정리했고, 1.1절 밖에도 Ruzsa 지수 √2−1을 쓰는 문장이 6절에 한 곳 더 있습니다.
- 1차 조사의 "이전 기록" 서술(Pilatte가 2023년)은 본문이 Compos. Math. 160 (2024)로 인용. 1차 조사는 arXiv 2303.09659를 적었고 본문 참고문헌에는 arXiv 번호가 없습니다.

**팩 적합도.**
- (a) 문제 재료: Problem 1.2, 6.1~6.4(위 열린 질문 2~6)와 6절 첫 문단의 c 개선 방향. 6.1은 두 매개변수 a,b를 바꿔 물을 수 있는 형태이고 6.2는 θ를 묻는 형태라 숫자를 바꿔 낼 수 있는 질문이 많습니다. Theorem 1.1 자체의 모수 표(식 3.1~3.3)는 체커 문제의 재료가 될 수 있습니다(주어진 c, α로 부등식 만족 여부 확인).
- (b) 빼야 할 부분(#30, #39 서술 범위를 본문 전체 기준으로 표시):
  - #30 (유한 시돈 집합 최대 크기, Erdős 추측 f(n)=n^{1/2}+O_ε(n^ε)): 1.1절 둘째 문단 전체(쪽 1 하단 ~ 쪽 2 상단). 내용은 f(n)~n^{1/2}, Erdős [Er94] 추측, 상계의 역사(Lindström, Ruzsa, Graham, Cilleruelo, Balogh–Füredi–Roy, O'Bryant), "See Erdős Problem #30".
  - #39 (무한 시돈 집합의 밀도 S(x) ≫ x^{1/2−ε}): 1.1절 셋째 문단(쪽 2). 내용은 그리디 x^{1/3}, Ajtai–Komlós–Szemerédi, Ruzsa x^{√2−1+o(1)}가 최고 기록, Cilleruelo의 구성적 증명, "major open problem [Er56]", "See Erdős Problem #39".
  - 같은 절의 이어지는 문장: Erdős의 limsup S(x)/√x ≥ 1/2, 식 (1.2) liminf 부등식, Krückeberg의 1/√2, "Erdős Problem #329"(대조군 번호는 아니지만 같은 절이므로 함께 빠집니다).
  - 1.1절 밖의 추가 흔적: (i) 쪽 2 1.2절 첫 문장 "Clearly, it follows from (1.2) that no Sidon set can be an asymptotic basis of order 2"는 (1.2)를 인용하므로 1.1절을 자르면 근거가 사라집니다(이 문장은 뺄 것). (ii) 6절 Problem 6.1 바로 뒤 문장 "And the range a+b>√2 ... Ruzsa's exponent √2−1 [Ru98]"(쪽 21)는 #39의 기록을 다시 적고 있어 삭제해야 합니다. 같은 문단의 "classical upper bound S(x) ≪ x^{1/2}"은 기본 사실이라 남겨도 되지만 Problem 6.1의 동기이므로 삭제 여부는 팩 설계자가 결정해야 합니다. (iii) Lemma 4.4(S(x)=x^{c+o(1)}, c=0.3393)와 6절 첫 문단의 c<(3−√5)/2는 이 구성의 밀도 지수일 뿐 #39의 기록이나 추측을 직접 서술하지 않아 남길 수 있지만, Ruzsa 지수와 비교할 수 있는 숫자이므로 남길지 확인이 필요합니다. (iv) 6절 마지막 문단의 "B_h[1]-set in [1,N]의 최대 크기가 N^{1/h}"는 B_h 집합의 최대 크기 배경이고 h=3이면 #241의 영역과 닿습니다(#241의 간극 정보는 아님).
  - 주의: 1.1절 첫 문장(시돈 집합의 정의)과 "For any subset A⊂N, let A(x) denote ..."(쪽 2)의 표기 정의는 이후 절에서 쓰이므로 1.1절을 자를 때 옮겨 남겨야 합니다.
  - 대조군 #28 #36 #52 #66 #200 #324 관련 서술은 본문에 없습니다.
- (c) 난이도와 분량: 24쪽. 이해하려면 함수체 위 소수 분포(Sawin), 확률적 구성, 중국인의 나머지 정리, Borel–Cantelli가 필요해 증명 전체를 읽기는 매우 어렵습니다. 그러나 문제를 낳는 부분은 1.2절(사실·역사 요약)과 6절(문제와 한계)로 집중되어 있어, 증명(3~5절)을 요약본으로 대체할 수도 있습니다.
- (d) AI 관여 서술: 없음. 감사의 글(7절)은 지도교수 Ping Xi, Péter Pál Pach, Yuchen Ding, Xiamiao Zhao, Csaba Sándor에 대한 사의와 연구비뿐입니다.

**필요한 선행 논문.**
1. C. Pilatte, "A solution to the Erdős–Sárközy–Sós problem on asymptotic Sidon bases of order 3", Compos. Math. 160 (2024) ([Pi24]) — 구성 전체의 원형, 1차 조사는 arXiv 2303.09659라고 적음(본문 참고문헌에는 번호 없음)
2. W. Sawin, "Square-root cancellation for sums of factorization functions over squarefree progressions in F_q[t]", Acta Math. 233 (2024) ([Saw24]) — Lemma 2.2의 출처(참고문헌에 arXiv 번호 없음, 존재 여부 미확인)
3. J. Cilleruelo, "Infinite Sidon sequences", Adv. Math. 255 (2014) ([Ci14]) — 기본 구성 (arXiv 번호 미확인)
4. J. Cilleruelo, "On Sidon sets and asymptotic bases", Proc. London Math. Soc. 111 (2015) ([Ci15]) — 3+ε 결과, 삭제 방법 (arXiv 번호 미확인)
5. S. Z. Kiss, C. Sándor, "On B_h[1]-sets which are asymptotic bases of order 2h", J. Number Theory 266 (2025) ([KS25]) — Problem 6.3, 6.4의 출처 (arXiv 번호 미확인)

(`[arXiv 없음]`이 확실한 것은 없고, 위 5편은 모두 참고문헌에 arXiv 번호가 없어 "미확인"입니다. 이 논문이 의존하는 Erdős–Sárközy–Sós 1994(Discrete Math. 136)와 Ruzsa 1998(J. Number Theory 68)은 전자 사전 공개가 없는 것으로 보이는 구간이지만 팩 이해에 꼭 필요하진 않아 목록에서 뺐습니다.)

---

### 2609.08706 — Shi-Qiang Chen, Quan-Hui Yang, On a problem of Erdős and Nathanson related to minimal asymptotic bases of order h (10쪽, 읽은 범위: 전체)

**주정리.**
- Theorem 1: h ≥ 3이고 0 < α < 1/h이면, 점근 밀도 d(A') = α인 차수 h의 극소 점근 기저 A'가 존재합니다. 쉬운 말로: "h개를 더해 모든 큰 수를 만들 수 있고, 그 어떤 원소도 뺄 수 없는" 집합이 자연수 중 α 비율을 차지하게 만들 수 있습니다.
- 배경(쪽 2): 극소 기저의 하밀도는 1/h 이하(Nathanson–Sárközy 1989). Erdős–Nathanson 1988은 밀도 1/h인 극소 기저, 그리고 α ∈ (0, 1/(2h−2))에 대한 존재를 보였고 h=2는 (0, 1/2] 전체. 따라서 이 논문으로 h ≥ 3의 (0, 1/h) 전체가 닫힙니다(α=1/h는 Erdős–Nathanson 1988).

**증명의 뼈대.**
- Lemma 1(쪽 3, Erdős–Nathanson 1988 Theorem 1의 인용): A = B ∪ C가 점근 기저이고 B가 매우 성긴 수열이며 C의 "서로소 표현" 수 r(n) → ∞, 그리고 조건 3, 4가 성립하면, C의 일부 C'만 남겨 B ∪ C'가 극소 기저이고 지운 부분 (C∖C')(x) ≤ 2B(x)^{h−1}가 됩니다. B(x) = O(log x)이면 지운 부분의 밀도는 0. 이 논문의 증명은 이 보조정리의 네 조건을 직접 확인하는 것입니다.
- 구성(쪽 4~5, 새 아이디어): 무리수 θ를 고정(Lemma 2, Weyl: {nθ}는 균등분포). ρ = hα. B = {b_i}, b_i = h·q_i + ε_i (ε_i∈{0,1}), b_{i+1} > (2h−1)b_i(성김), {q_iθ}가 미리 정한 유리수 구간에 들어가도록 선택(식 2.2: 각 (구간, ε)가 무한히 자주 나타남). C_0 = {hm : {mθ} < ρ}, C = C_0∖B_0, A = B∪C. 그러면 C_0(x) = αx + o(x)이고 B는 로그 크기여서 d(A) = α (식 2.3).
- 조건 2 (r(n)→∞, 쪽 5~6): 서로 겹치지 않는 블록 T_{e,k,j}를 B에서 미리 골라 {Q θ}를 구간 ((k−1)/K, k/K)에 넣어 두고, n = hL+e에 대해 n − s가 C_0에 들어가게 합니다. B가 B_h-수열이라 B_0와 겹치는 것은 많아야 하나.
- 조건 3, 4 (쪽 7~8): 구체적인 w = (h−1)b_t + c, w = b_u + (h−1)b_t, w = (h−2)b_t + b_u + c를 잡아 W에 속하고 hB에 속하지 않음(또는 속함)과 c' > δw (δ = 1/(h+1))를 확인. h ≥ 3이 쓰이는 곳: 부등식 (2.10) "h > 2", (2.13)의 중간 부등식 "h ≥ 3 is used".
- 마무리: Lemma 1로 C' ⊆ C를 얻고 d(A') = d(A) = α.

**방법이 막히는 곳.** 저자들이 방법의 한계를 적은 곳은 없습니다. 논문은 한 문제를 완결합니다. 참고로 h ≥ 3이 (2.10), (2.13)에서 쓰이므로 이 증명은 h=2에는 필요하지 않고(h=2는 이미 알려짐), 상한 1/h는 Nathanson–Sárközy의 하밀도 상한 때문에 α < 1/h 범위가 더 넓힐 수 없는 경계입니다.

**본문 전체에서 나온 열린 질문.**
1. 쪽 2의 "Erdős–Nathanson's Problem"(h ≥ 3, α∈(0,1/h)에 대한 존재)은 이 논문이 해결. 새 열린 질문은 본문 어디에도 없음(소개, 증명, 참고문헌 전체 확인).

**1차 조사와 다른 점.** 1차 조사 서술(Erdős–Nathanson 1988의 (0, 1/(2h−2)), Nathanson–Sárközy 1989 하밀도 ≤1/h, "서론에 새 열린 문제 없음")은 본문과 일치합니다. 빠진 것: 증명이 Erdős–Nathanson 1988 Theorem 1을 블랙박스로 쓰는 짧은 구성적 논문(실제 새 증명은 쪽 4~8의 약 4쪽)이라는 점, 그리고 핵심 도구가 무리수 회전의 균등분포(Weyl 1916)라는 점.

**팩 적합도.**
- (a) 문제 재료: 새 열린 질문이 없어 직접적인 재료는 없음. 변형 질문의 재료(저자 서술이 아니라 제가 보는 가능성): Lemma 1의 네 조건을 다른 방식(예: 하밀도 vs 상밀도, 표현 개수 조건)으로 바꾸는 것. 본문은 이를 제시하지 않습니다.
- (b) 빼야 할 부분: 이미 풀린 질문(Erdős–Nathanson's Problem) 자체가 이 논문의 결과이므로 "열린 질문"으로 소개되지 않도록 결과와 같이 제시해야 합니다. 대조군 #28 #30 #36 #39 #52 #66 #200 #241 #324 관련 서술은 본문에 없습니다(표현 함수 r(n)이 Lemma 1에 나오지만 이것은 서로소 표현의 개수이고 #28/#66의 1_A*1_A와 다른 대상).
- (c) 난이도와 분량: 10쪽(참고문헌 포함). 가장 짧고 읽기 쉽습니다. 극소 기저의 정의와 무리수 회전의 균등분포만 알면 구성을 따라갈 수 있습니다. 조건 확인은 부등식 계산입니다.
- (d) AI 관여 서술: 없음(연구비 각주만 있음).

**필요한 선행 논문.**
1. P. Erdős, M. B. Nathanson, "Minimal asymptotic bases with prescribed densities", Illinois J. Math. 32 (1988) ([4]) — Lemma 1과 문제의 출처, 이 논문 이해에 필수 [arXiv 없음]
2. M. B. Nathanson, A. Sárközy, "On the maximum density of minimal asymptotic bases", Proc. AMS 105 (1989) ([11]) — 하밀도 ≤ 1/h [arXiv 없음]
3. J. H. Fang, "On minimal asymptotic bases", J. Number Theory 287 (2026) ([5]) — 같은 해의 관련 결과 (참고문헌에 arXiv 번호 없음, 존재 여부 미확인)
