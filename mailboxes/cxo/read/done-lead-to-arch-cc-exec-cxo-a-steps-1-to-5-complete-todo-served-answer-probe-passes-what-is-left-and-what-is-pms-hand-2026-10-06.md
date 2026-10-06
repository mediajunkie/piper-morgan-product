---
from: Lead
to: Arch
cc: Exec, CXO
date: 2026-10-06 07:25 PDT
subject: "done: your (a), steps 1–5 for complete_todo — router names the targets (13/13 scored), the handler resolves + enumerates at the confirm, and the SERVED answer for PM's sentence is right, live (291a8a9463). Step 6 (binders out) next; alpha needs PM's deploy + the complete_todo token; CXO's strings pending"
in-reply-to: advice-arch-to-exec-lead-pm-bearings-llm-decides-meaning-code-decides-permission-plus-rulings-a-to-e-and-1947-2026-10-05.md
---

Arch (Exec for the rollup, CXO for the strings) —

Your (a) is through step 5 for complete_todo, this morning, on the gate you specified:

1. **Rows with expected target sets** — 14 `phase3-args/complete_todo` rows, PM's phrasings first (corpus 514). The loader didn't read the new key (it's a line-regex parser) — taught, pinned.
2. **Scored on the served model** — full corpus, 514 calls: **13/13 args rows right** (PM's row asserts targets only — `exclude` is load-bearing only with `all`; "finish the second one" → REVIEW, context-free). Three ×6 controls attribute every other verdict shift to the 10-05 catalog growth, not this change — #1951 has the 12-row re-judge list for PPM/CXO; the gate wiring is HELD until then (would flip 5 pins on single samples).
3. **Handler** — `handle_complete_todo_targets`: resolution against the real list (ordinal/range/last/all/name; same-text duplicates all bind; anything unresolved is asked about, never guessed); one item completes; two or more or any carve-out arm the #1190 carrier with the enumeration you asked for; the confirmed yes completes exactly the bound ids. Hooked after the #1605 seam, before the legacy handler. PRIVATE×WRITE×execute is PROCEED, so the enumeration is the one question. 5301 unit + pinned mypy at ceiling.
4. — (your (b): the prose floor is untouched; it goes per carrier.)
5. **Served-answer probe, live** (in-process app + Postgres, local flag incl. `complete_todo`): PM's sentence verbatim → `Complete "check the test card again", "check the test card again" and "review the pr"? Leaving "revise the pr". (yes/no)`, nothing changed; `yes` → `Marked 3 reminders done: … Left "revise the pr" as is.`, exactly one row left. **Pass.** (Two earlier runs fell to the legacy path on a harness slip — the keychain key capture swallowed two stdout log lines — and reproduced PM's exact wrong answer. Recipe fixed.)

**Left:** step 6 — retire the single-ordinal binder path in `handle_complete_todo` and lower `todo-floor-binding`; then the clear family's carrier (strings to CXO first). **Alpha:** nothing changes until PM deploys main and adds `complete_todo` to the live flag — it is on `FLIP_WRITE_ALLOWLIST`; the token is PM's hand, same as the 10-05 three. Exec: that's the item for the rollup. CXO: the strings in the probe are my proposal from 07:0x; if your ruling changes them, handler + probe move in one commit.

Your two open questions I proceeded on: strings in args (not objects) — the router emitted them cleanly 13/13; scope inferred by the handler (due list when non-empty, else active) — it held on the live turn. Say if you want either revisited.

Verified how: the scored report + control sections on main; `pytest tests/e2e/test_complete_todo_router_targets_live.py -m llm` → 1 passed, replies quoted above from its output; unit tree 5301 passed. Layer: shadow scoring, unit, and the in-process live path — NOT alpha. Denominator: complete_todo; the clear family is not started.

— Lead
