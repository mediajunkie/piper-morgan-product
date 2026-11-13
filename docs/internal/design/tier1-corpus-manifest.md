# Tier 1 corpus manifest

**Owner:** Docs. **Issue:** #2355 (part of the self-knowledge epic #2349). **Created:** 2026-11-13. **File:** `tier1-corpus-manifest.csv`. **Checker:** `scripts/validate_tier1_manifest.py`.

One row per item Piper may use to answer about itself on every install. A row is a source plus its owner and when it was last checked. The manifest holds no answer text.

## Columns

`id`, `part` (a to d of #2355, or `candidate`), `topic`, `item` (the one file Piper reads, in the user register and voice-passed, the only path a build may index, as `path`, `path#heading` or `path::symbol`), `derived_from` (what the item's facts are checked against: ADRs, docs, code. Never indexed. Several joined by "; "), `source_kind` (`doc` or `generated`), `tier` (always 1 here), `status` (`candidate`, `unverified`, `verified`), `last_verified` (an ISO date, set only when the item's facts were checked against `derived_from` or the served build, with the method in `notes`), `reverify_window_days`, `owner`, `voice_pass` (CXO: `pending`, `passed`, `returned`), `notes`.

## Rules the checker enforces

- Every `item` and `derived_from` path exists in the checkout, and a `path#heading` must resolve to a heading or bold line in the file (Arch, 11-13).
- An `item` may not be an ADR, a `.py` file or a design record marked not ratified. A row past `candidate` needs an item, and a `verified` row needs a date.
- No `item` lies under `dev/`, `mailboxes/`, `docs/omnibus-logs/` or agent memory (these are never indexed, #2356).
- A `verified` row has a date. A row past its window is reported. With `--strict`, unverified and past-window rows fail, which is the behaviour Lead's deploy check can adopt.
- Ids are unique and the enums hold.

## Rules from the rulings

- Part (d) is one row for `docs/ALPHA_KNOWN_ISSUES.md`. A fixed limit is deleted from that file, never marked fixed (Arch, 11-13).
- The only list of what Piper offers comes from part (a), generated, never from a hand-written row (Arch, 11-13).
- Windows (14 days for generated and known-limits rows, 30 for how-it-works rows, 90 for methodology rows) are Docs' first proposals and Lead's check may change them.
- Nothing here is approved wording. CXO passes each row's text and xian approves before anything ships.

Run: `python3 scripts/validate_tier1_manifest.py` (add `--strict` to see what a deploy check would block).

## Which rows are indexed (Lead, 11-13)

**Only `verified` rows are indexed.** A `candidate` or `unverified` row indexes nothing, whatever its `item` says. A row set back to `unverified` drops out of what Piper reads. That is the honest way out when a row can't be re-checked in time, and it never holds a deploy.

## Gates

- `python3 scripts/validate_tier1_manifest.py` lists errors and notes. Errors fail.
- `--strict` also fails on every note (unverified and past-window rows). That is Docs' own stricter read.
- `--deploy` is the narrow gate for a deploy check (Arch's rule, 11-13). A row is indexed only when it is `verified`, `voice_pass` is `passed`, its `item` resolves and it is inside its window. A row that fails any of those drops out of the index at build and is reported as a `DROP` line (id and reason, no text). The deploy is refused, exit 1, only for an indexed `item` on an excluded path (`dev/`, `mailboxes/`, omnibuses, memory, an ADR, a `.py` file or a not-ratified record) or a malformed manifest.
- A generated row (`source_kind=generated`) carries no hand-set date and no window check. Its test belongs to the generator (Lead): the catalog must match the offered connector set.
- The checker's name uses underscores so it imports as `scripts.validate_tier1_manifest` (`heading_resolves`, `offered_names`).
- `last_verified` is `YYYY-MM-DD` in Pacific time, and the check compares against the Pacific date.
