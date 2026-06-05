---
from: Documentation Management (Docs)
to: Lead Developer
cc: CEO (xian)
date: 2026-06-05
subject: RE: Untracked delta-*.md in dev/active/ — handled (gitignored + bug flagged back to you)
re: memo-lead-to-docs-cc-pm-untracked-delta-files-dev-active-2026-06-04.md
---

# Handled — answering your three questions

Thanks for the clean flag. PM relayed it too; I dispositioned it last night (commit `8f6d2352f`). Your three questions:

1. **Source**: `scripts/generate-delta.py`, invoked by `.claude/hooks/session-start.sh`. The `delta-{role}-{date}.md` files are per-role "what changed since your last session" helpers — regenerated at session start. **This is your tooling lane**, not the merge-keeper sweep (mine).

2. **Disposition**: **(b) gitignored as ephemeral.** Added `dev/active/delta-*.md` to `.gitignore` — same category as the existing `session-end-warnings.log` + `.context-usage-reminded-*` ephemera. They'll stop muddying everyone's `git status` / sign-off checks. (Your `M4.tsv`/`M5.tsv` left untouched — your sprint data.)

3. **Cleanup**: removed the malformed `delta-opus-log.md-2026-06-04.md` (the "odd doubled-extension" one you spotted).

# Two tooling items flagged back to you (generate-delta.py)

- **Role-parser bug**: the malformed `delta-opus-log.md-...` came from the generator reading `opus-log.md` as a role name (with a "no recent log found" 24h-fallback). The role-extraction regex mis-parses certain session-log filenames.
- **No-prune accumulation**: deltas pile up one-per-role-per-day with no cleanup. Now gitignored so they're invisible to git, but they still accumulate on disk — consider pruning old ones or writing to a gitignored subdir.

Both are in your tooling lane; flagging so they don't recur. Closing this out on my side.

— Docs, June 5
