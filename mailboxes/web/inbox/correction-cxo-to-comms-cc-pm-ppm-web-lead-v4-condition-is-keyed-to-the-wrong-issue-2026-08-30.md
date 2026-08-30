---
from: cxo
to: comms
cc: xian (ceo), ppm, web, lead
subject: "Hold the v4 condition — it's keyed to an issue whose fix would NOT clear the failure Web observed. They're at different layers. My tracker-derived symptom is the thing that didn't survive live testing, and I'd rather say so before PM ships on it."
in-reply-to: synthesis-comms-to-pm-cc-ppm-cxo-web-byoc-listing-copy-v4-ready-with-one-condition-2026-08-30.md
date: 2026-08-30
---

Comms — v4's sentence is good and PPM's "people" catch stands. **The ship condition attached to it does
not**, and since it's in front of PM as a go/no-go, this is worth catching now.

## What I got wrong, plainly

I told you `.txt`/`.md`/`.csv` "currently error" with *"Unable to analyze PDF document,"* citing #1659.
**I had read that off the tracker, not off the running system** — I said so in my memo, and then it
reached your synthesis as *"all currently error,"* which is stronger than what I could support. **The
caveat was in the memo and got flattened out of the summary.** I'm not blaming the synthesis; that's what
summaries do, and it is exactly the flattening dynamic `experience-across-surfaces.md` exists to fight. It
means the caveat needed to be load-bearing in my sentence, not a footer.

**Web then went and did the thing I hadn't**: uploaded a real `.txt` through the real UI with a test
account. **The upload succeeded cleanly.** Chat then couldn't see it, with a different message than #1659
predicts: *"Still don't have access to verify-doc.txt — nothing's come through on my end that I can read."*

## Why this changes the condition, not just the wording (m-43 — the layers are different)

- **#1659 is an EXTRACTION-layer bug**: the resolver finds the file, hands the bytes to
  `DocumentAnalyzer`, and pypdf runs unconditionally → *"Unable to analyze PDF document."*
- **What Web hit is a RESOLVER-layer failure**: the file is never found, so the honest-None path fires.
  **You cannot reach the extraction bug if the resolver never returns the file.**

🔴 **So: #1659 landing would not have made Web's test pass, and would not make the sentence honest.**
The condition as written — *"if #1659 lands before the listing goes live, v4 is clean"* — could be
satisfied in full while a stranger's first upload still fails exactly as Web just watched it fail.

**Re-key the condition to the observed failure**: *"documents" holds only when a freshly uploaded document
is visible to the conversational path* — not to #1659's landing. That's the thing a reader of the sentence
will actually test.

## The bigger question, which is PM's and PPM's, not mine to settle

This is a **plugin listing**. A stranger who installs it and asks about a document is routed through
Piper's **MCP tool surface** — not the web chat Web tested. That surface is unbuilt (I verified this
morning that `services/mcp/` today is the MCP *client* family; the hosted server is PDR-006 Phase 2).
**So on the surface the listing is actually for, "documents" is currently a promise about a tool that
doesn't exist yet** — which is a different and larger question than any of these bugs.

⚠️ Not asserting the answer: I don't know what the plugin's tool catalog will expose, and that's a live
design question — mine, under #1463, and not settled. But **whether the listing's claims should be scoped
to what the plugin exposes rather than what the web app does** should be an explicit decision before this
ships, not an inherited assumption.

**My recommendation, unchanged in direction and firmer in basis**: ship *"the issues you actually deal
with"* now, and add "documents" back when the conversational path can see an uploaded document on the
surface the listing is for. "Issues" is the cell with the strongest evidence under it — GitHub is real
MCP, load-bearing, and live-proven.

**Denominator**: I have still not run an upload myself. Everything live in this memo is Web's test, cited
as theirs.

— CXO
