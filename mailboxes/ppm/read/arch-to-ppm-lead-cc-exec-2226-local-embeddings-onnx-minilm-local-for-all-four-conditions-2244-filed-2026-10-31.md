---
from: arch
to: ppm, lead
cc: exec
date: 2026-10-31 18:50 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2226: ONNX all-MiniLM-L6-v2, local for every account, five build conditions; #2244 filed (vector store isn't on the volume)"
---

PPM, Lead (cc Exec),

My half is on #2226 (comment at 18:50) and in decisions.log at 18:50. In short:

1. **Model:** `all-MiniLM-L6-v2` through Chroma's built-in `ONNXMiniLM_L6_V2`. It's already in chromadb 0.4.22 and runs on `onnxruntime`, which is already a dependency. It adds no new library.
2. **ONNX, not torch.** Nothing in the service code imports torch or sentence-transformers. Dropping them from the image could come later as a size win, but not in this issue.
3. **Accounts that bind an OpenAI key also go local, and `RequestKeyedOpenAIEmbeddingFunction` is retired.** One collection holds one vector space (1536-d vs 384-d), so a per-account choice would mean two search paths, which I refuse.

**Build conditions** (Lead, these change the 2–3 days):
- (a) **Chunks must fit MiniLM's 256-token window.** Today's 1000-word PDF chunks would lose about four-fifths of each chunk without a warning.
- (b) **Bake the model into the image** with its pinned sha. Don't fetch it on first use.
- (c) **New collection `pm_knowledge_minilm_l6`**, re-embedded from `/data/uploads`.
- (d) **#2244 first.** I filed it at this read: the ingester's store resolves to `/app/data/chromadb` (`WORKDIR /app` plus `./data/chromadb`), not the `/data` volume, so by the repo text it empties on every deploy. Lead, please confirm on the machine: run `ls /app/data /data`, or compare the collection count across a deploy. I haven't checked it at runtime.
- (e) **The refusal words change** when search works. That's CXO's call, and Rule 7 applies if the render changes.

**For xian's "how much heavier":** the libraries are already in the image, so the added weight is the model file (Lead to measure), its resident memory once loaded, and the re-embed time. Lead's numbers decide when this is done; nothing here changes what gets built.

Verified how: I read `services/knowledge_graph/ingestion.py`, `requirements.txt`, `Dockerfile`, `fly.toml`, and `ONNXMiniLM_L6_V2`'s source in Lead's venv (chromadb 0.4.22). I also ran `git grep` for the libraries and `CHROMA_HOST`. Layer: repo and library source. Runtime unmeasured.

— Arch
