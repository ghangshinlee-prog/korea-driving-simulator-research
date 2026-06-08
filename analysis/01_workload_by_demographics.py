"""
Vision-workload measures by driver demographics.

Computes per-driver eye-tracking workload measures and examines how they vary by
AGE GROUP (30s / 40s / 50s) and GENDER — the safety-evaluation angle of the M.S.
thesis. Measures:
  - Average pupil diameter (fixations) — arousal / cognitive load
  - ICA (Index of Cognitive Activity) = |Δ pupil diameter| within a driver
  - Fixation duration
  - Saccade peak velocity & amplitude (visual search intensity)

Per-driver means are computed first (one value per participant) so each driver
contributes equally; group statistics and one-way ANOVA across age groups follow.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

import config as C


def load():
    df = pd.read_csv(C.EYE_PATH, sep="\t")
    fix = df[df["Event_type"] == "Fixation"].copy()
    sac = df[df["Event_type"] == "Saccade"].copy()
    fix["ICA"] = (fix.groupby("Participant")["Average_pupil_diameter"]
                  .transform(lambda x: x.diff().abs()))
    print(f"[1] {df['Participant'].nunique()} drivers | "
          f"{len(fix):,} fixations, {len(sac):,} saccades")
    return fix, sac


def per_driver(df, value):
    keys = ["Participant", "Age_Group", "Gender"]
    return (df.dropna(subset=[value])
            .groupby(keys, observed=True)[value].mean().reset_index())


def summary_and_anova(metric_tables):
    sum_rows, test_rows = [], []
    for label, (df, value) in metric_tables.items():
        pdm = per_driver(df, value)
        # by age group
        for age in C.AGE_ORDER:
            v = pdm.loc[pdm["Age_Group"] == age, value].dropna()
            ci = 1.96 * v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else np.nan
            sum_rows.append({"metric": label, "group": f"Age {age}s",
                             "n": len(v), "mean": round(v.mean(), 4),
                             "ci95": round(ci, 4)})
        # by gender
        for g in C.GENDERS:
            v = pdm.loc[pdm["Gender"] == g, value].dropna()
            ci = 1.96 * v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else np.nan
            sum_rows.append({"metric": label, "group": g, "n": len(v),
                             "mean": round(v.mean(), 4), "ci95": round(ci, 4)})
        # one-way ANOVA across age groups + t-test by gender
        groups = [pdm.loc[pdm["Age_Group"] == a, value].dropna() for a in C.AGE_ORDER]
        F, p_age = stats.f_oneway(*groups)
        m = pdm.loc[pdm["Gender"] == "Male", value].dropna()
        f_ = pdm.loc[pdm["Gender"] == "Female", value].dropna()
        t, p_sex = stats.ttest_ind(m, f_, equal_var=False)
        test_rows.append({"metric": label, "anova_F_age": round(F, 3),
                          "anova_p_age": round(p_age, 4),
                          "ttest_p_gender": round(p_sex, 4),
                          "age_sig": "yes" if p_age < C.SIG else "no",
                          "gender_sig": "yes" if p_sex < C.SIG else "no"})
    summ = pd.DataFrame(sum_rows)
    tests = pd.DataFrame(test_rows)
    summ.to_csv(C.RESULT_DIR / "workload_by_demographics.csv", index=False)
    tests.to_csv(C.RESULT_DIR / "workload_demographic_tests.csv", index=False)
    print("[2] summary + tests written")
    print(tests.to_string(index=False))
    return summ


def fig_age(summ):
    C.style_pub(plt)
    metrics = ["Pupil diameter (mm)", "ICA", "Fixation duration (ms)", "Saccade peak velocity"]
    fig, axes = plt.subplots(1, 4, figsize=(19, 4.8))
    for ax, m in zip(axes, metrics):
        sub = summ[(summ["metric"] == m) & summ["group"].str.startswith("Age")]
        ax.bar(sub["group"], sub["mean"], yerr=sub["ci95"], capsize=5,
               color=[C.AGE_COLORS[a] for a in C.AGE_ORDER], edgecolor="#333")
        ax.set_title(m)
    fig.suptitle("Vision-workload measures by driver age group (mean ± 95% CI)",
                 fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(C.FIG_DIR / "01_workload_by_age.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("    saved 01_workload_by_age.png")


def fig_gender(summ):
    C.style_pub(plt)
    metrics = ["Pupil diameter (mm)", "ICA", "Fixation duration (ms)", "Saccade peak velocity"]
    fig, axes = plt.subplots(1, 4, figsize=(19, 4.8))
    for ax, m in zip(axes, metrics):
        sub = summ[(summ["metric"] == m) & summ["group"].isin(C.GENDERS)]
        sub = sub.set_index("group").reindex(C.GENDERS).reset_index()
        ax.bar(sub["group"], sub["mean"], yerr=sub["ci95"], capsize=5,
               color=[C.GENDER_COLORS[g] for g in sub["group"]], edgecolor="#333")
        ax.set_title(m)
    fig.suptitle("Vision-workload measures by driver gender (mean ± 95% CI)",
                 fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(C.FIG_DIR / "02_workload_by_gender.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("    saved 02_workload_by_gender.png")


def main():
    fix, sac = load()
    metric_tables = {
        "Pupil diameter (mm)": (fix, "Average_pupil_diameter"),
        "ICA": (fix, "ICA"),
        "Fixation duration (ms)": (fix, "Duration"),
        "Saccade peak velocity": (sac, "Peak_velocity"),
        "Saccade amplitude": (sac, "Saccade_amplitude"),
    }
    summ = summary_and_anova(metric_tables)
    print("[3] rendering figures ...")
    fig_age(summ)
    fig_gender(summ)
    print("[done] demographic vision-workload analysis complete.")


if __name__ == "__main__":
    main()
