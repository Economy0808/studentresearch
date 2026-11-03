"""Metrics from spec §11. Usage: python analyze.py [--data-dir data] [--out results]"""
import argparse
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

import llm
import pipeline
from store import now, read_jsonl

try:
    from pipeline import EXCLUDED_PROBLEMS
except ImportError:  # pipeline.py not yet carrying the constant
    EXCLUDED_PROBLEMS = {"P-fdf0ff", "P-2e0477"}

PROBLEM_ITEMS = ["clarity", "difficulty", "richness", "want_to_solve"]
SOLUTION_ITEMS = ["correctness", "clarity_sol"]
NULLABLE = {"problem": ["clarity", "difficulty", "want_to_solve", "known_problem"],
            "solution": ["correctness", "clarity_sol", "understandable"]}
RATING_COLS = {"rater", "rater_type", "target_type", "target_id", "richness_list", "known_problem", "understandable",
               *PROBLEM_ITEMS, *SOLUTION_ITEMS}
CORRECT_AT = 4   # a correctness score >= 4 counts as "rater judged the solution correct" (same bar as success)
SMALL_N = 10     # tests / rates with fewer observations per group than this get a caveat


def load(data_dir: Path):
    ex = set(EXCLUDED_PROBLEMS)
    P = pd.DataFrame(pipeline.all_problems(data_dir))
    P = P[~P["id"].isin(ex)].reset_index(drop=True)
    S = pd.DataFrame(read_jsonl(data_dir / "solutions.jsonl"))
    ex_sol = set()
    if not S.empty:
        ex_sol = set(S.loc[S["problem_id"].isin(ex), "id"])
        S = S[~S["problem_id"].isin(ex)].reset_index(drop=True)
    R = pd.DataFrame(read_jsonl(data_dir / "ratings.jsonl"))
    R = R.reindex(columns=sorted(set(R.columns) | RATING_COLS))   # empty / partial files still have every column
    R = R[~R["target_id"].isin(ex | ex_sol)].reset_index(drop=True)
    V = pd.DataFrame(read_jsonl(data_dir / "verifications.jsonl"))
    if not V.empty:
        V = V[~V["solution_id"].isin(ex_sol)].drop_duplicates("solution_id", keep="last")
        V["verdict"] = V["verdict"].astype(str).str.lower()
    for c in ["clarity", "difficulty", "want_to_solve", *SOLUTION_ITEMS]:
        R[c] = pd.to_numeric(R[c], errors="coerce")
    R["richness"] = pd.to_numeric(R["richness_list"].apply(lambda x: len(x) if isinstance(x, list) else None), errors="coerce")
    psrc = P.set_index("id")["source"]
    actor = psrc.copy()
    if not S.empty:
        S["source"] = S["problem_id"].map(psrc)
        psrc = pd.concat([psrc, S.set_index("id")["source"]])
        actor = pd.concat([actor, S.set_index("id")["solver"]])
    R["source"] = R["target_id"].map(psrc)   # generator of the problem behind the target
    R["actor"] = R["target_id"].map(actor)   # who wrote the target itself (generator or solver)
    R["grade"] = R["source"].map(llm.GRADE)
    R["is_self"] = (R["rater_type"] == "ai") & (R["rater"] == R["actor"])   # AI rater scoring its own problem / solution
    return P, S, R, V


def no_self(R, excl_self):
    return R[~R["is_self"]] if excl_self else R


def q_g(R, excl_self=False):
    prob = no_self(R[R.target_type == "problem"], excl_self)
    return prob.groupby(["rater_type", "source"])[PROBLEM_ITEMS].mean().round(2)


def compare_self(R, tt, items, key):
    """Mean items per (rater_type, key): `<item>_all` = all AI raters, `<item>_excl_self` = without the author's own
    rating (key = generator for problems, solver for solutions). Human rows are identical in both."""
    sub = R[R.target_type == tt]
    ns = sub[~sub.is_self]
    g = ["rater_type", key]
    out = sub.groupby(g)[items].mean().add_suffix("_all").join(ns.groupby(g)[items].mean().add_suffix("_excl_self"))
    out["n_all"], out["n_excl_self"] = sub.groupby(g).size(), ns.groupby(g).size()
    return out[[f"{it}_{v}" for it in items for v in ("all", "excl_self")] + ["n_all", "n_excl_self"]].round(2)


def kruskal(R, excl_self=False):
    """One observation per problem (mean over raters of that type), grouped by generator grade.
    excl_self drops each AI generator's own rating of its own problems before averaging."""
    rows = []
    prob = no_self(R[(R.target_type == "problem") & R.grade.notna()], excl_self)
    for rt, sub in prob.groupby("rater_type"):
        per_target = sub.groupby(["grade", "target_id"])[PROBLEM_ITEMS].mean().reset_index()
        for item in PROBLEM_ITEMS:
            groups = {int(g): d[item].dropna().astype(float).values for g, d in per_target.groupby("grade")}
            groups = {g: v for g, v in groups.items() if len(v)}
            if len(groups) < 2:
                continue
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                try:
                    h, p = stats.kruskal(*groups.values())
                except ValueError:
                    h, p = float("nan"), float("nan")
            medians = {g: float(pd.Series(v).median()) for g, v in groups.items()}
            rows.append({"rater_type": rt, "item": item, "n_problems": int(sum(len(v) for v in groups.values())),
                         "H": round(float(h), 3), "p": f"{p:.3g}", "medians_by_grade": medians,
                         "median_range": round(max(medians.values()) - min(medians.values()), 3),
                         "small_n": f"n<{SMALL_N} per group" if min(len(v) for v in groups.values()) < SMALL_N else ""})
    return pd.DataFrame(rows)


def success(S, V, R):
    """Per solution: 1.0/0.0/NaN. A pass/fail verdict decides, 'na' (no candidate submitted) is a failure; otherwise
    claimed solved AND mean AI correctness ≥ 4, counting only AI raters other than the solver itself.
    `success` (= `success_budget0`) scores pipeline budget_exceeded rows as 0; `success_budget_excl` leaves them missing."""
    S = S.copy()
    S["budget"] = S["budget_exceeded"].eq(True) if "budget_exceeded" in S else False
    v = V.set_index("solution_id")["verdict"] if not V.empty else pd.Series(dtype=object)
    sol = R[(R.target_type == "solution") & (R.rater_type == "ai") & ~R.is_self]
    corr = sol.groupby("target_id")["correctness"].mean()

    def f(s):
        if s["budget"]:  # pipeline-written time-budget row: a failed attempt
            return 0.0
        vd = v.get(s["id"])
        if vd in ("pass", "fail"):
            return float(vd == "pass")
        if vd == "na":
            return 0.0
        c = corr.get(s["id"], float("nan"))
        if pd.isna(c):
            return float("nan")
        return float(s.get("claimed_status") == "solved" and c >= 4)

    S["success"] = S.apply(f, axis=1)
    S["success_budget0"] = S["success"]
    S["success_budget_excl"] = S["success"].where(~S["budget"])
    S["verified"] = S["id"].map(v).isin(["pass", "fail"])
    return S


def budget_counts(S):
    """Budget-exceeded placeholder rows per solver, per problem generator and per (generator, solver) pair."""
    rows = []
    for by in (["solver"], ["source"], ["source", "solver"]):
        for key, grp in S.groupby(by):
            rows.append({"by": "x".join(by), "group": key if isinstance(key, str) else " / ".join(key),
                         "n_solutions": len(grp), "n_budget_rows": int(grp["budget"].sum()),
                         "budget_share": round(float(grp["budget"].mean()), 3)})
    return pd.DataFrame(rows)


def ladder_ceiling(S, P, col="success"):
    """Per (generator, kind): checkable problems are scored by their checker, open ones by AI correctness, so they are not pooled.
    col picks the variant: `success` (= success_budget0, budget rows as 0) or `success_budget_excl` (budget rows missing)."""
    S = S[S["source"].isin(llm.GRADE)].copy()
    S["solver_grade"] = S["solver"].map(llm.GRADE)
    S["kind"] = S["problem_id"].map(P.set_index("id")["kind"])
    rows = []
    for (g, kind), grp in S.groupby(["source", "kind"]):
        gg = llm.GRADE[g]
        own, up, low = grp[grp.solver == g][col], grp[grp.solver_grade > gg][col], grp[grp.solver_grade < gg][col]
        rows.append({"generator": g, "kind": kind, "self_success": own.mean(), "n_self": int(own.notna().sum()),
                     "upper_success": up.mean(), "n_upper": int(up.notna().sum()),
                     "lower_success": low.mean(), "n_lower": int(low.notna().sum()),
                     "ladder": up.mean() - own.mean(), "ceiling": low.mean(), "n_verified": int(grp.verified.sum()),
                     "n_budget_rows": int(grp["budget"].sum()),
                     "small_n": f"n<{SMALL_N} per cell" if 0 < min(own.notna().sum(), up.notna().sum(), low.notna().sum()) < SMALL_N else ""})
    return pd.DataFrame(rows).round(3)


def rater_vs_checker(R, V):
    """Rater correctness vs the checker verdict (pass/fail only; na/error skipped), per rater and pooled by rater type.
    agreement = share of ratings where (correctness >= CORRECT_AT) matches (verdict == pass). scope `excl_self` drops AI
    raters' ratings of their own solutions (shown for AI raters only; humans are unaffected)."""
    if V.empty:
        return pd.DataFrame()
    sub = R[R.target_type == "solution"].merge(V.loc[V["verdict"].isin(["pass", "fail"]), ["solution_id", "verdict"]],
                                               left_on="target_id", right_on="solution_id")
    sub = sub[sub["correctness"].notna()]
    rows = []

    def add(label, scope, g):
        p, f = g[g.verdict == "pass"]["correctness"], g[g.verdict == "fail"]["correctness"]
        rows.append({"rater": label, "scope": scope, "n_pass": len(p), "n_fail": len(f),
                     "mean_corr_pass": p.mean(), "mean_corr_fail": f.mean(), "diff": p.mean() - f.mean(),
                     "agreement": ((g["correctness"] >= CORRECT_AT) == (g.verdict == "pass")).mean(),
                     "small_n": f"n<{SMALL_N}" if len(g) < SMALL_N else ""})

    for scope, ss in (("all", sub), ("excl_self", sub[~sub.is_self])):
        for rater, g in ss.groupby("rater"):
            if scope == "all" or g.rater_type.iloc[0] == "ai":
                add(rater, scope, g)
        for rt, g in ss.groupby("rater_type"):
            if scope == "all" or rt == "ai":
                add(f"ALL_{rt}", scope, g)
    return pd.DataFrame(rows).round(3)


def _known(R):
    """Problem ratings with kp = 1.0 (rater flagged `known_problem` true) / 0.0 / NaN (null = could not judge)."""
    pr = R[R.target_type == "problem"].copy()
    pr["kp"] = pr["known_problem"].map({True: 1.0, False: 0.0})
    return pr[pr["kp"].notna()]


def novelty_generator_report(P):
    """Generator-side self-report on the problem rows: novelty_confidence (0-1) and whether `resembles_known` was filled."""
    P = P.reindex(columns=list(P.columns.union(["novelty_confidence", "resembles_known"])))
    P = P.assign(novelty_confidence=pd.to_numeric(P["novelty_confidence"], errors="coerce"),
                 resembles_known=P["resembles_known"].map(lambda x: isinstance(x, str) and bool(x.strip())))
    return P.groupby("source").agg(n_problems=("id", "size"), mean_novelty_confidence=("novelty_confidence", "mean"),
                                   resembles_known_share=("resembles_known", "mean")).round(3)


def novelty_flags(R):
    """Share of problems flagged known_problem, per generator and rater type. known_any = problems flagged by at least one
    rater of that type; known_rate = share of individual ratings; `_excl_self` drops the generator's own rating."""
    pr = _known(R)
    rows = []
    for (src, rt), g in pr.groupby(["source", "rater_type"]):
        row = {"source": src, "rater_type": rt, "n_problems": g.target_id.nunique()}
        for tag, gg in (("all", g), ("excl_self", g[~g.is_self])):
            per = gg.groupby("target_id")["kp"].max()
            row[f"known_any_{tag}"] = per.mean() if len(per) else float("nan")
            row[f"known_rate_{tag}"] = gg["kp"].mean()
            row[f"n_ratings_{tag}"] = len(gg)
        row["small_n"] = f"n<{SMALL_N} problems" if row["n_problems"] < SMALL_N else ""
        rows.append(row)
    return pd.DataFrame(rows).round(3)


def novelty_by_rater(R):
    pr = _known(R)
    return pr.groupby(["rater", "source"]).agg(n_ratings=("kp", "size"), known_rate=("kp", "mean")).round(3)


def novelty_manip_check(R):
    """Manipulation check: how often raters flag the real (human-control) problems as known, next to their rate on
    AI-generated problems. ANY_<type> = problems flagged by at least one rater of that type."""
    pr = _known(R)
    if pr.empty:
        return pd.DataFrame()
    hc, ag = pr[pr.source == "human"], pr[pr.source.isin(llm.GRADE)]
    rows = []

    def rate(g, any_):
        return g.groupby("target_id")["kp"].max().mean() if any_ else g["kp"].mean()

    def add(label, h, a, any_):
        rows.append({"rater": label, "n_human_control": h.target_id.nunique(), "known_human_control": rate(h, any_),
                     "n_ai_generated": a.target_id.nunique(), "known_ai_generated": rate(a, any_),
                     "known_ai_generated_excl_self": rate(a[~a.is_self], any_),
                     "small_n": f"n<{SMALL_N} human-control problems" if h.target_id.nunique() < SMALL_N else ""})

    for rater in sorted(pr["rater"].dropna().unique()):
        add(rater, hc[hc.rater == rater], ag[ag.rater == rater], False)
    for rt in sorted(pr["rater_type"].dropna().unique()):
        add(f"ANY_{rt}", hc[hc.rater_type == rt], ag[ag.rater_type == rt], True)
    return pd.DataFrame(rows).round(3)


def cannot_judge(R):
    """Human raters' null share by target type and author, per item and overall; grade vs per-rating null share.
    `actor` is the author of the target: the generator for problems, the solver for solutions."""
    hum = R[R.rater_type == "human"]
    rows, rhos = [], {}
    for tt, cols in NULLABLE.items():
        sub = hum[hum.target_type == tt]
        if sub.empty:
            continue
        sub = sub.reindex(columns=list(sub.columns.union(cols)))
        for act, grp in sub.groupby("actor"):
            per_item = grp[cols].isna().mean()
            rows.append({"target_type": tt, "actor": act, "n_ratings": len(grp),
                         "cannot_judge_rate": round(float(grp[cols].isna().values.mean()), 3),
                         **{f"cj_{c}": round(float(per_item[c]), 3) for c in cols}})
        graded = sub[sub["actor"].isin(llm.GRADE)]
        if len(graded) >= 3:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                rhos[tt] = (stats.spearmanr(graded["actor"].map(llm.GRADE), graded[cols].isna().mean(axis=1)), len(graded))
    return pd.DataFrame(rows), rhos


def human_ai_agreement(R, excl_self=False):
    """Human mean vs AI mean per target; excl_self drops the author's own AI rating from the AI mean."""
    rows = []
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = R[R.target_type == tt].reindex(columns=list(R.columns.union(items)))
        h = sub[sub.rater_type == "human"].groupby("target_id")[items].mean()
        a = no_self(sub[sub.rater_type == "ai"], excl_self).groupby("target_id")[items].mean()
        j = h.join(a, lsuffix="_h", rsuffix="_a", how="inner")
        for it in items:
            pair = j[[f"{it}_h", f"{it}_a"]].dropna()
            if len(pair) >= 3:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    rho, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
                rows.append({"target_type": tt, "item": it, "n": len(pair), "spearman_rho": round(float(rho), 3), "p": f"{p:.3g}",
                             "small_n": f"n<{SMALL_N}" if len(pair) < SMALL_N else ""})
    return pd.DataFrame(rows)


def kendall_w(R):
    """Kendall's W with the tie correction: W = 12S / (k²(n³−n) − kΣT_j), T_j = Σ(t³−t) over rater j's tie groups."""
    rows = []
    hum = R[R.rater_type == "human"]
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = hum[hum.target_type == tt]
        for it in items:
            if sub.empty or it not in sub:
                continue
            m = sub.pivot_table(index="target_id", columns="rater", values=it, aggfunc="first").dropna()
            n, k = m.shape
            if k < 2 or n < 2:
                continue
            ranks = m.rank()
            rsum = ranks.sum(axis=1)
            ssq = float(((rsum - rsum.mean()) ** 2).sum())
            ties = sum(float((vc ** 3 - vc).sum()) for vc in (ranks[c].value_counts() for c in ranks.columns))
            denom = k ** 2 * (n ** 3 - n) - k * ties
            w = 12 * ssq / denom if denom > 0 else float("nan")
            rows.append({"target_type": tt, "item": it, "n_items": n, "n_raters": k,
                         "kendall_W": round(w, 3) if w == w else w})
    return pd.DataFrame(rows)


def self_preference(R):
    """bias = (mean deviation of a rater's score on its OWN work) − (same on others' work), where deviation is the score
    minus the mean of the OTHER AI raters on the same target. NaN when no other AI rater scored that target."""
    ai = R[(R.rater_type == "ai") & R["actor"].isin(llm.GRADE)].copy()
    rows = []
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = ai[ai.target_type == tt].reindex(columns=list(ai.columns.union(items)))
        if sub.empty:
            continue
        for it in items:
            sub[it] = pd.to_numeric(sub[it], errors="coerce")
            # deviation of each rating from the mean of the OTHER AI raters on the same target
            g = sub.groupby("target_id")[it]
            total, cnt = g.transform("sum"), g.transform("count")
            others_mean = (total - sub[it]) / (cnt - 1)
            sub[f"dev_{it}"] = sub[it] - others_mean
        for rater, grp in sub.groupby("rater"):
            own, other = grp[grp.actor == rater], grp[grp.actor != rater]
            rows.append({"rater": rater, "target_type": tt, "n_own": len(own), "n_other": len(other),
                         **{f"bias_{it}": round(float(own[f"dev_{it}"].mean() - other[f"dev_{it}"].mean()), 3) for it in items}})
    return pd.DataFrame(rows)


def main(data_dir: Path = Path("data"), out: Path = Path("results")) -> dict:
    P, S, R, V = load(data_dir)
    out.mkdir(parents=True, exist_ok=True)
    have_S = not S.empty
    S = success(S, V, R) if have_S else S
    cj, rhos = cannot_judge(R)
    tables = {"q_g": q_g(R), "q_g_excl_self": q_g(R, excl_self=True), "q_g_compare": compare_self(R, "problem", PROBLEM_ITEMS, "source"),
              "solution_scores_compare": compare_self(R, "solution", SOLUTION_ITEMS, "actor"),
              "kruskal": kruskal(R), "kruskal_excl_self": kruskal(R, excl_self=True),
              "budget_rows": budget_counts(S) if have_S else pd.DataFrame(),
              "ladder_ceiling": ladder_ceiling(S, P) if have_S else pd.DataFrame(),
              "ladder_ceiling_budget_excl": ladder_ceiling(S, P, "success_budget_excl") if have_S else pd.DataFrame(),
              "rater_vs_checker": rater_vs_checker(R, V),
              "novelty_generator_report": novelty_generator_report(P), "novelty_flags": novelty_flags(R),
              "novelty_by_rater": novelty_by_rater(R), "novelty_manip_check": novelty_manip_check(R),
              "cannot_judge": cj, "human_ai_agreement": human_ai_agreement(R),
              "human_ai_agreement_excl_self": human_ai_agreement(R, excl_self=True),
              "kendall_w": kendall_w(R), "self_preference": self_preference(R)}
    n_rat = len(R)
    notes = {"q_g_excl_self": ["AI raters' ratings of their own generated problems dropped; human ratings unchanged. q_g = all raters."],
             "q_g_compare": ["`_all` = all AI raters, `_excl_self` = without the generator's own rating (humans identical)."],
             "solution_scores_compare": ["same split for solutions: `_excl_self` drops the solver's own rating of its solution."],
             "kruskal_excl_self": ["generator's own rating dropped before averaging each problem's score; compare with `kruskal`."],
             "budget_rows": ["budget_exceeded rows are pipeline placeholders (no answer within the time budget); `success`/`success_budget0` "
                             "scores them 0, `success_budget_excl` (see ladder_ceiling_budget_excl) leaves them missing."],
             "ladder_ceiling": ["variant success_budget0: budget rows count as failures."],
             "ladder_ceiling_budget_excl": ["variant success_budget_excl: budget rows excluded (treated as missing)."],
             "rater_vs_checker": [f"checkable problems, verdict pass/fail only; agreement = share of ratings with (correctness >= {CORRECT_AT}) == (verdict is pass)."
                                  if not V.empty else "no verifications yet."],
             "novelty_generator_report": ["novelty_confidence / resembles_known are the GENERATOR's self-report on the problem row "
                                          "(ratings carry only `known_problem`); human-control problems have none (NaN)."],
             "novelty_flags": ["known_problem flagged by raters; known_any = problems flagged by at least one rater of that type. "
                               "source=human are the real (Erdos) control problems."],
             "novelty_manip_check": ["recognition rate of human-control problems vs AI-generated ones, per rater."]}
    if n_rat == 0:
        notes["q_g"] = ["no ratings yet; run eval or import-human first (rating-based tables are empty)."]
        print("no ratings yet; rating-based tables are empty (budget/novelty-generator tables still computed)")
    elif _known(R).empty:
        notes["novelty_flags"].append("no known_problem values in the ratings (field absent or all null).")
    md = ["# Metrics", f"generated {now()}", f"excluded problems: {sorted(EXCLUDED_PROBLEMS)}", f"{n_rat} ratings", "",
          "success for unverified solutions = claimed_status solved AND mean AI correctness >= 4 (see n_verified);",
          "the solver's own rating is excluded from that mean; a verdict 'na' (no candidate) counts as failure.",
          "ladder_ceiling is split by problem kind: checkable problems are scored by their checker, open ones by AI ratings.",
          "AI-rater aggregates over problems/solutions come in two versions: all AI raters, and `_excl_self` (author's own rating dropped).", ""]
    for name, df in tables.items():
        df.to_csv(out / f"{name}.csv", index=(df.index.names[0] is not None), encoding="utf-8")
        md += [f"## {name}", *notes.get(name, []), df.to_string() if not df.empty else "_no data_"]
        if "small_n" in df and df["small_n"].astype(bool).any():
            md.append(f"caveat: some rows rest on fewer than {SMALL_N} observations per group; treat p-values and rates as descriptive.")
        md.append("")
    for tt, (res, n) in rhos.items():
        md += [f"{tt}: grade vs per-rating null share — spearman rho={res.statistic:.3f}, p={res.pvalue:.3g}, n={n}"
               + (f" (caveat: n<{SMALL_N})" if n < SMALL_N else ""), ""]
    (out / "metrics.md").write_text("\n".join(md), encoding="utf-8")
    prob = R[(R.target_type == "problem") & (R.rater_type == "ai") & R.richness.notna()]
    if not prob.empty:
        ax = prob.boxplot(column="richness", by="source")
        ax.set_title("richness by generator"); plt.suptitle("")
        plt.savefig(out / "richness_by_source.png", dpi=120, bbox_inches="tight"); plt.close("all")
    return tables


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--out", type=Path, default=Path("results"))
    a = ap.parse_args()
    main(a.data_dir, a.out)
    print(f"wrote {a.out / 'metrics.md'}")
