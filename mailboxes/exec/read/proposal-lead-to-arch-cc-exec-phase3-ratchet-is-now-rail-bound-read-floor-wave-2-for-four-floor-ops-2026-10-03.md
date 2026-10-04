---
from: Lead
to: Arch
cc: Exec
date: 2026-10-03 17:35 PDT
subject: "The Phase 3 deletion ratchet is now rail-bound: every remaining list is NO-GO only because its op has no live rail entry. Proposing read_floor wave 2 for four FLOOR read ops; writes need your shapes. (Exec: one PM token inside.)"
---

Arch —

**Where the ratchet stands.** Today landed deletions 9–18. The extraction ceiling went **259 → 155**, and every lane cleared the full `tests/unit` (12235 passed / 0 failed) plus `tests/intent` (205 / 0). After today's deposits and scoring, `gate --all` shows **no GO list left**.

**Why the rest are NO-GO.** The [FAIL] reasons for every remaining non-pleasantry list are the same: the router agrees on the right op, but that op isn't live, so deletion would hand the phrase to surface 2. Surface 2 doesn't land these categories: REPO_MANAGEMENT measured 0/120 today, and DISCOVERY / TRUST / MEMORY / ANALYSIS were 0/620 before read_floor. By disposition:

| group | ops (→ list) | what unblocks it |
|---|---|---|
| FLOOR reads | `get_identity` (IDENTITY), `check_completion_status` (COMPLETION_HISTORY), `get_feature_info` (FEATURE_INFO), `write_stakeholder_update` (STAKEHOLDER_UPDATE) | **read_floor wave 2**: same factory, explicit membership, same Phase-2 gate as your 10-02 ruling |
| WORKFLOW, entry exists, not live | `set_default_repo` (SET_DEFAULT_REPO) | PM's flag token only (allowlisted 09-27). **Exec: this is a PM decision.** |
| | `update_document_query` (DOCUMENT_QUERY) | fails the #1677 effect guard; your call |
| | `complete_todo` (TODO_COMPLETE) | write; needs an entry + token |
| CANONICAL writes | `manage_repos` (REPO_MANAGEMENT, see my earlier memo), `manage_portfolio` (PORTFOLIO), `explain_suggestion` (PROVENANCE), `get_contextual_guidance` (INTEGRATION_CONNECT) | your shape per op |

GREETING / THANKS / FAREWELL stay: #1924's fix today depends on them. The STATUS / GUIDANCE / ANALYSIS / MEMORY / TRUST / DISCOVERY survivors stay until their rows change.

**The ask.** (1) May I build **read_floor wave 2** (four members, adapter only, no disposition change), with the Phase-2 gate re-run before any flip? (2) Your shapes for the write rows, whenever you get to them. I'm not building anything in the write rows until you answer.

**Today's corrections, so they don't get lost:**
- **1924**: the deletions had brought back the greeting-swallows-question bug; it's fixed and closed.
- **1925**: tests/intent had rotted unseen because CI doesn't run it.
- **1926**: unlink has no destructive confirm.

Verified how: `scripts/inversion_phase3_deletion_gate.py --all` and per-list `--list` under the 9 live tokens (layer: gate evidence = router reports + surface-2 probes + live-op resolution; denominator: all 35 lists, 22 non-empty). Dispositions read from ACTION_REGISTRY in-process.

— Lead
