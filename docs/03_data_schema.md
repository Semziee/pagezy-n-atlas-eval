# Data Formats

This document describes the data formats currently used by the app and
workflows. The passage corpus and the SQuAD-derived training/evaluation files
have related but not identical provenance and should not be treated as one
curated dataset.

## App passage corpus

`data/passages.jsonl` contains one JSON object per line. Current records use
fields similar to:

```json
{
  "id": "narrative-01",
  "age_group": "8-12",
  "language": "english",
  "read_text": "Passage text...",
  "audio_script": "Passage text for an audio workflow...",
  "quiz": [
    {
      "question": "What is the moral of the story?",
      "options": ["Perseverance", "Speed", "Laziness", "Haste"],
      "correct": "Perseverance",
      "explanation": "The explanation shown after a correct answer."
    }
  ],
  "diagnostic_focus": "comprehension",
  "human_verified": false
}
```

The app reads `id`, `read_text`, and the first item in `quiz` (including
`question`, `options`, `correct`, and `explanation`). The other fields are
descriptive or intended for future use. The current app does not use
`audio_script` to play audio.

The checked-in corpus has 20 records in English, Pidgin, and Yoruba. Records
have different `human_verified` values; inspect each record before reuse. Do
not describe all records as human-reviewed or curriculum-validated.

## Generated passage drafts

`scripts/gen-passages.py --lang <english|pidgin|yoruba>` generates drafts and
appends them to `data/draft_passages.jsonl`. Generated records are marked
`human_verified: false`. The script does not validate the content, check schema
completeness, or perform human review. Review the content and provenance before
adopting it in the demo corpus.

## Training and holdout files

`scripts/prepare-dataset.py` samples 500 records from the
`rajpurkar/squad` dataset, then writes 400 records to
`data/train_400.jsonl` and 100 to `data/test_100.jsonl`. Each output record
contains:

- `id`, `age_group`, `language`, and `read_text`
- `quiz`: a one-item list with `question`, `options`, `correct`, and
  `explanation`
- `human_verified`, set by the script based on the original SQuAD source

The script's options contain the answer plus placeholder distractors. This is
not a validated multiple-choice assessment dataset. Running the script
overwrites the checked-in train and holdout files.

## Evaluation output

`harness/eval_finetuned.py` reads the first 20 rows from
`data/test_100.jsonl` and writes one row per model and example to
`results/2026-10-12_finetune_eval.csv`. Columns include `model`, `item_id`,
`response`, `grounded`, `refused`, and `words`. `grounded` is a literal
substring match to the expected answer; `refused` uses a list of phrase
matches. These are simple heuristics, not human judgments or comprehensive
safety/factuality measures.

## Handling guidance

- Keep generated drafts separate from reviewed material.
- Preserve the origin and license terms for third-party data.
- Check the `human_verified` field and source before using a passage with
  learners.
- Back up result files before rerunning scripts that overwrite them.
