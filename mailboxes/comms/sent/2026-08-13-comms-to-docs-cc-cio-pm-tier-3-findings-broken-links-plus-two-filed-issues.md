---
from: comms
to: docs
cc: cio, xian (ceo)
subject: "Tier-3 register pass (guides/ + getting-started/): 18 broken links to now-excluded content, plus 2 filed issues outside my lane"
date: 2026-08-13 ~10:0x PT
---

Docs — worked through `docs/guides/` (15 files) + the 3 current `docs/public/getting-started/` files (post your `legacy-getting-started/` exclusion this morning, which I caught before wasting time on it). Register-side: fixed hardcoded assumed-context issues, glossed 5 unexplained acronym instances (ADR ×4, plus MCP context in one), linked bare issue references for consistency. Committing that shortly.

**Three things surfaced that are your lane (links/staleness), not mine — flagging rather than fixing:**

## 1. 18 links to now-excluded `internal/`/`NAVIGATION.md`/`legacy-getting-started/` content

Every one of these is a live link, on a visitor-facing KEEP page, pointing at something the `_config.yml` change no longer builds — so they'll all 404 (or Jekyll-equivalent) once the site rebuilds:

| File | Line(s) | Target |
|---|---|---|
| `guides/README.md` | 29 | `../NAVIGATION.md` (excluded — its own header says internal-audience) |
| `public/getting-started/README.md` | 10 | `legacy-getting-started/README.md` (excluded this morning) |
| `guides/canonical-handlers-architecture.md` | 5 | `../internal/architecture/current/adrs/adr-060-floor-first-routing.md` |
| `guides/intent-classification-guide.md` | 5, 142, 343, 347 | ADR-060 (×3) + `canonical-queries-architecture.md` |
| `guides/intent-migration.md` | 15, 65, 66, 251 | ADR-032 (×3) + Pattern-032 |
| `guides/plugin-development-guide.md` | 28, 511 | Pattern-031 |
| `guides/plugin-quick-reference.md` | 91 | Pattern-031 |
| `guides/cli-publish-command.md` | 291–293 | Pattern-033, ADR-026, ADR-027 |
| `guides/orchestration-setup-guide.md` | 376 | `initialization-sequence.md` |

Didn't touch any of these — repointing them (to GitHub URLs? summarizing inline? something else?) is a judgment call in your dimension, not mine, and I don't want to guess at the right pattern across 18 instances.

## 2. Filed, not fixed — outside register scope

- **#1610**: `ALPHA_AGREEMENT_v2.md` ships with a literal `[contact email]` placeholder in a legal agreement — open since Oct 2025, duplicated in 2 other docs. Needs PM's actual address once, then one fix across all three files.
- **#1611**: `mac-dock-integration.md` is built entirely around PM's own "6:00 AM PT standup" routine (not a visitor's) and describes what looks like a stale two-process architecture (port 8081 `uvicorn` frontend) that every current doc I checked today contradicts (single `main.py` server, port 8001 only). Both problems are bigger than a register fix — recommend someone with architecture context checks whether the two-process startup is even current before deciding whether to rewrite or pull the file from KEEP.

Continuing to hold at tier 3 — 15 of the 18 files are done (register-clean or fixed), `mac-dock-integration.md` itself I left untouched pending #1611.

— Comms
