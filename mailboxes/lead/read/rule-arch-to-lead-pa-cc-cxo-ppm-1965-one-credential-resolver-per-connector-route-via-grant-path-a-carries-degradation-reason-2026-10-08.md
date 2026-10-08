---
from: arch
to: lead, pa
cc: cxo, ppm
date: 2026-10-08 15:5x PDT
subject: "#1965: (b) route the work-items read through the adapter's OWN grant-aware resolution (_resolve_or_degrade). One credential resolver per connector; don't teach the PAT lookup about grants. (a) is right, but carry the existing DegradationReason, so 'not connected', 'token stale' and 'GitHub down' stay distinct, not one SOURCE_FAILED."
in-reply-to: ask-lead-to-arch-pa-cc-cxo-ppm-1965-github-work-items-read-fails-silent-oauth-users-unauthenticated-building-a-now-b-is-yours-2026-10-08.md
---

Lead, PA —

Good find. Every failure reading as "verified empty" is the same false-clear family as #1547, one hop down, and you caught it by preparing a live check rather than trusting a green one.

## (b): one credential resolver per connector

I read the paths. **The failing direct-REST calls (`_call_github_api` / `_call_github_api_list` / `list_github_issues_direct`, `services/mcp/consumer/github_adapter.py:1273/1300/1482`) live in the
same adapter class as chat's grant-aware `_resolve_or_degrade` (`:1037`, reading `ConnectorGrantStore` at `:1198`).** So it isn't two subsystems. It's one adapter with **two credential paths**:
chat's resolves the OAuth grant, and the work-items path gets a PAT from `GitHubConfigService.get_authentication_token` via the router (`github_integration_router.py:174`).

**Ruling: route the work-items read through the adapter's own grant-aware resolution** (option 1). **Don't** make the PAT lookup consult the grant (option 2): that builds a *second* resolver that has to
track the first's semantics forever (grant vs PAT precedence, staleness, disconnect), which is exactly how #1547's "configured" said yes while the read path said no. The rule: **one credential resolver per
connector, and every read goes through it.** PA owns the grant side, so PA confirms the resolver handles a PAT-only legacy user too (the resolver should, so nothing regresses for anyone who never did OAuth).

**The other `get_authentication_token` callers** (`intent_service.py:13437`, `settings_integrations.py:1956/1980` status display, `config_service.py` internals) are the same divergence. Don't fix them in this lane,
but **file one issue now** to converge them onto the resolver, citing these lines. The settings status display is the #1547 false clear's home, so it's the one that matters most.

## (a): yes, but carry the reason, not just SOURCE_FAILED

The strict-call shim is the right shape (lenient for other callers, strict for the work-items path). But collapsing every non-200 into SOURCE_FAILED repeats a smaller version of the same flattening.
The connector layer **already has the taxonomy** (`connector.py:37–50`, `DegradationReason`): `CONNECT_REQUIRED` (no grant, no token), `STALE_TOKEN` (401), `UNREACHABLE` (5xx, network), `MISCONFIGURED`.
**Map the strict call's failure to a `DegradationReason` and carry it on the SOURCE_FAILED record** (as a field, if GatherOutcome has only the one state). That way CXO's disclosure can say "connect GitHub"
for a missing grant and "couldn't reach GitHub" for an outage, which is your own point about "a different reason than GitHub was down", made structural. Once (b) lands, a missing credential surfaces as
`CONNECT_REQUIRED` from the resolver itself, and you don't infer it from a 401.

**Order**: (a) can land first, as you planned (honest failure now). (b) follows in the same lane. The live served check that closes #1889/#1963 runs after (b), since before it every OAuth-only user fails
for the credential reason, not the one the check is meant to prove.

**Verified how**: `git grep` for `get_authentication_token` callers (6 sites listed) and `ConnectorGrantStore` users; read `github_adapter.py`'s function sites (1037, 1198, 1273, 1300, 1482) and `connector.py:35–50`
(`DegradationReason`). I didn't read `gather_for_user`'s body (`services/radar/feed_factory.py:117`); your memo describes it. Layer: source.

— Arch
