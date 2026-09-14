# Root README.md Review — Weekly Docs Audit #1801 (2026-09-14)

Scope: top-level `/README.md` (distinct from `docs/README.md`, the pmorgan.tech homepage
content, reviewed separately). Read against `CLAUDE.md`'s "Critical Paths" section,
`CONTRIBUTING.md`, `docs/README.md`, and `pyproject.toml` as ground truth for what's current.

## Summary

Root README is generally in good shape — no "NEW:" claims, no accidental test content, no
markdown artifacts, no stale version numbers (it doesn't quote a version number at all, so
nothing to drift). One real finding: **the Developer Quick Start is missing two required setup
steps that both `CONTRIBUTING.md` and `docs/README.md` include**, which would leave a fresh
clone with no working database.

## Findings

### 1. Developer Quick Start is missing `.env` setup and the DB migration step (real gap)

`README.md` lines 20–37 ("For Developers"):

```bash
# Clone and setup
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv venv && source venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start infrastructure
docker compose up -d

# Run the application
python main.py
```

Compare to `CONTRIBUTING.md` lines 65–86 (the canonical engineer setup path since #1708,
2026-08-31, "probe-measured... not assumed") and `docs/README.md` lines 71–86, both of which
include:

```bash
cp .env.example .env
...
alembic upgrade head
```

Root README has neither. Without `cp .env.example .env`, there's no local env file for the
Anthropic/GitHub keys (`.env.example` exists at repo root and is the documented starting point
everywhere else). Without `alembic upgrade head`, `docker compose up -d` brings up an empty
Postgres 14 container with no schema, and `python main.py` would hit against an unmigrated DB.
CONTRIBUTING.md's version is annotated "probe-measured (Lead, 2026-08-31 fresh-clone test)" —
i.e., someone actually verified that exact sequence works end-to-end; root README's shorter
version has not been verified against that same bar and is missing steps that sequence found
necessary.

**Suggested fix**: either replace the root README snippet with (or link directly to) the
CONTRIBUTING.md 1b sequence, since CONTRIBUTING.md is already the canonical engineer-setup
doc per the #1708 ruling (ALPHA_QUICKSTART.md explicitly says "local setup now lives [in
CONTRIBUTING.md], not here" — root README should follow the same pointer rather than
maintaining a second, drifted copy of the same steps).

### 2. No "NEW:" claims found

`grep -in "new:" README.md` returns nothing. No stale feature-announcement language to flag.

### 3. No stale version number

Root README doesn't quote a version number anywhere (no `v0.8.x` string), so there's nothing to
compare against `pyproject.toml`'s `version = "0.8.11.0"`. Not a defect — just noting the check
was run and came back clean because there's no version claim to go stale.

### 4. External links — pmorgan.tech usage is internally consistent but the README conflates "read the docs" with "use the app"

Root README references `pmorgan.tech` five times (build badge, docs badge, Quick Start,
Documentation section, Support section) and never mentions `pipermorgan.ai` or
`piper-morgan.fly.dev`. `pmorgan.tech` itself resolves fine (`curl -o /dev/null -w '%{http_code}'
https://pmorgan.tech` → `200`), so this is not a broken link.

However, per `docs/ALPHA_QUICKSTART.md` (rewritten 2026-08-31 per #1708), the actual hosted app
alpha testers use lives at **`piper-morgan.fly.dev`**, not `pmorgan.tech` (which serves the
`docs/README.md` documentation content, not the product). Root README's "For Alpha Testers"
section (lines 13–18) says:

```
If you're part of the Piper Morgan alpha program, go to [pmorgan.tech](https://pmorgan.tech) for:
- Alpha Quick Start
- Testing Guide
- Known Issues & Workarounds
```

This is technically correct — pmorgan.tech is where the *linked docs* live — but a tester
following only the root README never sees the actual app URL (`piper-morgan.fly.dev`) until they
click through to Alpha Quick Start. Not a broken link or factual error, but worth a note: if the
goal is fastest-path-to-using-the-app (which is the whole point of the #1708 rewrite — "no
clone, no Docker... time to first use: however long it takes to log in"), the root README could
say so directly rather than routing every alpha tester through an extra hop. Judgment call for
Docs/PM — flagging, not asserting this needs a fix.

### 5. Referenced files all exist

Confirmed present: `CONTRIBUTING.md`, `docs/TECHNICAL-DEVELOPERS.md`, `docs/NAVIGATION.md`,
`docs/legal/values.md`, `requirements.txt`, `.env.example`. No dead links to internal repo
paths.

### 6. Recent history

`git log -3 -- README.md` shows the most recent touches were license-related (2026-08-13 Apache
2.0 adoption, 2026-08-16/08-21 legal follow-ups) — no one has touched the Developer Quick Start
section itself since before those passes, which is consistent with finding #1 above having gone
unnoticed (the legal edits were scoped to the badge/license lines, not the setup steps).

## Not filed as issues

Per audit instructions, this doc reports findings only — Docs (or whoever picks this up) should
decide whether #1 warrants a tracked issue (recommended, since it's a genuine "fresh clone
won't work" gap) and whether #4 is worth a copy tweak or is fine as-is.
