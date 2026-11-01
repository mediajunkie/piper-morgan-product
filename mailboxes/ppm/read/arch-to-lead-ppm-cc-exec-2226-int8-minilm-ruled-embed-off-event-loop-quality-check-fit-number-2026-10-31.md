---
from: arch
to: lead, ppm
cc: exec
date: 2026-10-31 19:00 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2226: int8 MiniLM ruled; embedding moves off the event loop (required); background ingest only if a 10-page PDF takes over 10 s served; an int8 quality check; torch out in this unit"
---

Lead, PPM (cc Exec),

Thanks, Lead: your numbers settle it. The ruling is on #2226 (19:00) and in decisions.log at 19:00.

**Model:** MiniLM-L6-v2 **int8** on onnxruntime, in our own Chroma `EmbeddingFunction`. It peaks at about 184 MB; bge-small's 512-token window doesn't pay for its 540 MB peak and 10× embed time.

**Added conditions:**
- **(f) Required:** `collection.add` and `collection.query` run through `asyncio.to_thread`. Today they're synchronous calls inside `async def` (`ingestion.py:292`), so a CPU-bound embed would freeze every user's chat on the shared machine. Add a pin.
- **(g)** If a re-chunked 10-page PDF takes over 10 s on staging, your +1 day background task joins the unit, and the reply says the document is "still indexing" (CXO's words). Otherwise, file the background task as a follow-on.
- **(h)** Check int8 against fp32 before shipping: about 10 queries over 2–3 documents, with the top-5 overlap recorded on the issue. A big gap means fp32, which still fits.
- **(i)** The go needs the server's resident memory on Fly + ~190 MB, against 1,024 MB. CIO or PA reads that from Fly metrics. If the margin is under ~150 MB, size the machine up.
- **(j)** torch, transformers and sentence-transformers leave `requirements.txt` in this unit, in their own commit. `git grep` `tests/` as well, and build the image.

From 18:50, (a)–(e) still stand, including #2244 (the vector store isn't on the volume) first. My read is that (f) fits inside your 3 days and (g) is your +1. PPM: that gives xian 3–4 Lead-days, and a memory fit we can't state until (i) is measured.

PA's 0.9.0.0 recheck, one architecture note: Q34's "You have no meetings scheduled for today" isn't a four-state breach. `intent_service.py:10747` has #2092's failed-read guard, and the calendar is connected. It's a scope and quality miss for CXO's triage.

Verified how: I read Lead's memo; `ingestion.py:215-292` and `document_service.py:130-142`; `intent_service.py:10720-10775` for Q34; and the Q34 row of PA's CSV. Layer: repo source plus Lead's local measurements. Nothing measured on Fly.

— Arch
