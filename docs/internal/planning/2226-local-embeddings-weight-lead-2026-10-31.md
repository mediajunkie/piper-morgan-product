# #2226: how much heavier is Piper with a local embedding model? (Lead, 2026-10-31)

Asked by PPM 18:47 (xian, decisions.log 10-31 18:46: embeddings computed inside Piper; the operator-funded OpenAI key is off the table). Arch owns the model choice and ONNX vs torch; these are the measurements that choice needs. Everything below was measured on the Lead seat's Mac (Apple Silicon, Python 3.11.15, the repo venv). **The Fly machine is a `shared-cpu-1x` with 1 GB** (`fly.toml`, `fly machine status`: 1 shared vCPU, 1024 MB); its per-chunk times will be several times slower than these, and I did not measure them there. Memory is process `maxrss` (peak resident set), which is the number that matters against a 1 GB cap.

## 1. Runtime memory

| Path | Imports only | Model loaded | Peak while embedding | Notes |
|---|---|---|---|---|
| torch + sentence-transformers, all-MiniLM-L6-v2 | 415 MB | 765 MB | 853 MB (batch 16) | first-run figures incl. download machinery |
| torch + sentence-transformers, bge-small-en-v1.5 | 415 MB | 444 MB | 603 MB (batch 4, 512 tokens) | steady-state torch figure |
| **onnxruntime + tokenizers, MiniLM fp32** (`onnx/model.onnx`, 90 MB) | 50 MB | 218 MB | 257 MB (batch 4) / 457 MB (batch 16) | 1 intra-op thread |
| **onnxruntime + tokenizers, MiniLM int8** (`onnx/model_quint8_avx2.onnx`, 23 MB) | 50 MB | 122 MB | **184 MB (batch 4)** / 369 MB (batch 16) | 1 thread |
| onnxruntime, bge-small fp32 (133 MB, 512 tokens) | 50 MB | 282 MB | 540 MB (batch 4) / **1,174 MB (batch 16)** | batch 16 alone exceeds the machine |

Reading: **torch in the web process is 450–850 MB on its own and does not fit beside the server in 1 GB.** The ONNX int8 path adds roughly 120 MB resident plus 60 MB per batch of 4 at embed time. The server's own resident size on the Fly machine is **unmeasured by me** (no `fly ssh` on this seat; CIO or PA can read it from the Fly metrics page); the fit question is `server RSS + ~190 MB` against 1,024 MB with the OS's share taken out. Batch size is the lever on the peak; keep it at 4 or lower on that machine.

## 2. Image size and deploy time

- Already in the image today (Dockerfile lines 43–44 install the CPU torch wheel and `requirements.txt`): on disk in the venv, `torch` 356 MB, `transformers` 102 MB, `onnxruntime` 68 MB, `numpy` 60 MB, `tokenizers` 8 MB, `sentence_transformers` 3 MB. **No file under `services/`, `web/`, `main.py` or `scripts/` imports torch, transformers, sentence_transformers, onnxruntime or tokenizers** (grep this turn). So today's image carries ~530 MB of libraries nothing runs.
- Added by a local model, baked into the image: **23 MB** (MiniLM int8), 91 MB (MiniLM fp32), 133 MB (bge-small). Bake it in (a layer before `COPY . .`, cached across builds); a runtime download from Hugging Face would put a 23–133 MB fetch and HF availability on every cold start.
- If Arch picks ONNX, `torch`, `transformers` and `sentence-transformers` can leave `requirements.txt`: **about −460 MB on disk**, so the image gets smaller, not larger. If torch stays, the delta is the model file only.
- Deploy time today: the "Deploy main to piper-morgan-staging" step took 2 m 31 s (run 41249007456, 22:39:07Z → 22:41:38Z). A 23–133 MB layer adds its registry push once when it changes (tens of seconds), nothing per deploy afterwards.
- Cold start: an ONNX session loads in 0.1–0.2 s; torch import plus model load took 10–13 s here (and `sentence_transformers` alone imported in 2.8–27 s depending on the OS cache), inside a 30 s health-check grace period.

## 3. Embed time per typical document

- Ingestion today (`services/knowledge_graph/ingestion.py:312–335`): PDF text split into **1,000-word chunks with 200-word overlap**, embedded by `text-embedding-ada-002` through ChromaDB; `ingest_pdf` is awaited inline by `document_service.py:138`, so embed time lands in the upload request.
- **A 1,000-word chunk is about 1,234 word-piece tokens.** all-MiniLM-L6-v2 embeds at most 256 tokens (its `tokenizer.json` even defaults to 128); bge-small 512. A local small model therefore sees only the first 10–40% of each current chunk. **Re-chunking to the model's window is part of the unit** (≈200 words for a 256-token model, ≈400 for 512), which multiplies chunk count by 3–5×.
- Measured, local, 1 thread for ONNX: MiniLM int8 **29 ms/chunk**, MiniLM fp32 72 ms, bge-small fp32 at 512 tokens 330 ms; torch bge-small (multi-thread) 41 ms; MiniLM single-query latency 16–26 ms.
- Typical document = a 10-page PDF ≈ 5,000 words: today 6 chunks; re-chunked for MiniLM ≈ 30 chunks → **≈1 s local, call it 3–6 s on the shared vCPU**; for bge-small at 512 tokens ≈ 15 chunks → ≈5 s local, 15–30 s on Fly. A 50-page PDF is five times that. So with bge-small, or any document over a few dozen pages, ingestion should move off the request (a background task with the honest "indexing" reply), which is new work.

## 4. Re-size of the 2–3 days

**3 Lead-days for the ONNX path** (was 2–3): a `LocalEmbeddingFunction` on ChromaDB's protocol (onnxruntime + tokenizers, model baked into the image, batch ≤ 4, the server never imports torch, pinned); re-chunking to the model window; **a collection per embedding model** (ada's 1,536 dims and MiniLM's 384 cannot share a collection, so existing OpenAI-embedded documents are re-embedded on their next upload or by a one-off re-index, which on partner accounts is a handful of files); the `request_spend_key("openai")` path removed from ingestion (Arch's call for accounts that bind an OpenAI key); the search reply's "can't search yet" line retired; a served turn on a partner account for the acceptance row. **+1 day if ingestion moves to a background task** (bge-small, or documents past a few dozen pages). The torch path is not sized: it does not fit the machine.

## Verified how

Scripts in the Lead scratchpad (`emb-torch.py`, `emb-onnx.py`, `emb-onnx2.py`, `emb-bge.py`), each run this evening in the repo venv with the Anthropic env stripped; `resource.getrusage` maxrss; `huggingface_hub` downloads of the two models' files with their on-disk sizes; `du -sm` of the venv's site-packages; `grep` of the app tree for the five imports; `gh run view` for the deploy step timing; `fly machine status` for the machine size; the ingestion source for chunking and the inline await. Layer: local process measurements and repository facts. Not measured: anything on the Fly machine (server RSS, CPU speed), and the models' retrieval quality, which is Arch's choice to make.

## Addendum 19:0x: Arch's pick, Chroma's built-in `ONNXMiniLM_L6_V2`, measured as it ships

Arch (18:50) picked `all-MiniLM-L6-v2` through chromadb 0.4.22's built-in `ONNXMiniLM_L6_V2` (onnxruntime, already a dependency). Its source: it downloads `onnx.tar.gz` (model.onnx 90.4 MB, tokenizer, vocab; 168 MB in `~/.cache/chroma/onnx_models` after extraction) from an S3 URL with a pinned sha256 on first use, truncates and pads to 256 tokens, batches 32 at a time, and passes no session options. Measured, cache warm, fresh process each, 50 chunks of 200 words (256 tokens padded), process maxrss:

| Configuration | loaded | peak | ms/chunk |
|---|---|---|---|
| **default on this Mac: CoreML execution provider** | 850 MB | **9,811 MB** | 71 |
| CPU provider, default threads (10 cpus), batch 32 (the class default) | 274 MB | 578 MB | 17 |
| CPU provider, 1 thread, batch 32 | 274 MB | 579 MB | 77 |
| CPU provider, 1 thread, **batch 4** | 283 MB | **302 MB** | 72 |

Readings. (1) The first row is a developer-machine hazard, not a Fly one: onnxruntime on macOS picks the CoreML provider by default, and the class ran at 9.8 GB on a laptop; pass `preferred_providers=["CPUExecutionProvider"]` (the constructor takes it) so dev runs and tests behave like Linux. (2) On the CPU provider, which is all Fly has, the class costs **about 275 MB loaded (chromadb imported too) and 580 MB peak at its default batch of 32, or 300 MB peak at batch 4**; the batch size is fixed at 32 inside `_forward`, so the build must call `_forward(..., batch_size=4)` or subclass. (3) Per chunk at one thread it is 72–77 ms with 256-token padding, the same as the unpadded run; the 17 ms figure uses ten cores the Fly machine does not have. (4) A 10-page PDF re-chunked to 200 words (≈30 chunks) is about 2.3 s at one thread here, so several seconds on the shared vCPU, inside the upload request as the code stands. Two conditions to add to Arch's five: the CPU provider named explicitly, and the batch capped at 4 (or a measured 8) on the 1 GB machine.

**#2244 (Arch's condition d):** this seat cannot run `fly ssh`, so the runtime confirmation (`ls /app/data /data` on the web machine, and the collection count across a deploy) is PA's or CIO's. The repo text reads the same to me: `DocumentIngester(chroma_path="./data/chromadb")` with no caller passing a path, `WORKDIR /app`, volume at `/data` used only by `UPLOAD_DIR`. Size of #2244 itself: half a day (a `CHROMA_PATH` setting defaulting to `/data/chromadb` under Fly and `./data/chromadb` locally, the setup check reporting it, a deploy-spanning served count).
