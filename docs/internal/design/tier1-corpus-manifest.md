# Tier 1 corpus manifest

**Owner:** Docs. **Issue:** #2355 (part of the self-knowledge epic #2349). **Created:** 2026-11-13. **File:** `tier1-corpus-manifest.csv`. **Checker:** `scripts/validate_tier1_manifest.py`.

One row per item Piper may use to answer about itself on every install. A row is a source plus its owner and when it was last checked. The manifest holds no answer text.

## Columns

`id`, `part` (a to d of #2355, or `candidate`), `topic`, `item` (the one file Piper reads, in the user register and voice-passed, the only path a build may index, as `path`, `path#heading` or `path::symbol`), `derived_from` (what the item's facts are checked against: ADRs, docs, code. Never indexed. Several joined by "; "), `source_kind` (`doc` or `generated`), `tier` (always 1 here), `status` (`candidate`, `unverified`, `verified`), `last_verified` (an ISO date, set only when the item's facts were checked against `derived_from` or the served build, with the method in `notes`), `reverify_window_days`, `owner`, `voice_pass` (CXO: `pending`, `passed`, `returned`), `approved` (the commit sha of the item when xian approved it, set only from his quoted yes, with the quote's location in `notes`), `notes`.

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
- Nothing here is approved wording until its row's `approved` column is set. CXO passes each row's text (`voice_pass`), and xian's approval is recorded in `approved` (a commit sha, below).

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

## A dropped row never reads as "nothing to say" (PPM, 11-13)

When a row drops out of the index, Piper must not answer on that topic as if there were nothing to say. For `d-known-limits` above all, "any known problems?" with the row dropped gets "I can't confirm my current list of known limits right now", never an empty-sounding answer. The same holds for any part (b) topic whose item has dropped. The mechanism is Arch's and Lead's (the build can write the set of dropped ids where the conduct layer reads them), the wording is CXO's, and the first served test case is in #2356's question set. This is in place before the first row goes `verified`.

## The fifth condition: `approved` (Arch and CIO, 11-13)

A row is indexed only when it is `verified`, `voice_pass` is `passed`, the item resolves, it is inside its window, **and `approved` holds the sha of the item at xian's quoted approval.** Every non-blank line of the current item must also appear in the item at that sha. Deleting a line keeps the approval, so a fixed limit leaves `known-limits.md` without a new approval. Adding or changing a line needs a new one. A mismatch is a `DROP` with the reason "text changed since approval", never a refused deploy. One approval can cover many rows, and each row records the sha its item had then. The check needs git history, so it runs where history exists (the lint job and Docs' runs), and the deploy build trusts the column only when that check is green on the commit it builds (Lead decides how). For a generated row the approval sits on the template, not the output: the part (a) generator's templates and the stand-in template, each once.

## The stand-in for a dropped row (CXO, 11-13)

When a row drops, its topic gets one stand-in: "I can't confirm {topic} right now, so I won't guess, and I won't tell you there's nothing to know. If it matters, tell me what you're trying to do and I'll say what I can check." `{topic}` is a user's phrase, one line per row id in `docs/tier1/stand-ins.md`. That file is itself a manifest row (`s-stand-ins`), so the phrases get CXO's pass, xian's approval and the line check like any item, and `--strict` fails a row with no line there (Arch, 11-13). The offer is "I'll say", never "I'll fix". Arch's mechanism (each dropped row becomes a generated stand-in in the index) and Lead's build are theirs.
