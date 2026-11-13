# Tier 1 corpus manifest

**Owner:** Docs. **Issue:** #2355 (part of the self-knowledge epic #2349). **Created:** 2026-11-13. **File:** `tier1-corpus-manifest.csv`. **Checker:** `scripts/validate-tier1-manifest.py`.

One row per item Piper may use to answer about itself on every install. A row is a source plus its owner and when it was last checked. The manifest holds no answer text.

## Columns

`id`, `part` (a to d of #2355, or `candidate`), `topic`, `source` (a path, `path#heading` or `path::symbol`, several joined by "; "), `source_kind` (`doc` or `generated`), `tier` (always 1 here), `status` (`candidate`, `unverified`, `verified`), `last_verified` (an ISO date, set only for a row someone actually checked against the code or the served build), `reverify_window_days`, `owner`, `voice_pass` (CXO: `pending`, `passed`, `returned`), `notes`.

## Rules the checker enforces

- Every source path exists in the checkout.
- No source lies under `dev/`, `mailboxes/`, `docs/omnibus-logs/` or agent memory (these are never indexed, #2356).
- A `verified` row has a date. A row past its window is reported. With `--strict`, unverified and past-window rows fail, which is the behaviour Lead's deploy check can adopt.
- Ids are unique and the enums hold.

## Rules from the rulings

- Part (d) is one row for `docs/ALPHA_KNOWN_ISSUES.md`. A fixed limit is deleted from that file, never marked fixed (Arch, 11-13).
- The only list of what Piper offers comes from part (a), generated, never from a hand-written row (Arch, 11-13).
- Windows (14 days for generated and known-limits rows, 30 for how-it-works rows, 90 for methodology rows) are Docs' first proposals and Lead's check may change them.
- Nothing here is approved wording. CXO passes each row's text and xian approves before anything ships.

Run: `python3 scripts/validate-tier1-manifest.py` (add `--strict` to see what a deploy check would block).
