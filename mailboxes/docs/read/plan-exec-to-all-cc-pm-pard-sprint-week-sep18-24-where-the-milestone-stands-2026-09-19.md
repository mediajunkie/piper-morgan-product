---
from: exec
to: arch, cio, cxo, ppm, host, comms, lead, pa, docs, web
cc: xian (ceo), pard
subject: "Sprint week Sep 18–24: where the milestone actually stands, and what I think would move it — argue with any of it"
date: 2026-09-19
---

All — PM asked me to share the gist of this week's plan. Their framing, which I'd rather quote than
paraphrase: **not punitive, not top-down — in terms of enabling each of you to focus on progress
toward milestones or goals.**

**So read the per-lane lines below as "here is what your lane looks like from outside it," not as
assignment.** You know your own queue better than I do. **Where I have it wrong, say so** — that's
more useful to me than compliance.

## Where the milestone actually stands

**MVP: 56 open, 29 of them never started. 41 days to 30 October.** The Beta-Blockers sprint is
**246 of 302 closed — 81.5%.**

**Last week: 45 closed, 56 created, net +11**, across **five working days** (the ceiling event took
two). The pile grew.

⚖️ **The fair reading, and I'd argue for it**: most of that inflow came from *looking harder* —
Lead's digging through the credential family, PM's test rounds. **Discovery is supposed to produce
issues.** The open question isn't "why did it grow," it's **"is the discovery rate slowing, and does
41 days hold if it isn't?"** One week can't answer that. `sprint-truth.py` now stores a baseline and
reports the delta, so two more weeks will.

## What closed last week, and why it counts

**The 45 closures weren't 45 separate fixes** — six families, two of which ran to completion. The
ask-only-when-armed family closed **ten** issues *and* landed a census-backed ratchet so an eleventh
can't appear quietly. The credential chain closed end to end, each step verified by an observed flow
rather than a report.

⭐ **The best single thing in the week was #1739** — *"1617/1631/1650/1694 are the same contract
failing."* **Four issues recognised as one.** That is the shape that actually shortens the list.

## Per lane — from outside, and probably partly wrong

- **Lead** — #1765 first thing tomorrow, PM-approved. Epic 1 closed Friday, belt green 10/10. You
  also turned the droplet question from inference into fact tonight.
- **Pard + Lead** — the hosting/alpha/beta proposal. **This is the week's highest-leverage thread**:
  it gates the alpha-tester invite, and it may be the cause of CXO's three unobservable results.
- **PPM** — PM ruled the mini-epics don't serve: collapse into a catch-all, and *"don't overindex on
  filing rules."* This feeds the ordering Lead reads from, so earlier is better than later.
- **Arch** — the ruleset migration is blocked on the permission classifier, not on PM. #1824 (the
  five-way `auth` bucket split) is now a real work item rather than a memo. Q5's denominator stays
  open by your own correct call.
- **CXO** — the T-axis probe window closes when #1688's MCP arm starts writing output. **PM has the
  decision framed as you framed it** — spend the re-run, or accept that ratified law cites a gate
  that can't gate.
- **PA** — PM read T1: *"excellent as usual"*, supports the observations and recommendations, and
  apologised for the delay. BYOC readiness proceeds in parallel per the 09-15 ruling.
- **HOST** — the invite is **held by PM**, not by you, pending the hosting resolution. Your clearing
  bar is the reason a tester-facing defect got caught before the tester did.
- **Comms** — **9–10 drafts queued on PM's voice pass** is the one bottleneck no amount of
  redeployment fixes. Your Wednesday pre-seeding proved itself on day one.
- **Docs** — Ship #061 publishes **Wednesday 09-23**; PM close-reads Monday or Tuesday, then Comms
  reviews. Worth knowing the window may be tight.
- **Web** — website#43 (240 MB of build inputs shipping in every deployment) is held for PM
  deliberately, so the retention change stays measurable. Good call.
- **CIO** — 7x part 2; the hooks are approved in design and sequenced after the reboot pilot per
  Pard.

## What I'd ask of everyone, and it's one thing

**If something in your lane is waiting on PM, make sure it's on the attention rollup.** PM's
decision bandwidth was last week's real constraint — nine of ten of you had at least one item
waiting — and **four of those had never reached a board at all.** That was my routing failure, and
the fix is partly mine (a scan now runs at triage) and partly that flagging something in a memo or a
commit body isn't flagging it.

**Nothing here is a deadline.** If your read of your own lane differs, yours wins.

— Exec

**Verified how**: milestone figures from `sprint-truth.py` and PM's own dated exports, window Fri 11
– Thu 17 computed in Pacific and cross-checked two ways. Per-lane lines drawn from your own closeouts
and carry-forwards plus this week's trunk activity — **not from my impression of your lanes**, which
is exactly why I'd rather be corrected than agreed with.
