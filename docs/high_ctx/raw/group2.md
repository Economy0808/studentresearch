# 가법 조합론 최전선 문헌 조사: 그룹 2 (K5–K8)

조사 날짜: 2026-11-06
맡은 키워드: K5 다항식 세메레디 정리와 다항식 진행 / K6 제곱수 차이를 피하는 집합 (사르쾨지) / K7 캡 세트와 유한체 모형 / K8 반데르바르덴 수와 등차수열 램지 수

읽은 범위 표기: "초록" = arXiv 초록 페이지, "서론" = arXiv HTML(또는 PDF) 서론과 주요 정리 진술, "서론+본문 일부" = 서론 외에 일부 절·주석까지.
모든 arXiv 번호, 저자, 제목, 첫 제출일은 위 방식으로 연 페이지에서 옮겼습니다. 제출일은 arXiv 초록 페이지의 v1 날짜입니다.

공통 주의 (연구자가 알아야 할 것)
- 2026년 논문 중 일부는 증명이나 구성을 AI가 만들었다고 밝힙니다. 해당 논문 비고에 적었습니다. 아직 검증 중인 주장과 arXiv에 없는 주장은 "arXiv 아님/미검증"으로 따로 표시했습니다.
- 대조군(#28, #30, #36, #39, #52, #66, #200, #241, #324)과 직접 겹치는 논문은 이 그룹에서 찾지 못했습니다. 다만 K6의 "사르쾨지 문제"와 K5의 "x, x+P(y) 꼴"은 #324(다항식 시돈)와 이름이 비슷할 뿐 다른 문제입니다. 각 후보의 비고에 겹침 여부를 따로 적지 않은 것은 겹치지 않는다는 뜻입니다.

---

## K5. 다항식 세메레디 정리와 다항식 진행 (polynomial Szemerédi theorem, polynomial progressions, nonlinear Roth)

**쉬운 설명.** 보통의 세메레디 정리는 "충분히 빽빽한 정수 집합에는 등차수열이 있다"는 말입니다. 등차수열은 x, x+y, x+2y처럼 간격 y가 같은 수들이지요. 다항식 세메레디 정리는 간격을 곱하거나 제곱하는 식으로 바꿔도 같은 일이 생긴다고 말합니다. 예를 들어 x, x+y, x+y² (간격이 y, y²로 다른 모양)도 빽빽한 집합에는 반드시 나타납니다. 이 정리는 1996년 이미 증명됐지만 "얼마나 빽빽해야 하는가"를 숫자로 말하는 증명은 몇 가지 특수한 경우에만 있습니다. 이 분야의 최전선은 그 "얼마나"를 점점 구체적으로 줄여 가는 일입니다.

**최전선 요약.**
2023년 이전 상태 (배경):
- 일반 다항식 진행에 대한 수치 있는 증명은 없었고, 특수한 경우만 있었습니다. 사르쾨지(x, x+y²), Prendiville(같은 차수 동차다항식), Peluse–Prendiville(x, x+y, x+y²; 밀도 (log N)^(-c) 꼴), Peluse(서로 다른 차수이고 상수항이 0인 다항식들; 밀도 (log log N)^(-c) 꼴)가 대표입니다 (2505.16822 서론에 정리된 것을 옮김).
2024–2026에 바뀐 것:
- Shao–Wang (2505.16822, 2025-05): 서로 다른 차수이고 상수항이 0인 다항식 P_1,...,P_m에 대해, {1..N}의 부분집합이 밀도 ≥ (log N)^(-c)이면 x, x+P_1(y),...,x+P_m(y) (y≠0)가 들어 있습니다 (c는 다항식에만 의존). 이전 최고 (log log N)^(-c)(Peluse)에서 (log N)^(-c)로 로그 하나를 줄인 것입니다. 쉬운 말로: "필요한 밀도의 기준이 한 단계 더 낮아졌다."
- Altman–Sawhney (2506.13010, 2025-06): 고정된 다항식 P (P(0)=0)의 배수 간격 x, x+a_1P(y),...,x+a_tP(y). P'(0)≠0이고 t=3이면 |A| ≪ N exp(-c(log log N)^c), P'(0)≠0이고 더 길면 N exp(-c(log log log N)^c), P'(0)=0이면 N(log log log N)^(-c). 유한체 Z/NZ (N 소수)에서도 "전달(transference)" 가능한 진행에 N exp(-c'(log log log N)^c') 꼴. 이전에는 단항식 P에 대해 Prendiville의 N(log log N)^(-c')뿐이었습니다.
- Krause–Mousavi–Tao–Teräväinen (2608.19525, 2026-08): 간격을 (p−1) (p는 소수)로 제한한 진행. 서로 다른 차수일 때 |A| ≪ N(log N)^(-c_*), 선형(x, x+(p−1),..., 길이 k) k=3일 때 N exp(-(log log N)^c), k≥4일 때 N exp(-(log log log N)^c). 비선형 길이 3 이상에서는 이 형태의 수치 있는 결과가 처음이라고 밝힙니다.
- Leng–Sah–Sawhney (2402.17995, 2024-02): 보통 등차수열(k≥5)에서 r_k(N) ≪ N exp(-(log log N)^(c_k)). 다항식은 아니지만 위 결과들이 기대는 기준선입니다.

**남은 경계.** (모두 논문이 직접 한 말입니다)
1. 일반 다항식 진행(다항식 차수가 같거나 상수항이 있는 경우 등)의 수치 있는 세메레디 정리 전체: "a quantitative version of the general polynomial Szemerédi theorem remains an open challenge" (2505.16822 서론). 밀도 증가 논법이 일반 다항식 수열에서는 실패한다는 언급도 있습니다.
2. Altman–Sawhney는 P'(0)=0일 때의 N(log log log N)^(-c)이 "can likely be improved" (Remark 1.2)라고 씁니다 (2506.13010).
3. 소수 간격에서 상수항이 0인 다항식 범위를 벗어나면 결과가 확장되는지는 "left open" (2608.19525).
4. 팝뷸러 차이(popular difference) 버전의 지수 한 번 개선은 "an inverse theorem with a precise value of the exponent b"가 필요해 보인다고 합니다 (2505.16822 5절, Proposition 5.1 뒤의 주석).

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2505.16822 | 2025-05-22 | Xuancheng Shao, Mengdi Wang | Quantitative bounds in a popular polynomial Szemerédi theorem | 서로 다른 차수·상수항 0 다항식 진행에 (log N)^(-c) 밀도 한계와 효과적 팝뷸러 차이 버전 | 초록 + 서론 + 본문 일부 | 25쪽. 최전선을 가장 직접 보여 줌 |
| 2506.13010 | 2025-06-16 | Daniel Altman, Mehtaab Sawhney | On polynomial progressions via transference | 고정 다항식 배수 간격 진행의 효과적 한계와 Z/NZ에서의 전달 정리 | 초록 + 서론 | 34쪽. Leng의 추측 1–3을 "essentially resolves", 추측 1은 반례가 있다고 명시 |
| 2608.19525 | 2026-08-20 | Ben Krause, Hamed Mousavi, Terence Tao, Joni Teräväinen | Quantitative bounds for sets lacking polynomial progressions with shifted prime difference | 간격이 소수−1인 다항식 진행의 수치 있는 한계 (Wooley–Ziegler 정리의 수치화) | 초록 + 서론 + Tao 블로그 | 60쪽. 지금 가장 최신. 지그엘 영점 처리 등 기술적 |
| 2402.17995 | 2024-02-28 | James Leng, Ashwin Sah, Mehtaab Sawhney | Improved bounds for Szemerédi's theorem | k≥5에서 r_k(N) ≪ N exp(-(log log N)^(c_k)) | 초록 | 선형 기준선. 다항식 논문들이 인용 |
| 2407.08637 | 2024-07-11 | Noah Kravitz, Borys Kuca, James Leng | Corners with polynomial side length | 변의 길이가 다항식 값인 "코너"를 피하는 집합이 N²/(log log log N)^c 이하 | 초록 | 2차원 버전. 읽은 범위 얕음 |
| 2508.04680 | 2025-08-06 | Ben Krause, Ana de Orellana | On polynomial progressions inside sets of large dimension | 하우스도르프 차원이 1에 가까운 집합에서 다항식 진행 | 초록 | 연속(실수) 설정. 팩 부적합에 가까움 |

**팩 추천.** 2505.16822 (Shao–Wang)와 2506.13010 (Altman–Sawhney). 두 편 모두 "이전 최고 → 이 논문 → 남은 문제"가 서론에 선명하게 적혀 있고, 서로 다른 경우(서로 다른 차수 / 고정 다항식 배수)를 다루어 모델이 "그 사이의 빈틈"을 문제로 낼 수 있습니다. 2608.19525는 가장 최신이지만 60쪽에 소수 분포 기술이 많아 팩 분량 대비 효율이 낮을 수 있습니다. 대안으로 둡니다.

---

## K6. 제곱수 차이를 피하는 집합 / 사르쾨지 문제 (Sárközy's theorem, sets lacking square differences)

**쉬운 설명.** {1,...,N}에서 수를 골라 두 수의 차가 절대로 제곱수(1, 4, 9, 16, ...)가 되지 않게 하려면 최대 몇 개까지 고를 수 있을까요? 1970년대에 푸르스텐베르크와 사르쾨지가 "N에 비해 아주 작은 비율밖에 못 고른다"는 것을 증명했습니다. 지금은 그 "아주 작다"가 얼마나 작은가(위에서 누르는 한계)와 얼마나 많이 고르는 방법이 있는가(아래에서 받치는 구성) 사이의 간격이 최전선입니다. 위쪽 한계는 N에서 거의 지수적으로 작아지는 수준까지 내려왔는데, 아래쪽 구성은 N^0.75 정도입니다. N^(1-c) 꼴의 위쪽 한계가 되는지(거듭제곱 절약) 여부가 가장 큰 미해결 문제입니다.

**최전선 요약.** (s(N) 또는 D(N) = 제곱 차이가 없는 부분집합의 최대 크기)
2023년 이전 상태 (배경):
- 위쪽: 사르쾨지 N(log log N)^(2/3)(log N)^(-1/3); Pintz–Steiger–Szemerédi N(log N)^(-(1/12) log log log log N); Bloom–Maynard(2020) N(log N)^(-c log log log N).
- 아래쪽: 확률적 삭제로 N^(1/2); Ruzsa(1984)가 N^0.733077, Beigel–Gasarch와 Lewko가 각각 독립적으로 N^0.7334118 (2411.17448 서론, 2608.01325 서론에 정리).
2024–2026에 바뀐 것:
- 위쪽 (Green–Sawhney, 2411.17448, 2024-11-26): |A| ≪ N exp(-c√(log N)). 제출 당시는 지수 1/4−o(1)이었다가 개정으로 1/2가 되었습니다. 쉬운 말로: 이전의 "로그의 거듭제곱 분의 1" 수준에서 "exp(−√log N)" 수준으로 크게 내려왔습니다.
- 위쪽 개선 (Fan–Lott, 2610.07765, 2026-10): |A| ≤ N exp(-c√(log N · log log N)). 같은 논문이 이 "반데르코르푸트 방법" 자체로는 이 이상(거듭제곱 절약)을 낼 수 없음을 증명합니다 (Theorem 1.3, 한계의 하한이 exp(-C√(log N log log N))).
- 아래쪽 (Krachun, 2608.01325, 2026-08-02): D(N)의 지수를 0.7334에서 α* ≈ 0.7527964558로 올림. Ruzsa 방법이 3/4에서 멈춘다는 알려진 한계를 넘었습니다. 열 개의 소수 쌍 (3,2), (7,3), (11,4), (19,5), (23,5), (31,7), (43,7), (59,9), (71,9), (103,11)을 쓰는 구성입니다.
- 일반화: 교차 다항식(0으로 만드는 정수가 있는 다항식) h에 대해 X exp(-c_0(log X)^μ) (Adajar 외, 2605.16216). 세제곱 차이에는 거듭제곱 절약 N^(59/60+ε)이 증명되었습니다 (Fan–Lott–Magyar–Matolcsi–Ruzsa, 2611.05267, 2026-11-03). 두 제곱의 합 차이는 N^(7/8+ε) (Fan–Lott, 2606.29185). 홀수 거듭제곱의 짝수 개 합은 N^(1-(1/k)min{sσ_k,1/2}+ε) (Kalogirou 외, 2609.16595).
- arXiv 아님/미검증: 2611.05267은 "OpenAI가 제곱 차이에 거듭제곱 절약을 주장하는 preprint를 냈다"고 쓰고 (그 preprint가 "교차 다항식 차이에 거듭제곱 절약" 버전으로 일반화), 이를 [14], [15]로 인용합니다. 검색으로 OpenAI 쪽 문서명 "A power saving for square-difference-free sets"(2026-09-24)와 "A power saving for intersective polynomial differences with an exponent depending only on the degree"(2026-10-05)를 찾았지만 arXiv 번호가 없고 PDF 본문은 열지 못했습니다 ([미확인]). 2610.07765 저자들은 AI 회사의 초안이 "largely unreadable"하다고 평하며 인정하지 않습니다. 위키백과 "Square-difference-free set" 쪽에는 Jones 0.753742, Naslund 0.7580758318 등 2026년 AI 사용 구성이 표로 올라 있으나 arXiv 번호를 확인하지 못했습니다 ([미확인], 팩 후보 아님).

**남은 경계.**
1. 거듭제곱 절약 N^(1-c)가 정말 성립하는가. "It is a longstanding open question whether |A| ≪ N^(1−c)" (2611.05267 서론). Green–Sawhney 2411.17448도 "It remains a major open question"이라 쓰고 "yes일 것으로 추측한다"고 덧붙입니다. 현재 arXiv에서 증명된 것은 세제곱 이상뿐이며, 제곱에 대한 OpenAI 주장은 검증 전입니다.
2. 아래쪽 지수의 참값. 현재 arXiv 최고는 α*≈0.7528이고, Krachun은 소수 1000 이하에서는 최적이지만 모든 소수에서 최적인지는 "t(p) < p^{0.5056}" 같은 증명 안 된 부등식이 필요하다고 밝힙니다 (2608.01325). Erdős식 추측 D(N) ≥ N^(1-ε)(모든 ε)이 참인지도 열려 있습니다 (위키백과 문구, arXiv 아님).
3. 세제곱의 정확한 지수: "Whether D_3(N) ~ C·N^γ for some γ ∈ [β, 59/60]", 그리고 극한 lim log D_3(N)/log N이 존재하는지 (2611.05267). 제곱에 대해 같은 질문을 Ruzsa가 했다고 적혀 있습니다.
4. Green–Sawhney 예시는 밀도 증가법이 N exp(-c(log N)^(3/4))보다 강한 결과를 주지 못할 수 있음을 시사 ("at least in anything like the form", 2610.07765 서론).

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2411.17448 | 2024-11-26 | Ben Green, Mehtaab Sawhney | New bounds for the Furstenberg-Sárközy theorem | 제곱 차이 없는 집합이 N exp(-c√log N) 이하 | 초록 + 서론 | 개정(v2)으로 지수 1/4→1/2. 사실상 기준 논문 |
| 2610.07765 | 2026-10-06 | Steve Fan, Andrew Lott | The optimal van der Corput property for squares | N exp(-c√(log N log log N))와, 이 방법으론 거듭제곱 절약 불가를 증명 | 초록 + 서론 | v2에서 제목 변경(v1: "A new bound for the Furstenberg–Sárközy theorem using the van der Corput property"). 저자가 LLM을 상담역으로 썼다고 밝히고 직접 검증했다고 씀 |
| 2608.01325 | 2026-08-02 | Dmitry Krachun | Square-Difference-Free Sets beyond the Three-Quarter Barrier | 제곱 차이 없는 집합의 크기 하한 지수를 0.7528로 올림 | 초록 + 서론 + 구성 (HTML) | 7쪽. 아래쪽 최전선. 짧고 구성이 구체적 |
| 2611.05267 | 2026-11-03 | Steve Fan, Andrew Lott, Ákos Magyar, Máté Matolcsi, Imre Z. Ruzsa | On the van der Corput property for cubes | 세제곱 차이 없는 집합이 N^(59/60+ε) 이하 (거듭제곱 절약) | 초록 + 서론 | 제출 3일 전. 거듭제곱 절약 최초 사례 중 하나. AI 관련 논쟁 언급. 새로움 때문에 아직 검토 이력 짧음 |
| 2605.16216 | 2026-05-15 | Carlo Francisco E. Adajar 외 8명 | Extensions of the Furstenberg-Sárközy theorem via the arithmetic level-d inequality | 교차 다항식 h에 대해 D(h(N),X) ≤ X exp(-c_0(log X)^μ) | 초록 + 서론 | 초록 페이지는 v2에서 μ≤1/2로 확장됐다고 쓰는데, 열어 본 HTML 서론은 μ<1/2이고 μ=1/2는 "seems hopeless"라고 씀. 버전 차이 [확인 필요] |
| 2606.29185 | 2026-06-28 | Steve Fan, Andrew Lott | The van der Corput property for sums of two squares | 두 제곱의 합 차이를 피하는 집합이 N^(7/8+ε) 이하 | 초록 + 서론 | Younis의 N^(1/2) 구성과 지수 틈 남음 |
| 2609.16595 | 2026-09-15 | Alexandros Kalogirou, Andrew Lott, Ákos Magyar, Akash Singha Roy | The Furstenberg-Sárközy theorem for sums of an even number of odd powers | 홀수 거듭제곱 짝수 개 합을 피하는 집합의 거듭제곱 절약 한계 | 초록 | 얕게 읽음 |
| 2405.00868 | 2024-05-01 | John R. Doyle, Alex Rice | The Furstenberg-Sárközy theorem for polynomials in one or more prime variables | 소수 변수 다항식 차이에 대한 상한 | 초록 | 얕게 읽음 |
| 2508.18990 | 2025-08-26 | Dev Ranjan Pandey, Jyoti Prakash Saha | Furstenberg-Sárközy theorem over number fields | 수체의 정수환으로 일반화 | 초록 | 주변 주제 |
| 2508.03650 | 2025-08-05 | Christian Dean, Haley Havard, Elizabeth Hawkins, Patch Heard, Andrew Lott, Alex Rice | Notes and computations on forbidden differences | 제곱 N≤300, 소수−1 N≤500 정확한 최대 크기 계산과 서베이 | 초록 | 컴퓨터 계산 자료. 체커 문제를 낼 때 참고 가치 |
| 2608.30078 | 2026-08-30 | Khalid Younis | Sets whose differences avoid a bracket quadratic | 일반화 다항식(가우스 기호 포함) 차이에 대한 N^(1-c) 상한 | 초록 | 얕게 읽음 |

**팩 추천.** 2608.01325 (Krachun)와 2610.07765 (Fan–Lott). Krachun은 7쪽짜리라 짧고 "아래쪽 구성이 왜 0.75에서 막혔다가 풀렸는가"가 구체적으로 적혀 있어 문제가 나오기 좋습니다. Fan–Lott는 "지금 쓰는 방법으로는 이 이상 안 된다"는 한계를 증명해 위쪽 최전선을 선명하게 보여 줍니다. 두 편이 한 쌍으로 위·아래 간격을 보여 줍니다. 2411.17448도 좋은 대안이지만 36쪽에 가깝습니다. 2611.05267은 가장 흥미롭지만 사흘 전 논문이고 AI 주장 논쟁과 얽혀 있어 연구자 판단이 필요합니다.

---

## K7. 캡 세트와 유한체 모형 (cap sets, finite field models, slice rank, 하한 구성 포함)

**쉬운 설명.** F_3^n은 각 좌표가 0, 1, 2 중 하나인 길이 n 벡터의 모임입니다. 카드게임 SET과 같은 구조로, 점 세 개가 한 직선 위에 있으면(합이 0이면) "한 줄"입니다. 캡 세트는 한 줄도 포함하지 않는 점들의 모임이고, 가장 큰 캡 세트가 얼마나 큰지가 질문입니다. 정수에서 풀기 어려운 등차수열 문제를 이 "장난감 모형"에서 먼저 풀어 보면 아이디어가 드러난다는 것이 유한체 모형의 취지입니다. 2016년 Ellenberg–Gijswijt가 위쪽 한계를 2.756^n으로 극적으로 낮췄고, 이후 위쪽은 거의 움직이지 않은 채 아래쪽 구성이 컴퓨터 탐색으로 조금씩 올라가는 중입니다.

**최전선 요약.**
2023년 이전 상태 (배경):
- 위쪽: 자명하게 3^n. Meshulam 이후 Bateman–Katz가 3^n/n^(1+ε) 정도. 2016년 Ellenberg–Gijswijt(Croot–Lev–Pach의 다항식 방법 기반, slice rank 방법으로 정리): |A| ≤ (2.7552...)^n. 2021년에 √n 분의 1 인수가 추가됨 (arXiv 2103.06481 검색 결과로만 확인, 열어 보지 않음 [미확인]).
- 아래쪽: Edel (2.217389)^n, Tyrrell(2209.10045, 2022 → 후보 아님) (2.218)^n, FunSearch (Nature 2023) (2.2202)^n.
2024–2026에 바뀐 것:
- 아래쪽 2.2203: Zhai 외 X-evolve(2508.07932, 2025-08-11)가 부분 허용 집합을 더 크게 만들어 C ≥ 2.2203. Terence Tao의 최적화 상수 목록도 이 값을 현재 최고로 적고 있습니다. 이 논문은 cs.AI 분야이고 LLM 진화 탐색법 논문입니다.
- 주의: Croot–Lev–Pach 서베이(2408.02328, 2024-08-05)는 Naslund의 (2.2208)^n을 인용합니다. 근거 문헌은 "E. Naslund, Lower bounds for the Shannon capacity of hypergraphs"라는 manuscript입니다. arXiv 번호를 찾지 못했습니다 ([미확인]). Tao 목록은 이 값을 반영하지 않으므로 두 출처가 다릅니다.
- 곱 구성의 한계 (Hametner–Tyrrell, 2606.12194, 2026-06-10): 캡 세트 A⊂F_3^n에 대해 차원 2nr에서 r·|A|^(2r−2) 크기의 캡 세트를 만드는 "확장 곱" 구성. 결론: 고정된 어떤 캡 세트의 직접 곱만으로는 점근적으로 최적인 하한을 얻을 수 없습니다. 다만 저자들은 이 구성이 기록을 넘기는 데 쓸모 있는 방법은 아니며 개선폭이 소수점 452번째 자리라고 씁니다 (Remark 4.1).
- 유한체 모형 쪽 3-AP 하한: F_p^n에서 3-등차수열 없는 집합의 크기 (cp)^n, c>1/2 (소수 p≥3인 모든 p; 1940년대 구성은 c=1/2) (Elsholtz–Hunter–Proske–Sauermann, 2406.12290, 2024-06-18). 정수에서는 Behrend 구성의 첫 준다항식적 개선.
- 극한 사례: 소수 체 F_p^3에서 직선 없는 집합 크기에 p^(3/2) 급 초선형 추가 (Kovács, 2605.23437, 2026-05-22).
- 위쪽 한계에 대해 2024–2026 arXiv에서 2.7552를 낮춘 논문은 찾지 못했습니다. 서베이 2408.02328도 이를 "slice rank 자체를 피하는 것이 장벽"이라는 취지로 언급합니다 (검색 결과로 확인, 서베이 본문은 서론과 "Directions"절만 읽음).

**남은 경계.**
1. 직접 곱 구성이 점근적으로 최적일 수 있는가: 이 질문은 Hametner–Tyrrell이 "아니오"로 답했습니다 (2606.12194 서론). 다음 질문은 확장 곱 구성을 연립방정식으로 일반화하는 것: "Conjecture 4.4"(비퇴화 genus-one 평행이동불변 연립방정식에 대해서도 같은 결과일 것).
2. 세 개 항 이상으로 확장: "Can algebraic methods be used to estimate the size of the largest set S without a k-term progression in F_p^n, for k ≥ 4?" (2408.02328 5절 Directions).
3. 차이가 {0,1}^n에 속하는 제한된 설정: "how large can a subset S ⊂ F_3^n be given that S does not contain any three-term arithmetic progression with the difference in {0,1}^n?" (같은 곳).
4. 정수 설정에도 대수적 방법을 쓸 수 있는가, 여러 대수적 방법(Chevalley–Warning, Stepanov, Nullstellensatz, slice rank)이 "같은 방법"인가 (같은 곳).
5. 참값: 위쪽 2.7552^n과 아래쪽 약 2.22^n 사이의 간격. Tyrrell(2209.10045, 2022)은 모든 허용 집합이 존재한다고 가정하면 124^(n/6)≈2.233^n이 가능하다는 조건부 하한(구성 가능성)을 제시했습니다 (검색 결과 요약; 본문 미확인, 후보에서 제외).

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2606.12194 | 2026-06-10 | Paul Hametner, Fred Tyrrell | Beating Product Constructions for Linear Equations Over Finite Fields | 직접 곱을 능가하는 "확장 곱" 구성; 곱 구성만으로는 최적 하한 불가 | 초록 + 서론 + Remark 4.1–4.4 | 10쪽. 열린 추측 4.4 포함 |
| 2408.02328 | 2024-08-05 | Ernie Croot, Vsevolod F. Lev, Péter Pál Pach | Past and future of the cap set problem | 캡 세트 문제의 역사, 최근 진전, 향후 방향 서베이 | 초록 + 본문(서론, 기록 정리, Directions) | 서베이이나 열린 질문이 명시적. Naslund 2.2208 인용 |
| 2508.07932 | 2025-08-11 | Yi Zhai 외 9명 | X-evolve: Solution space evolution powered by large language models | LLM 진화 탐색으로 캡 세트 하한 2.2203 | 초록 | cs.AI. 수학 논문이라기보다 방법 논문. 저자 수가 많아 표에서는 축약 |
| 2406.12290 | 2024-06-18 | Christian Elsholtz, Zach Hunter, Laura Proske, Lisa Sauermann | Improving Behrend's construction: Sets without arithmetic progressions in integers and over finite fields | Behrend 구성의 첫 개선과 F_p^n에서 (cp)^n, c>1/2 | 초록 | 15쪽. 정수-유한체 가교 |
| 2602.05254 | 2026-02-05 | Cassie Grace, José Felipe Voloch | Algebraic capsets | F_3의 확대체 위 방정식으로 캡 세트 구성, 가장 작은 "완전 캡 세트" | 초록 | 얕게 읽음 |
| 2604.26989 | 2026-04-28 | Anthony Kable, Melissa Mills, David J. Wright | Subgroups of Finite Fields As Cap Sets | 유한체의 승법 부분군이 캡 세트가 되는 예(SET, EvenQuads 연결) | 초록 | 작은 차원의 구체 사례 |
| 2605.23437 | 2026-05-22 | Benedek Kovács | A superlinear improvement on line-free sets in F_p^3 | F_p^3 직선 없는 집합 하한에 p^(3/2) 급 개선 | 초록 | 7쪽. 소수 체 설정 |
| 2405.00923 | 2024-05-02 | Jakob Führer, Jozsef Solymosi | Caps and Wickets | 캡 세트 추정을 이용해 "wicket" 하이퍼그래프 튀란 수 하한 | 초록 | 주변 응용 |

**팩 추천.** 2606.12194 (Hametner–Tyrrell)와 2408.02328 (Croot–Lev–Pach 서베이). 전자는 10쪽에 정확한 정리와 열린 추측이 있고, 후자는 현재 기록·인용 계보(Edel → Tyrrell → FunSearch → Naslund)와 열린 질문 목록이 명시적입니다. 둘 다 대조군과 겹치지 않습니다. 하한을 컴퓨터가 올리는 최근 흐름(X-evolve 2508.07932)은 흥미롭지만 수학적 열린 질문을 직접 담지 않아 후순위입니다.

---

## K8. 반데르바르덴 수와 등차수열 램지 수 (van der Waerden numbers, Ramsey numbers for progressions)

**쉬운 설명.** 1부터 N까지 수를 r가지 색으로 칠할 때 같은 색으로만 이루어진 k개짜리 등차수열이 반드시 생기는 가장 작은 N이 반데르바르덴 수 w(k; r)입니다. 색이 2개이고 k=3이면 9입니다(8까지는 피할 수 있고 9부터는 불가능). 이 수가 유한하다는 것은 1927년에 알려졌지만, 얼마나 빠르게 커지는지는 아직 잘 모릅니다. 위쪽 한계는 탑 꼴로 엄청나게 크고, 아래쪽 한계는 지수 꼴이라 간격이 거대합니다. 2026년에 아래쪽 한계 쪽에서 여러 소식이 한꺼번에 나왔습니다.

**최전선 요약.**
2023년 이전 상태 (배경):
- 위쪽: Shelah(1988) 원시 재귀 한계; Gowers(2001) w(k;r) ≤ 2^(2^(r^(2^(2^(k+9))))). Leng–Sah–Sawhney(2402.17995, 2024)가 고정된 k에 대해 w(r,k) ≤ 2^(2^((log r)^(c_k)))로 개선 (2603.25922 서베이와 2606.02541 서론에 인용됨).
- 아래쪽: Erdős–Rado(1952) √(2k r^k); Lovász 지역 보조정리 r^(k-1)/(4k); Berlekamp(1968) 소수 p에 w(p+1;2) > p·2^p; Blankenship–Cummings–Taranchuk(1705.09673, 2017) 점화식; Green(2102.01543, 2021)과 Hunter(2111.01099, 2021)의 w(3,k) ≥ k^(Ω(log k/log log k)); Hunter(2301.06212, 2023-01-15, 이후 Israel J. Math. 267 (2025))의 r≥5색 지수적 개선. 이 셋은 2023년 이전 제출이라 후보에서 제외했습니다.
2024–2026에 바뀐 것:
- 2색 대각선 (Campos–Fox–Schildkraut, 2608.20824, 2026-08-21): w(k) ≥ (1−o(1))·k·2^(k−1)을 모든 k에 대해 증명. Berlekamp는 k−1이 소수일 때만 했고, Erdős의 추측을 확인했습니다. 서로 다른 소수에 대한 Berlekamp 채색들의 곱으로 만듭니다. 이전 일반 최고는 Kozik–Shabanov의 c·2^k. 초록에 "ChatGPT 5.6 Sol Pro"가 채색과 증명을 만들었다고 밝혀 있습니다 (본문 서론도 같은 문장). 5쪽.
- 3색 (Fox–Hunter, 2606.02541, 2026-06-01): 충분히 큰 k에서 2^(k·log*(k)/4)까지 w(k;3)가 크다고 증명. 따라서 3색 w(k;3)은 어떤 지수 함수보다 빠르게 증가합니다. r이 (log k)^(3/ε) 이상이면 w(k;r) ≥ r^((1−ε)k log k). 또 Erdős–Graham의 "정규(canonical) 반데르바르덴 수" H(k)가 H(k) ≥ k^((1−o(1))k log k)라서 H(k)^(1/k)/k → ∞ 문제가 해결됩니다.
- 정규 반데르바르덴 수의 독립적 약한 해결 (Bae, 2604.20588, 2026-04-22): Erdős Problem #190. H(k)^(1/k)/k가 k/log k의 상수배(상수는 1/e로 수렴) 이상이라 극한이 무한대임을 보임. Fox–Hunter가 더 강한 결과를 얻었다고 명시.
- 2색 비대각 w(3,k) (Cao, 2609.31798, 2026-09-25): w(3,k) ≥ k^(Ω(log k)). Hunter의 k^(Ω(log k/log log k))에서 log log k 손실을 제거. 위쪽은 Raghavan의 exp(O((log k)^6 (log log k)^6)) (이 논문 서론에서 인용). 참값이 k^(Θ(log k))일 수 있다고 추정.
- 구체적 작은 수 (Kim, 2610.32000, 2026-10-22): 3색에서 9≤k≤28에 대해 알려진 공개 하한을 모두 넘는 명시적 값. 다만 이 방법은 점근 증가율을 올리지 못한다고 저자가 밝힘.
- 서베이 (Bergelson–Richter, 2603.25922, 2026-03-26): 역사와 응용 중심. 알려진 정확한 값 W(2,3)=9, W(3,3)=27, W(4,3)=76, W(2,4)=35, W(3,4)=293, W(2,5)=178, W(2,6)=1132 정리.
- 미확인: Stanford 세미나 안내문에 w(k;r) > (r!−o(1))^k (고정 r, 큰 k) 형태의 결과 발표가 있다는 검색 결과가 있었으나 arXiv 번호를 찾지 못했습니다 ([미확인]). Fox–Hunter 서론은 Hunter(2025)의 고정 r≥5 결과를 (3^(r/3))^((1−o(1))k)로 인용합니다 (r≥6이 3의 배수일 때).

**남은 경계.**
1. Erdős의 500달러 문제: w(k;2)가 초지수적으로 증가하는가. Fox–Hunter 서론: "remains open, though Erdős guessed it holds". 지금 증명된 것은 2색 k·2^(k−1) 수준(2608.20824)과 3색 초지수(2606.02541)입니다.
2. w(3,k)의 참값: Cao는 k^(Θ(log k))가 맞을 수 있다는 "some evidence"만 제시하고, 위쪽 한계는 exp(O((log k)^6(log log k)^6)) 수준이라 아래쪽과 지수 간격이 큽니다 (2609.31798).
3. 다색 지수 개선의 병목: Fox–Hunter는 필요한 집합을 만들 방법을 모르기 때문에 지수를 "1+Ω(1)" 인수만큼 개선하지 못한다고 서술 ("not aware of any way to construct a set"), 소수의 색에 대해서도 같은 방법이 작은 수 하한을 주리라 짐작 (2606.02541).
4. 위쪽 한계의 탑 구조: 여전히 Gowers의 5중 지수 꼴에서 Leng–Sah–Sawhney가 고정 k에서 줄인 수준입니다 (arXiv 서베이 2603.25922, 서론 일부만 읽음). Graham의 $1000 문제(w(k) < 2^(k²)인가) 같은 직접 진술은 내가 읽은 부분에서 확인하지 못했습니다 ([미확인]).

**후보 논문.**
| arXiv | 첫 제출일 | 저자 | 제목 | 한 일 (한 줄) | 읽은 범위 | 비고 |
|---|---|---|---|---|---|---|
| 2606.02541 | 2026-06-01 | Jacob Fox, Zach Hunter | Three-color van der Waerden numbers grow super-exponentially | w(k;3)이 지수보다 빠르게 증가함을 증명하고 H(k) 문제 해결 | 초록 + 서론 | 19쪽. 상태 정리 및 열린 질문이 명확 |
| 2609.31798 | 2026-09-25 | Haitao Cao | An improved lower bound for the van der Waerden number w(3,k) | w(3,k) ≥ k^(Ω(log k)) | 초록 + 서론 + 방법 | 짧음(13KB). 방법이 구체적 (원환 위의 얇은 껍질로 채색) |
| 2608.20824 | 2026-08-21 | Marcelo Campos, Jacob Fox, Carl Schildkraut | A new lower bound for two-color van der Waerden numbers | 모든 k에서 w(k) ≥ (1−o(1))k·2^(k−1) | 초록 + 서론 | 5쪽. 초록과 서론에 ChatGPT 5.6 Sol Pro가 채색·증명을 생성했다고 명시 |
| 2604.20588 | 2026-04-22 | Ji Ho Bae | A resolution of Erdős Problem #190 via Erdős-Lovász, BCT, and Baker-Harman-Pintz | 정규 반데르바르덴 수 H(k)에 대한 Erdős–Graham 문제 해결 | 초록 | 10쪽. Fox–Hunter가 더 강한 결과로 대체했다고 인용. 대조군 아님(#190은 대조군 목록에 없음) |
| 2610.32000 | 2026-10-22 | Seonbin Kim | Polychromatic blocks and explicit lower bounds for multicolour van der Waerden numbers | 3색 9≤k≤28의 명시적 하한을 새로 올림 | 초록 | 12쪽. 컴퓨터 검증, 점근 개선 아님 |
| 2402.17995 | 2024-02-28 | James Leng, Ashwin Sah, Mehtaab Sawhney | Improved bounds for Szemerédi's theorem | 고정 k에서 반데르바르덴 위쪽 한계 개선의 원천 (r_k(N) 개선) | 초록 | K5와 중복. 위쪽 한계 쪽 근거 |
| 2603.25922 | 2026-03-26 | Vitaly Bergelson, Florian K. Richter | Van der Waerden's theorem on arithmetic progressions: a survey of some historical and modern developments | 정리의 역사와 파급 서베이, 알려진 한계 정리 | 초록 + 2.1절(한계와 정확한 값) | 49쪽. 열린 문제 절은 이 주제와 무관 |
| 2606.22155 | 2026-06-20 | Younes Mouhib | Lower Bounds for the Hales-Jewett Numbers via Symmetric and One-Weight Colorings | HJ(3,3) ≥ 22, HJ(4,2) ≥ 14 등 호르-주잇 수 하한 | 초록 | 주변 주제. SAT 계산 |

**팩 추천.** 2606.02541 (Fox–Hunter)와 2609.31798 (Cao). Fox–Hunter는 현재 하한 상태와 열린 질문(Erdős 500달러 문제)을 한 서론에 모아 놓았고, Cao는 방법이 짧고 구체적인 비대각 사례입니다. 2608.20824는 가장 짧고 극적이지만 증명을 AI가 만들었다고 밝혀서, 이 실험에서 AI 산출물과 인간 산출물의 구분이 중요한 연구자라면 포함 여부를 직접 판단하시기 바랍니다.
