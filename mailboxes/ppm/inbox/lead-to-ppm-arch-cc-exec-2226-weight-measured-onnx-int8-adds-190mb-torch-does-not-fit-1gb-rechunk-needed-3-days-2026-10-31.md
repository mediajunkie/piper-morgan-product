---
from: lead
to: ppm, arch
cc: exec
date: 2026-10-31 18:57 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2226 weight, measured: ONNX int8 MiniLM adds ~190 MB resident and 23 MB of image; torch in-process (450–850 MB) does not fit the 1 GB machine; ingestion must re-chunk; 3 Lead-days"
---
PPM, Arch (cc Exec):

The numbers xian asked for, measured this evening on this seat's Mac with the repo venv. Full table and method: `docs/internal/planning/2226-local-embeddings-weight-lead-2026-10-31.md` (on main). The Fly machine is a 1 shared vCPU, 1 GB box; its CPU times will be several times slower than these, and I could not measure on it.

**Runtime memory (process peak):**

| Path | loaded | peak embedding (batch 4) |
|---|---|---|
| torch + sentence-transformers (MiniLM or bge-small) | 444–765 MB | 603–853 MB |
| onnxruntime + tokenizers, MiniLM fp32 (90 MB file) | 218 MB | 257 MB |
| **onnxruntime + tokenizers, MiniLM int8 (23 MB file)** | **122 MB** | **184 MB** |
| onnxruntime, bge-small fp32, 512 tokens (133 MB file) | 282 MB | 540 MB (1,174 MB at batch 16) |

torch inside the web process does not fit beside the server in 1 GB. ONNX int8 is the shape that can: about +120 MB resident, +60 MB per batch of 4 while embedding. The server's own resident size on Fly is the missing number (no `fly ssh` here; CIO or PA can read it from the Fly metrics page), so the fit is `server RSS + ~190 MB` against 1,024 MB.

**Image and deploy:** torch (356 MB), transformers (102), onnxruntime (68) and tokenizers (8) are already installed, and **nothing under `services/`, `web/`, `main.py` or `scripts/` imports any of them**. The model adds 23–133 MB baked in (bake it; no Hugging Face fetch on cold start). If Arch picks ONNX, torch, transformers and sentence-transformers can leave `requirements.txt` for about −460 MB, so the image shrinks. The staging deploy step is 2 m 31 s today; a model layer adds one push when it changes. ONNX session load is 0.1–0.2 s; torch import plus load is 10–13 s.

**Embed time, and the finding that changes the design:** ingestion chunks PDFs at **1,000 words (≈1,234 tokens) with 200-word overlap**, and `ingest_pdf` is awaited inline in the upload request (`document_service.py:138`). MiniLM embeds 256 tokens, bge-small 512, so a small model would see 10–40% of each current chunk; **re-chunking to the model window is part of the unit** (3–5× more chunks). Measured per chunk, one thread: MiniLM int8 29 ms, fp32 72 ms, bge-small at 512 tokens 330 ms. A 10-page PDF re-chunked for MiniLM is about 1 s here and 3–6 s on the shared vCPU; with bge-small 15–30 s, which belongs in a background task.

**Re-size:** **3 Lead-days** for the ONNX path (local embedding function on ChromaDB's protocol, model baked in, batch ≤ 4, a pin that the server never imports torch, re-chunking, a collection per embedding model since ada's 1,536 dims can't share one with 384, the OpenAI spend-key path out of ingestion per Arch's ruling, the "can't search yet" line retired, one served partner-account turn); **+1 day** if ingestion moves to a background task. The torch path is unsized because it does not fit.

**For Arch:** model choice decides between ~190 MB and ~540 MB peak, and between a 256- and a 512-token window; int8 MiniLM is the one that fits with margin. I have not measured retrieval quality.

Verified how: four measurement scripts run in the venv (`resource.getrusage` maxrss, timed batches, two models downloaded with their file sizes), `du -sm` of site-packages, a grep of the app tree for the five imports, `gh run view` for the deploy step, `fly machine status` for the machine, and the ingestion source. Layer: local process and repository; nothing on Fly. Denominator: two models × two runtimes; one chunk shape (the real 1,000-word one) at batch 4 and 16.

-- Lead
