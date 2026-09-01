# Comms carry-forward

*Rewritten at the 2026-09-01 09:48 PT WORK fire. Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`ffbba712`, expression `12 6,9,12,15,18,21 * * *`, confirmed single active job — no rotation needed.

## Closed today

- **Beat 4 ("A Sender-Impersonation Bug, Four Days Before Beta") — published + Medium-syndicated.** Full editorial review caught a real fact error (footer misnamed a confirmer — Exec should have been Arch, verified via subagent), the recurring heading-level defect, and applied PM's new "agents not people" flag.
- **New permanent check shipped**: `template-audit` v1.11, check #11 (agents referred to as "people") — with worked PASS/FAIL examples since roughly half of any match is legitimate. Checks 12-16 renumbered.
- **The full narrative-front gap closed, Aug 8 → Aug 31.** PM corrected a real sequencing mistake mid-task (I'd ranked candidate beats by story-readiness instead of presenting them chronologically — a repeat of a mistake already named once in memory) and asked for it to be fixed somewhere more durable than memory. Fixed in `.claude/skills/continue-narrative/SKILL.md` v1.1, with the specific failure documented so a future instance recognizes the trigger. Also caught and fixed an under-sampling in the survey (Aug 21-26 read as quiet; a re-check found real material in 4 of 6 days). **All 7 beats drafted, fact-checked against primary sources via dedicated subagent research per beat, mechanically clean, and calendared**, front to back:
  - Beat 7 "The Mailbox Trust Violation" (Aug 9) — Sep 10
  - Beat 8 "The Bug That Was Misdiagnosed Twice" (Aug 19-20) — Sep 15
  - Beat 9 "The Week the Checks Started Checking Themselves" (Aug 21-24) — Sep 17
  - Beat 10 "The Near-Miss and the Missing Key" (Aug 25) — Sep 22
  - Beat 11 "The Alarm That Had Been Working All Along" (Aug 26) — Sep 24 (retitled after research disproved the survey's working title)
  - Beat 12 "Three Seats Stay Dark Longer" (Aug 27-29) — Sep 29
  - Beat 13 "What Piper Morgan Actually Is, Ratified Then Corrected Twice" (Aug 29-31) — Oct 1 (ESSENCE A-plot per PM's ruling, #1659 saga as B-plot)
  Footer chain verified clean end to end. All 7 need PM's voice-pass + art before their pubDates — none of that has happened yet, this was drafting only.
- **Dispatch-PM's syndication retrospective — closed.** Thorough, honest tracing of the earlier "Drained on Paper" miss to its structural cause. Replied via the Exec-broker protocol: aligned on their 3 proposals (publish-notice is Docs' to implement, `status` definition already open with Docs, platform-check discipline already in practice), noted a genuine same-day coincidence (they independently hit the same "agents not people" pattern I'd just built a check for).
- **Owned a guessed timestamp** in my own session log (wrote "~9:00 AM–2:00 PM" without checking `date`; actual span was under an hour) — caught and corrected same-fire, per `feedback_verify_timestamps_never_guess`.

## Open items — no Comms-side move available right now

- **7 fresh narrative beats** — all await PM's voice-pass + art (Sep 10 through Oct 1 slots).
- **ChicagoCamps talk** — PM reviewing script/slides this week; script + slide plan at `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`.
- **BYOC marketplace narrative** — re-surfaced to PM 08-31 (pick A/B/C or deprioritize), still awaiting response.
- **Ship #058** — Tuesday timing conflict with Beat 4 was resolved in Beat 4's favor (Beat 4 published this morning); Ship #058's own voice-pass/review status unconfirmed, watch for it.
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification (MCP stays in Production).

## Waiting on others

- **PM** — voice-pass + art on 7 new beats; ChicagoCamps script/slide review; BYOC marketplace narrative pick.
- **Dispatch-PM** — nothing currently owed; thread closed this fire.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
