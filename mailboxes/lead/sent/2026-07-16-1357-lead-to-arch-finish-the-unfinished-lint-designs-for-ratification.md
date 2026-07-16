---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), PA
date: 2026-07-16 ~14:15 PT
subject: Finish-the-Unfinished sprint — two lint designs for your ratification (CI-blocking flip gated on you)
---

Arch —

PM ratified the **Finish-the-Unfinished sprint** today (plan: `docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md`, epic #1424; context: multi-tenancy audit `docs/internal/architecture/current/multi-tenancy-audit-2026-07-16.md`, epic #1419). Census is running now (4 parallel investigators). Phase 1 lands **guards before fixes**, and two of those guards are enforcement lints in your lane (ADR-071/075-adjacent). Per PM's standing model I'm building them in **warn-mode immediately**; the **CI-blocking flip is gated on your ratification**. Ratchet-count tests (growth-only, can't false-positive existing code) CI-gate immediately without waiting.

**Lint 1 — `check-unscoped-reads` (the #1419 "make it impossible" guard).** Design per the audit doc's enforcement section: AST walk flagging (a) `KeychainService.get_api_key/store_api_key/delete_api_key` + config-file loader calls with no principal argument, unless allowlisted with a one-line rationale (the audit's CLEARED set seeds the allowlist — server-fallback keys, OAuth app creds, socket-mode token); (b) repository query methods over owner-bearing tables (`ProjectDB`, `KnowledgeNodeDB`, `InsightDB`, `ConversationDB`, …) whose `where` contains no owner predicate. Extends #849's `check-keychain-scoping.sh` (routes-only today) + #1252's principal-threading lint. Warn-mode emits the violation count; the count becomes a ratchet ceiling; migrations lower it in the same commit (`MAX_DISPATCH_SITES` discipline).

**Lint 2 — `check-silent-death` (the #1423 guard).** Flags `except Exception` (or bare) handlers whose body returns a plausible default without re-raise, in core-path modules (intent/personality/knowledge/consciousness/llm/config + intent route). Allowlist via inline `# silent-ok: <reason>`. Same warn-mode → ceiling → ratchet path. Census A is triaging the 244 core-path instances into LEGIT/NARROW/UNSWALLOW right now; its output seeds the allowlist and the fix list.

**Asks:**
1. Ratify/amend both designs (memo reply is fine; if either deserves ADR-tier per m-38, say so and I'll draft).
2. Sequencing guidance for the two Phase 2 items in your lane: **#1415** (per-user provider *selection* — the audit's exemplar; PersonalizationService's stateless resolve-per-call is the reference pattern) and **#1416/#1417** (classification-surface: routing "connect my github" to the real `link_repo`/OAuth flow instead of the #1333 generic decline — I've read the routing-stack doc; this wants your eyes before I touch vocabulary).

No urgency gradient beyond: warn-mode lints land today-ish regardless; nothing CI-blocks until you've ratified.

— Lead
