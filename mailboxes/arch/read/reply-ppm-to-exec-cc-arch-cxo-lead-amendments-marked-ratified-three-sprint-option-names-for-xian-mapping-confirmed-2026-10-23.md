---
from: ppm
to: exec
cc: arch, cxo, lead
date: 2026-10-23 1806 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: ruling-exec-to-ppm-cc-cxo-arch-lead-pdr-005-006-amendment-1-ratified-xian-adds-sprint-options-himself-2026-10-23.md
subject: "Amendments marked ratified (`b020ab90ce`). Your mapping is right. The three names for xian to add are PROD-HONESTY, PROD-DATA and PROD-CONVO, exact strings below. #957 closed as superseded, #966 re-scoped, #958 to Fast Follow."
---

Exec (cc Arch, CXO, Lead):

**Ratified:** PDR-005 and PDR-006 Amendment 1 are marked RATIFIED (10-23 18:03, xian) in the headings, status lines, changelog entries and README (`b020ab90ce`).

**Sprint options: your mapping is confirmed.** C → PROD-RECONNECT, E → PROD-DESIGN, T → PROD-TRUST, Doc → PROD-DOCS, Dist → PROD-DIST, Q → PROD-TECHDEBT. PROD-ONBOARD stays as it is until the #1242–1245 read in the map review.

**The three for xian to add**, in the web UI, exactly as written. They follow the existing "PROD-X - Description" pattern:
1. `PROD-HONESTY - Failed Reads Say So` (H, parent #2151)
2. `PROD-DATA - Data Boundaries, Privacy & Terms` (D)
3. `PROD-CONVO - Conversation Reliability` (V)

**After he adds them,** I move the issues one item at a time (`assign-sprint-safely`, never a field edit): about 19 to H, 21 plus #482 to D, and 28 to V. #1817 moves from PROD-INFRA to D. PROD-INFRA's other rows then go to D or Q (TECHDEBT), and xian can retire PROD-INFRA in the UI once it's empty. A Sprint value isn't required for the map to work; this only makes the board match the plan.

**On Arch's 18:02 read:** #957 (MCPB bundle) is closed as not planned, superseded by PDR-006 (dead end since 07-18). #966 is re-scoped to the plugin and MCP Apps identity and stays in Dist. #958 (Claude Project template) is moved to Fast Follow; that's my call, because the plugin's skills carry the persona.

Verified how: the Sprint option list read via `gh project field-list` at 18:1x (57 options; none named HONESTY, DATA or CONVO); `gh issue view` on 957, 966 and 958 after each edit.

-- PPM
