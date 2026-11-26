# A Systematic Comparison of Parameter-Efficient Fine-Tuning and Retrieval-Based In-Context Learning for Large Language Model-Based Question Answering

This repository contains the research notebooks and supporting artifacts for the comparative study of parameter-efficient fine-tuning (PEFT) and retrieval-based in-context learning (RB-ICL) for generative question answering.

**Repository:** <https://github.com/TheNexoraLabs/peft-vs-rbicl-qa>

## Authors

The author order follows the current manuscript:

- **Mahsima Ebrahimi Moghadam** — National University of Skills (NUS), Tehran, Iran. Equal contribution.
- **Seyyed Amir Hossein Mousavi** — Science and Research Branch, Islamic Azad University, Tehran, Iran. Equal contribution.
- **Ensieh AbbasiRad** — National University of Skills (NUS), Tehran, Iran. Supervising and corresponding author.

The first and second authors contributed equally. Full affiliation details are provided in [`AUTHORS.md`](AUTHORS.md).

## Repository status

This repository provides the research notebooks and supporting artifacts for the comparative study. It includes data-minimized evaluation results and aggregate human-evaluation summaries. It does not redistribute benchmark source text, model weights, raw annotator-level records, or credentials. See the documentation for provenance and known reproducibility limitations.

## Experimental systems

The study evaluates six configurations:

| Notebook | Configuration |
|---|---|
| `notebooks/01_lora_llama31.ipynb` | LoRA with Meta-Llama-3.1-8B-Instruct |
| `notebooks/02_dora_llama31.ipynb` | DoRA with Meta-Llama-3.1-8B-Instruct |
| `notebooks/03_lora_deepseek_distill.ipynb` | LoRA with DeepSeek-R1-Distill-Llama-8B |
| `notebooks/04_dora_deepseek_distill.ipynb` | DoRA with DeepSeek-R1-Distill-Llama-8B |
| `notebooks/05_rb_icl_llama31.ipynb` | RB-ICL with the Llama 3.1 backbone |
| `notebooks/06_rb_icl_deepseek_distill.ipynb` | RB-ICL with the DeepSeek-R1-Distill-Llama backbone |
| `notebooks/07_shared_qa_inference.ipynb` | Shared inference workflow used with the selected final checkpoint |
| `notebooks/08_shared_qa_scoring.ipynb` | Shared answer-scoring workflow |

## Datasets

The prepared QA corpus was constructed from SQuAD v2, TweetQA, CoQA, and NLQuAD. The prepared CSV is not redistributed here. The notebooks expect `finetune_dataset_fixed_3000.csv`; obtain the source data from the authorized dataset repositories and make the prepared CSV available to the runtime. The authors confirmed that the differently mounted CSV copies used in the final runs have identical contents.

The supplementary HotpotQA material is not required for the six primary systems unless explicitly stated by the corresponding notebook.

## Environment and authentication

The experiments were developed in a Kaggle GPU environment. Principal package versions and installation notes are provided in `environment/installation_notes.md` and in the notebook setup cells. Exact compatibility depends on the runtime image, CUDA version, and GPU availability.

Some models may require Hugging Face authentication and acceptance of their model terms. Authenticate interactively or use the platform's secret manager. Never commit Hugging Face, Kaggle, or other access tokens to this repository.

## Results and analysis

- `results/primary_300/` contains data-minimized per-example metric results for the primary 300-example evaluation.
- `results/overlap_filtered_280/` contains the 280-example overlap-filtered sensitivity analysis.
- `results/statistical_analysis/` contains the reported statistical tables.
- `results/human_evaluation/` contains aggregate human-evaluation tables and figures. Raw annotator-specific files and the full adjudicated annotation source are not redistributed.
- `results/training_logs/` contains PEFT training and evaluation logs.
- `results/resource_usage/` records resource-measurement sources. Full saved-Notebook duration, code-level timing scopes, and manuscript-reported Training/Adaptation and QA Runtime are kept distinct; see `docs/RUNTIME_MEASUREMENT_PROVENANCE.md`.

The compact result files omit benchmark context, questions, reference-answer text, and generated answer text. `scripts/add_sample_ids.py` documents the stable sample-ID construction used for paired analysis.

## Statistical analysis

The statistical-analysis implementation is in `analysis/statistical/statistical_analysis.py`. Required Python packages are listed in `analysis/statistical/requirements.txt`. The script and the published tables should be interpreted together with `docs/STATISTICAL_REPRODUCIBILITY_CHECK.md`.

## Human evaluation

Human-acceptability summaries use the manuscript's definition (`No error` + `F*`). The repository contains aggregated tables and figures only. It does not contain row-level annotator-specific files or raw annotation exports. No claim is made that retrieval correctness was independently verified.

## Citation

The repository citation metadata is provided in [`CITATION.cff`](CITATION.cff). Please cite the repository when using its code or derived artifacts. When the associated manuscript is published, add its final journal citation and DOI to the repository citation metadata and manuscript.

## License

The code in this repository is distributed under the [MIT License](LICENSE). The license applies to the repository code and associated software files. Dataset materials, pretrained model weights, and third-party assets remain subject to their respective licenses and terms.

## Known limitations of this release candidate

- The prepared dataset CSV and model weights are not included.
- Some paths and caches remain Kaggle-oriented and may need adaptation outside Kaggle.
- Reproducing the exact reported model runs may require the original GPU runtime, model access, and data revisions.
- Raw inference outputs and row-level human annotations are intentionally withheld.
- The reconstructed error taxonomy is withheld pending verification against the original annotation guideline.
