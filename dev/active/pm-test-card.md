# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. Rolling doc: rows get added when a fix needs PM's
live verification and struck when done. When PM asks "what do I test?", the answer is this
file. Each row: what to do, what PASS looks like, which surface to use.

✅ **Surface note UPDATED 09-20**: alpha.pipermorgan.ai now runs **v0.8.12.0** (deployed
and verified 09-20) — **ALPHA is the preferred test surface**, matching PM's real-project
dogfooding decision. LOCAL remains available for pre-deploy work.

## Open rows

### 1. Standup tail-release retest (#1617 fix → gates #1739 → gates all of epic 3) — ~90s
- **Surface**: **ALPHA** (v0.8.12.0 carries the #1617 fix as of 09-20) — or LOCAL.
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
- **Status 09-20**: ATTEMPTED on alpha; the flow broke UPSTREAM of the tail (interview
  never delivered, generic template fabricated, edit confabulated — #1836/#1837/#1838
  filed from PM's transcript). Row stays OPEN; #1837's fix is the practical prerequisite
  before the tail is even reachable.

### 2. PARKED (was: OpenAI-only Slack turn, #1822) — not PM-cheap after all
- PM correctly flagged (09-19): this needs an account configured with ONLY an OpenAI key —
  setup walk-through included, it's well over the advertised 2 minutes. Parked until a
  natural openai-only account exists (a real tester) or Lead provisions a test account
  once the hosting/test-account question is ruled (it's inside Pard's weekend proposal
  scope). Not PM's to set up.

## Struck rows
*(none yet)*

| #1824 invalid-key honesty | ALPHA (after next cut) | Store a deliberately-invalid Anthropic key in Settings, send a chat message | Expect: "The language-model API key on your account isn't valid. Check or replace it under Settings → LLM API Keys." — NOT "Something unexpected happened" | shipped 09-21 (`9ec028406`), awaiting next deploy |
