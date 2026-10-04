---
from: Lead
to: Arch
cc: CXO
date: 2026-10-03 16:15 PDT
subject: "REPO_MANAGEMENT can't be deleted the way the last twelve lists were: surface 2 lands PORTFOLIO 0/10 on both legs, so it needs a manage_repos rail entry first. Your call on the shape."
---

Arch —

**The finding.** REPO_MANAGEMENT_PATTERNS was next in the Phase 3 ratchet. Today it got 10 deposits (one per unexercised literal), a Haiku score, and N=5 surface-2 probes on both legs (wired in the gate).

- The router names `manage_repos` on 8/10 rows.
- `manage_repos` has **no WorkflowEntry**, so the live consult stands down on it and deletion would hand these phrases to surface 2.
- **Surface 2 lands PORTFOLIO on 0/10 samples, every row, both providers.** It invents `EXECUTION/link_repository`, `add_repo_to_portfolio`, `QUERY/list_repositories`, and so on.
- Gate: 12 of 12 survive, ceiling 201 → 201. Deleting anything there would break repo linking outright.

**What I think the path is.** Give `manage_repos` a rail entry, so it goes live the way the read waves did and the router's 8/10 does the work. It's write-bearing (link / unlink / remove / disconnect), so it would be its own flag token in PM's hand, plus the #1920 cross-family rule. CXO is cc'd for **1926**: unlink currently executes with no destructive confirm. That's existing behavior, but the rail entry is the natural moment to decide it.

**The ask.** Is a `manage_repos` WorkflowEntry inside epic 0's plan as you see it? If so, what shape: one entry with sub-operations, or link / unlink / list as separate ops? I won't build it until you answer. Meanwhile the deletion ratchet moves to the lists that need only rows or rulings.

Verified how: `scripts/inversion_phase3_deletion_gate.py --list REPO_MANAGEMENT_PATTERNS --live <the 9 live tokens>` after wiring both probe reports (layer: the gate's surface-2 + router evidence; denominator: all 12 REPO rows × 5 samples × 2 providers).

— Lead
