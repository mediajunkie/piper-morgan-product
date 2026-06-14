# M3-Close Triage — what actually blocks M3 vs. what's just MVP-tagged

**Status**: DRAFT for PM · **Author**: Lead Dev · **Date**: 2026-06-14
**Question (PM)**: of the ~76 open "MVP"-milestone issues, which actually block **M3 close** vs. which are just tagged to the milestone and can slip?

**Caveat**: precise M3/M4/M5 placement is the board's **Iteration field** (the milestone is the July-4 MVP umbrella, not the iteration). This is a best-effort cut by title/label/session-knowledge — reconcile against the board. But the headline doesn't depend on it:

---

## Headline: you're DAYS from M3 close, not weeks

**M3 close is gated by exactly one issue — #1165** (it *is* the "M3 closing gate"). Everything else on the MVP milestone is M4 / M5 / Fast-Follow work that's tagged to the umbrella, **not** a precondition for calling M3 done.

### M3-CLOSE BLOCKERS (the whole list)
- **#1165 — M3 closing gate.** Remaining: (1) the UAT walk — **item 1 (#1155) ✅ just passed**; items 2–5 (#496 / #497 / #1133 / #1143) still to walk; (2) the History→Radar scope decision (✅ decided — Radar work captured in #1090 → M5). On a clean walk, #1165 closes and **M3 closes with it.**

That's it. Nothing else blocks the *close*.

---

## BETA-MUST-FIX (don't slip past beta — correctness/trust; M4-priority, not M3-close blockers)
The risks you flagged + their siblings. These don't block M3 *close*, but they should land before real users:
- **#1223** — `get_recent_turns` returns oldest turns, not most-recent (silent data-correctness bug). ⚠️ your call-out.
- **#1218 / #1217** — `#NNN` patterns mis-trigger `close_issue` at full confidence / floor personhood assumption (PA-filed routing bugs). ⚠️ real for a PM tool that quotes issue numbers constantly. *(Note: I couldn't reproduce these in 10 probes earlier — they're context-dependent; worth a focused repro with PA's session before/while fixing.)*
- **#1216** — workstyle-provenance honesty (trust). You placed it M4 (Trust & Learning); agree it's beta, not post-MVP.
- Adjacent: **#1105** (LLM keychain re-paste regression), **#1131** (stateless judge flags honest todos), **#1151** (empty `original_message` response), **#1219** (classifier false-negatives).

## SECURITY — needs an explicit beta-vs-release call (don't let these hide in the 76)
- **#358 — Encryption at rest (priority: critical, size: large).** Real user data in beta → this needs a deliberate placement, not drift. HOST/Arch + you.
- **#542** (token revocation on disconnect), **#482** (KMS), **#441** (auth phase 2), **#1149** (debug-route prod exposure).

## CONNECTOR REFACTOR → M4/M5 (today's decision; MCP)
#1220 (umbrella) · #1226 (debt) · #1199 (two stores) · #1227 (Slack mrkdwn) · #1225 (module dismiss) · #1201 (Slack inbound setup) · #1061 (multi-OAuth) · WS-9 identity unification. Scoped in `connector-refactor-sprint-scope-2026-06-14.md`; awaits Arch's ADR before decomposition.

## M4 — Trust & Learning
#954 (trust-lite) · #955 (pref-infer) · #956 (learning-surface) · #1062 (learning ph3) · #1174 (proactive presence) · #1166 (type-2 dreaming) · #1209 (autonomous-executor flesh-out) · #973 / #972 (memory audits) · #1185 (BYO-key multi-tenant).

## M5 — Polish & Distro
UI design-floor: #1169 (epic) / #1170 / #1171 / #1172 / #1173 / #1164 / #1048 / #1043 / #1090 (UI-1.0 + Radar) / #713 / #712 / #998. Distribution/MCP-packaging: #966 / #959 / #958 / #957 / #829 / #830 / #831 / #832 / #302. Portability/hosting: #1167 / #1168 / #1176 / #1162.

## FAST-FOLLOW / TECH-DEBT (slip freely)
#1224 · #1211 · #1144 · #1139 · #1138 · #1153 · #1175 · #1028 · #1206 · #683 · #865 · #1001 · #1203 · #1202 · #1184 · #1183 · #1186 · #1190 · #1160 · #558 · #557 (websocket) · #371 (timeseries) · #118 (multi-agent coordinator).

---

## Recommended next moves
1. **Finish the #1165 walk** (items 2–5) → close M3. That's the days-not-weeks path. *(In progress; item 1 passed.)*
2. **Re-tag the board** so "MVP/M3" reflects reality — most of the 76 are M4/M5/Fast-Follow. (PM/PPM own the Iteration field; this doc is the input.)
3. **Make the explicit calls** on the two things that shouldn't drift: the **beta-must-fix** set and **#358 (encryption at rest)**.
4. Connector refactor + identity unification proceed on the MCP track (Arch ADR → decompose).
