# 정독 결과 G조: 2512.11217, 2404.02244, 2604.25893, 2506.20813

작성 기준: 2026-11-06. 네 편 모두 `fulltext/<번호>.txt`를 처음부터 끝까지(부록·참고문헌 포함) 읽었습니다.
- 텍스트 추출에서 부등호 "≤, ≥"가 빠진 곳이 많습니다(특히 2404.02244). 식의 방향은 문맥으로 복원했고, 2604.25893의 식 하나(쪽 4)는 PDF 쪽 이미지로 직접 확인했습니다.
- 쪽수는 논문 자체 쪽 번호 기준입니다.
- 인용은 15단어 이내로 줄였고, 위치는 절/쪽으로 적었습니다.
- "기억"이라고 적은 arXiv 번호는 참고문헌에 없어 제 기억에 의존한 것이므로 확인이 필요합니다.

---

### 2512.11217 — Rushil Raghavan, Improved Bounds for the Freiman–Ruzsa Theorem (29쪽, v2 2026-02-26, 읽은 범위: 전체)

**주정리.**
- **Theorem 1.4.** G가 임의의 아벨 군, A⊆G가 유한집합이고 |A+A| ≤ K|A|이면, Question 1.2가 f(K) = O(log(3K)·log log(3K))로 성립합니다. 즉 A는 최대 exp(f(K))개의 볼록 코셋 수열(convex coset progression) 평행이동으로 덮이고, 그 수열의 차원은 ≤ f(K), 크기는 ≤ exp(f(K))|A|입니다.
  - 쉬운 말: 더해도 K배밖에 안 커지는 집합은 "부분군 + 격자점을 볼록 도형으로 자른 것"의 평행이동 exp(log K · log log K)개 정도로 덮입니다. 이전 최고(Sanders–Konyagin, Theorem 1.3)는 지수가 log^{3+o(1)}(2K)였습니다.
  - 상수 3은 K가 1에 가까워도 f가 양수이도록 넣은 것입니다(각주 2). 범위는 임의의 아벨 군이며 Z, Z^d, 비틀림 군을 모두 포함합니다.
  - 정의 2.6: d차원 볼록 수열 = 대칭 볼록체 Q⊂R^d와 준동형 φ:Z^d→G로 φ(Z^d∩Q)로 쓰이는 집합. 볼록 코셋 수열 = H+P (H는 부분군).
- **Abstract.** v2 초록은 아직 "exp(C_ε log(2K)^{1+ε})" 꼴(ε>0 임의)로 적혀 있습니다. 이것은 본문 Theorem 1.4보다 약한 서술입니다(아래 "1차 조사와 다른 점" 참고).
- **Conjecture 1.5 (다항 Freiman–Ruzsa).** f(K)=O(log 2K)이어야 한다는 추측입니다. 같은 서술이 ε=0에 해당하며, 비틀림이 유계인 군에서는 GGMT(2404.02244)가 증명했습니다.
- **Proposition 2.11.** 함수 τ[X;Y] = d[X;Y] + (η/log₂(3K))(d[X;U_A]+d[Y;U_A]) (η=1/438)의 최소화 짝 (X,Y)는 K=O(1)이거나, X가 "다항 성장 차수 d=O(log 3K), 규모 Cd⁵"를 가지며 d[X;U_A] ≤ 30 d log d입니다.
  - 다항 성장(Def 2.8): 모든 n ≤ N에 대해 H(nX) ≤ H(X)+d log n.
- **Proposition 2.13.** 위와 같은 X가 있으면 차원 O(d log d), 크기 ≤ exp(O(d log d))|A|인 볼록 코셋 수열 M이 있어 A가 K·exp(O(d log d))개의 M 평행이동으로 덮입니다.
- **Theorem 1.8 (U³ 역정리, 홀수 위수 유한 아벨 군).** ‖f‖_{U³} ≥ η이면 계수 |S| = O(log(1/η)^{1+o(1)}), 반지름 exp(−O(log(1/η)^{1+o(1)}))인 정칙 Bohr 집합과 국소 이차 함수 φ가 있어 상관이 exp(−O(log(1/η)^{1+o(1)})) 이상입니다. 증명은 부록 C에 "스케치"만 있습니다.

**증명의 뼈대.**
- §2.2 전략: 증명은 정보이론(엔트로피) 부분과 푸리에 부분으로 나뉩니다. 엔트로피 부분은 GGMT의 "Ruzsa 거리 감소" 논법에서 끝마무리(endgame)를 빼고, 합 X+Y와 섬유(fibre) X|X+Y 연산만 씁니다.
- §3 (Prop 3.1 → Prop 2.11): 최소화 짝은 모든 2≤n≤log(K)⁶에 대해 d[nX;nY] ≤ log k + (73η log k log n)/log₂(3K)를 만족합니다(log k=d[X;Y]). 어기면 τ를 더 줄이는 짝이 있어 최소성에 모순입니다. 도구는 섬유 보조정리에서 나온 Prop A.10(d[X;Y]+d[(n−1)X;(n−1)Y] ≥ d[nX;nY]+d[X|nX;Y|nY])입니다.
  - 핵심 새 아이디어는 **벌점항 η/log₂(3K)로 X를 U_A에 묶은 τ 함수**와 **n배 합 nX 전체에 대한 귀납**입니다. 벌점항 최적화는 Fredy Yip의 제안으로, 이 덕분에 v1의 logloglog 항이 사라졌습니다(감사의 글).
- §4 (푸리에, Prop 2.13): Prop 4.1은 H((n+1)X)−H(nX) ≤ 1/16을 줍니다. Prop 4.2는 KL 발산과 Pinsker 부등식으로 S⊆supp X, S−S⊆Bohr 집합, log|S| ≥ H(Z)−4d[X;Z]−2log2를 만듭니다. Prop 4.3은 L² 노름으로 큰 Bohr 집합의 크기를 억제합니다.
  - 매개변수를 ℓ≈32 d log d, ε⁻¹=O(d log d), ℓm≤Cd⁵로 잡습니다. Sanders의 Theorem B.9(Bohr 집합이 작게 자라면 볼록 코셋 수열)와 Ruzsa 덮개 보조정리로 마무리합니다.
  - Sanders가 Croot–Sisask 거의 주기로 만든 희소하고 차수 높은 집합을 이 논문은 "더 촘촘하고 차수 낮은" 확률변수로 바꾸며, 이것이 절약의 원천입니다(§2.2 끝).
- §5는 한계 논의입니다. 부록 A는 엔트로피 Ruzsa 계산, 부록 B는 푸리에·Bohr 집합과 약한 보골류보프 보조정리(Lemma B.14, B.15), 부록 C는 U³ 스케치입니다.

**방법이 막히는 곳.**
- **log d 손실.** §5 p.16: 거의 주기 논법에서는 H(ℓX)와 H(X)의 차가 O(log K)보다 큽니다. 가우시안 계산(σ₂²=O(σ₁²/d)이면 H(Z_{σ₁²})−H(Z_{σ₂²})=Ω(d log d))이 이 손실이 본질적임을 보입니다. 저자의 결론: "새 아이디어 없이는 Theorem 1.4보다 나은 경계가 나오기 어렵다"(§5 p.17). 정리의 loglog 인자는 d log d(d~log K)에서 옵니다.
- **Bogolyubov–Ruzsa 포함형이 안 나옴.** §1.1 p.3: 이 방법은 A+…+A 안의 큰 볼록 코셋 수열을 직접 증명하지 못합니다. Sanders의 Theorem 1.7(2A−2A, 차원 O(log⁶))은 개선되지 않았습니다.
- **끝마무리 장벽 1.** §5 p.17: 비틀림이 있는 군에서는 GGMT가 감소를 못 얻을 때 다른 연산으로 끝냈지만, Z^d에서는 안 됩니다. 이산 가우시안은 배가 Θ(d)로 커질 수 있고, 합·섬유 연산에 대해 닫혀 있기 때문입니다. 그래서 귀납의 "기저 사례"가 d[X₁;X₂]=O(1)이 아닐 수 있습니다.
- **장벽 2 (안정적 극값 특성화).** §5 p.17–18: 유계 비틀림에서는 d[X;Y]≤ε이면 부분군 H가 있어 d[X;U_H],d[Y;U_H] ≤ 12ε입니다(Green–Manners–Tao). 정수에서는 가우시안이 극값 후보이고 Shannon–Stam 부등식의 안정성이 필요한데, Courtade–Fathi–Pananjady가 보인 반례(무거운 꼬리 가우시안 혼합)가 방법의 한계를 보여 줍니다. 이산 안정성은 로그 오목일 때만 알려져 있습니다([7] Gavalakis–Kontoyiannis).
- **조합적 대 엔트로피적 다항 성장의 간격.** §2.2 p.8: 조합적 조건 (2)가 엔트로피 조건 Def 2.8을 함의하지만 역은 거짓입니다([11, App. B]). 그래서 Sanders의 증명을 그대로 못 쓰고 수정해야 했습니다.

**본문 전체에서 나온 열린 질문.**
1. (§1 p.2, Conj 1.5) 임의 아벨 군에서 f(K)=O(log 2K)인가. 현재는 loglog 인자가 남습니다. "natural to wonder if we can take f(K) = O(log(2K))".
2. (§1.1 p.3) 이 방법으로 A+…+A 안의 볼록 코셋 수열을 얻을 수 있는가. 저자는 "perform even more poorly at this task"라고 적었습니다.
3. (§1.1 p.3–4, Thm 1.8) U³ 역정리에서 경계 모양을 Theorem 1.4의 log·loglog와 같게 만들 수 있는가. "do not obtain a bound of exactly the same shape". 짝수 위수 군은 다루지 않았습니다.
4. (§1.1 p.4) Prendiville의 "이차 준위집합에 상대적인 U³ 역정리"와 Brauer 사각형 Ramsey 수 추정을 일반 유한 아벨 군으로 옮길 수 있는가. "interested to see if a similar result is possible for general finite abelian groups".
5. (§2.2 p.9) 이 방법이 Croot–Sisask 보조정리를 쓰는 다른 응용들의 양적 개선으로 이어지는가. "very interested to see if the methods in this paper can be used".
6. (§5 p.17, 장벽 1) Z^d에서 Ruzsa 거리 귀납의 끝마무리와 기저 사례는 무엇이며 다항 경계를 줄 만큼 효율적인가.
7. (§5 p.17, 프로그램 (1)) "진정으로 d차원"(초평면에 갇히지 않은)이고 엔트로피가 충분히 큰 Z^d 값 확률변수의 배가가 (d/2)log2−ε 이상인가. 저자는 이 부분이 "may be within reach"라고 합니다.
8. (§5 p.17–18, 프로그램 (2)) 배가가 거의 최소인 변수가 가우시안에 가까운가(Ruzsa 거리 의미). Shannon–Stam 안정성의 이산판은 어렵습니다.
9. (§5 p.18) Kac–Bernstein 정리의 안정성 추정을 이산화해 Ruzsa 거리와 연결하는 방법: "we do not see at present how to discretize".
10. (§2.2, 정의 2.10 아래) τ의 상수 1/438, 30은 "no effort to improve" 한 것입니다. 열린 질문은 아니고 최적화 여지입니다.

**1차 조사와 다른 점.**
- 1차 조사의 "남은 경계 2"(일반 유한 아벨 군 전체에 대한 효율적 결과, "일반 유한 아벨 군에서 비슷한 결과가 가능한지 보고 싶다")는 맥락이 틀렸습니다. Theorem 1.4는 이미 임의의 아벨 군에 대한 정리입니다. 그 문장은 위 질문 4(p.4)에 있고, PFR이 아니라 Prendiville의 이차 준위집합 U³ 역정리에 대한 것입니다. 이 항목은 빼거나 질문 4로 바꿔야 합니다.
- 1차 조사의 "엔트로피 Ruzsa 거리의 안정성이 PFR 증명의 마지막 장벽"은 과장입니다. 논문은 장벽을 둘(끝마무리, 안정적 극값 특성화)로 적고, 이 절을 "speculative"이며 전문가들에게는 이미 알려졌을 것이라고 밝힙니다.
- 빠진 것:
  - 초록과 본문의 불일치(위 주정리). 초록은 1+ε 꼴이고 Theorem 1.4는 log·loglog입니다.
  - 부록 C의 U³ 역정리 스케치(Theorem 1.8).
  - 본문이 GGMT와 비교해 "m³이 log log K보다 훨씬 클 때 이 경계가 더 낫다"고 적은 것(p.3). 다만 GGMT는 부분군 덮기이고 이 논문은 볼록 코셋 수열이라 같은 대상이 아닙니다.
- 1차 조사의 나머지(Theorem 1.4, Sanders–Konyagin 지수, ε=0 미해결)는 본문과 일치합니다.

**팩 적합도.**
- (a) 재료: §5 전체(장벽 1·2와 프로그램 (1)(2))가 가장 좋습니다. Example 2.7(포함형 A₁ 대 덮개형 A₂, 엔트로피 합 성장이 log n·log K 대 n·log K)은 구체적이고 검산 가능한 재료입니다. 정의 2.6, 2.8, Question 1.2도 쓸 만합니다. 부록 C의 U³ 부분은 이 논문의 질문 3·4로 이어집니다.
- (b) 뺄 곳: 대조군(#28 #30 #36 #39 #52 #66 #200 #241 #324) 관련 서술은 본문에 없습니다. 이미 풀린 질문도 없습니다. 다만 초록의 "1+ε" 문장은 본문과 어긋나므로 고치거나 빼야 합니다. 부록 B·C는 분량이 크고 보조적이라 제외 가능합니다.
- (c) 난이도와 분량: 높음. 엔트로피 계산과 푸리에·Bohr 집합이 섞입니다. 팩에는 §1, §2, §5(약 11–12쪽)와 Prop 2.11·2.13의 진술만 넣는 편이 안전합니다. §3·§4의 본문 증명은 계산이 길고 문제 재료가 적습니다.
- (d) AI 관여 서술: 없음. 감사의 글은 Fredy Yip(비공개 소통), Tao, Leng, Green을 적고 NSF 지원만 있습니다.
- **판정: 상.**

**필요한 선행 논문.**
1. [10] Gowers–Green–Manners–Tao, On a conjecture of Marton, Ann. Math. 201 (2025), arXiv 2311.05762 (번호는 GGMT 2404.02244의 참고문헌 [3]에 있음). 1차 조사에는 "2023년이라 배경만"으로 나옴.
2. [11] Green–Manners–Tao, Sumsets and entropy revisited, 2025, arXiv 2306.13403. 섬유 보조정리와 장벽 2의 기저 사례를 줍니다.
3. [26] Sanders, On the Bogolyubov–Ruzsa lemma, Anal. PDE 5 (2012). 번호는 참고문헌에 없음(기억: 1011.0107, 확인 필요).
4. [27] Sanders, The structure theory of set addition revisited, Bull. AMS 50 (2013). §9–11이 이 논문 §4의 원형이며 Theorem 2.12, B.9의 출처. arXiv 번호는 확인하지 못함. arXiv 없음일 가능성이 있어 확인 필요.
5. [30] Tao, Sumset and inverse sumset theory for Shannon entropy, CPC 19 (2010). 번호는 참고문헌에 없음(기억: 0906.4000, 확인 필요).

---

### 2404.02244 — Gowers, Green, Manners, Tao, Marton's Conjecture in abelian groups with bounded torsion (33쪽, v2 2024-05-20, 읽은 범위: 전체)

**주정리.**
- **Theorem 1.1.** G가 비틀림 m(모든 g에 mg=0, m≥2는 최소일 필요 없음)인 아벨 군이고 A가 유한 비공집합이며 |A+A| ≤ K|A|이면, A는 크기 ≤ |A|인 부분군 H의 (2K)^{O(m³)}개 코셋으로 덮입니다. 게다가 H⊆ℓA−ℓA이고 ℓ ≪ (2+m log K)^{O(m³ log m)}입니다.
  - 쉬운 말: 한 가지 진법(m진수)으로 잘리는 세계에서는 "더해도 K배 이하인 집합"이 부분군 하나의 K의 거듭제곱(다항식) 개수 평행이동으로 덮입니다. 마턴 추측의 완전한 증명입니다.
  - m=2(F₂ⁿ)은 앞선 논문 [3]에서 K의 지수 12로 증명됐고, 각주 2에 Liao가 11, 이어 9로 줄였다고 적혀 있습니다([8]).
  - G가 유한할 필요는 없습니다. A가 유한이면 A가 생성하는 군이 유한입니다.
- **Theorem 1.3 (엔트로피판).** X,Y가 G값 확률변수이면 부분군 H가 있어 d[X;U_H], d[Y;U_H] ≪ m³ d[X;Y]입니다. X,Y가 원점 포함 대칭집합 S에 값을 가지면 H⊆ℓS, ℓ ≪ (2+m d[X;Y])^{O(m³ log m)}입니다. Theorem 1.3 ⇒ Theorem 1.1은 부록 B에 전부 있습니다.
- **Corollary 1.2.** p가 홀수, f:F_pⁿ→C가 1-유계, ‖f‖_{U³} ≥ η(0<η≤1/2)이면 이차 다항식 φ가 있어 |E f(x)e_p(−φ(x))| ≫ η^{O(p³)}입니다. 증명은 부록 C(스케치)입니다.
- **Prop 2.2.** 다중거리 D[X_I] 한 번의 불평등으로 Σd[X_i;U_H] ≪ m³ D[X_I]입니다.
- **Prop 2.3 (감소).** η=c/m³일 때 D>0이면 D[X'_I] ≤ (1−η)D[X_I] − ηΣd[X_i;X'_i]인 X'_I가 있으며, 값은 m³S에 있습니다.
- **Prop 2.4 (기저).** D[X_I]<c₀이면 H가 있어 Σd[X_i;U_H] ≪ m D[X_I]이고 H⊆6S입니다.
  - 다중거리(Def 2.1): D[X_I] = H(ΣX̃_i) − (1/|I|)ΣH(X̃_i). |I|=2이면 d[X₁;−X₂]와 같습니다.

**증명의 뼈대.**
- §2: Prop 2.3을 t=⌊Cm³ log(2+k)⌋번 반복하고 Prop 2.4로 마무리합니다(k=D[X_I]). 삼각부등식으로 합산하면 Σd[X_i;U_H] ≪ m³k이 나옵니다. [3]은 최소화 짝의 컴팩트성을 썼는데, 여기서는 근사 최소화에 의한 구체적 반복이라 H의 위치(ℓS 안)를 추적할 수 있다는 점이 다릅니다(Remark 2.5).
- §3: 다중거리와 Ruzsa 거리의 관계(Lemma 3.1), Theorem 1.3의 유도, Prop 2.4의 증명(Green–Manners–Tao [4, Thm 1.3]에서 나옴).
- §4: **다중거리 연쇄 법칙**(Lemma 4.1–4.3, Corollary 4.4)입니다. [3]의 섬유 항등식의 다중 변수판이며 이 논문의 핵심 새 아이디어입니다("a key innovation").
- §5.1: Prop 5.1. 감소가 불가능하다는 가정(5.2)과 Cor 4.4가 합쳐져, m×m 배열의 행합·열합 상호정보량 I ≤ 2m(2m+1)ηk를 줍니다.
- §5.2 끝마무리: Y_{i,j}, i,j∈Z/mZ가 독립이고 Y_{i,j}가 X_i의 사본일 때 W=ΣY_{i,j}, Z₁=Σ iY_{i,j}, Z₂=Σ jY_{i,j}, Z₃=Σ(−i−j)Y_{i,j}로 두면 Z₁+Z₂+Z₃=0이 항등적으로 성립합니다. 이 항등식은 "G가 m-비틀림이어서 Z/mZ의 원소를 곱할 수 있기" 때문에 의미가 있습니다. Prop 5.3: W를 조건으로 Z₁,Z₂,Z₃는 두 개씩 거의 독립입니다. 엔트로피 BSG(Lemma 5.5)로 배가가 작은 U를 얻어 (5.3)에 넣으면 m³ηk+η(m² log₂m)k ≫ k가 되어 k=0이 아니면 모순입니다.
- 부록 A: 엔트로피 Ruzsa 계산. Lemma A.3은 Bukh의 "dilate 합" 추정의 엔트로피판으로 H[X−aY]−H[X] ≪ (1+log|a|)d[X;Y]입니다. 부록 B: 엔트로피 PFR → 조합 PFR(Ruzsa 덮개 보조정리). 부록 C: U³.

**방법이 막히는 곳.**
- **다항 Bogolyubov를 못 얻음.** §1 p.2: H⊆2A−2A이면서 |H| ≥ K^{−O_m(1)}|A|인 부분군이 있다는 "다항 Bogolyubov 추측"을 "m=2에서도" 얻지 못했습니다. 이 방법이 주는 것은 H⊆ℓA−ℓA에서 ℓ이 K의 polylog 크기라는 약한 형태입니다.
- **m 의존.** 지수 O(m³)과 ℓ의 O(m³ log m)은 "additional effort로 개선될 수 있을 것"이라 합니다(§1 p.2). m이 커질수록 η=c/m³이 작아져 반복 횟수 s≈Cm³ log(2+k)가 늘어나는 것이 원인입니다.
- **비틀림 가정 의존.** §5.2의 항등식 Z₁+Z₂+Z₃=0은 Z/mZ 계수 곱셈이 정의되는 군에서만 쓸 수 있습니다. 이 논문은 비틀림 없는 군을 다루지 않고 정수에서의 한계는 논의하지 않습니다(그 논의는 Raghavan §5에 있음).
- Sanders의 결과(H⊆2A−2A, 크기 exp(−C_m log⁴(2K))|A|)와 Konyagin의 log^{3+ε} 결과 사이에는 포함 관계 H⊆2A−2A 대 지수 개선이라는 맞바꿈이 있었는데, 이 논문은 그 맞바꿈을 완전히 없애지 못했습니다(§1 p.2).
- 부록 C 각주 5 p.32: Green–Tao [5, Cor 3.2]는 일반적으로는 거짓입니다(Candela–González-Sánchez–Szegedy). 보충 부분군일 때만 성립하고 F_pⁿ에서는 모든 부분군이 보충이라 무해합니다.

**본문 전체에서 나온 열린 질문.**
1. (§1 p.2) 다항 Bogolyubov 추측: H⊆2A−2A이고 |H| ≥ K^{−O_m(1)}|A|인 부분군이 있는가. "We have been unable to achieve this even in the m = 2 case."
2. (§1 p.2) 지수 (2K)^{O(m³)}과 ℓ의 m 의존을 줄일 수 있는가. "can probably be improved with additional effort".
3. (§1 p.2, 각주 2) m=2에서는 12→11→9로 줄었지만, 일반 m에서 명시적인 최적 상수는 알려지지 않았습니다(본문이 질문으로 적은 것은 아니고 읽으면 드러나는 간격).
4. (부록 A, Lemma A.3 앞 p.4) 거친 부등식 4|a|와 정교한 (1+log|a|) 부등식이 같은 지수를 주므로 로그판은 "of some independent interest"라고 합니다. 질문은 아니고 향후 응용 가능성을 말한 것입니다.

**1차 조사와 다른 점.**
- 1차 조사 "남은 경계 3"(m 의존이 사라져야 정수판으로 간다)은 GGMT 본문에 없는 해석입니다. 본문은 "m 의존은 개선될 수 있을 것"이라고만 적고 정수나 비틀림 없는 군은 다루지 않습니다.
- 빠진 것:
  - 정리의 "Moreover" 부분(H⊆ℓA−ℓA, ℓ ≪ (2+m log K)^{O(m³ log m)}).
  - **다항 Bogolyubov 추측이 m=2에서도 안 풀렸다**는 명시적 미해결 문장(질문 1).
  - Corollary 1.2(홀수 표수 U³ 역정리, η^{O(p³)}).
  - 일반 m에 대해 Liao의 개선이 없다는 점(개선은 F₂ⁿ에서만).
- 1차 조사의 "(2K)^{O(m³)}개 평행이동, 크기 ≤ |A|인 부분군"은 정확합니다. 「AFST 2026 게재」는 이 판(v2)의 본문에 서지 정보가 없어 확인할 수 없습니다.

**팩 적합도.**
- (a) 재료: 정리와 §1의 배경 단락(Sanders, Konyagin와의 비교). 질문 1·2, §5.2 끝마무리(항등식 Z₁+Z₂+Z₃=0과 비틀림의 역할)는 "왜 정수에서 안 되는가"를 모델이 스스로 추론하게 할 수 있는 좋은 재료입니다. 다중거리 정의(Def 2.1), Lemma 3.1, 연쇄 법칙(Lemma 4.1)은 검산 가능한 정리입니다.
- (b) 뺄 곳: 대조군 관련 서술 없음. 이미 풀린 질문 없음. 각주 2의 Liao 개선은 풀린 부분이므로 단순 배경으로만 남기면 됩니다.
- (c) 난이도와 분량: 높음(엔트로피 계산). 33쪽 중 팩에는 §1–§2, §5.2의 항등식 부분, 부록 A의 정리 진술(약 10쪽)이 적당합니다. §4–§5.1의 긴 계산은 문제를 낳기보다 길을 막습니다.
- (d) AI 관여 서술: 없음. 감사의 글은 Zach Hunter의 의견·정정만 적습니다.
- **판정: 단독으로는 중(명시적 열린 질문이 2개뿐), Raghavan과 한 쌍이면 상.** 한 쌍이면 "비틀림 유계에서는 해결, 정수는 미해결"의 경계가 선명해집니다.

**필요한 선행 논문.**
1. [3] Gowers–Green–Manners–Tao, On a conjecture of Marton, arXiv 2311.05762. 이 논문의 F₂ 원형이고 "섬유 항등식"을 줍니다.
2. [4] Green–Manners–Tao, Sumsets and entropy revisited, arXiv 2306.13403. Prop 2.4의 근거 [4, Thm 1.3].
3. [19] Tao, Sumset and inverse sumset theory for Shannon entropy, CPC 19 (2010). 엔트로피 BSG의 출처. 번호는 참고문헌에 없음(기억: 0906.4000, 확인 필요).
4. [17] Sanders, On the Bogolyubov–Ruzsa lemma, Anal. PDE 5 (2012). 이전 최고의 경계. 번호 확인 필요(기억: 1011.0107).
5. [5] Green–Tao, An inverse theorem for the Gowers U³(G)-norm, Proc. Edinb. Math. Soc. 51 (2008). 부록 C가 이것을 수정합니다. 번호는 참고문헌에 없어 확인 필요.

---

### 2604.25893 — Yifan Jing, Akshat Mudgal, A structure theorem for sets with doubling 4+δ (30쪽, v1 2026-04-28, 읽은 범위: 전체)

**주정리.**
- **Theorem 1.2.** ε', δ>0이고 δ가 ε'에 비해 충분히 작다고 하자. A⊂Z가 유한 비공집합이고 |A+A| ≤ (4+δ)|A|이면 다음 중 하나가 성립합니다. (1) 1차원 등차수열 P⊆Z가 있어 |P| ≫_δ |A|이고 |A∩P|/|P| ≥ 1/2−ε'. (2) 진짜(proper) 2차원 등차수열 Q⊆Z가 있어 |Q| ≫_δ |A|이고 |A∩Q|/|Q| ≥ 1−ε'. A+A를 A−A로 바꿔도 같은 결론입니다.
  - 쉬운 말: 배가가 4를 조금 넘어도 집합은 (1) 밀도 약 1/2로 한 줄에 놓이거나 (2) 가득 찬 2차원 격자 블록에 놓입니다. 두 모양은 각각 극단 예 (1.3), (1.4)에 해당하므로 ε'에 대한 의존을 빼면 최적입니다(p.3).
  - 범위: 정수 집합입니다. 실수 유한집합도 Freiman 20-동형 때문에 같은 결론이 성립합니다(p.3).
  - 이 논문은 |P|≫_δ|A|의 상수가 "산술 정칙성 보조정리"에서 오므로 비효과적이며 δ와 ε'의 정량적 관계를 적지 않았습니다.
- **Corollary 1.3 ("거의 모든 합" 판).** Γ⊆A×A, |Γ| ≥ (1−δ')|A|², |A+_Γ A| ≤ (4+δ)|A|이면 (1) 또는 (2). Shao의 거의 모든 BSG와 Theorem 1.2를 결합해 얻습니다.
- **Corollary 1.4 (Bogolyubov–Ruzsa형).** |A+A| ≤ (4+δ)|A|이면 41A−40A가 차원 d≤2, |P|≫_δ|A|인 진행을 포함합니다. 차원 상한이 최적이라는 점이 장점이고 대가는 2A−2A 대신 41A−40A를 쓰는 것입니다(p.4).
- Lemma 2.3(EGM): P가 1차원 진행, |P|≥12, X⊆P, |X|/|P|>1/2이면 P⊆5X−4X. Lemma 2.4: P가 X를 포함하는 가장 작은 진행이고 |X|≥100, |X|/|P|>2/5이면 P⊆9X−8X. Lemma 2.5: 진짜 2차원 Q, X⊆Q, |X|≥(1−c)|Q|, c<1/10이면 Q⊆41X−40X.
- 반례 (p.4): A₁={0,10N,2^N}+[N]은 |A₁+A₁|=6(2N−1) ≤ 4|A₁|−6인데 |Q|≪|A₁|인 2차원 진행에 들어가지 않습니다. 곧 A 전체가 구조에 들어갈 수는 없고 밀도 높은 부분만 잡힙니다.

**증명의 뼈대.**
- §2 (조밀 모형으로의 환원): Green–Ruzsa 직선화(Lemma 2.6)로 A를 [N]의 부분집합(Freiman 동형)으로 옮깁니다. Lemma 2.3–2.5(Lev의 Lemma 2.2에 기반한 초등적 보골류보프 보조정리)로 구조를 원래 집합으로 되돌립니다. Theorem 2.1이 조밀판입니다. 보골류보프형 보조정리 2.4, 2.5는 증명이 짧고 초등적입니다.
- §3: Eberhard–Green–Manners §4를 따라 산술 정칙성 보조정리로 1_A = f_struct+f_sml+f_unf로 분해하고, Z/qZ×[0,1]×T^d 위의 문제로 옮깁니다(Lemma 3.1–3.3, (3.9)).
- §4: 섬유 A_{a,i}의 크기를 작은 것·중간 것·큰 것으로 나누기 위해 매개변수 ε'>δ>ε를 새로 도입합니다(**새 아이디어 1**). Tao의 T^d에서의 Kneser 부등식(Lemma 4.1)과 역 Kneser 정리(Lemma 4.2)로 세 경우, 곧 1차원 구조 경우, 2차원 구조 경우, 확장 경우로 나눕니다.
- §5 (확장 경우): 최대 섬유에 큰 섬유를 하나씩 더해 대부분의 섬유 합에서 배가 2를, 양의 비율의 섬유 합에서 2+δ를 얻습니다. 평면 Brunn–Minkowski(Lemma 5.1, EGM Lemma 4.9)와 결합해 |A+A| ≥ (4+δ/5)|A|. Remark 5.2: 모든 손실을 o(δ)로 눌러야 하고 양의 비율의 섬유에서 이득을 얻어야 합니다(**새 아이디어 2**).
- §6–§8 (2차원 구조 경우): §6은 준동형 φ(x)=a·x의 정수 벡터 a가 유계(Prop 6.1)임을 볼록기하로 보입니다(Lemma 6.2: 경계 측도 Γ(a)=2‖a‖₂). §7은 Lipschitz 근사(Lemma 7.2)와 U² 직교성(Lemma 7.3)으로 A가 비동차 Bohr 집합 B에서 밀도 1−O(ε')을 가짐을 보입니다. §8은 Bohr 집합 안에 진짜 ≤2차원 진행이 있음을 보입니다(Lemma 8.1–8.2). θ가 무리수이면 연분수, 유리수이면 Minkowski 제2정리(기하 수론). 이 부분이 **새 아이디어 3**(§6의 ‖a‖ 제어와 §8 유리수 경우)입니다.

**방법이 막히는 곳.**
- **작은 δ에 한정.** §1 p.2–3: K<4에서는 EGM, 이 논문은 K=4+δ(δ가 매우 작음)입니다. 증명은 "Brunn–Minkowski–Kneser 하한에 δ만큼 이긴다"는 데서 오기 때문에 손실을 o(δ)로 눌러야 합니다(증명 개요 p.6, Remark 5.2). 이것이 일반 K로 못 가는 직접 이유입니다.
- **일반 K는 PFR에서도 안 나옴.** §1 p.4: 임의의 K에 대한 Question 1.1이 "정수에서 다항 Freiman–Ruzsa 추측을 가정해도 따라 나오지 않는 것 같다"고 적습니다.
- **A 전체를 담을 수 없음.** p.4의 반례 A₁. 연속 설정(Figalli–Jerison)에서는 A 전체가 효율적으로 덮이지만 이산에서는 아닙니다.
- **연속과의 차이.** p.4: 연속의 역 Brunn–Minkowski의 직접 유사판은 Z에서 자주 실패합니다. 예: A⊂Z^d에서 σ₋[A] ≤ 2d−2+1/(d−1)(Ruzsa의 문제, 최근에야 최적임이 해결, [2,18]).
- **비효과적 상수.** 산술 정칙성 보조정리의 증가 함수 F(M)과 M ≪_{ε,F} 1 때문에 |P|≫_δ|A|와 δ,ε'의 관계가 명시되지 않습니다. 논문은 이를 문제로 적지 않았습니다.
- **Lemma 2.3, 2.4의 밀도 한계.** p.8: 밀도 > 1/2 조건은 날카롭습니다(P=[2l], X=2·[l]이면 mX−nX는 1을 못 담음). 더 작은 밀도 2/5까지는 "가장 작은 진행" 조건이 있어야 합니다.
- **유리수 θ.** §8 p.26: (cF(M),N)-무리성이 θ∉Q를 함의하지 않아 연분수가 곧바로 안 통하고 기하 수론으로 따로 처리합니다.

**본문 전체에서 나온 열린 질문.**
1. (§1 p.1, Question 1.1 = Green의 100 open problems 중 Problem 30) K≥2, |A−A|≤K|A|일 때 구조적 부분집합 A'⊆A가 "명백히" |A'−A'| ≤ (K+ε)|A'|를 만족하도록 항상 찾을 수 있는가. K=4+δ만 답했습니다.
2. (§1 p.4) 임의의 K>1에서의 Question 1.1은 PFR over Z를 가정해도 따라 나오지 않는 것 같다: "does not seem to follow even conditionally".
3. (§1 p.2) 배가 <10/3에 대한 Freiman의 오래된 추측("an old conjecture of Freiman"). Jin이 큰 집합·3+ε까지만 확인했습니다.
4. (§1 p.3) 결론 (1.2)가 "ε'에 대한 의존을 빼면" 최적이라는 문장이 남깁니다: δ와 ε' 사이의 최적 정량적 의존과 비효과적 |P|≫_δ|A|를 효과적으로 만들 수 있는가(본문이 질문으로 적지는 않은 암묵적 질문).
5. (§1 p.4, Cor 1.4) 41A−40A를 2A−2A로 줄일 수 있는가, 아니면 41, 40이 필요한가(본문은 차원 상한이 최적이라 하고 포함 지수는 논하지 않음. 암묵적).
6. (§1 p.4) 역 Brunn–Minkowski의 이산판이 Z에서 어디까지 가능한가("much harder to prove in Z"). 명시적 질문은 아니고 비교 서술입니다.

**1차 조사와 다른 점.**
- 1차 조사의 "남은 경계 2"(연속에서는 집합 전체가 구조 안에 들어가는데 이산에서도 가능한가)는 틀렸습니다. 논문은 p.4에서 그것이 **불가능하다**고 반례 A₁로 보였습니다("not possible to have the entirety of A contained"). 이 항목은 삭제해야 합니다.
- 빠진 것:
  - 정리가 A−A와 실수 집합에도 성립한다는 점.
  - Corollary 1.3(거의 모든 합 판).
  - 상수 |P|≫_δ|A|의 비효과성.
  - Lemma 2.3–2.5(초등적 보골류보프형 보조정리)의 존재.
  - p.4의 반례 A₁ 자체와 비교 대상 Ruzsa의 σ₋ ≤ 2d−2+1/(d−1).
- 1차 조사의 "Theorem 1.2, 41A−40A, Question 1.1 확인"은 맞습니다.
- 본문 오탈자 하나: §4 p.16 "(a₀,i₀) ∈ E be such that α(a₀,i₀) is maximal"에서 E가 아니라 E의 여집합이어야 맞습니다(뒤에서 α가 크다는 것을 쓰므로). 팩에 넣을 때 혼동 소지가 있습니다.

**팩 적합도.**
- (a) 재료: 정리 1.2와 두 극단 예 (1.3)(1.4), 반례 A₁, Question 1.1, Corollary 1.4. 특히 §2의 Lemma 2.2–2.5는 짧고 초등적이며 "41, 40, 1/2, 2/5가 최적인가"라는 검산 가능한 문제를 낳기 좋습니다. 작은 N에서 컴퓨터로 확인할 수 있는 유한판(예: 특정 X에 대해 mX−nX가 P를 덮는 최소 m,n)을 만들 수 있습니다.
- (b) 뺄 곳: 대조군 관련 서술은 없습니다. 서론이 Erdős sum-free 정리를 EGM의 응용으로 언급하지만 대조군 문제 번호와 직접 겹치지 않습니다. 이미 풀린 질문 없음. 본문 오탈자(위)는 고쳐서 넣을 것.
- (c) 난이도와 분량: §1–§2(약 10쪽)는 읽기 쉽고 §3–§8은 산술 정칙성 보조정리와 Kneser 이론으로 무겁습니다. 팩에는 §1, §2, §5 요약, Remark 5.2와 증명 개요(p.4–7)만 넣는 편이 좋습니다.
- (d) AI 관여 서술: 없음. 감사의 글은 연구비만 적습니다.
- **판정: 상.**

**필요한 선행 논문.**
1. [4] Eberhard–Green–Manners, Sets of integers with no large sum-free subset, Ann. Math. 180 (2014). Theorem 6.4, §4, Lemma 6.3, Lemma 4.9, 부록 A의 출처. 참고문헌에 번호 없음(기억: 1301.4579, 확인 필요).
2. [9] Green, 100 open problems (Problem 30 = Question 1.1). **[arXiv 없음]** (저자 웹 문서).
3. [28] Tao, An inverse theorem for an inequality of Kneser, Proc. Steklov Inst. Math. 303 (2018). Lemma 4.1, 4.2의 출처. 참고문헌에 번호 없음, 확인 필요.
4. [3] Eberhard, The abelian arithmetic regularity lemma, arXiv 1606.09303 (참고문헌에 번호 있음).
5. [10] Green–Ruzsa, Sets with small sumset and rectification, Bull. LMS 38 (2006). Lemma 2.6의 출처. 번호는 참고문헌에 없음, 확인 필요.
   - 참고: §8의 [27] Tao의 블로그 글 "Continued fractions, Bohr sets, and the Littlewood conjecture"은 **[arXiv 없음]** (웹 문서)이나 Lemma 8.2를 이해하는 데 꼭 필요하지는 않아 위 5편에서는 뺐습니다.

---

### 2506.20813 — Rupert Li, Lampros Gavalakis, Ioannis Kontoyiannis, Entropic additive energy and entropy inequalities for sums and products (27쪽, v2 2025-11-19, 읽은 범위: 전체)

**주정리.** 기호: h는 미분 엔트로피(자연로그), H는 이산 엔트로피, a(X,Y)=연속 변수의 엔트로피 가법 에너지입니다.
- **Lemma 3.1.** a(X,Y) = 2h(X,Y)−h(X+Y). Lemma 3.2: h(X+Y)+a(X,Y) = 2h(X,Y) ≤ 2h(X)+2h(Y)이고 여유분은 정확히 2I(X;Y)이므로, X,Y가 독립이면 등호입니다.
  - 쉬운 말: "에너지가 크다 ⇔ 합의 엔트로피가 작다"를 한 줄 항등식으로 만든 것입니다. 조합적 부등식 E(A,B) ≥ |A|²|B|²/|A+B|의 엔트로피판입니다.
- **Corollary 3.3–3.7.** a ≥ (3/2)h(X)+(3/2)h(Y)−log C ⇔ h(X+Y) ≤ ½h(X)+½h(Y)+log C−2I(X;Y). 또한 이는 h(X)와 h(Y)가 가깝다는 것과 동치입니다(Cor 3.5).
- **Theorem 4.3 (미분 엔트로피 BSG).** a(X,Y) ≥ (3/2)h(X)+(3/2)h(Y)−log C이면, X+Y를 조건으로 하는 조건부 독립 사본 (X₁,Y₁),(X₂,Y₂)에 대해 h(X₁|X+Y) ≥ h(X)−2log C, h(Y₂|X+Y) ≥ h(Y)−2log C이고 X₁,Y₂는 조건부 독립이며 h(X₁+Y₂|X+Y) ≤ ½h(X)+½h(Y)+log C입니다.
  - Tao·Kontoyiannis–Madiman 판과 비교하면 오차가 (36)(37)에서는 더 나쁘고 (38)에서는 더 좋습니다(p.13).
- **Lemma 5.1 (이산).** s(X)=H(X+X')−H(X)에 대해 s(X) ≤ H(X)−(log 2)(1−ΣP(a)²)이고, 등호는 서포트가 Sidon 집합일 때만 성립합니다.
- **Prop 5.2 (안정성).** s(X) ≥ H(X)−(log 2)(1−ΣP²)−C이면 Sidon 집합 B⊂A가 있어 P(X∈B) ≥ 1−C/(p*·log 2) (p*=최소 확률, 서포트가 유한). Prop 5.5: s(X) ≥ H(X)−ε이면 max P ≥ 1−ε/log 2.
- **Theorem 6.5.** 곱셈 엔트로피(R^×에서의 Haar 측도 기준)의 square-quotient 부등식 ½ ≤ σ̃(X)/δ̃(X) ≤ 2. **Theorem 6.6**: 곱셈 Plünnecke–Ruzsa.
- **Theorem 7.2 (ring Plünnecke–Ruzsa).** X,Y,Z,W가 i.i.d. 연속, log|X| 적분가능이면 h(XY−ZW) ≤ 5h(XY)+2h(X+Y)−6h(X)−4E[log|X|]. Theorem 7.6(일반 m×n)과 7.7(이산, 정역(integral domain) 값, X≠0 a.s.).
- **Theorem 7.8 (기울기 부등식).** h((X±Y)/(Z±W))+5h(X) ≤ 4h(XY)+2h(X±Y). 이산 판 [18, Thm 4.7]의 "부분 유사판"(p.23).
- **§8 (Z 값 엔트로피 합-곱).** Example 8.1: P(X=0)=1/3, 나머지는 {1..n}에서 균등이면 max{H(X+X'),H(XX')} ≤ (4/3+o(1))H(X)이므로 Goh의 추측 (59)가 성립한다면 ε≤1/3이어야 합니다. Example 8.2: |A+A|≥|A|^{2−ε}이어도 H(U_A+U_A') < (1+ε−o(1))H(U_A)일 수 있습니다.

**증명의 뼈대.**
- §2: 배경(엔트로피-크기 대응, Ruzsa 거리, 가법 에너지, Goh의 이산 에너지 A(X,Y)=2H(X,Y)−H(X+Y)).
- §3: Lemma 3.2가 조합 부등식 (11)의 엔트로피 유사판이고, 여기서 Goh의 이산 결과를 연속 변수로 확장합니다. **새 아이디어**: 이산 증명이 쓰던 "함수적 부분모듈성"이 미분 엔트로피에서는 거짓이므로 **정보 처리 부등식**(데이터 프로세싱)으로 바꿉니다(§1.2, §3, Lemma 4.2, Prop 7.1, Lemma 7.3 모두).
- §4: Lemma 4.2(max{h(X₁−X₂),h(X₁−Y₂)} ≤ 2h(X)+2h(Y)−a)에서 Theorem 4.3이 나옵니다(기본 항이 이산에서도 그대로 통함).
- §5: Lemma 5.1은 R(a,b)=log(Σ_c P(c)P(a+b−c)/(P(a)P(b)))−(log 2)1_{a≠b} ≥ 0의 평균으로 쓰고, Prop 5.2는 마르코프 부등식과 "나쁜 쌍에서 확률이 작은 원소 제거"로 Sidon 집합을 만듭니다.
- §6: 연속 변수를 군 R^×의 값으로 보고 [16]의 군 일반화로 합 부등식들을 곱 부등식으로 옮깁니다.
- §7: Prop 7.1(h(X(Y+Z))+h(X,Y,Z) ≤ h(X,Y+Z)+h(XY,XZ)−E log|X|)과 Lemma 7.3을 Theorem 7.2에 넣고, Prop 7.4에서 귀납으로 n개 곱의 합으로 확장해 Theorem 7.6을 얻습니다.
- §8: 두 개의 구체 예(위).

**방법이 막히는 곳.**
- **유한 서포트가 필요.** §5 p.15–16: Prop 5.2의 오차 C/(p*·log 2)는 최소 확률 p*에 의존하며, Example 5.3, 5.4는 이 의존을 피할 수 없음을 보입니다. Example 5.4: 4N원소 집합에 대해 C=log2/(4N)→0인데 P(X∈B)≤3/4. 그래서 안정성 함수 f가 존재하는지를 열린 문제로 적었습니다.
- **BSG의 오차 맞바꿈.** §4 p.13: Theorem 4.3은 조건부 엔트로피 (36)(37)은 Tao 판보다 나쁘고 (38)은 더 좋습니다. 둘을 동시에 개선할 수 있는지는 적혀 있지 않습니다.
- **엔트로피 합-곱의 상수.** §8 p.24: 조합 합-곱에서 Bloom의 ε=1/3+2/951이 지금까지의 최고인 반면 엔트로피에서는 그 유사판이 **거짓**입니다(ε≤1/3). 곧 Erdős–Szemerédi식 정리가 엔트로피에서 성립한다 해도 조합 정리보다 훨씬 좁은 범위입니다. "any other value gives a constant larger than 4/3": 이 예의 방법으로는 4/3을 넘어 낮출 수 없습니다.
- **조합→엔트로피 이식 불가.** Example 8.2: |A+A|≥|A|^{2−ε}만으로는 엔트로피 합이 커지지 않습니다.
- Theorem 7.8은 이산판 [18, Thm 4.7]의 "partial analog"일 뿐입니다(p.23).

**본문 전체에서 나온 열린 질문.**
1. (§5 p.16, "Open problem") H(X) ≤ D이고 조건 (42)를 상수 C로 만족하는 이산 변수에 대해, C→0일 때 0으로 가는 함수 f(C,D)가 있어 P(X∈B) ≥ 1−f(C,D)인 Sidon 집합 B⊂A가 항상 있는가. "It would be interesting to determine whether there exists a function f(C, D)".
2. (§8 p.24) Z 값 i.i.d. X,X'에 대해 max{H(X+X'),H(XX')} ≥ (1+ε−o(1))H(X)가 어떤 ε>0에서 성립하는가(Goh의 추측 (59)). 저자는 성립한다면 ε≤1/3임만 보였습니다. **→ 1차 조사에 따르면 2607.29042가 8/7로 이미 답함.**
3. (§8 p.24) H(X)→∞에서 max ≥ (2−o(1))H(X)가 성립하는가: "it might be tempting to conjecture". Example 8.1로 거짓입니다(상한 4/3).
4. (§8 p.25) |A+A|≥|A|^{1+ε}이면 H(U_A+U_A') ≥ (1+ε'−o(1))H(U_A)인 ε,ε'∈(0,1)이 있는가. "one may wonder". Example 8.2는 가장 약한 형태(|A+A|≥|A|^{2−ε})를 반증할 뿐 작은 ε 전체는 닫지 않습니다.
5. (§7.2 p.23) Theorem 7.8은 이산판의 부분 유사판입니다. 완전한 연속 유사판(암묵적, 본문이 질문으로 적지 않음).
6. (§1 p.1–2) 다른 개선 가능성: 엔트로피 Plünnecke–Ruzsa(Tao)가 "절대 상수를 잃는다"는 점. 이 논문의 (23)은 Y_i별 상수 K_i로 정확합니다(p.6). 질문은 아닙니다.

**1차 조사와 다른 점.**
- 1차 조사는 열린 문제를 "2개"(§8의 정수 합-곱, §5의 f(C,D))라고 했는데, 본문에서 "Open problem"이라는 이름이 붙은 것은 §5의 하나뿐입니다. §8은 Goh의 추측과 한계를 보이는 예로 구성되며 긍정적 결과는 없습니다("We do not present any positive results").
- 빠진 것:
  - Prop 5.2의 p* 의존과 Examples 5.3–5.4(그래서 f(C,D) 질문이 생김).
  - Theorem 7.8(기울기 부등식)과 §6의 곱셈 엔트로피(Haar 측도, 스케일 불변).
  - §8의 서술이 일부 낡았다는 점: "널리 추측되는 ε≤1"과 "Bloom의 ε=1/3+2/951이 최고"는 1차 조사가 적은 대로 2605.28781(실수에서 합-곱 반증)과 Cushman 개선(2512.13849) 이전의 서술입니다.
- "IEEE Trans. Inform. Theory 72(3) 게재"는 확보한 판(arXiv v2, 2025-11-19)에 서지 정보가 없어 확인할 수 없습니다.
- 나머지(Theorem 4.3, 환 Plünnecke–Ruzsa, 연속 에너지 동치, Sidon 근방)는 본문과 일치합니다.

**팩 적합도.**
- (a) 재료: §3–§5가 가장 좋습니다. 항등식이 짧고 증명이 검산 가능하며, Lemma 5.1(Sidon 서포트에서의 등호)은 정확한 식이라 모델이 변형 문제를 낼 수 있습니다. §5의 열린 문제(f(C,D))와 Examples 5.3, 5.4가 "왜 p*가 필요한가"를 알려 줍니다. §4의 BSG 오차 맞바꿈도 재료입니다. §6–§7은 곱셈 엔트로피 식이 많아 분량이 큽니다.
- (b) 뺄 곳: **§8 전체**(대조군 #52 인접, 이미 풀린 질문). 초록 마지막 두 문장, §1.3 "On the entropic Erdős–Szemerédi sum-product phenomenon" 단락, §2의 Goh 추측 언급, 참고문헌 [2],[3]도 함께 정리할 것. §7은 합-곱 부등식이지만 "합과 곱의 엔트로피를 동시에 작게 못 한다"는 형태가 아니라 환 Plünnecke–Ruzsa 상한이므로 대조군 #52와 직접 겹치지는 않지만 인접하므로 연구자가 판단하십시오. §5의 Sidon 집합은 대조군 #30·#39(Sidon 집합의 최대 크기·밀도)와 대상은 같지만 질문이 다릅니다(여기서는 엔트로피 안정성). 그래도 "Sidon" 키워드가 겹치므로 팩 구성 시 한 번 확인하길 권합니다.
- (c) 난이도와 분량: 중간. 정의가 많지만 대부분 Shannon형 항등식과 부등식 사슬이라 모델이 따라가기 쉽습니다. 27쪽 중 §8을 빼고 §1–§5(약 16쪽)와 §7의 진술만 넣으면 적당합니다.
- (d) AI 관여 서술: 없음. 감사의 글이 없고 각주에 소속과 연구비만 있습니다.
- **판정: 중.** 명시적 열린 질문이 §5 하나뿐이고(§8을 빼면) 나머지는 증명된 부등식이라 모델이 문제를 스스로 지어내야 합니다. 대신 재료의 정확성과 검산성은 높습니다.

**필요한 선행 논문.**
1. [5] Goh, On an entropic analogue of additive energy, arXiv 2406.18798. 이미 1차 조사 후보에 있음. 이 논문의 이산 모태이며 Theorem 6(Goh의 BSG)과 Prop 3, 7, 8, 10을 연속으로 옮긴 것입니다.
2. [25] Tao, Sumset and inverse sumset theory for Shannon entropy, CPC 19 (2010). 엔트로피 Ruzsa 거리와 BSG의 출처. 번호는 참고문헌에 없음(기억: 0906.4000, 확인 필요).
3. [12] Kontoyiannis–Madiman, Sumset and inverse sumset inequalities for differential entropy and mutual information, IEEE TIT 60(8) (2014). 연속판 기초. 번호는 참고문헌에 없어 확인 필요.
4. [16] Madiman–Kontoyiannis, Entropy bounds on abelian groups and the Ruzsa divergence, IEEE TIT 64(1) (2018). §6의 군 일반화 출처. 번호는 참고문헌에 없어 확인 필요.
5. [18] Máthé–O'Regan, Discretised sum-product theorems by Shannon-type inequalities, arXiv 2306.02943. §7이 이 논문의 연속판입니다.
   - 참고: Gowers–Green–Manners–Tao [7][8]와 Bloom [2](arXiv 2501.09470)은 배경입니다.

---

## 요약 표 (한 줄 판정)

| 논문 | 판정 | 이유 |
|---|---|---|
| 2512.11217 | 상 | 정수 포함 일반 군의 현재 최고. §5가 장벽을 구체적으로 적음. 대조군과 무관. 초록-본문 불일치 주의 |
| 2404.02244 | 단독 중, 쌍이면 상 | 명시적 열린 질문 2개(다항 Bogolyubov, m 의존). Raghavan과 쌍으로 경계가 선명해짐 |
| 2604.25893 | 상 | 극단 예·반례·Question 1.1이 선명. 초등 보조정리(§2)는 검산형 문제 재료. 1차 조사의 "남은 경계 2"는 틀림 |
| 2506.20813 | 중 | 증명된 부등식이 많고 열린 질문은 §5 하나. §8은 대조군 #52 인접·이미 풀림이므로 제외 필수 |

## `[arXiv 없음]` 및 번호 미확인 선행 논문

- **[arXiv 없음]**
  - Green, 100 open problems(2604.25893의 Question 1.1 출처, 웹 문서).
  - Tao, 블로그 글 "Continued fractions, Bohr sets, and the Littlewood conjecture"(2604.25893 Lemma 8.2, 선택).
- **번호 미확인(참고문헌에 없고 기억에 의존하거나 모름)**
  - Sanders, On the Bogolyubov–Ruzsa lemma(기억 1011.0107).
  - Sanders, The structure theory of set addition revisited(arXiv 여부 모름. arXiv 없음일 수 있음).
  - Tao, Sumset and inverse sumset theory for Shannon entropy(기억 0906.4000).
  - Eberhard–Green–Manners(기억 1301.4579).
  - Tao, An inverse theorem for an inequality of Kneser.
  - Green–Ruzsa, Sets with small sumset and rectification.
  - Green–Tao U³ 역정리.
  - Kontoyiannis–Madiman 2014.
  - Madiman–Kontoyiannis 2018.
  - 이 번호들은 arXiv API 조회가 되지 않아 확인하지 못했습니다.
