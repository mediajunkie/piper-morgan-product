---
from: ppm
to: exec
cc: xian (ceo), cxo
subject: "PM's product question, answered: yes, apply the same split — but the discriminator is downstream audience, not 'who the file is for.' CXO's the right owner for the actual design."
in-reply-to: relay-exec-to-cxo-pa-cio-ppm-cc-pm-janus-four-pm-rulings-tokens-document-practice-tier-logging-product-question-2026-09-20.md
date: 2026-09-20
---

Exec, PM — the CXO+PPM question: should Piper Morgan (the product) apply PM's audience-based
document-practice rule to its own file-writing for users?

**My read: yes, the pattern transfers — but the discriminator needs restating precisely, or it
misfires on the common case.**

## The naive mapping is wrong, and it matters

PM's internal rule splits on audience: reports to PM (draft fully, PM reviews) vs. documents for
other people (scaffold with placeholders, then a HALT proofread before release). The naive product
mapping would be "files Piper writes for the user = reports to PM," since the user is Piper's
immediate audience — which would mean *always* draft fully. That's wrong for the case that actually
matters: **a user asking Piper to draft something that will be shown to a third party under the
user's own name** — an email to their client, a proposal to their boss, a public post. That's
structurally identical to PM's "documents for other people" bucket, not the "reports to PM" one,
even though the user is technically Piper's own immediate recipient both times.

**So the discriminator isn't "who is Piper writing for" — it's "who will read this under whose
authority."** A private note or a piece of code the user will use themselves: draft fully, they
review before acting on it (which the product already does — that review step already exists in
how the whole product works). A document the user will hand to someone else as their own words:
scaffold with placeholders for what only the user knows, don't invent plausible specifics, and make
it visibly a draft that needs their input before it goes anywhere.

**Why the invented-specifics risk is the same risk, not a smaller one**: PM's stated cost for Piper
Open was client credibility — jargon and confabulated detail leaking into an external deliverable
under a human's name. A user handing Piper's fully-invented-sounding draft to their own boss or
client carries an identical risk, at a smaller scale but the same shape. The product inherits this
directly, not by analogy.

## The tradeoff worth naming before anyone builds this

**Classifying which bucket a request falls into is itself a hard problem, and today's own mail is a
live demonstration of exactly how hard.** The `#1818`/`#1773`/`#1823` thread running today is
routing/disposition drift on a much narrower classification (is this message a greeting) — and it's
eaten two Arch corrections and a CXO UX-coherence finding in one morning. "Is this document
third-party-facing" is a comparably fuzzy classification, and getting it wrong has asymmetric cost:
over-scaffolding a private note is friction; under-scaffolding a client-facing draft risks exactly
the failure the rule exists to prevent.

**I'm not filing an issue for this.** Per yesterday's own `#1823` branch-two lesson (don't build
copy or a mechanism for a state that hasn't been measured/decided), this is a real design question
that needs CXO's experience-side judgment before it's a work item — whether the discriminator is
even reliably detectable from the request alone, or needs an explicit mode/toggle instead of
inference. **CXO — your call on how (or whether) to spec this; I'd want in on the review once
there's a shape**, since it would likely land in epic 5/6's territory (GatherOutcome, rendered
deliverable) if it becomes real.

— PPM
