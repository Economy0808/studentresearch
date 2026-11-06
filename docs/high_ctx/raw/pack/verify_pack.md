# 고컨텍스트 팩(세 줄기) 독립 검증 기록

기준일 2026-11-06. 대상: `pack/additive_comb_high_lineages.md`(초안) → `pack/additive_comb_high_lineages_v2.md`(고친 판).
방법: 정리 진술은 arXiv LaTeX 원본(`...spare-guGKTj\...\scratchpad\src\*.tex`)과, Lev 2000·Green 100은 `gh.psVy\files\*.txt`와 대조했습니다. 원본 폴더에 없는 논문은 arXiv API로 초록·코멘트를 보고, 필요한 6편(2609.27044, 2501.10203, 2404.09639, 2605.13628, 2610.03750 외 API 메타데이터)은 PDF를 `gh.psVy\verify_dl\`에 받아 텍스트로 읽었습니다. 2026년 해결 논문은 API `search_query`(줄기별 키워드 20여 개, 제출일 내림차순)로 점검했습니다. 받은 파일 속 지시문·코드는 따르거나 실행하지 않았습니다.

분량: 초안 4,900단어 → v2 5,150단어 안팎(`## Result:` 세 절 각 1,380 / 1,330 / 1,310단어, 서식 예시 120단어). 절 구조와 순서는 그대로입니다.

## 1. 고친 곳 (24곳)

| # | 위치 | 원래 | 고침 | 근거(원본 위치) |
|---|---|---|---|---|
| 1 | 맨 윗줄 제목 | `# DRAFT — additive combinatorics pack (high context, three lineages)` | `# DRAFT — additive combinatorics pack` | **실험 조건 유출.** `pipeline.parse_context`가 파일 전체를 프롬프트에 넣으므로 "high context"가 모델에게 보입니다. 저컨텍스트 팩·`context/README.md` 규격의 제목과 같게 맞춤 |
| 2 | L1 정의 "3-AP-free" | $r_3(N)$ is the integer case $G=[N]$ | 정수 경우(부분집합 of $[N]$) | $[N]$은 군이 아님(표기 정리) |
| 3 | L1 Origin | Erdős and Turán posed in 1936 … | 이름을 빼고 "posed in 1936 (2603.27045, Question 1.1); Roth (1953) …" | 사실은 맞음(2603.27045 tex 75행). 대조군 "Erdős–Turán 추측"과 이름이 겹쳐 연상 위험이 있어 보수적으로 뺌(**판단**, 되돌려도 사실 오류는 아님) |
| 4 | L1 Milestones, 하한 | Elkin (2010, Israel J. Math. 184) … gain of $(\log_2N)^{1/4}$ | Elkin (Israel J. Math. 184, **2011**); Behrend의 $o(1)$에 숨은 $(\log_2N)^{-1/4}$ 손실을 $(\log_2N)^{1/4}$ 이득으로 | 2406.12290 tex 117행(본문 "In 2010"), 참고문헌 600행(2011, 93–128) |
| 5 | L1 Kelley–Meka | "the survey 2408.02328 quotes exponent $1/11$"; Bloom–Sisask "by a better bootstrapping step" | 1/11 언급 삭제. 지수 1/12는 2603.27045·2406.12290·Bloom–Sisask 해설(2302.07211)이 모두 적는 값임을 밝힘. Bloom–Sisask는 "simple modification" | 2603.27045 tex 정리 1.2; 2406.12290 tex 107행; arXiv API 2302.07211 초록(1/12), 2309.02353 초록(1/9). 서베이 2408.02328 tex 127행의 1/11은 서베이 쪽 오기로 판단 |
| 6 | L1 캡 세트 하한 | $2.2202^n$ (Romera-Paredes et al., Nature 2024; quoted in 2406.12290) | 저자·학술지 삭제. "admissible set을 더 잘 찾아 얻은 값: 2.2202(2406.12290이 인용), 현재 기록 2.2203…(2606.12194가 인용)" | **수칙 1·2.** 2.2202·2.2203은 AI 탐색 결과(2406.12290 tex 143행 "using artificial intelligence", 2606.12194 tex 145행 FunSearch·X-evolve). 사람 논문이 인용한 수치만 남김 |
| 7 | 같은 항목, $\mathbb F_5^n$ | Elsholtz–Lipnik–Siebenhofer, Pollak | Elsholtz, Proske, Pollak, Lipnik, Siebenhofer; $(35^{1/3})^{n-o(n)}$ | 2406.12290 tex 143행("the first and third author, Pollak, Lipnik and Siebenhofer"), 2606.12194 tex 370행 |
| 8 | 같은 항목 | "refined to $o(n)$ error by Elsholtz–Pach 2020" | "the best explicit $o(n)$ term is due to Elsholtz–Pach (DCC 88, 2020)" | 2406.12290 tex 131행: $o(n)$ 항의 최선 정량값이 Elsholtz–Pach |
| 9 | L1 Raghavan 항목 끝 | 리터럴 `\n- *Hametner–Tyrrell…`(줄바꿈이 문자로 들어가 두 항목이 한 줄) | 항목 분리, 정리 1.5에 "저자가 새롭지 않다고 적음" 추가 | 서식 오류. 2603.27045 tex 정리 1.5 아래 문단 |
| 10 | L1 Hametner–Tyrrell | "with $r>|A|^2$ this beats $|A|^{1/n}$" | 좌표당 비율 $|B|^{1/(2nr)}$이 $|A|^{1/n}$을 넘음 | 2606.12194 tex 156–163행(정리 1.1·따름정리 1.2) |
| 11 | 같은 항목 | genus-one 조건 일부 생략 | $s\ge3$ 변수, $q$는 소수 거듭제곱 명시 | 2606.12194 tex 167–177행(정리 1.3) |
| 12 | L1 Where the methods stop 마지막 | "a 2026 preprint (arXiv:2609.27044, Karingula–Lovett) is reported to show the slice-rank method cannot give exponential savings for $k\ge4$" | 삭제. 대신 Green Problem 9(iii)의 현황 문장과 Conlon–Fox–Pham(2605.13628, 2026-05)의 제한 공차 결과(0∈S, $|S|>(q+1)/2$이면 $q^{(1-\varepsilon_q)n}$; $\{0,1\}\subset\mathbb F_3$는 제외됨) | **수칙 2.** 2609.27044 PDF: 저자 소속 "Agentin AI", 본문 "AI methodology" 단락(ChatGPT-6 Astra로 증명 전략 탐색·논증 점검, 다중 AI 에이전트). 내용(초록) 자체는 초안 서술과 일치했으나 AI 관여로 제외. Green 100 Problem 9(iii) 주석; 2605.13628 초록·정리 1(감사의 글 없음, AI 언급 없음) |
| 13 | L1 Known open questions 5 | "(see the partial negative result above)"; "per Green's list, Bhangale–Khot–Minzer and Liu showed …" | AI 논문 참조 삭제. Green Problem 9(iii) 질문, Problem 17(2025 갱신: Bhangale–Khot–Liu–Minzer, Green은 지수적으로 작은 밀도도 가능하다고 봄), Conlon–Fox–Pham Problem 8($|S|=\lfloor(q+1)/2\rfloor$부터 범위 개선) 추가 | green_100.txt 593–631, 810–815행; 2605.13628 텍스트 162–165행 |
| 14 | L1 Where the methods stop 둘째 | "if so, one logarithm of loss would remain" | "가능하더라도 $\mathbb F_q^n$와 $\mathbb Z/N\mathbb Z$ 사이에 로그 하나의 손실은 있어야 한다" | 2603.27045 tex 188행 |
| 15 | L2 Origin | Freiman 정리: "lies in a proper generalized progression of dimension $O_K(1)$ and size $O_K(|A|)$" | "$O_K(1)$개 평행이동의 (볼록) 진행으로 덮이고, 특히 $A$의 큰 부분이 유계 차원 고유 진행에 들어감" | 2512.11217 tex 86행(정리 1.1), 2604.25893 서론("large subset contained in") |
| 16 | L2 Milestone 1 | "(the $3k-4$ theorem; …)" | "Freiman's $3k-3$ theorem for difference sets" (Lev–Smeliansky, Acta Arith. 70, 1995) | 2604.25893 서론: $|A-A|<3|A|-3$ 진술을 "Freiman's $3k-3$ theorem"이라 부름; 참고문헌 LS1995 |
| 17 | L2 Current frontier, Raghavan | 최소화 범함수 $d[X;Y]+\frac{\eta}{\log\log 3K}(\dots)$ | $\tau[X;Y]=d[X;Y]+\frac{\eta}{\log_2(3K)}(d[X;U_A]+d[Y;U_A])$, $X,Y$는 $A$ 위, 합과 섬유만 사용(끝마무리 없음) | 2512.11217 tex 247–248행(정의, $\eta=1/438$) |
| 18 | L2 Where the methods stop, Small doubling | "The density thresholds $1/2$ in the lemmas are sharp." | 1차원 Bogolyubov형 보조정리($|X|>|P|/2$이면 $P\subseteq5X-4X$)의 1/2가 날카로움, 예 $P=[2l]$, $X=2\cdot[l]$ | 2604.25893 tex 354행 |
| 19 | L3 Origin | "see also Erdős–Graham 1980, p. 95" | 쪽수 삭제("also in the Erdős–Graham problem book, 1980") | p. 95를 어떤 원본에서도 확인 못 함. Lev 2000 참고문헌 [5] |
| 20 | L3 Pollard | "number of residues with at least $i$ representations $a+b$" | "$c=a+b$로 적어도 $i$가지로 쓰이는 잉여류의 수" | 대조군 키워드("표현 함수·표현 수") 회피(**판단**). 진술은 Lev 2000 텍스트 537행과 일치 |
| 21 | L3 Dias da Silva–Hamidoune | "in two-set form $|A\dot+B|\ge\min\{|A|+|B|-3,p\}$" | Erdős–Heilbronn 추측의 증명; 두 집합 형태는 Lev가 적은 진술이라고 구분 | Lev 2000 텍스트 7, 20–24행; 2503.09121 tex 서론 |
| 22 | L3 Bollobás–Leader–Tiba | 정리 35와 대칭 결과를 한 문장에 섞음("for symmetric $R$, …") | Thm 35: 차수 $d(n)=o(n)$, $|A|\le(1-\varepsilon)p/2$, 크기 $\le c$의 $A'$. Thm 9: **고정** $d$, 대칭 $R$, $n_0(\varepsilon,d)\le|A|<(1-\varepsilon)p/2$ | 2503.09121 tex 서론 정리 1.3·따름정리 1.4(BLT22 Theorem 35, 9 인용) |
| 23 | L3 Known open questions 3 | "Lev (2000): the exact threshold … in the third line of (Q) and the truth of the second line; …" | Lev가 물은 것(식 (Q)의 참, 임의 유한군, 최선 하한, 계수 $1-\delta$→1 또는 $1-\varepsilon$, $B=A$에서 0.80)과 지금 남은 것(둘째 줄, 셋째 줄의 올바른 문턱—Ouyang이 $(1+\delta)p$ 필요를 보임)을 구분 | Lev 2000 텍스트 165–191, 517, 747, 756행; 2503.09121 tex(추측 1.13 뒤 문단) |
| 24 | L3 Known open questions 6 | "the corrected Bukh conjecture … for general $k$" | 기약·서로소 조건 명시, $k=1$은 Conlon–Lim 이전 논문이 해결 | 2508.18586 tex 176–197행 |

## 2. 원본과 대조해 확인만 된 주요 진술

**L1 (3항 등차 없는 집합)**
- Kelley–Meka 지수 **1/12**(2603.27045 정리 1.2, 2406.12290 107행, 2302.07211 초록), Bloom–Sisask **1/9**(2309.02353 초록, 2603.27045 정리 1.3), Bloom–Sisask 2020 $N/(\log N)^{1+c}$(2007.03528 초록).
- Raghavan 정리 1.4: $\exp(-\log(N)^{1/6-o(1)})N$, 정밀형 $\exp(-\Omega(\log^{1/6}N\,(\log\log N)^{-1/6}))N$; 초록은 $\log\log$ 지수 $-1$(더 약한 서술). 정리 1.5 $\mathbb F_q^n$ 1/5, "not a new result". 5단계 설계, 반복 체질, 반지름 추적, "no known analogue"(101행), 로그 손실 문단(188행). 감사의 글에 AI 없음.
- EHPS: $C=2\sqrt{\log_2(24/7)}\approx2.667$, 증명 하한 $N2^{-C\sqrt{\log_2N}}/(10^9(\log_2N)^{3/2})$(309행), 정리 1.2(소수 $p$, $n$이 $p$에 대해 충분히 큼), $c<\sqrt{7/24}$, 정리 1.3 상수 $10^6m^2n^3$, 명제 2.2($T$, $f:T\to[0,100/\varepsilon^2]$), 측도 0, $x-y$로는 거짓, "somewhat ad-hoc", $c=1/2$ 장벽, $c\approx0.85$ 대 0.540 간격, EG의 $c_p\to0.841$.
- Croot–Lev–Pach $3.611^n$, Brown–Buhler 1982, Frankl–Graham–Rödl 1987, Meshulam 1995, Lev 2004 $2|G|/\mathrm{rank}(2G)$, Lev 2012 조합적 증명, Sanders 2009($\mathbb Z_4^n$), Bateman–Katz, Roth $N/\log\log N$, Heath-Brown·Szemerédi $0<\delta<1/2$, Bourgain 1999·2008, Sanders 2011·2012, KM의 $\mathbb F_p^n$ $2^{-\kappa_pn^{1/9}}$(2408.02328 182–185행).
- 캡 세트: Edel 2004(2.217389), Tyrrell 2023(2.218, Discrete Anal. 2023:20), 상한 2.7552(2606.12194 140행), 현재 하한 2.2203…(145행).
- Hametner–Tyrrell 정리 1.1($|B|=r|A|^{2r-2}$, $\mathbb F_3^{2nr}$), 보조정리 2.1 구성($A_1=A\times A$, $A_2=T(A_1)$, $B_j=A_1^{j-1}\times\{0\}^{2n}\times A_2^{r-j}$), 정리 1.3의 $d$, Remark(452번째 자리, $d=39\to6$, $p>5$와 $\mathbb F_5^n$ 기록을 못 넘음), 계 방정식 추측.
- 2408.02328 §5 Directions 다섯 항목. Green 100(2025-12 갱신) Problem 9·17 주석.

**L2 (작은 배가 집합)**
- 2512.11217: 정리 1.4 $f(K)=O(\log(3K)\log\log(3K))$, 추측 1.5 $O(\log 2K)$, Green–Ruzsa $O(K^4\log^{O(1)}2K)$, Sanders·Konyagin $O(\log^{3+o(1)}2K)$, Sanders Bogolyubov 차원 $O(\log^6 2K)$·크기 $\exp(-O(\log^{6+o(1)}2K))$, Manners(타원체 동치, 1709.09738 초록), Lovett–Regev(상자형 거짓), $m^3\gg\log\log K$ 비교, 약한 PFR, 정리 1.8(홀수 위수 $U^3$, 같은 모양 미달), Prendiville 확장 관심, §5 장벽(가우시안, Courtade–Fathi–Pananjady, 로그 오목, Kac–Bernstein, "may be within reach", "without any new ideas"). 참고문헌 연도·권호(Freiman 1966/1973, Ruzsa 1994/1999, Green–Ruzsa 2007, Sanders 2012/2013, GGMT Ann. of Math. 201 (2025)).
- 2404.02244: 정리 1.1($(2K)^{O(m^3)}$, $\ell\ll(2+m\log K)^{O(m^3\log m)}$), Liao 각주($2K^{11}$ 다음 $2K^9$; 2404.09639 초록 $C=9$), Sanders $\exp(-C_m\log^4 2K)$, Konyagin $\exp(C_{m,\varepsilon}\log^{3+\varepsilon}2K)$, 다항 Bogolyubov 미달, 따름정리 1.2($\eta^{O(p^3)}$), $\eta=c/m^3$.
- 2604.25893: 정리 1.2 진술, EGM 정리 6.4($1/2+c\varepsilon$, Ann. of Math. 180, 2014), Jin(Adv. Math. 2007), Freiman 10/3 추측(Bolyai 11, 1999), 따름정리($41A-40A$), $A_1=\{0,10N,2^N\}+[N]$의 $|A_1+A_1|=4|A_1|-6$, $\sigma_-\le2d-2+1/(d-1)$, PFR로도 일반 $K$는 안 따라 나옴, 감사의 글에 AI 없음.
- Bloom 2501.11580: $|A+tA|\le K|A|$, 계수 $O(\log K)$, Discrete Analysis 2025(API journal_ref).
- Green 100 Problem 30·49·50(Sanders $\log^{4+o(1)}$, Kościuszko $\log^{3+\eta}$, $[N]$판).

**L3 (제한 합집합, 대수적 배수)**
- Lev 2000(EJC 7 R4): 정리 1 세 경우, 정리 2·3·4, 따름정리 1, Bilu–Lev–Ruzsa(DCG 19, 1998)의 Conjecture 2와 $(k,d)$ 반례($|A|+|B|=p+k+1-d$, $|A+^\tau B|=|A|+|B|-k-1$), 단사 $\tau$에 대한 질문 (2) 세 줄, "Is it true that"·"may not be the case", 예($\lfloor4p/3\rfloor$, $p-2$; $|A|=(p+1)/2$, $p-3$), "major open problem for generic restriction", 0.80.
- Ouyang 2503.09121 v3: 정리 1.5·1.6(상수 $\alpha$, $p_0=4^{10\Delta}$)·1.7($\beta$, $p_0=\exp(O_\varepsilon(\Delta))$), 따름정리 1.8($c_\varepsilon=(\varepsilon/10^{1600})^{10^{6400}/\varepsilon^4}$), 정리 1.9($\lfloor5\Delta/2\rfloor$), 추측 1.10, 정리 1.11(i)(ii)(iii), 따름정리 1.12, 추측 1.13, 정리 1.14, "bottleneck", "$c_\varepsilon$ not linear", 보조정리 4.1과 Remark 4.2, §4 "no advantage". 감사의 글에 AI 없음.
- 셋째 줄 반례 범위: $|A|=6\lfloor p/11\rfloor-3$이면 $2|A|\ge p+2 \iff \lfloor p/11\rfloor\ge r+8$($p=11k+r$)이고, $k\ge18$이면 늘 성립하므로 **모든 소수 $p\ge199$**에서 성립(초안 그대로 맞음). 그보다 작은 157, 167, 179, 181, 191에서도 성립(앞 단계 계산).
- Conlon–Lim 2508.18586: 정리 1.2와 $H$ 정의, 추측 1.1(KP), 교정 Bukh 추측, 기약·서로소·pre-commuting 정의, 정리 1.7, $k=1$ 따름정리, §10(오차 $O(|A|/\sqrt{\log_{(k)}|A|})$, $O(|A|^{1-1/d})$ "likely to be difficult", $O(|A|^{1-\sigma})$, "quite orthogonal", 3×3 예와 $8|A|$, $C|A|$조차 미증명). $H(\sqrt2)=(1+\sqrt2)^2$ 계산 확인.
- Green 100 Problem 2(Sanders $(\log n)^{1+c}$, Beker $c=1/69$, Ruzsa $e^{C\sqrt{\log n}}$), Problem 25(Erdős–Sárközy–Sós 1989). Beker 2501.10203 본문 $c=1/69$, 감사의 글에 AI 없음.

## 3. "Known open questions"가 2026-11 현재 열려 있는가

- L1 1–5: 열림. arXiv 검색("three-term arithmetic progressions", "cap set(s)", "progression-free", "Behrend", "Kelley Meka", "Roth's theorem")에서 2026년 해결 논문 없음. 새로 반영한 부분 진전은 Conlon–Fox–Pham 2605.13628(사람 논문)뿐.
- L2 1–7: 열림. 단 **2512.04433(Kazemi Moghadam, 2025-12, v3)이 정수 PFR을 "해결"했다고 주장**합니다. 채택하지 않았습니다. 단독 저자이고, 진술("$\mathbb Z$에서 지수 $K^{O(1)}$인 부분군")이 정수에서는 사실상 의미가 없으며, 이후의 Raghavan v2(2026-02)와 Jing–Mudgal(2026-04)이 PFR을 여전히 추측으로 다룹니다. 연구자 확인을 권합니다.
- L3 1–6: 열림. 검색("restricted sumset", "Erdos-Heilbronn", "forbidden pairs", "dilates", "Krachun")에서 Lev 질문·Ouyang 추측·Conlon–Lim 질문을 푼 2026년 논문 없음. 2609.14544·2609.10148·2609.23343은 $a\ne b$형 제한 합(Erdős–Heilbronn 임계쌍)이고 Lev의 매칭 질문과 다름. 2608.04760(Freiman–Lev 추측 증명, 정수 $2^\wedge A$)은 팩이 다루지 않는 질문.
- **주의(L3 질문 4, Green Problem 2):** 2610.03750(Yao Zhi, 2026-09)이 Beker의 지수를 개선해 $c<1/36$을 주장합니다. PDF의 "Declaration on the use of artificial intelligence"에 ChatGPT(GPT-5.6 Sol)로 증명 세부와 정량 계산을 반복 점검했다고 적혀 있어 **수칙 2로 넣지 않았습니다**. 그래서 팩의 "$c=1/69$"는 사람 결과로는 최선이지만, AI 관여 원고가 더 나은 값을 주장한다는 사실은 연구자가 알고 있어야 합니다(모델이 같은 방향의 개선을 "새 문제"로 낼 수 있음).

## 4. 수칙 점검 결과

- **수칙 1(AI·형식 검증·회사·모델 이름):** v2에 AI, 언어 모델, 컴퓨터 탐색, Lean·형식 검증, Nature/FunSearch/회사명 없음(정규식 점검). 캡 세트 기록 값은 사람 논문 인용으로만 남김.
- **수칙 2(최전선 AI 관여):** 초안이 인용한 논문을 원문·초록으로 점검.
  - 제외: 2609.27044(Karingula–Lovett, ChatGPT-6 Astra), 2610.03750(새로 찾음, 넣지 않음).
  - 인용 값만 허용: 2.2202, 2.2203…(각각 2406.12290, 2606.12194가 인용).
  - AI 없음 확인: 2406.12290, 2603.27045, 2606.12194, 2408.02328, 2512.11217, 2404.02244, 2604.25893, 2503.09121, 2508.18586, 2501.10203, 2605.13628, 2501.11580(초록), 2302.07211·2309.02353·2007.03528(초록).
  - 참고: 2404.09639(Liao)는 감사의 글에서 PFR Lean 프로젝트 팀이 정리 4를 형식 검증했다고 적습니다. 사람 팀의 검증이고 팩에는 Lean 언급이 없습니다.
- **수칙 3(대조군):** 시돈·$B_h$·합이 모두 다른 집합·$r_A(n)$·합-곱·최소 겹침·소수 등차·Erdős–Turán·erdosproblems 번호 모두 없음. Ouyang §5(회피 집합이 시돈 집합)와 Lev 정리 3의 시돈 관찰은 초안부터 빠져 있음. 경계 사례 두 곳을 보수적으로 고침(고친 곳 3, 20).
- **수칙 4(실험·평가 언급):** 제목의 "high context"를 뺌(고친 곳 1). 남은 것: 제목의 `DRAFT`와 끝의 "Format examples … They are not to be posed again." 둘 다 `context/README.md` 규격과 저컨텍스트 팩에 같은 형태로 있어 그대로 두었습니다. 두 조건에 똑같이 들어가므로 조건 간 차이는 아닙니다.
- **수칙 5(풀린 것을 열린 것으로):** 위 3절. Lev 셋째 줄은 "큰 $p$에서 거짓", 첫째 줄은 "$(1-\varepsilon)p$까지 증명"으로 정확히 표시돼 있음. 직접곱 최적성 질문은 해결됨으로 적혀 있음.
- **수칙 6(15단어 넘는 원문 인용):** 따옴표 인용은 모두 10단어 이하. 원본 13편과 12단어 연속 일치를 기계 점검한 결과 수식 기호열(예: 볼록 진행 정의, Ruzsa 함수 형식)만 겹치고 문장 인용은 없음.
- **독립 가독성:** 세 `## Result:` 절은 각자 정의 블록(머리 Definitions의 해당 소절)과 출처를 갖고 서로를 참조하지 않음. L1 마지막 Background 한 줄만 다른 주제(Szemerédi 정리)를 언급.

## 5. 확인하지 못한 것

- 2606.12194의 Remark·추측 번호(1.5, 4.1–4.4)는 tex의 등장 순서로 추정했습니다(공용 카운터 가정).
- Edel 2.217389, Tyrrell 2.218은 서베이와 인용 논문에서만 확인(원 논문 미열람).
- Ouyang 정리 1.11(ii)의 "$\le p-3$" 자체(보조정리 4.1 구성의 정확성)는 다시 계산하지 않았습니다(앞 단계가 400 미만 소수에서 확인).
- Lev 질문 둘째 줄($|A|+|B|=p+1$)이 "증명도 반증도 없다"는 것은 원본들에 해당 결과가 없다는 데 근거한 판단입니다.
- Pan–Sun, Károlyi, Alon–Nathanson–Ruzsa, Pollard, Bukh(2008) 등은 Ouyang·Lev·Conlon–Lim의 참고문헌 서지로만 확인.
- 2512.04433의 정수 PFR 주장은 본문을 읽지 않았습니다(초록과 후속 논문들의 서술로만 판단).
- arXiv 검색은 키워드 기반이라 놓친 2026년 논문이 있을 수 있습니다.
