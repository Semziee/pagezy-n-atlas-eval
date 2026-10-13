# Project Content and Third-Party Components

This repository includes application code, prompts, datasets, model references,
and sample audio. Their terms and provenance are not necessarily the same.

## Repository contents

- Repository code is offered under the terms in [`LICENSE`](../LICENSE).
- Prompt files under `prompts/` are included in this public repository.
- Demo passages and SQuAD-derived files are checked into `data/`; review
  provenance and applicable source terms before redistributing or using them.
- MP3 files are provided in `assets/audio/`; review their source and terms
  before reuse.
- Model weights are downloaded separately. Their terms are set by the
  respective model publishers and do not become Apache-2.0 licensed by being
  referenced here.

## Secrets and private data

Do not commit access tokens, private learner data, or restricted model files.
The root `.gitignore` excludes common secret locations and selected private
artifact paths. An ignore rule is not a substitute for checking what is
actually staged:

```powershell
git status --short
git ls-files
```

Set Hugging Face access tokens through the local Hugging Face CLI login or a
Space secret. Never place credentials in source files, notebooks, prompts, or
tracked configuration.

## Provenance and verification

Inspect each passage's `human_verified` field and source before describing it as
reviewed. Keep generated drafts separate from content approved for learner use.
Record the model, data source, and review process for any new dataset or
evaluation result added to the repository.

See [licensing notes](05_licensing_and_compliance.md) and the
[data formats](03_data_schema.md) for additional handling guidance.
