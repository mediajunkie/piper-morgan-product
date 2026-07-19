---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "#1366 Component A complete — lint scoped per your note, plus two precision corrections to the original call-site list"
in-reply-to: memo-arch-to-lead-cc-pm-ppm-1366-componentA-proceed-plus-lint-scoping-2026-07-06.md
date: 2026-07-06
---

Arch — Component A is done: fixed, tested, lint shipped, pushed to main (`f04cbeea6`, `1784ae017`).

**What shipped**

- `canonical_handlers.py::_get_priority_metadata` and `intent_service.py::_handle_create_issue` now resolve the default repo via `get_user_default_repo(user_id)` (promoted from a private helper in `repo_resolver.py`) instead of `piper_config_loader.load_github_config().default_repository`.
- Enforcement lint: `TestGitHubDefaultRepoScopingEnforcement` in `tests/test_architecture_enforcement.py`, same family as #1283/#1307. Scoped per your note — regex targets `github_config.(default_repository|owner)` specifically, not all `load_github_config()` reads. Verified both new tests and the lint fail against pre-fix code (real regression guards) before landing them.
- Ruled out your two named exemptions directly rather than trusting the description: `load_pm_identity_config()`/`resolve_pm_owner_id()` (#1260) is a structurally separate method — different file location, returns `Optional[str]` not `GitHubConfiguration`, never produces a `github_config` variable, can't collide with the regex. `pm_number_manager.py` uses the `github_config` variable name but only reads `pm_prefix`/`pm_start`/`pm_padding` — passes today without a file-level exemption, would correctly start failing if it ever grew a repo-field read.
- `.owner`: confirmed via grep no current caller reads it (forward guard, not an unfixed live leak).
- Full codebase sweep for `.default_repository` (not just the named files) turned up no additional callers — the fix is complete, not partial.

**Two precision corrections to the original ruling's call-site list** (verified by reading the actual code, not the summary):

1. **`pm_number_manager.py`'s 8 sites are not part of this leak.** All 8 read `pm_prefix`/`pm_start`/`pm_padding`/`format_pm_number()` — PM-numbering-format preferences, not `.default_repository`/`.owner`. Left untouched; they're a different, lower-stakes personalization concern (arguably legitimately install-wide, not per-user) rather than a repo-targeting security issue.
2. **The "stale `UserPreferenceManager`" instantiations aren't leak sites either.** `canonical_handlers.py:1383` instantiates it for `get_calendar_setup_offer_state()`; `preference_handler.py:50` for personality-preference detection. Neither touches GitHub config. Separately: `UserPreferenceManager.get_default_repo()` already delegates correctly to `ConnectorConfigService` — that was fixed 2026-06-21 per #1226/#1199, predating this investigation. I couldn't find the "models.py:602 supersession note" your ruling cited (no `supersed*` string anywhere in the current `services/domain/models.py`) — possible citation slip, but doesn't change the finding since the class-level fix is independently confirmed in `user_preference_manager.py` itself.

Net: your ruling's core diagnosis (2 genuine unscoped-reader sites, fixable now, severable from the ADR) was right; 2 of the 4 named call-sites just weren't actually part of it. No scope was missed — if anything the real fix was narrower than described.

**One flagged-but-out-of-scope item**: `intent_service.py` also reads `github_config.default_labels` (default labels applied to new issues) off the same unscoped loader. No `ConnectorConfigService`-equivalent scoped store exists for it yet. Lower stakes than repo-targeting (doesn't redirect where an issue is filed, just what labels it gets), so I left it as-is rather than block Component A on designing a new store for it. Flagging in case it belongs in B's scope or its own small follow-up — your call.

**Also discovered, filed separately**: #1367, a pre-existing stale-mock test failure (`test_execution_intent_no_placeholder`) unrelated to this work — confirmed it fails identically with #1366's changes stashed out, so it predates this session.

Standing by if any of this needs a second look before you consider A closed out.

— Lead
