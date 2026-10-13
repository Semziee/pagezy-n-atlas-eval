# 02 — System Architecture: How Every Part Connects

## The One-Sentence Architecture
> One repository, four layers, two entry points: curated data feeds an evaluation
> harness and a product demo, both running on the same inference layer, with every
> artifact scored, logged, and traceable back to its source.

## Layer Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│ PRODUCT LAYER (app/)                    HARNESS LAYER (harness/) │
│  Gradio Tab 1: Pagezy Demo              Gradio Tab 2: Leaderboard│
│  - select passage                       - rubric scores per model│
│  - "Read Aloud" (TTS/pre-recorded MP3)  - safety checks          │
│  - answer question                      - run logs               │
│  - diagnostic: Decoding vs Comprehension                         │
└───────┬──────────────────────────────────────┬───────────────────┘
        │ calls                                │ calls
┌───────▼──────────────────────────────────────▼───────────────────┐
│ INFERENCE LAYER (scripts/run-inference.py)                       │
│  N-ATLAS-LLM (primary)  |  Qwen2.5-3B  |  Llama-3.2-3B           │
│  HF transformers, bfloat16 / 4-bit bitsandbytes                  │
│  Dev: Google Colab T4/A100  →  Demo: HF Spaces                   │
└───────┬──────────────────────────────────────────────────────────┘
        │ prompted with
┌───────▼──────────────────────────────────────────────────────────┐
│ DATA LAYER (data/)                                               │
│  data/passages.jsonl — 40–60 human-verified passages             │
│  fields: id, language, curriculum_tag, text, questions[],        │
│          diagnostic_type, tts_audio_path                         │
└──────────────────────────────────────────────────────────────────┘
        │ every run produces
┌──────────────────────────────────────────────────────────────────┐
│ RESULTS LAYER (results/)                                         │
│  results/YYYY-MM-DD_<task>_<model>.json + TEMPLATE_result_log.md │
│  Immutable. Append-only. This is our evidence and our CV.        │
└──────────────────────────────────────────────────────────────────┘
```

## The Connection Map (What Reads What, What Produces What)

This is the "no orphan files" guarantee. Every file must appear here.

| File | Reads | Produces | Consumed by |
|---|---|---|---|
| `data/passages.jsonl` | Human curation (Day 1) | Verified passages | `harness/eval_finetuned.py`, `app/app.py`, demo video |
| `scripts/gen-passages.py` | N-ATLAS-LLM | Draft passages (raw) | Human review → `data/passages.jsonl` |
| `harness/eval_finetuned.py` | `data/passages.jsonl` + 4 models | `results/*_finetune_eval.csv` | Leaderboard tab, README table |
| `harness/rubric.py` | Evaluator prompts | Scores 1–5 + safety flags | `harness/eval_finetuned.py` |
| `app/app.py` | `data/passages.jsonl` + N-ATLAS | Diagnostic result + hint | Gradio Tab 1, demo video |
| `app/app.py` (Tab 2) | `results/*.csv` | Rendered leaderboard | Gradio Tab 2, demo video |
| `scripts/where_am_i.py` | All checklists + results | Next-action report | You, every morning |
| `results/TEMPLATE_result_log.md` | — (template) | Filled run logs | You, after every eval run |

**Rule: if you create a file not in this table, either add it to the table or delete the file.**

## Data Flow — One Full Lap (Trace This)

1. Day 1: `gen_passages.py` prompts N-ATLAS → 20 raw passages → **human review**
   → corrections applied → `data/passages.jsonl` (labeled "Curriculum-aligned, human-verified").
2. Day 2: `run_eval.py` loads each passage, asks each of 3 models to generate a
   hint for a deliberately wrong answer → `rubric.py` scores relevance, simplicity,
   cultural relevance, safety (1–5) → `results/2026-10-08_hint_eval.json`.
3. Day 2: `diagnostics.py` compares silent-read score vs audio-assisted score →
   emits `DECODING_GAP` or `COMPREHENSION_GAP`.
4. Day 3: Gradio Tab 1 runs the full loop live (passage → audio → answer → hint →
   diagnostic). Tab 2 renders the results JSONs as the leaderboard.
5. Day 5: the demo video shows Tab 1, then Tab 2, then states compliance posture.
6. Day 6: everything deployed; results JSONs are the submission's evidence trail.

## Infrastructure Decision (Already Made — Do Not Re-litigate)

- **Development:** Google Colab free T4, 3B–8B models in 4-bit via bitsandbytes.
- **Demo hosting:** Hugging Face Spaces (free CPU; request GPU upgrade if needed).
- **No local GPU purchase. No local env rabbit holes.** Reproducible cloud
  pipelines + documented constraints is the remote-employer signal we want.
