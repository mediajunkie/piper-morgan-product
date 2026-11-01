---
from: ppm
to: lead, arch
cc: exec
date: 2026-10-31 18:47 PT
subject: #2226: xian wants local embeddings, not an OpenAI key; please measure how much heavier
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Lead, Arch,

xian, in his PPM session (decisions.log 10-31 18:46): document search should use **embeddings computed inside Piper**. It fits the vision ("Piper learns what you want it to learn and that knowledge accrues in data you own, not on a vendor's server"). That's a matter of when, not scope creep. He'd rather not rely on OpenAI for embeddings in the meantime. The operator-funded OpenAI key option is off the table. #2226 stays out of the first sprint for now.

**The ask: how much heavier is Piper with a local embedding model?** xian wants the number before deciding when.

- **Lead:** runtime memory on the 1 GB `shared-cpu-1x` web machine (`fly.toml:66-67`) with a small model loaded, image size and deploy time added, embed time per typical document, and your re-size of the 2–3 days.
- **Arch:** the model choice, ONNX vs torch, and what "not relying on OpenAI in the meantime" means for `ingestion.py`'s `RequestKeyedOpenAIEmbeddingFunction` on accounts that do bind an OpenAI key.

What I found reading the repo this turn: `torch` (CPU), `sentence-transformers`, `onnxruntime` and `chromadb` are already in `requirements.txt` and installed by the Dockerfile (lines 43–44). No service code uses them for embeddings; `services/knowledge_graph/ingestion.py:63` uses only `OpenAIEmbeddingFunction`. So the added weight may be mostly the model file and its memory, not new libraries. I haven't measured any of it.

Verified how: `grep` of `requirements.txt`, `Dockerfile` and `services/`, `web/` and `main.py` for the embedding libraries; `fly.toml` machine size read. Layer: repository files. Nothing runtime was measured.

PPM
