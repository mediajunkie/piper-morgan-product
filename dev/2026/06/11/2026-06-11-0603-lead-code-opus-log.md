# Lead Developer — Session Log 2026-06-11

**Role:** Lead Developer (Claude Code, Opus)
**Branch/worktree:** `claude/1187-floor-wiring` @ `piper-morgan-product-1158-summarize-taxonomy`
**Started:** 06:03 PDT (Thu Jun 11), continuing the M3 #1187/#1192 thread with PM in tandem.

## Carry-in from June 10 (see that log for full detail)
- **#1187** SUMMARIZE-fetch: Gap-1 (issue-number extraction) + floor-injection mechanism merged to main; INERT until GitHub repo-resolution works. Issue stays OPEN, blocked on #1192.
- **#1192** integrations last-mile (M3): (c) GitHub connect endpoint fixed + merged (validate via `GET /user`, off the `test_connection` migration orphan). (a) approved + next: **read-bridge** — point `repo_resolver._resolve_from_user_default` at the persistent #573 store (`data/github_preferences.json`) the UI already writes, since the #1042 `UserPreferenceManager` path is in-memory + re-instantiated-empty (never worked).
- PM-approved ordering: (1) #1192(a)+(c) → close #1187; (2) #1143 composting dev-trigger; (3) #313 next slices; (4) #1129 Slack Socket Mode (gated on PM re-registration).

## Today's plan
1. Implement slice (a) read-bridge + tests (confirm `default_repository` format — owner/name vs id).
2. Restart server (env-stripped) → PM UATs slice (c) connect fix at `/settings/integrations/github`.
3. Post-(a): PM UATs #1187 `summarize issue #N` for real → tune floor wording → close #1187 + #1192(a)/(c).

## Entries

## ~06:00–08:00 PDT — #1192(a)+(c) + #1187 unblock: connect → designate repo → summarize, all through the product

PM-approved order (1): #1192(a)+(c) → close #1187. Tandem with PM all morning. Shipped + on main:

- **#1192(c) connect fix** (`6e5229fb2`): `router.test_connection()` was a migration orphan (#198 left it unimplemented on BOTH adapter + spatial) → 500'd every PAT (#541 stuck-state; PM's "working PAT fails"). New `token_validator.verify_github_token` (direct `GET /user`); both save+status endpoints rewired. Test-theatre caught (old tests mocked the orphan → passed while prod 500'd). PM connected a PAT via UI — verified.
- **#1192(a) read-bridge** (`871b60e9f`): resolver read in-memory `UserPreferenceManager` (always empty, re-instantiated per call) while UI wrote persistent `data/github_preferences.json` — two disconnected stores. Pointed `repo_resolver._resolve_from_user_default` at the persistent store. Default-repo set in settings now reaches the chat path.
- **UAT found Blocker 1 (credential priority)** (`29555f84d`): `get_authentication_token` was env-first (#578) → a stale `.env` GITHUB_TOKEN shadowed the valid connected keychain token → adapter auth failed → floor. PM: ".env is a floor, not a ceiling." Flipped: a connected user's keychain token wins over env; "system" still uses env.
- **Blocker 2 (Option C)** (`29555f84d`): MCP adapter returns a lossy issue dict (no comments, description-not-body) — too thin for a summary. New `issue_fetch.fetch_issue_with_comments` (direct REST, raw shape + comment thread). `_fetch_issue_content` now: parse #N (Gap-1) → resolve repo (slice a) → token (keychain-first) → direct fetch → formatter.
- **End-to-end verified** (real scenario, stale .env present + connected user): `_fetch_summary_source_content` → **25,139 chars + 8 comments** for #1124 (vs old thin 306/floor). 90 unit tests pass (1 pre-existing #1188 fail). #1192 updated with progress + still-open (d) "what I'm seeing" panel doesn't reflect connections, (b) project-threading, store-unification debt.

**The deep-debug arc**: the live UAT floored despite correct data. Traced through classifier (correct: SYNTHESIS+source_type) → fetch (returned None) → a misleading in-process test artifact (heavy `import` reloads `.env`, re-shadowing the popped token) → the real env-first credential bug. Lesson: in-process repro of server behavior must control dotenv reload (pop AFTER import), else the .env token masks the keychain path.

- **Mail**: replied to PA's BYO-key build-order memo (Lead sanity-check: order holds, Gap A(i) parallelizable, encryption-key-location is the real #358 substance, #1192 adjacency); triaged PPM's #1185 roadmap-placement memo (cc, response-requested:none) — Gap A(i)-into-M4 is Lead's call, noted for M4 planning.

**Open**: PM's live `summarize github issue #1124` UAT result (server live pid 58728) → then tune `_format_domain_context` summary wording → close #1187 + #1192(a)/(c).

## ~23:00 PDT — DAY-CLOSE: #1187 CLOSED (live-verified), #1192(a)+(c) done

PM ran the browser UAT (m1-test): `summarize github issue #1124` → faithful structured summary (Problem/Solution/Phases/Impact) from the full body + 8 comments. **Live root cause of the final floor**: the full classification pipeline (learned-pattern/KG enrichment for a returning user) collapses to `action="summarize_github_issue"` and OMITS the `source_type` slot — so the dispatcher's `source_type=="github_issue"` gate returned None. Fresh/standalone classifier sets it cleanly, which is why unit tests + in-process repro passed while the live path failed. **Fix** (`15617d1cf`): dispatcher infers `github_issue` from the collapsed action / unambiguous message when the slot is absent — defensive regardless of classifier path. Diagnostic log confirmed (`ctx_keys` had no source_type), then stripped. +4 inference tests (23 total green).

- **#1187 CLOSED** (completed) — full evidence comment (3 "what to build" items delivered; commits `03a0cbf58`/`29555f84d`/`15617d1cf`; 38 unit tests across 3 files).
- **#1192 updated** — (a) read-bridge + (c) connect + bonus keychain-first credential priority DONE; (b) project-threading, (d) connect-status panel/connect-offer, store-unification remain (M3).

**Morning resume (PM-approved order)**: (1) #1192(a)+(c)→#1187 ✅ DONE → next (2) #1143 composting dev-trigger (small, env-indep) → (3) #313 file-browser next slices (UI/UAT) → (4) #1129 Slack Socket Mode (gated on PM re-registration). Server left running (pid 16918) for tomorrow.

## Memory & briefing surfaces referenced this session
- **Referenced:** CLAUDE.md (env-stripped restart; `--body-file` for gh backticks; keychain `_api_key` convention; mailbox-on-main bridge + sign-off; close-issue-properly = update body before close); `feedback_close_issue_properly_skill_recurring_miss` (checked #1187 for checkboxes before closing — none); `feedback_investigate_before_extending_all_work` (traced the whole connect/classify chain end-to-end before each fix); `feedback_make_promises_durable_no_happy_talk` (each fix landed with tests, not just assertion); methodology-30 consumer-trace (the deep classify→fetch→auth→adapter trace); Pattern-045/test-theatre (tests mocked the orphaned test_connection AND used a fresh classifier without learned patterns — both hid live bugs); duty-cycle-tick (light IDLE fires through the UAT day).
- **Loaded but not referenced:** most M3 standing-context runway (superseded by the #1187/#1192 thread all day); cross-pollination brief; ROSTER.
- **Wanted but not found:** read:project scope to query the M3 board directly (had to reconstruct M3-remaining from session knowledge); a canonical "classifier output contract under the full pipeline vs standalone" doc — the learned-pattern/KG enrichment dropping source_type is exactly the kind of divergence that needs documenting.

## Sign-off (June 11)
