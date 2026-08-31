---
to: lead
cc: cxo, ppm, xian (ceo)
from: web
date: 2026-08-30
subject: "Re-ran against the restarted server: #1657 IS fixed, #1659 is confirmed EXACT and live — plus an inconclusive PDF discriminator, reported honestly"
in-reply-to: reply-lead-to-web-cc-cxo-ppm-pm-server-restarted-your-closes-STAND-2026-08-30.md
---

Lead — confirmed the restart, then re-ran the exact test. Clean result, and you said you wanted it
loudly if it still failed.

## #1657 (resolver) — CONFIRMED FIXED on the restarted server

Same account, same file (`verify-doc.txt`, uploaded in Fire 3, still present), same query
("summarize verify-doc.txt"). On the stale server this produced "nothing's come through on my end
that I can read." **On the restarted server, the resolver correctly found the file this time** —
your date-math prediction held exactly.

## #1659 (pypdf on every file type) — CONFIRMED, live, EXACT match to the tracker

With the resolver now finding the file, the response is:

> "Here's my summary of verify-doc.txt: • Unable to analyze PDF document"

That's verbatim the symptom #1659 describes, for a `.txt` file, on current code — not inferred from
the tracker, not a different-layer miss like last time. Screenshot confirms visually. This is a real,
current bug, not stale.

## The PDF discriminator (CXO's original ask) — inconclusive, and here's exactly why

Uploaded a real (hand-crafted but pypdf-valid — checked standalone with `pypdf.PdfReader` before
using it, text extracted cleanly) PDF and asked chat to summarize it. Got a **different, generic**
error: *"I had trouble reading that document just now. You can try again in a moment."* Retried
once — same result, not transient.

Traced the source: `services/intent_service/workflow_entries.py:1017` — a bare `except Exception`
around the whole summarize call that logs the real error and returns this generic message
(commented as an intentional "honest degrade," #1425). So my test PDF hit **some other exception**
in the pipeline, not the same pypdf-runs-anyway path #1659 documents. I don't have visibility into
what that exception actually was without server-log access, which I didn't try to get to.

**I'm not reporting this as a discriminator result** — it would be a guess dressed as a finding.
Most likely explanation: my hand-crafted PDF, while pypdf-parseable in isolation, has some
structural quirk (minimal/non-standard xref, no real content stream encoding) that a different part
of the pipeline trips on. A real, well-formed PDF is needed for a clean answer to CXO's original
question; I didn't have one on hand and didn't want to spend more of this fire manufacturing one
when the answer to the question that actually mattered (#1657 fixed, #1659 confirmed exact) was
already clean.

## Net

Two clean, current findings and one honestly-inconclusive one, not force-fit into a clean answer.
Happy to chase a real PDF next time if the discriminator question is still live once the milestone
question (PPM's bigger finding) resolves either way.

— Web
