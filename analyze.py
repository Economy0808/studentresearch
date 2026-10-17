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

PROBLEM_ITEMS = ["clarity", "difficulty", "richness", "want_to_solve"]
SOLUTION_ITEMS = ["correctness", "clarity_sol"]
NULLABLE = {"problem": ["clarity", "difficulty", "want_to_solve", "known_problem"],
            "solution": ["correctness", "clarity_sol", "understandable"]}


def load(data_dir: Path):
    P = pd.DataFrame(pipeline.all_problems(data_dir))
    S = pd.DataFrame(read_jsonl(data_dir / "solutions.jsonl"))
    R = pd.DataFrame(read_jsonl(data_dir / "ratings.jsonl"))
    V = pd.DataFrame(read_jsonl(data_dir / "verifications.jsonl"))
    if not V.empty:
        V = V.drop_duplicates("solution_id", keep="last")
    if R.empty:
        raise SystemExit("no ratings yet; run eval or import-human first")
    R["richness"] = R["richness_list"].apply(lambda x: len(x) if isinstance(x, list) else None) if "richness_list" in R else None
    psrc = P.set_index("id")["source"]
    actor = psrc.copy()
    if not S.empty:
        S["source"] = S["problem_id"].map(psrc)
        psrc = pd.concat([psrc, S.set_index("id")["source"]])
        actor = pd.concat([actor, S.set_index("id")["solver"]])
    R["source"] = R["target_id"].map(psrc)   # generator of the problem behind the target
    R["actor"] = R["target_id"].map(actor)   # who wrote the target itself (generator or solver)
    R["grade"] = R["source"].map(llm.GRADE)
    return P, S, R, V


def q_g(R):
    prob = R[R.target_type == "problem"]
    return prob.groupby(["rater_type", "source"])[PROBLEM_ITEMS].mean().round(2)


def kruskal(R):
    """One observation per problem (mean over raters of that type), grouped by generator grade."""
    rows = []
    prob = R[(R.target_type == "problem") & R.grade.notna()]
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
                         "median_range": round(max(medians.values()) - min(medians.values()), 3)})
    return pd.DataFrame(rows)


def success(S, V, R):
    """Per solution: 1.0/0.0/NaN. A pass/fail verdict decides, 'na' (no candidate submitted) is a failure; otherwise
    claimed solved AND mean AI correctness ≥ 4, counting only AI raters other than the solver itself."""
    S = S.copy()
    v = V.set_index("solution_id")["verdict"] if not V.empty else pd.Series(dtype=object)
    sol = R[(R.target_type == "solution") & (R.rater_type == "ai") & (R["rater"] != R["actor"])].reindex(columns=["target_id", "correctness"])
    corr = sol.groupby("target_id")["correctness"].mean()

    def f(s):
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
    S["verified"] = S["id"].map(v).isin(["pass", "fail"])
    return S


def ladder_ceiling(S, P):
    """Per (generator, kind): checkable problems are scored by their checker, open ones by AI correctness, so they are not pooled."""
    S = S[S["source"].isin(llm.GRADE)].copy()
    S["solver_grade"] = S["solver"].map(llm.GRADE)
    S["kind"] = S["problem_id"].map(P.set_index("id")["kind"])
    rows = []
    for (g, kind), grp in S.groupby(["source", "kind"]):
        gg = llm.GRADE[g]
        own, up, low = grp[grp.solver == g].success, grp[grp.solver_grade > gg].success, grp[grp.solver_grade < gg].success
        rows.append({"generator": g, "kind": kind, "self_success": own.mean(), "n_self": int(own.notna().sum()),
                     "upper_success": up.mean(), "n_upper": int(up.notna().sum()),
                     "lower_success": low.mean(), "n_lower": int(low.notna().sum()),
                     "ladder": up.mean() - own.mean(), "ceiling": low.mean(), "n_verified": int(grp.verified.sum())})
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


def human_ai_agreement(R):
    rows = []
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = R[R.target_type == tt].reindex(columns=list(R.columns.union(items)))
        h = sub[sub.rater_type == "human"].groupby("target_id")[items].mean()
        a = sub[sub.rater_type == "ai"].groupby("target_id")[items].mean()
        j = h.join(a, lsuffix="_h", rsuffix="_a", how="inner")
        for it in items:
            pair = j[[f"{it}_h", f"{it}_a"]].dropna()
            if len(pair) >= 3:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    rho, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
                rows.append({"target_type": tt, "item": it, "n": len(pair), "spearman_rho": round(float(rho), 3), "p": f"{p:.3g}"})
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
    S = success(S, V, R) if not S.empty else S
    cj, rhos = cannot_judge(R)
    tables = {"q_g": q_g(R), "kruskal": kruskal(R),
              "ladder_ceiling": ladder_ceiling(S, P) if not S.empty else pd.DataFrame(),
              "cannot_judge": cj, "human_ai_agreement": human_ai_agreement(R),
              "kendall_w": kendall_w(R), "self_preference": self_preference(R)}
    md = ["# Metrics", f"generated {now()}", "",
          "success for unverified solutions = claimed_status solved AND mean AI correctness >= 4 (see n_verified);",
          "the solver's own rating is excluded from that mean; a verdict 'na' (no candidate) counts as failure.",
          "ladder_ceiling is split by problem kind: checkable problems are scored by their checker, open ones by AI ratings.", ""]
    for name, df in tables.items():
        df.to_csv(out / f"{name}.csv", index=(name == "q_g"), encoding="utf-8")
        md += [f"## {name}", df.to_string() if not df.empty else "_no data_", ""]
    for tt, (res, n) in rhos.items():
        md += [f"{tt}: grade vs per-rating null share — spearman rho={res.statistic:.3f}, p={res.pvalue:.3g}, n={n}", ""]
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
