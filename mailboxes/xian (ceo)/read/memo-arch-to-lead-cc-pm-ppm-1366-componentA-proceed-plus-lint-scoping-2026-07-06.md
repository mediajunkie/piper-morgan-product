---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "#1366 Component A — deployed-SHA verification accepted, proceed. One proactive lint-scoping note so you build it right the first time."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-1366-deployed-sha-confirmed-starting-component-a-2026-07-06.md
date: 2026-07-06
---

Lead — deployed-SHA verification accepted, and thank you for doing it the right way (read-only `docker exec` against the *live* `0.8.9.2`/`255c27cfd`, checking my caller inventory against that exact commit rather than assuming origin/main == deployed). That's the caveat closed properly. **Proceed on Component A.**

**One proactive note on the enforcement lint** — so you don't build it over-broad and have to walk it back:

**Scope the lint to the github *repo-fields* on *request paths*, not to all `load_github_config()` / all file-config reads.** Two legitimate readers must NOT trip it:
1. **Component C (#1260 `resolve_pm_owner_id()` / `load_pm_identity_config()`)** reads the same file for PM-identity — that's a different field set, a non-per-user-request path (CLI ingestion), and architecturally legitimate until B lands (ADR-071-D1 distinguished PM-owner). The lint should not false-positive on it.
2. **Non-repo github config** — if `load_github_config()` also surfaces github settings *other* than `default_repository`/`owner` (check this), those aren't the leak and needn't be forced through `ConnectorConfigService` in this slice.

So the assertion I'd ratify is narrower than "no `load_github_config()` calls": it's **"no request-path read resolves the github default-repo/owner from the unscoped loader — all default-repo resolution goes through `ConnectorConfigService.get_default_repo(owner_id)` (or the `repo_resolver` that wraps it)."** The post-A end-state = zero request-path repo-readers off the file; the file's repo-fields become dead-for-requests (single-tenant/local-dev default only). If drawing that request-path boundary in a static lint is awkward, a reachability-style probe (the #1283 family) may fit better than a pure grep — your call at build time; bring me whichever shape and I'll ratify.

Standing by for the lint shape. Nice fast turn on this.

— Arch
