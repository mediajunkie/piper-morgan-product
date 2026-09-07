# Root README.md Review — 2026-09-07 (FLY-AUDIT #1725)

**Reviewed**: `/README.md` (repository root, GitHub-view README — distinct from `docs/README.md`,
the pmorgan.tech homepage, which is reviewed separately in this same audit pass).

**Last real edit**: 2026-08-21 (`git log -1 --format="%ai" -- README.md`) — 17 days old at time of
this review, well inside a reasonable currency window for a low-churn top-level file.

## Checklist items and evidence

- **Outdated "new" claims (`NEW:` >2 weeks old)**: `grep -n "NEW:" README.md` — zero hits. File
  does not use "NEW:" markers at all. Clean.
- **External links current and working**:
  - `https://pmorgan.tech` (appears 4x as badge + prose links) — not independently re-curled in
    this pass beyond the docs/README.md check below, but same domain/target verified live there
    (`curl -s -o /dev/null -w "%{http_code}"` → `200`).
  - `https://github.com/mediajunkie/piper-morgan-product` and `.../actions`, `.../issues`,
    `.../discussions` — base repo URL curled directly: **200**.
  - `https://www.apache.org/licenses/LICENSE-2.0` — curled directly: **200**.
  - `https://img.shields.io/badge/...` badge URLs — shields.io badge-rendering endpoints, not
    independently curled (these are dynamically generated badge images, not content pages; not
    meaningfully "broken" in the sense this check cares about).
  - No dead links found among the content links that were checked.
- **Code examples still accurate**: the Quick Start block (`git clone` → `python -m venv venv` →
  `pip install -r requirements.txt` → `docker compose up -d` → `python main.py`) matches the
  corrected flow already verified elsewhere in this audit cycle (SETUP.md's three onboarding
  defects were fixed 2026-09-01, including confirming `python main.py` — not
  `python -m uvicorn web.app:app` — is the real server-start command). Consistent, no drift found.
- **Setup instructions match current process**: `.env.example` is referenced only indirectly here
  (the file doesn't walk through `.env` configuration at all — it defers entirely to
  `docs/TECHNICAL-DEVELOPERS.md` and pmorgan.tech for the full flow). `.env.example` confirmed
  present in the tree via `git ls-files | grep -x '\.env\.example'`. No PIPER.user.md vs
  database-config confusion in this file — it doesn't touch that distinction at all, correctly
  leaving it to the linked Technical Reference.
- **Content is brief and evergreen**: 61 lines total, no sprint-specific or date-specific claims,
  no version number stated (delegates versioning to pmorgan.tech / releases). This is by design —
  the file explicitly routes anyone wanting current state to pmorgan.tech and
  `docs/TECHNICAL-DEVELOPERS.md` rather than duplicating status here. Nothing to go stale.
- **No accidental test content or markdown artifacts**: `grep -n "TODO\|FIXME\|xxx\|XXX\|lorem ipsum" README.md`
  — zero hits. Clean.
- **Linked docs exist**: `CONTRIBUTING.md`, `docs/TECHNICAL-DEVELOPERS.md`, `docs/NAVIGATION.md`,
  `docs/legal/values.md` — all confirmed present via `ls`.
- **No deprecated feature/workflow references**: no mention of `MorningStandupWorkflow` or any
  other retired class/workflow name anywhere in this file (checked via grep across `README.md`
  specifically, not just the general docs/ sweep).

## Verdict

**Clean pass — no findings, no fixes needed.** The root README is intentionally thin (a pointer
document, not a status document), which is exactly why it stays evergreen: it has almost nothing
in it that *can* go stale. No new GitHub issue filed for this file.

**Verified how**: direct grep/curl checks against the live file and live external URLs, as listed
above (method = grep + curl + git log + git ls-files; layer = file content + external link
liveness, not a rendered-page check; denominator = all content links in the file that resolve to
an external URL, all internal doc links the file points to, and the specific checklist items named
above — 8 of 8 sub-items checked).
