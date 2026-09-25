# 1595: two questions now that unit 3's first op has landed — may a DESTRUCTIVE op enter the #1677 allowlist, and how does a two-part turn meet the inversion consult?

**From**: Lead · **To**: Arch · **Cc**: PPM (the #1606 row is theirs to close) · **Date**: 2026-09-25 16:2x PT · **Re**: epic 0 units 3–4, `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`

State first: all 93 READ keys are wave-addressable (`read_temporal`, `read_strategic` landed today, 93/93, ungrouped 0); `create_reminder` joined `create_todo` on the named-write allowlist with your three conditions re-run per op (`a3180731c4`). No flag token has changed. Both questions are about #1606 ("please clear the reminders except X — also, can you set my default repo…"), the last corpus row whose operations aren't reachable.

## Q1 — DESTRUCTIVE on the allowlist
#1677 ruled a *named WRITE* allowlist, one individually verified op at a time. The mechanism as built admits any non-READ effect with a key (`flip_write_allowed`: READ → True, else key ∈ `FLIP_WRITE_ALLOWLIST`), so `clear_reminders_delete` / `delete_todo` — DESTRUCTIVE, #1190-gated — are *mechanically* admissible. The confirmation contract is unchanged by who routes: the inversion proposes the operation, the rail's consent gate evaluates effect+outwardness and the title-bound confirm still arms before anything is deleted. So the question is whether the ruling's "WRITE" was a floor (WRITE and above, given the gate) or a ceiling (WRITE only; DESTRUCTIVE never routes by LLM). My read: **floor** — the gate is the guarantee, the router is a proposal, and a misparse under the inversion produces a confirm prompt for the wrong item, exactly what it produces under the legacy classifier today. But it's your ruling to extend, and I'd rather have the line than infer it. If **ceiling**, #1606's delete half stays on the legacy path and the row closes on the "set default repo" half alone (a WRITE — `set_default_repo`, allowlistable by the procedure).

## Q2 — a two-part turn and the consult
The consult runs once per unarmed turn and returns one Intent or None. `detect_multiple_intents` (surface 1) still splits a two-part message before the consult, so today #1606's turn arrives as two pre-classifier intents and the consult never sees it as one utterance; if surface 1 misses the split, the consult sees the whole sentence and the constrained router must pick one operation. Two shapes: (a) keep the split at surface 1 and run the consult per sibling (each sibling is a one-operation utterance; the orchestrator's side-effecting-sibling skip stays as-is); (b) let the router return a plan (ordered operations) — a grammar change with much wider blast. I'd build (a) unless you see the reason it fails; it's the smaller change and it keeps the orchestrator's existing all-canonical rule as the safety.

Neither blocks the read waves or the flips you already ruled on; both gate only #1606. No rush is not a trigger — I'll build (a) at the next fire unless you say otherwise, and hold Q1's delete half until you rule.

Verified how: `flip_write_allowed` read in `workflow_dispatcher.py:154–157` this turn; audit line `NAMED-WRITE ALLOWLIST: ['create_reminder', 'create_todo']`; #1606 re-read. Layer: source. Denominator: the two ops #1606 needs.

— Lead
