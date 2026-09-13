# Exec (Chief of Staff) — carry-forward

**Rewritten 2026-09-12 ~23:25 PT at day-close.**

## Cron
Job `83258e51`, `38 6,10,14,18,22` — 5 fires/day. Armed 09-11 06:55, expires ~09-18 → **rotate ~09-16.**

## ⭐ Where the weekly cycle stands
**Ship #060, window Fri 09-04 → Thu 09-10.** Omnibus 7/7 · 10/10 reports · **internal report
delivered** · **prep complete** (calendar verified, 3 pubs all live 200, hero verified 200,
omnibus day-types read: 7/7 HIGH-COMPLEXITY: COORDINATION).
🔴 **PM RULED the internal-report discussion comes BEFORE the Ship draft.** Hold confirmed correct.
**The draft has not started and should not until that conversation happens.**

## OWED TO PM — the epic accounting, numbered, with denominators
PM's ask via Janus: *"Epic 1 — closed, blocked, or currently worked? Epic 2 — same. Etc."* and
*"I keep hearing 'green for the first time' across various scopes, and I suspect slippery
denominators."*
⚠️ **Method caveat that must ship WITH the numbers**: my first pass regex-counted every issue
*mentioned* in an epic section, not members — it reported epic 2 as "2 open" when the doc says
#1750/#1751 were *"deliberately NOT folded in."* **Epic 2 is closed as scoped.** Membership vs
mention must be stated explicitly or the accounting becomes the thing PM is skeptical of.
**Live open counts (09-12 19:0x):** E1 **4** (#1687 #1747 #1764 #1765) · E2 **closed as scoped** ·
E3 **2** (#1739 umbrella, #1771) · E4 6 · E5 6 · E6 2 · E7 3 · E8 2.
**Still needed**: Lead's own account of working epic-5 items while epic 3 is open — I have the fact,
not the reason, and PM asked for the rule to be visibly applied rather than drifted past.

## Blocked on PM
- **#1617 standup retest** — PM runs it directly with me.
- **Bot → protected main**: ruleset + `github-actions` bypass actor (repo public, zero rulesets = free).
- **Vercel** deployment-storage deletion (14.91/10 GB).
- ✅ **#1687 secret rotation is UNBLOCKED** — Lead posted the fingers-comment 09-12 21:48.

## State at close
**29 issues closed today, 26 MVP** — the biggest day of the window. MVP **44 not done** (30 Sprint
Backlog, 3 In Progress, 7 In Review, 4 Product Backlog); **1,158 done**; **0 unmilestoned held.**
⚠️ **Lead's day-close says "31 closes"; I count 29 Pacific / 23 UTC.** Three numbers, one day — not
an error by anyone, but **exactly the denominator drift PM named this afternoon.** Flag it in the
accounting rather than pick one silently.

## Landed today without me
CIO off the belt + v1.35 shipped with the denominator CXO asked for · PPM ratified milestone-required
filing AND gave all six singletons epic homes · Janus triaged all 16 orphan memos (one was live) and
named their channel · PM ruled orphan mailboxes: only PM-team members get boxes here.

## Standing corrections on me
- ⚠️ **`echo` after `||` asserts nothing** — my push wrapper printed "pushed ✓" on a failed push
  (09-12 07:0x). **Verify pushes by re-reading `origin/main`.** Done every fire since.
- ⚠️ **`closedAt` is UTC** — compute closures in Pacific, and say which.
- ⚠️ **Re-check an anomalous reading once before reporting** (PM's rule). Applied 4×; changed my
  reading twice.
- ⚠️ **Membership is not mention** — new, from tonight's epic count.
