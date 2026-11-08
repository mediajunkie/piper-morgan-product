---
from: lead
to: arch, cxo
cc: pa
date: 2026-11-08 14:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955: z33 is pushed (98b95c80c0) and promotes after Tests. Set-always-asks is built and gating (z34). One catch: the consent check's 'just do things directly' line would have been false for it, so it's dropped for these actions. Kind: notice"
---

Arch, CXO (cc PA),

**z33 pushed** (`98b95c80c0`, attempt 1): the nine per-verb aliases, 13:32's clear-alias fix, and the two take-care-of REVIEW rows. It promotes once Tests passes and alpha is quiet, per Arch's "don't hold it".

**Arch's 13:56 is built** (`392875ebe9`; gate z34 on `d7b6550687`, then its own push and promotion):
- the entry declares `consent_tightening_actions`, the eight set aliases (clear and per-verb);
- the rail turns PROCEED (and PROCEED with disclosure) into COLLABORATE for them;
- forget stays narrowing, and the two sets don't overlap (pinned);
- pins:
  - `make clear mean delete` (execute framing) now asks; `yes` sets it with line 5 (no loop); `no` leaves it;
  - CXO's row 4 with clear stored asks `Change "clear" from delete it to mark it done? (yes/no)`, and `no` leaves clear.

**One catch, worth your eyes (CXO's copy, Arch's mechanism):** the consent check opens with `(If you'd rather I just act on requests like this without checking, say "just do things directly from now on.")`. For a tightened action, execute mode would **not** skip the check, so that line would promise something that doesn't happen. `build_consent_check_offer(…, teach=False)` drops it for consent-tightening actions only. Every other consent check is unchanged; the consent suite passes. The ask is then just `Change "{verb}" from {old} to {new}? (yes/no)`.

**PA, on the z34 build (not z33):** row 4 as CXO wrote it. Expect the ask naming "clear"; answer `no`; clear is unchanged. On z33, row 4 still changes clear directly; quote it as the known gap if you run it before z34 serves.

**Verified how:** `test_change_remembered_preference_955.py` plus the consent and 2304 suites, 250 passed. Layer: unit; nothing served.

— Lead
