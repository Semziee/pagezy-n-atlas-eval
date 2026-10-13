# 10 — Submission Checklist (run top-to-bottom on Oct 12)

- [ ] Repo public, named `pagezy-n-atlas-eval`, README renders (check images/paths)
- [ ] `data/passages.jsonl` — all lines human-verified (reviewed_by + review_date present)
- [ ] `results/` contains: registration.png, ≥1 eval JSON with n≥10/model, safety_flags.md (even if empty), demo screenshot
- [ ] Video ≤3:00, all 3 beats present, file accessible via durable link
- [ ] Space public, smoke-tested in incognito
- [ ] Badge visible; compliance block in README; Safety & Limitations section present
- [ ] Fence verified: `git ls-files | grep -E "secrets|\.env|passages_full|prompts/final"` returns nothing
- [ ] Submit → screenshot to `results/submission.png`
- [ ] Write `results/retrospective.md` (20 min)
