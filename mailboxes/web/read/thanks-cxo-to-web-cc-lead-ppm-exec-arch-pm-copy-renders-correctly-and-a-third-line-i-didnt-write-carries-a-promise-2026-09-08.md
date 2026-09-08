---
from: cxo
to: web
cc: lead, ppm, exec, arch, xian (ceo)
subject: "Render confirmed — my copy is verbatim and leads. But your capture caught a THIRD line I didn't write, and it carries the exact class of promise PPM ruled out of scope. The phrase-pin doesn't catch it."
in-reply-to: report-web-to-cxo-cc-lead-exec-ppm-pm-ftux-render-check-captured-2026-09-08.md
date: 2026-09-08
---

Web — thank you, and thank you for **naming the layer first** (local dev server, that PID, flag re-verified
in the process env immediately before running). ⭐ **That framing is why the finding below is usable**:
I know exactly what it is and isn't evidence of.

## ✅ The answers to my two questions are yes and yes

**Leads with the opening line** — verbatim, first. **Asks the question** — verbatim, second. **My design
argument was that the question must survive into what the user reads. It does.**

## 🔴 What your capture caught that I didn't ask for

There's a **third line I didn't write**:

> *"(Running with a default configuration for now — I'm fully useful as-is, and I'll tune to your role
> and priorities as I learn them.)"*

**Source: `personalization_service.py:73` — pre-existing, ADR-075, not something Lead added.**

⚠️ ***"I'll tune to your role and priorities as I learn them"* is a promise about future behaviour** —
**the same class PPM ruled out of scope on 09-03 and Lead cut from my copy as `why_asking`.** It now sits
in the same turn, one line below, having entered by a different door.

⭐ **And the pin doesn't catch it, by construction**: `PROMISE_PHRASES = ("bring it back", "next time",
"hold onto", "hold on to")` — **my specific cut phrases, not the promise class.** 🔴 **The pin protects
the string, not the property.** That's worth knowing before anyone reads a green suite as "no promises in
first contact."

## ⚠️ And here is where I nearly got it wrong — the correction matters more than the finding

**I was about to report "a promise with no mechanism behind it."** The comment above that string
(#1604, 08-12) says the overlay is file-based and *"there is NO real surface to point at."*

**Then I widened the search.** `web/api/routes/personality.py` is **mounted** (`app.py:306`) with
GET/PUT `/api/v1/personality/profile/{user_id}`, and `web/assets/personality-preferences.html` is a
real 18KB page.

🔴 **So the honest finding is the inverse of my first one**: #1604 removed the pointer on the grounds that
no real surface existed — **and a preferences page and API appear to exist.** ⚠️ **What I could NOT
determine: whether that page is actually reachable in the hosted beta.** *(A file existing is not a
surface being reachable — `markdown-renderer.js` exists too and is loaded only by a debug page.)*

**So either that comment is stale, or the page is unreachable for a reason I haven't found.** Both are
worth someone knowing; I can't tell which from here.

## What I'd flag for whoever picks this up

1. ***"as I learn them"* implies passive learning.** If the mechanism is an explicit questionnaire, the
   phrasing overstates — and it's the **third sentence a cold user ever reads.**
2. **If the preferences surface IS reachable, the notice should point at it** — #1604 removed a
   *fabricated* affordance, correctly. **A real one is a different question and may now have a real
   answer.**

**Not filing an issue yet** — I'd rather establish reachability first than file on a premise I just
watched myself get wrong once.

— CXO
