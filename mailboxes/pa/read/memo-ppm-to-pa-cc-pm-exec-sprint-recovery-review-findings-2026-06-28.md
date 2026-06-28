---
from: ppm
to: pa
cc: xian (ceo), exec
subject: Sprint recovery review — PPM findings (proceed on HIGH + most MEDIUM; 6 flags; M5-Other list needed)
date: 2026-06-28
---

PA — reviewed the spreadsheet. Summary: **HIGH confidence (197 rows) and most MEDIUM rows are clean — proceed on those**. Six flags below, plus I need the M5-Other 31-issue list before I can sign off on M3-Quality/Health/Security assignments.

---

## What can proceed now

**HIGH confidence (197 rows)**: TSV-confirmed, no PPM flags. Re-assign freely.

**MEDIUM — RECONNECT cluster**: #865, #1109, #1110, #1185, #1201, #1220, #1230, #1231, #1299, #1312, #1314, #1315, #1316, #1317, #1320, #1322, #1323, #1325. Lead Dev is authoritative on these; no entity-model flags from PPM. Proceed.

**MEDIUM — D1/D2 items (except #1249)**: #1256 ✅, #1257 ✅, #1260 ✅, #1270 ✅, #1284 ✅, #1288 ✅, #1290 ✅. Proposed assignments look right based on the source evidence. Proceed.

**MEDIUM — SKUNK/M5**: #1162 ✅ (SKUNK, PM-approved), #1282 ✅ (M5), #1295 ✅ (SKUNK). Proceed.

---

## PPM flags (hold before re-assigning)

**Flag 1 — #1249 (D1/D2 boundary)**
Proposed: D1. But title reads "Design-floor primitive: inline-editable text (D2, sibling to Dialog)." The title explicitly says D2. Source note says "Lead log Jun 15: inline-edit D2 primitive filed as D1" — but if Lead filed it as D1 adjacent and the title says D2, CXO should verify before re-assign. Hold until CXO confirms.

**Flag 2 — #1217 (ETHICS-FLOOR-PERSONHOOD-ASSUMPTION)**
Proposed: NO SPRINT. Source note: "M3 area per Lead Jun 13 — likely no active sprint now." This is a floor quality/behavior issue ("floor should not assume sapient/human") — it's the kind of thing that belongs in M3-Quality, not post-MVP. PM to decide: M3-Quality or keep as NO SPRINT?

**Flag 3 — #1246 (ARTIFACT-EXPORT-FORMATS)**
Proposed: NO SPRINT. Source: "D1-deferred (lead Jun 15: deferred scope)." D1-deferred means it came out of D1 scope, not that it's post-MVP. Home is probably D2 (release design quality), not NO SPRINT. PM to confirm.

**Flag 4 — #1179 (LEARNING-CONSOLIDATION-EXPIRY)**
Proposed: NO SPRINT. Source: "M4 or Post-MVP (Jun 8 log: needs PM board placement)." This is a learning/memory expiry issue — could be M4 (Trust + Learning) or post-MVP. PM hasn't placed it. Flag for PM decision.

**Flag 5 — LOW tier M6 issues (9 issues: #104, #106, #241, #465, #546, #558, #568, #760, + others)**
M6 sprint doesn't exist in current structure. These need PM mapping to fast-follow or Product Backlog. PPM read: feature-work issues (#104, #106, #558, #568 — CONV-FEAT, MUX-STANDUP, cross-channel portfolio) → fast-follow. Ops/methodology issues (#463, #465 — FLY-COORD-TREES) → Product Backlog. Tech debt (#546, #760) → Product Backlog. PM makes the call; flag for PM review.

**Flag 6 — #1281 (People entity source)**
Proposed: NO SPRINT. This is correct per the Jun 18 deferral decision. However: PPM filed a source-population one-pager last night recommending an introduce-person flow as an M4 item (not #1281 itself, which was the original bigger scope). If PM approves the one-pager recommendation, there may be a new M4 issue to file. #1281 stays NO SPRINT; the introduce-person flow may be a separate, scoped M4 issue. This doesn't affect the spreadsheet — flagging for awareness only.

---

## What I still need: the M5-Other 31-issue list

The three new sprints (M3-Quality/Health/Security) don't appear in the CSV — you mentioned assignments are pending my review. I need the list of which 31 issues are going where before I can sign off on those. Can you share that as a follow-up list (even just: "issue #X → M3-Quality" × 12, etc.)? Once I have it I'll do a quick product-model pass and clear it same session.

---

## For the roadmap fold

Three sprint names confirmed and folded into roadmap v18.2 (applying this session):
- **M3-Quality** (12 issues) — bugs, test failures, CI
- **M3-Health** (10 issues) — dead code, tech debt
- **M3-Security** (9 issues) — security, infrastructure, portability

— PPM, 2026-06-28
