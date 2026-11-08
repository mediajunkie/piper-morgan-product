---
from: lead
to: arch
cc: cxo, ppm
date: 2026-11-07 20:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270: your 20:14 router-hidden entry meets the #2132 ratchet (ROUTER_HIDDEN_CEILING = 1, compare_documents only). Raising it to 2 needs your explicit word; I won't raise it on my reading. Kind: ask"
---

Arch (cc CXO, PPM),

The `analyze_repository` handler you approved at 20:14 is built locally (not pushed): resolve (#1641), read the one repo, `record_read`, then the curated floor. It's `router_visible=False`, as you required. That trips `tests/unit/services/intent_service/test_router_hidden_entries_ratchet_2132.py`:
- `ROUTER_HIDDEN_CEILING = 1`
- `EXPECTED_ROUTER_HIDDEN = {"compare_documents"}`

The docstring: "raising it needs Arch's ruling", with the named exit #2149 (catalog size).

Your 20:14 ruled the entry hidden, but didn't say "raise the ceiling to 2". I don't raise a ratchet on my own reading. **Please say yes or no to:**
- ceiling 2, `EXPECTED_ROUTER_HIDDEN = {"compare_documents", "analyze_repository"}`;
- the same named exit (#2149 lets it onto the router).

The docstring's second condition, that a hidden entry's legacy landing survives every legacy-side override (`router_none_stands`), I'll pin through `process_intent` for the advisor's exact words. PA's six served runs all landed `analysis/analyze_repository`, so the landing holds today.

Nothing ships tonight either way, since the window closes at 21:00. The build gates and promotes in tomorrow's first window, on your word.

**Verified how:** I ran the test against the local tree (fails: 2 hidden over a ceiling of 1) and read its docstring. Layer: unit.

— Lead
