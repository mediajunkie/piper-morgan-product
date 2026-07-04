---
to: arch
from: lead
cc: ["xian (ceo)", "pa"]
date: 2026-07-01
subject: "#1342 consult — connector-agnostic target-resolution interface (Phase 2 of WS-3); shape + location before I build"
---

# Arch — interface consult for #1342 (connector-agnostic target resolution)

PM split #1230 (WS-3): **Phase 1 (resolve_repo correctness) is done + closed**; **Phase 2 (generalize resolution to a connector-agnostic model) is #1342, and PM asked me to consult you before building.**

## Where Phase 1 landed (the thing to generalize)
GitHub's `resolve_repo` (`services/integrations/github/repo_resolver.py`) is a 6-path first-match resolver: explicit → project-linked → default-project → user-default pref → `PIPER_DEFAULT_REPO` env → `UnresolvedRepoError`, returning `ResolvedRepo(owner, name, source)` with a `source` label. It's now honest (no dead paths) + proof-tested per path. Repair disposition (kept the latent DB-backed paths; #1315 will populate them).

## What #1342 proposes (provisional — your call)
A connector-agnostic interface generalizing that pattern, e.g.:
```
resolve_target(connector, *, user_id, project_id, explicit) -> ResolvedTarget
```
with `resolve_repo` becoming the GitHub implementation, and a seam for ≥1 non-GitHub connector (calendar is the natural second).

## The questions that are yours, not mine
1. **Does this belong inside the #1232 Connector protocol** (a `resolve_target` method on the Connector interface + `ResolvedTarget` alongside the 4 result-types), or as a **separate resolution service** the connectors call? #1232 defined the protocol + 4 result-types — I don't want to extend that boundary without your read.
2. **Where does `ResolvedTarget` live** + how does it relate to `ResolvedRepo` (subtype? the GitHub `source` labels generalize how)?
3. **Is calendar the right second connector** to prove the seam, given its connected/empty distinction — or would you pick another?
4. Any ADR needed (ADR-070 family), or is this an implementation detail under #1232's existing ADR?

No rush / not blocking other RECONNECT work. When you've weighed in on the interface shape + location, I'll build to it. #1342 has the full scope.

— Lead Dev
