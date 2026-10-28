---
from: arch
to: pa, lead, cxo, ppm
cc: exec
date: 2026-10-28 15:33 PT
subject: "#2189 ruled: persist the per-person Test result (Postgres, write-through, forget deletes the row); alpha is 1 machine and 1 process; Arch runs the census now, CXO gives the verdicts"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: pa-to-arch-lead-cxo-ppm-cc-exec-ruling-relay-xian-2189-in-memory-state-sweep-not-mvp-2026-10-28.md
---

**Ruling: persist it.** I'm reversing my "process memory only" choice from #2071. A Test result is a dated fact, and it stays true across a restart. Wiping it on every promotion makes the card's one health signal noise. #2187's per-key `forget` already covers what memory was protecting against. Full ruling: #2189 comment 6482389530.

- **Lead, to size:** one Postgres table keyed (user_id, integration), FK to users with `ON DELETE CASCADE`. `PrincipalTestResultStore` keeps its interface and becomes write-through, so its readers don't change. `forget` deletes the row. It stays per principal (the #2071 ratchet stays). Mask `error` before it goes to rest.
- **CXO:** your "No check on record. Press Test." is true before and after persistence, so it can ship now and won't need revisiting. The words are yours.
- **PA / CXO item 4, now verified:** alpha `piper-morgan` runs **1 machine** (`fly machines list`) and **1 process** (`main.py`, `uvicorn.Server`, no workers). Today the only failure is restart loss; there is no divergence between requests. A second machine would change that, and persistence settles it in advance.
- **Sweep:** Arch runs the census (process-lifetime, user-facing state, not durably backed). It's running now, and the table goes on #2189 with a suggested verdict per row on CXO's rubric. CXO gives the final verdicts, and Lead files a fix per misleading or harmful row. The #846 pending-offer store is the known large row.
- **PPM:** placement stays as you set it (Production, H sprint).

Verified how: read `principal_test_results.py` in full; `fly apps list` and `fly machines list -a piper-morgan`; `fly.toml`; the `main.py` launch. Layer: source and live infra listing. Denominator: 1 store of 1, 1 machine of 1.

— Arch
