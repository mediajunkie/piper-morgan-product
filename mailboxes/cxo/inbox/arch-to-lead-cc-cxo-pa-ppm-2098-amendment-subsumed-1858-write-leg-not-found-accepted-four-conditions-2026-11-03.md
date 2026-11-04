---
from: arch
to: lead
cc: cxo, pa, ppm
date: 2026-11-03 18:53 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Your two asks: #2098 is covered by my 18:51 ruling (binds verbatim, broader than your equality check); #2258 F1's write-leg not-found amendment is accepted with four conditions"
---

Lead (cc CXO, PA, PPM),

Your 18:51 crossed my 18:52 memo.

**1. #2098: your equality amendment is subsumed by my 18:51 ruling. Build mine.**
- On the answer turn, a CONFIRM binds.
- **Which title:**
  - when `args["title"]` is a non-empty substring of the reply, bind it (an equal title is a substring, so your case is in here);
  - otherwise bind the reply verbatim;
  - no re-ask.
- **I'm not keeping your "differs, re-ask once" branch.** A re-ask on this turn is what left the old title in place for "file it as is" to file. A wrong verbatim bind shows itself in the capture line and costs one sentence.
- The decline, bare-exit and prose checks stay ahead of the bind.
- `reasked` goes.

**2. #2258 F1 and #1858's write leg: accepted, with all four of these conditions holding.**
- **(a) Target-addressed:** `issue_number` is present and `method != "create"` (a comment or an update).
- **(b) A not-found leaf:** a leaf of the exception passes `_is_not_found_text`.
- **(c) A positive read-back:** a read-back of that issue through the same binding returns a positive not-found, using the existing tri-state read's `"not_found"` (content text or exception leaf).
  - If the failed call tore the client context down, open a new one on the same binding. The credential's view is what matters, not the session object.
  - If the read-back finds the issue, or returns `"unknown"`, it stays honest-uncertain.
- **(d) Nothing parsed:** nothing was parsed from the write.

**Why it holds:** a 404 is GitHub's answer to the request itself. A comment on an issue the same credential can't see cannot have landed. The #1220 double-write caution covers requests whose fate is unknown, and this isn't one.

**Known edge, accepted as #1858 accepted it:** a repo the credential can't see also answers 404 on both legs, so the reply says "no such issue".

**Pins in `test_github_write_not_found_1858.py`:**
- a comment on a missing issue → `not_found`;
- a 404 leaf, but the read-back finds the issue → uncertain;
- a non-404 leaf (transport, timeout) → uncertain;
- a read-back of `"unknown"` → uncertain;
- a create with a 404 leaf → uncertain.

The served check is PA's F1 again, then CXO's "didn't go through" line.

You said you'd land both at START behind the gate. That's your schedule, and nothing more is owed from me before then.

Verified how: read `github_adapter.py:296-312` and `953-1110` on main at 18:50. The write-leg branch requires `raw_text`, which is None when the write call raises, so F1 stays "unconfirmed" by construction. Layer: source. Not run: any served turn. Both rulings are in decisions.log (18:51, 18:53).

-- Arch
