---
from: arch
to: lead
cc: exec, host, cio, ppm
date: 2026-11-04 18:35 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1551 and #2188 validated; one lint gap (unresolved env reads, 20 found) to fix first; the 50 sites ruled; #2157 lines need three fixes before the window; #2158's three questions answered"
---

Lead (cc Exec, HOST, CIO, PPM),

All four rulings are in decisions.log at 18:34, with the full per-site list. In short:

**1. #2188 review-issue follow-up (1f7124d641): validated.** 7859 and 7876 match the 16:15 ruling, text unchanged, three pins, Tests green. **New, outside the 13:43 rule as written:** the not-connected reply ("GitHub isn't connected yet…") is an operation not performed. 16 sites in intent_service give it: 14 with `success=True` and 7427 with False. They go False behind a new kind, `NotPerformed.NOT_CONNECTED`, text unchanged, as one family unit. Please file it. It does not block invites.

**2. #1551 (c77eb9bbc2, 600a851938, 4def7f9b0a): matrix and offer pin validated. The lint is validated with one gap, to fix before you start moving modules.**
- **The gap:** a read whose name doesn't resolve (a loop variable, a local, a method's return) is invisible to the lint. I measured 20 in 11 files, including GitHubConfigService's own `GITHUB_TOKEN` loop (config_service.py:221) and its default-repo loop (253), and `{provider}_API_KEY` in llm_config_service (386, 442).
- **Rule:** an unresolved read is a site (`env_name` "unresolved"), baselined and ruled like the rest. Fail closed; don't chase patterns.
- **Also:** key `SYSTEM_ONLY` on (path, env name), so a new name in an already-ruled module still fails.

**3. The 50 sites:**
- **System-only (move them):** JWT, the Postgres reads, the credential-store selector, every OAuth App registration secret (GitHub, Google ×3, Slack client and signing), the MCP consent secret, the shadow LLM key, config_validator's seven, calendar's secrets-file and per-account token-file names, demo, the four `get_authentication_token('system')` calls, and repo_resolver's two (13:16).
- **Conditional:**
  - llm_config_service's four provider keys: cite the pin that a keyless user turn is refused before the env key is reached (#1807/#1320). If no such pin exists, write one.
  - `get_authentication_token(user_id)`: leaves HELPERS once line 221 is a visible ruled site and the #1461 pin is cited.
- **A fix, in #1551's unit:** integration_status_service:300. Calendar says "configured via env" from `GOOGLE_CALENDAR_CREDENTIALS` or `MCP_ENABLED` for a user with no token of their own, and calendar is on the beta set. The env leg should count only for a principal-less call, the shape GitHub's leg already has at 266. Whether alpha sets either name is unverified (it's xian's read, names only).
- **Remove:** `get_default_repository` and `get_allowed_repositories` feed only `get_configuration_summary`, and I found no live consumer. A repo is per-account, so remove these with delete-module-safely rather than ruling them system-only.
- **Stay baselined:** the Slack sites under #1481 and the Notion sites under #2238, behind the offer pin.

**4. #2157 lines: valid against the 16:38 form, with three fixes before HOST asks for the window.**
- (a) Proof 2's shell-2 line carries the drill password, so it also runs in xian's own terminal. It should set `ALEMBIC_DATABASE_URL`: `get_sync_migration_url` reads that name before `DATABASE_URL` (session_factory.py:80).
- (b) `verify_stored_credential_decrypt.py` defaults `--database-url` to `DATABASE_URL`. Inside alpha's container that is alpha's live database, so a dropped or mis-quoted flag proves alpha and prints `ok`. Fix:
  - make the flag required;
  - refuse when its host equals the process's `DATABASE_URL` host;
  - print the code with the word (`fail:2`), since `fly ssh -C` may not pass the exit status back.
  The script changes, so the promotion precondition comes back.
- (c) Add a stop line: never `fly postgres attach` the drill app. Attaching sets `DATABASE_URL` on the target and restarts it, which would boot Piper on the copy.

HOST: both your readings are right. The log is your session log with no data in it. The copy's counts may be lower by what was written after the snapshot, but the earliest user's id and timestamp must match exactly.

**5. #2158 data half:**
- **The MCP app:** it has no volume. Its OAuth rows are in alpha's Postgres, and the plan erases codes, refresh tokens and access tokens by user_id (erase_user.py:200-202). Client registrations have no owner, and the rate counters live only in process memory. The census pin keeps this true.
- **`audit_logs`:** deletion stays. Keeping a security record past an account is a retention policy for xian.
- **N:** read the retention live at the sitting rather than from the 09-22 runbook. The person is told a number of days, in CXO's words.

Verified how: I read 1f7124d641's branches and pins at 7800-7895, the lint in full, the matrix's seams and cells, the offer pin, each of the 50 sites at its line plus its consumers where the ruling turned on them, an AST scan of services+web for unresolved reads (20 of all env reads), the two drill docs, the decrypt script, `get_sync_migration_url`, erase_user.py's plan and census, and fly.mcp.toml. Alpha `/health` at 18:33: `9824d7d5b2`, healthy. Layer: source, CI status, health page. Not run: the unit tests (no venv on this seat; Tests is green on main), and nothing on Fly or alpha.

-- Arch
