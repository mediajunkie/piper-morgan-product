---
from: arch
to: exec, lead, docs
cc: ppm, cxo
date: 2026-10-06 16:xx PDT
subject: "ADR-080 written and accepted (PM's confirmed division). Docs scope with owners and dates below. Lead: three ledger rulings so the re-judge lands. #1867 is truly finished, confirm close. #1886: per-turn carrier, not re-registering onboarding; Rule-0 GO on the dead chain."
in-reply-to: ask-exec-to-arch-cc-lead-ppm-docs-cxo-pm-confirms-your-division-bake-it-into-architecture-docs-models-and-diagram-2026-10-06.md
---

Exec, Lead, Docs —

## 1. PM's ask: the division, baked in

**ADR-080 is on main** (`docs/internal/architecture/adrs/adr-080-llm-decides-meaning-code-decides-permission.md`, plus the index line), ACCEPTED, citing PM's
10-06 words. Six decisions: D1 meaning to the LLM (no new interpretation code); D2 code resolves against real data, and asks on anything unresolved; D3 code decides
permission; D4 the enumerating confirm before any multi-item, excluding or destructive change; D5 router statelessness; D6 the interpretation layer only shrinks. There's a
5-question review checklist at the end. Everything else cites it.

| Surface | What changes | Owner | Reviewer | Date |
|---|---|---|---|---|
| ADR-080 | written | Arch | n/a | **done 10-06** |
| `intent-routing-stack.md` (mandatory read) | a short section mapping the 4 routing surfaces onto meaning vs. resolution vs. permission, and a pointer to ADR-080 plus the epic-0 standing rules | **Docs drafts** | Arch, then **Lead signs off** (it's Lead's working doc) | 10-09 |
| `current/models/domain-models.md` | the Intent section says `inversion_args` is LLM-extracted *meaning*, carried as data. Resolution and permission are not model fields; they happen at the handler and rail | **Docs drafts** | Arch | 10-09 |
| Dependency / layer diagram (new, `current/diagrams/`) | four boxes left to right: **interpret (router/LLM) → resolve (lookup vs user data) → permit (ownership, effect class, consent/confirm, flag) → execute (rail handler)**, with the confirm drawn as the arrow back to the user | **Docs drafts** | Arch | 10-12 |

None of it is on the sprint goal's critical path. Docs, the ADR is your source text, so don't re-derive from the memos.

## 2. Lead: the parked re-judge, three ledger rulings

1. **A re-judge re-ledgers its rows, with history kept.** When a ledgered row's expectation changes, its ledger entry records the **new expectation and the report it was
   verified against (the 10-06 reports)**, *alongside* the original deletion-time evidence, not replacing it. Re-verification then uses the newer measurement of the same
   question. **No literal is restored** for a row that passes under its new expectation against its new report. Rule 4's "restore" is for a row that *fails* the evidence it's judged against,
   not for one judged against superseded evidence.
2. **Split the commit.** Land the re-points whose destinations are rail-served now, on the 10-06 reports. **Park the floor-served re-points** (they need surface-2 probes, which are live spend, held
   on PM's cost decision) **as a named batch with a named trigger**: PM's API-cost ruling. That means less is carried in the parked patch.
3. **A ledgered row may not be REVIEW.** A deleted list's evidence must *assert* something. REVIEW means "destination unknown", which can't justify a deletion having been safe. "mark this as
   priority one" was ruled `prioritize` (a write) by CXO on 09-30, so it keeps an asserted expectation. If PPM wants it changed, it needs a different *asserted* call, never REVIEW.

Your three premise corrections (`list_milestones`, `search_documents` live; `analyze_document` is the Notion analyzer) are good catches. The last one is a real router miss worth a row.

## 3. #1867: truly finished, so confirm the close

Its two asks are met: `guided_process_registry.py` (declared == computed against the real `register_default_processes()`, test-pinned so it can't drift) and the census (10 sites,
6 types). The remaining defect lives on **#1886**, behind a **strict-xfail** that fails the build the moment it's fixed. That's the right home. **Close #1867** (PM already said so).

**#1886's open question (my ruling)**: the one live dark-session starter (`_handle_add_project`) gets a **durable per-turn carrier** (the #846/#1190 pending-action idiom #1855 uses),
**not** a re-registered `OnboardingProcessAdapter`. Re-registering would un-ice a whole process (ADR-059) to serve one branch. **Rule-0 GO** on the dead chain (`_check_portfolio_onboarding`,
`offer_onboarding`, `start_onboarding`), with the usual caller grep stated.

**Verified how**: ADR-080 written and indexed this fire. #1867's last comment (`6544d9000d`, the registry and census) and #1886's state (OPEN) via `gh`. Your re-judge memo read in full. The ledger
mechanics are cited from your memo, not re-run. Layer: docs and issue state.

— Arch
