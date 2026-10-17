"""Metrics from spec §11. Usage: python analyze.py [--data-dir data] [--out results]"""
import argparse
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
NULLABLE = {"problem": ["clarity", "difficulty", "want_to_solve"],
            "solution": ["correctness", "clarity_sol", "understandable"]}


def load(data_dir: Path):
    P = pd.DataFrame(pipeline.all_problems(data_dir))
    S = pd.DataFrame(read_jsonl(data_dir / "solutions.jsonl"))
    R = pd.DataFrame(read_jsonl(data_dir / "ratings.jsonl"))
    V = pd.DataFrame(read_jsonl(data_dir / "verifications.jsonl"))
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
    rows = []
    prob = R[(R.target_type == "problem") & R.grade.notna()]
    for rt, sub in prob.groupby("rater_type"):
        for item in PROBLEM_ITEMS:
            groups = [g[item].dropna().astype(float).values for _, g in sub.groupby("grade")]
            groups = [g for g in groups if len(g)]
            if len(groups) < 2:
                continue
            try:
                h, p = stats.kruskal(*groups)
            except ValueError:  # all values identical
                h, p = float("nan"), float("nan")
            rows.append({"rater_type": rt, "item": item, "H": round(h, 3), "p": round(p, 4),
                         "medians_by_grade": [float(pd.Series(g).median()) for g in groups]})
    return pd.DataFrame(rows)


def success(S, V, R):
    """Per solution: 1.0/0.0/NaN. Verified → pass==1; otherwise claimed solved and mean correctness ≥ 4."""
    S = S.copy()
    v = V.set_index("solution_id")["verdict"] if not V.empty else pd.Series(dtype=object)
    corr = R[R.target_type == "solution"].groupby("target_id")["correctness"].mean()

    def f(s):
        if s["id"] in v.index and v[s["id"]] in ("pass", "fail"):
            return float(v[s["id"]] == "pass")
        c = corr.get(s["id"], float("nan"))
        if pd.isna(c):
            return float("nan")
        return float(s.get("claimed_status") == "solved" and c >= 4)

    S["success"] = S.apply(f, axis=1)
    S["verified"] = S["id"].isin(v.index)
    return S


def ladder_ceiling(S):
    S = S[S["source"].isin(llm.GRADE)].copy()
    S["solver_grade"] = S["solver"].map(llm.GRADE)
    rows = []
    for g, grp in S.groupby("source"):
        gg = llm.GRADE[g]
        own = grp[grp.solver == g].success.mean()
        upper = grp[grp.solver_grade > gg].success.mean()
        lower = grp[grp.solver_grade < gg].success.mean()
        rows.append({"generator": g, "self_success": own, "upper_success": upper, "lower_success": lower,
                     "ladder": upper - own, "ceiling": lower, "n_verified": int(grp.verified.sum())})
    return pd.DataFrame(rows).round(3)


def cannot_judge(R):
    hum = R[R.rater_type == "human"]
    rows = []
    for tt, cols in NULLABLE.items():
        sub = hum[hum.target_type == tt]
        for src, grp in sub.groupby("source"):
            rows.append({"target_type": tt, "source": src, "n_ratings": len(grp),
                         "cannot_judge_rate": round(float(grp[cols].isna().values.mean()), 3)})
    df = pd.DataFrame(rows)
    rho = None
    if not df.empty:
        t = df[df["source"].isin(llm.GRADE)]
        if len(t) >= 3:
            rho = stats.spearmanr(t["source"].map(llm.GRADE), t["cannot_judge_rate"])
    return df, rho


def human_ai_agreement(R):
    rows = []
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = R[R.target_type == tt]
        h = sub[sub.rater_type == "human"].groupby("target_id")[items].mean()
        a = sub[sub.rater_type == "ai"].groupby("target_id")[items].mean()
        j = h.join(a, lsuffix="_h", rsuffix="_a", how="inner")
        for it in items:
            pair = j[[f"{it}_h", f"{it}_a"]].dropna()
            if len(pair) >= 3:
                rho, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
                rows.append({"target_type": tt, "item": it, "n": len(pair), "spearman_rho": round(rho, 3), "p": round(p, 4)})
    return pd.DataFrame(rows)


def kendall_w(R):
    rows = []
    hum = R[R.rater_type == "human"]
    for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
        sub = hum[hum.target_type == tt]
        for it in items:
            if sub.empty or it not in sub:
                continue
            m = sub.pivot_table(index="target_id", columns="rater", values=it, aggfunc="first").dropna()
            n, k = m.shape
            if k >= 2 and n >= 2:
                rsum = m.rank().sum(axis=1)
                ssq = float(((rsum - rsum.mean()) ** 2).sum())
                rows.append({"target_type": tt, "item": it, "n_items": n, "n_raters": k,
                             "kendall_W": round(12 * ssq / (k ** 2 * (n ** 3 - n)), 3)})
    return pd.DataFrame(rows)


def self_preference(R):
    ai = R[(R.rater_type == "ai") & R["actor"].isin(llm.GRADE)]
    rows = []
    for rater, grp in ai.groupby("rater"):
        for tt, items in (("problem", PROBLEM_ITEMS), ("solution", SOLUTION_ITEMS)):
            sub = grp[grp.target_type == tt]
            if sub.empty:
                continue
            own, other = sub[sub.actor == rater][items].mean(), sub[sub.actor != rater][items].mean()
            rows.append({"rater": rater, "target_type": tt, **{f"bias_{it}": round(own[it] - other[it], 3) for it in items}})
    return pd.DataFrame(rows)


def main(data_dir: Path = Path("data"), out: Path = Path("results")) -> dict:
    P, S, R, V = load(data_dir)
    out.mkdir(parents=True, exist_ok=True)
    S = success(S, V, R) if not S.empty else S
    cj, rho = cannot_judge(R)
    tables = {"q_g": q_g(R), "kruskal": kruskal(R),
              "ladder_ceiling": ladder_ceiling(S) if not S.empty else pd.DataFrame(),
              "cannot_judge": cj, "human_ai_agreement": human_ai_agreement(R),
              "kendall_w": kendall_w(R), "self_preference": self_preference(R)}
    md = ["# Metrics", f"generated {now()}", "",
          "success for unverified solutions = claimed_status solved AND mean correctness >= 4 (see n_verified).", ""]
    for name, df in tables.items():
        df.to_csv(out / f"{name}.csv", encoding="utf-8")
        md += [f"## {name}", df.to_string() if not df.empty else "_no data_", ""]
    if rho is not None:
        md += [f"grade vs cannot_judge_rate: spearman rho={rho.statistic:.3f}, p={rho.pvalue:.4f}", ""]
    (out / "metrics.md").write_text("\n".join(md), encoding="utf-8")
    prob = R[(R.target_type == "problem") & R.richness.notna()]
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
