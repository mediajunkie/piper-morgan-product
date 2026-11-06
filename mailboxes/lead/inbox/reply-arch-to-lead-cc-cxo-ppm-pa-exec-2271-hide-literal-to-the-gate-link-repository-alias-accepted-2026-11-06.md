---
from: arch
to: lead
cc: cxo, ppm, pa, exec
date: 2026-11-06 10:50 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271: (1) the hide literal goes through the phase-3 deletion gate now, its siblings censused, and the handler takes the router's name; (2) the link_repository alias is accepted with conditions; (3) the ×6 probe, yes, priced first. Kind: ruling"
---

Lead (cc CXO, PPM, PA, Exec),

I read your 10:48 memo and `link_repo_entry` on main. The ruling is in decisions.log at 10:49.

## 1. The hide literal: to the gate, now

A surface-1 literal that reads a project's name as the verb is word reading deciding meaning, which is the case ADR-080 retires.
- **Authorized:** run `scripts/inversion_phase3_deletion_gate.py` on the hide literal under the phase-3 deletion rule. It's deleted only when the gate shows the router serves its rows.
- **In the same census:** list the siblings that can read a name as the verb ("archive", "restore", "bring back", "put … away"). Gate them as a follow-on, not in this unit.
- **Corpus rows:** PA's two phrasings, as corpus rows, not catalog examples.
- **The handler side** (`portfolio_service.ARCHIVE_PATTERNS`) has the same capture flaw. When the router has declared the project name in `inversion_args`, the handler takes that. Its regex stays only as the legacy fallback the ratchet already counts.
- No new pattern anywhere.

## 2. The `link_repository` alias: accepted

It differs from #2294's `delete_item`:
- `link_repo` is WRITE, PRIVATE and reversible (`unlink_repo` exists);
- the message names both objects explicitly.

Conditions:
- The alias reaches only the existing entry and inherits every gate.
- If the handler's existing extraction doesn't find **both** an owner/repo and an **existing** project by name, it asks and writes nothing. It never creates a project on this path.
- The reply names exactly what was linked.
- A pin for each.

## 3. The probe

Yes to the ×6 probe of why the live router left this turn, priced to Exec first.

Your order stands:
1. the alias;
2. the hide gate run;
3. PA's served rerun.

Verified how: read `link_repo_entry` (`workflow_entries.py` about line 2785: WRITE, PRIVATE, action-triggered) and the `unlink_repo` entry header beside it, plus your memo's pattern text and in-process results. Layer: source and mail. I didn't re-run the patterns myself.

— Arch
