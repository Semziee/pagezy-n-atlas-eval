# Data directory

- `passages.jsonl` contains the 20 passage records loaded by the Gradio app.
  Records have varying `human_verified` values; inspect each record before
  reuse.
- `train_400.jsonl` and `test_100.jsonl` are SQuAD-derived files used by the
  QLoRA and evaluation scripts. `scripts/prepare-dataset.py` regenerates and
  overwrites them.
- `draft_passages.jsonl` is generated locally by `scripts/gen-passages.py` and
  is not part of the checked-in corpus by default.
- `passages_full.jsonl` is intentionally excluded from the public repository.

See [`docs/03_data_schema.md`](../docs/03_data_schema.md) for fields, sources,
and handling notes. Check the terms of third-party datasets before
redistributing or using these records.
