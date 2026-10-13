# Safety and Limitations

Pagezy is a research and demonstration prototype, not a validated educational
assessment, clinical tool, or production service.

## Current limitations

1. **Scores are manual.** The app asks the user to set reading and listening
   scores. It does not measure a learner's reading, listening, or comprehension
   performance.
2. **No speech input or audio playback in the app UI.** There is no child-speech
   recognition or audio upload workflow. Sample MP3 files are present in the
   repository, but the current interface does not play them.
3. **Heuristic diagnostic.** `app/diagnostics.py` applies fixed score thresholds
   and returns a short message. It has not been validated against teachers,
   learners, or a clinical assessment.
4. **Limited feedback.** The learner tab shows a fixed hint for incorrect
   answers. Model-generated hints are available only in the separate Model
   Arena.
5. **Model output can be wrong or unsafe.** The Arena's grounding indicator is
   a substring match and does not establish factuality or safety. The app does
   not block or automatically review unsafe generated text.
6. **Small, mixed-verification corpus.** The app's 20 passages are a demo set;
   records have different `human_verified` values. The set is not comprehensive
   curriculum coverage.
7. **Deployment limits are not enforced by the app.** The UI displays N-ATLAS
   attribution and license text, but does not implement a 1,000-user cap.
   Confirm current model terms and deployment requirements independently.

## Safer use

- Do not use the diagnostic to label, rank, place, or make high-impact
  decisions about a learner.
- Treat generated text as unreviewed until a qualified person has checked it.
- Do not enter personal or sensitive learner information. The app has no
  account system, but the hosting platform and its logs have separate behavior
  that should be reviewed before public deployment.
- Check the `human_verified` field and provenance of every passage before
  presenting it as reviewed educational material.
- Obtain appropriate consent and governance review before any future collection
  or use of child data.

See [licensing notes](05_licensing_and_compliance.md) for model, data, and
deployment considerations.
