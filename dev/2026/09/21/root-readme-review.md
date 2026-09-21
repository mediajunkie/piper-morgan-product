# Root README.md Review — Weekly Docs Audit #1844 (2026-09-21)

**File reviewed**: top-level `/README.md` (49 lines) — the GitHub-facing repository README, distinct
from `docs/README.md` (the pmorgan.ai homepage-facing file, reviewed separately in this session's
handback, not as a saved file per the task instructions).

**Method**: read the full file; diffed against last week's companion review
(`dev/2026/09/14/root-readme-review.md`, Weekly Docs Audit #1801) to see what changed since;
`git log` on `README.md` since that review; cross-checked referenced paths, `pyproject.toml`
(version `0.8.13.0`), and `docs/_config.yml` (Jekyll site exclude list).

## Summary

Root README is in good shape. The one real gap flagged last week (#1801, 2026-09-14) — the
Developer Quick Start snippet missing `.env` setup and the `alembic upgrade head` migration step —
**has already been fixed** (commit `fa0a092e6`, 2026-09-14, same day it was flagged): the inline
snippet was replaced with a pointer to `CONTRIBUTING.md`'s probe-verified sequence. No new
regressions found this week. One pre-existing, already-flagged-but-not-actioned observation
carries forward (external-link framing, below) — still a judgment call, not a defect.

## Findings

### 1. No "NEW:" claims (clean)

`grep -in "new" README.md` returns nothing — no feature-announcement language, stale or otherwise,
to flag.

### 2. No stale version number (clean, N/A)

Root README doesn't quote a version string anywhere, so there's nothing to drift against
`pyproject.toml`'s current `0.8.13.0`. Nothing to check here by design.

### 3. Setup instructions — now current (confirmed fixed since last audit)

"For Developers" (lines 20–26) now reads:

> Full setup steps (including environment configuration and database migration) live in
> **[CONTRIBUTING.md](CONTRIBUTING.md)** — that sequence is probe-verified against a fresh clone
> and is the canonical starting point.

This replaced a drifted inline `git clone` / `docker compose` / `python main.py` snippet that
skipped `.env` setup and the Alembic migration (last week's finding #1). Verified `CONTRIBUTING.md`
exists and its setup section (checked in this session) includes both missing steps. This is the
correct pattern — one canonical setup sequence, not a second copy that can drift — and matches
`ALPHA_QUICKSTART.md`'s equivalent pointer to `CONTRIBUTING.md` for engineers.

Note: this "For Developers" pointer is a **different concern from the hosted-only alpha-testing
model** (#1708). Root README's "For Alpha Testers" section (lines 13–18) already routes testers to
pmorgan.tech / the Alpha Quick Start rather than describing a local install, so it does not
contradict the hosted-only model. "For Developers" describing a local dev setup is expected and
correct — CONTRIBUTING.md itself frames local setup as the engineer/contributor path, not the
tester path.

### 4. External links — pmorgan.tech usage is internally consistent (unchanged from last week, still worth a look)

Root README references `pmorgan.tech` five times (build/docs badges, Quick Start, Documentation
section, Support section) and never mentions `pipermorgan.ai` or the hosted app URL
(`alpha.pipermorgan.ai`). This is unchanged since last week's review, which found the domain
resolves and is internally consistent (not a broken link).

Carried-forward observation (not asserting a fix is needed — still a judgment call, as last week's
review said): a reader following only the root README's "For Alpha Testers" section is routed to
pmorgan.tech for docs, and only reaches the actual hosted-app URL (`alpha.pipermorgan.ai`) after
clicking through to Alpha Quick Start. Given the #1708 hosted-only philosophy ("no clone, no
Docker... time to first use: however long it takes to log in"), the root README could name the app
URL directly rather than adding a hop — but this is cosmetic, not a defect, and was already flagged
without action requested last week. Not re-flagging as new.

### 5. No accidental test content or markdown artifacts (clean)

No TODO/FIXME/lorem-ipsum/placeholder text, no stray code-fence artifacts, no HTML comments left
in. File reads as intentional, finished prose throughout.

### 6. Referenced files/paths all exist (confirmed)

`CONTRIBUTING.md`, `docs/TECHNICAL-DEVELOPERS.md`, `docs/NAVIGATION.md`, `docs/legal/values.md` —
all present. Badge links (GitHub Actions workflow, license) are structurally standard and not
flagged as suspect.

### 7. Brevity / evergreen judgment call

The file stays short (49 lines) and defers essentially all substantive content — quick start,
alpha onboarding, technical reference, architecture — to `pmorgan.tech` or `CONTRIBUTING.md` rather
than duplicating it inline. This is the right shape for a GitHub root README: it doesn't need
pruning or restructuring. No section reads as out of place or as something that should move
elsewhere.

## Not filed as issues

No new issues warranted this week — the one live gap from last week's review is already closed by
commit `fa0a092e6`. Finding #4 (pmorgan.tech-only framing in the alpha-tester section) remains a
non-blocking judgment call, consistent with last week's disposition; leaving it unfiled per that
same reasoning unless PM/Docs wants it revisited.

## Overall assessment

**Pass.** Root README is current, internally consistent, free of stale claims or test artifacts,
and the one real gap found in the prior audit cycle was fixed same-day. No action required this
week.
