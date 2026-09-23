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
- ⚠️ **Key isolation (added 09-23, matters if you hold BOTH provider keys)**: run the test with
  the invalid Anthropic key as your ONLY stored key (temporarily remove the OpenAI one). The
  #1823 any-spendable-provider gate means a valid second key may legitimately serve the request
  and the error path under test never fires — a pass-by-masking, not a pass. Restore both after.
- **Surface**: **ALPHA** — LIVE NOW (shipped 09-21 `9ec028406`, deployed in the cutover).
- **Do**: in Settings → LLM API Keys, store a deliberately-invalid Anthropic key on your
  account, then send any chat message.
- **PASS**: the reply says the key on YOUR account isn't valid and points at Settings →
  LLM API Keys — a specific, honest sentence. FAIL: "Something unexpected happened" (the
  exact live symptom this fixed) or any generic error.
- **Cleanup**: restore your real key after.

### 2. OpenAI-only Slack turn (#1822) — UNPARKED 09-23, conditional on Slack being linked
- **A DIFFERENT test from row 1** (the two got blurred in chat 09-23, hence this spelling-out):
  row 1 tests an ERROR MESSAGE on the web surface with a BROKEN key; this row tests a SUCCESS
  path on the SLACK surface with a VALID key — that a Slack turn is answered spending the
  sender's own OpenAI key (the #1822 fix).
- **Do** (only if your Slack is already linked to your alpha account): make your VALID OpenAI
  key the only stored key (no Anthropic), then send Piper any message via Slack.
- **PASS**: a normal, working reply (your OpenAI key did the work). FAIL: a keyless wall or
  generic error.
- **Sequencing tip**: pairs with row 1 in one sitting — row 1's state (only fake-Anthropic) →
  this row's state (only real-OpenAI) → restore. Was parked as "not PM-cheap" when it implied
  provisioning a separate account; PM holding a real OpenAI key changes that.

## Struck rows
- ✅ **Row 1 STRUCK 2026-09-23** — #1617 tail-release retest PASSED (PM, live on the Fly-served
  alpha, ~9:37 AM: turn 2 reached the issue rail first try, crisp confirm, no swallow). #1739's
  last dependency discharged; epic 3 unblocked. Same run yielded 6 filed findings
  (#1855–#1860) + evidence comments on #1843/#1828 — none reopen #1617.
