# CHECKPOINTS — Go/No-Go Gates (The Project's Heartbeat)

Every task in `day_plans/` maps to a checkpoint ID. You are never "doing the
project"; you are clearing the next checkpoint. The status file `results/status.json`
is updated by `scripts/where_am_i.py`.

## Gate 1 — End of Day 1: "Data Exists" (CP-1.x)
- [x] CP-1.1 Competition registered; submission format confirmed.
- [x] CP-1.2 GitHub repo created, kit committed, branch protection set.
- [x] CP-1.3 N-ATLAS access via HF working (sanity check logged).
- [x] CP-1.4 20 draft passages generated (Mixed English, Yoruba, Pidgin).
- [x] CP-1.5 All 20 human-reviewed, corrected, and committed to `data/passages.jsonl`.
- [x] CP-1.6 `scripts/prepare_dataset.py` built to pull a 500-row SQuAD benchmark for ML scale

## Gate 2 — End of Day 2: "Pipeline Works & Model Fine-Tuned" (CP-2.x)
- [x] CP-2.1 `run_eval.py` runs base N-ATLAS, Qwen, and Llama on the 20 Nigerian passages.
- [x] CP-2.2 Base models scored, results JSON logged (Proved 3.50 cultural baseline gap).
- [x] CP-2.3 Rubric v1 frozen (LLM-as-a-Judge prompt).
- [x] CP-2.4 Diagnostic function returns correct label on 5 hand-crafted test cases.
- [x] CP-2.5 QLoRA fine-tune completed on 400 SQuAD rows to bridge the pedagogical gap.
- [x] CP-2.6 Fine-tuned adapter pushed to Hugging Face (`Semziee/pagezy-n-atlas-qlora-500`).

## Gate 3 — End of Day 3: "Demoable" (CP-3.x)
- [x] CP-3.1 Tab 1 full loop works live: passage → audio → answer → hint → diagnostic.
- [x] CP-3.2 Tab 2 leaderboard renders real eval results (The 4.47 vs 3.50 metrics).
- [x] CP-3.3 At least 2 pre-recorded MP3s wired in (Accessibility layer).
- [x] CP-3.4 App integrates the fine-tuned QLoRA adapter for hint generation.

## Gate 4 — End of Day 4: "Credible" (CP-4.x)
- [x] CP-4.1 "Powered by Awarri" badge in footer.
- [x] CP-4.2 README states N-ATLAS Research License compliance.
- [x] CP-4.3 Safety & Limitations section complete.
- [x] CP-4.4 `requirements.txt` pins versions; tested fresh.

## Gate 5 — End of Day 5: "Told" (CP-5.x)
- [x] CP-5.1 3-minute video recorded: Problem → Demo → Engineering Rigor (The Fine-Tune).
- [x] CP-5.2 Video shows the NBS/UNICEF stat and the read-vs-listen explanation.
- [x] CP-5.3 Video shows leaderboard tab + states ASR fine-tuning roadmap.

## Gate 6 — End of Day 6: "Submitted" (CP-6.x)
- [x] CP-6.1 Demo served via Google Colab with live Gradio share link (used instead of HF Spaces).
- [x] CP-6.2 Repo link + Gradio live link + HF Model link + video submitted via portal.