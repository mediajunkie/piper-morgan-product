# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. Rolling doc: rows get added when a fix needs PM's
live verification and struck when done. When PM asks "what do I test?", the answer is this
file. Each row: what to do, what PASS looks like, which surface to use.

✅ **Surface note UPDATED 09-22 (post-cutover)**: alpha.pipermorgan.ai is now **served by Fly**,
running **v0.8.13.0 + the five 09-21 post-release closures** (sha 609a07b9 = origin/main).
**Both open rows are live on ALPHA right now** — the cutover deploy carried everything.
You'll need a fresh login (sessions didn't migrate, by design).

## Open rows

### 1. Standup tail-release retest (#1617 fix → gates #1739 → gates all of epic 3) — ~90s
- **Surface**: **ALPHA** — now READY: the #1836/#1837 upstream fixes that blocked the 09-20
  attempt shipped in v0.8.13.0 and are live post-cutover; the tail is reachable again.
- **Do**: run a standup to completion — through the final summary and its "Anything else?"
  tail. Then send, in order, your exact three turns from the 08-13 transcript:
  1. `do things directly from now on`
  2. `change the status of issue #99999 to Done` — deliberately nonexistent: the PASS
     criterion is ROUTING (the command reaching the issue rail), not the mutation
     succeeding, so an honest "issue not found" from the rail is a PASS and nothing real
     gets mutated.
  3. the same command again if turn 2 misbehaved.
- **PASS**: turn 2 reaches the issue rail on the FIRST try — no re-rendered standup
  summary, no "Your standup is ready! Have a great day!" swallowing the command. The
  completed flow releases its claim; off-tail turns process as normal intents.
- **On PASS**: say so — it discharges #1739's last dependency and unlocks epic 3's floor.
  On FAIL: paste the transcript; that reopens #1617 with fresh evidence.
- **History**: 09-20 attempt broke UPSTREAM of the tail (#1836/#1837/#1838 filed from PM's
  transcript); those fixes are now the code you're testing.

### 2. Invalid-key honesty retest (#1824) — ~60s
- **Surface**: **ALPHA** — LIVE NOW (shipped 09-21 `9ec028406`, deployed in the cutover).
- **Do**: in Settings → LLM API Keys, store a deliberately-invalid Anthropic key on your
  account, then send any chat message.
- **PASS**: the reply says the key on YOUR account isn't valid and points at Settings →
  LLM API Keys — a specific, honest sentence. FAIL: "Something unexpected happened" (the
  exact live symptom this fixed) or any generic error.
- **Cleanup**: restore your real key after.

### 3. PARKED (was: OpenAI-only Slack turn, #1822) — not PM-cheap after all
- Needs an account configured with ONLY an OpenAI key — over the advertised 2 minutes to
  set up; not PM's to set up. Revisit when a natural openai-only tester exists or the
  test-account policy (pipeline plan §4d) produces one.

## Struck rows
*(none yet — rows 1 and 2 strike on your say-so)*
