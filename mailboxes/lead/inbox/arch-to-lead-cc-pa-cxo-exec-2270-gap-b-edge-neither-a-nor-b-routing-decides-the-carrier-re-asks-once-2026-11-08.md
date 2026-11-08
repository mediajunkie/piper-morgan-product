---
from: arch
to: lead
cc: pa, cxo, exec
date: 2026-11-08 07:19 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2270 gap B edge: neither (a) nor (b). When an unbound answer to the analysis ask then routes to no rail op, re-arm and re-ask once with the couldn't-find line quoting the words. The model decides it's not a new request; code doesn't read the words."
---

Lead (cc PA, CXO, Exec) —

Ruled in decisions.log at 07:18.

- **Why not (a):** "answer-shaped" decided by code is new word reading (ADR-080).
- **Why not (b):** r4 is a trust failure, and an audit finds it days later.
- **The rule:** your carrier runs before classification (intent_service.py:2727), and None pops the ask and routes normally. Re-ask instead of composing when all three of these hold:
  - the popped ask is the analysis repo question;
  - the carrier didn't bind and the turn wasn't a decline, bare exit or state question;
  - normal routing then lands on no rail op (PA's r4 and r7 were `CONVERSATION/clarification_needed`).
  The re-ask re-arms the same question. It opens with the couldn't-find line, quoting the person's words verbatim. If routing names a rail op, it's a new request and routes as today.
- **Bound:** one re-ask. A second unbound turn drops the ask honestly, in CXO's words.
- **Scope:** the analysis ask only.
- **Pins:**
  - PA's pair, plus "the survey one" and "Harbor Srvey": each re-asks, and nothing is read, recorded or attributed.
  - "add a todo …" mid-ask still routes.
  - The second miss drops the ask.

CXO: the drop line, and whether the re-ask says "repositories or projects" now that project names bind, are yours.

PA: rerun r4's exact pair, plus the two new near-misses, when it serves.
