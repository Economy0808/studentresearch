# 가법 조합론 최전선 조사: 그룹 1

조사 날짜: 2026-11-06

맡은 키워드:
- K1. 3항 등차수열의 밀도 한계 / 로스 정리 정량화 (3-term progressions, Roth bounds)
- K2. 세메레디 정리의 정량적 한계 (Szemerédi's theorem, k-term progressions bounds)
- K3. 고워스 노름 역정리의 정량화 (quantitative inverse theorems for Gowers norms)
- K4. 코너 문제와 다차원 세메레디 (corners problem, multidimensional Szemerédi)

방법과 한계 (먼저 읽어 주세요):
- 모든 후보는 arXiv 초록 페이지(https://arxiv.org/abs/<ID>)를 열어 번호, 저자, 제목, 첫 제출일(v1)을 옮겨 적었습니다.
- WebFetch 도구는 페이지를 작은 모델로 요약해 돌려주므로, 초록 원문은 "의역"으로 받은 경우가 많습니다. 아래 부등식과 지수는 논문 HTML 본문에서 도구가 "정확히 인용"했다고 돌려준 것만 적었고, 그렇지 않은 것은 `[요약 경유]`로 표시했습니다. 수치를 논문에 인용하기 전에는 원문 PDF로 한 번 더 확인하길 권합니다.
- "읽은 범위" 표기: 초록 = 초록 페이지, 서론(HTML) = HTML 본문 앞부분 약 10만 자를 도구가 요약한 것(전체가 아님).
- 대조군 Erdős 문제(#28, #30, #36, #39, #52, #66, #200, #241, #324)를 주로 다루는 논문은 이 그룹 후보에 없습니다. 그래서 `대조군 관련` 표시는 아래에 쓰지 않았습니다. 다만 K4의 skew corner 논문이나 K2의 #200(소수 등차수열 길이)과 이름이 비슷한 항목이 섞이지 않았는지 사용자가 한 번 더 보면 좋습니다.

---

## K1. 3항 등차수열의 밀도 한계 / 로스 정리 정량화 (Roth's theorem, 3-term progressions)

**쉬운 설명.** 1부터 N까지의 수 중에서 "세 수가 같은 간격으로 늘어선 것(예: 3, 7, 11)"이 하나도 없도록 최대한 많이 고르면 몇 개까지 고를 수 있느냐는 질문입니다. 로스(1953)는 "충분히 큰 N에서는 전체의 일정 비율 이상을 고르면 반드시 그런 세 수가 생긴다"는 것을 보였고, 이후 70년간 그 "일정 비율"이 N이 커질수록 얼마나 빠르게 0에 가까워지는지를 정밀하게 재 왔습니다. 위쪽 한계(이만큼 넘으면 반드시 생김)와 아래쪽 한계(이만큼은 실제로 피할 수 있음) 사이의 간격이 이 분야의 "최전선"이며, 이 간격이 좁아질수록 "수에 얼마나 많은 질서가 숨어 있는가"를 정확히 알게 됩니다.

**최전선 요약.** r_3(N)을 "1..N에서 3항 등차수열 없이 고를 수 있는 최대 개수"라 합니다.

2023년 이전 상태:
- 위쪽: 로스 (1953) O(N/log log N)에서 시작해 Bloom–Sisask (2020, arXiv:2007.03528)의 r_3(N) ≪ N/(log N)^{1+c}까지 "N 나누기 로그의 거듭제곱" 꼴이었습니다. (arXiv:2603.27045 서론에서 확인한 서술)
- 아래쪽: Behrend (1946)의 r_3(N) ≥ N·2^{−(2√2+o(1))√(log₂N)}. 70여 년간 지수의 상수만 미세 조정(Elkin 등)되었습니다.

2023–2026에 바뀐 것:
- 위쪽 (2023): Kelley–Meka가 r_3(N) ≤ N·exp(−Ω((log N)^{1/12})), Bloom–Sisask가 지수를 1/9로 개선했습니다. "로그 장벽"이 무너져 "준다항식(quasipolynomial)" 수준이 되었습니다. 뜻: 고를 수 있는 비율이 N^(-작은 수)에 가깝게 급격히 줄어든다는 것. (2023년 결과이므로 배경으로만 사용)
- 위쪽 (2026, 이 조사의 핵심): Raghavan이 지수를 1/9에서 1/6으로 올렸다고 주장합니다. 초록: |A| ≤ exp(−c·(log N)^{1/6}·(log log N)^{−1})·N (arXiv:2603.27045, 초록 v3 확인). 방법: Kelley–Meka의 "sifting"을 반복하는 변형 + Bloom–Sisask의 개선된 Croot–Sisask 거의 주기성 부트스트랩. 유한체 F_q^n에서는 지수 1/5를 얻지만 이미 다항식 방법(Ellenberg–Gijswijt)이 더 좋아 새롭지 않다고 저자가 적었습니다.
  - 확인 필요: v3 초록은 구간 {1..N}이라 쓰는데, v1 HTML 서론의 정리 1.4는 Z/NZ(odd N)에서 exp(−log(N)^{1/6−o(1)})로 적혀 있습니다. 구간 {1..N}에서 정말 1/6이 성립하는지(초록 기준) 혹은 Z/NZ에서만인지(본문 기준)는 최신 PDF에서 사용자가 확인해야 합니다. 이 불일치를 해소하지 못했습니다.
- 아래쪽 (2024): Elsholtz–Hunter–Proske–Sauermann (arXiv:2406.12290)이 Behrend 이후 처음으로 상수 개선을 넘어서는 구성을 냈습니다. 정리 1.1: r_3(N) ≥ N·2^{−(C+o(1))√(log₂N)}, C = 2√(log₂(24/7)) < 2√2. 핵심은 2차원 판 위에서 밀도 7/24인 "재귀 가능한" 집합(기존 1차원 방식의 (1/2)²=1/4를 능가)을 쓴 것입니다. 유한체에서는 정리 1.2: r_3(F_p^n) ≥ (cp)^n, c > 1/2 (1940년대부터 c=1/2이 한계였음). 선행 논문 arXiv:2401.12802(Elsholtz–Proske–Sauermann, c=0.54)와 Hunter의 arXiv:2401.16106은 이 논문과 합쳐졌습니다.
- 뜻: 위쪽 지수 1/6 대 아래쪽 지수 1/2 사이가 여전히 벌어져 있습니다 (지수 기준 격차 1/6 vs 1/2).

**남은 경계.**
1. 위쪽 지수를 Behrend의 1/2에 맞출 수 있는가. Raghavan(arXiv:2603.27045)은 Bohr 집합 밀도 증가로 1/2+o(1)에 이르는지 모르며, 정수 경우와 유한체 경우 사이에서 로그 두 번을 잃는 것이 장벽이라고 서술합니다.
2. 아래쪽 구성의 상수 개선. arXiv:2406.12290은 "상수 7/24는 2차원 재료 집합 T를 더 잘 고르면 개선될 가능성이 있다(plausible)"고 적었습니다. (본문을 도구가 요약한 문장)
3. F_p^n에서 하한 c(>1/2, 약 0.54)와 상한(Ellenberg–Gijswijt, p→∞에서 약 0.841) 사이의 간격.
4. 작은 소수(F_3, 캡셋)의 지수 2.2180… (Tyrrell, arXiv:2209.10045, 2022 배경 자료)와 상한 2.7552… 사이 간격. 2026 새 결과는 확인하지 못했습니다.

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2603.27045 | 2026-03-27 | Rushil Raghavan | Improved Bounds for 3-Progressions | Roth 상한 지수를 1/9에서 1/6(과 log log 보정)으로 개선 주장 | 초록 + 서론(HTML v1) | 가장 최신 최전선. 초록(구간)과 본문 정리(Z/NZ)의 불일치 확인 필요. 본문 24쪽 |
| 2406.12290 | 2024-06-18 | Elsholtz, Hunter, Proske, Sauermann | Improving Behrend's construction: Sets without arithmetic progressions in integers and over finite fields | Behrend 이후 처음으로 상수를 넘어선 하한 (C=2√log₂(24/7) < 2√2) | 초록 + 서론(HTML) | 하한 쪽 최전선 |
| 2401.12802 | 2024-01-23 | Elsholtz, Proske, Sauermann | New lower bounds for three-term progression free sets in F_p^n | Z_m^n에서 (cm)^n, c=0.54 > 1/2 (Salem–Spencer 1942 돌파) | 초록 | 위 논문의 선행 |
| 2401.16106 | 2024-01-29 | Zach Hunter | New lower bounds for r_3(N) | 정수에서 준다항식 개선 하한 (v3에서 EHPS와 합병) | 초록 | 위 논문에 합쳐짐, 참고용 |
| 2501.10203 | 2025-01-17 | Adrian Beker | The Erdős–Moser sum-free set problem via improved bounds for k-configurations | Kelley–Meka류 기법을 k-배치(k-configuration)에 적용: 밀도 α 집합이 N ≥ exp((k log(2/α))^{O(1)})에서 포함 | 초록 | Erdős–Moser 문제는 대조군 목록(#28 등)에 없음. 응용 쪽 |

**팩 추천.**
- 2603.27045 (Raghavan): 상한의 현 최전선(2026년 3–5월)이고, 서론에 "1/2에 이를 수 있는가", "로그 두 번 손실" 같은 열린 질문이 직접 나옵니다. 대조군과 겹치지 않습니다. 단 위 불일치 때문에 팩에는 서론과 정리 진술을 넣고 본문 증명은 빼는 편이 안전합니다.
- 2406.12290 (EHPS): 하한 쪽 최전선이고 "7/24는 개선 가능"이라는 구체적 열린 질문이 있어 새 문제를 낳기 좋습니다.

---

## K2. 세메레디 정리의 정량적 한계 (Szemerédi's theorem, k-term progressions bounds)

**쉬운 설명.** 세 수가 아니라 k개 수가 같은 간격으로 늘어선 것(k항 등차수열)을 고르는 문제입니다. 세메레디(1975)는 "충분히 큰 수의 범위에서 일정 비율 이상을 고르면 어떤 k에 대해서든 반드시 k항 등차수열이 생긴다"고 증명했습니다. 이 분야의 질문은 "그 일정 비율이 N에 따라 얼마나 작아져야 하는가"입니다. k가 커지면 증명이 급격히 어려워져, 3항일 때는 거의 최적에 가까운 답이 있지만 5항 이상은 2024년까지 거의 25년간 개선이 없었습니다.

**최전선 요약.** r_k(N)을 1..N에서 k항 등차수열 없이 고를 수 있는 최대 개수라 합니다.

2023년 이전 상태 (2025년 Peluse 서베이 arXiv:2509.22962, 식 (2.5) 부근 서술):
- k=3: Kelley–Meka 이후 N·exp(−c(log N)^{1/12}).
- k=4: Green–Tao (2017) r_4(N) ≪ N/(log N)^c. (로그의 거듭제곱)
- k≥5: Gowers (2001) |A|/N = O(1/(log log N)^{2^{−2^{k+9}}}). 즉 "log log N의 아주 작은 거듭제곱"으로, 2024년 직전까지 최고였습니다.
- 아래쪽: Behrend 구성은 모든 k≥3에서 쓰이며, Rankin (1961) exp(−C_k(log N)^{1/⌈log k⌉}).

2024–2026에 바뀐 것:
- 2024-02 Leng–Sah–Sawhney (arXiv:2402.17995): k≥5에서 r_k(N) ≪ N·exp(−(log log N)^{c_k}), c_k ∈ (0,1). 25년 만에 Gowers 이후 첫 개선이며, 방법은 고워스 노름의 준다항식 역정리(K3의 arXiv:2402.17994) + Heath-Brown–Szemerédi 밀도 증가. c_k의 구체적 값은 논문에 없습니다(존재만 증명).
- 2025-05 Shao–Wang (arXiv:2505.16822): 다항식 세메레디 정리(서로 다른 차수, 상수항 0)에서 (log N)^{−c} 밀도면 충분하다는 "다항로그" 상한과 "인기 있는 차이(popular difference)" 판. 서론에 일반 다항식 경우는 열려 있음.
- 2025-09 Peluse 서베이 (arXiv:2509.22962): 이 흐름을 "Gowers 이후 첫 정량적 개선"이라 요약.

뜻: k≥5에서 "log log N 의 거듭제곱"에서 "exp(−(log log N)^c)" 꼴로 향상되었지만, 여전히 k=3(약 exp(−(log N)^{1/6}))이나 k=4((log N)^{−c})에 비해 훨씬 약합니다.

**남은 경계.**
1. k≥5에서 다항로그 (log N)^{−c} 이상의 상한이 성립하는가 (현재 exp(−(log log N)^{c_k})). Leng–Sah–Sawhney가 "naive 적용은 오히려 약하다"고 한 이유: 전역 역정리가 준다항식 상관만 주기 때문(arXiv:2402.17995 서론, 요약 경유). 저자가 직접 "open"이라 쓴 문장은 찾지 못했습니다.
2. 하한(Behrend/Rankin)과 상한 사이가 k≥4에서 "엄청나게 큼(massive)"(Peluse 서베이 서술).
3. 일반 다항식 세메레디 정리의 다항로그 상한 (Shao–Wang 서론: 일반 경우는 열려 있음).
4. c_k의 명시적 값.

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2402.17995 | 2024-02-28 | James Leng, Ashwin Sah, Mehtaab Sawhney | Improved Bounds for Szemerédi's Theorem | k≥5에서 r_k(N) ≪ N exp(−(log log N)^{c_k}) | 초록 + 서론(HTML) | K2의 핵심. 2001년 Gowers 이후 첫 개선 |
| 2509.22962 | 2025-09-26 | Sarah Peluse | Finding arithmetic progressions in dense sets of integers | 위 흐름의 서베이(Gowers 이후 고차 푸리에 해석 정리) | 초록 + 본문 앞부분(HTML) | 비전공자용으로 가장 읽기 좋음. 팩에 넣기 좋은 해설 |
| 2505.16822 | 2025-05-22 | Xuancheng Shao, Mengdi Wang | Quantitative bounds in a popular polynomial Szemerédi theorem | 서로 다른 차수 다항식 진행에 대한 다항로그 상한 + popular 판 | 초록 | 다항식 세메레디 쪽 최전선 |
| 2411.15137 | 2024-11-22 | Amey Bhangale, Subhash Khot, Yang P. Liu, Dor Minzer | Reasonable Bounds for Combinatorial Lines of Length Three | 밀도 (log log log log n)^{−c}면 [3]^n에서 조합적 직선 존재 (Polymath의 log* 개선) | 초록 + 서론(HTML) | 밀도 Hales–Jewett(세메레디의 조합판) 쪽. K4에도 관련 |
| 2605.06360 | 2026-05-07 | Jingwei Guo, Changxing Miao, Guoqing Zhan | A multidimensional Szemerédi theorem in integers | [N]^n에서 (log N)^{−c}면 x와 r^{m_i} 이동 배치 존재 (Peluse–Prendiville–Shao 2차원 확장) | 초록 | K4에도 관련. 요약만 읽음 |

**팩 추천.**
- 2402.17995: 정수에서 k≥5 상한의 현 최전선이고, 서론에 방법의 한계가 명시되어 있어 "무엇이 막고 있는가"를 묻는 문제를 낳기 쉽습니다.
- 2509.22962: 서베이라 앞선 결과 전체의 지도를 제공해 팩의 길잡이로 좋습니다. 대조군(#200 등)과 겹치지 않습니다.

---

## K3. 고워스 노름 역정리의 정량화 (Quantitative inverse theorems for Gowers norms)

**쉬운 설명.** 고워스 노름은 "수열이 얼마나 무작위처럼 보이는가"를 재는 자입니다. 역정리는 반대로 "무작위처럼 안 보이면(노름이 크면), 그 수열은 어떤 규칙적인 구조(다항식처럼 도는 패턴)와 닮아 있다"고 말해 줍니다. 이 역정리가 있어야 세메레디 정리를 증명할 수 있는데, 중요한 것은 "노름이 δ만큼 크면 구조와 얼마나(δ의 어떤 함수만큼) 닮는가"입니다. 이 함수가 좋을수록(다항식에 가까울수록) 세메레디 정리의 정량적 상한이 좋아집니다. Green은 이를 이 분야의 "아마도 가장 큰 열린 문제"라고 불렀습니다.

**최전선 요약.**

2023년 이전 상태:
- Green–Tao–Ziegler의 일반 U^{s+1}[N] 역정리는 정량화하면 탑(tower) 꼴이 되고, Manners의 정량 판은 d ≤ δ^{−O_s(1)}, ε^{−1}, K, M ≤ exp(exp(δ^{−O_s(1)}))로 "이중 지수" 손실이 있었습니다 (arXiv:2402.17994 서론). U^3은 Green–Tao와 Sanders, U^4는 Leng이 준다항식 수준을 얻었습니다.
- 유한체 F_p^n의 U^4에서는 Gowers–Milićević가 탑 3겹(exp^{(3)}), 이후 Kim–Li–Tidor와 Lovett가 단일 지수까지 개선했습니다 (arXiv:2601.01682 서론 서술).

2024–2026에 바뀐 것:
- 2024-02 Leng–Sah–Sawhney (arXiv:2402.17994): 임의의 s에서 U^{s+1}[N] 역정리의 준다항식 판. ‖f‖_{U^{s+1}[N]} ≥ δ이면 차수 s 영매니폴드 G/Γ와 Lipschitz 함수 F가 있어 상관 ≥ ε, 이때 d ≤ log(1/δ)^{O_s(1)}, ε^{−1}, K, M ≤ exp(log(1/δ)^{O_s(1)}). (서론 도구 인용) 핵심 입력은 Leng의 닐수열 효율적 균등분포 이론(arXiv:2312.10772, 2023, 배경).
- 2024-10 Milićević (arXiv:2410.08966): F_p^n의 U^4 노름 준다항식 역정리, 새 "추상 Balog–Szemerédi–Gowers" 정리를 도구로 사용. (초록)
- 2026-01 Milićević (arXiv:2601.01682): 일반 유한 아벨군의 U^4 준다항식 역정리. |G|가 6과 서로소이면 Bohr 집합 위의 "almost-cubic polynomial" 장애물 (정리 1.2: Bohr 집합 여차원 (2 log c^{−1})^{O(1)}, 상관 ≥ exp(−(2 log c^{−1})^{O(1)})), G=(Z/2^dZ)^n이면 3차 다항식 (정리 1.3). Jamneshan–Shalom–Tao의 질문(Question 1.9)에 U^4 경우 답함.

뜻: 이제 모든 차수에서 "준다항식" 손실만 있고, 다항식 손실의 역정리는 어느 차수에서도 일반적으로는 모릅니다.

**남은 경계.**
1. 다항식 손실의 역정리(상관 ≥ δ^{O_s(1)})가 성립하는가. 2402.17994는 이를 "열린 문제"로 직접 쓰지는 않고 Green의 말 "perhaps the biggest open question in the subject"를 인용합니다.
2. 일반 유한 아벨군에서 U^5 이상의 역정리 (Milićević 2601.01682는 U^4만). Jamneshan–Tao 일반 역정리 추측을 저자가 "almost-trilinear forms로 가능할 법하나 이 논문에서는 추구하지 않는다"고 서술.
3. 저자 서술: (Z/kZ)^n에서 밀도 1/k 집합이 5항 등차수열을 포함하는가 같은 세메레디형 변형은 "그럴 법하지만 증명 못함"(2601.01682, 서론 요약 경유).
4. 역정리를 쓴 세메레디 상한이 k≥5에서 다항로그에 못 미치는 이유(K2).

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2402.17994 | 2024-02-28 | James Leng, Ashwin Sah, Mehtaab Sawhney | Quasipolynomial bounds on the inverse theorem for the Gowers U^{s+1}[N]-norm | 모든 s에서 준다항식 역정리 | 초록 + 서론(HTML) | K3의 핵심 |
| 2601.01682 | 2026-01-04 | Luka Milićević | General inverse theory for the U^4 norm | 일반 유한 아벨군에서 U^4 준다항식 역정리, almost-cubic polynomial | 초록 + 서론(HTML) | 가장 최신. 열린 질문이 명시적 |
| 2410.08966 | 2024-10-11 | Luka Milićević | Quasipolynomial inverse theorem for the U^4(F_p^n) norm | F_p^n의 U^4 준다항식 역정리 | 초록 | 위 논문의 선행 |
| 2509.22962 | 2025-09-26 | Sarah Peluse | Finding arithmetic progressions in dense sets of integers | 고차 푸리에 해석과 역정리의 역할 서베이 | 초록 + 본문 앞부분 | K2와 중복. 입문용 |

**팩 추천.**
- 2402.17994: 가장 일반적인 준다항식 역정리이고 서론에 Manners 이중지수에서 준다항식으로의 "무엇이 바뀌었는가"가 정확히 서술됩니다.
- 2601.01682: 2026년 최신이고 "Question 1.9"처럼 이름 붙은 열린 질문과 시도해 볼 방향이 명시되어 있어 문제를 낳을 만합니다.

---

## K4. 코너 문제와 다차원 세메레디 (Corners problem, multidimensional Szemerédi)

**쉬운 설명.** 격자 위의 점을 골랐을 때 "ㄱ자 모양 세 점 (x,y), (x+d,y), (x,y+d)"(코너)가 반드시 생기는가를 묻습니다. 3항 등차수열을 2차원으로 올린 문제로, 코너가 없으면서 최대한 큰 집합이 얼마나 되는지를 재는 것이 핵심이고, 이는 컴퓨터과학의 "여러 사람이 이마에 숫자를 붙이고 합을 맞추는 통신 게임"의 비용과 직접 연결됩니다. 1차원 3항 등차수열보다 훨씬 어려워서 2024년까지 Shkredov(2006)의 "log log N 에 비례하는 약한 개선"이 최고였는데, 2025년에 한 번에 "준다항식"이 되었습니다.

**최전선 요약.**

2023년 이전 상태:
- 상한: Shkredov (2006) [N]×[N]에서 |A| ≤ N²(log log N)^{−Ω(1)}. 유한체에서는 Lacey–McClain이 같은 꼴, 일반 군에서는 Sanders가 |G|²·(log log|G|)^{−1} 꼴 (arXiv:2504.07006 서론).
- 하한: Behrend형, 밀도 ≥ e^{−O(√log N)}. Green (2021, arXiv:2102.11702)이 지수 상수를 개선했고 Green의 torus 논문(arXiv:2209.10012)이 하위 항을 개선 (검색 요약 경유, 이 보고에서 직접 열람하지 않음).

2024–2026에 바뀐 것:
- 2024-02/04 skew corner(코너를 비튼 쉬운 변형): Beker (arXiv:2402.19169)가 하한 n²·exp(−O(√log n))과 상한 O(n²(log n)^{−c})를 주었고, 이어 Jaber–Lovett–Ostuni (arXiv:2404.07380, 상한 n²·exp(−Ω(log^{1/12} n)))와 Milićević (arXiv:2404.07180, exp(−c log^c n)·n²)가 독립적으로 Kelley–Meka 기법으로 하한 모양과 거의 일치하는 상한을 얻었습니다.
- 2025-04 Jaber–Liu–Lovett–Ostuni–Sawhney (arXiv:2504.07006): 정리 1.1: 유한 아벨군 G에서 코너 없는 A ⊆ G×G는 |A| ≤ |G|²·exp(−c(log|G|)^{1/600}). 유한체 판 (N=2^n) 정리 1.3: |A| ≤ N²·exp(−c(log N)^{1/178}). 저자는 1/600을 최적화하지 않았다고 서술합니다. Shkredov의 log log 꼴에서 준다항식으로 "이중 지수적" 도약입니다. 응용: 3인 NOF 비결정적 프로토콜의 Exactly-N 통신량 Ω((log N)^{Ω(1)}) (Corollary 1.7), 4인은 Ω(log log log log N) (Cor. 1.8), 3차원 코너 채색은 색 c·log log log|G|개로도 단색 코너가 생김 (Cor. 1.2).
- 2024-11 Bhangale–Khot–Liu–Minzer (arXiv:2411.15137): [3]^n에서 조합적 직선(밀도 Hales–Jewett, 길이 3)을 밀도 (log log log log n)^{−c}에서 보장. Shkredov의 코너 증명을 번역한 방식.
- 2024-07 다항식 코너: Kravitz–Kuca–Leng (arXiv:2407.08637), N²/(log log log N)^c 꼴. Peluse–Prendiville–Shao (arXiv:2407.08338): (x,y), (x+z,y), (x,y+z²)의 popular 판.
- 2026-05/09: Guo–Miao–Zhan (arXiv:2605.06360), Lott–Magyar–Ponagandla (arXiv:2609.13126, [N]^d의 심플렉스 닮은꼴에 exp(−c√log N) 상한).

뜻: 2차원 코너는 이제 3항 등차수열(1/12 지수)과 같은 부류의 "준다항식"이지만, 지수가 1/600으로 Behrend 1/2와 크게 떨어져 있습니다.

**남은 경계.**
1. 코너 상한 지수를 1/600에서 Behrend 1/2 쪽으로 올릴 수 있는가. 저자는 "기법으로는 1/2에 못 미칠 것 같다(appear unable to yield results approaching 1/2)"고 적었습니다 (arXiv:2504.07006 서론 요약).
2. 3차원 이상의 코너/단체(simplex)의 정량적 상한. 2504.07006은 3차원 코너의 "색칠 판"만 얻었고 밀도 판은 열려 있음 (log log log|G|라는 매우 약한 결과). 이 점은 서론 서술 기반이며 저자가 "open"이라 쓴 문장은 확인하지 못했습니다.
3. 정수 [N]²에서 Kelley–Meka식 코너 상한(논문은 일반 아벨군; 정수 판은 Discrete Analysis 서술에 따르면 같은 저자들이 exp(−C(log N)^{1/600})로 언급).
4. 밀도 Hales–Jewett: 길이 4 이상(DHJ[k], k≥4)의 합리적 상한. Bhangale et al.이 "비슷한 방법으로 가능할 것 같으며 k항 CSP 결과의 유사물이 필요, 향후 연구 계획"이라 적었습니다 (arXiv:2411.15137).
5. 일반 다차원 다항식 세메레디 정리의 다항로그 상한 (Guo–Miao–Zhan, Shao–Wang이 부분적으로만 해결).

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2504.07006 | 2025-04-09 | Michael Jaber, Yang P. Liu, Shachar Lovett, Anthony Ostuni, Mehtaab Sawhney | Quasipolynomial bounds for the corners theorem | 코너 없는 집합 ≤ |G|²exp(−c(log|G|)^{1/600}), NOF Exactly-N 통신 하한 | 초록 + 서론(HTML) | K4의 핵심. 한 사이트가 FOCS 2025 best paper라 서술했으나 직접 확인 못함 `[미확인]` |
| 2404.07380 | 2024-04-10 | Michael Jaber, Shachar Lovett, Anthony Ostuni | Strong Bounds for Skew-Corner-Free Sets | skew corner 상한 n²exp(−Ω(log^{1/12} n)) | 초록 | 코너의 쉬운 변형. 위 논문의 전 단계 |
| 2404.07180 | 2024-04-10 | Luka Milićević | Good bounds for sets lacking skew corners | skew corner 상한 exp(−c log^c n)n² (독립) | 초록 | Pratt의 질문을 사실상 해결 |
| 2402.19169 | 2024-02-29 | Adrian Beker | Improved bounds for skew corner-free sets | skew corner 하한 n²exp(−O(√log n)) 구성, 상한 O(n²(log n)^{−c}) | 초록 | Behrend형 구성 |
| 2411.15137 | 2024-11-22 | Amey Bhangale, Subhash Khot, Yang P. Liu, Dor Minzer | Reasonable Bounds for Combinatorial Lines of Length Three | 밀도 HJ(3)에 (log log log log n)^{−c} | 초록 + 서론(HTML) | 코너 증명을 번역한 사례. 다차원 세메레디의 조합판 |
| 2407.08637 | 2024-07-11 | Noah Kravitz, Borys Kuca, James Leng | Corners with polynomial side length | 다항식 변 길이 코너 N²/(log log log N)^c | 초록 | 다차원 다항식 세메레디 |
| 2407.08338 | 2024-07-11 | Sarah Peluse, Sean Prendiville, Xuancheng Shao | Bounds in a popular multidimensional nonlinear Roth theorem | (x,y),(x+z,y),(x,y+z²)의 popular 판 | 초록 | 지수 의존성(탑이 아님) |
| 2605.06360 | 2026-05-07 | Jingwei Guo, Changxing Miao, Guoqing Zhan | A multidimensional Szemerédi theorem in integers | [N]^n에서 (log N)^{−c} 다항로그 상한 | 초록 | 최신. 요약만 읽음 |
| 2609.13126 | 2026-09-11 | Andrew Lott, Ákos Magyar, Nagendar Reddy Ponagandla | Quasipolynomial density bounds for K-point configurations in Z^d | [N]^d에서 닮은 단체 없는 집합 ≤ N^d exp(−c√log N) (d ≥ 4K+4) | 초록 | 가장 최신. 날짜는 열어 본 페이지 기준 |
| 2512.15125 | 2025-12-17 | Carl Schildkraut | Abelian structure in approximate groups and Alon's conjecture on Ramsey Cayley graphs | JLLOS 코너 결과 등을 이용한 비가환군 "local Roth" 정리 | 초록 | 코너는 응용 쪽 |

**팩 추천.**
- 2504.07006: 코너 문제의 현 최전선이고, 3차원 코너와 NOF 통신 복잡도라는 서로 다른 열린 방향을 담고 있어 새 문제를 낳기 좋습니다. 대조군과 겹치지 않습니다.
- 2404.07380 (또는 2411.15137): 가장 읽기 쉬운 "작은 사례"입니다. Kelley–Meka 기법을 skew corner에 옮긴 과정이 K1의 Raghavan 논문과 연결되는 점이 팩 내부의 일관성을 줍니다. 한 편만 넣어야 하면 팩 크기를 고려해 2504.07006을 우선합니다.

---

## 부록: 확인하지 못한 점과 주의

- Raghavan(arXiv:2603.27045) 초록과 본문 정리의 구간/Z/NZ 불일치 (K1).
- Bloom–Sisask(arXiv:2309.02353, 2023-09)과 Kelley–Meka(arXiv:2302.05537, 2023-02)는 2023년 결과여서 후보에서 제외했습니다 (배경 설명에만 사용).
- 위키 등 2차 자료에서 얻은 서술은 `[요약 경유]`로 표시했고, 모든 후보의 번호·저자·날짜는 arXiv 초록 페이지에서 옮겼습니다.
- 2504.07006에 대해 검색 결과 어떤 사이트가 "FOCS 2025 best paper"라고 적었으나, 원 논문이나 FOCS 페이지에서 확인하지 못했습니다 `[미확인]`.
- K1의 F_3^n 캡셋 하한(Tyrrell 2022)은 2024–2026 후보가 아니라 배경이며, DeepMind(FunSearch, 2023-12) 개선은 직접 확인하지 못했습니다.
