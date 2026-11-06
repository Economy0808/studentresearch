# 구해 주실 자료: 참고문헌 목록

기준일 2026-11-06. 정독판(`2026-11-06-additive-comb-deep-reading.md`)의 "구해 주실 자료"를 참고문헌 형식으로 옮겼습니다.

**서지 출처.** 서지는 이 자료를 인용한 논문의 참고문헌에서 그대로 가져왔습니다. 어느 논문에서 가져왔는지는 항목마다 `출처`에 적었습니다. arXiv 정보는 arXiv API로 확인했습니다.

**학술지 논문은 2편뿐입니다.** 필수 8개 중 학술지에 실린 것은 6번(Lev)과 7번 원논문(GTZ)입니다. 나머지는 원고, GitHub 저장소, 사전 공개 논문이라 권호와 쪽이 없습니다.

## 수집 결과(2026-11-06)

5번을 뺀 필수 자료를 공개 출처(GitHub, EJC, Green 웹페이지)에서 직접 받아 `docs/high_ctx/supplied/`에 번호를 붙여 넣었습니다. 정독 결과는 `2026-11-06-additive-comb-supplement.md`에 있습니다.

| # | 상태 | 파일 | 확인된 사실 |
|---|---|---|---|
| 1a, 1b | 받음 | `01a_…`, `01b_…` | 저자 표기는 "OpenAI"입니다. `openai/math` 목록에서 1b는 #182입니다. |
| 2 | 받음 | `02_Naslund_exponent-0.7580758_2026-10.pdf`(.tex 포함), `02c_…` 동반 논문 | 저장소 README에 따르면 10월 판(0.7580758318)이 9월 판(0.75806746)을 **대체**했습니다. 9월 판은 커밋 `e5d6937`에 남아 있습니다. Tao 표에 따르면 Hexagon 2610.00151v1(2026-10-07)도 이 10월 판입니다. 따라서 2a와 2b는 같은 저자의 이전 판과 새 판이고, 기록 순서는 Naslund 0.75806746 → Jones 0.75806770 → Naslund 0.7580758입니다. |
| 3a | 받음 | `03a_…` | 이 원고의 값은 0.753742입니다. 0.75806770은 3b에 있습니다. |
| 3b | 받음(README, PROOF.md) | `03b_…` | 0.75806770413은 "Naslund 0.75806746의 개선"이라고 적혀 있습니다. 논문 PDF는 저장소에 없습니다. |
| 4a | 받음 | `04a_…` | |
| 4b | 받음 | `04b_…` | 제목: *Monochromatic finite sums and products in the positive integers* (2026-09-23). |
| 5 | **못 찾음** | | 공개본, 초록, 학술지판이 모두 없습니다. 다른 논문들은 "원고"나 "발표 예고"로만 인용합니다. 저자에게 직접 요청하는 것 말고는 방법이 없어 보입니다. |
| 6 | 받음 | `06_Lev2000_EJC_R4.pdf` | 아래 "6번 확인" 참고 |
| 7 | 받음 | `07_GTZ_erratum_2024.pdf` | Green 웹페이지에 있는 정오표(2024-04)입니다. 명제 8.3이 "as stated로는 성립하지 않는다"며 고친 판을 줍니다. arXiv v5와는 별개 문서입니다. |
| 8 | 받음 | `08_Green_100-open-problems.pdf` | |

**6번 확인(Ouyang 반례 판정에 필요했던 것).** Lev 2000 EJC 논문은 처음 추측(결론 |A+B| ≥ min{|A|+|B|−3, p})을 스스로 "너무 낙관적"이라 철회합니다. 그리고 τ가 단사인 경우에 대해 세 갈래 추정을 다시 묻습니다. 세 갈래는 "|A|+|B| ≤ p이면 |A|+|B|−3", "= p+1이면 p−3", "≥ p+2이면 p−2"입니다. 그러면서 "그렇지 않을 수도 있지만 진실에 가깝다"고 덧붙입니다. 결론 절에도 "|A|+|B| ≥ p+2이면 p−2인가"를 열린 문제로 다시 적습니다. Ouyang이 서론에 옮겨 적은 Lev 추측은 이 세 갈래를 그대로 옮긴 것입니다(|A|, |B|의 역할 이름만 바뀜). 따라서 Ouyang 구성(|A| ≈ 6p/11, 짝짓기 제한, 합집합 p−3)은 Lev가 실제로 던진 셋째 갈래 질문에 대한 반례입니다. 다만 Lev는 이것을 확고한 추측보다 열린 질문에 가깝게 적었습니다.

**파일 이름.** 직접 구하신 파일은 `docs/high_ctx/supplied/`에 넣고 이름 앞에 번호를 붙여 주세요(예: `06_Lev2000.pdf`).

## 필수

| # | 참고문헌 | 출처 | 어디서 구하나 | 판정할 것 |
|---|---|---|---|---|
| 1a | OpenAI, *A power saving for square-difference-free sets*, preprint (2026-09-24), with accompanying Lean formalization. | 2611.05267 참고문헌 [14] | github.com/openai/math. 2610.07765 각주가 첫 커밋 `adc7f12…`(2026-10-06)을 가리킵니다. | K6 상한이 N^(1−c)로 바뀌었는지 |
| 1b | OpenAI, *A power saving for intersective polynomial differences with an exponent depending only on the degree*, preprint (2026-10-05). | 2611.05267 참고문헌 [15] | 위와 같은 저장소 | 위와 같음 |
| 2a | E. Naslund, *Square-difference-free sets: exponent 0.75806746*, 2026. Manuscripts and Lean formalization. | 2610.07765 참고문헌 [Nas26] | https://github.com/enaslund/sarkozy-lower-bound-0.758 | K6 하한 기록의 정확한 값 |
| 2b | E. Naslund, Hexagon 사전 공개 논문 hexagon:2610.00151v1 (2026-10-07). 제목은 확인하지 못했습니다. | 1단계 검증 노트 `verify_12.md`. 출처는 Tao의 표와 위키백과 | Hexagon 사이트 | 0.7580758이라는 값이 여기서 나왔는지. 2a와 같은 작업일 수 있습니다. |
| 3a | J. D. Jones, *A lower bound for the Furstenberg–Sárközy problem*, 2026. Manuscript and Lean formalization. | 2610.07765 참고문헌 [Jon26a] | https://github.com/JD-Jones-ASES/fs-lower-bound | K6 하한(0.75806770) |
| 3b | J. D. Jones, *Lower bounds for sets without perfect-power differences*, 2026. Mathematical account and Lean formalization. | 2610.07765 참고문헌 [Jon26b] | https://github.com/JD-Jones-ASES/nk-lean | 위와 같음 |
| 4a | OpenAI, *Quantitative Superexponential Bounds for van der Waerden Numbers*, `openai/math` #160 (2026-09-23). | 1단계 검증 노트 `verify_5.md` | github.com/openai/math | K8 반데르바르덴 수의 최전선. 대조군에서 빠진 #138을 풀었다는 주장 |
| 4b | OpenAI, `openai/math` #164 (2026-09-23). Hindman의 유한합·유한곱 추측 증명 주장. 정확한 제목은 확인하지 못했습니다. | 1단계 검증 노트 `verify_5.md` | github.com/openai/math | K17 최전선 |
| 5 | E. Naslund, *Lower bounds for the Shannon Capacity of Hypergraphs*, manuscript, 2024. | 2406.12290 참고문헌, 2408.02328 참고문헌 [33] | 공개본을 찾지 못했습니다. 저자 웹페이지나 저자에게 직접 요청해야 할 수 있습니다. | K7 캡 세트 하한 2.2208 |
| 6 | V. F. Lev, *Restricted set addition in groups. II. A generalization of the Erdős–Heilbronn conjecture*, Electron. J. Combin. **7** (2000), Research Paper 4, 10 pp. | 2503.09121 참고문헌 [Lev00b] | EJC 누리집(무료 공개) | Ouyang의 구성이 Lev 추측의 반례인지 |
| 6′ | V. F. Lev, *Restricted set addition in groups. I. The classical setting*, J. London Math. Soc. (2) **62** (2000), no. 1, 27–40. | 2503.09121 참고문헌 [Lev00a] | 학교 도서관 | 6에 추측 원문이 없을 때만 필요합니다. |
| 7 | B. Green, T. Tao, T. Ziegler, *Erratum for "An inverse theorem for the Gowers U^{s+1}[N]-norm"*, manuscript. | 2402.17994 참고문헌 [GTZ24] | Green 또는 Tao 웹페이지 | K3. 2402.17994가 고친 명제 8.3에 기댑니다. |
| 7 원논문 | B. Green, T. Tao, T. Ziegler, *An inverse theorem for the Gowers U^{s+1}[N]-norm*, Ann. of Math. (2) **176** (2012), 1231–1372. | 2601.01682 참고문헌 | arXiv:1009.3998. 이 번호는 제가 직접 받을 수 있습니다. | 참고용 |
| 8 | B. Green, *100 open problems*, manuscript. | 2601.01682 참고문헌 [Green100] | https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf | K3, K10, K15가 인용하는 문제 문구(문제 6, 30, 56) |

**7번 주의.** arXiv 1009.3998의 최신판 v5(2026-04-23)에는 "보조정리 13.2의 잘못을 고쳤다"는 설명이 붙어 있습니다. 하지만 2402.17994(2024)가 인용하는 정오표는 명제 8.3의 오류를 다룹니다. 그래서 v5와는 다른 문서로 보입니다. 정오표가 따로 없고 v5만 있다면 v5를 알려 주세요.

## 선택: 배경 이해용

| 참고문헌 | 출처 | 비고 |
|---|---|---|
| ChatGPT 6.0 Astra, *An analytic proof for two colors* (대화 기록). | 2609.34676(Leng) 참고문헌 [1] | AI가 증명을 찾은 1차 자료입니다. 공개 주소는 논문에 없습니다. |
| T. Tao, V. H. Vu, *Additive Combinatorics*, Cambridge Stud. Adv. Math. **105**, Cambridge University Press, 2006 (paperback 2010). | 여러 논문 | 교과서 |
| T. Tao, *Continued fractions, Bohr sets, and the Littlewood conjecture*, blog post, 2012-01-03. | https://terrytao.wordpress.com/2012/01/03/continued-fractions-bohr-sets-and-the-littlewood-conjecture/ | 웹 글 |
| F. A. Behrend, *On sets of integers which contain no three terms in arithmetical progression*, Proc. Nat. Acad. Sci. U.S.A. **32** (1946), 331–332. | 2406.12290 | 고전 |
| I. Z. Ruzsa, *Difference sets without squares*, Period. Math. Hungar. **15** (1984), no. 3, 205–209. | 2608.01325 | 고전 |
| P. Erdős, R. L. Graham, *Old and new problems and results in combinatorial number theory: van der Waerden's theorem and related topics*, Enseign. Math. **25** (1979), 325–344. | 2606.02541 | 고전 |
| H. Lefmann, T. Thiele, *Point sets with distinct distances*, Combinatorica **15** (1995), 379–408. | 2605.03181 | 고전 |

정독판의 선택 목록에 있던 나머지 고전(Abbott 1990, Martinet 1978, Sánchez-Flores 1998, Erdős–Nathanson 1988)과 Hunter 세미나, Cameron 문제 페이지는 받아 둔 원본에서 정확한 서지를 찾지 못했습니다. 필요해지면 따로 찾겠습니다.
