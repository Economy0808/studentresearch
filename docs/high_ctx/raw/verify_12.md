# 검증 결과: group1.md (K1–K4), group2.md (K5–K8) (2026-11-06)

방법: 각 논문의 arXiv 초록 페이지 원문(HTML)을 내려받아 제목·저자·제출 이력·초록을 기계적으로 뽑았고, 쟁점이 있는 논문은 arXiv HTML 본문(버전 지정)을 텍스트로 바꿔 해당 문장을 직접 찾았습니다(요약 모델 경유 아님). 최신성 점검은 arXiv API의 제출일 역순 검색과 Tao의 "optimization constants" 표(4a 캡 세트, 4b 사르쾨지)로 했습니다. 서지(번호·제목·저자·v1 날짜)는 아래 모든 항목에서 조사 파일과 일치했고, 철회된 논문은 없습니다.

| arXiv | 키워드 | 판정 | 고칠 내용 |
|---|---|---|---|
| 2603.27045 | K1 | 수정 필요 | 불일치 해소됨. v1 정리 1.4는 Z/NZ(N 홀수)와 (log log N)^{-1}, v3 정리 1.4는 {1..N}과 (log log N)^{-1/6}. 어느 쪽이든 {1..N}에서 1/6 성립. "1/2+o(1)" 대신 v3 문구 "1/2−o(1)" |
| 2406.12290 | K1, K7 | 확인 | C=2√log₂(24/7), F_p^n에서 c<√(7/24)≈0.540, "7/24는 개선될 법함"(plausible) 모두 본문과 일치 |
| 2402.17995 | K2, K5, K8 | 확인 | 초록과 일치(v2, 13쪽) |
| 2509.22962 | K2, K3 | 확인 | 2025 JMM Current Events Bulletin 수반 글(26쪽) |
| 2402.17994 | K3 | 확인 | 초록, Green 인용("perhaps the biggest open question") 일치. 단 아래 K3 요약 수정 참고 |
| K3 최전선 요약 | K3 | 수정 필요 | "다항식 손실 역정리는 어느 차수에서도 모름"은 틀림(유한체 U^3은 PFR로 다항식). 2026 후속 3편 누락 |
| 2601.01682 | K3 | 확인 | Question 1.9(Jamneshan–Shalom–Tao), almost-trilinear, 5항 변형 "plausible" 모두 본문과 일치 |
| 2504.07006 | K4 | 수정 필요 | `[미확인]` 해제: FOCS 2025 최우수 논문 공동 수상 확인. "남은 경계 3"(정수 [N]² 판)은 열린 문제가 아님: 본문에 Z/4NZ 임베딩으로 같은 결론이 난다고 적혀 있음 |
| 2404.07380 | K4 | 확인 | v3(2025-09)가 Discrete Analysis 게재본(27쪽) |
| 2411.15137 | K2, K4 | 확인 | 초록과 일치 |
| 2505.16822 | K5 | 확인 | v2(2025-11-11) 있음. "remains an open challenge" 문장 일치 |
| 2506.13010 | K5 | 확인 | 정리 1.1의 세 경우, Remark 1.2 "can likely be improved", Leng 추측 1–3과 추측 1 반례 모두 일치 |
| 2608.01325 | K6 | 확인 | α*=0.7527964558…, 열 개 (p,t) 쌍, 조건 t(p)<p^{0.50559…} 일치. 이전 지수 표기는 0.7334117…(…118 아님) |
| 2610.07765 | K6 | 수정 필요 | AI 공개를 더 정확히: 정리 1.3(방법의 한계) 증명은 LLM과의 대화에서 발견됐다고 저자가 밝힘. OpenAI 초안을 "인정하지 않는다"는 과장. 저자들은 초안이 읽기 어렵다는 것과 제출 시각만 지적하고 정오는 판단하지 않음 |
| 2611.05267 | K6 | 수정 필요 | 이 논문에는 "AI 논쟁"이 없음. OpenAI 사전 공개 논문 [14][15]를 "claiming"으로 중립 인용만 함. "거듭제곱 절약 최초 사례 중 하나"는 "순수 거듭제곱 하나(세제곱)에 대한 거듭제곱 절약"으로 좁혀야 함 |
| 2605.16216 | K6 | 수정 필요 | 불일치 해소됨. 현재 v2의 초록과 정리 1.1은 모두 0<μ<1/2(등호 없음). "≤1/2"은 arXiv 코멘트 칸의 저자 메모일 뿐임. v1은 μ<1/4. μ=1/2은 "seems hopeless" |
| 2411.17448 | K6 | 확인 | v2에서 지수 1/4−o(1)→1/2. "major open question"과 "yes일 것으로 추측" 일치 |
| OpenAI 사전 공개 논문 2편 | K6 | 확인 불가 | arXiv에 없음. Tao 표 4b는 OAI2026(2026-09-24자, 10-06 공개)을 현재 위쪽 한계 N^{1−c}로 올려 둠. 정오는 독립 검증하지 못함 |
| K6 아래쪽 최전선 | K6 | 수정 필요 | arXiv 최고는 0.7528(Krachun). arXiv 밖 기록은 Naslund 0.7580758(Hexagon 사전 공개 논문, AI 작성, Lean 검증)이고 Tao 표와 위키백과가 현재 최고로 기재. N^{1−ε} 추측은 "Erdős식"이 아님 |
| 2606.12194 | K7 | 확인 | Remark 4.1 "452nd decimal place", Conjecture 4.4 일치. 현재 기록 출처로 X-evolve(2508.07932)를 인용 |
| 2408.02328 | K7 | 확인 | 본문에 Naslund [33] (2.2208)^n 인용 확인. 근거는 "Lower bounds for the Shannon Capacity of …" 원고 |
| 2508.07932 / 캡 세트 하한 | K7 (K1) | 수정 필요 | 2.2203은 초록에서 확인. 2.2208은 출처를 찾지 못해 확인 불가. group1 K1 "남은 경계 4"의 2.2180도 낡은 값 |
| 2606.02541 | K8 | 확인 | 정리 1·2·3, Bae 독립 결과, "not aware of any way to construct" 일치. "remains open" 인용은 원문이 아닌 의역 |
| 2609.31798 | K8 | 확인 | 초록 일치. 위쪽 exp(O((log k)^6(log log k)^6))은 Raghavan 초록식에서 유도한 값(v3 정리 1.4를 쓰면 (log k)^6·log log k) |
| 2608.20824 | K8 | 수정 필요 | 초록은 "채색"만 ChatGPT 5.6 Sol Pro가 찾았다고 씀. 서론은 채색과 한 증명이 ChatGPT 질의로 생성됐다고 쓰지만, 실린 증명과 글은 저자들 것이라고 명시함 |

## 항목별 설명

**2603.27045 (Raghavan), 구간 대 Z/NZ: 해소.** v1 HTML 정리 1.4는 "N>1 홀수, A⊆Z/NZ, |A|≤exp(−Ω(log(N)^{1/6}·log log(N)^{−1}))N"입니다. v3(2026-05-15) 정리 1.4는 "A⊆{1,…,N}, |A|≤exp(−Ω(log(N)^{1/6}·log log(N)^{−1/6}))N"입니다. {1..N}은 홀수 법 약 2N의 Z/N'Z 안에 넣을 수 있으므로 Z/NZ 판에서 구간 판이 바로 나옵니다. 그래서 "1/6 지수가 {1..N}에서 성립한다"는 두 버전 모두에서 맞습니다. 남은 사소한 어긋남이 있습니다. v3 초록은 아직 log log의 지수를 −1로 쓰고 v3 정리는 −1/6로 써서, 정리 쪽이 조금 더 강합니다. 팩에는 v3 정리 1.4를 쓰는 것이 안전합니다. 서론의 열린 질문 문장은 v3에서 "exp(−log(N)^{1/2−o(1)})"로 고쳐졌으므로 조사 파일의 "1/2+o(1)"을 바꿔야 합니다. "로그 두 번 손실" 서술은 원문과 일치합니다.

**K3 최전선 요약.** (1) "다항식 손실 역정리는 어느 차수에서도 일반적으로 모른다"는 정수 [N]의 U^3 이상에 대해서만 맞습니다. 유한체 F_p^n의 U^3 역정리는 다항식 정리 PFR(Gowers–Green–Manners–Tao, 2023)로 다항식 손실이 이미 알려져 있습니다(일반 지식이며 이번에 원문을 열어 확인하지는 않음). 범위를 "정수 설정에서"로 한정하기를 권합니다. (2) 2026년 후속을 다음과 같이 보탭니다. 아래는 모두 arXiv 초록 확인입니다.
- Milićević 2609.33733(2026-09-27): p≥k일 때 모든 U^k(F_p^n)의 준다항식 역정리. 2410.08966의 U^4를 모든 차수로 넓힘.
- Jamneshan–Shalom–Tao 2601.00961(2026-01-02): 유계 지수 군에서 정성적 역정리.
- Candela–González-Sánchez–Szegedy 2601.08810: 유계 랭크 유한 아벨군에서 Jamneshan–Tao 추측 증명.
- Milo–Moshkovitz 2603.16836: 차수 d+1 다항식에 대한 "거의 다항식" U^d 판.
따라서 "남은 경계 2"(일반 유한 아벨군 U^5 이상)는 아직 열려 있지만, 유한체 고표수 경우는 2609.33733이 이미 답했습니다.

**2504.07006 (코너).** FOCS 2025 Best Paper Award 공동 수상작 3편 중 하나임을 focs.computer.org/2025/best-paper-awards 페이지에서 확인했습니다. 서론에는 "By embedding [N] into the cyclic group Z/(4N Z) one may obtain a similar conclusion for corner–free subsets of [N]×[N]"이 있습니다. 따라서 K4 "남은 경계 3"은 열린 문제가 아니므로 지워야 합니다. 1/600과 1/178, "approaching the 1/2 exponent"를 얻지 못한다는 문장은 원문과 일치합니다. 초록에는 지수가 Ω(1)로만 적혀 있다는 점을 덧붙이면 좋습니다.

**2605.16216: μ≤1/2 대 μ<1/2, 해소.** 초록 본문은 "for every 0<μ<1/2"이고, 정리 1.1도 "Let 0<μ<1/2"입니다. 조사자가 본 "≤1/2"은 초록이 아니라 arXiv 코멘트 칸("…for any 0<μ\leq 1/2 from 0<μ\leq 1/4")에 있습니다. 본문 경과 설명을 보면 범위가 v1의 μ<1/4에서 중간 초안의 μ<1/3을 거쳐 v2의 μ<1/2로 넓어졌습니다. 본문은 "Achieving μ=1/2 … seems hopeless with current technology"라고 씁니다. 결론적으로 정답은 **μ<1/2(등호 없음)**이고, 코멘트 칸의 ≤는 저자 쪽 표기 오류로 보입니다. 이 결과는 일반 교차 다항식에 대한 것이고, 제곱만 보면 Green–Sawhney(μ=1/2)와 Fan–Lott가 더 강합니다.

**사르쾨지 문제, 현재 최고 상·하한(2026-11-06 기준).**
- 위쪽, arXiv 기준: Fan–Lott 2610.07765, |A|≤N·exp(−c√(log N·log log N))입니다. 같은 논문은 van der Corput 방법으로는 이보다 나아질 수 없다는 것도 증명했습니다(a₀≥exp(−C√(log N log log N))).
- 위쪽, arXiv 밖: OpenAI "A power saving for square-difference-free sets"가 |A|≤CN^{1−c}를 주장합니다. 2026-09-24자 문서이고 10-06에 공개됐습니다. Tao 표 4b는 이를 위쪽 한계 "1−c"로 올려 두었고, c의 값은 쓸모 있게 나오지 않는다고 적었습니다. 2611.05267(Ruzsa·Matolcsi 공저)은 "claiming"으로만 인용합니다. 독립 검증은 못 했으므로 `[미검증]` 표시를 유지합니다.
- 아래쪽, arXiv 기준: Krachun 2608.01325, 지수 0.7527964558…입니다.
- 아래쪽, arXiv 밖: Naslund 0.7580758(Hexagon 사전 공개 논문 hexagon:2610.00151v1, 2026-10-07)입니다. 논문에 GPT-6-Astra가 쓰고 Claude Opus 5.5가 고쳤다고 공개되어 있고 Lean 형식 검증이 있습니다. 그 밖에 Jones 0.75806770413(논문 없음, Lean 검증)과 Jones 0.753742가 있습니다. Tao 표와 위키백과는 모두 0.7580758을 현재 최고로 적고 있습니다.
- 조사 파일 고칠 점: K6 "아래쪽 현재 arXiv 최고 0.7528"은 맞습니다. 다만 "현재 알려진 최고"는 0.7580758(AI 생성, arXiv 밖)이라고 따로 밝혀야 합니다. 또 "Erdős식 추측 D(N)≥N^{1−ε}"는 출처를 잘못 붙였습니다. 에르되시의 추측은 반대 방향(N^{1/2}·polylog)이었고 Sárközy와 Ruzsa가 반증했습니다. N^{1−ε} 추측은 위키백과가 다른 문헌에 근거를 두고 적은 것이며, OpenAI 주장이 맞다면 이 추측은 거짓이 됩니다.

**2610.07765 (Fan–Lott), AI 공개.** 원문은 이렇습니다. "used a large language model (LLM) as a sounding board … The proof of Theorem 1.3 was discovered during later conversations with the LLM … the manuscript was prepared and verified by the authors". 즉 "방법의 한계" 정리의 증명 착상이 LLM에서 나왔습니다. AI 산출과 인간 산출을 구분하려는 이 연구에서는 이 사실을 표에 명시해야 합니다. OpenAI 초안에 대해서는 "appears to be AI-written and largely unreadable"이라고 쓰고, 자신들의 v1이 그 커밋보다 16시간 56분 15초 앞섰다고 적었을 뿐입니다. 정오를 부정하지는 않았습니다.

**2611.05267.** 본문의 OpenAI 언급은 "Very recently, OpenAI [14] released a preprint claiming such a bound."와 참고문헌 [14], [15]뿐입니다. 거듭제곱 절약은 이전에도 있었습니다. 소수−1 차이(Green), 두 제곱의 합(Fan–Lott 2606), 홀수 거듭제곱의 짝수 개 합(Kalogirou 외 2609) 등입니다. 이 논문의 새로움은 "세제곱이라는 단일 거듭제곱"에 대한 것입니다. 세제곱의 열린 질문(D₃(N)~CN^γ, 극한 존재)은 원문과 일치합니다.

**캡 세트 하한 2.2203 대 2.2208.**
- 2.2203: X-evolve 초록에서 "C ≥ 2.2203"을 확인했습니다. Tao 표 4a의 최고값도 2.2203입니다. Hametner–Tyrrell(2026-06, Tyrrell은 2.2180 기록 보유자)도 "현재 기록"으로 X-evolve를 인용합니다.
- 2.2208: Croot–Lev–Pach 서베이(2024-08)가 "Naslund [33] … (2.2208)^n"을 인용하는 것은 확인했습니다. 근거 원고 "Lower bounds for the Shannon Capacity of hypergraphs"는 웹 검색으로 찾지 못했습니다.
- 정리하면, 이 원고는 X-evolve(2025-08)보다 앞서는데도 이후 문헌들이 2.2203을 기록으로 취급합니다. 2.2208은 공개 검증된 값으로 쓰기 어렵습니다.
- 권고: "2.2203(arXiv, 공개 검증), 2.2208은 서베이가 인용한 미공개 원고로 확인 불가"로 적습니다. group1 K1 "남은 경계 4"의 "2.2180(Tyrrell)"도 2.2203으로 고칩니다.
- 관련 신규 논문: Karingula–Lovett 2609.27044(2026-09)는 k≥4에서 slice rank 방법이 지수적 절약을 줄 수 없음을 보였습니다. 서베이 "Directions"의 열린 질문 2(k≥4에 대수적 방법을 쓸 수 있는가)에 부분적으로 답하므로 K7 "남은 경계 2"에 덧붙일 만합니다. Bucić–He–Lee 2610.26686(2026-10)은 Erdős–Szemerédi 해바라기 추측을 모든 k≥3에서 증명했다고 주장합니다. k=3은 캡 세트에서 따라 나오던 경우입니다.

**2608.20824 (Campos–Fox–Schildkraut), 실제 주장.**
- 초록: "The coloring for general k can be viewed as a product of Berlekamp's colorings for various primes. It was found by ChatGPT 5.6 Sol Pro." 초록이 말하는 것은 채색뿐입니다.
- 서론: "The coloring used to prove Theorem 1, as well as a proof of Theorem 1, were generated by a query to ChatGPT 5.6 Sol Pro. The proof we present, while drawing somewhat on the proof given by ChatGPT, was produced by the authors … All of the writing is our own."
- 따라서 조사 파일의 "초록에 ChatGPT가 채색과 증명을 만들었다고 밝혀 있습니다(본문 서론도 같은 문장)"는 고쳐야 합니다. 정확히는 이렇습니다. 채색과 최초 증명은 AI가 만들었고, 논문에 실린 증명과 글은 저자들이 Berlekamp 증명 해설을 고쳐 다시 썼습니다.
- 주정리 w(k)≥(1−o(1))k2^{k−1}과 "Erdős 추측 lim w(k)/2^k=∞ 확인"은 원문과 일치합니다.

**2609.31798 (Cao).** 위쪽 한계 exp(O((log k)^6(log log k)^6))은 Cao가 Raghavan의 r₃ 상한을 초록 형태(log log의 −1제곱)로 대입해 유도한 것입니다. 원문에 그대로 있으므로 인용은 맞습니다. Raghavan v3 정리 1.4를 쓰면 (log k)^6·log log k로 조금 좋아진다는 점만 각주로 두면 됩니다.

**대조군 겹침.** 팩 추천 논문 중 대조군 Erdős #28, #30, #36, #39, #52, #66, #200, #241, #324를 주로 다루는 논문은 없습니다. 이 9개는 시돈 집합, 합-곱, 덧셈 기저 표현 수, 소수 등차수열 길이, 최소 겹침, 다항식 시돈 같은 주제입니다(이 저장소 hakjayeon_guide.html의 대조군 표와 대조). 2608.20824의 "Erdős 추측"(w(k)/2^k→∞)과 2604.20588의 #190은 대조군 목록에 없습니다.

**최신성 점검(한 번 검색).** arXiv API를 제출일 역순으로 검색한 결과는 다음과 같습니다.
- K1 Roth 상한 1/6, K2 k≥5, K4 코너 1/600, K8 w(k;3), w(3,k): 조사 파일보다 새로운 갱신을 찾지 못했습니다.
- K3: 위 "K3 최전선 요약" 항목의 2026 논문 4편이 누락되어 있습니다.
- K5: Zhao 2610.13204(x, x+y, x+y² 비선형 Roth)가 새로 나왔습니다. 다만 그 한계 N·exp(−c(log log N)^β)는 Peluse–Prendiville의 기존 다항로그 한계보다 약해 보이므로 팩 후보로 권하지 않습니다(초록만 확인).
