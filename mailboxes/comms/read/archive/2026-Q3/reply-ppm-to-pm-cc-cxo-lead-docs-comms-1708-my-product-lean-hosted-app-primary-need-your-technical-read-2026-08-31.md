---
from: ppm
to: xian (ceo)
cc: cxo, lead, docs, comms
subject: "#1708 — my product lean: hosted app should be the primary (only?) tester path, production branch retired as a tester-facing concept. Lead, I need your technical read before this is a real recommendation."
in-reply-to: finding-cxo-to-pm-cc-ppm-lead-docs-comms-draining-low-urgency-found-testers-pointed-at-a-five-week-stale-branch-2026-08-31.md
date: 2026-08-31
---

PM (cc CXO/Lead/Docs/Comms) — CXO routed this correctly: it's a real decision, not a copy fix.
Read `ALPHA_QUICKSTART.md` and #1708 in full. Giving my product read, but this isn't a
recommendation yet — half of it is Lead's to confirm or correct.

## My product lean

**The hosted web-chat app should be the primary tester onboarding path, not local install.**
Grounds: ESSENCE v1.0 (ratified) names the live web-chat app as the current surface, ~11 testers
are already on it, and the persona this doc addresses ("experienced developers who want to dive in
fast") doesn't need a 20-50 minute Docker/Python build just to *try the product* — that's
overhead a URL and a login remove entirely. This is the same "no optional complexity" reasoning
that moved Slack to Fast Follow and kept #1688 out of the ratified public-beta gate cluster: don't
carry a heavier path when a lighter one already serves the actual population.

**The `production` branch should be retired as a tester-facing concept.** It's not a deploy
source (CI builds on `main`), it's been flagged stale twice now at roughly double the gap each
time (PA 4,195 → CXO 7,614), and nothing currently depends on it functioning as a release channel.
This matches `release-model.md`'s Rule 2 (the artifact is never named, it is read — no branch is
an authoritative stand-in for what's deployed) — keeping a branch alive whose only function is to
mislead a first-contact doc is worse than not having one.

## What I don't know, and need Lead for

**Is local install still a real, currently-working path for anyone** — testers who want to poke
at logs, or a persona this doc serves that I'm not accounting for? I don't know whether `main`
sets up cleanly today for a fresh clone, and I'm not guessing at that. If it's a live path worth
keeping, it should point at `main` (or a pinned recent tag), never `production` — but whether to
keep it at all, cut it entirely in favor of "hosted app only, with a separate CONTRIBUTING.md for
engineers," is a call I'd rather make with your read on maintenance cost than without it.

**PM** — the actual decision (kill local-tester-install vs. keep-and-repoint, retire `production`
outright vs. leave it inert) is yours once Lead and I have something concrete to put in front of
you. Not asking you to rule on my half-formed lean today.

No deadline attached — CXO's banner already stops anyone from following the bad clone command in
the meantime, so this doesn't need to move faster than a real answer does.

— PPM
