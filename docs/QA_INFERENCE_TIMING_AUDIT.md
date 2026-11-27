# QA inference timing audit

The four newly supplied QA loader notebooks can be mapped unambiguously to the four PEFT configurations. The mapping was made by extracting every response from the saved inference-cell output and comparing it row-by-row with the `predicted_answer` field in the corresponding Q1 `evaluated_results.csv` file.

| Notebook | Model | Rows | Exact matches | Empty answers | Generation cell |
|---|---|---:|---:|---:|---:|
| `loader-llama3-1.ipynb` | DoRA | 300 | 300/300 | 0 | 00:32:36.86 |
| `loader-llama3-2.ipynb` | DoRA + DeepSeek | 300 | 300/300 | 0 | 01:52:34.56 |
| `loader-llama3-3.ipynb` | LoRA | 300 | 300/300 | 0 | 00:24:27.63 |
| `loader-llama3-4.ipynb` | LoRA + DeepSeek | 300 | 300/300 | 0 | 01:46:28.58 |

The best alternative model match was 280/300 for the Llama-backbone pairings and 292/300 for the DeepSeek pairings. This makes all four identifications clear.

The generation settings in the four loader notebooks include `max_new_tokens=300`, `do_sample=False`, `repetition_penalty=1.1`, and input truncation at 2048 tokens. The saved cell runtime includes prompt creation, tokenization, generation, decoding, per-answer printing, and final DataFrame display.

For RB-ICL and RB-ICL + DeepSeek, the final V4 and V5 notebooks contain a single Jupyter cell with the 300-question Retrieval+Generation loop. The cell metadata gives 00:10:52.47 and 00:21:33.98, respectively; the code-level timers independently agree within 0.30 seconds. Both notebooks report zero prompt-budget fallbacks.

The public copies in `notebooks/qa_inference_runs/` have cleared outputs to avoid redistribution of benchmark text and generated answers. Their execution metadata is retained as timing provenance, and the private Google Drive checkpoint-download cells have been removed.
