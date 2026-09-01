# GitHub and Tooling Gotchas

Incident-sourced reference for high-severity, no-undo failure modes. Rules summarized in `CLAUDE.md`; full detail here.

---

## SSH over port 443

**When**: `git push` / `git fetch` hangs or returns `ssh: connect to host github.com port 22: Operation timed out`. Common on conference Wi-Fi, hotel networks, and some corporate firewalls.

**Fix** (one-time per machine):
```bash
ssh-keyscan -t rsa,ed25519 -p 443 ssh.github.com 2>/dev/null >> ~/.ssh/known_hosts
```

Then prefix git operations:
```bash
GIT_SSH_COMMAND="ssh -p 443" git -c url.'git@ssh.github.com:'.insteadOf='git@github.com:' push origin main
```

Non-destructive — uses a different route for that invocation only; doesn't change repo or SSH config. Log the workaround in your session log so other agents on the same network know it works.

---

## GitHub Projects v2: NEVER full-replace a single-select field option list

**Severity**: No undo path. This wiped sprint assignments for all 1175 items on the "Building Piper Morgan" project board on 2026-07-05.

**What happens**: `updateProjectV2Field`'s `singleSelectOptions` argument is a **full replace**, not an additive merge. Submitting the complete option list back — even with every existing option's name/color/description faithfully reproduced — causes GitHub to treat every option as newly created, silently detaching every item's stored reference to the old option IDs. The item's field value doesn't become wrong or hidden — it becomes genuinely empty.

**There is no API undo path.** No version history is exposed for Projects v2 custom fields.

**Safe approach**: Add options through the GitHub web UI (Project → field settings → add option). This is additive and doesn't touch existing item assignments. If you must use the API, test against a throwaway field on a brand-new project first — never assume "this succeeded on something similar" means it's safe here.

**Backup and restore path** (built 2026-07-12):
- `scripts/snapshot-project-board.sh` writes a dated full-board snapshot to `dev/snapshots/project-board-YYYY-MM-DD.tsv` — run after any batch of Sprint-field changes.
- `scripts/restore-sprint-field-from-snapshot.py` compares live state to the most recent snapshot and restores drift (dry-run by default; `--apply` to execute).

**Decision record**: `docs/internal/planning/sprint-recovery-decisions-log.md` — read this before re-deriving anything by hand if this happens again.

---

## GitHub commit messages: auto-close ignores negation

**What happens**: GitHub auto-closes any issue referenced by a `close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved` keyword immediately adjacent to `#N` in a commit message pushed to the default branch — via plain keyword matching, not semantic understanding. It cannot distinguish "resolved #1278" from "**not yet** resolved: #1278". Both silently close the issue.

**Incident**: 2026-07-04/05 (PPM) — a commit message explicitly trying to say the opposite ("Flagged, not yet resolved: #1278...") closed a live, unfinished Beta Blocker.

**When referencing an issue you do NOT want to close**: avoid putting a close/fix/resolve-family word immediately before `#N`. Rephrase — "issue #1278 still needs..." or "#1278 remains open" — or write the number without `#` (`issue 1278`) if you need the keyword nearby.

**After any commit referencing an issue you meant to leave open**: `gh api repos/mediajunkie/piper-morgan-product/issues/N --jq .state` — costs nothing to verify.

**If you discover an accidental close**: `gh issue reopen N` immediately. Also scan recent commit messages for the same pattern — a single bad phrasing habit tends to repeat in a session.

---

## Keychain credential storage — use `KeychainService`, not `security` CLI

**What happens**: `KeychainService.store_api_key(provider, value)` stores credentials under service name `"piper-morgan"` and account name `f"{provider}_api_key"` — the `_api_key` suffix is appended automatically. Storing via `security add-generic-password` with a different account name makes the credential invisible to the server.

**Incident**: 2026-05-20 — PM stored `slack_client_id` via `security` CLI; the server's OAuth init couldn't find it. Failure mode looked like "Please specify client_id" from Slack. Two migration passes were needed.

**Correct way** (from a venv-aware Python shell):
```bash
./venv/bin/python -c "
from services.infrastructure.keychain_service import KeychainService
KeychainService().store_api_key('slack_client_id', '<value>')
"
```

**Correct way via `security` CLI** (if you must — keep the `_api_key` suffix):
```bash
security add-generic-password -U -s "piper-morgan" -a "slack_client_id_api_key" -w "$VAL"
```

**Verify what the server actually sees**:
```bash
./venv/bin/python -c "
from services.infrastructure.keychain_service import KeychainService
k = KeychainService()
for p in ['slack_client_id', 'slack_client_secret', 'notion', 'github']:
    v = k.get_api_key(p)
    print(f'{p}: present={bool(v)} len={len(v) if v else 0}')
"
```

**User-scoped credentials** (Slack bot/user tokens, per ADR-058): `KeychainService.store_api_key(provider, value, username=user_id)`. Account name becomes `f"{user_id}_{provider}_api_key"`. Same gotcha; same fix.

## Amber billing hazard: never export `ANTHROPIC_API_KEY` host-wide (shell profile / launchctl)

*(Relocated 2026-08-13 from `docs/setup/llm-api-keys-setup.md`, where it had been written for the
wrong audience — a visitor-facing setup doc; Comms caught it in the docs-site register pass,
commit `285f2a0c1` has the removal. Original warning, Pard 2026-08-05, preserved verbatim below;
it had no other home in the repo.)*

> ⚠️ **Never use a shell-profile or `launchctl setenv` export of `ANTHROPIC_API_KEY` on Amber (or
> any shared multi-session host).** Claude Code reads `ANTHROPIC_API_KEY` from the environment, so
> a host-wide export silently redirects **every resident session's** billing off the Max
> subscription onto metered API — no error, no signal until the Console bill. On Amber use
> KeychainService only. *(Pard, 2026-08-05; verified clean at time of writing — prevention, not
> remediation.)*

Related but distinct from CLAUDE.md's `ANTHROPIC_API_KEY` warning: that one covers the transient
shell-*inherited* empty key shadowing the server's credential resolution; this one covers a
*persistent host-wide* export capturing every session's billing. Both resolve to the same rule —
credentials go through KeychainService, never the environment, on shared hosts.

---

## Windows: `git clone` fails with "Filename too long"

**When**: Cloning this repo on Windows fails partway through with errors like
`error: unable to create file mailboxes/.../some-very-long-memo-name.md: Filename too long`.

**Why**: Windows' effective `MAX_PATH` is 260 characters, counting the full path INCLUDING the
clone-destination prefix (e.g. `C:\Users\alexandra\Documents\GitHub\piper-morgan-product\`, often
50-90 characters on its own). Cohort mailbox memo filenames are long by convention (they encode
sender, recipients, and subject inline) — some existing `mailboxes/` paths already exceed 250
characters on their own, which overflows the Windows budget once the clone prefix is added. This
was caught by the `windows-clone-test` job (now in `.github/workflows/windows-test.yml`; ported
2026-08-13 from the retired always-red `ci.yml`, where the same red had been invisible for
unrelated reasons). See #1616.

**Fix (the practical 90% fix — no repo change needed)**: git-for-windows supports long paths;
it's just off by default. Enable it per-repo or globally:
```
git config --global core.longpaths true
```
This alone is often enough. If clone still fails, Windows itself also needs long-path support
enabled at the OS level (Windows 10 version 1607+ / Windows 11, admin PowerShell, one-time,
requires reboot):
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
Both settings are opt-in and non-destructive — enabling them doesn't change anything about the
repo itself, only what the local Windows filesystem/git client will accept.

**What the repo does going forward**: `scripts/mailbox_filename_lint.py` (wired into `lint.yml`,
`.mailbox-filename-lint-baseline.txt` for the ratchet) blocks new `mailboxes/` paths over 180
characters, so the problem stops getting worse. Existing long filenames are **intentionally left
as historical record**, not renamed — per #1616's recommendation, only rename them if a real
Windows contributor needs to work in the repo and the workaround above genuinely doesn't cover
their case.

## Four instrument-integrity gotchas from the 2026-08-29 → 08-31 arc (Lead)

**mypy gate counts are toolchain-AND-platform sensitive.** The ratchet's numbers are only
meaningful under the CI-pinned bare venv (mypy==2.3.0 + the pinned lib set); a dev venv inflates
counts (more imports resolve). Even the pinned venv on macOS reads ±1 off CI's ubuntu on 4 codes.
Deltas with per-file attribution are the reliable local measure; CI is the sole authority on
absolutes. (Found during the #1436 drift fix; reconfirmed byte-identical across three disposal
batches.)

**A reload=False dev server is a SNAPSHOT, not "the dev server."** Its memory is the code at its
start time; disk moves on without it. Any verification against it is meaningless without
comparing the process start time to the fix's merge time. A stale server can only produce false
FAILS for post-start fixes — never false passes — which is also the recovery logic when one is
discovered late. (17-day-stale instance found by Web 08-30; explained a "resolver bug" entirely.)

**Restarting the server: kill by PORT, verify by NEW-PID + START-TIME.** On macOS the venv
symlink resolves, so the process cmdline shows the framework Python — `pgrep -f "venv/bin/python"`
matches NOTHING, `kill` of the resulting empty var no-ops silently, the replacement server dies
on the occupied port inside nohup, and `curl /health` answers green FROM THE OLD PROCESS. Three
silent layers, one false restart (twice in one day, 08-30). Correct procedure:
`kill $(lsof -ti:8001)` → verify port EMPTY → relaunch → verify the port's new owner has a fresh
start time (`ps -p $(lsof -ti:8001) -o lstart=`). Bare /health cannot distinguish old from new.

**macOS Keychain ACL hang on rebuilt venvs** (#1711 tracks the code fix): a NEW python binary
requesting an EXISTING keychain item blocks indefinitely and silently in SecItemCopyMatching
("Validating LLM providers..." then nothing, 0% CPU — the permission dialog is GUI-only).
Truly-fresh machines are fine (no item → falls through to the /setup wizard). Workarounds: click
Always Allow once at the dialog, or PIPER_CREDENTIAL_STORE=db. Bites anyone who rebuilds a venv
on a machine that has run the setup wizard.
