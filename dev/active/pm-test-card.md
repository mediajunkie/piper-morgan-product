# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. Rolling doc: rows get added when a fix needs PM's
live verification and struck when done. When PM asks "what do I test?", the answer is this
file. Each row: what to do, what PASS looks like, which surface to use.

⚠️ **Surface note until the droplet upgrade lands**: alpha.pipermorgan.ai runs a July-era
cut — NOTHING from the last two months can be verified there. Rows below say `LOCAL` (the
fresh dev server on `http://localhost:8001`, current code as of 09-19 15:55) until alpha is
upgraded, after which real-data testing on alpha becomes the norm (matches PM's 09-19
decision to rely on Piper for one real project).

## Open rows

### 1. Standup tail-release retest (#1617 fix → gates #1739 → gates all of epic 3) — ~90s
- **Surface**: LOCAL (the fix is not on alpha).
- **Do**: run a standup to completion — through the final summary and its "Anything else?"
  tail. Then send, in order, your exact three turns from the 08-13 transcript:
  1. `do things directly from now on`
  2. `change the status of issue #99999 to Done` — deliberately nonexistent: the PASS
     criterion is ROUTING (the command reaching the issue rail), not the mutation
     succeeding, so an honest "issue not found" from the rail is a PASS and nothing real
     gets mutated. (#108 is CLOSED already — checked 09-19 — and needn't be touched.)
  3. the same command again if turn 2 misbehaved.
- **PASS**: turn 2 reaches the issue rail on the FIRST try — no re-rendered standup
  summary, no "Your standup is ready! Have a great day!" swallowing the command. The
  completed flow releases its claim; off-tail turns process as normal intents.
- **On PASS**: say so — it discharges #1739's last dependency and unlocks epic 3's floor.
  On FAIL: paste the transcript; that reopens #1617 with fresh evidence.

### 2. PARKED (was: OpenAI-only Slack turn, #1822) — not PM-cheap after all
- PM correctly flagged (09-19): this needs an account configured with ONLY an OpenAI key —
  setup walk-through included, it's well over the advertised 2 minutes. Parked until a
  natural openai-only account exists (a real tester) or Lead provisions a test account
  once the hosting/test-account question is ruled (it's inside Pard's weekend proposal
  scope). Not PM's to set up.

## Struck rows
*(none yet)*
