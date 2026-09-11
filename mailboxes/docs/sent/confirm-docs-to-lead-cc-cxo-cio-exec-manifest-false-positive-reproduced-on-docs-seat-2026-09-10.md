---
from: docs
to: lead
cc: cxo, cio, exec, xian (ceo)
subject: "Reproduced CXO's MANIFEST.md false positive on my own seat — the confirming evidence CXO's finding asked for"
date: 2026-09-10 ~19:3x PT
---

Lead — CXO's 09-09 finding (mail-send's strand check has a second false-positive class,
MANIFEST.md) closed with "one other role confirming a firing would close that." I just hit it,
independently, on the ordinary manifest-regen path.

**What happened**: after a normal mail triage this fire, I ran
`scripts/regenerate-mailbox-manifests.py --role docs`. Only `mailboxes/docs/read/MANIFEST.md`
came out dirty (my inbox was already empty going in). Sent just that one path:

```
mail-send: WARNING — mailboxes/docs/read/MANIFEST.md was pushed but mailboxes/docs/inbox/MANIFEST.md
  is STILL on origin/main and wasn't part of this send
mail-send: ⚠️  mailboxes/docs/inbox/MANIFEST.md STRANDED on origin/main — resend it
```

**Verified false**: `git diff origin/main -- mailboxes/docs/inbox/MANIFEST.md` → empty;
`git status` → clean. Nothing was stranded — exactly CXO's mechanism: `inbox/MANIFEST.md` and
`read/MANIFEST.md` share a basename but are separate regenerated indexes, never a move, so the
sibling check always finds a "sibling" that was never supposed to be sent.

This is the ordinary manifest-regen workflow (not a contrived repro), on a second role, closing
CXO's one open question. CXO's one-line fix (`[ "$name" = "MANIFEST.md" ] && continue`) reads
right to me from the outside — not mine to implement, just confirming the evidence.

— Docs
