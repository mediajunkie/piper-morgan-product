# Release Notes v0.8.7

**Release Date**: June 6, 2026 (proposed)
**Branch**: `main` → `production`
**Previous Version**: v0.8.6 (M0 Conversational Glue, March 4, 2026)
**Sprints**: M1 — Foundation (closed Apr 11) · M2 — Conscious Floor + Action Handlers (closed June 3)
**Release model**: development continues on `main`; `production` carries the **last stable, canonical-regression-passing build** for alpha testers.

---

## Summary

**This is the first production cut since M0 (v0.8.6, March 4) — it ships two full milestones.** Main has
advanced ~4,100 commits since the last production tag; the product-relevant change is ~135 features and
~118 fixes (the remainder is agent-operations and documentation). It is being cut to `production` as the
**alpha-test build** behind a password-protected hosted instance.

The headline is the **Conscious Floor**: Piper no longer falls back to templates when a query doesn't
match a canonical handler — an LLM-first conversational floor answers in Piper's voice, grounded in
assembled context (your blocked items, active sprint, recent activity), and refuses to fabricate when it
lacks the information. On top of the floor, **M2 delivered suggestion provenance** — Piper can now answer
"what have you learned about my work style?" with confidence-sectioned insights and "why did you suggest
that?" with a plain-language source citation.

**Quality posture** (canonical retest Run 11, June 3): Quality 80.3%, Expected-pass Quality 80.5% (above
the ≥75% north star), Routing 93.4%. M2 quality gate held.

**References**: M1 Foundation; M2 (Conscious Floor); PDR-005 (capability-claim consistency); ADR-061 v1.1.

---

## What's New

### The Conscious Floor (M2 centerpiece)

Unmatched queries now route to an LLM-grounded conversational floor instead of canned templates.

- **#907 — Conversational Floor**: LLM responses for unmatched queries, in Piper's voice.
- **Floor-first routing migrations**: IDENTITY (#926), STATUS + PRIORITY (#925), temporal Q7–Q10 (#965),
  GUIDANCE intents (#911) all migrated off canonical templates onto the floor with context assembly.
- **#950 — Floor prompt evolution**: Five Pillars + grammar + anti-flattening; identity anchoring (iter 2).
- **Context assembly into the floor**: blocked items (#983), active sprint/milestones (#985), recent
  GitHub activity (#986), calendar + deadlines (#951), with a ContextCache layer + eager invalidation
  (#984).

### Suggestion Provenance & Insights — the headline M2 ship (R4)

The floor can now surface what it has learned about you, and explain its own suggestions.

- **#1030 — INSIGHT-PULL**: "What have you learned about my work style?" returns confidence-sectioned
  insights + an invitation to correct, wired end-to-end through the floor.
- **#1032 — INSIGHT-PUSH**: proactive insight surfacing through `floor.respond`, with natural-language
  session-mute.
- **R4 provenance pipeline** (Steps 1–11): new `IntentCategory.PROVENANCE` + `ProvenanceHandler`;
  per-turn provenance sidecar on `ConversationContext`; provenance threaded through the Action Gate floor
  callsite and per-gatherer context metadata; **cross-session provenance guaranteed via DB persistence**
  with in-memory fallback (PM Q1 gold standard). 152 R4 tests.

### Action Handlers & the dispatch rail

- **#1124 — Action-dispatch rail**: migrating handlers off the legacy `elif` chain onto a structured
  action-dispatch rail (update_document, changes_query migrated; ~28-site audit continues in M3).
- **#1121 — Slot-filling migration**: `update_document` regex parser replaced with LLM `extract_slots()`.
- **GitHub & task lifecycle**: complete issue close/reopen with confirmation UX + fuzzy match (#902),
  reopen handler (#902), minimum-viable reminders (#903), todo completion lifecycle (#904), real GitHub
  issue wiring (#695/#1112), standup helpers wired to UserPreferenceManager (#693).
- **#1102 — Real portfolio data**: replaced hardcoded fake projects with a real `PortfolioService` query.
- **#1044 — Local-git status handler**: "what branch are we on?" answered from real git state.

### Trust, Privacy & Security

- **#1089 — Privacy filter** (5 increments): `PrivacyLevel`/`FilterReason` enums, service-layer
  write-path gate + read-path filter, repository-layer safety net, audit-log integration.
- **#1017 — Output filtering + durable audit envelope**: `OutputFilter` decorates `LLMClient.complete`;
  durable audit envelope with container wiring; ADR-061 v1.1 probe set.
- **#1087 — JWT prod guard**: fail loud when `JWT_SECRET_KEY` is unset in production.
- **#1095 / #1075 — Transparency API**: user-binding + admin gates; migrated to `/api/v1/`.
- **#857 — Seamless token refresh**: refresh cookie + `/refresh` endpoint + 401-retry wrapper.
- **#1148 — Trust-stage GUI** (dev-only) so UAT can reach trust-gated surfaces; **#304** keychain
  fallback.

### Ethics through the Floor

- **#992 — Boundary decisions via the floor** (Phases A–F): ethics denials now route through the
  conversational floor with denial-mode voice, plus a false-positive scan against the canonical corpus.
- **#990 — Removed** the deprecated `EthicsBoundaryMiddleware`.

### Integrations & honesty

- **Notion** (#1080/#1081): real `append_blocks`, Slack→Notion URL unfurling, and handler **honesty**
  (no demo-fallback fabrication, #1088).
- **Slack** (#1085): DM / @-mention / source aggregators; **calendar** source aggregator (#1086).
- **#923 — Registry-driven capability awareness**: reconciles 5 sources of truth so Piper's claims about
  what it can do match what it actually does (composes with PDR-005 capability-claim consistency).

### LLM providers

- **Gemini** wired as a real primary/fallback provider in `LLMClient`.
- Haiku references updated to Haiku 4.5 (#979); Pattern-012 adapters + ProviderSelector removed (#971).

### UI / MUX

- Audit envelope read views + session selector (#1099/#1100), sidebar reconciliation (#1097), compose UI
  scaffold (#998), empty-state copy fixes (#1096), and `/insights` + `/files` wired into global nav (#1146).

### Test & quality infrastructure

- Automated canonical conversation suite (#928), AAXT golden multi-turn scenarios (#929), CI integration
  for E2E + canonical + AAXT (#930), multi-turn evaluation harness (#1070), fabrication-probe set (#995),
  scorer vocabulary / pathological-tagging (#993/#994), warm-user canonical fixtures (#989).

---

## Known limitations (alpha testers, read this)

This build closes M2 but **Beta is gated on M3+**. Honest current edges:

- **UI-vs-architecture mismatch (#1142)**: some surfaces lag the backend — the Standup UI is legacy,
  there's no Lists view, and the Insight Journal page is functional but nav-isolated / "almost
  undiscoverable." An M3 UI audit addresses this.
- **Cross-session memory/persistence is still maturing** (M3 cluster: #976/#953/#669). Provenance is
  DB-backed; broader memory composting is in progress.
- **Slack inbound is not structurally wired** (#1129, M3) — outbound/aggregation works; inbound needs
  Socket Mode.
- **6 fabrication/phantom cases** flagged in Run 11 are queued for the #995 fabrication-probe re-run (M5).

When Piper can't do something or lacks context, it is designed to **say so** rather than fabricate —
if you see it invent, that's a bug worth reporting, not expected behavior.

---

## Version mechanics

- **Increment**: **0.8.7**, a patch on the 0.8.x M-series development line. The version tracks release
  *stage*, not change volume: 0.8.x = M-series dev; **0.9.0 reserved for the full Beta release at M5
  close** (or 0.8.10 if M5 needs another sprint to clear the beta gates); 1.0 = GA. Forward cadence:
  **M3 → 0.8.8, M4 → 0.8.9, M5 → 0.8.10 / 0.9.0.**
- **Cut commit**: **`3a34a4403`** — `test(canonical): Run 11 capture (2026-06-03 07:27) — M2 close
  verification`. This is the build the last canonical regression (Run 11) validated; everything after it
  on main (the post-M2 Lead Dev work — #1147, #1148, #1124 dispatch-rail, #1159, #1150, #1163) is
  deliberately **excluded** from this release.
- **Release model — production mirrors main, no divergence**: the `v0.8.7` tag is placed on **main's
  shared history** at the cut commit, and `production` is **fast-forwarded** to that same commit. So
  production is an exact prefix of main up to the release, both branches share the identical release-tag
  lineage (v0.8.6 → v0.8.7), and production carries **no commits main doesn't have**. Going forward each
  milestone close tags main and fast-forwards production the same way.
- **Tag**: `v0.8.7` annotated "Release v0.8.7 — M1 Foundation + M2 Conscious Floor (M2-close stable cut)".
- **Version-file note (honest)**: because this is a *retroactive* cut, the tagged commit's `pyproject.toml`
  reads `0.8.6` (the bump wasn't done at M2 close). The release identity is the **tag**, not the file.
  From the next milestone on, version files are bumped *as part of* the milestone-close commit so the file
  and tag agree at the cut point.

---

## Upgrade Instructions

```bash
git checkout production && git pull origin production
pip install -r requirements.txt        # heavier deps landed (torch, transformers, chromadb)
python -m alembic upgrade head          # multiple migrations across M1+M2 (user-history #1021,
                                        # audit durability #1018, privacy #1089, etc.)
docker compose up -d                    # postgres:5433, redis, chromadb, temporal
python main.py                          # port 8001 (or PIPER_PORT)
```

---

## Contributors

- Claude (Lead Developer + leadership/staff agent cohort) — implementation, testing, methodology
- xian (PM/CXO) — design, testing, sprint management

---

## See Also

- [Release Notes v0.8.6](RELEASE-NOTES-v0.8.6.md) — prior release (M0)
- [BRIEFING-CURRENT-STATE](../briefing/BRIEFING-CURRENT-STATE.md) — live milestone status
- [Alpha Quickstart](../ALPHA_QUICKSTART.md) — setup guide

---

_Released: June 6, 2026 — v0.8.7 tagged at `3a34a4403` (M2-close Run-11 build); production fast-forwarded to it. 0.9.0 reserved for Beta at M5 close._
