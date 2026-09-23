# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. Rolling doc: rows get added when a fix needs PM's
live verification and struck when done. When PM asks "what do I test?", the answer is this
file. Each row: what to do, what PASS looks like, which surface to use.

✅ **Surface note UPDATED 09-22 (post-cutover)**: alpha.pipermorgan.ai is now **served by Fly**,
running **v0.8.13.0 + the five 09-21 post-release closures** (sha 609a07b9 = origin/main).
**Both open rows are live on ALPHA right now** — the cutover deploy carried everything.
You'll need a fresh login (sessions didn't migrate, by design).

## Open rows

### 1. Invalid-key honesty retest (#1824) — ~60s — THE ONE REMAINING QUICK ROW
- **Surface**: **ALPHA** — LIVE NOW (shipped 09-21 `9ec028406`, deployed in the cutover).
- **Do**: in Settings → LLM API Keys, store a deliberately-invalid Anthropic key on your
  account, then send any chat message.
- **PASS**: the reply says the key on YOUR account isn't valid and points at Settings →
  LLM API Keys — a specific, honest sentence. FAIL: "Something unexpected happened" (the
  exact live symptom this fixed) or any generic error.
- **Cleanup**: restore your real key after.

### 2. PARKED (was: OpenAI-only Slack turn, #1822) — not PM-cheap after all
- Needs an account configured with ONLY an OpenAI key — over the advertised 2 minutes to
  set up; not PM's to set up. Revisit when a natural openai-only tester exists or the
  test-account policy (pipeline plan §4d) produces one.

## Struck rows
- ✅ **Row 1 STRUCK 2026-09-23** — #1617 tail-release retest PASSED (PM, live on the Fly-served
  alpha, ~9:37 AM: turn 2 reached the issue rail first try, crisp confirm, no swallow). #1739's
  last dependency discharged; epic 3 unblocked. Same run yielded 6 filed findings
  (#1855–#1860) + evidence comments on #1843/#1828 — none reopen #1617.
