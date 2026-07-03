# Release Notes - v0.8.9.1

**Release Date**: July 2, 2026
**Type**: Patch Release (Security Fix)

---

## Summary

Emergency security patch. Anonymous requests to `/api/v1/intent` could silently be billed to the server's own Anthropic API key instead of being refused — discovered same-day during unrelated Caddy-gate investigation, root-caused, fixed, deployed, and versioned as this dot release so `production`'s branch history accurately reflects what's live.

---

## Security Fix

| Issue | Title | Fix |
|-------|-------|-----|
| [#1343](https://github.com/mediajunkie/piper-morgan-product/issues/1343) | Anonymous `/api/v1/intent` requests could silently bill the server's own Anthropic key | `resolve_request_api_key` now raises `AnonymousLLMKeyRequiredError` for unauthenticated + keyless requests instead of falling back to the server's key. Authenticated callers (logged in, no stored key — normal desktop/CLI use) are unaffected. BYOC (anonymous + own key, no login required) is unaffected. `/api/v1/intent` catches the refusal and returns an honest, actionable message instead of a silent bill. |

**Ratchet guard added** (`tests/test_anonymous_llm_key_boundary_1343.py`): any future anonymous-reachable route that touches the raw LLM-key resolver without handling the refusal now fails the test suite — the class of bug, not just the one instance, is covered going forward.

**Background context**: this fix pairs with the removal of the Caddy edge auth-gate (June 29) — the gate had been the only thing restricting who could reach this endpoint; removing it without this fix meant an open billing exposure. Full context in [#1343](https://github.com/mediajunkie/piper-morgan-product/issues/1343). The related open-registration question ([#1344](https://github.com/mediajunkie/piper-morgan-product/issues/1344)) is tracked separately and NOT part of this release.

---

## Deploy Infrastructure Fix

Discovered and fixed during this release's deploy — a container networking bug that briefly took the alpha site down mid-deploy:

- **`PIPER_HOST` now named in `docker-compose.yml`** (`app.environment`), set to `0.0.0.0` unconditionally. `main.py`'s uvicorn binding previously defaulted to `127.0.0.1` inside the app container — correct for the bare desktop `python main.py` path, but invisible to Docker's own port mapping and to sibling containers (Caddy) on the bridge network. Full incident writeup in `docs/internal/operations/alpha-deployment-runbook.md`.

---

## Testing

- **11,045 tests collected** on this release's codebase (`tests/archive/` excluded per repo convention; **20 pre-existing collection errors** elsewhere in the tree — confirmed unrelated to this release, none touch any file this patch changes; a symptom of `production` being 6 weeks / 983 commits behind `main`, not something introduced here; tracked as [#1346](https://github.com/mediajunkie/piper-morgan-product/issues/1346)).
- **51 tests targeted at this patch's actual changes pass clean** (resolver-level + route-level + the ratchet lint, run directly against this release's codebase).
- A full-suite execution run (all 11,045) was not completed within this release cycle — the suite's size makes a full run impractical for a 3-commit targeted hotfix; not attempted beyond the collection check + the changed-file-scoped run above. Recommend a full-suite pass as part of the next full release cut (production ← main).
- **Live functional verification** (see below) is the strongest signal for this specific patch and was completed.

---

## Verification

Live-verified on `alpha.pipermorgan.ai` post-deploy: an anonymous `POST /api/v1/intent` with no auth and no API key returns the honest refusal (`error_type: anonymous_key_required`), not a silent server-key bill. Site health, container stability, and the `PIPER_HOST` fix all confirmed live.

---

## Not Included

This is a targeted hotfix off `production` (v0.8.9), not a merge-forward from `main`. `main` has substantially more work (the RECONNECT sprint and related) not yet in this release — that will come with the next full release cut.
