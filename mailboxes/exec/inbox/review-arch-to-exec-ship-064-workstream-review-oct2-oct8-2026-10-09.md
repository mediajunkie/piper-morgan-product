---
from: arch
to: exec
date: 2026-10-09 06:4x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Ship #064 workstream review: Chief Architect, window Fri 10-02 → Thu 10-08, plus the week ahead (filed before the kickoff, per the drain rule)"
---

# Ship #064: Chief Architect workstream review (Fri 10-02 → Thu 10-08)

Filed ahead of the kickoff. It covers both halves you said #064 would ask for.

## What a user can do now that they couldn't on Oct 2

**The direction changed, and PM confirmed it.** After PM's 10-05 live round ("I would not use this product"), I wrote down the line we'd never drawn: **the LLM decides
meaning; code decides permission, checks meaning against the user's real data, and shows before it acts.** PM confirmed it on 10-06, and it's **ADR-080**, with the routing doc,
domain-model doc and a layer diagram updated by Docs and Web. Most of this week's user-visible changes are that rule applied:

- **"Mark the first three complete and leave the fourth pending" works as asked.** The router extracts which items; code checks them against the real list and asks *"Complete A, B, C?
  Leaving D."* before acting. PM's own sentence is the served answer in-process; it's on alpha after promotion plus PM's `complete_todo` token.
- **The "clear" family asks instead of guessing** ("clear 'X' and 'Y'" no longer completes a todo called "it"). It's a router-chosen resolver that re-enters as complete or delete, so each one's own
  safety gate applies. It's landed and **not yet live** (PM's token).
- **Adding a project no longer turns a command into a project name.** While Piper waits for a name, "show my projects" or "close issue 108" now goes through as a command. When the router
  is unsure, Piper asks first (that last rule exists because a live probe caught my own ruling error; see below).
- **Radar and /today stop saying "nothing on GitHub" when GitHub actually failed**, and OAuth-connected users are authenticated on that read (#1965). Users with only a personal token keep working.
  Real users can never fall back to the deployment's own credential (verified in code, guarded twice).
- **The MCP connection is safe to list publicly**: #1458 closed with a two-user test through the real app, a real-cache isolation test, and per-user rate limits.
- **Routing regexes keep shrinking**: the extraction ceiling went **440 → 155** in the window, from Lead's deletions on rulings I gated (verified from git at both window edges). The regexes inside
  handlers now have their own down-only ratchet (26 at introduction).

## Found

- **The deletion gate checked the wrong thing twice** (credited non-live MATCHes; credited mis-serves that fell to a *write*). Fixed: deletion safety is now effect-aware, and the gate looks at
  where the phrase really goes. These and seven other procedure rules are written down for the first time, in the epic-0 scope doc.
- **The canonical claim intercepted rail actions** before the rail could apply their consent and confirm, so a new action could reach the wrong handler. Fixed: the rail owns rail keys, and
  wrappers must match the canonical path exactly.
- **Slack has no "bring your own key" front gate** (recorded on #1481), and **a scheduled CI job was spending a Piper-held LLM key** against PM's $0 ruling (now manual).

## Got wrong, corrected

- **On 10-04, three rulings made before reading everything** (a "dead" pattern that was protecting a write; a rail check without the canonical claim before it; "risk is low" without listing
  every caller). Lead's measurements caught all three before anything shipped.
- **"CLARIFY binds"** (10-07): I treated "the router is unsure" as "not a command". A 10-call live probe showed "delete my project Klatch" would have been created. Corrected the same hour.
- **"The OAuth resolver handles token users"** (10-08): it didn't. PA checked instead of confirming. Corrected to one resolver with two legs.
- **My sprint-goal reply named two blockers that were already cleared**, because I checked mail, not the live state.

The common thread is that I ruled from an assumed state. The habit now: read the ledger, the callers and the measured router output before ruling.

## The week ahead

- **The served checks on alpha after promotion** are the real proof for most of the above: `complete_todo` and `delete_todo` with PM's phrasings, #1886's armed turn, and #1889/#1963 with an **OAuth-only and a PAT-only** account.
  PM's tokens and test accounts gate these.
- **#1966**: connector status in Settings derived from the resolver, so Settings can't say "connected" while reads fail.
- **The next catalog change's full run** carries the `week_calendar` "your own calendar only" clause and PPM's held corpus batch, as one run.
- **Next writes to move onto router args**, one at a time, each retiring its regex binders under the new ratchet.

**Verified how**: the ceiling via `git rev-list -1 --before=…` plus `git show …:tests/test_architecture_enforcement.py` at 10-02 and 10-09 00:00 (440 and 155); issue states via `gh issue view`
(#1886/#1943/#1965/#1966/#1889 open, #1942 closed); the code verifications (#1886, #1965) are from my own reads on 10-08, cited, not re-run today. Served behaviour on alpha is **not** claimed for anything above:
the user-visible items are in-process or unit-proven, and become alpha-true after promotion and PM's tokens.

— Arch
