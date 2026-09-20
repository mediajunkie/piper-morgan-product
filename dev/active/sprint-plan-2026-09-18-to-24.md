# Sprint plan — Fri 18 → Thu 24 September

**Written 2026-09-20 (Sunday), two days into the week.** Late by design of circumstance, not
intent — PM: *"better late than never and that will give us something to iterate on next Friday
morning."* **From next week this gets written Friday, as step 5b of the weekly cycle.**

⚠️ **This plan does not gate anyone.** PM's standing rule: *"The team should never freeze waiting
for the new week's plan. When in doubt, current priorities continue until refreshed or updated."*
If a role's own read of their lane differs from a line below, **theirs wins** and I'd rather hear it
than have it followed.

---

## Where the milestone stands

**MVP: 56 open, 29 never started. 41 days to 30 October.** Beta-Blockers sprint: **246 of 302
closed (81.5%).**

Last week closed 45 and created 56 — **net +11**, across five working days. Most of the inflow was
discovery inside families already being worked, not new surface. **The question this week is
whether that converges.** `sprint-truth.py` now snapshots and reports the delta, so Friday will
have an answer rather than an impression.

---

## The one thing this week is about

🔴 **Unblocking observation of production.**

Three separate problems turned out to share one absence, and none of them is a feature:

1. **Janne's invite is held** — the alpha runs `0.8.10.14`, deployed **July 16**, predating the
   server-key abolition. Our first external tester would land on a build that predates several of
   this month's rulings.
2. **CXO hit "nobody can see this in prod" three times in one day.** Only one of the three is the
   stale deploy. One needs a shell on the box; one was a verification run that simply wasn't against
   production.
3. **There is no test account** — no self-serve `/register` (removed in #1504), no documented login
   — so no signed-in view can be verified by anyone.

⭐ **CXO's line is the honest summary: "nothing routinely exercises production at all."**

**Success for the week**: a proposal PM can rule on that says what alpha and beta each *are*, how
code reaches them, and how anyone checks that it did. **Not the fix — the decision.**

**Owner**: Pard leads the process, Lead supplies the setup specifics. In flight since Friday.

---

## Per lane — intentions, not assignments

| lane | what I understand is in flight | gated on |
|---|---|---|
| **Lead** | #1765 as of this morning, PM-approved. Epic 1 closed Friday, belt green 10/10. | — |
| **Pard + Lead** | The hosting/alpha/beta proposal. **The week's highest-leverage thread.** | — |
| **Web** | **website#43 — GO'd this morning**, moving 240 MB of build inputs out of `public/`. Then Vercel verification. | — |
| **PPM** | Collapse the mini-epics into a catch-all per PM's ruling; refresh the ordering Lead reads from. | — |
| **Arch** | #1824 (the five-way `auth` bucket split) as a real work item; the ruleset migration when the permission classifier allows. | classifier |
| **CXO** | The T-axis probe decision — **the window closes when #1688's MCP arm starts writing output.** | **PM** |
| **HOST** | Trust gates; the invite roster stays held until the hosting decision. | hosting |
| **Comms** | The drafts queue — **9–10 pieces awaiting PM's voice pass.** Ship #061 review after PM's pass. | **PM** |
| **Docs** | Omnibus continuity; Ship #061 publish **Wed 09-23**. | PM's pass |
| **CIO** | 7x part 2; hooks sequenced after the reboot pilot per Pard. | — |
| **PA** | BYOC readiness in parallel per the 09-15 ruling. | — |

---

## What needs PM, and roughly what it costs

**Small — about fifteen minutes total, and each unblocks a role:**
- **Bets 001–003** — three fields on one memo. *"None named"* is a complete answer for the buyer.
- **CXO's probe** — spend the re-run before the window closes, or accept the gate stays unenforceable.
- **PA's question** — draft-then-review, or review-then-draft.
- **Web's `integration-reveals-all` workDate** — one yes/no.

**Needs a session, not a reply:**
- **Web's obs-pass walkthrough — 94 days old, ~31 items each needing a verdict.** This is the one to
  schedule rather than squeeze.
- **Web's site walkthrough — 113 days.**

**The real bottleneck, which no plan fixes:**
- **Comms' 9–10 queued drafts.** Growing at roughly three a week. Deploying the team differently
  does not touch this.

---

## What we are deliberately NOT doing

- **Not throttling the duty cycle.** Usage is at 40% one-third through, but Friday and Saturday
  carried the entire fleet renewal plus the closeout cycle — both one-time. **Reassess Monday
  10:00**: closer to 50% than to 33% means it is converging.
- **Not chasing the Ship.** Parked till after the weekend at PM's call; pubDate holds at Wed 09-23.
- **Not starting epic 6** or anything below it in the ordering. It is correctly waiting its turn.

---

## How we will know on Friday

**This is the half that makes the plan worth writing.** At Friday's review, against this document:

1. **Did the hosting proposal land, and did PM rule on it?**
2. **Is the invite sent, or is it held for a stated reason?**
3. **`sprint-truth` delta** — did the net move toward zero, or is inflow still outpacing closure?
4. **Did any epic close and stay closed?** Last week's answer was no; epic 2 closed and reopened.
5. **Which of the small PM items are still open?** If the same four are listed next Friday, the
   problem is the routing, not the items.

---

**Verified how**: milestone figures from `sprint-truth.py` and PM's dated exports. Per-lane lines
from each role's own closeout, carry-forward, or this week's trunk activity — **not from my
impression of their lanes**, and four roles have already confirmed their lane read is accurate.
Hosting facts from Lead's SSH read (`0.8.10.14`, July 16, corroborated three ways). **Layer:
reported state plus committed artifacts. I have not verified any role's in-flight work directly.**
