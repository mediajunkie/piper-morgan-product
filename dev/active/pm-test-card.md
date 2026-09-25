# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. Rolling doc: rows get added when a fix needs PM's
live verification and struck when done. When PM asks "what do I test?", the answer is this
file. Each row: what to do, what PASS looks like, which surface to use.

✅ **Surface note UPDATED 09-25 17:0x — alpha is on Fly v139 (`43e12de2d2`)**:
v0.8.14.0 plus everything of 09-24 and 09-25 — signup wizard (#1875), caching (#1859), timezone
surface (#1876) + one resolver (#1887), honest degrade copy (#1772), render-whole calendar blocks
(#1880), AND the inversion's write path: **`create_reminder` now routes through the constrained
router (PM flipped the flag 16:4x)**. **Ten rows testable; row 10 is the newest and ~30 s.**

## Open rows

### 10. Reminder with time+day routes through the inversion (#1559) — ~30 s — NEW 09-25
- **Why**: this exact phrasing was PM's 08-08 verbatim that the reminder pattern missed
  (turn 1 executed the wrong thing, turn 2 failed). `create_reminder` is now on the inversion's
  named-write allowlist and in the live flag; in the shadow score the phrase routed
  `create_reminder` at confidence 1.0.
- **Surface**: **ALPHA**, web chat, any account with a stored key.
- **Do**: send exactly `remind me at 3pm tomorrow to review the PR`.
- **PASS**: one reply that confirms a reminder for **tomorrow 3pm in your timezone** with the
  task "review the PR" (a confirm prompt first is fine — it's a WRITE). Then `what reminders do
  I have?` lists it with that time. FAIL: a project/issue/portfolio reply, "I couldn't work out
  the time", or a reminder at the wrong time.
- **Closes**: #1559 on a pass (paste the transcript on the issue or here).

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

### 3. Honest 404-close (#1858) — ~30s — LIVE
- **Do**: with GitHub connected, "close issue 99999 in mediajunkie/piper-morgan-product"
  (any number that doesn't exist).
- **PASS**: *"There's no issue #99999 in mediajunkie/piper-morgan-product — nothing was
  changed"* (or equivalent naming the repo). FAIL: the old *"may or may not have gone
  through"* hedge, or any claim it closed something.

### 4. Set your timezone + it persists (#1876 + #1574) — ~2 min — LIVE (v125)
- **Do**: Settings → **Preferences** (new card). You should see the nudge "Your browser says
  you're in America/Los_Angeles. Use that?" only if the stored zone differs from your browser's
  — for you they match, so pick any other zone from the select, save, then set it back. Also try
  in chat: `set my timezone to Helsinki` then `set my timezone to Los Angeles`.
- **PASS**: toast confirms; `what time is it for me?` renders in the chosen zone with its label
  ("10:41 PM EEST"); after a page reload (and the next deploy) the choice is still set. `set my
  timezone to Paris` → Europe/Paris; `set my timezone to Springfield` → an honest ask, no guess.
  **New step (#1887, v129+)**: with Helsinki set, `remind me tomorrow at 9am` — the saved reminder
  reads 9:00 AM Helsinki, not 9:00 AM in the browser's zone (due dates and clock faces now share
  one resolver). FAIL: a silent adoption of the browser zone, a reset after reload, a guessed zone,
  or a reminder interpreted in a different zone than the clock face shows.

### 5. Your clock, labeled (#1576 family) — ~1 min — LIVE
- **Do**: `what time is it for me?` and `what's my agenda today?`. While you're still on the
  default zone the time reply now SAYS so and points at Settings → Preferences.
- **PASS**: every time carries a zone label, meetings show real times (never "TBD"), a "Focus
  Time Available" block appears. FAIL: a bare or UTC face, or "TBD".

### 6. One-line add-project (#1856) — ~30s — LIVE
- **Do**: `add project One Job with repo Design-in-Product/one-job` (the exact line from
  your 09-23 transcript).
- **PASS**: created + linked in ONE turn with a confirmation naming both. Then try
  `add project with repo Design-in-Product/one-job` (no name) → you get the exact line to
  type and a way to cancel, not the same canned question twice.
- ✨ **Changed since yesterday (#1855 layer 2, live in this build)**: if Piper *asks*
  "Want me to add project One Job with repo Design-in-Product/one-job? Say yes, or tell me
  otherwise." then "yes" should DO it (the handler's own confirmation). If the question is worded
  any other way, or "yes" goes nowhere, that's a real finding — quote the exact sentence.

### 7. The chat you start before adding a key survives the trip to Settings (#1838) — ~2 min — LIVE (v127)
- **Do** (needs a keyless state — do it with a fresh test account, or temporarily remove your
  keys): type any message → get the "add your key" reply → Settings → LLM API Keys → add a
  key → come back to chat (the brand link or the rail).
- **PASS**: the thread you started is there — your message AND Piper's key ask — and its rail
  row has a real title, not "New conversation". Fail: an empty window, or the thread gone.
  This was your 09-20 "had to start over" report.

### 8. The composer grows instead of ticker-taping (#1737) — ~30s — LIVE (v127)
- **Do**: paste or type three or four sentences into the chat box. Then Shift+Enter, then Enter.
- **PASS**: the box grows line by line up to about six rows, then scrolls inside itself; text
  never runs off the right edge; Shift+Enter makes a new line; Enter sends. Works the same in
  the rail widget on other pages.

### 9. An old thread doesn't claim it's now (#1498) — ~30s — LIVE (v127)
- **Do**: open any conversation from a previous day (rail or history).
- **PASS**: the header reads "Conversation from <that day> at <that time>" in your zone — not
  "Good evening, <name> · <today>". Then "+ New chat": the greeting comes back, since a blank
  chat is the one place "now" is true. (The stale "calendar isn't connected yet" line inside an
  old reply is a separate item, not this row.)

## Struck rows
- ✅ **Row 1 STRUCK 2026-09-23** — #1617 tail-release retest PASSED (PM, live on the Fly-served
  alpha, ~9:37 AM: turn 2 reached the issue rail first try, crisp confirm, no swallow). #1739's
  last dependency discharged; epic 3 unblocked. Same run yielded 6 filed findings
  (#1855–#1860) + evidence comments on #1843/#1828 — none reopen #1617.
