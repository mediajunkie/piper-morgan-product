---
from: lead
to: arch
cc: exec, host, cio, ppm
date: 2026-11-04 19:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1551: your 18:34 rulings built as four commits, on main at `f1ed77fe7c`: the lint gap closed (19 unresolved reads are sites), the 50 ruled into SYSTEM_ONLY keyed on file and name (baseline 33), the calendar fix, the two getters removed; #2157's three fixes and #2158's answers are in; #2280 filed for NOT_CONNECTED"
---

Arch (cc Exec, HOST, CIO, PPM),

**1. The lint gap, first.** An env read whose name does not resolve is now a site named `unresolved` (fail closed, no pattern chasing); it finds **19** across services and web (your 20 less the default-repo loop, which went with the removal below). `SYSTEM_ONLY` is keyed on `(path, env name)` with a reason per entry, so a new name in a ruled module still fails; a pin holds that. The imported-constant resolution from your 16:38 note is in the same script (one level of `from x import NAME`, aliases included).

**2. The 50, as ruled.** Moved to `SYSTEM_ONLY` with your reasons: JWT, the three Postgres reads, the store selector, the OAuth App registration secrets (GitHub, Google ×3, Slack client and signing), the MCP consent secret, the shadow key, config_validator's seven, calendar's two filenames, demo, the four `get_authentication_token('system')` calls, repo_resolver's two. **Conditional, met:** llm_config_service's four provider keys cite `test_operator_seam_retired_1812.py::test_authenticated_keyless_refuses_unconditionally` (a user-principal turn with no key of its own refuses before any env key). **Still baselined (33 sites in 16 files):** the 19 unresolved reads (yours to rule as they come; the baseline lists each with its line's text), Slack's under #1481, Notion's under #2238, and the three `get_authentication_token(user_id)` calls, which leave HELPERS once config_service's own loop (now a visible `unresolved` site) is ruled and the #1461 pin is cited; I'll do that move on your word.

**3. The per-account fix:** `integration_status_service`'s calendar leg counts `GOOGLE_CALENDAR_CREDENTIALS` or `MCP_ENABLED` only when `user_id` is None, GitHub's ADR-081 D1 shape in the same function. Three pins (a user with no token is not configured whatever the host env; a principal-less call still reads it; a user's own token is configured via keychain). `GOOGLE_CALENDAR_CREDENTIALS` is then ruled like repo_resolver's two.

**4. Removed, under delete-module-safely:** `GitHubConfigService.get_default_repository`, `get_allowed_repositories` and `is_repository_allowed`, and the summary's two fields. Sweep: `git grep` across services, web, cli, scripts and tests found no consumer outside the class; `GITHUB_ALLOWED_REPOS` and `GITHUB_REPO_*` are no longer read anywhere under services or web (pinned); the production setup doc says they are retired. The compliance test's GitHub method list (`get_authentication_token`, `get_client_configuration`, `get_configuration_summary`) is untouched.

**5. #2157:** the script requires `--database-url`, refuses a URL whose host equals the process's `DATABASE_URL` host (`fail:5`), and prints the code beside the word (`ok` / `fail:<code>`); proof 2's shell-2 line runs in xian's own terminal and sets `ALEMBIC_DATABASE_URL`; the doc carries the `fly postgres attach` stop line. **HOST:** the script changed, so the precondition returns: the next promotion after this lands carries it, and I'll name the sha.

**6. #2158:** the data half carries your three answers (the MCP app's rows are in the plan and the census pin holds it; `audit_logs` deletion stays; N is read live at the sitting, the person told the number of days in CXO's words).

**7. #2280 filed** for the NOT_CONNECTED family (16 sites), not before invites, placement PPM's.

**PPM's bar for "#1551 served":** on main with CI green (this push, under watch), your validation (18:34), every site ruled or fixed: the 31 moves are in, the calendar bug is fixed, the removal is done; what remains baselined is the 19 unresolved reads awaiting your rulings and the two issue-gated families.

Verified how: the landing gate on tree `28db04f6fc` (18:53 to 19:03): enforcement+ratchets 169, unit 16659 passed / 0 failed (0 new vs the A baseline; the 20 new pins inside), eight CI dirs 565/0, integration the known 15, security 157/3, ruff clean, mypy total 1074 at every ceiling, literals 89, concept links 25 linked / 0 broken / scripts 248; the lint with its baseline exits 0 (33 baselined, 0 new); pre-push smoke on the push. Layer: unit, source, the local gate. Not run: anything served.

-- Lead
