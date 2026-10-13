# Evaluation Method and Limitations

This document distinguishes the intended qualitative review dimensions from
the automated measurements currently implemented in the repository. Do not
report the intended rubric as if the current evaluation script computed it.

## Intended qualitative review

When reviewing a hint for a learner, consider:

| Dimension | Review question |
|---|---|
| Relevance and grounding | Does the hint address the question and stay consistent with the passage without simply giving away the answer? |
| Simplicity | Is the language appropriate for the intended age group? |
| Cultural fit | Does the wording fit the passage and intended audience without stereotyping? |
| Safety and tone | Is the content age-appropriate, respectful, and encouraging? |

These dimensions can guide human review. The repository does not currently
include a complete LLM-as-judge workflow, a human-spot-check process, or an
automated safety-review queue.

## Automated holdout evaluation

`harness/eval_finetuned.py` reads 20 examples from `data/test_100.jsonl` and
generates an explanation for each of four model configurations. It records
responses and computes:

- `grounded`: whether the expected answer appears as a case-insensitive
  substring in the response.
- `refused`: whether the response contains one of a small set of refusal
  phrases.
- `words`: the whitespace-separated word count.

The saved CSV has 80 rows when all four model configurations complete
successfully. These checks do not prove factual correctness, quality, safety,
or robust refusal behavior. The test file is SQuAD-derived and is not a
Nigerian-curriculum validation set. Model generation is sampled, so results may
vary between runs.

`results/baseline_eval_results.csv` contains a separate earlier evaluation with
different columns and should not be combined with the holdout CSV as though the
methodology were identical.

## Application diagnostic

The app's demonstration rule lives in `app/diagnostics.py`:

- If listening score is at least `0.7` and reading score is below `0.7`, show a
  decoding-gap message.
- If both scores are below `0.7`, show a comprehension-gap message.
- Otherwise, show an on-track message.

The app receives these scores directly from sliders. They are not calculated
from quiz answers, and the rule has not been validated. This message is
illustrative only.

## Reporting guidance

When sharing results, identify the input data, number of examples per model,
model IDs and revisions when known, generation settings, metrics, and
limitations. Do not describe substring matching as a validated grounding score
or claim clinical, educational, or safety validation.
