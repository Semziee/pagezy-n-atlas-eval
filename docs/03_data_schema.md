# 03 — Data Layer Specification

## The Golden Dataset Rule
`data/passages.jsonl` is **append-only and human-verified**. Model output never
enters this file without a human review pass. The label "Curriculum-aligned,
human-verified" is our credibility — protect it.

## JSONL Schema (one passage per line)

```json
{
  "id": "eng-001",
  "language": "english | yoruba | pidgin",
  "curriculum_tag": "Nigeria-Primary-3-English | ...",
  "source": "model-generated + human-verified",
  "grade_level": 3,
  "text": "The passage text, 60–120 words for Primary 3.",
  "questions": [
    {
      "qid": "eng-001-q1",
      "question": "…",
      "options": ["A", "B", "C", "D"],
      "answer": "B",
      "skill": "literal | inferential | vocabulary"
    }
  ],
  "diagnostic_type": "read_vs_listen",
  "tts_audio_path": "assets/audio/eng-001.mp3",
  "reviewed_by": "<your name>",
  "review_date": "2026-10-07",
  "review_notes": "Fixed option C; simplified sentence 2."
}
```

## Field Rules
- `id`: `<lang>-<NNN>` — never reuse an ID, even if a passage is deleted (deletion = mark `deprecated: true`, never remove the line).
- `options`: always 4 options; exactly one correct.
- `tts_audio_path`: null is allowed at Day 1 for Yoruba/Pidgin if TTS unavailable — but ≥2 MP3s must exist by CP-3.3.
- Every line must have `reviewed_by` + `review_date`. Missing = not verified = cannot be used in the demo.

## Target Volumes
| Milestone | Passages | Mix |
|---|---|---|
| Day 1 (CP-1.5) | 20 verified | 10 English, 10 Yoruba or Pidgin |
| Day 3 (nice-to-have) | 40 | + science/social studies |
| Stretch | 60 | only if Gates 1–3 are green |

## Generation Prompt (Day 1, `scripts/gen_passages.py`)
System: "You are a Nigerian primary-school curriculum expert. Generate reading
comprehension passages aligned with the Nigerian curriculum. Language, grade,
topic, and difficulty are given per call."
User: "Generate 1 passage for Grade 3, language = {lang}, topic = {topic from
list: market day, rainy season, family, football, farming}. 60–120 words, then
exactly 3 questions with 4 options each, one correct. Output strict JSON matching
the schema in docs/03_data_schema.md."
**Why one passage per call:** failure isolation. A malformed call wastes one
prompt, not ten.

## Human Review Checklist (apply to every line, Day 1)
- [ ] Age-appropriate vocabulary for the stated grade
- [ ] Cultural context is Nigerian, not generic/Western
- [ ] Exactly one correct option per question; options are plausible
- [ ] At least one inferential question per passage (literal-only is too easy)
- [ ] Yoruba/Pidgin: idioms correct — flag anything that "sounds translated"
- [ ] JSON valid; all schema fields present
