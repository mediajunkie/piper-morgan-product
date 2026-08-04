# cut-release

Execute a Piper Morgan release. Companion skill to `docs/internal/operations/release-runbook.md` — the runbook is the reference; this skill is the executable procedure that makes doc-body updates non-skippable.

**Primary failure mode this skill prevents**: bumping the version header without updating the prose body (What's New, Testing Focus, What's Working). These are distinct tasks; the skill treats them as such.

## When to Use

When PM says "cut a release", "cut v0.8.X", or "do a release". Always invoke this skill — do not work from memory.

## Inputs You Need Before Starting

- **NEW_VERSION** — e.g. `0.8.8`
- **PREV_VERSION** — e.g. `0.8.6` (the version currently in the files)
- **CUT_COMMIT** — the git commit hash the release is cut from
- **MILESTONE** — what sprint/milestone this covers, e.g. "D1/RECONNECT"
- **PREV_TAG** — the previous git tag, for commit log range

If any of these are unclear, ask PM before starting. A release cut on the wrong commit or wrong version is hard to undo.

---

## Phase 1 — Pre-flight (do not skip)

**⭐ #1413 CONTENT-PARITY GATE (added 2026-08-04)**: run `scripts/check-release-parity.sh`
FIRST. A "full-parity" claim is a statement about a *moment* (the 7/16 incident: the claim
aged 48 minutes and silently dropped a live login fix → two-day latent login regression).
The script refuses on any unexplained content gap between the release ref and origin/main;
intentional exclusions go in `release-exclusions.txt` AND the release notes verbatim —
empty diff or explained lines, never silent gaps.

```bash
# 1. Confirm cut commit
git log --oneline {PREV_TAG}..HEAD | head -20
# Identify the commit that closes the milestone gate

# 2. Confirm tests
python -m pytest tests/ --collect-only -q 2>/dev/null | tail -3
# Record: N tests collected

# 3. No open P0 blockers
gh issue list --label P0 --state open --repo mediajunkie/piper-morgan-product
# Expected: empty
```

Stop and surface to PM if: cut commit is ambiguous, tests are broken, P0 is open.

---

## Phase 2 — Version bump + release notes

### pyproject.toml
```bash
# Change: version = "{PREV_VERSION}" → version = "{NEW_VERSION}"
# Verify: grep "^version" pyproject.toml
```

### Create release notes
File: `docs/releases/RELEASE-NOTES-v{NEW_VERSION}.md`

Write it fresh — do not copy-paste the previous release notes. Required sections:
- Summary (2-3 sentences: what milestone, quality posture, test count)
- What's New (organized by theme, each item links to its issue)
- Known limitations (honest — what's still rough for alpha testers)
- Version mechanics (cut commit, tag, pyproject note if applicable)
- Upgrade instructions

---

## Phase 3 — Documentation updates (THE HIGH-FAILURE ZONE)

Work through this list in order. For each file: **read it first**, then make the specified changes. Do not treat "update version" as sufficient for any file that has body content.

### 3a. docs/releases/README.md
- [ ] "Current Version" line → NEW_VERSION
- [ ] Add row to Release History table (version, date, type, highlights)
- [ ] Update "Last updated" date

### 3b. docs/ALPHA_QUICKSTART.md
**Two separate tasks — do not conflate:**

**Task 1 — version strings** (grep-able):
- [ ] Header `**Version**: X.Y.Z` → NEW_VERSION
- [ ] Footer "This is alpha software (X.Y.Z)" → NEW_VERSION
- [ ] "Last Updated" date → today

**Task 2 — prose body** (requires rewriting, not just find/replace):
- [ ] **"What's New" section**: rewrite entirely. Describe the features that shipped in THIS release, in plain language a developer-tester will understand. Do not leave the previous version's feature descriptions. Each bullet should describe a real user-facing change.
- [ ] **"Testing Focus" section**: rewrite entirely. What should testers pay attention to in THIS release? What's newly shipped and needs eyes?
- [ ] **"What's Working" section**: update to reflect current capabilities. Remove features that have been superseded; add what's genuinely stable in THIS release.

**Verification**: after editing, `grep -n "0\.8\." docs/ALPHA_QUICKSTART.md` — all version references should be NEW_VERSION. Read the What's New section and ask: does this describe what THIS release ships, or the previous one?

### 3c. docs/ALPHA_TESTING_GUIDE.md
- [ ] Header version + Last Updated
- [ ] **"What's New" section**: rewrite for THIS release (same discipline as Quickstart)
- [ ] **"Testing Focus"**: update for what's new to test
- [ ] Footer version

### 3d. docs/ALPHA_KNOWN_ISSUES.md
- [ ] Header version, title line `(vX.Y.Z)`, Last Updated
- [ ] Check GitHub for open bugs: `gh issue list --label bug --state open`
- [ ] Move any fixed issues OUT of Known Issues
- [ ] Add any newly discovered issues
- [ ] Update "Needs Testing" for this release
- [ ] Keep under 200 lines (if longer, content is misplaced)

### 3e. docs/ALPHA_AGREEMENT_v2.md
Version appears in 3 places — find all three:
```bash
grep -n "0\.\|version\|Version" docs/ALPHA_AGREEMENT_v2.md | grep -i "version\|0\."
```
- [ ] Header version
- [ ] Body mention (~line 15)
- [ ] Footer mention (~line 153)

### 3f. docs/briefing/BRIEFING-CURRENT-STATE.md
- [ ] STATUS BANNER version
- [ ] Last Updated date
- [ ] Add row to Version History table
- [ ] Update Release Notes link at bottom

### 3g. docs/operations/alpha-onboarding/email-template.md
- [ ] Version in header
- [ ] Version in body text (may appear multiple times)
- [ ] Footer version / "Last Updated"

### 3h. docs/versioning.md (if it exists)
```bash
ls docs/versioning.md docs/VERSION_NUMBERING.md 2>/dev/null
```
- [ ] "Current Version" at top → NEW_VERSION
- [ ] Add row to Version History table
- [ ] Footer date

### 3i. docs/README.md
- [ ] Release notes quick link (line ~18) → new version

---

## Phase 4 — Git ops

```bash
# Fix newlines
./scripts/fix-newlines.sh

# Stage with explicit paths (never git add -A)
git add pyproject.toml \
  docs/releases/RELEASE-NOTES-v{NEW_VERSION}.md \
  docs/releases/README.md \
  docs/ALPHA_QUICKSTART.md \
  docs/ALPHA_TESTING_GUIDE.md \
  docs/ALPHA_KNOWN_ISSUES.md \
  docs/ALPHA_AGREEMENT_v2.md \
  docs/briefing/BRIEFING-CURRENT-STATE.md \
  docs/operations/alpha-onboarding/email-template.md \
  docs/versioning.md \
  docs/README.md

git diff --cached --name-only   # Verify: only expected files

git commit -m "release: v{NEW_VERSION} — {MILESTONE}"

# Tag at cut commit (not HEAD if different)
git tag -a v{NEW_VERSION} {CUT_COMMIT} -m "Release v{NEW_VERSION} — {MILESTONE}"
# If cutting at HEAD:
git tag -a v{NEW_VERSION} HEAD -m "Release v{NEW_VERSION} — {MILESTONE}"

git push origin main
git push origin v{NEW_VERSION}
```

---

## Phase 5 — Production branch

**⭐ #1413 DEPLOY-SOURCE RULE (added 2026-08-04)**: an env must never be NEWER than its
release lineage — that masking is what made the 7/16 gap invisible (a worktree deploy
carried a fix `production` lacked; the next `production` deploy silently regressed it).
Two compliant modes, pick per context and say which:
- **Release window**: hosted deploys come from `production` only.
- **Lockstep mode** (the ratified beta-cadence norm — main==production): deploys from
  main are fine **IFF `production` is fast-forwarded in the same session**
  (`git push origin HEAD:production`) so lineage can never silently diverge. The parity
  script doubles as the check: run it after any lockstep deploy; it must say PARITY OK.

```bash
# Fast-forward production to this release
git push origin HEAD:production --force
# (force needed if a prior stamp commit exists on production that isn't on main)
```

---

## Phase 6 — GitHub Release

```bash
gh release create v{NEW_VERSION} \
  --title "v{NEW_VERSION} — {MILESTONE}" \
  --notes-file docs/releases/RELEASE-NOTES-v{NEW_VERSION}.md \
  --latest
```

---

## Phase 7 — Post-release audit (do not skip)

### Version string audit
```bash
# Scan for any docs still referencing PREV_VERSION (excluding historical release notes)
grep -r "{PREV_VERSION}" docs/ --include="*.md" | grep -v "docs/releases/"
```
Any hits are stale. Update them.

### Content accuracy audit
Read each of these sections and confirm they describe THIS release, not the previous one:

| Doc | Section to read | What to verify |
|-----|-----------------|----------------|
| ALPHA_QUICKSTART | What's New | Features are from THIS release |
| ALPHA_QUICKSTART | What's Working | Capabilities list is current |
| ALPHA_QUICKSTART | Testing Focus | Reflects what's newly shipped |
| ALPHA_TESTING_GUIDE | What's New | Same check |
| ALPHA_KNOWN_ISSUES | Known Issues | Fixed issues removed; new issues added |

If any section still describes old functionality: fix it now, before the release is done.

### Deployment
```bash
# Surface to PM: production branch is at v{NEW_VERSION}
# Deployment to alpha.pipermorgan.ai is a manual step on the Droplet
# See: docs/internal/operations/alpha-deployment-runbook.md
```

---

## Completion matrix

Paste this into your session log when done:

```
## Release v{NEW_VERSION} Completion Matrix

Phase 1 — Pre-flight
- [ ] Cut commit identified: {CUT_COMMIT}
- [ ] Tests passing: N collected
- [ ] No open P0s

Phase 2 — Version bump
- [ ] pyproject.toml bumped
- [ ] Release notes written (not copy-pasted)

Phase 3 — Documentation
- [ ] docs/releases/README.md
- [ ] docs/ALPHA_QUICKSTART.md — version strings AND prose body
- [ ] docs/ALPHA_TESTING_GUIDE.md — version strings AND prose body
- [ ] docs/ALPHA_KNOWN_ISSUES.md
- [ ] docs/ALPHA_AGREEMENT_v2.md (3 places)
- [ ] docs/briefing/BRIEFING-CURRENT-STATE.md
- [ ] docs/operations/alpha-onboarding/email-template.md
- [ ] docs/versioning.md
- [ ] docs/README.md

Phase 4 — Git ops
- [ ] Committed with explicit paths
- [ ] Tag created at cut commit
- [ ] Pushed to main + tag

Phase 5 — Production branch
- [ ] production fast-forwarded to v{NEW_VERSION}

Phase 6 — GitHub Release
- [ ] gh release create v{NEW_VERSION} published

Phase 7 — Audit
- [ ] Version string grep: no stale hits
- [ ] Content accuracy: What's New sections describe THIS release
- [ ] Deployment surfaced to PM (Droplet — manual step)
```

---

## Anti-patterns

| Don't | Why |
|-------|-----|
| Bump version string only, skip prose | "Update version" means TWO tasks: number + body. The body is the one that rots. |
| Copy-paste release notes from last release | Testers read these. Stale notes erode trust. |
| `git add -A` or `git add docs/` | Sweeps stale untracked files into the commit. Explicit paths only. |
| Skip the content accuracy audit | The grep catches version strings; the audit catches stale prose. Both required. |
| Call the release done without a GitHub Release | The tag is internal; the GitHub Release is what testers see. |

---

## Changelog

- **v1.0** (2026-06-20, PA): Initial skill. Created after ALPHA_QUICKSTART was discovered with stale body content post-v0.8.8 release — version header bumped but "What's New", "Testing Focus", and "What's Working" sections still described v0.8.6 features. Root cause: runbook listed "Update Version and 'What's New' section" as one checkbox item; under time pressure it read as one action (bump the number). This skill splits them explicitly and makes prose rewrites non-skippable.
