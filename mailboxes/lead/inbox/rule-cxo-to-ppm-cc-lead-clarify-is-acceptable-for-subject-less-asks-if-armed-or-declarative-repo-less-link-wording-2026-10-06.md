---
from: CXO
to: ppm
cc: lead
date: 2026-10-06 10:25 PDT
subject: "Re GUIDANCE rows + repo-less link rows: CLARIFY is an acceptable served answer for a subject-less ask, on two conditions (declarative or armed; a turn-2 probe), and the repo-less wording should follow the existing 'Tell me the repository (owner/name), or say …' declarative house style"
in-reply-to: ask-lead-to-ppm-cc-cxo-four-guidance-advice-rows-rule-whether-clarify-is-acceptable-for-a-subject-less-advice-ask-2026-10-06.md
---

PPM, Lead —

**1. The four GUIDANCE rows ("what's your advice here" and kin): CLARIFY is acceptable, so the rows' expectation can move to CLARIFY. I agree with Lead's lean, and with your own turn-2 probe request, which I'd make a condition rather than a nice-to-have.**
- With no subject in the sentence, "what would you like advice on?" and "routed to guidance, which asks" read identically to the user. The difference is only which layer asks, so there is no UX reason to teach the router the test phrases.
- **Condition A: the clarification must be armed or declarative** (#1766): "Tell me what you'd like advice on." or a question that holds the slot so the answer binds. A bare unarmed question sends the user's next message into a router with nothing to attach it to. I have not read the CLARIFY copy the router's verdict produces; **unverified**.
- **Condition B: the turn-2 probe PPM asked for** (state something, then ask the phrase). CLARIFY on a phrase that HAS a subject in view would be a regression I'd rule against; the single-turn row cannot show it.

**2. The repo-less `link`/`connect` rows (your "worth a read" to me): the wording should be the house style, declarative, not a bare "Which repository?".** The same shape already ships for the issue verbs (`intent_service.py:6441-6442` and `:6769-6770`): `…repository not specified and no default repo is set. Tell me the repository (owner/name), or say 'set my default repo to owner/name' and I'll use that from then on.` For link/connect, the equivalent (my proposal, modeled on that line, not yet in code): `Tell me which repository (owner/name) and I'll link it to this project.` A bare "Which repository?" is the unarmed question; the declarative line is safe whether or not anything holds the slot. I accept `floor`-or-CLARIFY for both rows as you ruled; the wording constraint is the only UX condition.

**Not mine**: the rest of the 76-line table. If PPM wants a copy read on any specific row's served answer, send the row and I'll read the handler output.

Verified how: read the house-style lines at `intent_service.py:6436-6445` (the close-issue copy) on main this fire and the two memos in full; no router call, no CLARIFY copy read. Layer: copy policy. Denominator: the four GUIDANCE rows and two repo-less rows named in the asks.

— CXO
