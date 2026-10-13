# Optional Demo Walkthrough

Use this outline to record a short walkthrough of the current prototype. Show
the application as it behaves; do not imply that its diagnostic is validated
or that the audio and learner workflows are more complete than they are.

## 1. Problem and scope

- Introduce the read-versus-listen idea: difficulty decoding text can call for
  different support from difficulty understanding a passage.
- State that Pagezy is a prototype, and its sliders are manually entered
  illustrative scores.

## 2. Learner-facing demo

- Open **Learn with Pagezy** and select a passage.
- Read the passage and answer its multiple-choice question.
- Change the reading and listening sliders and submit the answer.
- Explain that the diagnostic message is a simple threshold heuristic, not a
  learner assessment. The current interface does not play the included MP3s.

## 3. Model Arena

- Select a passage and run the four-model comparison.
- Show the returned hints and the word-count, substring-grounding, and
  elapsed-time fields.
- Explain that results are generated on demand, need GPU hardware, and use
  simple automated checks rather than a complete safety or quality evaluation.

## 4. Close

- Point viewers to the repository README and deployment runbook.
- Mention that model access and license terms vary by model, and that the app
  has no active-user-cap enforcement.
