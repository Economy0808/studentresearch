# DRAFT — additive combinatorics pack

## Definitions

Throughout, $\mathbb N=\{1,2,3,\dots\}$, $\mathbb N_0=\mathbb N\cup\{0\}$ and $[N]=\{1,\dots,N\}$. For positive functions, $f\ll g$ (equivalently $f=O(g)$) means $f\le Cg$ for a constant $C$; a subscript, as in $\ll_\varepsilon$, means $C$ may depend on that parameter; $f=o(g)$ means $f/g\to0$.

**Sumsets and representation functions.** For $A,B\subseteq\mathbb Z$, $A+B=\{a+b:a\in A,\ b\in B\}$, $A-B=\{a-b:a\in A,\ b\in B\}$, and $hA=A+\dots+A$ ($h$ summands, repetitions allowed). The number of ordered representations of $n$ as a sum of two elements of $A$ is $1_A*1_A(n)=|\{(a,a')\in A^2:\ a+a'=n\}|$; the number of unordered representations is $r_A(n)=|\{(a,a')\in A^2:\ a\le a',\ a+a'=n\}|$. Thus $n\in A+A$ iff $r_A(n)\ge1$.

**Additive bases.** A set $A\subseteq\mathbb N_0$ is an *asymptotic basis of order $h$* if $hA$ contains every sufficiently large integer. An asymptotic basis $A$ of order $2$ is *minimal* if $A\setminus\{a\}$ is not an asymptotic basis of order $2$ for every $a\in A$ (equivalently, no proper subset of $A$ is an asymptotic basis of order $2$).

**Sidon sets.** A set $A\subseteq\mathbb Z$ is a *Sidon set* ($B_2$ set) if $a+b=c+d$ with $a,b,c,d\in A$ forces $\{a,b\}=\{c,d\}$; equivalently all sums $a+b$ with $a\le b$ are distinct, equivalently all differences $a-b$ with $a\ne b$ are distinct.

**Perfect difference sets.** Let $v\ge1$. A finite set $B\subset\mathbb Z$ whose elements are pairwise distinct modulo $v$ is a *perfect difference set modulo $v$* if every nonzero residue class modulo $v$ equals $b-b'$ for exactly one ordered pair $(b,b')$ of distinct elements of $B$. Then $|B|(|B|-1)=v-1$; Singer's theorem produces such sets with $v=q^2+q+1$ and $|B|=q+1$ for every prime power $q$. A finite set $A$ *extends to a perfect difference set modulo $v$* if $A\subseteq B$ for some such $B$.

**Arithmetic progressions.** A $k$-term arithmetic progression ($k$-AP) is $x,x+d,\dots,x+(k-1)d$; it is non-trivial if $d\ne0$. Let $r_k(N)$ be the largest size of a set $A\subseteq[N]$ containing no non-trivial $k$-AP. Roth showed $r_3(N)=o(N)$ and Szemerédi showed $r_k(N)=o(N)$ for every $k$. A *finite colouring* of a set $X$ is a map from $X$ to a finite set; a subset of $X$ is *monochromatic* if the map is constant on it.

**Densities.** The upper density of $A\subseteq\mathbb N$ is $\overline d(A)=\limsup_{N\to\infty}|A\cap[N]|/N$ and its upper Banach density is $d^*(A)=\lim_{N\to\infty}\sup_{M\ge0}|A\cap\{M+1,\dots,M+N\}|/N$. If $\overline d(A)>0$ then $d^*(A)>0$.

**Sum-free sets.** A set $S\subseteq\mathbb Z$ is *sum-free* if there are no $x,y,z\in S$ (not necessarily distinct) with $x+y=z$.

**Typical shape of a problem.** Questions in this area usually ask for the order of growth (or the exact asymptotics) of an extremal function such as the largest size of a subset of $[N]$ with a prescribed additive property, whether a limit or a density exists, or whether an infinite set with prescribed additive structure exists.

## Result: Strong bounds for 3-term progressions
Statement. There is an absolute constant $\beta>0$ such that every set $A\subseteq[N]$ with $|A|\ge 2^{-O((\log N)^{\beta})}\,N$ contains a non-trivial $3$-term arithmetic progression. In particular $r_3(N)\ll_C N/(\log N)^{C}$ for every $C>0$. (Earlier results gave a $3$-AP only for $|A|\ge N/(\log N)^{1+c}$, for a constant $c>0$.)

Proof idea. The authors first develop new analytic methods for the analogous question over finite fields and then adapt versions of those methods to the integers.

Source: Kelley and Meka, 2023, arXiv:2302.05537, Erdős #140.

## Result: Sidon sets that are asymptotic bases of order 3
Statement. There exists a Sidon set $S\subseteq\mathbb N$ (necessarily infinite) that is an asymptotic basis of order $3$: every sufficiently large integer is a sum of three elements of $S$. This answers a question of Erdős, Sárközy and Sós.

Proof idea. The proof relies on a deep result of Sawin on the $\mathbb F_q[t]$-analogue of Montgomery's conjecture for convolutions of the von Mangoldt function.

Source: Pilatte, 2023, arXiv:2303.09659, Erdős #157.

## Result: An explicit economical additive basis
Statement. There exist an explicit set $A\subseteq\mathbb N_0$ and absolute constants $C,c>0$ such that $A+A=\mathbb N_0$ and the number $\sigma_A(n)$ of representations $n=a+a'$ with $a,a'\in A$ satisfies $\sigma_A(n)\le C\,n^{c/\log\log n}$ for all sufficiently large $n$; in particular $\sigma_A(n)=n^{o(1)}$, i.e. $\sigma_A(n)=o(n^{\varepsilon})$ for every $\varepsilon>0$. (The existence of such a set was proved earlier by Erdős by probabilistic methods; the point is an explicit construction.)

Proof idea. Write integers in the mixed radix system $(p_1^2,p_2^2,\dots)$ with primes $p_k\equiv3\pmod 8$ chosen as the least such prime in $[f(k),2f(k))$ for an increasing function $f$, restrict the $k$-th digit to a modular additive basis of $\mathbb Z/p_k^2\mathbb Z$ with bounded representation counts (Ruzsa's construction), and count digit choices digit by digit to bound the number of representations.

Source: Jain, Pham, Sawhney and Zakharov, 2024, arXiv:2405.08650, Erdős #29.

## Result: A finite Sidon set that extends to no perfect difference set
Statement. Erdős conjectured that every finite Sidon set $A\subset\mathbb N$ extends to a perfect difference set modulo $p^2+p+1$ for some prime $p$. The Sidon set $\{1,2,4,8,13\}$ does not extend to a perfect difference set modulo any $v>0$, so it is a counterexample to this conjecture. (Hall had published an earlier, different counterexample, $\{1,3,9,10,13\}$, in 1947.)

Proof idea. A perfect difference set $B$ modulo $v$ gives a cyclic projective plane with the polarity $x\leftrightarrow B-x$; Baer's parity results on its absolute points (the points $x$ with $2x\in B$) yield a contradiction for any $B$ containing $\{1,2,4,8,13\}$.

Source: Alexeev and Mixon, 2025, arXiv:2510.19804, Erdős #707.

## Result: Independence of three properties of order-2 bases
Statement. For an asymptotic basis $A$ of order $2$ consider (P1) $r_A(n)\to\infty$; (P2) $A=B\cup C$ for disjoint asymptotic bases $B,C$ of order $2$; (P3) $A$ contains a minimal asymptotic basis of order $2$. Erdős and Nathanson proved that if $r_A(n)>C\log n$ for all large $n$, for a constant $C>1/\log(4/3)$, then (P2) and (P3) both hold. Larsen proved that for slower growth of $r_A$ the three properties are independent: for each of the eight possible true/false combinations of (P1), (P2), (P3) there is an asymptotic basis of order $2$ with exactly that combination.

Proof idea. The bases are produced by a randomized iterative construction carried out inductively on exponentially growing intervals.

Source: Larsen, 2026, arXiv:2603.03472, Erdős #869, #871 (the paper also answers the first question of Erdős #868; the $\epsilon\log n$ strengthening is in a separate preprint; #871 was first settled in an earlier note by the same author).

## Result: Colouring versus density for progression-free subsets
Statement. For every integer $k\ge3$ and every real $\mu\in(0,\tfrac{k-1}{k})$ there is a set $X=X(k,\mu)\subseteq\mathbb N$ such that (i) every finite colouring of $X$ has a monochromatic $k$-term arithmetic progression, and (ii) every finite $Y\subseteq X$ has a subset $Z\subseteq Y$ with $|Z|\ge\mu|Y|$ containing no $k$-term arithmetic progression. The range of $\mu$ is sharp, since the theorem fails for $\mu>\tfrac{k-1}{k}$.

Proof idea. Prove a Hales–Jewett (combinatorial lines) version by a partite construction over hypergraphs with large chromatic number and a fractional $\mu$-property, then transfer it to the integers by an injective base-$T$ style encoding of the Hales–Jewett cube under which combinatorial lines become arithmetic progressions.

Source: Reiher, Rödl and Sales, 2023, arXiv:2311.08556, Erdős #847.

## Result: Infinite sumsets with a shift inside dense sets
Statement. Let $A\subseteq\mathbb N$ have positive upper Banach density (in particular, positive upper density suffices). Then there exist an infinite set $B\subseteq A$ and an integer $t\ge1$ such that $\{b_1+b_2:\ b_1,b_2\in B,\ b_1\ne b_2\}+t\subseteq A$. The shift $t$ cannot be dropped and the restriction $b_1\ne b_2$ cannot be removed.

Proof idea. Via a Furstenberg correspondence the statement is reduced to a dynamical one about "Erdős progressions", dynamical analogues of $3$-term progressions; one then constructs a measure on pairs lying above $3$-term progressions in the Kronecker factor and shows that almost every pair yields an Erdős progression.

Source: Kra, Moreira, Richter and Robertson, 2022, arXiv:2206.12377, Erdős #656.

## Result: Large sum-free subsets of sets of integers
Statement. There is an absolute constant $c>0$ such that every finite set $A$ of $n$ integers contains a sum-free subset $A'$ with $|A'|\ge n/3+c\log\log n$. (Earlier bounds: $n/3$ by an argument of Erdős, $(n+1)/3$ by Alon and Kleitman, and $(n+2)/3$ by Bourgain.)

Proof idea. As in the classical argument, take the elements $a\in A$ whose dilate $ax$ lands in the sum-free interval $(1/3,2/3)$ of the torus for a well-chosen $x$; the improvement reduces to showing that the $L^1$ norm of $\sum_{a\in A}\big(1_{(1/3,2/3)}(ax)-\tfrac13\big)$ is $\gg\log\log n$, which is proved by a structure theory for sets with small $L^1$ norm (small additive dimension, structured distribution modulo small primes) together with an explicit test function.

Source: Bedert, 2025, arXiv:2502.08624.

## Result: Improved bounds for Szemerédi's theorem
Statement. For every integer $k\ge5$ there is a constant $c_k>0$ such that $r_k(N)\ll_k N\exp\!\big(-(\log\log N)^{c_k}\big)$.

Proof idea. Combine recent quasipolynomial bounds for the inverse theorem for the Gowers uniformity norms with the Heath-Brown–Szemerédi density increment strategy as reformulated by Green and Tao.

Source: Leng, Sah and Sawhney, 2024, arXiv:2402.17995.

## Format examples
The following three statements are already solved. They are included only to show the usual phrasing and level of precision of an Erdős-style problem (define every symbol, ask one or two sharp questions). They are not to be posed again.

Example 1. Let $f(N)$ be the size of the largest Sidon subset of $\{1,\dots,N\}$ and let $A(N)$ be the number of Sidon subsets of $\{1,\dots,N\}$. Is it true that $A(N)/2^{f(N)}\to\infty$? Is it true that $A(N)=2^{(1+o(1))f(N)}$?

Example 2. If $\mathbb N$ is $2$-coloured, must there exist a monochromatic $3$-term arithmetic progression $x,x+d,x+2d$ such that $d>x$?

Example 3. Is it true that, given any infinite set $A\subset\mathbb N$, there is a set $B$ of density $0$ such that $A+B$ contains all except finitely many integers?
