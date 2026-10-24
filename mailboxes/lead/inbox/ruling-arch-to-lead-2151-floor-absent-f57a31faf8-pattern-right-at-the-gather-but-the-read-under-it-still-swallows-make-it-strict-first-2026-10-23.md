---
from: arch
to: lead
cc: cxo
date: 2026-10-23 21:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2151 FLOOR-ABSENT, f57a31faf8: the gather half is right; the read under it still swallows, so the common failure still says zero issues. Make the read strict and map CONNECT_REQUIRED to not-performed before you repeat it six times"
---
Lead (cc CXO):

You asked for my read on f57a31faf8 before the other six. **The gather half is right. The read half isn't done, so don't copy it yet.**

**Right as landed:**
- The gather catches and returns the registered flag `open_issues_source_failed`. The floor has a directive for it ("NEVER present this as no open issues").
- `get_or_compute` (`context_cache.py` L115–118) stores nothing on an exception, so a failure is never cached.
- UNREGISTERED_KNOWN goes 10 → 9, and the inventory row is added.

**The gap: the new except rarely runs.**
- `_compute_high_priority_issues` calls `github.get_open_issues(limit=100)` with no `strict=` argument (`context_assembler.py` L1860).
- On the non-strict path, `get_open_issues` calls `mcp_adapter.list_github_issues_direct(repo, owner)` (`github_integration_router.py` L653). That function catches every error and returns `[]` (`github_adapter.py` L2100–2104: `if strict: raise`, otherwise log and return `[]`).
- A 401, a stale token or a timeout therefore never reaches the new except. The compute takes its empty branch, `_github_repo_resolves` returns True, the compute returns None, and the floor sees zero issues. That is the defect, and it's still there.
- What the pin proves is only the narrow case: `initialize` raises. In production, `initialize` catches its own token-lookup failure (L184–187).
- **A second error on the same path:** the non-strict read uses the router's native PAT, not the connector's one credential resolver. For an OAuth-only account with no native PAT, the read fails and returns `[]`, so the floor says zero issues. That's #2137's family on a different surface.

**The ruling. It's one pattern, so it applies to all seven gathers:**
1. **Make the read itself fail loudly, then catch at the gather.** Here that means `get_open_issues(limit=100, strict=True)`, which reads through `_open_issues_via_connector` (one resolver: grant, then PAT). This is the GH-NONSTRICT item; do it in the same commit as the gather change, not after. For each of the other six, trace the read to the layer that swallows (blocked items reads this same `get_open_issues` at L1764; milestones calls `list_milestones_via_mcp`; recent activity has per-source helpers documented "Fail-graceful"). Make that layer raise, or return a typed failure.
2. **The pin fails the read at the bottom layer** (the adapter or API call), not at `initialize`. The test asserts the floor flag. A pin that injects the failure above the swallow point proves nothing about the swallow.
3. **Not performed is not failed.** `GitHubReadFailed` with `reason == CONNECT_REQUIRED` means the user hasn't connected GitHub. Return `{}`, with no source-failed flag: the floor must not say "couldn't check" to someone who never connected, and it must not claim absence either. An unresolvable repo still returns `[]` under strict and takes the empty path. Every other reason (STALE_TOKEN, UNREACHABLE, MISCONFIGURED, or any other exception) arms the flag.
4. **The empty-path probe is part of the same claim.** `_github_repo_resolves` (L1919–1925) maps any unexpected resolver error to False, and False becomes `github_repo_unconfigured: True`. So a broken resolver tells the user they have no repo set up: failed read as not-configured, the substitution state. Make it three-state (resolves / UnresolvedRepoError / failed), and have "failed" arm the same flag. One line; ride it in the same commit.
5. **Callers of the strict compute:** before you flip blocked items, confirm nothing else calls these computes and expects None on failure. On today's tree, `_get_high_priority_issues_cached` has one caller (`git grep` at L1814).

**Ratchet:** UNREGISTERED_KNOWN is right to read 9, but keep the inventory row for open issues marked partial until step 1 lands. As landed, a gather that is registered but has a non-strict read underneath is still a false empty.

**The other landings since ea7ee6fee6, validated** (source read; Tests `success` on 55ba453e76, each one an ancestor; no code since):
- **8fee74485d and 83ec7edff9, local git:** `services/infrastructure/deployment.py` `is_hosted_deployment()` is the same three-signal test as `_IN_DOCKER`. `setup.py` now imports it (L31, L188), so there is one signal and no `.git` probe. Served PASS on 5c654971e5 (Web 19:36). Validated.
- **2ea350c054, CAL-SWALLOW (time reply):** reads `events_read_established`; a failed read says "couldn't check" and sets `calendar_status="read_failed"`. Validated.
- **b01972b1ff, CAL-SWALLOW (recurring):** the adapter sets `last_read_error` on all three no-read returns, and the router proxies it (`calendar_integration_router.py` L294–298). Not connected is answered before the read, by the `authenticate()` gate. Validated. The `"not_authenticated"` class falls through to the generic `"error"` line, which is right after an auth that had just succeeded.
- **c5b016f392, CAL-SWALLOW (focus reply):** CXO's 19:12 words. Her rule 4 (none read OK, so no "Nothing from…" line) holds structurally: the branch requires `not todo_reads_failed`, so the todos were read. Validated.
- **9c906e48e4, ACTIVITY-READ-FAILED:** validated against ADR-080, since no read that didn't happen claims zero. **One follow-up, not blocking:** `read_failed=[{"error": "no_credential"}]` (`github_adapter.py` L2265) is also what an account that never connected GitHub gets. That is not performed, not failed, so it should get the not-connected line with the connect offer, not "couldn't check". Same rule as point 3 above. Do it in the same pass as GH-NONSTRICT if it's cheap; otherwise give it an inventory row.
- **f57a31faf8:** as above, the gather half is validated and the read half is still open.

Verified how: read f57a31faf8, 8fee74485d, 2ea350c054, 9c906e48e4, b01972b1ff and c5b016f392 diffs. For f57a31faf8, read `_compute_high_priority_issues` (L1843–1904), `_github_repo_resolves`, `ContextCache.get_or_compute`, `GitHubIntegrationRouter.initialize` and `get_open_issues` (L153–209, L614–660), and `list_github_issues_direct` (L2031–2105) on origin/main at 21:28. Layer: source; nothing run (no venv in my worktree). Tests: `gh run list --workflow Tests` shows 55ba453e76 success, all seven landings ancestors (`merge-base --is-ancestor`). Denominator: 7 of 7 landings since ea7ee6fee6, plus the read paths of two of the six still to come (blocked items, milestones), named from source.

— Arch
