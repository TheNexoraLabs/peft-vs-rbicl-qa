"""Paired statistical analysis for the 300-example primary evaluation.

Inputs are data-minimized per-system CSVs keyed by sample_id. The sample_id is
a SHA-256 identifier derived from [source_dataset, split, context, question];
the source text itself is not redistributed in this repository.

Run from any directory: python analysis/statistical_analysis.py
"""

from pathlib import Path
import hashlib

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests


# ============================================================
# CONFIGURATION
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "results" / "primary_300"
OUTPUT_DIR = ROOT_DIR / "results" / "statistical_analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "LoRA": DATA_DIR / "lora.csv",
    "DoRA": DATA_DIR / "dora.csv",
    "LoRA + DeepSeek": DATA_DIR / "lora_deepseek.csv",
    "DoRA + DeepSeek": DATA_DIR / "dora_deepseek.csv",
    "RB-ICL": DATA_DIR / "rb_icl.csv",
    "RB-ICL + DeepSeek": DATA_DIR / "rb_icl_deepseek.csv",
}


# ============================================================
# METRICS
# ============================================================

METRICS = [
    "exact_match",
    "token_f1",
    "rouge1",
    "rougeL",
    "meteor",
    "bertscore_precision",
    "bertscore_recall",
    "bertscore_f1",
    "semantic_similarity",
    "sacrebleu",
]


# ============================================================
# STATISTICAL SETTINGS
# ============================================================

N_BOOTSTRAP = 20_000

CONFIDENCE_LEVEL = 0.95

RANDOM_SEED = 42

ALPHA = 0.05


# ============================================================
# SAMPLE IDENTIFICATION AND LOADING
# ============================================================

def load_model_csv(model_name, path):
    """Load a data-minimized result file keyed by a stable sample_id."""
    if not path.exists():
        raise FileNotFoundError(f"File not found for {model_name}: {path}")

    print(f"Loading: {model_name} ({path})")
    df = pd.read_csv(path)

    required = ["sample_id", "source_dataset", "split", *METRICS]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{model_name} is missing columns: {missing}")

    df = df.copy()
    df["sample_id"] = df["sample_id"].astype("string").str.strip()
    if df["sample_id"].isna().any() or (df["sample_id"] == "").any():
        raise ValueError(f"{model_name} contains blank sample_id values.")
    if df["sample_id"].duplicated().any():
        raise ValueError(f"{model_name} contains duplicate sample_id values.")

    for metric in METRICS:
        df[metric] = pd.to_numeric(df[metric], errors="coerce")

    if df[METRICS].isna().any().any():
        missing_metrics = df[METRICS].isna().sum()
        raise ValueError(f"{model_name} contains missing/non-numeric metric values: {missing_metrics[missing_metrics > 0].to_dict()}")

    print(f"  rows = {len(df):,}; unique samples = {df['sample_id'].nunique():,}")
    return df


def align_pair(df_a, df_b, model_a, model_b):
    """Paired merge using the stable sample_id supplied with public results."""
    a = df_a[["sample_id", "source_dataset", "split", *METRICS]].copy()
    b = df_b[["sample_id", "source_dataset", "split", *METRICS]].copy()

    merged = pd.merge(
        a, b, on="sample_id", how="inner", suffixes=("__A", "__B"), validate="one_to_one"
    )
    if len(merged) == 0:
        raise ValueError(f"No paired samples found for {model_a} vs {model_b}.")

    # Since sample_id hashes the source dataset, split, context and question,
    # these metadata fields must agree for every matched sample.
    for field in ["source_dataset", "split"]:
        if not (merged[f"{field}__A"] == merged[f"{field}__B"]).all():
            raise ValueError(f"Matched sample_id values have inconsistent {field} for {model_a} vs {model_b}.")

    print(f"  {model_a} vs {model_b}: {len(merged):,} paired samples")
    return merged


# ============================================================
# PAIRED BOOTSTRAP
# ============================================================

def bootstrap_mean_difference(
    differences,
    n_bootstrap,
    confidence_level,
    rng,
):

    differences = np.asarray(
        differences,
        dtype=float,
    )

    differences = differences[
        np.isfinite(differences)
    ]

    n = len(differences)

    if n == 0:
        return np.nan, np.nan, np.nan

    observed = np.mean(differences)

    indices = rng.integers(
        0,
        n,
        size=(n_bootstrap, n),
    )

    bootstrap_means = (
        differences[indices]
        .mean(axis=1)
    )

    alpha = 1 - confidence_level

    lower = np.quantile(
        bootstrap_means,
        alpha / 2,
    )

    upper = np.quantile(
        bootstrap_means,
        1 - alpha / 2,
    )

    return observed, lower, upper


# ============================================================
# WILCOXON
# ============================================================

def wilcoxon_test(differences):

    differences = np.asarray(
        differences,
        dtype=float,
    )

    differences = differences[
        np.isfinite(differences)
    ]

    differences = differences[
        differences != 0
    ]

    if len(differences) == 0:
        return np.nan

    try:
        result = wilcoxon(
            differences,
            alternative="two-sided",
            zero_method="wilcox",
            method="auto",
        )

        return result.pvalue

    except ValueError:
        return np.nan


# ============================================================
# RANK-BISERIAL EFFECT SIZE
# ============================================================

def rank_biserial_effect_size(
    differences
):

    differences = np.asarray(
        differences,
        dtype=float,
    )

    differences = differences[
        np.isfinite(differences)
    ]

    differences = differences[
        differences != 0
    ]

    if len(differences) == 0:
        return np.nan

    ranks = pd.Series(
        np.abs(differences)
    ).rank(
        method="average"
    ).to_numpy()

    positive = ranks[
        differences > 0
    ].sum()

    negative = ranks[
        differences < 0
    ].sum()

    total = positive + negative

    if total == 0:
        return np.nan

    return (positive - negative) / total


# ============================================================
# ONE PAIRED COMPARISON
# ============================================================

def analyze_pair(
    merged,
    model_a,
    model_b,
    comparison_name,
    hypothesis_family,
    rng,
):

    rows = []

    for metric in METRICS:

        col_a = f"{metric}__A"
        col_b = f"{metric}__B"

        x = pd.to_numeric(
            merged[col_a],
            errors="coerce",
        ).to_numpy()

        y = pd.to_numeric(
            merged[col_b],
            errors="coerce",
        ).to_numpy()

        valid = (
            np.isfinite(x)
            &
            np.isfinite(y)
        )

        x = x[valid]
        y = y[valid]

        if len(x) == 0:
            continue

        # Positive value means model B is better.
        differences = y - x

        mean_a = np.mean(x)
        mean_b = np.mean(y)

        mean_difference, ci_low, ci_high = (
            bootstrap_mean_difference(
                differences,
                N_BOOTSTRAP,
                CONFIDENCE_LEVEL,
                rng,
            )
        )

        p_wilcoxon = wilcoxon_test(
            differences
        )

        effect_size = (
            rank_biserial_effect_size(
                differences
            )
        )

        win_rate_b = np.mean(
            differences > 0
        )

        tie_rate = np.mean(
            differences == 0
        )

        rows.append({
            "hypothesis_family":
                hypothesis_family,

            "comparison":
                comparison_name,

            "model_A":
                model_a,

            "model_B":
                model_b,

            "metric":
                metric,

            "n_paired":
                len(differences),

            "mean_A":
                mean_a,

            "mean_B":
                mean_b,

            "mean_difference_B_minus_A":
                mean_difference,

            "bootstrap_CI_95_lower":
                ci_low,

            "bootstrap_CI_95_upper":
                ci_high,

            "wilcoxon_p":
                p_wilcoxon,

            "rank_biserial_effect_size":
                effect_size,

            "B_win_rate":
                win_rate_b,

            "tie_rate":
                tie_rate,
        })

    return rows


# ============================================================
# HYPOTHESIS DEFINITIONS
# ============================================================

def define_hypotheses():

    return {

        # ----------------------------------------------------
        # H1
        # Adapter choice
        # ----------------------------------------------------

        "H1_adapter": [
            ("LoRA", "DoRA"),
            ("LoRA + DeepSeek", "DoRA + DeepSeek"),
        ],

        # ----------------------------------------------------
        # H2
        # Adaptation regime
        # ----------------------------------------------------

        "H2_regime": [
            ("RB-ICL", "LoRA"),
            ("RB-ICL", "DoRA"),
        ],

        # ----------------------------------------------------
        # H3
        # Effect of reasoning-oriented backbone
        # ----------------------------------------------------

        "H3_backbone": [
            ("LoRA", "LoRA + DeepSeek"),
            ("DoRA", "DoRA + DeepSeek"),
        ],

        # ----------------------------------------------------
        # H4
        # DeepSeek effect within RB-ICL
        # ----------------------------------------------------

        "H4_rb_icl_reasoning": [
            ("RB-ICL", "RB-ICL + DeepSeek"),
        ],
    }


# ============================================================
# RUN ALL PRIMARY COMPARISONS
# ============================================================

def run_primary_analysis(model_data):

    hypotheses = define_hypotheses()

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    all_rows = []

    for family, comparisons in hypotheses.items():

        print()
        print("=" * 70)
        print(f"HYPOTHESIS FAMILY: {family}")
        print("=" * 70)

        for model_a, model_b in comparisons:

            merged = align_pair(
                model_data[model_a],
                model_data[model_b],
                model_a,
                model_b,
            )

            comparison_name = (
                f"{model_b} vs {model_a}"
            )

            rows = analyze_pair(
                merged=merged,
                model_a=model_a,
                model_b=model_b,
                comparison_name=comparison_name,
                hypothesis_family=family,
                rng=rng,
            )

            all_rows.extend(rows)

    return pd.DataFrame(all_rows)


# ============================================================
# HOLM CORRECTION
# ============================================================

def apply_holm_by_hypothesis_family(
    results
):

    results = results.copy()

    results[
        "wilcoxon_p_holm"
    ] = np.nan

    grouped = results.groupby(
        "hypothesis_family"
    )

    for family, group in grouped:

        mask = (
            results["hypothesis_family"]
            == family
        )

        valid = (
            results.loc[
                mask,
                "wilcoxon_p"
            ]
            .notna()
        )

        if valid.sum() == 0:
            continue

        p_values = results.loc[
            mask & results["wilcoxon_p"].notna(),
            "wilcoxon_p"
        ].to_numpy()

        _, adjusted, _, _ = (
            multipletests(
                p_values,
                alpha=ALPHA,
                method="holm",
            )
        )

        indices = results.loc[
            mask & results["wilcoxon_p"].notna()
        ].index

        results.loc[
            indices,
            "wilcoxon_p_holm"
        ] = adjusted

    return results


# ============================================================
# BOOTSTRAP INTERPRETATION
# ============================================================

def add_interpretation_columns(
    results
):

    results = results.copy()

    results[
        "bootstrap_excludes_zero"
    ] = (
        (
            results[
                "bootstrap_CI_95_lower"
            ] > 0
        )
        |
        (
            results[
                "bootstrap_CI_95_upper"
            ] < 0
        )
    )

    results[
        "direction"
    ] = np.where(
        results[
            "mean_difference_B_minus_A"
        ] > 0,
        "Model B higher",
        np.where(
            results[
                "mean_difference_B_minus_A"
            ] < 0,
            "Model A higher",
            "No difference",
        ),
    )

    results[
        "statistical_conclusion"
    ] = np.where(
        results[
            "bootstrap_excludes_zero"
        ],
        "Difference supported by 95% bootstrap CI",
        "Difference not distinguishable from zero",
    )

    return results


# ============================================================
# INTERACTION ANALYSIS
# ============================================================

def interaction_analysis(
    model_data
):

    """
    Tests the backbone × adaptation-regime interaction.

    We compare:

        DeepSeek - Llama under PEFT

    against

        DeepSeek - Llama under RB-ICL

    using the difference-in-differences contrast.

    IMPORTANT:
    The current six-model design does not contain a separate
    DeepSeek RB-ICL prediction file unless RB-ICL + DeepSeek is
    interpreted as that condition.

    Therefore this analysis uses:

        PEFT:
            Llama = average(LoRA, DoRA)
            DeepSeek = average(LoRA+DeepSeek, DoRA+DeepSeek)

        RB-ICL:
            Llama = RB-ICL
            DeepSeek = RB-ICL+DeepSeek
    """

    # --------------------------------------------------------
    # Create aligned data
    # --------------------------------------------------------

    lora = model_data["LoRA"]
    dora = model_data["DoRA"]

    lora_ds = model_data[
        "LoRA + DeepSeek"
    ]

    dora_ds = model_data[
        "DoRA + DeepSeek"
    ]

    rb_icl = model_data["RB-ICL"]

    rb_icl_ds = model_data[
        "RB-ICL + DeepSeek"
    ]

    # --------------------------------------------------------
    # Use common samples across all six files.
    # --------------------------------------------------------

    common_keys = set(
        lora["sample_id"]
    )

    for df in [
        dora,
        lora_ds,
        dora_ds,
        rb_icl,
        rb_icl_ds,
    ]:
        common_keys &= set(
            df["sample_id"]
        )

    common_keys = sorted(common_keys)

    if len(common_keys) == 0:
        raise ValueError(
            "No samples are shared across "
            "all required conditions for interaction analysis."
        )

    print()
    print("=" * 70)
    print("INTERACTION ANALYSIS")
    print("=" * 70)

    print(
        f"Common samples: {len(common_keys):,}"
    )

    rng = np.random.default_rng(
        RANDOM_SEED + 100
    )

    rows = []

    for metric in METRICS:

        def get_values(df):

            indexed = df.set_index(
                "sample_id"
            )

            return pd.to_numeric(
                indexed.loc[
                    common_keys,
                    metric
                ],
                errors="coerce",
            ).to_numpy()

        lora_x = get_values(lora)
        dora_x = get_values(dora)

        lora_ds_x = get_values(
            lora_ds
        )

        dora_ds_x = get_values(
            dora_ds
        )

        rb_icl_x = get_values(rb_icl)
        rb_icl_ds_x = get_values(
            rb_icl_ds
        )

        valid = (
            np.isfinite(lora_x)
            &
            np.isfinite(dora_x)
            &
            np.isfinite(lora_ds_x)
            &
            np.isfinite(dora_ds_x)
            &
            np.isfinite(rb_icl_x)
            &
            np.isfinite(rb_icl_ds_x)
        )

        lora_x = lora_x[valid]
        dora_x = dora_x[valid]

        lora_ds_x = lora_ds_x[valid]
        dora_ds_x = dora_ds_x[valid]

        rb_icl_x = rb_icl_x[valid]
        rb_icl_ds_x = rb_icl_ds_x[valid]

        if len(lora_x) == 0:
            continue

        # ----------------------------------------------------
        # PEFT backbone effect
        # ----------------------------------------------------

        peft_lora_mean = (
            lora_x + dora_x
        ) / 2

        peft_ds_mean = (
            lora_ds_x + dora_ds_x
        ) / 2

        peft_backbone_effect = (
            peft_ds_mean
            -
            peft_lora_mean
        )

        # ----------------------------------------------------
        # RB-ICL backbone effect
        # ----------------------------------------------------

        rb_icl_backbone_effect = (
            rb_icl_ds_x
            -
            rb_icl_x
        )

        # ----------------------------------------------------
        # Difference-in-differences
        #
        # Positive = DeepSeek effect is greater under PEFT
        # Negative = DeepSeek effect is greater under RB-ICL
        # ----------------------------------------------------

        interaction = (
            peft_backbone_effect
            -
            rb_icl_backbone_effect
        )

        mean_diff, ci_low, ci_high = (
            bootstrap_mean_difference(
                interaction,
                N_BOOTSTRAP,
                CONFIDENCE_LEVEL,
                rng,
            )
        )

        p_wilcoxon = wilcoxon_test(
            interaction
        )

        effect_size = (
            rank_biserial_effect_size(
                interaction
            )
        )

        rows.append({
            "hypothesis_family":
                "H5_backbone_x_regime_interaction",

            "metric":
                metric,

            "n_paired":
                len(interaction),

            "PEFT_DeepSeek_minus_Llama":
                np.mean(
                    peft_backbone_effect
                ),

            "RB-ICL_DeepSeek_minus_Llama":
                np.mean(
                    rb_icl_backbone_effect
                ),

            "interaction_difference_in_differences":
                mean_diff,

            "bootstrap_CI_95_lower":
                ci_low,

            "bootstrap_CI_95_upper":
                ci_high,

            "wilcoxon_p":
                p_wilcoxon,

            "rank_biserial_effect_size":
                effect_size,
        })

    interaction_df = pd.DataFrame(
        rows
    )

    # Holm correction within interaction family
    if not interaction_df.empty:

        valid = interaction_df[
            "wilcoxon_p"
        ].notna()

        if valid.sum() > 0:

            _, adjusted, _, _ = (
                multipletests(
                    interaction_df.loc[
                        valid,
                        "wilcoxon_p"
                    ],
                    alpha=ALPHA,
                    method="holm",
                )
            )

            interaction_df[
                "wilcoxon_p_holm"
            ] = np.nan

            interaction_df.loc[
                valid,
                "wilcoxon_p_holm"
            ] = adjusted

    interaction_df[
        "bootstrap_excludes_zero"
    ] = (
        (
            interaction_df[
                "bootstrap_CI_95_lower"
            ] > 0
        )
        |
        (
            interaction_df[
                "bootstrap_CI_95_upper"
            ] < 0
        )
    )

    return interaction_df


# ============================================================
# CREATE PAPER-ORIENTED TABLE
# ============================================================

def create_paper_table(results):

    table = results[
        [
            "hypothesis_family",
            "comparison",
            "metric",
            "n_paired",
            "mean_A",
            "mean_B",
            "mean_difference_B_minus_A",
            "bootstrap_CI_95_lower",
            "bootstrap_CI_95_upper",
            "wilcoxon_p",
            "wilcoxon_p_holm",
            "rank_biserial_effect_size",
            "bootstrap_excludes_zero",
            "statistical_conclusion",
        ]
    ].copy()

    return table


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("FINAL HYPOTHESIS-BASED STATISTICAL ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------------
    # Load all models
    # --------------------------------------------------------

    model_data = {}

    for model_name, path in FILES.items():

        model_data[
            model_name
        ] = load_model_csv(
            model_name,
            path,
        )

    # --------------------------------------------------------
    # Primary hypothesis analysis
    # --------------------------------------------------------

    results = run_primary_analysis(
        model_data
    )

    # --------------------------------------------------------
    # Holm correction within hypothesis families
    # --------------------------------------------------------

    results = apply_holm_by_hypothesis_family(
        results
    )

    # --------------------------------------------------------
    # Add interpretation
    # --------------------------------------------------------

    results = add_interpretation_columns(
        results
    )

    # --------------------------------------------------------
    # Interaction
    # --------------------------------------------------------

    interaction = interaction_analysis(
        model_data
    )

    # --------------------------------------------------------
    # Save primary results
    # --------------------------------------------------------

    results_path = (
        OUTPUT_DIR
        / "primary_hypothesis_results.csv"
    )

    results.to_csv(
        results_path,
        index=False,
    )

    # --------------------------------------------------------
    # Save interaction results
    # --------------------------------------------------------

    interaction_path = (
        OUTPUT_DIR
        / "interaction_results.csv"
    )

    interaction.to_csv(
        interaction_path,
        index=False,
    )

    # --------------------------------------------------------
    # Paper-oriented table
    # --------------------------------------------------------

    paper_table = create_paper_table(
        results
    )

    paper_table_path = (
        OUTPUT_DIR
        / "paper_statistical_table.csv"
    )

    paper_table.to_csv(
        paper_table_path,
        index=False,
    )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    pd.set_option(
        "display.max_columns",
        None,
    )

    pd.set_option(
        "display.width",
        220,
    )

    print()
    print("=" * 70)
    print("PRIMARY HYPOTHESIS RESULTS")
    print("=" * 70)

    print(
        paper_table.to_string(
            index=False
        )
    )

    print()
    print("=" * 70)
    print("INTERACTION RESULTS")
    print("=" * 70)

    print(
        interaction.to_string(
            index=False
        )
    )

    print()
    print("=" * 70)
    print("FILES GENERATED")
    print("=" * 70)

    print(
        f"\nPrimary results:\n"
        f"{results_path}"
    )

    print(
        f"\nInteraction results:\n"
        f"{interaction_path}"
    )

    print(
        f"\nPaper table:\n"
        f"{paper_table_path}"
    )

    print()
    print(
        "Analysis completed successfully."
    )


if __name__ == "__main__":
    main()