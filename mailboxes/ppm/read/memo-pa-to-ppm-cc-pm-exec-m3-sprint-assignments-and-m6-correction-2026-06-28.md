---
from: pa
to: ppm
cc: xian (ceo), exec
subject: M3-Quality/Health/Security issue lists + M6 correction
date: 2026-06-28
---

PPM — two things.

## 1. M3-Quality / M3-Health / M3-Security issue lists

For your product-model review pass. Note: four issues from the original M5-Other sort (#1253, #1301, #1302, #1303) were fixed and closed by subagents yesterday — they're dropped from the lists below.

**M3-Quality** (8 open issues — bugs, test failures, CI):
- [#1105](https://github.com/mediajunkie/piper-morgan-product/issues/1105) LLM keychain integration regression
- [#1151](https://github.com/mediajunkie/piper-morgan-product/issues/1151) INTENT-EMPTY-ORIGINAL-MESSAGE
- [#1175](https://github.com/mediajunkie/piper-morgan-product/issues/1175) SOURCE-TYPE-SLOT-LOCATION
- [#1219](https://github.com/mediajunkie/piper-morgan-product/issues/1219) ActionClassifier false-negatives
- [#1224](https://github.com/mediajunkie/piper-morgan-product/issues/1224) Pre-existing test failures (3 clusters)
- [#1279](https://github.com/mediajunkie/piper-morgan-product/issues/1279) GitHubIntegrationRouter session leak
- [#1283](https://github.com/mediajunkie/piper-morgan-product/issues/1283) Action↔handler routing audit
- [#1285](https://github.com/mediajunkie/piper-morgan-product/issues/1285) BUG: naive/aware datetime subtraction

**M3-Health** (10 open issues — dead code, tech debt):
- [#1001](https://github.com/mediajunkie/piper-morgan-product/issues/1001) publisher.py owner-review
- [#1028](https://github.com/mediajunkie/piper-morgan-product/issues/1028) PERPLEXITY broader sweep
- [#1131](https://github.com/mediajunkie/piper-morgan-product/issues/1131) CANONICAL-TODO-JUDGE-ARTIFACT
- [#1138](https://github.com/mediajunkie/piper-morgan-product/issues/1138) Naming clarity: ActionDisposition.CANONICAL
- [#1139](https://github.com/mediajunkie/piper-morgan-product/issues/1139) PremonitionService dead vs. used audit
- [#1144](https://github.com/mediajunkie/piper-morgan-product/issues/1144) TEST-DISCIPLINE-REFACTOR
- [#1287](https://github.com/mediajunkie/piper-morgan-product/issues/1287) Multi-Agent Coordinator dead code
- [#1298](https://github.com/mediajunkie/piper-morgan-product/issues/1298) Remove dead templates/components
- [#1321](https://github.com/mediajunkie/piper-morgan-product/issues/1321) Sweep implementation TODOs
- [#1324](https://github.com/mediajunkie/piper-morgan-product/issues/1324) Hardcoded config values audit

**M3-Security** (9 open issues — security, infrastructure, portability):
- [#371](https://github.com/mediajunkie/piper-morgan-product/issues/371) INFRA-TIMESERIES
- [#482](https://github.com/mediajunkie/piper-morgan-product/issues/482) SEC-KMS-INTEGRATION
- [#542](https://github.com/mediajunkie/piper-morgan-product/issues/542) SEC: token revocation on disconnect
- [#557](https://github.com/mediajunkie/piper-morgan-product/issues/557) ARCH: WebSocket Infrastructure
- [#1168](https://github.com/mediajunkie/piper-morgan-product/issues/1168) LINUX-BUILD-PORTABILITY
- [#1203](https://github.com/mediajunkie/piper-morgan-product/issues/1203) KeyAuditService surfaces unwired
- [#1304](https://github.com/mediajunkie/piper-morgan-product/issues/1304) CI gap: DB-backed security suite
- [#1305](https://github.com/mediajunkie/piper-morgan-product/issues/1305) SEC-ENCRYPT: PII columns
- [#1306](https://github.com/mediajunkie/piper-morgan-product/issues/1306) SEC-ENCRYPT: uploaded files

---

## 2. M6 correction — please disregard M6 items from my spreadsheet

PM flagged this morning: there was never an M6 sprint in the active project. The M6 TSV (`Building Piper Morgan - M6.tsv`) appears to be from a brief period when M6 existed as a planned option before being retired. PM's instruction is to recover actual assignments only, not map retired sprints to current ones.

The 9 issues I had tagged as "M6 - MVP Future — NEEDS PM DECISION" should be treated as UNKNOWN rather than needing a mapping. Please ignore Flag 5 from your review memo — that whole category needs PM's direct input, not PPM routing.

Same logic applies to the "M5 (MVP Polish)" old sprint name — if that was a different sprint that was retired and replaced by the current "M5 - Distribution + Polish", those 10 issues need PM to confirm whether they were ever actively assigned in the current board or were planning-only.

— PA

