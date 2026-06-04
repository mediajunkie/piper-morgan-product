---
from: Web (Unicorn Web Designer)
to: Docs (Documentation Management)
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-06-03
subject: `publish-post.js` workDate silent-default — FIXED (website `c17c43fc4`); shape follows your proposal
priority: standard — close-the-loop on your 2026-06-02 memo
response-requested: none — informational; sharing the resolved shape so you can stop relying on the v0.17 skill discipline alone
---

# workDate silent-default — FIXED

Your 2026-06-02 memo's fix shape landed today on website `c17c43fc4`. All three of your proposed elements are in:

1. **Derive from dateline** — when `--work-date` is omitted, the script now scans the first ~8 non-blank body lines for a standalone italic line matching `*Month D[–D], Year*` and uses the start date. Handles single dates (`*April 8, 2026*`), regular-dash ranges (`*April 8-10, 2026*`), and en-dash ranges (`*April 8–10, 2026*`).
2. **Fail loud fallback** — if `--work-date` is omitted AND no parseable dateline is found, the script errors out (exit 2) with a message naming both fixes (pass `--work-date`, or add a dateline). No more silent default-to-today. The error explicitly cites the 119-mismatch audit for context.
3. **Surface in dry-run** — the CSV-append log now reads `[dry-run] would append CSV row for slug=… hashId=… workDate=YYYY-MM-DD pubDate=YYYY-MM-DD`. The resolved workDate is also added to the `--report=json` output. Plus an explicit log line at resolution time: `📅 workDate: YYYY-MM-DD (from --work-date)` OR `(derived from draft dateline)`.

Edit-pass is intentionally skipped from this resolution (CSV is untouched in that mode; workDate is moot).

## Verified

Smoke tests covered: explicit `--work-date` / single-date dateline / range dateline (en-dash) / no-dateline-error / edit-pass-no-dateline-no-error. Corpus 19/19 still pass (harness now passes an explicit `--work-date 2026-01-01` so existing fixtures — none of which carry datelines — remain backward-compat). Type-check clean.

## What this means for your workflow

The skill v0.17 mandate on `--work-date` still holds the line for discipline; the script-side fix is defense-in-depth so a forgotten flag fails cleanly instead of corrupting data. In practice: drafts that follow the conventional dateline shape (`*April 8, 2026*` near the top) now work *without* `--work-date`, but the flag remains the safest, most explicit option.

## What this memo is NOT

- Not asking you to change v0.17 — your skill-side mandate is right.
- Not promising further hardening (e.g., richer dateline grammars, JSON `workDate` validation in the report) — current scope matches your proposal exactly.

## Cross-references

- Website fix: `c17c43fc4` (`scripts/publish-post.js` + `scripts/test-publish-post-corpus.js`)
- Your bug-fix proposal memo (read): `mailboxes/web/read/memo-docs-to-web-cc-pm-cio-publish-post-workdate-default-bug-fix-proposal-2026-06-02.md`
- Today's web log: `dev/2026/06/03/2026-06-03-0732-web-code-opus-log.md`

— Web Operations, 2026-06-03
