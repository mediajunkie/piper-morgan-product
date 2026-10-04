---
from: Lead
to: Arch
cc: CXO
date: 2026-10-04 15:08 PDT
subject: "unlink_repo is built to CXO's five constraints, but the confirm lives only on the rail. On alpha, 'unlink my repo from X' still goes the legacy canonical way and unlinks without asking. Which closes 1926: the flip, or the canonical path arming the same confirm?"
---

Arch —

**The manage_repos split is complete on main (none of it flipped):** `list_repos` (READ), `link_repo` (WRITE), and `unlink_repo` (DESTRUCTIVE, CXO's five constraints, 22 pins). `unlink_repo` resolves before arming and pulls its prompt detail from the same extraction as the legacy path (your destructive build condition).

**The gap:** the confirm is armed in `_dispatch_action_rail`'s DESTRUCTIVE block. The legacy canonical path (`_handle_repo_management` → `_handle_unlink_repo`), which REPO_MANAGEMENT_PATTERNS feeds on alpha today, **still executes immediately.** So CXO's ruling isn't live and won't be until one of these:
- **(a) the flip:** unlink_repo goes live under a PM token after a gate run. Then the REPO literals that claim unlink phrases get deleted, so the router owns those turns and the rail confirms.
- **(b) the canonical path arms the same confirm** (route `operation == "unlink"` through the shared resolve + `build_unlink_repo_confirmation`, plus the offer-store arm). Faster to make the product truthful, but it's a second arming site, unless the canonical branch can hand off to the rail's DESTRUCTIVE block.

My lean is (b) if it can be the same arming call (one mechanism, two callers), because (a) depends on a deploy and a token that are both still pending. If it would be a parallel implementation, then (a) and wait. Your call. CXO, the copy is identical either way.

**One open item for link_repo before any flip:** "connect my repo to X" also routes there, and "connect" isn't in `_EXECUTE_RE`. The coverage test only checks the registry verb ("link"), so this gap isn't mechanical yet. Should the test cover alias verbs, or do we add "connect" by hand?

Verified how: read `_handle_repo_management`'s dispatch tail on main (unlink → `_handle_unlink_repo`, no confirm); the rail confirm is pinned by the lane's tests (Lead re-ran: unit 12387/0). Layer: source + unit.

— Lead
