# 가법 조합론 최전선 문헌 조사 (묶음 4)

조사 날짜: 2026-11-06
맡은 키워드: K13 시돈 집합과 B_h 집합 / K14 가법 기저와 표현 함수 / K15 합-없는 집합 / K16 조밀한 집합 안의 무한 합집합

조사 방법과 한계 (먼저 읽어 주세요)
- 목록은 arXiv API(export.arxiv.org)의 날짜순 검색으로 만들었고, 후보는 모두 `arxiv.org/abs/<ID>`를 직접 열어 번호, 저자, 제목, 첫 제출일(v1)을 옮겼습니다.
- "읽은 범위"가 `초록+서론`인 논문은 `arxiv.org/html/<ID>`의 서론을 읽었습니다. 다만 열람 도구가 긴 페이지를 요약해서 돌려주기 때문에, 긴 논문(2606.17487, 2504.06424, 2606.06669 등)은 서론 앞부분 위주로만 확인했습니다. `초록`은 초록 페이지만 읽은 것입니다.
- 본문의 증명은 읽지 않았습니다. "남은 경계"는 논문이 서론에서 직접 적은 문장을 근거로 했고, 근거가 불확실하면 `[미확인]` 또는 "추정"으로 표시했습니다.
- 이번에 확인한 철회 논문: 2507.23627(Faust–Tait, 우표 문제, v1·v2 모두 철회, 하한 증명에 틈이 있다고 저자가 적음)과 2604.25214(T. Niu, 철회, 이미 알려진 결과의 중복)는 후보에서 뺐습니다.
- 대조군 번호(#28, #30, #36, #39, #52, #66, #200, #241, #324)와 겹치는 논문은 표 비고에 `대조군 관련: 팩 제외 권고`로 표시했습니다. 확신이 없는 경우에는 `대조군 인접(확인 필요)`로 적었습니다.

---

## K13. 시돈 집합과 B_h 집합 (Sidon sets, B_h sets)

**쉬운 설명.** 시돈 집합은 "두 수를 더한 값이 서로 다 다르게 나오는" 수들의 모임입니다(예: 1, 2, 5, 11은 어떤 두 수를 골라 더해도 합이 모두 다릅니다). B_h 집합은 이것을 확장해 "h개를 더한 값이 모두 다른" 집합입니다. 묻는 것은 이런 성질을 지키면서 집합을 얼마나 크게 만들 수 있는가, 그리고 주어진 어떤 집합 안에서 시돈인 부분집합을 얼마나 크게 뽑을 수 있는가입니다. 암호, 오류정정 부호, 측정 장치 배치(골롬 자)와도 이어지는 문제라 연구가 활발합니다.

**최전선 요약.**

2023년 이전 상태 (배경)
- 1부터 N까지 안에서 시돈 집합의 최대 크기는 N^{1/2}와 거의 같습니다. 오차항을 N^{1/2} + 0.98183·N^{1/4} + O(1) 꼴로 줄인 결과가 알려져 있었습니다(Hou–Zhao 초록이 "이전 발표 계수 0.98183"로 인용).
- 임의의 n개 정수 집합이 항상 품는 시돈 부분집합의 크기 H(n)은 Abbott(1990)의 (0.0805+o(1))√n이 최고였습니다(Bailleul–Riblet 서론 인용). Erdős는 H(n)~√n이라고 추측했습니다.
- 크기 B_h 집합의 최고 상계는 C_h·N^{1/h}+O_h(1), C_h=(⌊h/2⌋!⌈h/2⌉!)^{1/h}입니다(Jia 1993, Chen 1994; 2606.30767 서론 인용).

2024–2026에 바뀐 것
- 유한 시돈 집합 크기의 오차 계수: N^{1/2} + γ·N^{1/4} + O(1)에서 γ ≤ 0.94349...로 낮춤 (2607.01169). 쉬운 말로: 시돈 집합이 N의 제곱근보다 얼마나 더 클 수 있는지의 "여분"이 더 작아졌습니다. 같은 해 10월 Carter–O'Bryant–Tao(2610.36207)는 지름 하한 diam ≥ k² − 1.89k^{3/2}와 |A| ≤ N^{1/2} + 0.945N^{1/4} + 0.447을 냈습니다. 두 논문 모두 #30 주제입니다.
- 임의의 n개 정수 집합 속 시돈 부분집합: H(n) ≥ (1/(3√3)+o(1))√n ≈ 0.19√n (2605.03181). Abbott의 0.0805보다 두 배 이상 좋아졌고, Erdős 추측값 1과는 아직 큰 차이가 있습니다. 같은 방법이 R^N의 점집합과 B_2[g]로도 확장됩니다.
- 약한 시돈 집합(x<y인 합만 서로 달라야 함)에서 가장 큰 시돈 부분집합의 최솟값이 정확히 g(n)=⌈(n+1)/2⌉로 결정됨 (2602.23282). Erdős의 (4,5)-집합 상수 c*는 1/2+1/10716 ≤ c* ≤ 3/5에서 9/17 ≤ c* ≤ 4/7로 좁혀졌으나 값은 아직 모릅니다.
- 제곱수 {1², ..., N²} 안의 시돈 집합: |A| ≤ N·exp(−c·log N/log log N). "로그의 거듭제곱보다 큰 절약"은 이 논문이 처음이라고 합니다 (2606.17487). 이전에는 Hanson의 O(N/(log N)^{1/2}).
- B_h 집합이 선형방정식을 피하면 크기가 최고 상계보다 상수배 작아짐, 극대 B_h 집합이 푸리에 의사난수임 (2606.30767).
- 군(group)에서: 쌍대군이 유계 비틀림일 때 시돈 집합 = 유한 개의 준독립 집합의 합집합 (2606.06669; 이전에는 소수 지수 Malliavin 1967, 제곱없는 지수 Bourgain 1983까지).
- 유한체/순환군에서 시돈 방정식을 일반화한 방정식 X+5Y=3U+3Z를 피하는 집합의 로그 밀도 약 0.5283 (>0.5) (2610.09887).
- 무한 B_h 집합의 밀도 척도 관련 논문(O'Bryant, Wang–Yang, Táfula)은 #39 주제라 아래 표에서 대조군으로 표시했습니다.

**남은 경계.**
1. Erdős 추측 H(n) ~ √n: 현재 하한은 약 0.19√n뿐입니다 (2605.03181 서론; 논문이 "Erdős's conjecture ... remains open"으로 정리).
2. 도미노, 소수 처음 n개, 제곱수 처음 n개 안의 시돈 집합 최대 크기: "Beyond these cases, little seems to be known" (2605.03181 서론).
3. 3-겹 시돈 집합: 크기 Ω(√N)인 Z_N의 3-fold Sidon 부분집합을 만드는 것은 열려 있음 (2606.30767 5절, "It remains an open problem").
4. 모든 시돈 집합이 유한 개 준독립 집합의 합집합인가: 일반 군에서 "longstanding open problem", Z의 경우는 "perhaps the most well-known open problem in the subject" (2606.06669 서론).
5. 제곱수 속 시돈 집합의 정확한 크기, 세제곱수 {1³, ..., N³} 안에 크기 ≫ N인 시돈 집합이 있는가 (2606.17487 서론이 Erdős 질문으로 인용).
6. 4변수 번역불변 방정식 중 B_h 크기 감소를 일으키는 것이 있는가 (2606.30767 1.3절, 예: 2(x₁−x₂)=3(x₃−x₄)는 배제되지 않았다고 적음).

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2605.03181 | 2026-05-04 | Alexandre Bailleul, Robin Riblet | On the largest Sidon subset in a finite subset of R^N | 임의의 n개 정수/R^N 점집합이 품는 시돈 부분집합 하한을 0.0805√n에서 (1/(3√3))√n ≈ 0.19√n로 올림 | 초록+서론 | Erdős 추측 H(n)~√n까지 큰 간극이 남음. 대조군 아님 |
| 2602.23282 | 2026-02-26 | Jie Ma, Quanyu Tang | Largest Sidon subsets in weak Sidon sets | 약한 시돈 집합 속 최대 시돈 부분집합의 최솟값을 ⌈(n+1)/2⌉로 정확히 결정, Erdős (4,5)-집합 상수를 9/17≤c*≤4/7로 좁힘 | 초록+서론 | c* 값은 미결정. 대조군 아님 |
| 2606.17487 | 2026-06-16 | Ernie Croot, Junzhe Mao, Cosmin Pohoata, Adam Sheffer, Chi Hoi Yip | A combinatorial large sieve for Sidon sets, distances, and norm forms | 제곱수 속 시돈 집합과 격자의 서로 다른 거리 문제에 처음으로 "로그 거듭제곱 이상" 절약, B_3[g](세제곱), B_4[g](네제곱) 첫 비자명 상계 | 초록+서론(앞부분) | 서론이 Erdős #773, #1206을 인용. 대조군 아님 |
| 2606.30767 | 2026-06-29 | Nathan Tung | Linear equations and chromatic thresholds in B_h sets | 선형방정식을 피하는 B_h 집합은 최고 상계보다 상수배 작고, 극대 B_h 집합은 푸리에 의사난수임을 보임 | 초록+서론 | B_h 크기 상계를 다루므로 #241(B_3 크기)과 인접(확인 필요). 팩에 넣을 때 주의 |
| 2606.06669 | 2026-06-04 | Mark Lewko | The Sidon Decomposition Problem in Abelian Groups of Bounded Torsion | 유계 비틀림 군에서 시돈 집합 = 준독립 집합의 유한 합집합 | 초록+서론(앞부분) | 조화해석 배경 필요. 열린 문제(Z의 경우) 명시. 대조군 아님 |
| 2610.09887 | 2026-10-07 | Katalin Gyarmati | Translation-invariant equations in F_p^n and groups | 시돈 방정식을 일반화한 방정식의 해 없는 집합 크기 상계(슬라이스 랭크)와 순환군 구성(밀도 약 0.5283) | 초록 | 대조군 아님 |
| 2409.03128 | 2024-09-04 | János Pach, Dmitrii Zakharov | Ruzsa's problem on Bi-Sidon sets | 덧셈·곱셈 모두 시돈인 부분집합 하한을 N^{1/3}에서 N^{1/3+7/78+o(1)}로 | 초록 | 대조군 아님 |
| 2607.01169 | 2026-07-01 | Jianfeng Hou, Hongbin Zhao | An Improved Upper Bound for Finite Sidon Sets via Vector-Valued Smoothing | F(N) ≤ N^{1/2}+0.9435·N^{1/4}+O(1) | 초록 | 대조군 관련: 팩 제외 권고 (#30) |
| 2610.36207 | 2026-10-26 | Daniel Carter, Kevin O'Bryant, Terence Tao | On the diameter and distribution of Sidon sets | 시돈 집합 지름 하한 k²−1.89k^{3/2}, [1,N] 안 크기 N^{1/2}+0.945N^{1/4}+0.447 | 초록 | 대조군 관련: 팩 제외 권고 (#30) |
| 2607.23795 | 2026-07-26 | Kevin O'Bryant | On the Thickness of Infinite Generalized Sidon Sets, II | 짝수 h에 대해 무한 B_h 집합의 계수함수 liminf 상계 | 초록 | 대조군 관련: 팩 제외 권고 (#39 계열) |
| 2611.01871 | 2026-11-01 | Guoqing Wang, Wenkai Yang | Infinite Generalized Sidon Sets with a Negative Answer to a Problem of Szemerédi | 무한 B_h 집합이 limsup A(x)/x^{1/h}=1/h, liminf=0을 가짐 | 초록 | 대조군 관련: 팩 제외 권고 (#39 계열) |
| 2607.20753 | 2026-07-22 | Christian Táfula | Infinite Sidon-type sets for zero-sum linear forms | 무한 시돈 집합의 밀도 정리를 영합 선형형식으로 일반화 | 초록 | 대조군 관련: 팩 제외 권고 (#39 계열) |

기타 참고(후보 아님): 2510.19804(Alexeev–Mixon, 유한 시돈 집합이 완전 차집합으로 확장된다는 Erdős 추측의 반례 {1,2,4,8,13}, 1000달러 상금 문제, 2025-10-22, 초록만 읽음). 문제 성립 확인용 사례로는 좋으나 이 키워드의 최전선 핵심은 아닙니다.

**팩 추천.**
1. **2605.03181 (Bailleul–Riblet).** 서론이 이전 최고 결과(Abbott 0.0805), 새 결과(0.19), Erdős 추측(1)을 한 곳에 숫자로 적어 둡니다. 간극이 크고 구체적이어서 "어떤 부분집합에서 더 낫게 할 수 있나"류 문제를 만들기 쉽습니다. 대조군과 겹치지 않습니다.
2. **2602.23282 (Ma–Tang).** 약한 시돈 집합이라는 비교적 새 개념, 정확한 값(⌈(n+1)/2⌉)과 아직 닫히지 않은 c*의 범위(9/17~4/7)가 함께 있습니다. 유한 판으로 만들어 체커로 채점하기 좋은 구조입니다. 대안으로 2606.17487을 넣을 수 있으나 정수론 도구(체)가 많이 필요합니다.

---

## K14. 가법 기저와 표현 함수 (Additive bases, representation functions)

**쉬운 설명.** 집합 A가 "기저"라는 것은 A의 두 원소(또는 h개 원소)를 더해서 거의 모든 자연수를 만들 수 있다는 뜻입니다. "표현 함수" r(n)은 n을 A의 두 원소의 합으로 쓰는 방법이 몇 가지인가를 세는 함수입니다. 핵심 질문은 두 가지입니다. A가 너무 크지 않으면서 모든 수를 표현할 수 있는가, 그리고 표현 방법의 수가 항상 커지는가 아니면 한없이 작게 억제될 수 있는가입니다. 가장 유명한 미해결 문제는 Erdős–Turán 추측(기저이면 r(n)이 유계일 수 없다)입니다. 이 추측은 대조군(#28)이므로 아래에서는 그 주변의 다른 질문 위주로 정리했습니다.

**최전선 요약.**

2023년 이전 상태 (배경)
- Erdős는 A+A=N이면서 표현 수가 O(log N)인 기저를 확률적으로 보였습니다(2405.08650 서론). Erdős–Turán 추측("로그 인자를 상수로 줄일 수 없다")은 "major open problem"입니다.
- 극소 점근 기저(Erdős–Nathanson 1988)에서 밀도 α인 극소 기저는 α ∈ (0, 1/(2h−2))에 대해서만 알려져 있었고(h=2는 (0,1/2]), 극소 기저의 하밀도는 1/h 이하입니다(Nathanson–Sárközy 1989) (2609.08706 서론 인용).
- 시돈 집합이면서 3차 점근 기저인 집합: Pilatte가 2023년 증명 (arXiv 2303.09659, 배경).

2024–2026에 바뀐 것
- 표현 수가 n^{c/log log n}으로 억제되는 "명시적" 기저 A+A=N 구성 (2405.08650; 이전 존재 증명은 비명시적). Erdős–Turán 추측과는 거리가 멉니다(로그보다 훨씬 약함).
- 모든 h ≥ 3과 0 < α < 1/h에 대해 밀도 α인 극소 점근 기저가 존재함 (2609.08706). 1988년 Erdős–Nathanson 열린 문제의 종결.
- 2차 점근 기저의 세 성질(표현 함수 발산 / 두 기저의 합집합으로 분해 가능 / 극소 기저를 포함)이 서로 독립임. 표현 함수 성장 조건이 로그보다 약할 때 8가지 조합이 모두 가능 (2603.03472).
- 무한 시돈 집합이 3−η차 점근 기저: 0<η<0.0527이면 m=s₁+s₂+s₃, min s_i ≤ m^{1−η}인 시돈 집합 존재. 쉬운 말로: 시돈 집합이 "3차 기저"가 되는 것에서 "거의 2.95차"까지 가깝게 만든 것입니다 (2607.11351).
- 도메인 변경: 집합 A를 B+B로 덮는 데 필요한 B의 최소 크기가 Z에서 Q로 가면 줄어드는 정도는 2배 이하(오차 O(√n)로 거의 정확), N에서 Z로는 O(n log n) (2409.07442). 이후 Xu가 BvHK 추측의 강화형 |B| ≥ n + C(t+1, 2)를 R^n에서 증명 (2605.10771).
- Erdős–Turán 추측의 밀도 버전: 비합 집합의 상밀도 D(E)<7/32이면 limsup r(n)>5 (Konstantoulas의 1/10에서 개선) (2605.30922). 대조군(#28) 직결.
- 표현 함수 성장 제어: 선형형식의 유계 점근 기저 존재 (2609.11848), Sárközy–Sós 1997 질문 두 개 해결 (2607.16613).

**남은 경계.**
1. 시돈 점근 기저의 최적 η: "Find an admissible constant η > 0, as large as possible" (Problem 1.2, 2607.11351 서론). 지금은 η<0.0527.
2. 합의 세 항을 비슷한 크기로 쓸 수 있는가: 어떤 θ<1에 대해 |s_i − m/3| ≪ m^θ인 무한 시돈 집합이 있는가 (Problem 6.2, 2607.11351).
3. B_h[1] 집합이 점근 기저가 되는 최소 차수 k(h), 그리고 (h+1)차 점근 기저가 B_h[g]가 되는 최소 g(h) (Problem 6.3, 6.4, 2607.11351).
4. 표현 수를 exp((log N)^ε) 이하로 억제하는 명시적 기저가 있는가: "would be interesting" (2405.08650 서론).
5. (조건부) 극소 점근 기저와 분해 가능성의 다른 성장 영역: 2603.03472 서론은 새 열린 문제를 명시하지 않습니다. [미확인: 본문 끝에 추가 문제가 있는지 읽지 않음]
6. 대조군 주변: Erdős–Turán 추측 자체(#28)와 r(n)≥C log n 문제(#66 계열)는 팩에서 빼야 합니다.

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2607.11351 | 2026-07-13 | Wei Niu | An asymptotic Sidon basis of order 3−η | 무한 시돈 집합이 3−η차 점근 기저가 될 수 있음 (0<η<0.0527) | 초록+서론 | 서론이 Erdős Problem #39를 "major open problem"으로 언급하나 이 논문 주제는 기저. 열린 문제 6개를 번호 붙여 명시. 대조군 인접(확인 필요) |
| 2609.08706 | 2026-09-08 | Shi-Qiang Chen, Quan-Hui Yang | On a problem of Erdős and Nathanson related to minimal asymptotic bases of order h | h≥3, 0<α<1/h인 밀도 α 극소 점근 기저 존재 증명 | 초록+서론 | 문제 하나를 완전히 닫음. 서론에 새 열린 문제 없음. 대조군 아님 |
| 2603.03472 | 2026-03-03 | Daniel Larsen | Three Questions of Erdős-Nathanson on Asymptotic Bases of Order 2 | 표현 함수 발산, 분해 가능성, 극소 기저 포함 세 성질의 독립성 | 초록+서론 | 표현 함수 r(n)→∞ 성질을 다루므로 #66과 인접(확인 필요) |
| 2405.08650 | 2024-05-14 | Vishesh Jain, Huy Tuan Pham, Mehtaab Sawhney, Dmitrii Zakharov | An explicit economical additive basis | A+A=N, 표현 수 n^{c/log log n}인 명시적 집합 | 초록+서론 | 서론이 Erdős–Turán 추측(#28)을 배경으로 다룸. 대조군 인접(확인 필요) |
| 2409.07442 | 2024-09-11 | Boris Bukh, Peter van Hintum, Peter Keevash | Additive Bases: Change of Domain | Ruzsa의 두 질문 해결: ℓ_Z ≤ 2ℓ_Q, ℓ_N = O(ℓ_Z log ℓ_Z) | 초록 | 대조군 아님 |
| 2605.10771 | 2026-05-11 | Zixiang Xu | A solution to a strengthened conjecture of Bukh, van Hintum and Keevash on additive bases | R^n에서 강화 추측 \|B\| ≥ n + C(t+1,2) 증명, 모든 기저에서 최적 | 초록 | 대조군 아님 |
| 2605.30922 | 2026-05-29 | Huixi Li, Zihan Zhang | An Improvement of Konstantoulas' Density Constant | Erdős–Turán 추측 밀도 버전의 상수를 1/10에서 7/32로 | 초록+서론 | 대조군 관련: 팩 제외 권고 (#28) |

기타 참고: 2603.29961 (Alexeev–Putterman–Sawhney–Sellke–Valiant, 2026-03-31)는 "가법 기저 A를 A₁, A₂로 나눠 각 A_i+A_i의 간격이 유계가 되게 할 수 있는가"라는 Erdős 질문을 포함하며 OpenAI 내부 모델의 증명이라고 초록에 밝혔습니다. 초록만 읽었고 답(예/아니오)은 초록에 없어 [미확인]입니다. 팩 후보로는 보류.
2507.23627(우표 문제 개선)은 철회됨. 2610.35027(van Doorn–Liu–Tang, 거의 완전한 덧셈 여집합, limsup A(x)B(x)/x ∈ [3/2, 2])은 기저의 쌍(여집합) 문제로 관련이 있으나 초록만 읽음.

**팩 추천.**
1. **2607.11351 (Niu).** 서론이 역사 → 새 결과 → 번호가 붙은 열린 문제(Problem 1.2, 6.1–6.4)를 한 곳에 정리해 줍니다. 구체적이고 숫자를 바꿔 물어볼 수 있는 열린 질문이 가장 많습니다. 단, 서론에 #39 언급이 있으니 팩 본문에서 그 문장은 제외하는 편이 안전합니다.
2. **2609.08706 (Chen–Yang) 또는 2603.03472 (Larsen).** 극소 기저 쪽의 최근 결과입니다. 둘 다 서론에 새 열린 문제를 적지 않으므로 "결과 + 닫힌 경계" 설명용입니다. 열린 질문을 담은 것을 원하면 Niu의 6절과 함께 2405.08650(서론의 "exp((log N)^ε)")을 보조로 쓸 수 있으나 #28 인접입니다.

---

## K15. 합-없는 집합 (Sum-free sets)

**쉬운 설명.** 합-없는 집합은 "집합 안의 두 수를 더한 값이 그 집합 안에 다시 나오지 않는" 집합입니다(예: 홀수 전체). 대표적인 질문은 임의의 n개 정수 집합에서 합-없는 부분집합을 얼마나 크게 뽑을 수 있는가입니다. Erdős는 항상 n/3 이상을 뽑을 수 있음을 보였고, 이 n/3이 거의 최선인지 오랫동안 물었습니다. 격자, 유한체, 군처럼 다른 환경에서도 최대 크기와 개수를 묻습니다.

**최전선 요약.**

2023년 이전 상태 (배경)
- Erdős: 모든 유한 정수 집합 A는 크기 ≥ |A|/3인 합-없는 부분집합을 가짐. Alon–Kleitman: (N+1)/3. Bourgain: (N+2)/3 (푸리에 해석). Shakan(2022)이 다른 증명. Eberhard–Green–Manners: S(N) ≤ N/3 + o(N)로 1/3이 점근적으로 최선 (Bedert 서론 정리).
- 유한 벡터공간 F_p^n의 큰 합-없는 집합 구조와 개수 연구가 진행 중이었음.

2024–2026에 바뀐 것
- 임의의 n개 정수 집합은 크기 ≥ n/3 + c·log log n인 합-없는 부분집합을 가짐 (2502.08624, Green의 100개 열린 문제 중 1번을 답함). 쉬운 말로: n/3에 "아주 천천히 커지는 덤"이 항상 붙는다는 것입니다. 이전에는 상수(+2/3)뿐이었습니다.
- Erdős–Moser 합-없는 집합 문제: 모든 유한 집합 A ⊂ Z는 |B| ≥ (log|A|)^{1+Ω(1)}이고 b₁+b₂ ∉ A (b₁≠b₂)인 부분집합 B를 가짐. k-배치 정리 개선으로 같은 형태의 최고 하한(Sanders)의 새 증명 (2501.10203). 이후 지수를 68에서 36으로 줄이는 개선 (2610.03750).
- 격자 정육면체 [n]^d에서 가장 큰 합-없는 집합의 극한 밀도를 모든 차원 d에서 결정: 두 개의 초평면 슬라이스 {1 ≤ L(x) < 2} 꼴이 최적 (2605.00816; d=1은 1/2, d=2는 3/5, d=3,4는 Lepsveridze–Sun). 이 극한 상수를 이용해 [n]^d의 합-없는 부분집합 개수도 2^{M+O(n^{d-1})}로 결정 (2608.23544, d≥3; 2510.15621, d=2).
- F_3^n: 밀도 1/6 초과 합-없는 집합을 분류하여 Lev의 주기성 추측 해결 (2408.15174). F_5^n: 크기 ≥ 28·5^{n−3}인 합-없는 집합은 두 평행 초평면에 들어가거나 Λ×F_5^{n−3}꼴 (2604.02894).
- 아벨군에서 극대 합-없는 집합의 개수: 중간 성장을 보이는 군이 무한히 많고, 이전 추측 여러 개가 반증됨 (2509.19248); 열린 문제 목록 (2506.17401).
- 대칭 영역에서 합-없는 부피 비율: 정육면체는 정확히 1/2, 공은 1/2+o(1) 이하 (2607.07991).

**남은 경계.**
1. EGM의 o(N) 항: "determining a reasonable upper bound remains an interesting problem" (2502.08624 서론). 즉 S(N) ≤ N/3 + (얼마?)의 정확한 크기가 미해결입니다. 하한은 log log N에 불과합니다.
2. L¹ 상수: 부분집합 B의 푸리에 L¹ 노름에 대해 log|B| ≪ ‖1̂_B‖₁ ≤ |B|^{1/2}의 두 상수 결정은 "well-known problem" (2502.08624 서론).
3. 볼록 영역 K ⊂ R²에서 가장 큰 합-없는 부분집합이 항상 {x∈K : L(x)∈T}꼴인가 (Problem 5.2, 2605.00816). 같은 논문이 d가 충분히 크면 일반 볼록집합에서는 성립하지 않음을 보였으므로 d=2가 남은 경계입니다.
4. 군의 극대 합-없는 집합 개수 추측 f_max(Z_5^k)=3^{n/10+o(n)} (Conjecture 2.3, 2506.17401). 단, 같은 분야의 다른 추측 일부는 2509.19248이 반증했으니 읽을 때 순서를 유의해야 합니다.
5. 적당히 일반적인 "type II 군"에서 서로 다른 극대 합-없는 집합 개수에 대한 추측이 어느 군까지 맞는가 (2506.17401의 질문, 2509.19248이 일부 반례).

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2502.08624 | 2025-02-12 | Benjamin Bedert | Large sum-free subsets of sets of integers via L¹-estimates for trigonometric series | n개 정수 집합은 크기 ≥ n/3 + c log log n 합-없는 부분집합을 가짐 | 초록+서론(앞 10만 자) | 대조군 아님. 이 분야 핵심 |
| 2605.00816 | 2026-05-01 | Peter Keevash, Jeck Lim | On the largest sum-free subset of the lattice cube | [n]^d의 최대 합-없는 부분집합 극한 밀도를 모든 d에서 결정 | 초록+서론 | 열린 문제 Problem 5.2 명시. 대조군 아님 |
| 2501.10203 | 2025-01-17 | Adrian Beker | The Erdős–Moser sum-free set problem via improved bounds for k-configurations | k-배치 밀도 임계값 개선, Erdős–Moser 합-없는 집합 문제 새 증명 | 초록 | 대조군 아님 |
| 2506.17401 | 2025-06-20 | Nathanaël Hassler, Andrew Treglown | Notes on sum-free sets in abelian groups | 아벨군의 극대 합-없는 집합에 관한 열린 문제 정리, 대부분 짝수 위수 군에서 극대 서로 다른 합-없는 집합 개수 계산 | 초록+서론/문제 절 | 일부 추측이 2509.19248에서 반증됨. 대조군 아님 |
| 2509.19248 | 2025-09-23 | József Balogh, Ramon I. Garcia, Hong Liu, Ningyuan Yang | Infinitely many groups exhibiting intermediate growth in maximal sum-free sets | 극대 합-없는 집합 수의 중간 성장 군 무한 족, Liu–Sharifzadeh와 Hassler–Treglown의 추측 반증 | 초록 | 대조군 아님 |
| 2408.15174 | 2024-08-27 | Christian Reiher | On Lev's periodicity conjecture | F_3^n에서 밀도 > 1/6인 합-없는 집합 분류, Lev 추측 해결 | 초록 | 대조군 아님 |
| 2604.02894 | 2026-04-03 | Christian Reiher, Sofia Zotova | Large sum-free sets in finite vector spaces II | F_5^n의 큰 합-없는 집합 분류 (Versteegen의 질문) | 초록 | 대조군 아님 |
| 2607.07991 | 2026-07-08 | Anubhab Ghosal, Dmitry Tsarev | On the largest size of sum-free sets in symmetric regions | σ([−1,1]^d)=1/2, 공은 1/2+o_d(1) 이하 | 초록 | Bukh의 질문에 대한 답. 대조군 아님 |

**팩 추천.**
1. **2502.08624 (Bedert).** 이 키워드의 가장 두드러진 최근 돌파구이며, 서론이 "Erdős → Alon–Kleitman → Bourgain → EGM(1/3이 최선) → 이 논문"의 정확한 흐름을 줍니다. "o(N) 항의 실제 크기"라는 열린 질문이 남아 있어 문제를 낳을 수 있습니다. 대조군과 겹치지 않습니다.
2. **2605.00816 (Keevash–Lim).** 정확한 상수 공식과 Problem 5.2(d=2 볼록 영역)가 있어, 유한판으로 체커를 만들기 좋은 구체적 환경(격자)을 제공합니다. 군 쪽 열린 문제를 원하면 2506.17401과 2509.19248을 함께 읽게 해야 합니다(앞 논문의 추측 일부가 뒤 논문에서 반증됨).

---

## K16. 조밀한 집합 안의 무한 합집합 (Infinite sumsets in dense sets)

**쉬운 설명.** 자연수의 부분집합이 "조밀하다"는 것은 큰 범위에서 일정 비율 이상의 수를 담고 있다는 뜻입니다. Erdős는 이런 집합이 항상 무한 집합 B의 합 B+B(또는 B+C, 약간 이동한 B+B+t)를 통째로 품고 있을 것이라고 추측했고, 이것이 2022년경 에르고딕 이론(동역학계 방법)으로 해결되었습니다. 이후 연구는 "어떤 모양의 무한 합집합이 조밀한 집합 안에 반드시 들어 있는가, 밀도가 얼마나 되어야 하는가, 다른 군에서도 되는가"로 옮겨 가고 있습니다.

**최전선 요약.**

2023년 이전 상태 (배경)
- 상밀도(upper Banach density)가 양인 집합은 무한 집합 B, C의 B+C를 품음(Moreira–Richter–Robertson 2019). Erdős의 B+B+t 추측도 Kra–Moreira–Richter–Robertson(KMRR)이 증명(arXiv 2206.12377, 2022년 제출, 배경으로만 인용). KMRR 서베이(arXiv 2311.06197)가 열린 문제 목록을 제시.

2024–2026에 바뀐 것
- 밀도 임계값: 하밀도 > 1/2 또는 상밀도 > 3/4이면 (이동 t∈{0,1}로) 무한 B+B+t가 존재, 하밀도 > 3/4 또는 상밀도 > 5/6이면 이동 불필요, 모두 최적. 3색 조밀 분할에서 단색 B+B+t 없는 예도 구성 (2404.12201). 이후 일반 아벨군으로 확장 (2504.08649), 다시 d_Φ(A)+d_{Φ/2}(A)>1이면 t+B+B⊂A라는 날카로운 조건 (2607.18132).
- 밀도 유한합 정리(Hindman 유한합 정리의 밀도판): 상밀도가 양인 A와 모든 k에 대해 무한 B와 이동 t가 있어 B의 서로 다른 m개(1≤m≤k)의 합이 모두 A−t에 속함 (2504.06424). 이를 강화한 판 (2510.18788)과 더 일반적인 무한 선형 패턴 분류 (2505.15458).
- Erdős의 B+C 추측의 짧은 증명 (2603.27258).
- 모든 가산 무한 아벨군에서 상밀도 양인 집합은 k개 무한 집합의 합 B₁+...+B_k를 품음. KMRR 서베이의 문제 약 20개를 해결/정정, B+B+t의 하밀도 상한이 1/2, B+B가 3/4임을 증명, 대부분 Lean 4로 형식화 (2610.39637).
- 반례 계열: 곱 집합과 다항 패턴에 대한 일반화는 거짓 (2404.17383, Straus 구성).
- 성장률: 무한 합집합에서는 B, C가 [N]에서 하한 H(N)→∞ 이상의 원소를 갖도록 보장하는 성장률이 존재하지 않음, 유한판에서는 크기 B, C가 log N 정도로 보장됨 (2606.07310).
- Owings 질문 해결: 자연수의 2색칠에는 항상 B+B가 단색인 무한 B가 존재 (2607.17333).
- 균일성과 합집합의 모양: U^k(Φ)-균일 집합에서 가능한 무한 합집합의 종류 (2601.06915, 2609.20522).

**남은 경계.**
1. 유한판 상계: 모든 δ밀도 A ⊂ {1..N}가 크기 ~log N인 B+C를 품는데, 반대로 limsup φ_δ(N)/log N < ∞가 성립하는가는 "seems out of reach" (KMRR Conjecture 4.10의 (2); 2606.07310 Remark 1.4). Konyagin–Shkredov가 (log N)(log log N)^{10+ε} 쪽 상계를 줌.
2. 최대값 버전: 밀도 1의 집합 A 또는 2색칠에서 max 형태의 성장률 상계가 모든 충분히 큰 N에서 성립하는가 (Question 3.3, 3.4, 2606.07310).
3. 임의의 Følner 수열 Φ에 대해, 부분수열 Ψ에서 d_Ψ(A)+d_{Ψ/2}(A)=1이면서 t+B+B ⊄ A인 A가 있는가: "probably very difficult in full generality" (Question 1.8, 2607.18132).
4. 서베이 문제 5.23과 §5.4(b)의 "두 번째 수정판"이 열려 있음 (2610.39637의 Table 1).
5. 진행 방식의 질문: 진보적 측도가 항상 Erdős 진행인가 "It would be interesting to know whether it always is" (2504.06424 4.1절).

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2504.06424 | 2025-04-08 | Bryna Kra, Joel Moreira, Florian K. Richter, Donald Robertson | The Density Finite Sums Theorem | 상밀도 양인 집합의 이동본이 무한 집합 B의 서로 다른 m개(m≤k) 합을 모두 품음 | 초록+서론(앞 10만 자) | 대조군 아님. 이 분야 핵심 |
| 2606.07310 | 2026-06-05 | Felipe Hernández, Luke Hetzel | On growth rates of infinite and finite sumsets | 무한 합집합 성장률 부존재, 유한판에서 크기 ~log N 보장 | 초록+서론 | 열린 질문(Question 3.3, 3.4) 명시. 대조군 아님 |
| 2610.39637 | 2026-10-29 | Shisheng Li, Yong Su | Solutions to several problems on infinite sumset configurations | 가산 무한 아벨군에서 B₁+...+B_k 존재, KMRR 서베이 문제 약 20개 해결, Lean 4 형식화 | 초록+서론(앞 10만 자) | 대조군 아님 |
| 2607.18132 | 2026-07-20 | Ioannis Kousek | Sharp density conditions for infinite B+B sumsets in abelian groups | d_Φ(A)+d_{Φ/2}(A)>1이면 t+B+B⊂A, 최적임 | 초록+서론 | Question 1.8 명시. 대조군 아님 |
| 2404.12201 | 2024-04-18 | Ioannis Kousek, Tristán Radić | Infinite unrestricted sumsets of the form B+B in sets with large density | B+B+t 존재의 밀도 임계값(1/2, 3/4, 5/6) 확정과 3색 반례 | 초록 | 대조군 아님 |
| 2504.08649 | 2025-04-11 | Dimitrios Charamaras, Ioannis Kousek, Andreas Mountakis, Tristán Radić | Infinite unrestricted sumsets in subsets of abelian groups with large density | 아벨군에서의 밀도 조건과 최적성 | 초록 | 대조군 아님 |
| 2607.17333 | 2026-07-19 | Wen Huang, Zhengxing Lian, Song Shao, Rongzhong Xiao, Leiye Xu, Shuhao Zhang | An affirmative answer to Owings's sumset question | 자연수의 임의의 2색칠에 B+B가 단색인 무한 B가 존재 | 초록 | 밀도 아닌 색칠 문제. 대조군 아님 |
| 2603.27258 | 2026-03-28 | Bryna Kra, Joel Moreira, Florian K. Richter, Donald Robertson | A short proof of Erdős's B+C conjecture | 상밀도 양인 집합이 두 무한 집합의 합을 품는다는 정리의 짧은 증명 | 초록 | 대조군 아님 |
| 2404.17383 | 2024-04-26 | Ethan Ackelsberg | Counterexamples to generalizations of the Erdős B+B+t problem | 곱 집합·다항 패턴 일반화의 반례 | 초록 | 대조군 아님 |

기타 참고: 2510.18788(Hernández–Kousek–Radić, 2025-10-21, 밀도 유한합 정리의 강화판과 최적성 반례, 초록만 읽음), 2505.15458(Hernández, 2025-05-21, 무한 선형 패턴, 초록만 읽음).

**팩 추천.**
1. **2504.06424 (KMRR, 밀도 유한합 정리).** 이 분야의 가장 큰 최근 결과이고 "Erdős가 물었던 Hindman 정리의 밀도판"이라는 서사가 분명합니다. 서론이 정리 → 필요한 이동 t(홀수 집합 반례) → Straus 반례를 함께 설명해 문제를 낳을 재료가 많습니다.
2. **2606.07310 (Hernández–Hetzel).** 열린 질문(3.3, 3.4)과 "seems out of reach"인 추측이 서론에 명시되어 있습니다. 숫자(log N 규모)가 들어 있어 유한판으로 바꾸기 쉽습니다. 서베이식 정리를 원하면 2610.39637로 대체할 수 있습니다.

---

## 요약 (키워드별 추천 번호)

- K13: 2605.03181, 2602.23282 (대안 2606.17487)
- K14: 2607.11351, 2609.08706 또는 2603.03472 (보조 2405.08650; Niu와 Jain 등은 대조군 인접 주의)
- K15: 2502.08624, 2605.00816
- K16: 2504.06424, 2606.07310 (대안 2610.39637)
