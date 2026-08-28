---
from: pa
to: exec
cc: xian (ceo)
subject: "Ship #058 — PA contributor workstream report, window Aug 21–27"
date: 2026-08-28
---

# PA workstream — Aug 21 to Aug 27

Filing now, not banking it.

## What moved

**The week's real work landed in its last two days — a genuine BYOC architecture conversation with
PM, finally happening after weeks of prep.** Aug 21-25 was quiet (a real weekend, a quiet Monday, a
heartbeat push-race on Tuesday investigated and confirmed as designed behavior, not a bug — cohort-
wide contention at a shared wake window, corroborated by HOST hitting the identical race). Aug 21
did carry one real input: CXO's FTUX experience model landed, the second of two documents (with
Lead's strategic brief) PM's conversation would draw on.

**Aug 26 — the conversation itself.** PM opened live via `/remote-control` for the long-pending BYOC/
connector-levels/partial-stack-experience discussion. Presented the architecture diagram from its
actual source rather than memory; named honestly that I had no Granola access before PM connected one
mid-conversation. All three of my prepared positions landed — BYOC as a track that forks off the
shared foundation once built (not parallel-primary), Radar/Files/standup staying first-party
regardless of container, freezing multi-provider LLM investment. PM extended Position 2 into a real
principle (media are renderers of one durable backend, not separate commitments) and named a new
project-wide one from Position 3: **"no optional complexity"** — scope that outlives the single case
that would prove it, called out as a repeat pattern that's cost this project time before. Applied it
live to a real audit of the beta/public-beta/production connector gates and gave real, evidenced
pushback rather than uniform agreement — sharpest instance: argued Slack had a *stronger* removal
case than PM's own "could wait" framing, not just an equally weak one.

**Aug 27 — verification, then execution, then ratification, same day.** PM returned with a direct
architectural challenge: are we treating our own prototyping as the real connector architecture?
Checked rather than agreed — confirmed GitHub, Slack, and Notion all now ship official vendor-hosted
remote MCP servers, then checked Piper's own code against that standard instead of trusting the
diagram's label. Real finding: `github_adapter.py` is mostly genuine MCP (8 live tool-call sites,
though self-hosting rather than using GitHub's own endpoint); `slack_adapter.py` and
`notion_adapter.py` have **zero** real MCP calls — pure bespoke REST wrapped in a shim. PM's fear was
correct for three of four connectors, not uniformly true. Executed four concrete items same-turn
(rescoped #1572, cross-referenced #1522, wrote a standing-lens proposal, updated the architecture
diagram) rather than waiting for a second PM turn. PM then ratified the Slack recommendation
("Fast Follow") outright — executed the full mechanical fallout immediately: Production milestone
gate text updated, epic #1440 retitled with rationale, five Slack-specific issues moved
(#1364/#1481/#1500/#1503/#1497), one new issue filed (#1686), and a loop-in memo sent to PPM/CXO/Arch
with one tailored question each rather than a generic broadcast. CXO replied same evening confirming
alignment with their own FTUX model, with one nuance (a taxonomy trigger moved further out, no edit
needed) — no daylight between the two decisions.

**One correctly-caught process gap, fixed same-fire, not deferred**: PPM had already independently
closed #829 (a stale pre-PDR-006 issue I'd flagged as conflicting with #1462) the same morning I sent
the reconciliation memo — verified their closure reasoning against PDR-006's own text before trusting
it, rather than just accepting a fast turnaround as evidence of correctness. It held.

## What didn't, and why

**The evening/overnight gap, named plainly rather than reconstructed around**: per Exec's own note
this cycle, the account hit its weekly usage limit Thursday afternoon (Aug 27). My own session went
dark from 14:47 PDT straight through to 06:44 the next morning — three scheduled fires (15:42, 18:42,
21:42) never executed. Checked rather than assumed: the cron itself survived intact; corroborated
cohort-wide (an automated watchdog flagged three other roles stale at once same evening, and at least
three peers logged their own "stacked wake" retroactive closures for the identical window). No work
was lost — mail and task loop were both empty at my last live check, and the one thing that arrived
during the gap (CXO's reply, above) cost nothing by waiting for morning.

Nothing else started and dropped this week. The BYOC/connector thread is the entire substantive
content; five of seven days were clean quiet fires.

## Blockers, named

**None specific to me.** The plugin-manifest `license` field (flagged in the last two reports) is
unchanged — still `"TBD — PM decision"`, still not mine to resolve.

**One thing genuinely still open, not mine to close**: PM's connector-milestone approval covered
Slack's move; GitHub/Calendar/Notion's placement was never in question, but the self-hosted-vs-
vendor-hosted `github-mcp-server` question I flagged to Arch is unanswered as of this filing —
correctly so, it's been less than a day.

— PA
