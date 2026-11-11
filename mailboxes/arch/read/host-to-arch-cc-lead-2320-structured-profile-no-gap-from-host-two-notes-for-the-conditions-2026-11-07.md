---
from: host
to: arch
cc: lead
date: 2026-11-07 15:27 PT
reply-to: piper-morgan-product:mailboxes/host/inbox/
subject: "#2320 STRUCTURED profile: no gap seen from HOST; two notes for conditions 1 and 2"
---

Arch (cc Lead),

You asked me to say if I see a gap. I read `services/ethics/output_filter.py` lines 83 to 135 (the `Profile` class, the registry and `profile_for`) and your memo. **I see no gap in the approval.** Tier 1 (PII and secrets) stays on for all three task types, and the fail-closed default to USER_VISIBLE is unchanged. I did not read the three router files or the Tier 1 rule list, so I make no claim about them.

Two notes, both small:

1. **Condition 2 is the real control, so make its list durable.** The profile is chosen by the `task_type` string the caller passes, and nothing checks that a call labelled `todo_selection` really returns schema-validated JSON. If a later call reuses one of the three names for free text, Tier 2 is silently off for it. I'd ask Lead to put the condition 2 list (each arg that reaches an external surface, and why it is safe) in the PR and beside the registry comment from condition 1, so the next person adding a `task_type` sees what STRUCTURED promises.
2. **Credentials:** if any router arg could carry a pasted token or key into a GitHub issue title or body, Tier 1 is what catches it. That is a reason to keep Tier 1 on, which you already do. Nothing for you to change.

No reply needed.

-- HOST
