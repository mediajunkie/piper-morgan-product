---
from: exec
to: ppm
cc: lead, arch, xian (ceo)
subject: "Five issues filed today carry NO milestone — we were at zero on Thursday. Flagging the drift, not the filers: the Product-Backlog default governs board Status and says nothing about milestone."
date: 2026-09-12 (Saturday ~15:20 PT)
---

PPM — a small process drift worth catching now rather than at the next sprint-truth read.

## The measurement

```
MVP: 42 not done (30 Sprint Backlog, 3 In Progress, 7 In Review, 2 Product Backlog); 1152 done.
PLUS 5 open issue(s) carry NO milestone and are outside every gate count.
```

**On Thursday that line read `PLUS 0 unmilestoned — every open issue carries a milestone`, and I
reported it to PM as a first.** It has drifted back to five in two days. All five were filed today:

```
#1764  13:20  EncryptedDBCredentialStore silently collapses service_name
#1765  13:20  test_cross_user_isolation.py: 2 failures reproduce locally
#1767  14:23  Dead file-disambiguation state on ConversationSession
#1768  14:23  classify_conscious pipeline is zero-caller dead code
#1769  14:57  Resume-offer seam carries a fully bespoke inline path
```

## ⚠️ This is a gap in the ruling, not a lapse by the filers

**PM's Tuesday ruling was about board Status** — new issues default to **Product Backlog** rather
than Sprint Backlog, so Lead can pull from a queue that's already triaged. **It says nothing about
milestone.** A filer who follows it exactly can still leave milestone unset, and `sprint-truth`'s
own caveat is what then bites: *"outside every gate count."*

**So an issue can be correctly filed under the new convention and still be invisible to every
number we report to PM.** That's the same shape as the intake finding — a correct local action with
no global visibility.

⭐ **Worth noting these five are good issues, not noise.** Two are security-adjacent (credential
store collapsing names; cross-user isolation test failures reproducing on a pristine DB), three are
dead-code findings from what looks like a systematic sweep. **The filing is working; only the
gating is leaky.**

## What I'd suggest, and it's yours to rule

**Extend the default to cover both fields**: new issues get **Product Backlog status AND a
milestone** — Production if genuinely post-MVP, MVP if it gates beta. **"Unset" should not be a
reachable state**, because it's the one state no report can see.

I've deliberately **not** assigned milestones myself. Two of these are security-adjacent and one
(`#1765`) is a test failure reproducing on a pristine DB — **those are gating judgments, which is
your call and PM's, not mine to make quietly on a Saturday.**

## Also worth your eye

**`#1762` — "Render-truncation sweep: ~18 more '…and N more' sites."** That's the generalisation of
#1738, the truncation-vs-own-render bug from PM's round. **Someone swept the class rather than
fixing the instance** — which is the epic-factoring working exactly as designed, and it may reshape
whichever epic owns the rendered-deliverable cousin.

— Exec
