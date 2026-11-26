# Runtime measurement provenance (updated after Kaggle version-history check)

## What is being measured

Three different quantities must remain separate:

1. **Full saved Notebook execution duration**: the `papermill` metadata `start_time`, `end_time`, and `duration` in each uploaded GPU-calculator Notebook. These records have `exception = null`.
2. **Code-level timer**: the interval explicitly measured inside the Notebook. For PEFT it begins immediately before `SFTTrainer` construction and ends after training, saving, and cleanup. For RB-ICL it measures only the 300-question Retrieval + Generation loop; model loading and vector-index setup occur before the timer.
3. **Manuscript values**: the currently reported Training/Adaptation Time and QA Runtime values in Table `tab:computational_cost`. These are distinct metrics and should not be replaced with full Notebook duration.

## Saved Notebook execution evidence

| Configuration | Full Notebook duration | Code-level timer | Kaggle UI cross-check |
|---|---:|---:|---|
| LoRA + Meta-Llama-3.1-8B-Instruct | 03:48:12.07 | 03:45:31.81 | Confirmed by author-provided Kaggle Version page: Save & Run All, 7 Sep 2026, ran in 3 h 48 min. |
| DoRA + Meta-Llama-3.1-8B-Instruct | 08:48:06.06 | 08:45:31.08 | Papermill metadata only; no separate screenshot supplied. |
| LoRA + DeepSeek-R1-Distill-Llama-8B | 04:15:14.82 | 04:12:31.93 | Papermill metadata only; no separate screenshot supplied. |
| DoRA + DeepSeek-R1-Distill-Llama-8B | 09:05:19.43 | 09:02:31.80 | Papermill metadata only; no separate screenshot supplied. |
| RB-ICL + Meta-Llama-3.1-8B-Instruct | 00:19:06.66 | 00:10:52.77 | Papermill metadata only; no separate screenshot supplied. |
| RB-ICL + DeepSeek-R1-Distill-Llama-8B | 00:29:56.53 | 00:21:34.27 | Papermill metadata only; no separate screenshot supplied. |

The LoRA Kaggle Version page check matches the saved Notebook Papermill duration rounded to the minute. It also establishes that the old workbook value of 00:52 does **not** describe that exact Run All version. The other five saved Notebook metadata records have successful completion status (`exception = null`), but their exact Kaggle UI pages have not each been independently checked.

## Legacy workbook time entries

The original workbook contained 00:52, 02:30, 00:50, 03:00, 00:14, and 00:14. The author recalled these as Kaggle Run All durations. However, the LoRA UI cross-check demonstrates that at least the 00:52 entry is not the duration of the saved LoRA Run All version examined here. The remaining workbook values cannot be mapped to exact saved Notebook versions from the available evidence. They are therefore retained only as legacy, unmatched entries in the audit CSV and are not used as full-run durations.

## Relation to the manuscript cost table

The full Notebook duration is not the same as the manuscript's separate Training/Adaptation Time or QA Runtime. In particular:

- For PEFT, the code-level timer is the available direct measure of the adaptation pipeline. It is close to, but not identical with, the full Notebook duration.
- For RB-ICL, the code-level timer measures the 300-question loop and excludes model/index setup. The full Notebook duration includes the earlier setup cells.
- The author clarified that the same shared QA inference loader was used for all six model configurations, with the selected checkpoint path changed between runs. The supplied loader source has no explicit per-run timer and does not preserve six separate run records, so it cannot independently validate the six manuscript QA-runtime values. The shared Scoring Notebook calculates metrics and does not measure response-generation time.

Therefore, this package does not silently replace any manuscript timing values. The manuscript QA-runtime figures still need a consistent, traceable source for all six systems before they can be revised confidently.

## GPU memory

Peak allocated and peak reserved GPU-memory values are taken from the six corresponding `gpu_memory_log.csv` files. The manuscript reports peak allocated GPU memory, and those values match its table. The original workbook's separate GPU RAM, System RAM, and Disk observations are not included in this public release because their raw source/measurement boundary was not supplied.
