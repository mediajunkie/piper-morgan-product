#!/usr/bin/env python3
"""Validate editorial-calendar.csv structure AND per-column semantics.

Catches three distinct classes:

  1. STRUCTURE  — CSV escape errors (unquoted commas in altText/caption/notes),
                  field-count drift (rows with != 18 fields), header mismatch.
  2. SHAPE      — a value sitting in the WRONG COLUMN while the field count stays
                  valid. This is the class a field-count check STRUCTURALLY CANNOT
                  SEE, and it has bitten twice: 2026-07-14 (Comms used row[-2] for
                  `notes`, which is index 15 — it landed on `altText`, index 16) and
                  2026-07-28 (Weekly Ship #050: `notes` held a duplicate draftPath,
                  `altText` held 1,000+ chars of editorial prose, `caption` held the
                  real alt text — field count stayed 18 throughout, so every
                  count-based verification passed).
  3. REFERENCE  — `draftPath` values that no longer resolve on disk. Drift rather
                  than corruption: 7 found and repaired 2026-07-29 (3 Weekly Ships
                  plus 4 narrative posts), every one caused by Step-9 archival moving
                  a draft into published/ without updating the row. A 2026-07-12 pass
                  fixed 22 instances without fixing the cause.

Severity is deliberate, and the split IS the design:

  ERRORS (exit 1)   — structure + shape. The file is corrupt, or a value is in the
                      wrong column. Always actionable.
  WARNINGS (exit 0) — reference staleness + soft heuristics. Reported loudly, never
                      blocking, because a heuristic that hard-fails causes FALSE
                      CORRECTIONS. Concrete precedent: on 2026-07-28 a naive
                      >320-char altText heuristic flagged 3 rows that turned out to be
                      genuinely long alt text matching the website verbatim. Docs
                      re-checked and cleared all three rather than "fixing" them.
                      A confident false correction to a shared file is worse than the
                      drift it claims to fix.

Usage:
    python3 scripts/validate-editorial-calendar.py            # errors fail, warnings print
    python3 scripts/validate-editorial-calendar.py --strict   # warnings also fail
    python3 scripts/validate-editorial-calendar.py --quiet    # print only problems

Exit codes:
    0 — no errors (warnings may have printed)
    1 — validation error(s) found
    2 — calendar file not found

Wired into:
    - Manual invocation by any agent after an /update-calendar pass
    - publish-to-blog Step 6 (mandated verification after calendar mutation)
    - Candidate: weekly docs audit + pre-commit hook

Rationale for the original structure check: 2026-05-17 incident — a hand-edit
introduced an unescaped comma in altText (field count drifted to 19). grep + awk
cannot catch escape errors on quoted fields; the Python csv module does.
"""

import csv
import os
import re
import sys
from pathlib import Path

CALENDAR = Path("docs/internal/planning/comms/editorial-calendar.csv")
EXPECTED_HEADER = [
    "title", "theme", "status", "workDate", "endWorkDate", "pubDate",
    "mediumURL", "liPubDate", "linkedinURL", "canonicalSite", "blogURL",
    "blogPath", "cartoon", "chatDate", "draftPath", "notes", "altText", "caption",
]
EXPECTED_FIELDS = len(EXPECTED_HEADER)

# --- enums. Empty is ALWAYS allowed: a queued row legitimately has blanks. ---
THEMES = {"building", "insight", "ship"}
STATUSES = {"drafted", "queued", "ready-for-docs", "published", "distributed"}
CANONICAL_SITES = {"distributed"}

# Recognized LEGACY vocabulary. These are drift (a superseded convention), NOT
# corruption (a value in the wrong column) — so they warn rather than error.
#
# This distinction was learned the hard way by this very script: its first run
# flagged 8 historical Weekly Ships (#019-#026) carrying theme='shipping news' as
# ERRORS. That is the pre-`ship` convention, correct when written. Hard-failing on
# it would have pressured the next agent into rewriting 8 historical rows to satisfy
# a checker — a false correction to a shared file, which is worse than the drift.
# An enum violation that is recognizable legacy vocabulary is drift; an
# unrecognizable value is corruption. Only the second should block.
LEGACY_THEMES = {"shipping news"}

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")     # workDate/endWorkDate/pubDate/liPubDate
US_DATE = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")   # chatDate uses M/D/YYYY — a real schema wart
ISO_DATE_COLS = ("workDate", "endWorkDate", "pubDate", "liPubDate")
URL_COLS = ("mediumURL", "linkedinURL", "blogURL")

# Soft threshold — WARNING ONLY. See the docstring on false corrections.
ALT_TEXT_WARN_CHARS = 400


def check_row(line_no: int, row: list[str], idx: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one aligned data row."""
    errors: list[str] = []
    warnings: list[str] = []

    def val(col: str) -> str:
        return (row[idx[col]] or "").strip()

    title = val("title")
    tag = f"Line {line_no} ({title[:44] or '<no title>'})"

    # --- SHAPE: enums (legacy vocabulary warns, unknown values error) ---
    if val("theme") and val("theme") not in THEMES:
        if val("theme") in LEGACY_THEMES:
            warnings.append(
                f"{tag}: theme={val('theme')!r} is legacy vocabulary (current: {sorted(THEMES)}) "
                f"— drift, not corruption; do not bulk-rewrite historical rows to satisfy this"
            )
        else:
            errors.append(f"{tag}: theme={val('theme')!r} not in {sorted(THEMES)}")
    if val("status") and val("status") not in STATUSES:
        errors.append(f"{tag}: status={val('status')!r} not in {sorted(STATUSES)}")
    if val("canonicalSite") and val("canonicalSite") not in CANONICAL_SITES:
        errors.append(
            f"{tag}: canonicalSite={val('canonicalSite')!r} not in {sorted(CANONICAL_SITES)}"
        )

    # --- SHAPE: dates ---
    for col in ISO_DATE_COLS:
        if val(col) and not ISO_DATE.match(val(col)):
            errors.append(f"{tag}: {col}={val(col)!r} is not YYYY-MM-DD")
    if val("chatDate") and not (US_DATE.match(val("chatDate")) or ISO_DATE.match(val("chatDate"))):
        errors.append(f"{tag}: chatDate={val('chatDate')!r} is not M/D/YYYY or YYYY-MM-DD")

    # --- SHAPE: URLs and paths ---
    for col in URL_COLS:
        if val(col) and not val(col).startswith("http"):
            errors.append(f"{tag}: {col}={val(col)[:56]!r} does not start with http")
    if val("blogPath") and not val("blogPath").startswith("/"):
        errors.append(f"{tag}: blogPath={val('blogPath')[:56]!r} does not start with '/'")
    if val("draftPath") and not val("draftPath").endswith(".md"):
        errors.append(f"{tag}: draftPath={val('draftPath')[:56]!r} does not end in .md")

    # --- SHAPE: the Ship #050 signature — a REPO PATH where prose belongs.
    # Must exclude URLs: this check's first run false-positived on a `notes` field
    # containing a claude.ai URL that happened to end in `.md`. A URL in free text is
    # legitimate; a repo-relative path is the shift fingerprint. Anchor on the repo's
    # actual draft/doc prefixes rather than on "looks pathlike". ---
    PATH_PREFIXES = ("docs/", "dev/", "scripts/", "mailboxes/", "knowledge/", "./", "/Users/")
    for col in ("notes", "altText", "caption"):
        v = val(col)
        if v.startswith("http"):
            continue
        if v.endswith(".md") and v.startswith(PATH_PREFIXES):
            errors.append(
                f"{tag}: {col} contains a REPO PATH ({v[:52]!r}) — "
                f"this is the 2026-07-28 column-shift signature"
            )

    # --- REFERENCE: draftPath resolves. WARNING: a row may legitimately precede
    # its draft file (draft-blog-post mandates the row at draft creation, but the
    # window exists), so this must not block. ---
    if val("draftPath") and not os.path.exists(val("draftPath")):
        warnings.append(f"{tag}: draftPath does not resolve — {val('draftPath')}")

    # --- REFERENCE: draftPath is archived once a post has gone live. Comms' 2026-08-03
    # finding — the check above only asks "does this path resolve," which a stale
    # pre-archival draft in drafts/ answers YES to, correctly, since the file is right
    # there. It just hasn't been moved to drafts/published/ yet even though the post
    # already published. 19 rows were caught this way (16 distributed + 3 published,
    # Jun 1 - Jul 28), each one a Step-9-archival miss that made a resolved question
    # look like it was still open in PM's queue. WARNING, not error: this is a Step-9
    # housekeeping signal, not a data-integrity one — nothing is broken while it's true. ---
    if val("status") in ("published", "distributed") and val("draftPath") and "/published/" not in val("draftPath") and "/superseded/" not in val("draftPath"):
        warnings.append(
            f"{tag}: status={val('status')!r} but draftPath doesn't point into drafts/published/ "
            f"— {val('draftPath')} (Step 9 archival likely missed)"
        )

    # --- SOFT: caption/cartoon naming DIFFERENT images.
    # Rewritten 2026-08-01 on Comms' finding. My first version flagged
    # "caption holds a media filename" as anomalous on its own — which found the
    # right rows and NAMED THE WRONG COLUMN.
    #
    # Comms owns `caption`, took the "cause NOT established" as an invitation, and
    # established it against 7 live published pages:
    #   - 9 of 16 are COSMETIC: caption is just cartoon + ".webp". Nothing to decide.
    #   - 7 of 16 are REAL: caption and cartoon name DIFFERENT images — and the page
    #     renders the one named in CAPTION, 7 of 7. `cartoon` is the stale column.
    #
    # ⚠️ The old wording invited someone to CLEAR the caption to "clean up" — which on
    # those 7 rows would delete the only surviving record of the real image and leave
    # the wrong one standing. A warning that points at the accurate column is worse
    # than no warning: it manufactures a confident, quiet, near-irreversible loss.
    #
    # So the informative test is the DISAGREEMENT, not the format.
    MEDIA = re.compile(r"^[\w.-]+\.(webp|png|jpe?g|gif|svg)$", re.I)
    cap = val("caption")
    cartoon = val("cartoon")
    if cap and MEDIA.match(cap):
        stem = cap.rsplit(".", 1)[0]
        if not cartoon:
            # Reconciled 2026-08-01: Comms counted 7 "real" rows, my first cut found 5.
            # Both were right — theirs included 2 rows where `cartoon` is EMPTY, which my
            # version skipped by requiring it non-empty. Those 2 are the MOST dangerous:
            # caption is the SOLE surviving record of the image, so a "cleanup" there is
            # unrecoverable from the calendar alone. Skipping them was the worse gap.
            warnings.append(
                f"{tag}: caption ({cap!r}) names an image and cartoon is EMPTY — "
                f"caption is the ONLY record of this post's image. DO NOT clear it."
            )
        elif stem != cartoon:
            warnings.append(
                f"{tag}: caption ({cap!r}) and cartoon ({cartoon!r}) name DIFFERENT images. "
                f"The live page is the tiebreaker — Comms verified 2026-08-01 that the page "
                f"renders CAPTION, 7/7. DO NOT clear caption; cartoon is the stale column."
            )
        # stem == cartoon -> cosmetic duplication (9 rows). Nothing to decide; silent.

    # --- SOFT: altText length. WARNING ONLY — long alt text is legitimate. ---
    if len(val("altText")) > ALT_TEXT_WARN_CHARS:
        warnings.append(
            f"{tag}: altText is {len(val('altText'))} chars (>{ALT_TEXT_WARN_CHARS}) — "
            f"verify it is genuinely long alt text, NOT shifted prose"
        )

    # --- SOFT: blogURL/blogPath must agree with EACH OTHER.
    # Deliberately NOT "a published row must have a blogURL" — that fired 31 times on
    # historical rows that predate the field, and 31 unactionable warnings is how a
    # checker teaches people to ignore it (the check-acronyms failure mode: replacing
    # a silent hole with a noisy false positive). Pair-consistency is the real signal:
    # a row carrying one half of the pair and not the other is internally wrong
    # regardless of era. ---
    if val("blogPath") and not val("blogURL"):
        warnings.append(f"{tag}: has blogPath but blogURL is empty (inconsistent pair)")
    if val("blogURL") and not val("blogPath"):
        warnings.append(f"{tag}: has blogURL but blogPath is empty (inconsistent pair)")

    return errors, warnings


def main() -> int:
    strict = "--strict" in sys.argv
    quiet = "--quiet" in sys.argv

    if not CALENDAR.exists():
        print(f"ERROR: {CALENDAR} not found (run from repo root)", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    row_count = 0
    idx = {name: i for i, name in enumerate(EXPECTED_HEADER)}

    with CALENDAR.open(newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.reader(f), 1):
            row_count += 1

            if line_no == 1:
                if row != EXPECTED_HEADER:
                    errors.append(
                        f"Line 1 (header) mismatch:\n"
                        f"  got:      {row}\n"
                        f"  expected: {EXPECTED_HEADER}"
                    )
                continue

            if len(row) != EXPECTED_FIELDS:
                preview = row[0][:60] if row else "<empty row>"
                errors.append(
                    f"Line {line_no}: {len(row)} fields (expected {EXPECTED_FIELDS}) "
                    f"— title={preview!r}"
                )
                continue  # shape checks are meaningless on a misaligned row

            row_errors, row_warnings = check_row(line_no, row, idx)
            errors.extend(row_errors)
            warnings.extend(row_warnings)

    data_rows = row_count - 1

    if warnings and not quiet:
        print(
            f"⚠ editorial-calendar.csv: {len(warnings)} warning(s) — reported, not blocking:",
            file=sys.stderr,
        )
        for w in warnings:
            print(f"   {w}", file=sys.stderr)
        print(
            "   (non-blocking BY DESIGN — a heuristic that hard-fails causes false "
            "corrections; see module docstring)",
            file=sys.stderr,
        )

    if errors:
        print(f"❌ editorial-calendar.csv: {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"   {e}", file=sys.stderr)
        return 1

    if strict and warnings:
        print(f"❌ --strict: {len(warnings)} warning(s) treated as errors", file=sys.stderr)
        return 1

    if not quiet:
        suffix = f", {len(warnings)} warning(s)" if warnings else ""
        print(
            f"✓ editorial-calendar.csv: {data_rows} data rows + 1 header, "
            f"all {EXPECTED_FIELDS} fields, shape + reference checks clean{suffix}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
