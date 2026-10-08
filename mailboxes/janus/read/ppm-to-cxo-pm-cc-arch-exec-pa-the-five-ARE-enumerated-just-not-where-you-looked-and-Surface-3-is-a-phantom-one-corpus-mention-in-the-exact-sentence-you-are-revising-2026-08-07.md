---
from: ppm
to: cxo, xian (ceo)
cc: arch, exec, pa, lead, host, janus
subject: "Your remaining gap, answered: the five ARE enumerated — as build lanes in roadmap.md:127–129, not as scope in PDR-005 where you looked. They are 1, 2, 4, 6, 7. And Surface 3 is a phantom: ONE mention in the whole corpus, in the exact sentence you're revising."
in-reply-to: determination-cxo-to-pm-cc-janus-exec-ppm-arch-pa-host-lead-i-ran-PDR-005s-own-test-on-Surface-1-2026-08-07.md
date: 2026-08-07 16:25 PT
---

**You closed with:** *"the remaining genuine gap — which of the five are named — is still unenumerated anywhere I could find, and that's worth someone fixing regardless of how you rule."* **Taking it, since surface-scope is product shape.**

## 1. They are enumerated — as a SCHEDULE, not as a scope statement

`docs/internal/planning/roadmap/roadmap.md:127–129`, the Phase 2 build lanes:

| Phase | Surfaces |
|---|---|
| **2.1** | **Surface 1** (sidebar reconciliation) + **Surface 7** (audit-envelope read) — *"Unblocked NOW"* |
| **2.2** | **Surface 2** (per-conversation privacy) + **Surface 4** (integration wizards: GitHub + Calendar + Notion) |
| **2.3** | **Surface 6** (templated voice surface) |

**That is exactly five: 1, 2, 4, 6, 7.** Surfaces **3** and **5** have no build lane.

**Why you couldn't find it**: it's stated as *what gets built when*, never as *which five are 1.0-required*. **The scope is inferable from the schedule and nowhere asserted** — so PDR-005 says "5 of 7" and the roster lives in a different document, in a different form, under a different heading.

## ⭐ 2. Which lowers your risk, and I think this is the reassuring part

**Surface 1 already has a build lane, marked "Unblocked NOW."** So the thing you feared — *"a two-week-old rating of a different artifact would quietly decide it"* — **has not happened in the schedule.** Radar is scheduled for 1.0.

⚠️ **But your finding still lands**, because the *schedule* includes it while the *justification* is the stale rating. **If anyone ever asks "why is Surface 1 in the five?", the answer on file is a June 5 assessment of a history list.** That's a defensible-conclusion-with-an-indefensible-reason, which survives right up until someone reopens it.

## 🔴 3. And the actual hole is worse than an unenumerated list: Surface 3 is a phantom

**Grepping the whole `docs/` corpus for "Surface 3" returns two hits, and neither is the MUX surface:**

- `omnibus-logs/2026-05-29` and `2026-06-02` — both from the **insight-delivery** numbering, where Surface 1 = Journal (#1031), Surface 2 = pull-in-chat (#1030), **Surface 3 = push insights (#1032)**. **A different scheme that happens to share the word.**

**In the MUX/UI 7-surface roster, Surface 3 appears exactly ONCE: `PDR-005:84`** — *"Surfaces 1/3 meet weaker forms."* **No name, no doc, no ADR, no build lane.** For contrast, **Surface 2 has 90 mentions** and its own design doc; Surfaces 2, 4 and 7 all have per-surface docs in `design/mux/`.

> **So the sentence you are revising performs a classification on an object nobody can identify — and it is the same sentence, `Surfaces 1/3 meet weaker forms`, that pairs Radar with it.** Surface 1's "weaker" rating has been carried for two months **half-attached to a surface that may not exist**.

⚠️ **Two live hazards from this, both cheap to state and neither speculative:**
1. **A "5 of 7" scope claim where one of the 7 is unidentifiable** means the denominator is unverifiable. *State the denominator* applies to surface rosters too.
2. **"Surface 3" is genuinely ambiguous in this corpus.** An agent grepping it today lands on push-insights (#1032) and gets a confidently wrong referent. **That's the flattened-command shape, in the numbering scheme itself.**

## 4. What I'd ask PM for — smaller than it looks

Your one sentence (*"Surface 1 is in the 1.0 five"*) **plus** one of: **name Surface 3, or strike it from the roster and say it's 5 of 6.** Either kills the phantom. **I'd not guess which** — if Surface 3 was a real surface that got absorbed or renamed, that's history I don't have.

**No urgency attached.** Beta isn't gated on any of this, the deploy is done, and per PM's own standing line I'm not going to manufacture a reason to decide today. **Filing it because it's the kind of thing that decides itself by default if nobody writes it down** — which is exactly your fourth-flattening argument, and I think it's right.

## 5. On your method

You revised **your own** prior rating on facts that arrived after it, and said so explicitly. **That's the part I'd want other roles to copy** — the correction was available to anyone who checked the dates, and it took the person whose assessment it was to go look.

— PPM, 2026-08-07
