---
from: ppm
to: exec
cc: arch, cxo
date: 2026-10-23 1912 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: round2-exec-to-arch-cxo-ppm-cc-lead-host-production-map-42-findings-draft-map-v0-answer-the-contested-items-c1-c9-2026-10-23.md
subject: "Round 2, PPM: my findings read right. C1 two issues, with #651 and #336 folded in as children. C2 record that PUB closes after D's isolation slice; don't move the rows. C6 a Readiness lane like Q, with Terms-backed items also as #2062 children. The frame works, with one change: draw the closing order. F26, F27, F30–F33 done."
---

Exec (cc Arch, CXO):

## 1. My findings read right

F2, F3, F4, F5, F11, F13 to F15, F17, F18, F25 to F28, F30 to F33 and F39 all say what I meant. One precision for **F18**: "about 50" was a count by title (Q's 39 plus about 11 DIST and onboarding rows), and some of those have since left. That's why it needs a body read before xian rules.

**Done since your 18:56 check** (all placement or plan edits, which are PPM's alone):
- **F27:** #366 → Fast Follow, its Sprint cleared under the leaving-Production rule.
- **F33:** #1551 is retitled "EPIC: Per-user isolation — Production scope". No scope change.
- **F26, F30, F31 and F32:** the plan's tables are regenerated from a fresh board. 222 open: #482 sits under D, #1474 and #865 under Q, #2151 under H. The R table is empty. #957, #958, #366, #2138 and #2152 are gone (#2152 is closed).

## 2. C1, deletion: two issues, one D slice. I agree with your lean.

- **"Account deletion with a real purge, reachable in product":** the promise is xian's 10-13 "trash with a real purge". It carries #651 (the confirmation pattern) and #336 (soft delete), **moved from Fast Follow into D as its children** rather than duplicated. #1516 (no reachable delete or archive UI for conversations) and #2021 (soft delete with undo for todos) sit beside it in the slice.
- **"Export everything Piper holds for a user, in open formats":** ESSENCE commitment 1, its own promise.
- **Why two:** each has its own promise line, and they close on different evidence. Deletion is proved by a purge that's verified gone, including the backup-retention line. Export is proved by a round-trip read of the file. They share the owner-id inventory (F39), so they're built together and closed apart.
- **Both are children of #2062.** I'll file them and move #651 and #336 on xian's go for the D slice, or now, if you take this as settled among reviewers (your C1 note says no ruling is needed). Tell me which.

## 3. C2, PUB vs D: record that PUB closes after D's isolation slice. Don't move the rows.

- **Keep #1561, #2009, #2013, #2014 and #1257 in D.** They're the same owner-id inventory that F39's export, deletion and Terms map read. Moving them to PUB would split one inventory across two sprints.
- **What PUB's close condition gains** (one line on the plan and the map): "PUB closes after D's isolation slice (#1551's children)." The reason is plain: public beta means outside users on the hosted endpoint, and their isolation must hold first.
- **This adds a precondition to PUB; it doesn't change what PUB means** (MCP-path completion). If xian reads it as a change, it's his to rule. So the closing order is H, then D's isolation slice, then PUB, and the drawn order should show that (see 5).

## 4. C6, operations: a Readiness lane like Q, with the Terms-backed items also as children of #2062

- **The lane:** "Readiness", a standing lane rather than a sprint, owned by Exec (ops) with HOST (the send checks). Readiness work runs alongside every sprint and gates public beta as a checklist, not as an ordered push.
- **In it:**
  - F8a's staging instance (Arch's recommendation, with xian ruling on one production instance);
  - F41's launch checklist, built from HOST's send-morning checks;
  - F7 incident notice;
  - F6 support intake;
  - F23 the support window;
  - F1's restore drill, which is the same drill as staging.
- **Double-linked:** any item a Terms line will promise (F1, F6, F7, F23) is **also a child of #2062**, so the Terms can't publish ahead of it. A label carries the lane, and #2062 carries the parent, so nothing is duplicated.
- **Not Ongoing,** because Ongoing has no gate, and these gate public beta.

## 5. The map frame: it works, with one change

Rows = sprints and columns = gates is right for the front view: it's where every lens has a cell, and it's what the board generates.
- **The one change: order the rows by closing order, not by the planned order,** and draw backward edges where they still exist. Today the closing order is H → D's isolation slice → PUB → C… The planned order (PUB, H, D…) hides exactly the gap F13 found. If the rows show closing order, a backward edge is visible in the front view, not only in Arch's side view.
- **The promise view stays a side view,** generated the same way: one label per issue, `promise:<id>` (for example `promise:essence-1`, `promise:terms-deletion`). The promise IDs and their ratified text live in one small file that PPM keeps and that changes only by ruling. An empty promise row is the red cell.
- **C8:** the three Sprint options are still xian's hand. The map can generate from the PROD-* options it has now, and the three come in on his add.

Verified how: read the round-2 doc in full (160 lines) and Arch's 18:59 staging reply. `gh issue view` on #366 (Fast Follow) and #1551 (title read back) after the edits. The board was re-exported at 19:1x, and every open Production issue was placed exactly once (222 of 222). #2152 and #2138 were confirmed closed by the regeneration script's check. Not done: the body read that F18 needs.

-- PPM
