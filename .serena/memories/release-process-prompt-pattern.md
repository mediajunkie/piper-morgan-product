# Release Process Prompt Pattern

## Problem Solved

On 2026-01-15, we discovered that v0.8.4.2 was released (code, tag, GitHub release) without following the release runbook. Documentation was missed:
- Release notes not created
- docs/README.md not updated
- docs/releases/README.md index not updated
- docs/versioning.md still showed 0.8.1

## Root Cause

The release runbook existed but wasn't invoked during "quick fix then release" flow. Claude Code agents need explicit instruction to follow the runbook.

## Solution: Prompt Pattern for Releases

When requesting a release, PM should use this prompt:

> "Cut a release for v0.8.X.Y. Follow the release runbook at docs/internal/operations/release-runbook.md step by step."

This ensures:
1. Agent reads the entire runbook first
2. Follows every step sequentially
3. Does not skip documentation updates

## Mandatory Documentation (per runbook v1.3)

Every release MUST update these files (complete inventory):

### Release Notes (4 files)
- `pyproject.toml` - version bump
- `docs/releases/RELEASE-NOTES-vX.Y.Z.md` - create new file
- `docs/releases/README.md` - update index (Current Version, Release History table, Last updated)
- `docs/README.md` - update release notes link
- `docs/versioning.md` - update Current Version, Version History table, Last updated

### Alpha Documentation (4 files)
- `docs/BETA_TESTING_GUIDE.md` - Version and Last Updated in header
- `docs/BETA_KNOWN_ISSUES.md` - Version, Last Updated, and title
- `docs/BETA_QUICKSTART.md` - Version and "What's New" section
- `docs/ALPHA_AGREEMENT_v2.md` - Version in 3 places (header, line 15, line 153)

### Alpha Template (1 file — single canonical template)
- `docs/operations/alpha-onboarding/email-template.md` - Version in multiple places
  - Note: The duplicate at `docs/alpha/templates/` was deleted in v0.8.5. Only one template should exist.

## Reference

- Release Runbook: `docs/internal/operations/release-runbook.md`
- Session where this was documented: `dev/2026/01/15/2026-01-15-0719-lead-code-opus-log.md`
