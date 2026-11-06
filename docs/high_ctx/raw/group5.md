# 가법 조합론 최전선 문헌 조사: 그룹 5

조사 날짜: 2026-11-06

맡은 키워드:
- K17. 방정식의 분할 정칙성 / 산술 램지 이론 (partition regularity of equations, arithmetic Ramsey theory)
- K18. 영합 문제 (zero-sum problems)
- K19. 확대 합집합과 제한 합집합 (sums of dilates, restricted sumsets)
- K20. erdosproblems.com 가법 조합론 태그의 2024–2026 해결 사례 (AI 관여 여부 포함)

**읽은 범위에 관한 공통 주의.** arXiv 초록 페이지는 WebFetch(요약 모델 경유)로 열어 제목, 저자, v1 제출일을 옮겼습니다. 따라서 "초록"이라고 적은 항목은 초록 요약을 읽은 것이고, 정리의 정확한 문구는 원문과 대조가 필요합니다. 서론(또는 본문 일부)까지 읽은 항목에는 따로 표시했습니다. erdosproblems.com 개별 문제 페이지는 직접 열어 읽었습니다. 사이트의 `problems.yaml`(Terence Tao 저장소 `teorth/erdosproblems`의 데이터)은 태그와 상태를 뽑는 데만 썼습니다. 이 사이트 본문과 Tao 위키에 나오는 AI 모델 이름(GPT-5.5 Pro, GPT-6 Astra, Claude Mythos 등)은 사이트에 적힌 그대로 옮긴 것이고, 제가 따로 검증한 것이 아닙니다.

---

## K17. 방정식의 분할 정칙성 / 산술 램지 이론 (partition regularity of equations / arithmetic Ramsey theory)

**쉬운 설명.** 자연수를 빨강, 파랑처럼 유한 개의 색으로 마음대로 칠한다고 합시다. 어떤 방정식에 대해 "어떻게 칠하든 같은 색 숫자들만으로 이루어진 해가 반드시 나온다"면 그 방정식을 분할 정칙(partition regular)이라 부릅니다. 선형 방정식은 라도(Rado)의 정리로 완전히 분류되어 있습니다. 그런데 x²+y²=z²(피타고라스 삼중쌍)이나 x+y=z²처럼 비선형 방정식은 이 분류가 통하지 않아, 색깔 수가 2개일 때조차 어렵거나 아직 모릅니다. "색칠이라는 임의의 무질서 속에서도 반드시 남는 질서"를 묻는 분야이고, 곱셈 구조와 덧셈 구조가 얽혀 있어 가법 조합론에서 가장 난해한 영역 중 하나입니다.

**최전선 요약.**

*2023년 이전 상태.*
- x²+y²=z²: 색이 2개일 때는 모든 칠하기에 단색 피타고라스 삼중쌍이 있음이 알려졌습니다(Heule–Kullmann–Marek 2016, SAT 풀이기 기반의 컴퓨터 증명이며 증명 파일이 약 200TB). 색이 3개 이상이면 열려 있었습니다. 이것은 2309.10636과 2609.34676의 서론에서 확인했습니다.
- x+y=z²: 일반 유한 색칠에서는 분할 정칙이 아닙니다(Csikvári–Gyarmati–Sárközy). 2색이면 분할 정칙입니다. x와 y만 같은 색이면 되는 변형은 Khalfalah–Szemerédi가 분할 정칙임을 보였습니다. 3색으로 비자명한 단색 해를 완전히 피하는 칠하기가 있다는 결과(Green–Lindqvist, arXiv 1608.08374)는 검색 결과 요약으로만 확인했습니다.
- 위 세 문장 모두 2023년 이전 배경입니다.

*2024–2026에 바뀐 것.*
- "피타고라스 쌍"(x²±y²=z²을 만족하는 z가 어딘가에 있는 x, y)은 유한 개의 색으로 어떻게 칠해도 x, y를 같은 색으로 잡을 수 있습니다. 삼중쌍 전체(x, y, z 모두 같은 색)는 아직 모릅니다. 이 결과(Frantzikinakis–Klurman–Moreira)는 v1이 2023-09-19라서 후보 표에는 배경으로만 넣었습니다. 공저자 3인의 후속 논문 2407.08360(2024-07)이 ax²+by²=cz²로 일반화해, 계수에 대한 자연스러운 조건 아래 x, y를 같은 색으로 잡을 수 있음을 보였습니다. 일부 계수에서는 Elliott형 추측을 가정합니다(초록 기준).
- 유한 개의 값만 갖는 완전 곱셈 함수의 등위집합으로 정의된 색칠에는 피타고라스 삼중쌍이 반드시 들어 있습니다. 이 결과의 적용 범위는 초록마다 표현이 조금 다릅니다(2309.10636 초록, 2508.09778 초록, 2607.04903 초록). 정확한 정리 범위는 원문 확인이 필요합니다.
- 비선형 항을 추가한 피타고라스형은 2색에서 분할 정칙입니다. x²+y²=z²+P(u₁,…,uₙ)이 적당한 다항식 P에 대해 2-정칙이라는 결과(2501.17203)가 있습니다. 같은 논문은 "m차 동차방정식 중 n-정칙이지만 (n+1)-정칙은 아닌 것이 모든 m, n에 대해 존재한다"는 정칙성 차수 결과도 줍니다. m=1일 때가 Rado 추측(Alexeev–Tsimerman, Golowich가 증명)입니다.
- 비선형 라도 정리: 라도의 "열 조건"이 비선형 항이 붙은 계에서도 충분조건이 되는 경우와, 그 필요조건의 일반화를 Goswami(2407.05542, 2024-07)가 보였습니다. Luperi Baglini–Vegnuti(2510.19370, 2025-10)는 "점근적 분할 정칙성"이라는 개념으로 페르마–카탈랑 방정식 등에 대한 부정적 결과를 모았습니다(둘 다 초록 기준).
- 2026-09-28자 Leng(2609.34676)는 2색 피타고라스 분할 정칙성의 새 해석적 증명을 줍니다. 초록과 서론에 증명이 "ChatGPT Astra가 찾았다"고 적혀 있습니다. 서론은 "일반 유한 색 문제는 여전히 열려 있다"고 밝힙니다.

**남은 경계.**
1. x²+y²=z²이 색 3개 이상에서도 분할 정칙인가. 2609.34676 서론이 "general finite-color problem remains open"이라고 명시합니다.
2. x²+y²=2z², x²+2y²=z²에서 두 변수를 같은 색으로 잡을 수 있는가. 2309.10636 서론의 Problem 2이며, 앞의 식은 Gyarmati–Ruzsa 추측이라고 적혀 있습니다.
3. 라도 조건을 만족하는 계수 (a, b, c)에 대해 유한 값 완전 곱셈 함수의 등위집합이 항상 ax²+by²=cz²의 해를 포함하는가. 같은 서론의 Problem 1이며, (1,1,2)와 (1,2,1)은 저자들이 처리하지 못했다고 합니다.
4. 이 영역 전체의 현황과 도전 과제를 정리한 서베이가 2411.17523입니다.

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2411.17523 | 2024-11-26 | N. Frantzikinakis | Partition regularity of homogeneous quadratics: Current trends and challenges | 동차 이차방정식의 분할 정칙성 현황과 열린 문제 서베이 | 초록 | 최전선 개관용 |
| 2407.08360 | 2024-07-11 | Frantzikinakis, Klurman, Moreira | Partition regularity of generalized Pythagorean pairs | ax²+by²=cz²에서 x, y를 같은 색으로 잡을 수 있음(일부는 Elliott형 추측 가정) | 초록 | |
| 2501.17203 | 2025-01-28 | S. D. Adhikari, S. Goswami | Homogeneous Patterns in Ramsey Theory | x²+y²=z²+P(u)가 2-정칙, 정칙성 차수 결과, A∪(A+B)∪A·B 단색 유한판 | 초록 | 댓글에 "Proofs are corrected"가 있어 증명이 수정된 판이 있음. 정리 진술은 이 판 기준으로 재확인 필요 |
| 2508.09778 | 2025-08-13 | N. Frantzikinakis, A. Mountakis | Recurrence for pretentious systems along generalized Pythagorean triples | 유사 곱셈(pretentious) 작용에 대해 ax²+by²=cz² 해를 따르는 재귀 | 초록 | 에르고딕 이론 방식 |
| 2607.04903 | 2026-07-06 | G. Azevedo, J. Moreira | Pythagorean triples in level sets of completely multiplicative functions | 단위원 값 완전 곱셈 함수 유한 개에 대해 모든 값이 1에 가까운 피타고라스 삼중쌍 존재 | 초록 | |
| 2609.34676 | 2026-09-28 | J. Leng | A new proof of two-color partition regularity of Pythagorean triples | 2색 피타고라스 삼중쌍 정칙성의 새 증명. ChatGPT Astra가 증명을 찾았다고 명시 | 초록 + 서론 | AI 관여 명시. 3색 이상은 열려 있음 |
| 2407.05542 | 2024-07-08 | S. Goswami | Nonlinear Kernel Partition Regularity: Necessary and Sufficient Conditions | 라도 열 조건의 비선형 확장 | 초록 | 보조 후보 |
| 2510.19370 | 2025-10-22 | L. Luperi Baglini, A. Vegnuti | Asymptotic Ramsey theory of Diophantine equations | 점근적 분할 정칙성 개념, 부정적 결과 | 초록 | 보조 후보 |
| (배경) 2309.10636 | 2023-09-19 | Frantzikinakis, Klurman, Moreira | Partition regularity of Pythagorean pairs | 모든 유한 색칠에서 피타고라스 쌍이 단색 | 초록 + 서론 | 2023년 제출이라 후보에서 제외, 배경으로만 사용 |

대조군 관련: 이 키워드의 논문은 Erdős #28, #30, #36, #39, #52, #66, #200, #241, #324 중 어느 것도 주된 주제로 다루지 않았습니다. 다만 #200(소수 등차수열)과 달리 이 키워드는 곱셈 구조를 쓰므로, #52(합-곱)와 가까운 논문(예: 2501.17203의 A∪(A+B)∪A·B 결과)을 팩에 넣을 때는 겹침 여부를 한 번 더 보십시오.

**팩 추천.**
1. **2609.34676 (Leng).** 아직 열린 "색 3개 이상" 문제를 서론이 명시하고, 증명 자체가 AI가 찾은 것이라 이 실험의 주제와도 맞닿습니다. 다만 증명이 짧고 닫힌 결과라서, 문제를 낳는 재료는 서론의 열린 질문 쪽에 있습니다.
2. **2411.17523 (Frantzikinakis 서베이).** 열린 문제와 도전 과제를 한곳에 모았고, 철학 전공자가 최전선의 위치를 읽기에 가장 쉽습니다. 문제를 낳을 만한 질문 목록이 가장 풍부합니다.

---

## K18. 영합 문제 (zero-sum problems)

**쉬운 설명.** 숫자 여러 개를 주고 "그중 몇 개를 골라 더하면 딱 0(또는 n의 배수)이 되게 할 수 있는가"를 묻는 분야입니다. 대표 정리인 Erdős–Ginzburg–Ziv(EGZ) 정리는 정수 2n−1개 중에는 합이 n의 배수가 되는 n개가 항상 있다고 말합니다. 숫자를 "순환군"이나 "격자점"으로 일반화하면 필요한 개수가 얼마인지(EGZ 상수, Davenport 상수)가 문제가 됩니다. 얼마나 많이 모아야 피할 수 없는 구조가 생기는지를 재는 일이라, 램지 이론과 가까운 극한 문제입니다.

**최전선 요약.**

*2023년 이전 상태.*
- 순환군 C_n에서 EGZ 상수는 2n−1입니다(원래의 EGZ 정리).
- 평면 격자 Z_n²에서는 s(Z_n²)=4n−3입니다(Kemnitz 추측, Reiher 2007). 고차원 Z_n^d의 정확한 값은 일반적으로 모릅니다.
- C_n^r에 대해 Harborth 구성이 s(C_n^r) ≥ 2^r(n−1)+1을 주며, n이 2의 거듭제곱이면 이 값이 맞다고 알려져 있습니다(2610.35819 초록 기준).
- 고정된 차원 d에서 소수 p가 커질 때, EGZ 상수는 근사적으로 p 곱하기 "약한 EGZ 상수"입니다(Zakharov, arXiv 2002.09892, 2020. 검색 결과 요약으로만 확인한 배경).
- 랭크 3 이상 군의 Davenport 상수와 EGZ 상수의 정확한 값은 대부분 미결입니다(검색 결과에서 Girard–Schmid 2018 논문의 서술을 확인한 수준).

*2024–2026에 바뀐 것.*
- **Property C, D 반증.** Wang–Zeng(2610.25271, 2026-10-18)은 모든 r ≥ 4와 모든 짝수 n에 대해, 두 성질이 "n이 2의 거듭제곱일 때에만" 성립함을 보였습니다. 그 결과 2007년 Gao–Hou–Schmid–Thangadurai의 Property C 질문에 부정으로 답하고, 2006년 Gao–Geroldinger의 Property D 추측을 반증합니다(초록 기준). 쉬운 말로, "가장 긴 영합 회피 수열은 한 가지 균일한 모양이다"라는 오랜 믿음이 짝수이면서 2의 거듭제곱이 아닌 n에서 틀렸다는 뜻입니다.
- **하한이 Harborth를 넘어섬.** Elsholtz(2610.35819, 2026-10-26)는 n=2^a·m, m ≥ 3 홀수, r ≥ 4일 때 s(C_n^r) ≥ 2^r(n−1) + (m−1)·2^{r−3}·⌊r/4⌋ + 1을 보였습니다. 초과분이 2^r보다 빨리 자라 r·2^r의 상수배 이상입니다(초록 기준).
- **상계 개선.** Girard–Zotova(2510.23543, 2025-10-27)는 Reiher의 Kemnitz 증명을 변형해 rank-two-like p-군과 그 직합에서 EGZ 상수의 상계를 개선했고, 임의로 큰 랭크를 갖는 새로운 무한 족에서 정확한 값을 정하며 Gao의 추측을 확인했습니다(초록 기준).
- **비가환군.** Zhao–Wang(2603.21052, 2026-03-22)은 위수가 4로 나누어지지 않는 비순환 군에서 Gao–Li(2010) 추측 E(G) ≤ 3n/2를 증명하고, 등호 군이 "지표 2인 순환 부분군을 갖는 군"임을 밝혔습니다. Qu–Wang–Li(2608.15568, 2026-08-16)는 비가환군의 Gao 추측형 등식 s(G)=η(G)+exp(G)−1을 지표 p인 순환 부분군을 갖는 군에 대해 증명했습니다(둘 다 초록 기준).
- **알고리즘.** Jo(2605.21753, 2026-05-20)는 정수 2n−1개에서 합이 n의 배수인 n개를 O(n) 시간(선형)에 결정적으로 찾는 알고리즘을 주었습니다. 기존에는 O(n log n), O(n log log log n)이었습니다(초록 기준).
- **Davenport 상수 변형.** Zhong(2503.21231, 2025-03-27)은 랭크 2 군에서 D_k(C_{n1}⊕C_{n2}) = n1 + k·n2 − 1(이미 알려진 값)이 되는 임계 길이의 영합 수열 중, 서로소인 영합 부분수열 k+1개로 쪼개지지 않는 것을 특징짓습니다(역문제, 초록 기준).
- Z.-W. Sun(2606.18234, 2026-06-16)은 "0 아닌 n의 배수가 아닌 정수 2n−1개 중 합이 n의 배수이되 n²의 배수는 아닌 길이 n 이하의 부분집합이 있다" 등 새 유형의 영합 문제와 추측들을 제시합니다(초록 기준).

**남은 경계.**
1. Property C, D가 n이 2의 거듭제곱이 아닌 경우에 틀렸다면, C_n^r의 EGZ 상수의 참값은 무엇인가. Elsholtz(2610.35819)가 "초과분이 2^r보다 빨리 자란다"고 했을 뿐 정확한 값은 열려 있습니다.
2. 비순환 군에서 E(G) ≤ 3n/2를 위수가 4의 배수인 경우까지 증명할 수 있는가(Gao–Li 추측의 나머지 부분, 2603.21052 초록의 "위수가 4로 나누어지지 않는" 조건 바깥).
3. 랭크 3 이상의 군에서 η, s, Davenport 상수의 정확한 값. Girard–Zotova는 "Gao의 추측을 새로운 무한 족에서 확인"한 것이지 일반 증명이 아닙니다(2510.23543).
4. Sun이 2606.18234에서 제시한 sr(n), tr(n) 계열 추측들. 컴퓨터로 작은 n을 확인할 수 있는 형태여서 checkable 문제로 바꾸기 쉽습니다.

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2610.25271 | 2026-10-18 | G. Wang, X. Zeng | Inverse Zero-Sum Problems of Erdős–Ginzburg–Ziv constant: Property C and Property D conjectures | r ≥ 4, n 짝수에서 Property C, D가 성립할 필요충분조건은 n이 2의 거듭제곱임. 2006년 추측 반증 | 초록 | 가장 최근의 반증 결과 |
| 2610.35819 | 2026-10-26 | C. Elsholtz | The Erdős–Ginzburg–Ziv constant of C_n^r for even n: rigid sequences, products, and growth beyond Harborth's bound | s(C_n^r)의 새 하한. 초과분이 r·2^r 규모 | 초록 | 위 논문의 직접 후속 |
| 2510.23543 | 2025-10-27 | B. Girard, S. Zotova | The Erdős–Ginzburg–Ziv constant of rank-two-like p-groups | Reiher 방법으로 상계 개선, 무한 족에서 Gao 추측 확인 | 초록 | |
| 2603.21052 | 2026-03-22 | Y. Zhao, G. Wang | The Erdős–Ginzburg–Ziv theorem constant of finite groups | 비순환군에서 E(G) ≤ 3n/2 (위수가 4로 나누어지지 않을 때) | 초록 | |
| 2608.15568 | 2026-08-16 | Y. Qu, G. Wang, Y. Li | The equality between the Erdős–Ginzburg–Ziv constant and the short product-one constant for finite nonabelian groups | 비가환군의 Gao 추측형 등식 일부 증명 | 초록 | |
| 2605.21753 | 2026-05-20 | S. Jo | Finding a Solution to the Erdős–Ginzburg–Ziv Theorem in Linear Time | EGZ 해를 선형 시간에 찾는 알고리즘 | 초록 | cs.DS 교차 분류 |
| 2503.21231 | 2025-03-27 | Q. Zhong | On the inverse problem of the k-th Davenport constants for groups of rank 2 | D_k 임계 길이 영합 수열의 구조 | 초록 | |
| 2606.18234 | 2026-06-16 | Z.-W. Sun | On zero-sum problems of new types | 새 유형의 영합 문제와 추측 | 초록 | |

대조군 관련: 해당 없음(Erdős 대조군 번호와 겹치는 논문 없음).

**팩 추천.**
1. **2610.25271 (Wang–Zeng)**. 오래된 추측 두 개를 실제로 반증해, "믿어 온 모양이 틀렸다"는 최전선의 성격이 선명합니다. 무한한 r과 n 전체에 걸친 진술이라 AI가 변형 문제를 만들 여지가 큽니다.
2. **2610.35819 (Elsholtz)**. 위 반증을 정량화한 직접 후속이어서 두 논문을 함께 읽으면 "이전 최고 → 반증 → 새 하한 → 남은 간극"이 한눈에 보입니다. 구체적 수열 구성이 있어 작은 (n, r)에서 컴퓨터 검증 가능한 문제(checkable)로 만들기 쉽습니다. 선정 시 두 논문 모두 2026년 10월 제출이라 아직 심사 전이라는 점을 감안하십시오.

---

## K19. 확대 합집합과 제한 합집합 (sums of dilates, restricted sumsets)

**쉬운 설명.** 유한한 숫자 집합 A가 있을 때, A의 모든 원소 쌍을 더해 만든 집합 A+A가 얼마나 작을 수 있는지를 묻는 것이 합집합 문제입니다. "확대 합집합" A+λ·A는 두 번째 항에 상수 λ를 곱해서 더하는 변형이고, "제한 합집합"은 서로 다른 원소끼리만 더하는 변형(Erdős–Heilbronn)입니다. 곱하는 수나 더하는 방식을 조금만 바꿔도 합집합의 최소 크기가 완전히 달라지고, 그 정확한 값을 구하는 것이 어렵습니다. 소수 p를 법으로 하는 세계(Cauchy–Davenport 정리)와 정수·복소수 세계가 서로 다른 모습을 보입니다.

**최전선 요약.**

*2023년 이전 상태.*
- Cauchy–Davenport: 소수 p에 대해 Z_p의 부분집합 A, B의 합집합 크기는 최소 min(|A|+|B|−1, p)입니다.
- Erdős–Heilbronn 추측(서로 다른 원소끼리의 합집합 크기가 최소 min(2|A|−3, p)): Dias da Silva–Hamidoune(1994)이 증명했고 Alon–Nathanson–Ruzsa가 다항식 방법으로 간단히 다시 증명했습니다. Erdős 문제 #476으로도 올라 있고 이미 해결 표시입니다.
- 확대 합집합: Bukh(2008)가 정수 집합에서 |A+3·A| ≥ 4|A|−O(1)을 보였고, 서로소 정수 λ₁,…,λ_k에 대해 |λ₁A+…+λ_kA|가 (|λ₁|+…+|λ_k|)|A|−O(1) 이상임이 Shakan(2014)에 알려졌습니다(둘 다 검색 결과 요약으로 확인한 배경).

*2024–2026에 바뀐 것.*
- **복소수, 대수적 확대.** Conlon–Lim(2508.18586, 2025-08-26)은 A가 복소수의 유한 부분집합이고 λᵢ가 대수적 수일 때 |A+λ₁A+…+λ_kA|의 하한을 "최선"이라 부르는 명시적 상수 곱하기 |A|(+저차항)로 줍니다. 증명은 R^d의 콤팩트 집합에 대한 선형변환 합의 측도 하한, 확대 합에 맞춘 Freiman 정리, 격자 밀도 분석을 결합하고, 응용으로 두 선형변환의 합에 대한 점근적 최적 하한을 얻습니다(초록 기준).
- **소수 위수군에서.** Conlon–Lim(2409.17112, 2024-09-25)은 Z_p의 밀도 α인 부분집합 A에 대해 A+λ·A가 얼마나 작을 수 있는지를, α를 고정하고 λ가 커질 때 "거의 최적"으로 결정합니다(초록 기준, 구체적 수치는 읽지 못함).
- **제한 합집합의 일반화.** Ouyang(2503.09121, 2025-03-12)은 Lev의 추측(관계 R이 대응(matching)이고 |A|+|B| ≤ p면 제한 합집합이 최소 |A|+|B|−3개)을 |A|+|B| ≤ (1−ε)p이고 p가 충분히 클 때 증명했습니다. 증명은 Bollobás–Leader–Tiba와 Green–Ruzsa의 정류성(rectifiability) 논증 위에 서 있습니다. 또한 크기 약 6p/11인 A로, 어떤 대응에 대한 자기 제한 합집합의 크기가 p−3이 되는 예를 만들어, 관계가 "같음"일 때(고전적 Erdős–Heilbronn)보다 훨씬 작은 합집합이 가능함을 보였습니다(초록 기준).
- **임의의 유한 아벨군.** Du–Pan(2403.03549, 2024-03-06)은 위수가 합성수인 일반 유한 아벨군 G에서 서로 다른 k개 원소의 합으로 이루어진 제한 k-겹 합집합의 크기가 min(G의 최소 소인수, k|A|−k²+1) 이상임을 보였습니다(초록 기준). Dias da Silva–Hamidoune 정리의 아벨군 일반화입니다.
- 임계 수 분류(Chen–Huang, 2602.10402, 2026-02-11): 제한 합집합과 관련된 임계 밀도를 짝수 위수 군에서는 정확히 정하고(|G|/2+1), 홀수 위수에서는 범위를 주며, 타원곡선 MDS 부호 추측에 응용합니다(초록 기준).
- 색 분할과 제한 자기 합집합(Irawan, 2509.20568, 2025-09-24): 순환군 Z_n을 k개 색 부류로 쪼갤 때의 제한 2-겹 합집합 극값 문제로, 소수 n에서는 정확한 최소값을 구했습니다(초록 기준).

**남은 경계.**
1. Lev 추측을 |A|+|B| ≤ p 전체로(ε 손실 없이) 증명할 수 있는가. 2503.09121은 |A|+|B| ≤ (1−ε)p까지만 증명합니다.
2. 확대 합 A+λ·A의 Z_p에서의 정확한 최소 크기. 2409.17112는 "α 고정, λ 큰" 영역에서 거의 최적이라고 했을 뿐 전 영역은 아닙니다.
3. 복소수 이외의 환(예: 초월 확대)이나 다변수 선형변환 합으로의 확장. 2508.18586은 대수적 λ에서 "최선인 상수"를 줍니다.
4. 홀수 위수 군의 제한 합집합 임계 수의 정확한 값. 2602.10402가 짝수 위수에서만 정확한 값을 줍니다.

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2508.18586 | 2025-08-26 | D. Conlon, J. Lim | Sums of algebraic dilates | 복소수 집합에서 A+λ₁A+…+λ_kA의 "최선" 하한(대수적 λ) | 초록 | 확대 합집합의 현재 최전선 |
| 2409.17112 | 2024-09-25 | D. Conlon, J. Lim | Sums of dilates over groups of prime order | Z_p에서 A+λA의 근사 최적 하한(α 고정, λ 큼) | 초록 | |
| 2503.09121 | 2025-03-12 | M. Ouyang | On restricted sumsets with bounded degree relations | Lev 추측을 (1−ε)p까지 증명, 6p/11 반례류 | 초록 | 제한 합집합의 열린 질문이 명시적 |
| 2403.03549 | 2024-03-06 | S. Du, H. Pan | The restricted sumsets in finite abelian groups | 일반 유한 아벨군으로 Dias da Silva–Hamidoune 확장 | 초록 | |
| 2602.10402 | 2026-02-11 | B. Chen, J. Huang | Critical Numbers for Restricted Sumsets: Rigidity and Collapse in Finite Abelian Groups | 제한 합집합 임계 수, 짝수 위수 정확값 | 초록 | |
| 2509.20568 | 2025-09-24 | K. M. Irawan | Judicious partitions for restricted self-sumsets in cyclic groups | 색 분할 아래 제한 자기 합집합의 극값 | 초록 | 보조 후보 |
| (배경) 2204.07559 | 2022 (검색 결과) | B. Bollobás, I. Leader, M. Tiba | Large sumsets from small subsets | Erdős–Heilbronn의 확장, Israel J. Math. 2025 게재 | 검색 결과 요약만 | 2022년 제출이라 후보에서 제외, 배경 |

대조군 관련: 해당 없음. 단 Erdős #52 (합-곱)는 이 키워드의 합집합 크기 문제와 같은 부류이므로, 곱셈이 섞인 논문을 고르면 겹칠 수 있습니다. 위 후보들은 모두 덧셈만 다룹니다.

**팩 추천.**
1. **2508.18586 (Conlon–Lim).** 확대 합집합의 "최선인 상수"를 주는 가장 최근의 최전선이며, 세 갈래 도구(측도, Freiman, 격자 밀도)가 한 논문에 모여 있어 문제를 낳을 재료가 많습니다. 대조군과 겹치지 않습니다.
2. **2503.09121 (Ouyang).** 제한 합집합에서 "Lev 추측을 어디까지 증명했는가"가 구체적 수치(1−ε, 6p/11, p−3)로 적혀 있어 최전선의 위치가 분명하고, 남은 구간이 곧 열린 문제입니다.

---

## K20. erdosproblems.com 가법 조합론 태그의 2024–2026 해결 사례 (AI 관여 포함)

**쉬운 설명.** erdosproblems.com은 Paul Erdős가 남긴 미해결 문제 1200여 개를 Thomas Bloom이 모은 사이트입니다. 문제마다 "가법 조합론", "시돈 집합", "가법 기저", "등차수열" 같은 태그가 붙어 있습니다. 2025년 후반부터 사람 수학자뿐 아니라 AI가 풀거나 일부를 해결한 문제가 이 사이트와 Terence Tao의 위키에 기록되고 있습니다. 이 절은 네 태그 문제 중 이 기간에 상태가 바뀌었거나 진전이 있었던 것을 모아, 해결 논문과 AI 관여 여부를 구분한 것입니다.

**조사 방법과 한계.**
- `problems.yaml`(1221개 문제)에서 네 태그 중 하나라도 붙은 문제는 154개였습니다(additive combinatorics 103, sidon sets 34, additive basis 31, arithmetic progressions 29, 중복 포함). 상태는 열림 77(Lean 형식화 중 1개 포함), 해결 계열 77입니다(2026-11-06 기준 내려받은 파일).
- **주의: yaml의 `last_update`는 믿을 수 없습니다.** 많은 항목이 데이터베이스 기준일인 2025-08-31로 되어 있습니다. #1은 yaml에 2025-08-31로 되어 있지만 실제 페이지는 2026-09-03에 편집되었고 GPT-6 Astra에 의한 반증이 적혀 있습니다. 그래서 각 문제의 페이지 본문과 "last edited" 날짜를 직접 읽었습니다(154개 전부 내려받아 읽음).
- **해결 표시가 곧 새 증명은 아닙니다.** 사이트에서 "해결"로 바뀐 문제 상당수는 오래된 문헌에서 이미 풀려 있었음이 뒤늦게 확인된 경우입니다(예: #333은 Erdős–Newman 1977, #339는 Hegyvári–Hennecart–Plagne 2003, #818은 Solymosi, #1187은 Green–Tao, #1193은 자명한 반례, #862는 Saxton–Thomason, #863은 Ho와 GPT-5.4 Pro가 문헌 논증으로 확인). 이런 사례는 "2024–2026 새 결과"에서 제외했습니다. Quanta(2026-08-03)도 #333에 대해 Barreto와 Price의 AI 증명(2025-12-25)이 1977년 논문에 이미 있었다고 보도했습니다.
- 사이트 본문은 참고문헌을 `[Hu25b]`처럼 약칭으로만 적고 링크는 붙이지 않아서(HTML에 arXiv 링크 0개), arXiv 번호는 검색과 arXiv 초록 페이지로 따로 찾았습니다. 찾지 못한 것은 `[미확인]`입니다.
- Tao 위키(`AI-contributions-to-Erdős-problems`)는 2026-06-30 기준으로 더 이상 갱신되지 않는다고 적혀 있습니다. 이후(6월 말–9월) 사례는 erdosproblems.com 페이지에서 직접 읽었습니다.

**최전선 요약. 새 결과가 확인된 사례(2024–2026), 대조군 제외.**

*(A) 사람 주도, AI는 형식화 또는 보조.*
- **#707 ($1000, 시돈 집합).** "모든 유한 시돈 집합은 어떤 유한 완전 차집합(perfect difference set)에 포함되는가"에 대해 Alexeev–Mixon(arXiv 2510.19804, 2025-10-22)이 반증했습니다. {1,2,4,8,13}은 어떤 완전 차집합으로도 확장되지 않으며, Marshall Hall Jr.가 1947년에 이미 다른 반례를 냈음을 뒤늦게 발견했습니다. ChatGPT로 Lean 형식화를 했다고 논문이 밝힙니다. 사이트 본문은 {1,2,4,8}이 p²+p+1 꼴 법의 완전 차집합으로 확장되지 않는다고 적었습니다. 남은 질문: 크기 4인 시돈 집합이 확장 가능한가(사이트는 {0,1,3,11}을 반례 후보로 적음).
- **#190 (정준 반 데르 바르덴 H(k)).** 사이트 본문: Hunter [Hu25b]의 점화식이 H(k)^{1/k}→∞를 함의했고, Bae [Ba26]가 H(k) ≥ k^{(2−o(1))k}, Fox–Hunter [FoHu26]가 독립적으로 H(k) ≥ k^{(1−o(1))k log k}를 얻었습니다. Fox–Hunter는 arXiv 2606.02541(2026-06-01)이며, 같은 논문이 3색 반 데르 바르덴 수 w(k;3)가 지수보다 빨리 증가함(2^{k·log* k/4} 근방의 3색칠하기)도 보입니다. 사이트 본문과 arXiv 초록에서 AI 관여는 언급되지 않았습니다.
- **#475 (Graham 재배열 추측, "valid ordering").** 충분히 큰 소수 p에서 해결됨. 네 구간으로 나뉘어 해결: 아주 작은 집합(Kravitz, arXiv 2407.01835, 2024-07-01, |A| ≲ log p / log log p), 작은 집합(Bedert–Kravitz, 2409.07403, 2024-09-11, exp((log p)^{1/4})), 중간(Pham–Sauermann, 2602.15797, 2026-02-17, p^{1−α} 이하의 충분히 큰 집합), 큰 집합(Bedert–Bucić–Kravitz–Montgomery–Müyesser, 2508.18254, 2025-08-25, |G|^{1−c} 이상). Costa–Della Fiore(2602.19989, 2026-02-23)는 순환군 Z_k에서 exp((log p)^{1/3})으로 개선했습니다. 모두 사람의 논문이며 AI 관여가 언급되지 않았습니다. 사이트 상태는 `decidable`로 표시되어 있습니다.
- **#29 ($100, 명시적 가법 기저).** A+A=N이고 모든 ε>0에서 표현 수 1_A*1_A(n)=o(n^ε)인 "명시적" 집합. Jain–Pham–Sawhney–Zakharov(arXiv 2405.08650, 2024-05-14). 표현 수 상계는 C·n^{c/log log n}. 저자들은 exp((log N)^ε) 이하의 명시적 구성이 흥미롭다고 적었습니다. 사람 논문입니다.
- **#139, #142, #3 (등차수열 없는 집합 r_k(N)).** Leng–Sah–Sawhney(arXiv 2402.17995, 2024-02-28)가 k ≥ 5에서 r_k(N) ≪ N·exp(−(log log N)^{c_k})를 증명했고, 사이트가 현재 최고로 인용합니다. 사람 논문입니다. 미해결 쪽(#3 $5000, #142 $10000)은 열려 있습니다.

*(B) AI가 풀었거나 핵심을 제공했다고 사이트에 적힌 사례.*
- **#1 ($500, 서로 다른 부분합).** 사이트 본문은 "GPT-6 Astra가 반증"이라 적고, 임의의 ε>0에 대해 N ≤ ε·2^n이 되는 서로 다른 부분합 집합이 무한히 많은 n에서 존재한다고 합니다(이전 최고는 Bohman의 0.22002·2^n, 하한은 Elkies–Gleason의 √(2/π)·2^n/√n 규모). Bloom이 직접 쓴 증명 해설(2026-09-03 편집)이 페이지에 있고, 증명은 비정량적(격자 근사의 비효과성)이라 정량 형태는 추측 수준으로 적혀 있습니다. 원 논문의 arXiv 번호는 `[미확인]`. OpenAI가 2026-08-01에 비공개 모델 Astra로 Erdős 문제 3개를 포함한 10개의 수학적 진전을 발표했다는 Quanta 보도는 있으나(문제 번호는 기사에 없음), #1이 그중 하나인지는 확인하지 못했습니다.
- **#42와 #43 (시돈 집합 쌍).** #42는 Sedov(ChatGPT와 Codex 사용)가 M=3까지, GPT 5.5 Pro(Sandhu의 프롬프트)가 모든 M에 대해 증명했다고 사이트에 적혀 있고(2026-05-10 편집), |B| ≫ (log log N / log log log N)^{1/2}까지 나온다고 합니다. 이 결과로 #43의 첫 질문은 부정적으로 답해졌고, #43의 둘째 질문은 Barreto가 부정으로 답했으며 Tao가 상계 1/√2·√N 증명을 댓글로 달았습니다. arXiv 번호 `[미확인]`.
- **#865 (Erdős–Sós, 쌍합 a+b, a+c, b+c ∈ A).** Cipollini의 arXiv 2606.29361(2026-06-28)이 f₃(N) ≤ 5N/8+O(1)을 증명했고 하한 구성과 합쳐 점근적으로 최적입니다. 사이트 본문은 "Cipollini와 GPT Pro가 해결"이라 적었고, 검색 결과의 부차 자료는 논문이 GPT-5.5 Pro로 작성되고 Aristotle로 Lean 형식화되었다고 서술합니다(논문 초록 페이지에는 AI 관여가 명시되지 않아 사이트와 부차 자료 기준). 상수 C는 판마다 다르다는 포럼 언급이 있어 판 확인이 필요합니다.
- **#871과 #868 (가법 기저에서 극소 기저 포함 여부).** #871은 Larsen이 Claude Opus 4.5를 사용해 부정으로 답했다고 사이트가 적었습니다(2026-01-06 편집). #868은 Larsen과 Larsen이 c·log n 표현 수에도 극소 기저를 포함하지 않는 기저가 있음을 보였다고 적혀 있고, 사이트 이력에서는 "preprint가 필요함"이라는 임시 표시가 있었습니다. arXiv 번호 `[미확인]`.
- **#330 (극소 기저).** GPT 5.5 Pro가 구성(Turturean의 프롬프트), 2026-05-11. arXiv `[미확인]`.
- **#198 (시돈 집합의 여집합).** AlphaProof가 명시적 시돈 집합 A={(n+1)!+n}을 찾음(2026-01). 대신 Baumgartner(1975)의 암시적 구성이 이미 있어 새 정리는 아니고, "더 명시적인 구성을 AI가 냄"에 가깝습니다.
- **#152 (시돈 합집합).** DeepMind(Lean 증명)가 |A|² 이상의 원소 수까지 증명했다고 사이트가 적었습니다(2026-05-17 편집). arXiv 번호 `[미확인]`(DeepMind의 2605.22763 논문이 353개 중 9개의 Erdős 문제를 자율 해결했다고 보고하지만, 어떤 문제인지는 초록에 없어서 이 문제가 포함되는지 확인하지 못했습니다).
- **#138 (반 데르 바르덴 W(k), 현재 "열림").** DeepMind가 W(k+1) ≥ W(k)+k를 증명(사이트 본문, 댓글 참조), r ≥ 3색에서는 Fox–Hunter가 W_r(k)^{1/k} 하한을 해결(2606.02541).
- **#847 (3-AP 없는 부분집합 분할).** Reiher–Rödl–Sales(arXiv 2311.08556, 2023-11)가 부정으로 답했습니다. v1이 2023년이라 배경으로만 둡니다. 사이트에는 AI가 이를 먼저 지적했다는 포럼 언급이 있으나 미검증입니다.

*(C) 그 밖에 이 기간 진전이 확인된 열린 문제(해결 표시 아님).*
- #169(Walker 2025), #335(Ackelsberg–Richter 2026), #757(Ma–Tang 2026), #787(Beker 2025), #788(Alon–Pham 2025), #792(Bedert 2025), #1206(Gabdullin–Konyagin 2024, Garaev–Garayev–Konyagin 2026), #749, #1194(GPT-5 계열의 부분 결과). 개별 arXiv 번호는 이번 조사에서 열어 보지 않았습니다 `[미확인]`.
- 같은 흐름에서 Ma–Tang(arXiv 2602.05768, 2026-02-05)이 #543(무작위 부분합, 태그는 number theory와 group theory)에서 Erdős의 추측을 소수 위수에서 증명했습니다(초록 기준, AI 관여는 초록에 없음. 검색 결과 부차 자료는 ChatGPT-5.2 Pro의 반례 제안이 출발점이었다고 서술). 이 문제는 이번 네 태그에는 들지 않아 참고로만 둡니다.

**AI 관여 전반 (과정 논문).**
- Feng 외 24인(arXiv 2601.22401, 2026-01-29, "Semi-Autonomous Mathematics Discovery with Gemini"): 열림으로 표시된 700개를 Gemini로 검토, 13개 중 5개는 새로운 자율 해결, 8개는 기존 문헌과 일치. 어려워서가 아니라 알려지지 않아서 열려 있었다는 결론(초록 기준).
- Tsoukalas 외(arXiv 2605.22763, 2026-05-21, "Advancing Mathematics Research with AI-Driven Formal Proof Search"): 353개 열린 Erdős 문제 중 9개를 자율 해결(초록 기준).
- Tao 위키(2026-06-30 기준): 독립 AI 기여 표 약 55줄, 문헌 대조 약 100건, 형식화 약 150건 등. 완전 해결(Full)로 기록된 가법 조합론 사례는 #38 (GPT-5.5 Pro), #1051 (Aletheia), #205, #457 등입니다(번호는 위키 표 기준, 이 중 #38 등은 태그를 따로 확인하지 못함).

**대조군 번호 처리.** 요청된 제외 목록(#28, #30, #36, #39, #52, #66, #200, #241, #324) 중 이 기간 진전이 확인된 것은 다음과 같고, 모두 후보에서 제외했습니다.
- #30(시돈 집합 최대 크기): Carter–Hunter–O'Bryant [CHO25]가 상계 상수를 개선. 제외.
- #36(최소 겹침): TTT-Discover LLM [YKLBMWKCZGS26]이 상계를 개선, 이전에 AlphaEvolve [GGTW25]. 제외.
- #52(합-곱): Cushman [Cu25]가 지수 1962/1469를 얻었고, Bloom–Sawin–Schildkraut–Zhelezov [BSSZ26]가 실수에서 합-곱 추측을 반증(Quanta가 arXiv 2605.28781로 보도, 직접 열어 보지 않음). Tao 위키는 Claude Mythos의 변형 기여도 기록. 제외.
- #28, #39, #66, #200, #241, #324는 이 기간 진전을 따로 찾지 못했고, 열어 본 범위에서 후보로 삼지 않았습니다.
- 팩 후보에서 이 번호들과 겹치는 것은 없습니다. 단 #190, #138 (Fox–Hunter)은 #200 (소수 등차수열)과는 무관합니다.

**남은 경계.**
1. #707: 크기 4인 시돈 집합이 모두 완전 차집합으로 확장되는가 (Alexeev–Mixon, 2510.19804, 사이트의 "open" 서술).
2. #190, #138: H(k)와 W(k)의 상한. 하한만 k^{(1−o(1))k log k} 규모로 올라갔을 뿐 상한은 크게 벌어져 있습니다.
3. #1: Astra의 구성이 비정량적이라, 사이트가 추측하는 n^{−c/log log n} 형태의 정량 개선이 가능한가. 하한 f(n) ≫ n^{−1/2}와의 간극도 남습니다.
4. #475: 소수가 아닌 일반 순환군과 일반 아벨군에서의 Graham–Alspach 추측(2602.19989가 "일반 아벨군은 열려 있다"고 서술).

**후보 논문.**

| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2510.19804 | 2025-10-22 | B. Alexeev, D. G. Mixon | Forbidden Sidon subsets of perfect difference sets, featuring a human-assisted proof | Erdős #707($1000) 반증, ChatGPT로 Lean 형식화 | 초록 | AI는 형식화 보조. 사람 주도 |
| 2606.02541 | 2026-06-01 | J. Fox, Z. Hunter | Three-color van der Waerden numbers grow super-exponentially | #190, #138의 3색 이상 해결, 정준 반 데르 바르덴 하한 | 초록 | 사이트와 arXiv 초록에서 AI 관여 언급 없음 |
| 2602.15797 | 2026-02-17 | H. T. Pham, L. Sauermann | On Graham's rearrangement conjecture | #475 중간 크기 집합 해결, 충분히 큰 p에서 완결 | 초록 | 사람 논문 |
| 2508.18254 | 2025-08-25 | B. Bedert, M. Bucić, N. Kravitz, R. Montgomery, A. Müyesser | On Graham's rearrangement conjecture over F_2^n | #475 큰 집합(|G|^{1−c} 이상) 해결 | 초록 | 제목은 F_2^n이나 임의 유한군의 결과도 포함. 사이트는 이 번호를 큰 집합 구간으로 인용 |
| 2409.07403 | 2024-09-11 | B. Bedert, N. Kravitz | Graham's rearrangement conjecture beyond the rectification barrier | #475 작은 집합 exp((log p)^{1/4}) | 초록 | |
| 2407.01835 | 2024-07-01 | N. Kravitz | Rearranging small sets for distinct partial sums | #475 아주 작은 집합 log p / log log p | 초록 | |
| 2602.19989 | 2026-02-23 | S. Costa, S. Della Fiore | New bounds for (weak) sequenceability in Z_k | 순환군에서 exp((log p)^{1/3})로 개선 | 초록 | |
| 2405.08650 | 2024-05-14 | V. Jain, H. T. Pham, M. Sawhney, D. Zakharov | An explicit economical additive basis | #29 명시적 구성, 표현 수 ≤ C·n^{c/log log n} | 검색 결과 요약(arXiv 초록 직접 열람은 못함) | 사람 논문 |
| 2606.29361 | 2026-06-28 | R. Cipollini | A sharp 5/8 bound for an Erdős–Sós pairwise-sums problem | #865 해결 (f₃(N) ≤ 5N/8+O(1)) | 초록 | 사이트와 부차 자료는 GPT-5.5 Pro 관여, arXiv 초록은 AI 언급 없음. 판별 변동 있음 |
| 2402.17995 | 2024-02-28 | J. Leng, A. Sah, M. Sawhney | Improved Bounds for Szemerédi's Theorem | k ≥ 5에서 r_k(N) ≪ N exp(−(log log N)^{c_k}) | 초록 | #3, #139, #142 관련. 사람 논문 |
| 2601.22401 | 2026-01-29 | T. Feng 외 | Semi-Autonomous Mathematics Discovery with Gemini: A Case Study on the Erdős Problems | Gemini로 열린 문제 700개 검토, 5개 새 해결 | 초록 | AI 관여 과정 논문 |
| 2605.22763 | 2026-05-21 | G. Tsoukalas 외 | Advancing Mathematics Research with AI-Driven Formal Proof Search | Lean 기반 에이전트가 353개 중 9개 자율 해결 | 초록 | AI 관여 과정 논문 |
| (#1, #42, #43, #152, #330, #868, #871) | [미확인] | 사이트 기재: GPT-6 Astra, GPT 5.5 Pro, DeepMind, Larsen 등 | | 위 본문 참조 | erdosproblems.com 페이지 | arXiv 원 논문 `[미확인]` |

대조군 관련: #30, #36, #52를 주로 다루는 논문(Carter–Hunter–O'Bryant, TTT-Discover, Bloom–Sawin–Schildkraut–Zhelezov 등)은 위 표에 넣지 않았고 `대조군 관련: 팩 제외 권고`입니다.

**팩 추천.**
1. **2510.19804 (Alexeev–Mixon).** $1000 상금이 걸린 Erdős 시돈 집합 추측을 반증한 사람 주도의 논문입니다. 왜 오래 열려 있었는지, 반례가 얼마나 작은 집합(5개 원소)인지, AI가 형식화에만 쓰였다는 점이 한눈에 보입니다. 대조군(#30, #39, #324)과 같은 "시돈" 계열이지만 최대 크기 문제가 아니라 "확장 가능성" 문제라 겹치지 않습니다. 남은 질문(크기 4 시돈 집합)이 구체적입니다.
2. **2606.02541 (Fox–Hunter).** 이 기간에 풀리거나 크게 진전된 등차수열 문제(#190, #138)를 한 논문이 설명하고, 서론에 Erdős–Graham 질문과의 관계가 적혀 있습니다. 대조군 #200(소수 등차수열)과는 다릅니다.
대안: Pham–Sauermann(2602.15797)은 한 추측이 여러 논문에 걸쳐 단계적으로 해결된 과정을 보여 주므로, "최전선이 어떻게 움직이는가"를 보려면 적합합니다. AI가 관여한 사례를 반드시 넣으려면 #865의 2606.29361을 쓰되, AI 관여 서술이 판마다 다르다는 점을 감안하십시오.
