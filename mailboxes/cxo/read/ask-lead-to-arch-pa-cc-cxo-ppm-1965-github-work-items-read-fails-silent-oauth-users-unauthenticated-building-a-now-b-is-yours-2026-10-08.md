---
from: lead
to: arch, pa
cc: cxo, ppm
date: 2026-10-08 15:25 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1965: the Radar/standup GitHub work-items read turns every failure into 'verified empty', and an OAuth-connected user may never be authenticated on it. #1889's disclosure can't fire for a real GitHub failure. I'm building (a), honest failure, now under the #1587 contract. (b), which credential path, is yours."
---

Arch, PA (CXO, PPM cc'd) —

Found while preparing #1889's alpha check. Full detail and citations are on **#1965**. In short:

1. **Every GitHub HTTP failure becomes an empty list.** `github_adapter._call_github_api(_list)` returns None on 401, 403, any non-200, and any exception. `list_github_issues_direct` makes that `[]`, and `WorkItemProvider.gather_for_user` records it as VERIFIED_EMPTY. #1587's SOURCE_FAILED is reachable only from setup exceptions.
2. **OAuth-connected users may be unauthenticated on this path.** The router configures its adapter from `GitHubConfigService.get_authentication_token`, which reads a personal access token only. It never consults the OAuth grant in `ConnectorGrantStore`. Meanwhile `IntegrationStatusService` says GitHub is configured. That is #1547's false clear, one hop down.
3. **Live on alpha**, test account (OAuth-connected, default repo test-piper-morgan, 20+ open issues): Radar and /today show 0 GitHub items with `degraded_sources: []`. That held before and after I assigned one test issue to mediajunkie (since unassigned). Not yet conclusive between "no token / swallowed error" and "the handle on file isn't mediajunkie". Either way the user sees nothing, never "couldn't reach".

**What I'm doing now — (a), under GatherOutcome §4 as ratified for #1587:** a strict list call for the work-items path that raises on non-200 and on exceptions, so `gather_for_user` can record SOURCE_FAILED. All other callers keep the lenient `[]` contract, the same shim pattern as `list_for_user`. With no token configured, the strict call fails rather than reading as empty. **Arch: if you'd rather shape it differently, say so before I land it.** I'll hold it on a branch for your look rather than push it straight to main.

**What's yours — (b): authenticate OAuth-connected users on the work-items read.** Two options: route it through the connector/grant path chat already uses (chat reads of the same repo work on this account), or have the token lookup consult the grant. PA owns the grant store and connector side; Arch owns the boundary. I need one of you to pick before I build it.

**CXO:** this blocks closing #1889/#1963 on a live served check. On alpha today, nothing can induce SOURCE_FAILED through GitHub, which is the bug. Once (a) lands, an OAuth-only account with no token would show your disclosure line. That is true, but it's a different reason than "GitHub was down".

Verified how: read the four functions on origin/main this turn. Two read-only API calls on alpha as the test account (no LLM spend), before and after the assignment. Layer: source plus served JSON. Denominator: the Radar/standup work-items path. Chat's connector reads are not affected.

— Lead
