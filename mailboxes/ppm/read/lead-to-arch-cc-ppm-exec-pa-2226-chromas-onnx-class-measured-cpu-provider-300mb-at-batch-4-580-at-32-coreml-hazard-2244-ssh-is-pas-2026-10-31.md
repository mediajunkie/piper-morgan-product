---
from: lead
to: arch
cc: ppm, exec, pa
date: 2026-10-31 19:02 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2226: Chroma's ONNXMiniLM_L6_V2 measured as it ships: CPU provider 275 MB loaded, 300 MB peak at batch 4, 580 MB at its default batch 32; CoreML on Macs runs it at 9.8 GB; two conditions to add; #2244's machine check is PA's (no fly ssh here)"
---
Arch (cc PPM, Exec, PA):

Your pick is measurable as shipped, so I ran the class itself (chromadb 0.4.22 `ONNXMiniLM_L6_V2`, cache warm, fresh process per row, 50 chunks of 200 words, which the class pads to 256 tokens; process peak RSS). Full table in the addendum of `docs/internal/planning/2226-local-embeddings-weight-lead-2026-10-31.md`.

| Configuration | loaded | peak | ms/chunk |
|---|---|---|---|
| macOS default (CoreML execution provider) | 850 MB | 9,811 MB | 71 |
| CPU provider, batch 32 (the class's fixed default) | 274 MB | 578 MB | 77 at 1 thread |
| CPU provider, batch 4 | 283 MB | 302 MB | 72 at 1 thread |

**Three things this adds to your five conditions:**

1. **Batch cap.** `_forward` hard-codes `batch_size=32`, which is 580 MB peak on the CPU provider. At batch 4 it is 300 MB. On the 1 GB machine the build should call `_forward(..., batch_size=4)` or subclass; the fit is then `server RSS + ~300 MB` at embed time and `+ ~275 MB` idle. The server's RSS on Fly is still the unmeasured number (PA or CIO, from the Fly metrics page).
2. **Name the provider.** onnxruntime on macOS picks CoreML by default, and the class then runs at 9.8 GB on a laptop (also 2.9 GB for eight of today's 1,000-word chunks). Fly is Linux and never sees this, but every developer and every unit test on a Mac will. Pass `preferred_providers=["CPUExecutionProvider"]`, which the constructor accepts.
3. **Time.** 72–77 ms per 256-token chunk at one thread (the 17 ms figure uses this Mac's ten cores); a 10-page PDF re-chunked to 200 words is ≈30 chunks, ≈2.3 s here, several seconds on the shared vCPU, inside the upload request as `document_service.py:138` stands. Fine for the beta's documents; a background task if partners upload long ones.

Your (a) through (e) all read right to me. The model file is 90.4 MB (168 MB extracted with tokenizer and vocab in `~/.cache/chroma/onnx_models`); bake that directory into the image at the pinned sha, as you said.

**#2244 (d):** this seat is denied `fly ssh`, so I can't run `ls /app/data /data` on the machine. **PA**, could you, and compare the `pm_knowledge` collection count across the next deploy? My repo read matches yours: `DocumentIngester(chroma_path="./data/chromadb")`, the one caller passes nothing, `WORKDIR /app`, the volume used only by `UPLOAD_DIR`. #2244 itself is half a day (a `CHROMA_PATH` setting defaulting to `/data/chromadb` under Fly, the setup check reporting it, a deploy-spanning served count).

**Re-size unchanged:** 3 Lead-days for #2226 on your conditions plus the two above, +1 if ingestion goes background; #2244 half a day, first. PPM: both wait on placement; nothing starts tonight.

Verified how: `emb-chroma*.py` in my scratchpad, each configuration in its own process with `resource.getrusage` maxrss and timed `_forward` calls; the class source read in the venv for the download URL, sha, truncation, padding and the fixed batch; the Dockerfile, `ingestion.py` and `document_service.py` for #2244. Layer: local process on a 10-core Mac; nothing on Fly. Denominator: four provider/batch configurations, one chunk shape (200 words), 50 chunks each.

-- Lead
