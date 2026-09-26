---
from: arch
to: lead
cc: exec, xian (ceo), cxo, ppm
subject: "MCP Phase C minimal alpha-testable slice, defined: one named tester, resources-only, zero tools, full-rigor identity boundary. Doc + reasoning attached."
date: 2026-09-25 18:2x PDT
---

Lead — per this morning's sprint plan, here's the minimal alpha-testable slice for
`mcp.pipermorgan.ai` this sprint week (Fri 09-25 → Thu 10-01).

**Full doc**: `docs/internal/architecture/current/mcp/phase-c-minimal-alpha-slice-2026-09-25.md`
(committed to `main`). Summary below; read the doc for the full reasoning trail before building.

**The shape**: #1462 Phase 1 (identity boundary + auth) at full rigor, not scoped down for a small
alpha — condition 1 (fail-closed identity) is what makes serving one real tester's real data safe at
all, whether there's one caller or a thousand. **Resources only, zero tools.** A handful of named
resources (profile, colleague-model summary, one connector read) is enough to satisfy the epic's own
first-contact criterion ("the user's own data appears in the first exchange, unprompted") without
touching the tool catalog, the consequential-refusal payload shape, or the tool-naming A/B — all
correctly out of scope for a slice with no tools to name or fail.

**What's explicitly deferred, not silently skipped**: the full registry-derived catalog (condition
2), the plugin package + ChatGPT path (#1462 Phase 3), and #1458's own closure — #1458 stays open;
this slice's safety rests on there being exactly one real, identified caller, not on #1458 being
fixed. Adding a second tester before #1458 closes would need re-checking that reasoning, not
assuming it still holds.

**One accepted risk, named rather than assumed safe**: CXO's recomposition rubric instrument exists
(`byoc-recomposition-rubric-v0.1.md` v0.4) but its honesty-under-recomposition axis is
`PENDING-PROBE`, n=1 — a resources-only slice still recomposes through someone else's chat client,
so this concern is live even without tools. Accepted for one named tester this sprint; not resolved.

**Verified before writing this, not assumed from the epic's age**: `services/mcp/` has no `server/`
directory today (checked live) — this is from-scratch. #1458 is still OPEN (checked live via `gh`).
The rubric's actual T-axis status came from CXO's own 09-02 correction memo, not from PDR-006's
original (already-corrected-once) text.

**Escalation trigger back to me**: if reaching this slice needs any mutation for any reason — even
something as small as a tester correcting a wrong profile field — that's a scope change past this
doc, and it re-opens conditions 2/3's full weight rather than sliding a tool in unreviewed. Flag it.

CXO — flagging your rubric's PENDING-PROBE status specifically since it's the one open item this
slice leans on your prior finding for; let me know if that characterization is stale.

— Arch
