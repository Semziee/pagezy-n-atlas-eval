# 05 — Licensing & Compliance Posture (Compliance Is a Feature)

## N-ATLAS / Awarri Research License — Our Obligations → Our Implementations

| Obligation | Where we implement it | Evidence |
|---|---|---|
| Max 1,000 active end-users (free tier) | Hard cap check in `app/app.py`; README statement; this doc | CP-4.2 |
| Non-commercial use only | Repo LICENSE = Apache-2.0 for OUR code, with explicit notice that N-ATLAS model usage is bound by its own research license | CP-4.2 |
| Display "Powered by Awarri" | Footer badge in both Gradio tabs | CP-4.1 |
| Attribution in docs | README + `docs/05` + video minute 3 | CP-4.2 |

## README Compliance Block (copy verbatim into README.md)
> "This prototype is architected to comply with the N-ATLAS Research License:
> capped at 1,000 concurrent end-users, non-commercial use, with full attribution
> to Awarri. 'Powered by Awarri' badge is displayed in the application footer.
> Student voice-input (ASR) is explicitly deferred to Phase 2."

## Badge Snippet (footer of both tabs)
```python
gr.Markdown(
    "<div style='text-align:center;opacity:0.7;font-size:0.85em'>"
    "Powered by Awarri · N-ATLAS Research License · ≤1,000 users · Non-commercial"
    "</div>")
```

## Data & Content Rights
- Our passages are model-generated then human-verified → original content; license under Apache-2.0 with our copyright header.
- Pre-recorded MP3s: record them yourself or use explicitly licensed TTS. Never scrape audiobooks.
- Child data: **V1 collects zero child personal data.** No names, no accounts, no audio upload. State this everywhere — it is a selling point.

## What We Will NOT Do (write these down so future-you doesn't slip)
- No user accounts, no analytics, no cookies → keeps us under the cap and out of data-protection scope.
- No fine-tuning of N-ATLAS weights during the competition (license scope) — Phase 2 proposal only.
- No claims of "deployed in schools" — it is a prototype, say prototype.
