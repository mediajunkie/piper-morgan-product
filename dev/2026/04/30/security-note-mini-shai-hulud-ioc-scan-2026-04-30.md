# Security Note — Mini Shai-Hulud IoC Scan

**Date**: 2026-04-30
**Verdict**: ✅ NO INDICATORS OF COMPROMISE on `mediajunkie/piper-morgan-product` repo or `mediajunkie` GitHub account
**Trigger**: Unsolicited warning email to `xian@pobox.com` claiming PM's GitHub account compromised
**Investigator**: Lead Developer (Claude Code), per CEO direction Apr 30 ~13:30 PT
**Scope**: This repo's working tree on `xian@cool` machine + full repo list on `github.com/mediajunkie`

---

## The threat (real)

**Mini Shai-Hulud** is the third wave of the Shai-Hulud worm campaign targeting npm packages. Detected by StepSecurity on April 29, 2026. Documented at:

- https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared

### Confirmed-compromised packages

All four are SAP enterprise development tools:

- `mbt@1.2.48`
- `@cap-js/sqlite@2.2.2`
- `@cap-js/postgres@2.2.2`
- `@cap-js/db-service@2.10.1`

### Attack mechanism

`preinstall` hooks in the compromised packages download the Bun JavaScript runtime and execute an 11.6 MB obfuscated payload that harvests developer credentials. Persistence is established via:

- `.claude/settings.json` SessionStart hook
- `.vscode/tasks.json` with `runOn: "folderOpen"`
- `.claude/execution.js` (11.6 MB payload copy)
- `setup.mjs` at project root (SHA-256: `4066781fa830224c8bbcc3aa005a396657f9c8f9016f9a64ad44a9d7f5f45e34`)

Exfiltration is via the victim's own GitHub account: malware creates Dune-themed repos (`sardaukar-sandworm-NNN`, `fremen-ornithopter-NNN`, etc.) with the description **"A Mini Shai-Hulud has Appeared"** to host stolen credentials.

### Targeted credentials

- npm tokens (`npm_[A-Za-z0-9]{36,}`)
- GitHub PATs / OAuth tokens
- AWS / GCP / Azure credentials
- SSH keys, Kubernetes tokens, cryptocurrency wallets

---

## The warning email (legitimate-shaped, but false-positive)

**From**: `chillax4nothing@gmail.com` (real Gmail account; SPF/DKIM/DMARC all PASS)
**To**: 13 BCC'd recipients including `xian@pobox.com`
**Sent**: 2026-04-30 16:03 EDT (delivered after 16s; spam score 0.0)
**Subject**: "Your GitHub Account maybe compromised - Please read"

**Email's claim**: *"my python script detected your github account as compromised because of a node module attack. I found a suspicious repository on your GitHub account that was created by the malware, not you. Your email was on your GitHub profile, so I'm reaching out."*

**Email's recommended actions** (cross-checked against StepSecurity's published guidance):

1. Delete any repos you don't recognize, especially with description "A Mini Shai-Hulud has Appeared"
2. Change all passwords and tokens (GitHub, npm, AWS/Azure/GCP, SSH keys, anything developer-related)
3. Delete `node_modules` and reinstall with `--ignore-scripts`
4. Check for hidden files: `.claude/settings.json`, `.claude/execution.js`, `.vscode/tasks.json`

**Verdict on the email**: most plausibly a wide-cast warn-everyone-with-X-feature outreach with low-precision detection (likely flagging any GitHub account that has a `.claude/` directory in any repo). Not phishing per se — the URL points to the real StepSecurity blog, not a phishing landing page — but the personal-detection claim is not corroborated by IoC scan.

---

## IoC scan results — all dimensions CLEAN

### Local repo (working tree)

| # | Dimension | Expected if compromised | Actual | Result |
|---|---|---|---|---|
| 1 | `.claude/settings.json` SessionStart hook target | Points to `.claude/execution.js` or runs `bun` payload | Points to `bash .claude/hooks/session-start.sh` (legitimate, hand-edited Apr 28) | ✅ Clean |
| 2 | `.claude/execution.js` exists? | Yes (11.6 MB obfuscated payload) | File does NOT exist | ✅ Clean |
| 3 | `.vscode/tasks.json` `runOn:folderOpen` task | Present, executes payload | No `runOn`, no `folderOpen`, no `bun` references | ✅ Clean |
| 4 | Top-level `setup.mjs` | Present at project root | File does NOT exist | ✅ Clean |
| 5 | "Mini Shai-Hulud" string anywhere in repo | Present in malware-created repo descriptions | Zero matches across all tracked files | ✅ Clean |
| 6 | `execution.js` or `setup.mjs` files anywhere | Present | Zero matches | ✅ Clean |
| 7 | Dune-themed branch names (sardaukar/mentat/fremen/sandworm/ornithopter/etc.) | Present as malware branch | Zero matches; only branch unfamiliar-to-investigator (`test-coverage-augmentation`) is authored by PM and contains legitimate test-coverage work | ✅ Clean |
| 8 | Recent commit authors (since 2026-04-25) | Mix of unknown authors | All `3227378+mediajunkie@users.noreply.github.com` (PM's GitHub no-reply email) | ✅ Clean |
| 9 | `package.json` files reference any of the 4 compromised packages | Present in dependencies | All `package.json` files (project root + tests/frontend + worktrees + skunkworks/mobile) — zero matches for `mbt`, `@cap-js/sqlite`, `@cap-js/postgres`, `@cap-js/db-service` | ✅ Clean |
| 10 | `.claude/settings.local.json` content | Malicious permission grants | Legitimate hand-edited Claude Code permissions (Bash venv/pytest/git/etc.) | ✅ Clean |

### GitHub account `mediajunkie` (full sweep)

| # | Dimension | Expected if compromised | Actual | Result |
|---|---|---|---|---|
| 11 | Total repos | Includes malware-created repos | 22 repos total; all recognizable PM work | ✅ Clean |
| 12 | Repos with description matching "Mini Shai-Hulud" or "Shai-Hulud has Appeared" | ≥1 | **0 matches** | ✅ Clean |
| 13 | Repos with Dune-themed names (regex: `sardaukar|mentat|fremen|sandworm|ornithopter|harkonnen|atreides|gurney|stilgar|jessica|paul|leto|chani|caladan|arrakis|bene-gesserit|kwisatz|muad|shaddam|piter|duncan|thufir`) | ≥1 | **0 matches** | ✅ Clean |
| 14 | 15 most recent repo creations | Includes malware-created | All recognizable: nyt-crossword, rebel-alliance-11ty-site, openlaws, va-workspace, dispatch, piper-morgan-website, github-projects-gantt, piper-morgan-product, test-piper-morgan, piper-morgan-poc, mediajunkie, handbook, ezone, civictech.club, optilisten | ✅ Clean |

---

## What this rules out

- This repo is not infected.
- PM's GitHub account does not host any malware-created exfiltration repos.
- Recent commit history shows only PM's own work; no unauthorized author has pushed.
- The compromised SAP packages are not in any `package.json` in this repo or its worktrees.

## What this does NOT rule out

- This investigation only covers `xian@cool` machine + `github.com/mediajunkie` account. If PM uses other Mac/Linux machines with shared GitHub auth, those should be checked separately (look for `.claude/execution.js`, `setup.mjs`, malware-named repos pushed from those machines).
- If PM has any non-Piper-Morgan side projects that use npm with the 4 SAP packages, those projects should be checked separately.
- The sender's claim of an existing suspicious repo could refer to a deleted-then-warned situation; a `gh repo list` only shows current state. But: GitHub does keep deleted-repo audit traces; if PM ever wants to verify history, the GitHub Account → Security log + `gh api /user/audit-log` would surface deletions.

## Recommended posture

**Don't blanket-rotate credentials** — the email's "change all passwords and tokens" instruction is reasonable IF compromised, wasteful otherwise. With clean IoC scan, this is wasteful.

**Do — low-cost hardening worth doing regardless**:

1. **Vigilance**: any future Claude Code session that sees `.claude/execution.js` appear, or a top-level `setup.mjs` appear, or branches/repos with the Dune-themed naming pattern → treat as high-priority security incident immediately.
2. **Pin npm versions** in `package.json` files for any active JS work; run `npm install --ignore-scripts` if you're paranoid about preinstall-hook attacks. The current `package.json` files in this repo are mostly inert (root `package.json` is for tooling; `skunkworks/mobile` and `tests/frontend` have npm deps but small surfaces).
3. **GitHub audit log review** (optional): `gh api /user/audit-log --paginate | grep -i create_repo` would show the chronological repo-creation log; if anything suspicious is in there even if currently deleted, this would surface it. Not required given the clean current-state scan.

## Files referenced

- This note: `dev/2026/04/30/security-note-mini-shai-hulud-ioc-scan-2026-04-30.md`
- StepSecurity blog: https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared
- Original email: stored in PM's email; Message-ID `<CABHH7pn=Gv3x0rm95tGcuYbETamH3JMf0UnOMW8GwxvPwK1Ljg@mail.gmail.com>`

— Lead Developer, 2026-04-30 14:15 PT
