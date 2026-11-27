# Human Evaluation Protocol and Error Codebook

## 1. Purpose and scope

This document describes the human evaluation used to assess generated answers in the question-answering experiments. It records the sample composition, the two-stage annotation and adjudication procedure, the operational error labels, and the statistics reported for annotation reliability and human acceptability.

The human evaluation is a manually annotated subset analysis. It is not a full human evaluation of every item in the 300-question automatic test set, nor is it a user-preference study.

## 2. Evaluation sample

The adjudicated evaluation set contains **1,200 model-response records** across six evaluated systems:

| System | Annotated responses |
|---|---:|
| LoRA | 200 |
| DoRA | 200 |
| RB-ICL | 200 |
| LoRA + DeepSeek | 200 |
| DoRA + DeepSeek | 200 |
| RB-ICL + DeepSeek | 200 |
| **Total** | **1,200** |

For each system, the 200 records comprise 50 question instances from each of the four source datasets: SQuAD v2, CoQA, TweetQA, and NLQuAD. The six systems were evaluated on the same underlying 200 question instances. The repository's sample-alignment diagnostic compares input signatures (dataset, split, context, and question) to document this correspondence; identifiers assigned to individual model-response records are not assumed to be globally identical.

The resulting counts describe this balanced human-evaluation subset. They should not be interpreted as counts from the full automatic test set.

## 3. Annotation and adjudication procedure

The procedure had two distinct stages:

1. **Independent initial annotation.** Two annotators independently assessed each model response and recorded their respective labels. The initial annotation stage was conducted under blinded conditions with respect to the evaluated system's identity.
2. **Adjudication.** A third reviewer, the supervising advisor, examined the two initial annotations together with the other information available for that record and entered the final decision in `final_error_code`. The third reviewer therefore acted as an adjudicator, not as a third independent rater: the adjudication stage explicitly used the first two reviewers' labels.

The `final_error_code` field is the adjudicated label used for the final error-distribution and acceptability analyses. The two initial labels (`annotator_1` and `annotator_2`) are used for inter-annotator agreement calculations. The adjudicated labels must not be substituted for either initial rater when calculating pre-adjudication reliability.

The three annotation files are author-held working records. The public repository does not redistribute those files or the merged row-level annotation table.

## 4. Error codebook

The following operational definitions are the error categories used in the study. A final code describes the principal outcome assigned to a response during adjudication.

### A — Answer content and completeness

| Code | Definition |
|---|---|
| **A1 — Wrong span or entity** | The prediction is factually or referentially wrong because it selects the wrong entity, span, value, person, place, object, or answer. |
| **A2 — Incomplete answer** | The prediction contains part of the required answer but omits an essential part of the reference or an essential sub-question. |
| **A3 — Unsupported content** | The prediction introduces substantive information that is not supported by the supplied context, including hallucinated facts, additional unsupported claims, or external knowledge inserted into a context-grounded QA task. |
| **A4 — Sub-question aggregation** | The question contains multiple explicit sub-questions and the model fails to correctly organize or answer those sub-questions as separate required components. |

### B — Abstention behavior

| Code | Definition |
|---|---|
| **B1 — False abstention** | The model abstains even though the answer is available or recoverable from the supplied context. |
| **B2 — Missed abstention** | The question is genuinely unanswerable from the supplied context, but the model produces a substantive answer instead of abstaining. |
| **B3 — Fallback paraphrase** | The model makes the correct abstention decision but uses wording different from the canonical fallback answer. |

### C — Response form and presentation

| Code | Definition |
|---|---|
| **C1 — Verbosity or padding** | The prediction contains unnecessary explanation, repetition, elaboration, or unsupported verbal padding that is not required to answer the question. |
| **C2 — Meta-commentary** | The model talks about the task, the user, external sources, how to answer, or what the user should do instead of directly answering the question. |
| **C3 — Reasoning-trace leakage** | The model exposes internal reasoning, chain-of-thought-like deliberation, hidden analysis, or extensive step-by-step reasoning that should not be part of the requested answer. |
| **C4 — Answer-type mismatch** | The prediction does not match the type or form of answer requested by the question. |

### D — Context and input-related failures

| Code | Definition |
|---|---|
| **D1 — Conversational reference** | The model fails to resolve conversational references, pronouns, ellipsis, or context-dependent references correctly. |
| **D2 — Long context or truncation** | There is evidence that long context, truncation, or context-window effects are responsible for the failure. |
| **D3 — Noisy or pragmatic input** | The failure is primarily caused by noisy, informal, ambiguous, fragmented, pragmatic, or socially implicit input. |

### Non-substantive outcomes

| Code | Definition |
|---|---|
| **F\*** | **Metric/reference artefact.** The issue is primarily caused by reference wording, normalization, or metric behavior rather than the model's actual task behavior. Under the study's operational definition, this is a non-substantive error category. |
| **No error** | The prediction is factually correct, supported by the context, responsive to the question, and acceptable in form. |

## 5. Human acceptability

Human acceptability is operationalized as:

\[
\text{Acceptable} = (\texttt{final\_error\_code} = \text{No error})\;\lor\;(\texttt{final\_error\_code} = \text{F*}).
\]

Thus, **No error** and **F\*** are counted as acceptable, while A1–D3 are counted as substantive errors. F\* is retained as a separate category in error-distribution tables; it is not merged into `No error` in those tables.

The reported counts in the adjudicated sample are:

| System | Acceptable | Rate |
|---|---:|---:|
| LoRA | 155 / 200 | 77.5% |
| DoRA | 148 / 200 | 74.0% |
| RB-ICL | 141 / 200 | 70.5% |
| LoRA + DeepSeek | 135 / 200 | 67.5% |
| DoRA + DeepSeek | 132 / 200 | 66.0% |
| RB-ICL + DeepSeek | 125 / 200 | 62.5% |

These rates are specific to the adjudicated 200-response subset per system and to the acceptability definition above. They are not a general-purpose preference score.

## 6. Inter-annotator agreement

Inter-annotator agreement is computed between the **two independent initial annotators**, before adjudication, using their 1,200 paired labels:

- Exact agreement: **722 / 1,200 (60.17%)**.
- Cohen's kappa: **0.397** (rounded to three decimal places).

These values describe agreement between the two initial annotators. The supervising advisor's adjudicated labels are not treated as an additional independent rating and are not included in this reliability calculation.

## 7. Confidence intervals

The human-acceptability tables report 95% percentile-bootstrap confidence intervals. The public analysis implementation uses 20,000 bootstrap replicates with seed 42 and resamples within each source-dataset stratum, preserving the observed number of records in each dataset for the relevant system. The implementation and generated aggregate tables should be kept synchronized if the analysis is rerun.

## 8. Public release and reproducibility

The public repository contains aggregate tables, figures, the sample-alignment diagnostic, the analysis-generation script, and this protocol/codebook. It does **not** contain the source annotation CSV files or the merged row-level annotation table. Those files include benchmark-derived context, questions, reference answers, model predictions, and annotator notes; they are retained by the authors and are not redistributed in this repository.

Because the author-held input table is not public, the aggregate-generation script is provided for transparency but cannot be executed from the public repository alone. A user seeking to reproduce the aggregates must have authorized access to the same adjudicated input table and the corresponding benchmark-derived records.

## 9. Interpretation and limitations

- The agreement statistic is calculated before adjudication; final error distributions and acceptability use the adjudicated labels.
- The adjudication process involved one supervising reviewer who had access to both initial labels and the accompanying record information. It should not be described as a third blind independent annotation.
- The human evaluation covers a balanced subset of 200 responses per system, not all responses in the automatic evaluation.
- The taxonomy-based acceptability outcome is not a holistic measure of user preference, helpfulness, or every dimension of answer quality.
- Automatic metrics and human labels capture different aspects of generated-answer behavior and should be interpreted as complementary evidence.
