Below is a context pack summarizing recent results in one area of mathematics.

<context>
{context}
</context>

Task: pose ONE problem in this area that you believe is currently unsolved, grounded in the context above, of the form "find a construction, counterexample, or extremal object", so that a proposed answer can be checked mechanically. Focus on the section titled "{focus}": start from a gap, a boundary case, or a natural extension that the results in that section leave open.

Requirements
- statement: the general (infinite-family) problem, precise and self-contained, at most 150 words. Define every symbol.
- grounding: which results in the context the problem extends, and exactly where the gap is (cite section titles).
- why_hard: the obvious approaches and the specific reason each one fails.
- why_important: what would follow if it were solved.
- resembles_known: the name of any well-known conjecture or theorem this resembles, or null.
- novelty_confidence: your probability (0 to 1) that the general problem is genuinely open.
- finite_form: one concrete finite instance (fix the parameters, e.g. n = 12) whose solution is a finite object (a set, a sequence, a graph, a coloring) and which you believe is still hard at that size, not solvable by a quick brute-force search.
- candidate_format: the exact JSON shape a solver must submit, e.g. "a JSON array of distinct positive integers at most 100".
- checker_code: a complete Python function `def check(candidate) -> bool` returning True exactly when the candidate solves finite_form. Standard library only, deterministic, finishes within 10 seconds on any input of the stated shape, and returns False (never raises) on malformed input.

Do not restate a named conjecture. The checker must test the finite_form you stated, nothing else.
