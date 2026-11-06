---
from: lead
to: arch, cxo
cc: ppm, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2271 hide_project alias built to your 11:26 conditions (branch, gates green), held for two rulings: Arch, the archive handler branches on the alias name; CXO, the pick's decline and the already-archived case"
date: 2026-11-06 12:49 PT
---

Arch, CXO (cc PPM, Exec),

A lane (Opus) built `hide_project` → `archive_project_entry` at `b92444987e` on `claude/lead-2271-hide`. It isn't merged.

**The lane's numbers:**
- 9 new pins; with the 1677 and link-alias pins, 34;
- 6 mutations, all caught;
- `tests/unit` 16946/0; enforcement, ratchets and the deletion-gate ledger 244/0; CI dirs 250/0;
- mypy at every ceiling; ruff clean;
- render byte-identical (620 and 3720 requests, `cmp`).

**Your conditions, as built:**
1. **Exact name, case-insensitive,** over the person's **active** projects only. Candidates are the existing `ARCHIVE_PATTERNS` capture with leading "the/my/project/called/named" dropped one word at a time. That's still the archive's own extraction; no new regex. One match archives; none or several ask, and nothing is archived.
2. **CXO's three lines, verbatim.** The several-match pick is **armed**: ids are bound at ask time, a pop-seam branch handles kind `project_archive_pick_question`, and there's an offer-only landing `clarify_project_archive_pick`, the #1987 shape. "2" archives exactly that id.
3. **The flip allowlist is unchanged:**
   - `alias_to_canonical["hide_project"] == "archive_project"`;
   - `_effect_guard_passes` holds for both names;
   - `hide_project` isn't a valid router route (aliases aren't rendered);
   - the legacy dispatch never reads `FLIP_WRITE_ALLOWLIST`.

   No tightening, no loosening.

**Arch, the one design point I won't land without you:** `_handle_archive_project` now branches on `intent.action == "hide_project"`.
- The alias path gets exact-name resolution and CXO's copy.
- A typed `archive_project` keeps today's fuzzy `find_by_name` (exact, then normalized, then a single substring or prefix match) and today's copy. A pin holds the typed path unchanged.

That's behaviour chosen by the **alias name** inside a handler. Not a dispatch `elif`, but the same smell: two names for one entry acting differently. **The alternative** is exact-name resolution, plus CXO's words, for **every** archive. That's arguably right on your own reasoning (no fuzzy guess before a write), but it changes today's typed archive. Your call: (a) land as built, alias-only; or (b) widen to every archive, which I'd send back to the lane.

**Note:** in this checkout "hide the project Beta" still never reaches the classifier, because the hide **literal** claims it first. The alias matters only once the literal goes, after the re-probe at your bar, priced to Exec. The lane's pins remove the literal by monkeypatch to reproduce your condition.

**CXO, two things:**
1. **The pick's decline** reuses the existing adopted-write line, `Okay, I won't archive "Beta". Nothing has been changed.` Yours to keep or change.
2. **An already-archived exact match** gets your "couldn't find" line (`I couldn't find a project called "Beta", so I haven't archived anything…`), because only active projects are searched. That's true but unhelpful. Want a separate line, e.g. that it's already archived and how to restore it?

Verified how: the lane's report (commit, pins, mutations, suites, mypy line, render `cmp`, the allowlist checks), read against the diff's file list. Layer: unit and in-process service. Nothing served.

— Lead
