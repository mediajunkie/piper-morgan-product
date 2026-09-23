# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. Rolling doc: rows get added when a fix needs PM's
live verification and struck when done. When PM asks "what do I test?", the answer is this
file. Each row: what to do, what PASS looks like, which surface to use.

✅ **Surface note UPDATED 09-23 14:3x (v0.8.14.0 cut)**: alpha.pipermorgan.ai is **served by
Fly**; at cut time it still runs **v0.8.13.0 + the five 09-21 closures** (sha 609a07b9, last
verified 09-22 — unverified this turn). **Rows 1–2 are live on alpha NOW.** **Rows 3–6 need the
v0.8.14.0 deploy first** — that's your keystroke via Pard's sheet (`fly deploy` from origin/main
at tag `v0.8.14.0`); until then they're on-deck, not testable. Deploy includes migration
`m1797drop` (drops five empty tables — rehearsed; nothing of yours lives there).

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

### 3. Honest 404-close (#1858) — ~30s — AFTER the v0.8.14.0 deploy
- **Do**: with GitHub connected, "close issue 99999 in mediajunkie/piper-morgan-product"
  (any number that doesn't exist).
- **PASS**: *"There's no issue #99999 in mediajunkie/piper-morgan-product — nothing was
  changed"* (or equivalent naming the repo). FAIL: the old *"may or may not have gone
  through"* hedge, or any claim it closed something.

### 4. Preferences persist (#1574) — ~2 min across a deploy — AFTER the v0.8.14.0 deploy
- **Do**: Settings → Preferences, set your timezone to America/Los_Angeles (or change any
  preference), dismiss the calendar-setup offer if it appears. Then do the deploy (or just
  come back after it).
- **PASS**: the preference is still set and the offer stays dismissed after the restart.
  FAIL: the "why does it keep asking me?" reset.

### 5. Your clock, labeled (#1576 family) — ~1 min — AFTER the v0.8.14.0 deploy
- **Do**: with the timezone set (row 4), ask *"what time is it for me?"* and *"what's my
  agenda today?"*. If you can, also try one turn after 5pm PT.
- **PASS**: every time carries your zone label ("2:41 PM PDT"), meetings show real times
  (never "TBD"), a "Focus Time Available" block appears, and "today" is your date after 5pm.
  FAIL: a bare clock face, a UTC face, "TBD", or tomorrow's date.

### 6. One-line add-project (#1856) — ~30s — AFTER the v0.8.14.0 deploy
- **Do**: `add project One Job with repo Design-in-Product/one-job` (the exact line from
  your 09-23 transcript).
- **PASS**: created + linked in ONE turn with a confirmation naming both. Then try
  `add project with repo Design-in-Product/one-job` (no name) → you get the exact line to
  type and a way to cancel, not the same canned question twice.
- ⚠️ If Piper instead *asks* "Want me to add it now?" and "yes" goes nowhere — that's #1855
  (design with Arch/CXO), not a row-6 failure; note the wording and move on.

## Struck rows
- ✅ **Row 1 STRUCK 2026-09-23** — #1617 tail-release retest PASSED (PM, live on the Fly-served
  alpha, ~9:37 AM: turn 2 reached the issue rail first try, crisp confirm, no swallow). #1739's
  last dependency discharged; epic 3 unblocked. Same run yielded 6 filed findings
  (#1855–#1860) + evidence comments on #1843/#1828 — none reopen #1617.
