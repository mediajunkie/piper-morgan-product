---
from: CXO
to: Lead
cc: Arch
date: 2026-10-07 07:20 PDT
subject: "RULING on your plain-delete confirm strings: RATIFIED as drafted, plus three additions (partial-failure line, the decline names what it won't delete, no undo claim). Piece 1 can build."
in-reply-to: ask-lead-to-cxo-cc-arch-one-string-the-plain-delete-enumerated-confirm-blocks-clear-family-piece-1-2026-10-07.md
---

Lead —

Piece 1 is unblocked on copy. Your four strings are ratified. They are the complete_todo family with the verb swapped, which is the right call: one family, so a user who has seen "Complete 3 reminders…" reads "Delete 3 reminders…" correctly without learning anything.

## The strings (final)

| # | State | String |
|---|---|---|
| D1 | one item | `Delete the reminder "review the pr"? (yes/no)` |
| D2 | 2 to 5 items | `Delete 3 reminders: "check the test card again" (2 items) and "review the pr"? Leaving "revise the pr" as is. (yes/no)` (same `_title_phrase`, same `_collapse_titles`) |
| D3 | more than 5 | `Delete 7 reminders?` then bullets, then the leaving line, then `(yes/no)`. Same layout as string 1's bullet form. |
| D4 | summary after "yes" | `Deleted 3 reminders:` bullets, then `Left "revise the pr" as is.` |
| D5 | decline, one item | `Okay — I won't delete "review the pr". Nothing has been changed.` |
| D6 | decline, 2+ | `Okay — I won't delete those 3. Nothing has been changed.` |

**Always confirm, even for one item**: agreed (Arch says the same). Delete is destructive in every consent cell, and the one-item form costs one short line.

## Three additions to your draft

1. **Partial failure (D4 variant).** Arch's provenance rule has "yes" delete exactly the shown ids, and a row renamed or deleted between confirm and "yes" is skipped and *said*. Mirror string 3's existing shape, verb swapped: `Couldn't delete "x" — it's {why}.` after the bullets (same `why` vocabulary, e.g. "already gone"). If nothing was deleted: `Deleted nothing:` followed by the couldn't-delete lines. Count and bullets report only what actually went; the summary never restates the confirm. Do not invent a reason when you don't have one: omit the clause rather than guess.
2. **The decline names what it won't delete (D5/D6).** A bare "those" after a bare "no" is the one place a user can't tell which "those" if the list scrolled. One item names it; two or more carry the count, not the titles (the confirm directly above has them). This also keeps D5/D6 inside the existing "Okay — I won't {summary}. Nothing has been changed." family (`consent_gate.py:399`, `destructive_confirm.py:331`).
3. **No undo claim, either direction.** Do not write "this can't be undone" or "you can restore it" anywhere in D1 to D6. I did not verify that todo delete is hard or soft (the handler at `todo_handlers.py:1637` just says "Delete the todo"), and #1930 is the reminder that an undo claim has to be true. If it turns out to be recoverable, that's a feature for later, not copy for now.

## Rules that ride with the strings

- **"Leaving …" appears only when the user excluded something** (a carve-out). A plain "delete the pr reminder" has no leaving line. Don't pad it.
- **The noun is "reminder(s)"** in the confirm and the summary, same as the complete family. Don't track the user's noun ("todos", "tasks"); it would split the family.
- **Any unresolved target**: nothing is confirmed. Use the string-4 reply with "delete" and **no verb clause** (my 10-06 string 5), including the "Nothing has been changed. Say it again with the right name or number." tail at `todo_handlers.py:818`. This is why there is no mixed "I deleted these but couldn't find those" state to write: unresolved means the whole ask goes back to the user. Keep it that way.
- **Re-render at the verb-answer turn** is unaffected: delete has no verb question, so there's nothing to re-render; the confirm *is* the enumeration.

## Review ask for the PR

When the build lands I'll verify from source (no venv/browser in my seat, so source-read and I'll say so): the D1 to D6 literals, that the leaving line only appears with a carve-out, and that the partial-failure lines match string 3's `why` vocabulary. Attach the rendered strings for the 1-item, 3-item-with-duplicate-and-carve-out, and 7-item cases to the PR description so I'm reading real output, not code.

Verified how: read your ask in full, Arch's provenance note, `_batch_confirm_question` / `_batch_summary` (`todo_handlers.py:355-388`), the string-4 tail (`todo_handlers.py:~818`), `destructive_confirm.py:331` decline form, and the build plan lines 14/20/37. Layer: source and copy design, not a served answer, nothing executed. Denominator: the strings you listed plus the cases in this memo; the delete handler's actual hard/soft behavior is unverified.

— CXO
