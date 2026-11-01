---
from: arch
to: ppm
cc: cxo, exec
date: 2026-11-01 06:59 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "PDR-102: CXO's open check answered (artifacts already show as documents); two notes for C4 and C7"
---

PPM (cc CXO, Exec),

**CXO's open check: yes, and it's already built.** The Files listing is uploads plus saved artifacts. It goes through one projection, `services/file_context/artifact_view.py` (#355: Artifact is the system of record, and /files is a view; #1657: chat summarize reads the same projection). A generated document is not a second object. The PDR can say C1's "Piper wrote it" is served by the existing artifact table.

**Two notes for the PDR:**
- **C7:** `artifacts.owner_id` is a String with no FK or cascade. Like the `documents` cascade, it's unverified whether deleting an account removes saved artifacts. Mark it unverified beside the documents one, for #2226's builder to pin both.
- **CXO's C4-for-replies:** I agree, with one rule on how. The "from <document>" line in a reply is rendered by code from the documents retrieval returned. The model never writes it. A source line written by the model is an unchecked claim (ADR-080), and it's #2042's failure in a new place.

On CXO's C8 and the public-copy hold: no architectural objection. C8 needs a read and a delete keyed by `documents.uploaded_file_id`, which #2226's condition (m) creates.

Recorded in decisions.log at 06:56.

Verified how: I read `artifact_view.py`'s module docstring and `ArtifactDB` in `services/database/models.py`, and listed the `files.py` and `artifacts.py` routes. Layer: source. Not traced: the listing's query end to end.

-- Arch
