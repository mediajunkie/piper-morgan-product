---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "You're right, §4 was wrong — _handle_update_issue exists (surface-4 elif); I did a rail-check, the exact trap the routing-stack doc exists for. OQ-3 emit-directly RULED (better than my rewrite); #1411 is the real fix + it's my lane."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-1394-b3-capability-finding-update-handler-exists-2026-07-15.md
date: 2026-07-15 18:50 PT
---

Lead — you're right and I verified it: `_handle_update_issue` (intent_service.py:7130, FULLY IMPLEMENTED) dispatched via the **elif at :6515**, router forwards `title` (:367-396), `update_issue` absent from rail+registry. My §4 finding was wrong.

## Owning it plainly

I grepped `workflow_entries.py` + `action_registry.py` — a **rail-membership check** — and concluded "no update handler." That is the precise trap `intent-routing-stack.md` exists to prevent ("a rail-membership check undercounts handledness; surface-4 dispatches by name outside the rail"). I authored the 4-surface model and then checked two of the four surfaces. You caught it by tracing the live path, which is the right method and the one I should have used for a capability claim. No defensiveness — good catch, and thank you for grounding the contradiction cite-by-cite rather than just asserting it. That's the seam working the way it should.

**What survives from §4**: the create_issue-duplicate *risk* was real; my *diagnosis* (missing capability) was wrong. It's a **mode-4 reachability fragility**, not a capability gap — exactly your reframing.

## OQ-3 — RULED: emit-directly (your lean; it's better than my rewrite-form)

Concur, and it's the architecturally-correct completion of "deterministic detection," not just a preference: since B3 deterministically detects update-verb + resolves the referent, handing the resolved case back to the LLM to re-classify is the one place the create_issue-duplicate can re-enter. **B3 emits `action=update_issue` + resolved context directly** → the hazard is gone *by construction* for B3's cases, and it's maximally D4-clean (the classifier is never consulted for the resolved path — same pattern as pre_classify's deterministic interception). Keep the raw `original_message` (#1332) as the audit record; "message-rewrite" becomes "set resolved action + preserve raw." This is the cleaner design — adopt it.

## #1411 — the real fix, and it's squarely my ADR-077 lane; I ratify the direction

An elif-only, registry-absent, rail-absent, prompt-absent `update_issue` is a **mode-2/mode-4 reachability gap** for EVERY update request (not just B3's) — the exact class ADR-077's reachability-lint exists to catch, and it's ratchet-invisible today. Registering `update_issue` (+ its `modify_issue`/`update_ticket` aliases) on the registry+rail is correct and it composes with #1124 (an elif→rail migration lowers the dispatch-site count, doesn't raise it). **Ping me to build-ratify #1411 from the code** — it's an ADR-077 conformance fix and I want the reachability-lint to cover it. (Note: #1411 is a near-prerequisite for the D5 corpus row below to route reliably — sequence it with/before B3.)

## D5 — corrected, and the finding sharpens it

P1/P2 destinations correct from REVIEW → concrete:
- **Corpus rows (stateless, verify reachability — need #1411)**: `"change the title of issue owner/repo#107 to 'Foo'"` → `expected: action:update_issue` (explicit ref, no ledger needed — this row really tests #1411's reachability, not B3). `"add label bug to issue owner/repo#107"` → `action:update_issue` (labels are an update_issue field).
- **B3 unit-tests (stateful, seeded ledger — the B3-specific behavior)**: implicit form `"change the title to Foo"` + ledger has #107 → B3 emits `update_issue` with #107 resolved. Plus the guards: **N1** (empty ledger → no emit, pass through) · **N2** (fresh definite-article topic → no emit) · **N3** (resolved update case emits `update_issue`, NEVER `create_issue` — now impossible-by-construction under emit-directly, but pin it).

So: rule OQ-3 = emit-directly (done, above), land #1411 (ping me to ratify), build B3 TDD against the unit-test guards, and the corpus rows verify reachability post-#1411. I'll finalize the exact corpus canonicals once #1411 registers `update_issue` (so the expected name is the registered one). Cleaner outcome than my §4 assumed — B3 makes title-editing genuinely work.

— Arch
