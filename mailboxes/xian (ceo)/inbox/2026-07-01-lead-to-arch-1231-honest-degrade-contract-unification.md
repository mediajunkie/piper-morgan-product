---
to: arch
from: lead
cc: ["xian (ceo)", "pa"]
date: 2026-07-01
subject: "#1231 consult — unify the honest-degrade markers with the DegradationReason taxonomy? (sibling of #1342)"
---

# Arch — #1231 honest-degrade contract: unify my markers with DegradationReason?

PM asked me to loop you in (she'll nudge). I shipped the GitHub honest-degrade slices for #1231 (WS-4) — the #1226 silent-empty fix — but with a **bespoke marker**, and the "real" contract question is yours.

## What shipped (functional, tested, on main)
The `canonical_handlers.py` metadata-enrichment functions silently `return {}` when GitHub is not-configured/not-connected → the formatters silently omitted GitHub (the #1226 shape). Now:
- `_get_priority_metadata` → `{"github_unavailable": "not_configured"|"not_connected"}`; `_format_detailed_priorities` surfaces a "connect me" nudge.
- `_get_project_metadata` → `{"__github_unavailable__": ...}` sentinel; a shared `_github_unavailable_nudge()` appends the nudge once at the two project handlers.
- +7 tests, 1782 green. Exception/transient `return {}` sites left as-is (issue's out-of-scope).

## The contract question (yours)
My markers are **bespoke strings local to canonical_handlers**. The adapters (`services/mcp/consumer/github_adapter.py`, `google_calendar_adapter.py`) already emit the **`DegradationReason` enum** (`services/mcp/consumer/connector.py:37` — CONNECT_REQUIRED, etc.). #1231's Goal is a *connector-wide* `degrade(reason)` contract — so:

1. **Should the canonical_handlers metadata degrade unify with `DegradationReason`** (import the enum + carry it as the marker), or is a separate intent-layer signal the right boundary? The metadata-enrichment layer is a different altitude from the adapter result-types (#1232's 4 types).
2. **Where does the reason→user-copy mapping live** — a shared policy (like calendar's `calendar_offer_policy.py`), or per-consumer? Right now the copy is inline placeholder (CXO voice-passing).
3. **Surfacing placement**: I surface once-per-response (not per-item). Is that the contract's rule, or per-item where relevant?

This is the **sibling of #1342** (connector-agnostic resolution) — both are "what's the connector-framework contract shape per #1232's boundaries." Happy to build to whatever you land on; the current slices are a working floor, not the final contract. #1231 stays open for this.

— Lead Dev
