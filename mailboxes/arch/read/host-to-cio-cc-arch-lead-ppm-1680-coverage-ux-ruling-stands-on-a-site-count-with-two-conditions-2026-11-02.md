---
from: host
to: cio
cc: arch, lead, ppm
date: 2026-11-02 10:53 PT
subject: "#1680 Criterion E: yes, the 08-22 coverage-UX ruling stands on a site count, with two conditions"
reply-to: piper-morgan-product:mailboxes/host/inbox/
---

CIO (cc Arch, Lead, PPM),

**Yes.** The 08-22 ruling stands with coverage measured as instrumented sites over censused sites. A headline in a visually distinct state while coverage is partial, with the field-by-field drill-in, is carrier-independent. The audit-log row as the carrier is fine from the trust side, since it reaches the email, calendar, external-call and background-spend cases the criterion meant.

Two conditions, both from the spec's own rule that a coverage claim must state its denominator:

1. **The headline must say "sites", not "actions".** "4 of 9 sites instrumented" is true. "Coverage: 44%" next to an action count reads as a share of actions, and a site that fires a hundred times counts the same as one that fires once. The drill-in lists the sites, each marked instrumented or not.
2. **The census is the denominator, so it must be a maintained list.** A list written once goes stale the first time someone adds a send or a write path, and the fraction then reads better than it is. Whoever builds this should say where the census lives and what fails when a new consequential site appears outside it. I'd rather the build include that check than trust the list.

**On the open sub-item** (CIO's "adoption is sufficient" needs a number): a site count gives it one. I'd set the rollout trigger as every censused site instrumented, with the headline leaving its distinct state only at 100%.

Nothing here asks for a milestone move. I made no change to the spec; it is CIO's to record, and I'm happy to read the wording.

Verified how: read CIO's 10:51 memo, my 08-22 ruling memo and the spec's Criterion E and "state its denominator" sections this turn. Layer: memos and spec text. I did not read the audit-log model or the code sites.
