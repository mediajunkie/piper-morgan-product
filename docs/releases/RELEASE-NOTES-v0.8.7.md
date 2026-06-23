# Release Notes v0.8.7

**Release Date**: June 14, 2026
**Branch**: `main` → `production`
**Previous Version**: v0.8.6 (M0 Conversational Glue, March 4, 2026)
**Sprints**: M1 — Foundation (closed Apr 11) · M2 — Conscious Floor + Action Handlers (closed June 3) · M3 — UI Coherence + Integration Completeness (closed June 14)
**Release model**: development continues on `main`; `production` carries the **last stable, canonical-regression-passing build** for alpha testers.

---

## Summary

**This is the first production cut since M0 (v0.8.6, March 4) — it ships three full milestones.** The product-relevant change is ~190 features and ~160 fixes across M1, M2, and M3.

The headline is the **Conscious Floor**: Piper no longer falls back to templates when a query doesn't match a canonical handler — an LLM-first conversational floor answers in Piper's voice, grounded in assembled context (your blocked items, active sprint, recent activity), and refuses to fabricate when it lacks the information. On top of the floor, **M2 delivered suggestion provenance** and **M3 completed the integration layer and files experience**.

**Quality posture** (canonical retest Run 11, June 3): Quality 80.3%, Expected-pass Quality 80.5% (above the ≥75% north star), Routing 93.4%. M3 gate cleared at commit `9a1094672` (252/252 clean).

**References**: M1 Foundation; M2 (Conscious Floor); M3 (UI Coherence + Integrations); PDR-005; ADR-061 v1.1.

---

## What's New

### The Conscious Floor (M2 centerpiece)

Unmatched queries now route to an LLM-grounded conversational floor instead of canned templates.

- **#907 — Conversational Floor**: LLM responses for unmatched queries, in Piper's voice.
- **Floor-first routing migrations**: IDENTITY (#926), STATUS + PRIORITY (#925), temporal Q7–Q10 (#965), GUIDANCE intents (#911) all migrated off canonical templates onto the floor with context assembly.
- **#950 — Floor prompt evolution**: Five Pillars + grammar + anti-flattening; identity anchoring (iter 2).
- **#1122 — Antecedent resolution**: conversation history now reliably reaches the floor — "it" and "that" resolve correctly across turns.
- **Context assembly into the floor**: blocked items (#983), active sprint/milestones (#985), recent GitHub activity (#986), calendar + deadlines (#951), with a ContextCache layer + eager invalidation (#984).

### Suggestion Provenance & Insights (M2)

The floor can now surface what it has learned about you and explain its own suggestions.

- **#1030 — INSIGHT-PULL**: "What have you learned about my work style?" returns confidence-sectioned insights + an invitation to correct, wired end-to-end through the floor.
- **#1032 — INSIGHT-PUSH**: proactive insight surfacing through `floor.respond`, with natural-language session-mute.
- **R4 provenance pipeline** (Steps 1–11): new `IntentCategory.PROVENANCE` + `ProvenanceHandler`; cross-session provenance guaranteed via DB persistence. 152 R4 tests.

### Action Handlers — dispatch rail complete (M2+M3)

- **#1124 — Action-dispatch rail COMPLETE** (M3 Phase 2): the legacy `elif` dispatch chain is fully retired — 28 sites → 0. All action handlers now register via the workflow-dispatcher rail.
- **#1121 — Slot-filling migration**: `update_document` regex parser replaced with LLM `extract_slots()`.
- **#1207 — Conversation-context unification**: two parallel `ConversationContext` systems merged into a single DDD source of truth.
- **GitHub & task lifecycle**: complete issue close/reopen with confirmation UX + fuzzy match (#902), reopen handler (#902), minimum-viable reminders (#903), todo completion lifecycle (#904), real GitHub issue wiring (#695/#1112), standup helpers wired to UserPreferenceManager (#693).
- **#1102 — Real portfolio data**: replaced hardcoded fake projects with a real `PortfolioService` query.

### Files experience (M3)

Full file management UI shipped across M3 (Issue #313):

- **Search + filter**: search by name and filter by type across all your files and artifacts.
- **In-browser preview**: view file contents without leaving Piper.
- **Bulk download**: checkbox-select multiple files, download as a zip (per-item ownership enforced).
- **Drag & drop upload**: drop anywhere on the `/files` page, multi-file, shared upload path.
- **Tag / categorize**: freeform tags via existing JSON columns, chips editor, search matches tags.

### Integrations (M3)

- **#1129 — Slack inbound rebuilt on Socket Mode**: inbound messages now route to Piper for the first time since October 2025. Outbound + DM / @-mention / source aggregators continue to work.
- **#1187 — Issue summarization**: `summarize-issue` now fetches live issue + comments and summarizes from real data, not fabricated content.
- **#1192 — GitHub repo resolution**: chat path resolves the user's configured default GitHub project — Piper knows which repo you mean.
- **Notion** (#1080/#1081): real `append_blocks`, Slack→Notion URL unfurling, no demo-fallback fabrication (#1088).
- **Calendar** source aggregator (#1086); Slack DM / @-mention aggregators (#1085).

### Home & content surfaces (M3)

- **#1194 — "Recently" view**: persistent recency panel on home surfaces composted insights — no consume-on-render.
- **#1195 — AutonomousExecutor wired**: pattern-application path now has a read-only autonomous executor (flag-gated, defense-in-depth).
- **Design language CXO Part-B**: B1 design tokens + Card component + home modules re-skinned per CXO spec.

### Trust, Privacy & Security

- **#1089 — Privacy filter** (5 increments): `PrivacyLevel`/`FilterReason` enums, service-layer write-path gate + read-path filter, repository-layer safety net, audit-log integration.
- **#1017 — Output filtering + durable audit envelope**: `OutputFilter` decorates `LLMClient.complete`; ADR-061 v1.1 probe set.
- **#1087 — JWT prod guard**: fail loud when `JWT_SECRET_KEY` is unset in production.
- **#1095 / #1075 — Transparency API**: user-binding + admin gates; migrated to `/api/v1/`.
- **#857 — Seamless token refresh**: refresh cookie + `/refresh` endpoint + 401-retry wrapper.
- **#1196–#1198 — Honesty batch**: no fabricated access claims, no false capability promises, no sycophantic confirmations — build guard enforces.

### Ethics through the Floor

- **#992 — Boundary decisions via the floor** (Phases A–F): ethics denials now route through the conversational floor with denial-mode voice, plus a false-positive scan against the canonical corpus.
- **#990 — Removed** the deprecated `EthicsBoundaryMiddleware`.

### LLM providers

- **Gemini** wired as a real primary/fallback provider in `LLMClient`.
- **Model alias deprecation map**: `MODEL_ALIASES` + resolver at all 3 request choke points — warns on stale alias hits; claude-sonnet-4-6 / claude-opus-4-8 updated before June 15 deprecation deadline.

### Test & quality infrastructure

- Automated canonical conversation suite (#928), AAXT golden multi-turn scenarios (#929), CI integration for E2E + canonical + AAXT (#930), multi-turn evaluation harness (#1070), fabrication-probe set (#995), scorer vocabulary / pathological-tagging (#993/#994), warm-user canonical fixtures (#989).

---

## Known limitations (alpha testers, read this)

This build closes M1+M2+M3. Honest current edges going into the RECONNECT sprint:

- **Standup UI is still legacy** — the backend honest standup engine shipped in M3; the UI hasn't been updated yet. Standup answers via the floor are good; the dedicated standup UI surface is stale.
- **Cross-session memory/persistence is maturing** (#976/#953/#669). Provenance is DB-backed; broader memory composting is in progress.
- **6 fabrication/phantom cases** flagged in Run 11 are queued for the #995 fabrication-probe re-run.

When Piper can't do something or lacks context, it is designed to **say so** rather than fabricate — if you see it invent, that's a bug worth reporting.

---

## Version mechanics

- **Increment**: **0.8.7**, tracking release *stage* (M-series dev line). 0.9.0 reserved for Beta at M5 close; 1.0 = GA.
- **Cut commit**: **`9a1094672`** — `log(lead): Fire 8 — M3 CLOSING GATE #1165 CLOSED (all 6 items verified); M3 gate cleared` (June 14, 2026). Canonical regression 252/252 clean at this point.
- **Tag**: `v0.8.7` annotated — "Release v0.8.7 — M1 Foundation + M2 Conscious Floor + M3 UI Coherence".
- **Version file note**: `pyproject.toml` at the M3-close commit still reads `0.8.6` (bump was not committed at gate close). The next release (v0.8.8) includes the pyproject bump to 0.8.8, so `0.8.7` self-reports via tag only. This is a known gap, not a rollback risk.
- **Release model**: `v0.8.7` tag on shared `main` history at the cut commit; `production` advances to `v0.8.8` (next release) rather than stopping at `v0.8.7` mid-stream.

---

## Upgrade Instructions

```bash
git checkout production && git pull origin production
pip install -r requirements.txt
python -m alembic upgrade head   # migrations across M1–M3
docker compose up -d              # postgres:5433, redis, chromadb
python main.py                    # port 8001 (or PIPER_PORT)
```

---

## Contributors

- Claude (Lead Developer + leadership/staff agent cohort) — implementation, testing, methodology
- xian (PM/founder) — design, testing, sprint management

---

## See Also

- [Release Notes v0.8.6](RELEASE-NOTES-v0.8.6.md) — prior release (M0)
- [Release Notes v0.8.8](RELEASE-NOTES-v0.8.8.md) — next release (D1/RECONNECT)
- [BRIEFING-CURRENT-STATE](../briefing/BRIEFING-CURRENT-STATE.md) — live milestone status
- [Alpha Quickstart](../ALPHA_QUICKSTART.md) — setup guide

---

_Released: June 14, 2026 — v0.8.7 tagged at `9a1094672` (M3-close gate, 252/252 clean). Three milestones shipped. v0.8.8 follows from D1/RECONNECT close._
