# Runtime measurement provenance (Q1-aligned update)

## Decision

The main manuscript table now reports (i) the explicit PEFT training/adaptation timer and (ii) the QA query-processing interval measured over the same 300-question primary test set (Q1) for all six systems. Full Notebook Run All durations are retained separately and are not substituted for QA runtime.

## QA model identification from the four uploaded loader notebooks

The four notebooks in `notebooks/qa_inference_runs/` were mapped to systems by extracting all 300 responses from their saved generation-cell outputs and comparing them row-by-row against the corresponding per-system `predicted_answer` column in the Q1 evaluation CSVs. Each mapping produced 300/300 exact matches and zero empty answers. The best alternative system had fewer matches (280/300 for the Llama-backbone pairings; 292/300 for the DeepSeek pairings), so the mapping is unambiguous.

| Uploaded source notebook | Identified system | Exact Q1 prediction matches | Generation-cell runtime | Full QA Notebook Run All |
|---|---|---:|---:|---:|
| `loader-llama3-1.ipynb` | DoRA | 300/300 | 00:32:36.86 | 00:35:17.63 |
| `loader-llama3-2.ipynb` | DoRA + DeepSeek | 300/300 | 01:52:34.56 | 01:55:55.00 |
| `loader-llama3-3.ipynb` | LoRA | 300/300 | 00:24:27.63 | 00:27:18.59 |
| `loader-llama3-4.ipynb` | LoRA + DeepSeek | 300/300 | 01:46:28.58 | 01:49:17.20 |

The notebook filenames themselves did not encode adapter/backbone identity; the system attribution above is based on exact prediction matching, not on the generic comments in the original loader cells.

## QA runtime definition used in the manuscript

All six systems were timed on 300 Q1 test questions.

- **LoRA/DoRA systems:** the saved Jupyter execution metadata (`iopub.execute_input` to `iopub.status.idle`) for the cell containing the complete 300-question generation loop was used. The interval includes prompt creation, tokenization, generation, decoding, per-answer console printing, and the final DataFrame output/display. The values are therefore observed inference-cell wall times, not pure GPU decoding times.
- **RB-ICL systems:** the Jupyter execution metadata for the cell containing the 300-question Retrieval+Generation loop in the final V4/V5 GPU-calculator notebooks was used. The cell intervals agree with the explicit `time.time()` timers to within 0.30 seconds. Model loading and vector-index construction occur before this cell. The notebook output reports 0/300 prompt-budget fallbacks for both systems.

These are the best available run-level measurements of the per-question QA pipeline for the common Q1 workload. Their boundaries are documented transparently; they should not be interpreted as a hardware-independent decoding benchmark.

## QA runtime values used in the paper

| System | QA runtime | Mean seconds/query |
|---|---:|---:|
| LoRA | 00:24:27.63 | 4.8921 |
| DoRA | 00:32:36.86 | 6.5229 |
| LoRA + DeepSeek | 01:46:28.58 | 21.2953 |
| DoRA + DeepSeek | 01:52:34.56 | 22.5152 |
| RB-ICL | 00:10:52.47 | 2.1749 |
| RB-ICL + DeepSeek | 00:21:33.98 | 4.3133 |

## Training/adaptation timing

The PEFT training/adaptation times remain the explicit code-level timers in the final GPU-calculator notebooks. The timer starts immediately before `SFTTrainer` construction and ends after training, model/tokenizer saving, cleanup, and CUDA synchronization. These are not full Notebook Run All durations.

| System | Training/adaptation time |
|---|---:|
| LoRA | 03:45:31.81 |
| DoRA | 08:45:31.08 |
| LoRA + DeepSeek | 04:12:31.93 |
| DoRA + DeepSeek | 09:02:31.80 |

## Full Notebook Run All durations kept separately

| System | QA-loader / RB-ICL full Notebook duration |
|---|---:|
| LoRA | 00:27:18.59 |
| DoRA | 00:35:17.63 |
| LoRA + DeepSeek | 01:49:17.20 |
| DoRA + DeepSeek | 01:55:55.00 |
| RB-ICL | 00:19:06.66 |
| RB-ICL + DeepSeek | 00:29:56.53 |

The previously reported PEFT QA times (27:31, 35:30, 1:49:29, and 1:56:11) are close to the full QA Notebook durations (within approximately 12–16 seconds), suggesting that they captured full Run All/session duration rather than the inference cell alone. The RB-ICL manuscript values did not match the inference-cell metadata or the saved full-run metadata. The current table now uses Jupyter execution-cell intervals for all six systems and records full Run All durations separately.

## Main table values and GPU memory

Peak allocated GPU memory remains unchanged and matches the six GPU memory logs: 11.622, 13.106, 11.866, 13.350, 7.171, and 7.414 GB in the manuscript's system order. The legacy workbook hour entries (00:52, 02:30, 00:50, 03:00, 00:14, 00:14) could not be mapped to the exact saved runs and are not used.
