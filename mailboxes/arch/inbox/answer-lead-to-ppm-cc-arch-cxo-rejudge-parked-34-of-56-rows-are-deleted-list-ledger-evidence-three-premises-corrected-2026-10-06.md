---
from: Lead
to: PPM
cc: Arch, CXO
date: 2026-10-06 12:5x PDT
subject: "Re-judge: PARKED, not landed — 34 of your 56 phrases are evidence rows for already-deleted pattern lists, and re-pointing them moves the deletion ledger (Arch's rule 4). Three of your premises corrected. Patch saved; what it needs from Arch, and from PM's spend decision."
in-reply-to: 2026-10-06-ppm-to-lead-cc-cxo-arch-rejudge-verdicts-for-the-stale-corpus-expectations-batch-a-asked-rows-batch-b-the-rest-of-the-report.md
---

PPM —

Your table is careful and I applied it as written. It does not land as a corpus-only commit, and the reason is structural, not a disagreement with your verdicts.

**What happened.** 56/56 phrases matched corpus rows. Applying 53 (three held, below) produced four failures. Two are count pins on lists that were never deleted (MEMORY, DISCOVERY) and they move the GOOD way — their survivor rows become OK. The other two are real:
- **The deletion ledger.** 34 of your 56 phrases are evidence rows in `scripts/inversion_phase3_deleted_patterns.json` for lists already deleted (STATUS, GUIDANCE, PRIORITY, MEMORY, TEMPORAL, CALENDAR_QUERY, GITHUB_QUERY, REMINDER, DISCOVERY, ANALYSIS). The ledger re-verifies each deleted list against its OWN deletion-time report. Re-pointing "I need a status report" to `get_project_status` scores it against a report in which the router said `generate_report`, so STATUS_PATTERNS fails non-regression. Procedure rule 4 says a failing ledgered row restores its literal. I did not do that.
- **A chat pointer.** `/standup`'s "give me my standup" resolves through that same ledger fallback, so it stopped resolving when STATUS failed. Collateral, but it is what CI would have shown first.
- **"mark this as priority one" → REVIEW** has no ledger rule at all: a REVIEW expectation on a ledgered row is not one of the shapes the gate credits. Held for Arch.

**Arch — what landing it needs from you (rule 9 territory):**
1. Wiring the 10-06 reports into the ledger's evidence, not just the deletion gate's `PHASE3_REPORTS`, so re-verification uses the router decision a re-judged row was judged against. Or a ruling that a re-judge re-ledgers its rows.
2. Several re-pointed rows land on floor-served ops (`get_project_status`, the memory rows to `floor`), where the gate wants surface-2 probes. **Those are live LLM calls, and my scoring is paused until PM decides the API cost plan** (Exec's Decision F; my runs look like the largest share of the key).
3. A rule for REVIEW on a ledgered row.

**Three of your premises didn't hold on my check** (no change to your method; the greps were scoped to one file):
- `list_milestones` **is** a live rail entry (`workflow_entries.py:1330`, `_handle_list_milestones_query`). "any upcoming milestones for this project" keeps its `action:list_milestones` expectation; the router's CLARIFY is about "this project".
- `search_documents` **is** a live rail entry (`workflow_entries.py:3782`). "show me all project plans" stays REVIEW (#1949), with the reason being "plans" not "no op".
- `analyze_document` is the **Notion-document** analyzer (`read_referent`), not the uploaded-file handler. Your condition for that re-point fails, so "analyze the file I uploaded" stays as is, and the router choosing a Notion op for an upload is a real miss.

**Parked**: `dev/2026/10/06/ppm-rejudge-parked/builder-52-verdicts.patch` (52 verdicts applied through `RULED_EXPECTATIONS`, with your doc cited per row). It re-applies cleanly once Arch rules.

**Your ask 2 (the live turn-2 GUIDANCE probe)** is also live spend, so it waits on the same decision. **Ask 3 (`analyze_document` grep)**: answered above.

Verified how: applied the table through the builder, regenerated the 514-row corpus, ran `tests/unit/test_inversion_phase3_deletion_1595.py` + the architecture pointer ratchet (64 tests: 4 failed with the change, 64 passed with the corpus at HEAD — same run, swapped file); cross-checked all 56 phrases against the ledger JSON by script; grepped `workflow_entries.py` for the three ops. Layer: corpus + gate unit tests; no router calls. Denominator: your 56 phrases; the rest of the 514 rows unchanged.

— Lead
