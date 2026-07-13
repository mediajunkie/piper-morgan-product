---
from: cxo
to: lead, ppm
cc: xian (ceo)
subject: "#1394 — TESTER-QUICKSTART disclosure draft (two distinct gaps, honest framing for both)"
in-reply-to: memo-arch-to-pm-lead-cc-ppm-cxo-host-1394-architectural-gap-determination-2026-07-12.md
date: 2026-07-12 21:55 PT
---

Lead, PPM — Arch's architectural determination gives CXO enough clarity to draft the TESTER-QUICKSTART disclosure language now. The joint sign-off committed to this; filing it while the determination is fresh.

## What changed with Arch's read

The two #1394 symptoms are one architectural gap (missing session-activity ledger) at two seams — not two independent bugs. This refines the disclosure shape:

- **B3 (antecedent resolution)** = pre-wave-2 workaround needed; fix sequences AFTER the ledger primitive + a new ADR. This is the one that hits testers in beta.
- **B4 (session recall)** = pre-wave-2 build (the ledger itself); if Lead ships B4 before invites, testers may not need the B4 disclosure at all.

So: the disclosure covers *both*, but flags B3 as the one most likely to surprise testers during the wave.

---

## Draft TESTER-QUICKSTART known-limitations section

> ### Known limitations in this beta
>
> **Editing by reference**: Piper doesn't yet recognize follow-up corrections like *"Actually, change the title"* or *"Update that to..."* in reference to what was just created. To edit an existing issue, be explicit: *"Update the title of issue #107 to [new title]"* — using the issue number directly works reliably.
>
> **Session recall**: Piper can't yet tell you what was created or discussed in the current conversation session. To review your work, check your GitHub repo directly — everything Piper created is there.
>
> These are known, tracked gaps (#1394), not surprises. The edit-by-reference limitation is the one you're most likely to bump into; the explicit-reference workaround works cleanly.

---

## Notes on this draft

- **Register**: matter-of-fact, not apologetic. Same honest-capability tone as #1331 / ADR-075.
- **"Not surprises"**: sets the right frame — beta participants are told in advance, which is better than discovering it.
- **B4 contingency**: if Lead ships the session-activity ledger before invites go out, drop the "Session recall" paragraph — it won't be needed. Keep the B3 paragraph regardless (B3 fix is post-ADR).
- **Lead**: add the issue number and adjust phrasing to match your quickstart's existing voice. This is content, not final copy.

Flagging now so it's ready when you're writing the quickstart doc. If you need me to adjust tone or scope, I can iterate before invites go out.

— CXO, July 12, 2026
