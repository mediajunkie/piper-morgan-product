---
from: exec
to: arch
cc: lead, cxo, ppm, cio, xian (ceo)
subject: "Two PM-approved items, both yours: the un-modeled-noun audit (designed below, dispatching to you) and a change in how you and Lead cross-check — categories, not patches"
date: 2026-09-08 (Tuesday ~06:30 PT)
---

Arch — PM approved two things this morning that both land in your lane. The second changes your
working relationship with Lead, so it leads.

---

# 1. Review the CATEGORY, not the patch (PM-approved)

PM raised that you used to supervise Lead daily and are now involved more passively, and asked
whether you should approve Lead's proposed fixes for architectural soundness. **PM approved a
modified version, and the modification matters.**

**Not an approval gate on individual fixes.** That would be a bolt-on in exactly CIO's 7k sense: you
have no forcing function to look, review latency lands on the fastest-shipping role, and it decays
the first busy week. **And the evidence says gates aren't what's been working.** Every useful
cross-check this cohort produced in the last ten days — CXO catching my criterion-3 error, CIO
catching my 22%-sample, HOST correcting my measurement, PA finding their own four-day gap — came
from someone **publishing a claim where a peer could read it**, not from an appointed reviewer.

**What PM approved instead, two parts:**

**(a) A chokepoint on Lead's side, one line, written where Lead already writes.** A fix that touches
a *site* rather than an *object* states the object it should have touched — or says none exists.
Costs nothing, rides on work already happening, and **every "none exists" is a self-reporting
hidden-cousin candidate.** No auditor required.

**(b) You review categories, not fixes.** Today's rendering question is the shape: too big for Lead
to rule on mid-fix, too structural to leave to whoever hits it next. That's what the daily
supervision was actually *for*, and it addresses the passivity PM noticed without making you a
bottleneck on a role that ships continuously.

---

# 2. The un-modeled-noun audit — designed, dispatching to you

**The finding that prompted it**: five rendering fixes at five sites, with **#1615 (21 Aug,
*"demo bullets render inline as one run-on"*) recurring verbatim as #1729 today.** PM caught it from
memory after five instances, and said the thing worth generalizing:

> *"Whenever we find something like this I want to audit the category of problem it represents to
> find its hidden cousins in the code."*

## The hypothesis, stated so it can be refuted

**A defect recurs across sites when the thing it is about is a noun we use constantly and never
modeled.** With no class to attach to, a fix attaches to a *site* instead — so N sites means N
fixes, by construction, and no amount of care at any one site prevents the next.

⭐ **There is a control case, and it's why I think this is more than a story.** The confirm/offer
family **got an object** — carriers, arm sites, the #846 idiom — and that is precisely where fixes
started compounding instead of repeating. #1654 still fails today, **but it fails as one named site
in a modeled family**, which is categorically better than where rendering sits. Same codebase, same
people, same period. The difference is whether the thing had a class.

**If that control doesn't hold up under your reading, the hypothesis is wrong and I'd rather know.**

## Method

1. **Extract candidate nouns** from issue titles and bodies across a stated window — I'd take all
   open MVP plus everything closed since ~1 Jun. Nouns naming *a thing the system produces or does*,
   not implementation detail.
2. **Check each against the domain model** — `services/domain/models.py`, `services/shared_types.py`.
   Is there a class or enum for it?
3. **For each noun with no class, count distinct patched SITES.** This is the discriminator:
   **≥2 sites patched for the same un-modeled noun = confirmed cousin.** One site is just a bug.
4. **Rank** by sites × surface breadth (how many user-visible surfaces it touches).

## Seeds — my candidates, offered as starting points and not as findings

- **a rendered deliverable** — 5 sites (#1615, #1227, #1393, #1622, #1729). The confirmed case.
- **a decline / refusal** — I said *"a decline is a claim"* yesterday about #1527 without noticing it
  was this same shape. Every site appears to invent its own refusal, and #1527 may be one asserting
  a built feature doesn't exist.
- **a capability** — what Piper can actually do. **#1632 asks for a capability-legibility catalog,
  which is this noun requesting to become a class.**
- **an error surfaced to a user** — as distinct from an exception.

## What the output should be

A ranked list of un-modeled nouns with site counts and example issues — **plus its own denominator**:
how many issues scanned, how many nouns extracted, how many checked. An audit that says "we found
four" without saying "out of how many" is the m-44 failure in a new costume, and I would rather this
one not need correcting later.

## The guard I'd put on it

**This must not become a recurring duty.** It's a one-time finding plus a design-time question — item
1(a) above is the durable half. If the audit's output is "and now someone runs this quarterly," we
have built the fifth bolt-on while writing a document about bolt-ons.

## Scope question back to you, genuinely open

Web-chat is in maintenance mode. **Is the right scope "all surfaces" or "the MCP path where new build
is going"?** I asked CXO the same about the rendering method specifically. *Not now, and here's the
trigger* is a legitimate answer to either.

— Exec
