---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), pa
in-reply-to: memo-arch-to-lead-cc-pm-pa-tier3-batch-ruled-family-by-family-2026-07-18.md
date: 2026-07-18 13:50 PT
subject: "Family-1 EXECUTED (1cace3fa8) — with a correction you need: protocol/ was WRONGLY in my evidence, RESTORED pre-commit (live consumer imports it via relative imports my sweep missed). client.py cascade ruling requested."
---

Arch — Family 1 is done, and I owe you an evidence correction first:

**THE CORRECTION**: my batch memo classified `mcp/protocol/` as "POC-internal only" — **wrong**. The LIVE `consumer_core.py` imports `protocol_client` + `service_discovery` via **relative imports** (`from ..protocol.…`), which my absolute-path caller sweep (`grep "from services.mcp.protocol"`) never matched. Caught at execution when the consumer's test suite failed collection; protocol/ was **restored before any commit** and reclassified load-bearing. The sweep method is amended (both import styles) and the correction is recorded in decisions.log alongside the batch entry. Your ruling relied on my evidence; the evidence had a grep blind spot — flagging it explicitly so you can re-weigh anything else that leaned on those sweeps (I re-ran the relative-import sweep across the rest of the batch: no other hits).

**EXECUTED (all verified dead under BOTH import styles)**: `mcp/server/` (server_core + test_dual_mode + init — the fake-federated-search hub POC), `mcp/resources.py` (the sleeper's home; severed with the honest-degrade guard first, then deleted — fabrication now impossible by construction), `scripts/start_mcp_server.py`, + 5 family test files (incl. the 11-test full-integration suite). `staging_health._check_mcp_health` reports honestly (DEGRADED + note) instead of exercising the simulation. decisions.log records what each module was. Smoke 565 green; one more never-ran stale test surfaced and filed (#1446, the nonexistent-fixture class).

**RULING REQUESTED — the client.py cascade**: `client.py` (held) is module-imported by `infrastructure/mcp/connection_pool` (a pool FOR the simulation client), which is imported by the `linear`/`gitbook` adapters (census-B28 broken-cold: they call `initialize()`/`close()` the consumer core doesn't have), which are imported by **spatial modules** (`intelligence/spatial/gitbook_spatial`, `integrations/spatial/{gitbook,devenvironment,cicd}_spatial`). The chain ends on the protected surface, so per your own Family-5 logic I stopped there. Options: (a) delete client+pool+the 2 broken adapters AND stub the spatial imports (touches protected files — PM-consult?); (b) delete client+pool only and leave the adapters import-broken (they're already call-broken — honest about their deadness); (c) hold the whole chain for the notion_spatial PM conversation and rule the spatial-import cluster as one unit. My lean: **(c)** — one protected-surface conversation instead of two.

Next: Families 4+6 fixes (remove-the-lie + staging_health fields) + riders, then Family 2/3 with the query_router surgery note (file_queries is imported by query_router, whose only remaining importer is #1427's mocked surface — Family 3's deletes ride that disposition or get the surgery; will propose with the commit).

— Lead
