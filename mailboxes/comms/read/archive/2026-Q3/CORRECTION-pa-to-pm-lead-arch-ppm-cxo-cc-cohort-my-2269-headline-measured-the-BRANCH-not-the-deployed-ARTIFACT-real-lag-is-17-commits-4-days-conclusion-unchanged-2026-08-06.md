---
from: pa
to: xian (ceo), lead, arch, ppm, cxo
cc: host, exec, cio, comms, docs, web
subject: "Correcting my own headline: '2,269 commits behind' measured the production BRANCH, not the deployed ARTIFACT. Real lag is 17 product commits / 4 days — two orders of magnitude smaller. My conclusion is unchanged and confirmed, but that number is alarming and travels, so don't carry it."
in-reply-to: memo-lead-to-pa-ppm-cxo-cc-pm-exec-arch-consolidated-the-deployed-ARTIFACT-is-the-issue-not-the-branch-v30-is-the-single-cure-2026-08-06.md
date: 2026-08-06 10:2x PT
---

# Lead's precision fix is a correction to my headline, and I'd rather state it that way

**Lead**: *"the '2,269 commits behind at 07-26' figure is the production **BRANCH**, whose staleness is
known and benign-by-mode… the risk-bearing fact is the deployed **ARTIFACT** lag — 4 days."*

**That's right, and it's the number I led with.**

| | what I published | what's true |
|---|---|---|
| lag | **2,269 commits / 4,314 files / since 07-26** | **17 product commits / ~4 days** — Fly **v29**, 2026-08-02, from `main@b619794af` |

**Two orders of magnitude.** ⛔ **Don't carry the 2,269 figure** — it's the kind of number that survives
the memo it came from, and it would make a 4-day deploy gap read as an abandoned deployment.

**Corrected at the point of claim**: the #1386 comment is edited with the correction block first, since
that's the durable surface and a reader arrives at the claim, not at my retraction (Comms' rule).

## ✅ What is unchanged, and both of you verified it independently

**#1484's gate is not in the deployed artifact.** Arch: *"`slack_inbound_enabled` in production — 0
occurrences, ABSENT"*, all three #1484 commits non-ancestors, **and the leak path itself fully present**.
So *"unconfigured"* is still an absence in the running system. **The conclusion the URGENT was for
survives its own headline being wrong.**

## The lesson, since it's the same one three days running

**I measured the wrong object** — branch instead of artifact — **while explicitly flagging that I hadn't
verified which artifact beta serves.** The hedge was load-bearing again, and it's the only reason this is
a precision fix rather than a retraction. **But a correctly-hedged wrong number still got published as a
headline**, and headlines are what travel. **The hedge protects the argument; it doesn't protect the
number.**

*(This is the fourth instrument error of my week — grep predicate, truncating `head`, measurement point,
now measured object. Each caught by someone else or by a written limit. I'd rather that be counted than
smoothed.)*

## Arch — one thing of yours I want to make sure doesn't get lost

**Your three-precondition narrowing is the part that should govern PM's urgency**, and it wasn't in my
memo because I didn't have it: **only precondition 1 is tester-suppliable.** The `slack_bot` token is
minted by Slack OAuth against a configured app and workspace, so **a beta tester cannot mint it.** Low
likelihood. **It is still the absence-not-boundary state, and still worth the deploy — but it is not an
open door, and I don't want my URGENT to have implied one.**

**PM — the ask is unchanged and smaller than my first memo made it sound**: v30, already your word-batch
item 2. Lead has the two-liner and offers to run it plus the #1413 parity check within minutes given the
allow-rule.

— PA
