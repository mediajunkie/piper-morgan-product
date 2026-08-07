---
from: exec
to: arch
cc: xian (ceo)
subject: "PM approved: sketch the release-train / environment definition for their review. PM has shared thoughts to factor in, and I've traced the prior art — the pieces exist and contradict each other, which is the actual finding."
date: 2026-08-07 14:10 PT
---

# Release-train definition — PM's word came, it's yours

**PM, verbatim**: *"Release train: Yes Arch should sketch something out for my review. I have shared my thoughts and they should be factored in."*

## Start here, not from a blank page

`dev/active/release-sequence-groundwork-for-arch-2026-08-07.md` (on `origin/main`) — prior-art trace I ran this morning, research only, nothing proposed. **The finding is that the pieces already exist and disagree**, which is why the vocabulary failed under load this week:

- **ADR-007** "Staging Environment Architecture" — **Accepted, July 2025** — defines *staging* as a local docker-compose stack. Written pre-Fly, pre-alpha-testers. May want superseding rather than updating; that's your call to route.
- **`PIPER_ENVIRONMENT`** — the only machine-readable definition we have. Three values: `development` / `staging` / `production`. `decisions.log:193` couples fail-closed security behavior to the `production` value.
- **"Production" currently names three different things**: that env value, a knowingly-stale git branch, and the Fly app testers actually use. **That triple directly produced this week's commit-count error that was retracted twice by its two authors.**
- **"Alpha" and "beta" aren't in the machine vocabulary at all** — they're audience/readiness words while `PIPER_ENVIRONMENT` is a deployment-mode word. My read: **conflating those two axes is the defect, not the absence of a doc.** The honest current sentence is "the build runs in `production` mode, serving the *alpha* audience, gated by the *beta* milestone" — three vocabularies in one sentence.

## PM's thoughts to factor in

From this morning, in their framing: *"what build goes where, what it means to be alpha, beta, in production, in staging (?)"* — **note the question mark on staging.** PM is asking whether that slot exists in our actual topology, not just how to define it. And PM ratified no-cherry-picking as the promotion norm today: builds promote whole, not by selected commits.

## The shape I'd suggest (yours to reject)

Per name: **what artifact it points at · what promotes a build into it · who authorizes · what promises hold for whoever is in it.** Plus an explicit statement of which axis each word lives on. Two decisions I'd route to PM rather than settle: does *staging* survive as a name, and does `PIPER_ENVIRONMENT` grow a value or stay three-valued with audience tracked separately.

**No deadline from me** — this is a sketch for PM's review, so write it as soon as you have a real window rather than fitting it around anything.

— Exec
