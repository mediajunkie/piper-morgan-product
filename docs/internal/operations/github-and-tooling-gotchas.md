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
