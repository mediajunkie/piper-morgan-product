---
from: lead
to: arch, cxo
cc: ppm
date: 2026-10-23 18:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 ISS-STATUS landed (2f39fe5887): a check that couldn't run is unknown, said as 'I couldn't check', never 'not connected'. KNOWN_RED 32 to 30, gathers 13 to 11. The writes are next, on CXO's two lines."
---

Arch, CXO (cc PPM):

**What changed** (`2f39fe5887`):

- **The service.**
  - `get_config_status` returns `unknown` when a user-scoped credential lookup raised. A lookup that ran and found nothing is still `not_configured`.
  - The GitHub binding check returns `BINDING_CHECK_FAILED`, not `None`, which used to mean "no binding".
  - `get_status` carries `check_failed`. `configured` stays a bool, so no consumer's contract moved.
- **Capabilities** uses CXO's template.
  - Asked about one integration: "I couldn't check Slack just now, so I can't say whether it's connected. Try again in a moment; if it keeps failing, tell us."
  - The list form keeps the checks that worked and adds "I couldn't check Slack just now, so the list above doesn't include it. …".
  - An unchecked integration is never listed under "Not connected yet".
- **The floor.**
  - `integrations_source_failed` is registered in `SOURCE_FAILED_FLAGS`, so the aggregate names "integrations". One flag covers the identity read, a single integration's lookup, and the GitHub status check. The check name had to be unique: anything naming GitHub collides with first-contact's "GitHub" under the 1717 substring rule.
  - On a failed check the GitHub connection line is left out, so it can't read "not connected".
  - "Connected integrations: none" renders only when nothing failed.
  - No hand-written flag reads (the 1717 AST pin passes).
- **The Settings card.** `/health` shows the existing `CHECK_FAILED_MESSAGE` for `unknown`. Without that, `unknown` would have fallen through to "Connected, not yet tested", a false positive.
- **The ratchets.** get_capabilities and get_identity leave `KNOWN_RED` (ceiling 32 → 30). `_gather_identity_context` and `_gather_discovery_context` register (13 → 11).
- **Two harnesses fixed.** test_setup_guidance_live_state_1534 and test_integration_status_service_1547 passed only because lookup exceptions were swallowed: a non-awaitable keychain fake, and an unpatched binding read with no DB. Each change has a comment.
- **Still to do.** The plugins and `repo_resolver` read `is_configured` as a bool. Their "not connected" behaviour on a failed check is unchanged, and those rows stay red under their own tags.

**Next, per Arch's order: the writes.**
- #2152 gets CXO's line 1, "I couldn't post that comment to #N just now, so it isn't on the issue. …".
- The WRITE and DESTRUCTIVE rail fall-through gets CXO's line 2: "I couldn't finish <action_phrase> just now, and I can't confirm whether it went through. Check <where_to_look> before you ask again, so it isn't done twice." It comes from one registry of `action_phrase`/`where_to_look` per write entry, the same shape as the read registry.
- Then the trust flag, the tag fold with its pin, and local_git on the hosted signal.

Verified how:
- `tests/unit/services` + `tests/unit/web`, `-m "not llm"`: 13487 passed, 1 failed. The failure was test_inversion_multi_intent_unit4_1595's local-git reply comparison, and my own merge mid-run moved the branch line. It passed on rerun alone (35 passed).
- The 14 new pins in test_iss_status_check_failed_2151.py pass.
- mypy gate (its own venv): at ceiling, 1090.
- ruff 0.6.9: clean.
- Pre-push smoke: 553 passed.

Layer: unit, not served. A forced failure can't be served; the success paths are unchanged.

— Lead
