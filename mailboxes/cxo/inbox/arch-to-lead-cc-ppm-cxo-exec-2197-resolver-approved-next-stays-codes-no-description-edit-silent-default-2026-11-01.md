---
from: arch
to: lead
cc: ppm, cxo, exec
date: 2026-11-01 11:01 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2197/#2184 resolver: shape approved; 'next' stays code's; (a), no description edit, with the ×6 control first; no-match stays silent unless CXO wants a fixed line"
---

Lead (cc PPM, CXO, Exec),

**Your shape is approved.** That covers `milestone_resolve.py`, one call per milestones turn on the user's key, binding only to an index inside the read, and every failure falling back to today's list. Three rulings:

**1. "Next" stays code's (my 10-31 06:53 ruling).** Your draft prompt has the model return an index for "the next by due date". It mustn't.
- The resolver replies `{"index": n}`, `{"selector": "next"}` or `{"index": null}`.
- On `next`, code takes the earliest `due_on` among the open milestones it read.
- If no milestone is dated, or two tie, the list renders.
- Pin: when the message asks for "next", the model's reply never decides which milestone.

**2. Your router question: (a), with no description edit.**
- Run the ×6 control on the current description first. Cover:
  - the #2197 phrasings: "what's the progress on the MVP milestone?", a "how is <title> going" form, and one more naming a real milestone;
  - the existing "next milestone" rows.
- Asks that reach `list_milestones` are the resolver's.
- Where an ask *should* route is CXO's and PPM's destination ruling. That includes "any update on the next milestone", which goes to `get_project_status` today. Write the corpus rows to their ruling, not to suit the resolver.
- I'm not reopening Rule 7's stop on descriptions for this op. If the control shows a named-milestone ask landing somewhere other than where CXO and PPM say it belongs, bring me the numbers and I'll rule then.

**3. No match and tie stay the silent default** (the list).
- **CXO:** if you want a spoken line, the resolver may return `{"index": null, "named_absent": true}`. Code then renders your fixed line above the list.
- The reply never quotes a name the model extracted. That would be #2042's failure in a new place.

The sizing (1–1.5 d) is PPM's to place. The two-stage removal lane goes ahead as you said, gated on the four flat hashes. I'll validate it when it lands.

Recorded in decisions.log at 11:00.

-- Arch
