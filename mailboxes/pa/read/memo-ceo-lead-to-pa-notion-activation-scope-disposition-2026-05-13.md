---
from: CEO (xian) + Lead Developer — co-signed
to: PA (Piper Alpha)
date: 2026-05-13
subject: NOTION activation (#304) scope disposition — search-only ships; write + Slack-xref deferred as demand-gated follow-ups
priority: normal — roadmap + backlog tracking ask
response-requested: roadmap update + backlog acknowledgment
---

PA —

Quick disposition memo so the Notion arc is tracked cleanly in both roadmap and backlog.

## The decision

CEO has ratified the following scope for **#304 NOTION activation**:

- **Ship**: search-only (`search_documents` action against live Notion workspace)
- **Defer (demand-gated, not deprioritized)**: write capability + Slack-Notion cross-reference verification

Rationale (Lead Dev's framing, CEO concurs):

- **Search is the load-bearing capability** — it augments every floor query that touches knowledge, compounds with calendar + GitHub + todos. Foundational for "Piper knows what's in your docs."
- **Write is plausible-later, not foundational** — most PMs still author in Notion's native editor. Chat-driven doc updates are a narrower use case with higher trust requirements (wrong content in wrong doc is a real failure mode). No current alpha-user signal that this is wanted.
- **Slack-Notion cross-reference** — single specific use case with zero current signal. Wait for actual demand.
- **Recovery cost is zero** — the write + Slack-xref code stays in tree, flag-gated, ready. Activating later costs the same as activating now. No architectural debt accrues while deferred.

The discipline that's served well across M2f: ship the minimum that gives users something to react to, then let demand drive what's next.

## Backlog issues filed (the tracking part)

Per CEO directive 2026-05-13, the deferred work is filed as separate issues so the backlog reflects it:

- **#1080 NOTION-WRITE**: Activate `update_document` capability (demand-gated). Trigger conditions: alpha user asks for write capability, OR recurring PM workflow surfaces where it would compress 2+ steps, OR 1.0 feedback signals chat-driven doc updates as wanted.
- **#1081 NOTION-SLACK-XREF**: Verify Slack→Notion cross-references render correctly post-#304. Trigger conditions: alpha user reports Slack-with-Notion-link missed context, OR Slack-Notion becomes a load-bearing workflow.

Both `priority: low` until trigger fires. Both reference #304 + the Phase 0 audit (`dev/2026/05/13/304-issue-audit.md`) for the full reasoning chain.

## Roadmap tracking ask

PA — please reflect this in the roadmap so the Notion arc is visible without being overweighted:

- **MVP / current sprint**: #304 search-only ship (5-8 hr, PM-blocked on token provisioning + read smoke)
- **MVP backlog / demand-gated**: #1080 write capability, #1081 Slack-xref
- **Status framing**: "Notion activation in alpha — search shipping; write deferred until user demand validates"

If the roadmap currently shows "Notion activation" as a monolithic item, please split it along these lines so future planning sessions see the right scope.

## What this is NOT

- Not a deprioritization of write capability or Slack-xref. The trigger conditions are written so future demand routes back to action.
- Not a one-way door. If alpha users start asking, the issues activate cleanly; no rework needed.
- Not an opinion that Notion writes are unwanted at 1.0 — only that we don't have signal yet and shouldn't pre-build before validation.

## What's next on #304

Lead Dev waiting on Q1-Q7 disposition (Phase 0 audit `dev/2026/05/13/304-issue-audit.md`) — most-consequential remaining decisions are Q1 (token via keychain vs env), Q3 (smoke split between PM + Lead Dev), and Q6 (this scope decision, now resolved). Once PM rules on the rest, activation can start.

Thanks for keeping the roadmap + backlog coherent.

— CEO (xian) + Lead Developer, co-signed, 2026-05-13
