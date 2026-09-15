# Exec (Chief of Staff) — carry-forward

**Rewritten 2026-09-14 ~23:30 PT at day-close.**

## Cron
`83258e51`, `38 6,10,14,18,22`. Armed 09-11 06:55, expires ~09-18 → **rotate ~09-16.**
⚠️ One job, correct expression — **NOT evidence the schedule is live.** Only a fire proves that.

## ⭐ Ship #060 — DRAFTED, awaiting PM's edit
`docs/public/comms/drafts/weekly-ship-060-draft-2026-09-14.md` · **calendar row added in the SAME
commit** (pubDate **2026-09-16**, Wednesday).
**PM's direction, followed**: *"focuses on what was delivered primarily in the product and
secondarily in process improvements"* and *"finding our own errors… not necessarily fresh… a single
item."* **Self-correction appears once, in the P.S., not as the theme.**
Title: **"Four bugs, one contract."** Template audit clean — 0 semicolons, 0 banned terms, 0 bare
issue numbers in prose, 5 workstreams engineering-first, 5 learning-pattern components, hero image
live-verified 200.

## Resolved tonight without me
- **#1810 hold LIFTED.** HOST verified before ruling (`gh issue view` + `merge-base`), kept the
  struck-through status history visible rather than erasing it. **Janne's invite is ready** with one
  condition: **the invite asks Janne to configure his own LLM key first** — defense-in-depth against
  **#1809**, which is still open.
- ⚠️ **CXO corrected the record: their FTUX rider was NOT satisfied** by Lead's run, and owned the
  mis-specification as theirs. **The FTUX first exchange remains unobserved in production.**
- **Dispatch repo mass deletion** — 1,683 of 1,684 files deleted by an ordinary-looking commit
  against an incomplete local clone. **Found by the nightly stranded-work sweep, reverted, verified
  by live `ls-remote`.** Nothing needed from me; on the radar as a clone-integrity pattern.
- **PPM owned the epic-12 mistake** rather than defending it — epic 2 reopened, epic 12 retired.
  **Now 11 epics** (my own 09-13 accounting said 9; the drift was real and PM caught it first).

## Blocked on PM
1. ⭐ **The ruleset** — verified still ZERO rulesets, #1744 open, parked since Friday. **Parks Arch
   AND CXO.** Highest leverage item on the board.
2. **Janne's invite** — cleared to send with the key-first condition.
3. **Vercel** deployment storage · **PA's sequencing answer** · **Ship #060 edit before Wed 09-16.**

## State
MVP **54 not done** (32 Sprint Backlog, 3 In Progress, 6 In Review, 13 Product Backlog);
**1,171 done**; 0 unmilestoned. Belt clean.

## Standing corrections on me
- ⚠️ **"No conclusion" is not "no failure"** (cancelled CI runs read as clean).
- ⚠️ **`echo` after `||` asserts nothing** — verify pushes against `origin/main`.
- ⚠️ **`closedAt` is UTC** — compute in Pacific, say so.
- ⚠️ **Membership is not mention** (epic counts).
- ⚠️ **Don't hand-roll liveness comparisons.** My `(role)` grep has a **29% false-negative rate**;
  the belt is wake-window-aware and I am not. **Check every named role's cadence before escalating.**
- ⚠️ **Re-check an anomalous reading once before reporting.** Applied 7×; changed the reading 3 times.
