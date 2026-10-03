# Unobservables (running list)

| # | What can't be observed | Why | How to observe instead | Added by |
|---|---|---|---|---|
| U1 | All LLM-backed behavior: intent classification, chat responses, synthesis | No LLM key in the container | Add a spend-capped test `ANTHROPIC_API_KEY` env var, or human testing on alpha | Phase 0 |
| U2 | Credential storage and integration OAuth flows | No `ENCRYPTION_MASTER_KEY`, no provider OAuth apps | Test env vars plus sandbox OAuth apps; or human test on alpha | Phase 0 |
| U3 | ChromaDB, Temporal, GitHub MCP sidecar paths | Docker Hub rate-limited (429) | Retry pulls later or use a mirror; or a local session | Phase 0 |
| U4 | Live alpha (Fly) behavior and real user activity | Out of scope for a read-only review without credentials | PM/Lead to share read-only metrics, or a human walk-through | Phase 0 |
| U5 | Cowork scheduled jobs on PM's machine | Not stored in the repo | Exec or PM supplies an inventory | Plan v0.4 (H1b) |
