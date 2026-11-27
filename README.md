# A Systematic Comparison of Parameter-Efficient Fine-Tuning and Retrieval-Based In-Context Learning for Large Language Model-Based Question Answering

This repository contains research notebooks and supporting artifacts for a comparative study of parameter-efficient fine-tuning (PEFT) and retrieval-based in-context learning (RB-ICL) for generative question answering.

**GitHub repository:** https://github.com/TheNexoraLabs/peft-vs-rbicl-qa

## Archived release and DOI

The current software release (**v0.1.2**) is archived on Zenodo:

- **Version DOI (v0.1.2):** https://doi.org/10.5281/zenodo.24597976

The previous archived release (**v0.1.1**) is also available:

- **Version DOI (v0.1.1):** https://doi.org/10.5281/zenodo.24582468

- **Concept DOI (all versions):** https://doi.org/10.5281/zenodo.24582467

Use the version-specific DOI when citing or identifying the exact software snapshot. Use the Concept DOI when referring to the project across releases.

## Authors

- **Mahsima Ebrahimi Moghadam** — National University of Skills (NUS), Tehran, Iran. Equal contribution.
- **Seyyed Amir Hossein Mousavi** — Science and Research Branch, Islamic Azad University, Tehran, Iran. Equal contribution.
- **Ensieh AbbasiRad** — National University of Skills (NUS), Tehran, Iran. Supervising and corresponding author.

Full affiliation details are provided in `AUTHORS.md`.

## Experimental systems

The study evaluates six configurations:

| Configuration | Main notebook |
|---|---|
| LoRA + Meta-Llama-3.1-8B-Instruct | `notebooks/01_lora_llama31.ipynb` |
| DoRA + Meta-Llama-3.1-8B-Instruct | `notebooks/02_dora_llama31.ipynb` |
| LoRA + DeepSeek-R1-Distill-Llama-8B | `notebooks/03_lora_deepseek_distill.ipynb` |
| DoRA + DeepSeek-R1-Distill-Llama-8B | `notebooks/04_dora_deepseek_distill.ipynb` |
| RB-ICL + Meta-Llama-3.1-8B-Instruct | `notebooks/05_rb_icl_llama31.ipynb` |
| RB-ICL + DeepSeek-R1-Distill-Llama-8B | `notebooks/06_rb_icl_deepseek_distill.ipynb` |

Shared inference/scoring notebooks are `notebooks/07_shared_qa_inference.ipynb` and `notebooks/08_shared_qa_scoring.ipynb`. Four additional cleaned QA execution records for the PEFT configurations are stored under `notebooks/qa_inference_runs/`; outputs are cleared while run timestamps are retained.

## Datasets

The prepared QA corpus was constructed from SQuAD v2, TweetQA, CoQA, and NLQuAD. Prepared dataset CSVs and benchmark source text are not redistributed. The notebooks expect a prepared CSV to be supplied locally or in the Kaggle runtime. The authors confirmed that the differently mounted prepared CSV copies used in the final runs have identical contents.

## Environment and authentication

The experiments were developed in Kaggle GPU notebook environments. Principal package versions are listed in `environment/installation_notes.md` and the notebook setup cells. Some models may require Hugging Face authentication and acceptance of model terms. Authenticate interactively or use a platform secret manager; never commit access tokens.

## Results and timing

- `results/primary_300/`: data-minimized per-example metrics for the primary 300-question evaluation.
- `results/overlap_filtered_280/`: sensitivity analysis on the 280-question overlap-filtered subset.
- `results/statistical_analysis/`: reported statistical tables.
- `results/human_evaluation/`: aggregate human-evaluation tables and figures.
- `results/training_logs/`: PEFT training and evaluation logs.
- `results/resource_usage/`: computational-cost workbook, GPU memory measurements, training timers, QA inference cell measurements, and Notebook run metadata.

All six QA timing values in the current computational-cost table cover the same 300-question Q1 test set. Four PEFT QA notebooks were matched to the corresponding model by exact row-wise prediction equality (300/300 for each). The RB-ICL values come from Jupyter execution metadata for the 300-query Retrieval+Generation cells, cross-checked against explicit internal timers. See `docs/RUNTIME_MEASUREMENT_PROVENANCE.md` and `docs/QA_INFERENCE_TIMING_AUDIT.md` for exact timer boundaries and timestamps.

The compact public per-example result files omit benchmark context, question, reference-answer text, and generated answer text. Raw annotation-level files and model weights are not redistributed.

## Statistical and human analysis

The statistical implementation is in `analysis/statistical/statistical_analysis.py`. Human-evaluation aggregates use the manuscript's acceptability definition (`No error` + `F*`). The two initial annotators were evaluated for pre-adjudication agreement; a supervising third reviewer adjudicated the final labels after reviewing both initial labels and the accompanying record information. The protocol and complete error codebook are documented in [`docs/HUMAN_EVALUATION_PROTOCOL.md`](docs/HUMAN_EVALUATION_PROTOCOL.md). Raw annotator-level files are not redistributed. No claim is made that retrieval correctness was independently verified.

## Citation and license

Citation metadata is in `CITATION.cff`. Cite the Version DOI corresponding to the release snapshot you use; use the Concept DOI when citing the project across versions. The repository code is distributed under MIT; datasets, pretrained models, and third-party assets remain under their respective terms.

## Known limitations

- Prepared dataset CSVs and model weights are not included.
- Reproduction may require Kaggle-compatible CUDA/GPU versions, access to gated models, and the original dataset revisions.
- The QA time figures are observed notebook/loop wall times, not hardware-independent GPU decoding benchmarks.
- Raw inference outputs and raw annotations are withheld; the error-code definitions and annotation procedure are documented in `docs/HUMAN_EVALUATION_PROTOCOL.md`.
