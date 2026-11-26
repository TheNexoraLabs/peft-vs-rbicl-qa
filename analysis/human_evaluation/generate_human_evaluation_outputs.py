#!/usr/bin/env python3
"""
Generate publication-ready Error Analysis tables and figures from the annotated QA CSV.

Input:
    annotated_output_final.csv

Output directory:
    error_analysis_output_final/

The script uses only Python's standard library plus matplotlib for figures.
It does NOT require pandas/openpyxl.

Main outputs:
    CSV + LaTeX tables:
      01_overall_error_distribution
      02_substantive_error_rates
      03_dora_vs_lora
      04_rb_icl_error_profile
      05_dataset_by_model_error_profile
      06_abstention_analysis
      07_model_dataset_summary
      (qualitative examples intentionally withheld from public generation)

    Figures:
      fig_error_heatmap.png
      fig_substantive_error_rates.png
      fig_abstention_rate.png

Notes:
- final_error_code is treated as the adjudicated/final error label.
- "No error" and "F*" are reported separately from substantive error codes.
- The script does NOT invent question-type labels. source_dataset is used as the
  available dataset-level axis for difficulty/failure-pattern analysis.
"""

from __future__ import annotations

import csv
import math
import os
import re
from collections import Counter, defaultdict
from statistics import mean

import matplotlib.pyplot as plt


INPUT_CSV = "annotated_output_final.csv"
OUTPUT_DIR = "error_analysis_output_final"

# Keep the error order stable across tables/figures.
ERROR_ORDER = [
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3",
    "C1", "C2", "C3", "C4",
    "D1", "D2", "D3",
    "F*",
    "No error",
]


# Reconstructed operational definitions based on the annotation rationales
# present in the dataset. These are documentation aids and should be checked
# against the original annotation guideline before publication.
ERROR_DEFINITIONS = {
    "A1": "Wrong span or entity: the prediction is factually or referentially wrong because it selects the wrong entity, span, value, person, place, object, or answer.",
    "A2": "Incomplete answer: the prediction contains part of the required answer but omits an essential part of the reference or an essential sub-question.",
    "A3": "Unsupported content: the prediction introduces substantive information that is not supported by the supplied context, including hallucinated facts, additional unsupported claims, or external knowledge inserted into a context-grounded QA task.",
    "A4": "Sub-question aggregation: the question contains multiple explicit sub-questions and the model fails to correctly organize or answer those sub-questions as separate required components.",
    "B1": "False abstention: the model abstains even though the answer is available or recoverable from the supplied context.",
    "B2": "Missed abstention: the question is genuinely unanswerable from the supplied context, but the model produces a substantive answer instead of abstaining.",
    "B3": "Fallback paraphrase: the model makes the correct abstention decision but uses wording different from the canonical fallback answer.",
    "C1": "Verbosity or padding: the prediction contains unnecessary explanation, repetition, elaboration, or unsupported verbal padding that is not required to answer the question.",
    "C2": "Meta-commentary: the model talks about the task, the user, external sources, how to answer, or what the user should do instead of directly answering the question.",
    "C3": "Reasoning-trace leakage: the model exposes internal reasoning, chain-of-thought-like deliberation, hidden analysis, or extensive step-by-step reasoning that should not be part of the requested answer.",
    "C4": "Answer-type mismatch: the prediction does not match the type or form of answer requested by the question.",
    "D1": "Conversational reference: the model fails to resolve conversational references, pronouns, ellipsis, or context-dependent references correctly.",
    "D2": "Long context or truncation: there is evidence that long context, truncation, or context-window effects are responsible for the failure.",
    "D3": "Noisy or pragmatic input: the failure is primarily caused by noisy, informal, ambiguous, fragmented, pragmatic, or socially implicit input.",
    "F*": "Metric/reference artefact: the issue is primarily caused by reference wording, normalization, or metric behavior rather than the model's actual task behavior; F* is non-substantive.",
    "No error": "The prediction is factually correct, supported by the context, responsive to the question, and acceptable in form.",
}
CORE_METRICS = [
    "exact_match",
    "token_f1",
    "rouge1",
    "rougeL",
    "meteor",
    "bertscore_f1",
    "semantic_similarity",
    "sacrebleu",
]

TEXT_FIELDS = [
    "question", "answer", "predicted_answer", "notes_1", "notes_2",
]


def clean(value: str | None) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: str) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("Input CSV is empty.")
    return rows


def ensure_required_columns(rows: list[dict[str, str]]) -> None:
    required = {
        "sample_id", "model", "source_dataset", "split",
        "question", "answer", "predicted_answer",
        "final_error_code", "is_abstention", "abstention_type",
    }
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def write_csv(path: str, headers: list[str], body: list[list[object]]) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(body)


def latex_escape(value: object) -> str:
    """Escape literal text for LaTeX without re-escaping inserted commands."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in str(value))


def write_latex_table(path: str, caption: str, label: str,
                      headers: list[str], body: list[list[object]],
                      alignment: str | None = None) -> None:
    if alignment is None:
        alignment = "l" + "r" * (len(headers) - 1)

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{" + alignment + r"}")
    lines.append(r"\toprule")
    lines.append(" & ".join(latex_escape(h) for h in headers) + r" \\")
    lines.append(r"\midrule")
    for row in body:
        lines.append(" & ".join(latex_escape(v) for v in row) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{" + latex_escape(caption) + r"}")
    lines.append(r"\label{" + label + r"}")
    lines.append(r"\end{table}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def make_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def pct(n: int, d: int) -> str:
    return f"{(100.0 * n / d):.1f}%" if d else "0.0%"


def sort_models(rows: list[dict[str, str]]) -> list[str]:
    # Preserve a useful methodological ordering where possible.
    preferred = ["LoRA", "DoRA", "RB-ICL", "LoRA+DeepSeek", "DoRA+DeepSeek", "RB-ICL+DeepSeek"]
    actual = list(dict.fromkeys(r["model"] for r in rows))
    return [m for m in preferred if m in actual] + [m for m in actual if m not in preferred]


def sort_datasets(rows: list[dict[str, str]]) -> list[str]:
    preferred = ["squad_v2", "coqa", "tweet_qa", "NLQuAD"]
    actual = list(dict.fromkeys(r["source_dataset"] for r in rows))
    return [d for d in preferred if d in actual] + [d for d in actual if d not in preferred]


def code_order(rows: list[dict[str, str]]) -> list[str]:
    actual = {clean(r["final_error_code"]) for r in rows}
    return [c for c in ERROR_ORDER if c in actual] + sorted(actual - set(ERROR_ORDER))


def group(rows: list[dict[str, str]], key_fn):
    out = defaultdict(list)
    for r in rows:
        out[key_fn(r)].append(r)
    return out


def error_counter(rows_subset: list[dict[str, str]]) -> Counter:
    return Counter(clean(r["final_error_code"]) for r in rows_subset)


SUBSTANTIVE_CODES = {
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3",
    "C1", "C2", "C3", "C4",
    "D1", "D2", "D3",
}

def substantive_error_count(rows_subset: list[dict[str, str]]) -> int:
    return sum(
        1 for r in rows_subset
        if clean(r["final_error_code"]) in SUBSTANTIVE_CODES
    )


def shorten(text: str, max_len: int = 420) -> str:
    text = re.sub(r"\s+", " ", clean(text))
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"



def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float:
    """Compute Cohen's kappa without requiring scikit-learn."""
    if len(labels_a) != len(labels_b) or not labels_a:
        return float("nan")

    n = len(labels_a)
    observed = sum(a == b for a, b in zip(labels_a, labels_b)) / n

    counts_a = Counter(labels_a)
    counts_b = Counter(labels_b)
    labels = set(counts_a) | set(counts_b)

    expected = sum(
        (counts_a[label] / n) * (counts_b[label] / n)
        for label in labels
    )

    if expected == 1.0:
        return 1.0

    return (observed - expected) / (1.0 - expected)


def agreement_stats(rows_subset: list[dict[str, str]]) -> tuple[int, int, float, float]:
    """Return N, exact agreements, exact agreement %, and Cohen's kappa."""
    a = [clean(r.get("annotator_1")) for r in rows_subset]
    b = [clean(r.get("annotator_2")) for r in rows_subset]

    valid = [(x, y) for x, y in zip(a, b) if x and y]
    if not valid:
        return 0, 0, 0.0, float("nan")

    a_valid = [x for x, _ in valid]
    b_valid = [y for _, y in valid]

    exact_n = sum(x == y for x, y in zip(a_valid, b_valid))
    exact_pct = 100.0 * exact_n / len(valid)
    kappa = cohen_kappa(a_valid, b_valid)
    return len(valid), exact_n, exact_pct, kappa


def build_interannotator_agreement(rows, models, datasets):
    """Create overall and grouped agreement statistics."""
    headers = ["Group", "N", "Exact agreement", "Exact agreement (%)", "Cohen's kappa"]
    body = []
    csv_body = []

    groups = [("Overall", rows)]

    for m in models:
        groups.append((f"Model: {m}", [r for r in rows if r["model"] == m]))

    for d in datasets:
        groups.append((f"Dataset: {d}", [r for r in rows if r["source_dataset"] == d]))

    for label, subset in groups:
        n, exact_n, exact_pct, kappa = agreement_stats(subset)
        body.append([
            label,
            n,
            exact_n,
            f"{exact_pct:.2f}%",
            f"{kappa:.3f}" if not math.isnan(kappa) else "NA",
        ])
        csv_body.append([
            label,
            n,
            exact_n,
            exact_pct,
            kappa if not math.isnan(kappa) else "",
        ])

    write_csv(
        os.path.join(OUTPUT_DIR, "09_interannotator_agreement.csv"),
        ["group", "N", "exact_agreement_n", "exact_agreement_pct", "cohen_kappa"],
        csv_body,
    )

    write_latex_table(
        os.path.join(OUTPUT_DIR, "09_interannotator_agreement.tex"),
        "Inter-annotator agreement before adjudication. Exact agreement is the proportion of cases with identical labels; Cohen's kappa is computed over the same pre-adjudication labels.",
        "tab:interannotator_agreement",
        headers,
        body,
        alignment="llrrr",
    )

    # The reconstructed taxonomy table is intentionally not generated for public release;
    # its definitions require validation against the original annotation guideline.


def build_overall_error_distribution(rows, models, codes):
    headers = ["Model"] + [f"{c} n (%)" for c in codes]
    body = []
    csv_body = []
    for m in models:
        rr = [r for r in rows if r["model"] == m]
        c = error_counter(rr)
        row = [m]
        csv_row = [m]
        n = len(rr)
        for code in codes:
            cell = f"{c[code]} ({pct(c[code], n)})"
            row.append(cell)
            csv_row.append(f"{c[code]}")
        body.append(row)
        csv_body.append(csv_row)

    write_csv(
        os.path.join(OUTPUT_DIR, "01_overall_error_distribution.csv"),
        ["model"] + codes,
        csv_body,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "01_overall_error_distribution.tex"),
        "Final error-code distribution by model. Values are counts with percentages in parentheses.",
        "tab:overall_error_distribution",
        headers,
        body,
        alignment="l" + "r" * len(codes),
    )


def is_annotated(row: dict[str, str]) -> bool:
    """True when a final adjudicated human label is present."""
    return clean(row.get("final_error_code")) != ""


def numeric_values(rows_subset, field):
    values = []
    for row in rows_subset:
        raw = clean(row.get(field))
        if not raw:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if math.isfinite(value):
            values.append(value)
    return values


def percentile(sorted_values, p):
    """Linear-interpolated percentile (0 <= p <= 1)."""
    if not sorted_values:
        return float("nan")
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * p
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


def stratified_bootstrap_ci(annotated_rows, datasets, n_boot=20000, seed=42):
    """Percentile CI for acceptability, resampling within each dataset.

    Each row is treated as one annotated response. The same dataset-stratified
    design is used for every model, preserving the observed number of rows in
    each dataset stratum (normally 50 per dataset).
    """
    import random
    rng = random.Random(seed)
    strata = {d: [r for r in annotated_rows if clean(r.get("source_dataset")) == d]
              for d in datasets}
    if any(not strata[d] for d in datasets):
        missing = [d for d in datasets if not strata[d]]
        raise ValueError(f"Cannot bootstrap: no annotated rows for dataset(s): {missing}")

    def acceptable(row):
        return clean(row.get("final_error_code")).casefold() in {"no error", "f*"}

    observed_n = sum(len(strata[d]) for d in datasets)
    observed_success = sum(acceptable(r) for d in datasets for r in strata[d])
    observed_rate = observed_success / observed_n if observed_n else float("nan")

    boot_rates = []
    for _ in range(n_boot):
        successes = 0
        total = 0
        for d in datasets:
            group_rows = strata[d]
            n = len(group_rows)
            sampled = [group_rows[rng.randrange(n)] for _ in range(n)]
            successes += sum(acceptable(r) for r in sampled)
            total += n
        boot_rates.append(successes / total if total else float("nan"))
    boot_rates.sort()
    return observed_rate, percentile(boot_rates, 0.025), percentile(boot_rates, 0.975)


def normalized_match_text(value: object) -> str:
    """Normalize whitespace/case for a conservative text-based sample check."""
    return " ".join(clean(value).casefold().split())


def sample_content_signature(row: dict[str, str]) -> tuple[str, str, str, str]:
    """Return a model-independent signature of the input QA instance.

    sample_id may be unique to each system's prediction record. For checking
    whether systems were evaluated on the same input, compare source dataset,
    split, context, and question instead of assuming IDs are globally shared.
    """
    return (
        normalized_match_text(row.get("source_dataset")),
        normalized_match_text(row.get("split")),
        normalized_match_text(row.get("context")),
        normalized_match_text(row.get("question")),
    )


def write_sample_alignment_diagnostic(annotated_rows, models):
    """Write an audit file; do not abort descriptive tables on model-specific IDs.

    Exact Match and human acceptability are calculated within each model's own
    annotated rows, so cross-model ID equality is not a prerequisite for those
    descriptive statistics. This diagnostic separately checks whether the
    underlying QA inputs appear aligned across systems.
    """
    from collections import Counter

    rows_by_model = {
        model: [r for r in annotated_rows if clean(r.get("model")) == model]
        for model in models
    }
    present_models = [model for model in models if rows_by_model[model]]
    reference_model = present_models[0] if present_models else ""
    reference_rows = rows_by_model.get(reference_model, [])

    ref_ids = Counter(
        (normalized_match_text(r.get("source_dataset")), normalized_match_text(r.get("sample_id")))
        for r in reference_rows
    )
    ref_signatures = Counter(sample_content_signature(r) for r in reference_rows)
    out = []
    for model in present_models:
        subset = rows_by_model[model]
        id_counts = Counter(
            (normalized_match_text(r.get("source_dataset")), normalized_match_text(r.get("sample_id")))
            for r in subset
        )
        signatures = Counter(sample_content_signature(r) for r in subset)
        if model == reference_model:
            id_match, content_match, missing, extra = "reference", "reference", 0, 0
        else:
            id_match = "yes" if id_counts == ref_ids else "no"
            content_match = "yes" if signatures == ref_signatures else "no"
            missing = sum((ref_signatures - signatures).values())
            extra = sum((signatures - ref_signatures).values())
        out.append([
            model, len(subset), len(id_counts), len(signatures),
            id_match, content_match, missing, extra,
        ])

    write_csv(
        os.path.join(OUTPUT_DIR, "sample_alignment_diagnostic.csv"),
        ["model", "n_annotated", "unique_dataset_sample_ids", "unique_input_signatures",
         f"sample_ids_match_{reference_model}", f"input_signatures_match_{reference_model}",
         "input_instances_missing_vs_reference", "input_instances_extra_vs_reference"],
        out,
    )

    if len(present_models) > 1:
        all_content_aligned = all(
            Counter(sample_content_signature(r) for r in rows_by_model[m]) == ref_signatures
            for m in present_models[1:]
        )
        all_ids_aligned = all(
            Counter(
                (normalized_match_text(r.get("source_dataset")), normalized_match_text(r.get("sample_id")))
                for r in rows_by_model[m]
            ) == ref_ids
            for m in present_models[1:]
        )
        if all_ids_aligned:
            print("Sample alignment check: dataset/sample_id keys match across systems.")
        elif all_content_aligned:
            print(
                "NOTE: sample_id values differ across systems, but normalized "
                "dataset/split/context/question signatures match. Continuing; "
                "the tables use each system's annotated rows."
            )
        else:
            print(
                "WARNING: annotated QA inputs do not appear fully aligned across "
                "systems by dataset/split/context/question. Descriptive per-model "
                "tables will still be generated, but do not describe them as a "
                "paired or matched cross-system comparison until the source data is checked."
            )
    return reference_model


def build_human_acceptability_tables(rows, models, datasets):
    """Generate human-label counts and within-system EM/acceptability tables.

    Exact Match and human acceptability are computed on the same annotated rows
    for each individual system. sample_id need not be globally identical across
    systems; potential input alignment is separately audited and reported.
    """
    annotated_rows = [r for r in rows if is_annotated(r)]
    if not annotated_rows:
        raise ValueError("No annotated rows found: final_error_code is blank for every row.")

    model_aliases = {
        "LoRA+DeepSeek": "LoRA + DeepSeek",
        "DoRA+DeepSeek": "DoRA + DeepSeek",
        "RB-ICL+DeepSeek": "RB-ICL + DeepSeek",
    }

    # A duplicate key inside a single model is still suspicious, but the IDs
    # are not required to be shared across models. Emit a diagnostic report
    # based on model-independent input content before generating the tables.
    for model in models:
        subset = [r for r in annotated_rows if clean(r.get("model")) == model]
        if not subset:
            continue
        keys = [(clean(r.get("source_dataset")), clean(r.get("sample_id"))) for r in subset]
        if len(keys) != len(set(keys)):
            raise ValueError(
                f"Duplicate (source_dataset, sample_id) among annotated rows for {model}. "
                "Please check whether the CSV contains duplicate annotated records."
            )
    write_sample_alignment_diagnostic(annotated_rows, models)

    # Table 1: label counts + human acceptability + stratified bootstrap CI.
    detailed_headers = [
        "Model", "N", "No error", "F*", "Substantive errors",
        "Acceptable n (%)", "95% CI (%)"
    ]
    detailed_body, detailed_csv = [], []
    for model in models:
        subset = [r for r in annotated_rows if clean(r.get("model")) == model]
        if not subset:
            continue
        counts = Counter(clean(r.get("final_error_code")) for r in subset)
        n = len(subset)
        no_error = counts["No error"]
        fstar = counts["F*"]
        substantive = sum(counts[c] for c in SUBSTANTIVE_CODES)
        acceptable = no_error + fstar
        if no_error + fstar + substantive != n:
            other = n - (no_error + fstar + substantive)
            raise ValueError(
                f"Final-label counts do not partition N for {model}; "
                f"{other} row(s) have unaccounted labels."
            )
        _, lo, hi = stratified_bootstrap_ci(subset, datasets)
        model_label = model_aliases.get(model, model)
        detailed_body.append([
            model_label, n,
            f"{no_error} ({pct(no_error, n)})",
            f"{fstar} ({pct(fstar, n)})",
            f"{substantive} ({pct(substantive, n)})",
            f"{acceptable} ({100*acceptable/n:.1f}%)",
            f"[{100*lo:.1f}, {100*hi:.1f}]",
        ])
        detailed_csv.append([
            model_label, n, no_error, 100*no_error/n, fstar, 100*fstar/n,
            substantive, 100*substantive/n, acceptable, 100*acceptable/n,
            100*lo, 100*hi
        ])

    write_csv(
        os.path.join(OUTPUT_DIR, "11_human_acceptability_detailed.csv"),
        ["model", "n_annotated", "no_error_n", "no_error_pct", "Fstar_n", "Fstar_pct",
         "substantive_errors_n", "substantive_errors_pct", "acceptable_n", "acceptable_pct",
         "ci95_lower_pct", "ci95_upper_pct"],
        detailed_csv,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "11_human_acceptability_detailed.tex"),
        "Final-label counts and human-judged acceptability by system. Acceptability is defined as No error + F*. Confidence intervals are 95% dataset-stratified percentile bootstrap intervals based on 20,000 resamples (seed=42).",
        "tab:substantive_error_rates", detailed_headers, detailed_body,
        alignment="lrrrrrr",
    )

    # Table 2: the same annotated response subset is used for Exact Match and
    # human acceptability. Do not use the separate eight-metric average here:
    # it is not the manuscript's original descriptive aggregate score.
    comparison_headers = [
        "Configuration", "Exact Match (annotated subset)",
        "Human-acceptable n (%)", "95% CI (%)"
    ]
    comparison_body, comparison_csv = [], []
    for model in models:
        human_rows = [r for r in annotated_rows if clean(r.get("model")) == model]
        if not human_rows:
            continue
        em_vals = numeric_values(human_rows, "exact_match")
        accept_n = sum(
            clean(r.get("final_error_code")).casefold() in {"no error", "f*"}
            for r in human_rows
        )
        _, lo, hi = stratified_bootstrap_ci(human_rows, datasets)
        model_label = model_aliases.get(model, model)
        em_n = len(em_vals)
        em_mean = sum(em_vals) / em_n if em_n else float("nan")
        comparison_body.append([
            model_label,
            f"{em_mean:.4f} (n={em_n})" if em_n else "NA",
            f"{accept_n}/{len(human_rows)} ({100*accept_n/len(human_rows):.1f}%)",
            f"[{100*lo:.1f}, {100*hi:.1f}]",
        ])
        comparison_csv.append([
            model_label, em_mean, em_n, accept_n, len(human_rows),
            100*accept_n/len(human_rows), 100*lo, 100*hi
        ])

    write_csv(
        os.path.join(OUTPUT_DIR, "12_automatic_vs_human_acceptability.csv"),
        ["configuration", "exact_match_mean_annotated_subset", "exact_match_n",
         "acceptable_n", "annotated_n", "acceptable_pct", "ci95_lower_pct", "ci95_upper_pct"],
        comparison_csv,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "12_automatic_vs_human_acceptability.tex"),
        "Exact Match and human-judged acceptability within each configuration's annotated response subset. Exact Match is computed only for responses with a final human label. Acceptability is defined as No error + F*. Confidence intervals are 95% dataset-stratified percentile bootstrap intervals based on 20,000 resamples (seed=42). Cross-system input alignment is audited separately in sample_alignment_diagnostic.csv.",
        "tab:human_acceptability", comparison_headers, comparison_body,
        alignment="lrrr",
    )

    print("Generated tables:")
    print(" - 11_human_acceptability_detailed.tex/.csv")
    print(" - 12_automatic_vs_human_acceptability.tex/.csv")
    print("Note: the comparison table computes Exact Match on the annotated rows only.")


def build_substantive_error_rates(rows, models):
    headers = ["Model", "N", "No error", "F*", "Substantive errors"]
    body = []
    csv_body = []
    for m in models:
        rr = [r for r in rows if r["model"] == m]
        n = len(rr)
        c = error_counter(rr)
        sub = substantive_error_count(rr)
        body.append([
            m,
            n,
            f"{c['No error']} ({pct(c['No error'], n)})",
            f"{c['F*']} ({pct(c['F*'], n)})",
            f"{sub} ({pct(sub, n)})",
        ])
        csv_body.append([m, n, c['No error'], c['F*'], sub,
                         f"{100*sub/n:.2f}" if n else "0"])

    write_csv(
        os.path.join(OUTPUT_DIR, "02_substantive_error_rates.csv"),
        ["model", "N", "no_error_n", "Fstar_n", "substantive_error_n", "substantive_error_pct"],
        csv_body,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "02_substantive_error_rates.tex"),
        "Summary of substantive error rates, with No error and F* reported separately.",
        "tab:substantive_error_rates",
        headers,
        body,
    )


def build_pairwise_dora_lora(rows):
    pairs = [("DoRA", "LoRA"), ("DoRA+DeepSeek", "LoRA+DeepSeek")]
    codes = [
            "A1", "A2", "A3", "A4",
            "B1", "B2", "B3",
            "C1", "C2", "C3", "C4",
            "D1", "D2", "D3",
        ]
    headers = ["Error", "DoRA n (%)", "LoRA n (%)", "Difference (pp)"]
    all_body = []
    all_csv = []

    for left, right in pairs:
        sub = rows
        lc = error_counter([r for r in rows if r["model"] == left])
        rc = error_counter([r for r in rows if r["model"] == right])
        ln = sum(1 for r in rows if r["model"] == left)
        rn = sum(1 for r in rows if r["model"] == right)
        pair_body = []
        pair_csv = []
        for code in codes:
            lp = 100 * lc[code] / ln if ln else 0
            rp = 100 * rc[code] / rn if rn else 0
            pair_body.append([code, f"{lc[code]} ({lp:.1f}%)", f"{rc[code]} ({rp:.1f}%)", f"{lp-rp:+.1f}"])
            pair_csv.append([code, lc[code], lp, rc[code], rp, lp-rp])
        safe = re.sub(r"[^A-Za-z0-9]+", "_", left + "_vs_" + right).strip("_").lower()
        write_csv(
            os.path.join(OUTPUT_DIR, f"03_dora_vs_lora_{safe}.csv"),
            ["error_code", left + "_n", left + "_pct", right + "_n", right + "_pct", "difference_pp"],
            pair_csv,
        )
        write_latex_table(
            os.path.join(OUTPUT_DIR, f"03_dora_vs_lora_{safe}.tex"),
            f"Substantive error profile: {left} versus {right}. Difference is left minus right percentage points.",
            f"tab:dora_lora_{safe}",
            headers,
            pair_body,
        )
        all_body.append((left, right, pair_body))
        all_csv.append((left, right, pair_csv))


def build_rb_icl_error_profile(rows):
    rb_icl_models = [m for m in ["RB-ICL", "RB-ICL+DeepSeek"] if any(r["model"] == m for r in rows)]
    codes = [
        "A1", "A2", "A3", "A4",
        "B1", "B2", "B3",
        "C1", "C2", "C3", "C4",
        "D1", "D2", "D3",
        "F*",
    ]
    headers = ["Error / outcome"] + [f"{m} n (%)" for m in rb_icl_models]
    body = []
    csv_body = []
    for code in codes:
        row = [code]
        csv_row = [code]
        for m in rb_icl_models:
            rr = [r for r in rows if r["model"] == m]
            c = error_counter(rr)
            n = len(rr)
            row.append(f"{c[code]} ({pct(c[code], n)})")
            csv_row.extend([c[code], 100*c[code]/n if n else 0])
        body.append(row)
        csv_body.append(csv_row)

    # Abstention rates as a separate outcome row.
    row = ["Abstention (YES)"]
    csv_row = ["Abstention"]
    for m in rb_icl_models:
        rr = [r for r in rows if r["model"] == m]
        n = len(rr)
        c = sum(1 for r in rr if clean(r["is_abstention"]).upper() == "YES")
        row.append(f"{c} ({pct(c, n)})")
        csv_row.extend([c, 100*c/n if n else 0])
    body.append(row)
    csv_body.append(csv_row)

    write_csv(
        os.path.join(OUTPUT_DIR, "04_rb_icl_error_profile.csv"),
        ["outcome"] + [x for m in rb_icl_models for x in (m + "_n", m + "_pct")],
        csv_body,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "04_rb_icl_error_profile.tex"),
        "Error and abstention profile of retrieval-based in-context learning methods.",
        "tab:rb_icl_error_profile",
        headers,
        body,
        alignment="l" + "r" * len(rb_icl_models),
    )


def build_dataset_model_error_profile(rows, models, datasets):
    # This table focuses on the number of substantive errors per model/dataset.
    headers = ["Dataset"] + [f"{m} subst. error rate" for m in models]
    body = []
    csv_body = []
    for d in datasets:
        row = [d]
        csv_row = [d]
        for m in models:
            rr = [r for r in rows if r["source_dataset"] == d and r["model"] == m]
            n = len(rr)
            sub = substantive_error_count(rr)
            rate = 100*sub/n if n else 0
            row.append(f"{sub}/{n} ({rate:.1f}%)")
            csv_row.extend([sub, n, rate])
        body.append(row)
        csv_body.append(csv_row)

    write_csv(
        os.path.join(OUTPUT_DIR, "05_dataset_by_model_error_profile.csv"),
        ["dataset"] + [x for m in models for x in (m + "_substantive_error_n", m + "_N", m + "_rate_pct")],
        csv_body,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "05_dataset_by_model_error_profile.tex"),
        "Substantive error rates by dataset and model.",
        "tab:dataset_model_error_profile",
        headers,
        body,
        alignment="l" + "r" * len(models),
    )


def build_abstention_analysis(rows, models):
    types = ["correct_abstention", "false_abstention", "missed_abstention", "fallback_paraphrase"]
    headers = ["Model", "Abstention YES", "Correct", "False", "Missed", "Fallback paraphrase"]
    body = []
    csv_body = []
    for m in models:
        rr = [r for r in rows if r["model"] == m]
        n = len(rr)
        yes = sum(clean(r["is_abstention"]).upper() == "YES" for r in rr)
        c = Counter(clean(r["abstention_type"]) for r in rr)
        body.append([
            m,
            f"{yes} ({pct(yes, n)})",
            f"{c['correct_abstention']}",
            f"{c['false_abstention']}",
            f"{c['missed_abstention']}",
            f"{c['fallback_paraphrase']}",
        ])
        csv_body.append([m, n, yes, 100*yes/n if n else 0,
                         c['correct_abstention'], c['false_abstention'],
                         c['missed_abstention'], c['fallback_paraphrase']])

    write_csv(
        os.path.join(OUTPUT_DIR, "06_abstention_analysis.csv"),
        ["model", "N", "abstention_yes_n", "abstention_rate_pct",
         "correct_abstention_n", "false_abstention_n", "missed_abstention_n", "fallback_paraphrase_n"],
        csv_body,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "06_abstention_analysis.tex"),
        "Abstention behavior by model.",
        "tab:abstention_analysis",
        headers,
        body,
    )


def build_model_dataset_summary(rows, models, datasets):
    headers = ["Model", "Dataset", "N", "Substantive errors", "F*", "No error", "Abstention"]
    body = []
    csv_body = []
    for m in models:
        for d in datasets:
            rr = [r for r in rows if r["model"] == m and r["source_dataset"] == d]
            n = len(rr)
            c = error_counter(rr)
            sub = substantive_error_count(rr)
            abst = sum(clean(r["is_abstention"]).upper() == "YES" for r in rr)
            body.append([m, d, n, f"{sub} ({pct(sub,n)})", f"{c['F*']} ({pct(c['F*'],n)})", f"{c['No error']} ({pct(c['No error'],n)})", f"{abst} ({pct(abst,n)})"])
            csv_body.append([m,d,n,sub,c['F*'],c['No error'],abst])
    write_csv(
        os.path.join(OUTPUT_DIR, "07_model_dataset_summary.csv"),
        ["model","dataset","N","substantive_errors_n","Fstar_n","no_error_n","abstention_n"],
        csv_body,
    )
    write_latex_table(
        os.path.join(OUTPUT_DIR, "07_model_dataset_summary.tex"),
        "Model- and dataset-level summary for qualitative error analysis.",
        "tab:model_dataset_summary",
        headers,
        body,
        alignment="llrrrrr",
    )


def build_qualitative_examples(rows, models, per_model=3):
    """
    Select representative substantive errors for qualitative inspection.
    Selection is deterministic:
      - Prefer distinct error codes.
      - Prefer notes_2 when available, otherwise notes_1.
      - Prefer shorter examples so the resulting table remains readable.

    These are candidates for manual review before publication; the script does not
    claim that all selected examples are the most important cases.
    """
    candidates = []
    for m in models:
        rr = [r for r in rows if r["model"] == m and clean(r["final_error_code"]) not in {"No error", "F*", ""}]
        used_codes = set()
        selected = []
        # First pass: one example per distinct code.
        for r in rr:
            code = clean(r["final_error_code"])
            if code in used_codes:
                continue
            selected.append(r)
            used_codes.add(code)
            if len(selected) >= per_model:
                break
        # Second pass if too few distinct codes.
        if len(selected) < per_model:
            selected_ids = {r["sample_id"] for r in selected}
            for r in rr:
                if r["sample_id"] not in selected_ids:
                    selected.append(r)
                    if len(selected) >= per_model:
                        break
        candidates.extend(selected)

    headers = ["Model", "Dataset", "Sample", "Error", "Question", "Reference", "Prediction", "Annotation rationale"]
    body = []
    csv_body = []
    for r in candidates:
        rationale = clean(r.get("notes_2")) or clean(r.get("notes_1"))
        row = [
            r["model"], r["source_dataset"], r["sample_id"], r["final_error_code"],
            shorten(r["question"], 260), shorten(r["answer"], 240),
            shorten(r["predicted_answer"], 240), shorten(rationale, 360)
        ]
        body.append(row)
        csv_body.append(row)

    write_csv(
        os.path.join(OUTPUT_DIR, "08_qualitative_examples.csv"),
        [h.lower().replace(" ", "_") for h in headers],
        csv_body,
    )
    # This table is intentionally landscape-style in most papers.
    write_latex_table(
        os.path.join(OUTPUT_DIR, "08_qualitative_examples.tex"),
        "Representative qualitative error cases selected from the annotated dataset; examples should be manually reviewed before inclusion in the final manuscript.",
        "tab:qualitative_examples",
        headers,
        body,
        alignment="llrlllll",
    )


def build_figures(rows, models, datasets, codes):
    # Figure 1: heatmap of substantive error rates by model and code.
    substantive_codes = [c for c in codes if c not in {"No error", "F*"}]
    matrix = []
    for m in models:
        rr = [r for r in rows if r["model"] == m]
        n = len(rr)
        c = error_counter(rr)
        matrix.append([100*c[code]/n if n else 0 for code in substantive_codes])

    fig, ax = plt.subplots(figsize=(12, 5.5))
    im = ax.imshow(matrix, aspect="auto")
    ax.set_xticks(range(len(substantive_codes)))
    ax.set_xticklabels(substantive_codes)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models)
    ax.set_xlabel("Substantive error code")
    ax.set_ylabel("Model")
    ax.set_title("Substantive Error Distribution by Model")
    for i in range(len(models)):
        for j in range(len(substantive_codes)):
            ax.text(j, i, f"{matrix[i][j]:.1f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="Percentage of model samples")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_error_heatmap.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Figure 2: substantive-error rate by model.
    rates = []
    for m in models:
        rr = [r for r in rows if r["model"] == m]
        rates.append(100*substantive_error_count(rr)/len(rr))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(models, rates)
    ax.set_ylabel("Substantive errors (%)")
    ax.set_xlabel("Model")
    ax.set_title("Substantive Error Rate by Model")
    ax.tick_params(axis="x", rotation=25)
    for i, v in enumerate(rates):
        ax.text(i, v, f"{v:.1f}%", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_substantive_error_rates.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Figure 3: abstention rate by model.
    abst_rates = []
    for m in models:
        rr = [r for r in rows if r["model"] == m]
        yes = sum(clean(r["is_abstention"]).upper() == "YES" for r in rr)
        abst_rates.append(100*yes/len(rr))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(models, abst_rates)
    ax.set_ylabel("Abstention rate (%)")
    ax.set_xlabel("Model")
    ax.set_title("Abstention Rate by Model")
    ax.tick_params(axis="x", rotation=25)
    for i, v in enumerate(abst_rates):
        ax.text(i, v, f"{v:.1f}%", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_abstention_rate.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def build_readme(rows, models, datasets, codes):
    total = len(rows)
    lines = [
        "# Error Analysis Outputs",
        "",
        f"Generated from `{INPUT_CSV}`.",
        "",
        f"- Total samples: {total}",
        f"- Models: {', '.join(models)}",
        f"- Datasets: {', '.join(datasets)}",
        f"- Final error codes: {', '.join(codes)}",
        "- The source-construction script samples 50 instances per dataset per model with `random_state=42`.",
        "- `final_error_code` is the primary source for error-distribution tables.",
        "- `No error` and `F*` are reported separately from substantive error codes.",
        "",
        "## Recommended manuscript use",
        "1. Main paper: use aggregate tables 01, 02, 03, and 04; qualitative examples are withheld from public output pending source-data redistribution review.",
        "2. Main paper or appendix: use 05 for dataset-level differences.",
        "3. Methods/annotation reliability: use agreement statistics separately if desired.",
        "4. Agreement: use 09_interannotator_agreement for Methods/annotation reliability.",
        "5. The reconstructed taxonomy table is withheld until checked against the original annotation guideline.",
        "6. sample_alignment_diagnostic.csv checks input-signature alignment; model-specific sample_id values may differ.",
        "6. Figures: the heatmap and substantive-error-rate figure are the most useful.",
        "",
        "## Important interpretation note",
        "This script does not create a question-type taxonomy because the CSV contains no explicit question-type label. `source_dataset` is used as the available dataset-level grouping.",
    ]
    with open(os.path.join(OUTPUT_DIR, "README.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    make_output_dir()
    rows = read_csv(INPUT_CSV)
    ensure_required_columns(rows)
    legacy_model_names = {"RAG": "RB-ICL", "RAG+DeepSeek": "RB-ICL+DeepSeek", "RAG + DeepSeek": "RB-ICL+DeepSeek"}
    for row in rows:
        row["model"] = legacy_model_names.get(clean(row.get("model")), clean(row.get("model")))
    models = sort_models(rows)
    datasets = sort_datasets(rows)
    codes = code_order(rows)

    build_overall_error_distribution(rows, models, codes)
    build_substantive_error_rates(rows, models)
    build_human_acceptability_tables(rows, models, datasets)
    build_pairwise_dora_lora(rows)
    build_rb_icl_error_profile(rows)
    build_dataset_model_error_profile(rows, models, datasets)
    build_abstention_analysis(rows, models)
    build_model_dataset_summary(rows, models, datasets)
    # Qualitative examples are intentionally not generated in the public release.
    # They contain benchmark-derived text and require separate redistribution review.
    build_interannotator_agreement(rows, models, datasets)
    build_figures(rows, models, datasets, codes)
    build_readme(rows, models, datasets, codes)

    print(f"Done. Outputs written to: {OUTPUT_DIR}/")
    print(f"Rows: {len(rows)}")
    print(f"Models: {models}")
    print(f"Datasets: {datasets}")
    print(f"Error codes: {codes}")


if __name__ == "__main__":
    main()
