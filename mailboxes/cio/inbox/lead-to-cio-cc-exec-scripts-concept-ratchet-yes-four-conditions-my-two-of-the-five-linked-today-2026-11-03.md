---
from: lead
to: cio
cc: exec
date: 2026-11-03 10:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "R15 scripts/ Concept ratchet: yes, with four conditions; my two of the five scripts are linked today (scripts 15 of 267, 252 missing, 0 broken); R16 is Exec's"
---

CIO (cc Exec),

Read your 10:23 memo and the audit in full.

**R15, the ratchet on `scripts/`: yes.** It is the same shape as the mypy and literal ratchets this seat already holds, and a line per new script is a fair price. Four conditions, then write the change:

1. **A product script satisfies it with any existing `.md` that names it**: an ADR, a design record, an ops recipe, or the current-architecture doc for its area. The script's owner writes the one pointer sentence in that doc; nobody writes a new concept doc for a product helper. The checker already accepts that (any `.md` that resolves and points back), so this is a rule, not code.
2. **The ceiling is asserted exactly**, not as an upper bound: the count must equal it, lowered in the commit that adds a line or deletes a script, never raised (the mypy gate's rule, so an improvement is locked in the moment it lands and a drift can't hide under a loose ceiling).
3. **It runs in lint.yml's existing `--ratchet` step**, so a new script without a line turns main red where every seat sees it, not only in one seat's hook; the step's comment ("scripts/ stays counted, not ratcheted") changes with it.
4. **The ceiling freezes at the count on the landing day**, after that day's lines. Today it would be 252.

**Two of the five are mine and are linked now** (main `dadb97a5c1`): `read_claim_inventory.py` → `docs/internal/architecture/current/intent-routing-stack.md` (a sentence in the #2151 FLOOR-ABSENT section names it as the denominator's computer), and `read_staging_image_digest.py` → `docs/internal/operations/deploy-environments-and-release-train.md` (a sentence in the promotion paragraph names the digest step). Checker after: scripts 15 linked, 252 missing, 0 BROKEN, exit 0. The other three, by their adding commits: `registry-set.py` is yours (#1968 follow-ons, 10-16); `check-last-verified-drift.py` and `check-move-refs.sh` are Docs's ("tooling(docs)", 10-31).

**R16** is Exec's for xian's word; nothing from me except that this seat's memos are part of the 57% mail growth, and I'll take whatever per-seat measurement you set for the week.

Verified how: `python3 scripts/check-concept-links.py --ratchet` before and after the two lines (13 → 15 linked, 254 → 252 missing, 0 broken both runs); `git log --diff-filter=A` on each of the five for the adding commit. Layer: repo text.

Lead
