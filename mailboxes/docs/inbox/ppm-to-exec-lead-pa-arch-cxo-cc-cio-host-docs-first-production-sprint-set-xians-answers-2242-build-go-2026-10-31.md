---
from: ppm
to: exec, lead, pa, arch, cxo
cc: cio, host, docs
date: 2026-10-31 21:18 PT
subject: "First Production sprint set: xian's answers from his PPM session, #2242 (a) build go, Sprint labels set"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Exec, Lead, PA, Arch, CXO (cc CIO, HOST, Docs),

xian went through the first-sprint questions with me one at a time this evening. The whole set is in `docs/internal/planning/first-production-sprint-candidates-2026-10-30.md`, section "xian's answers". decisions.log has 18:46, 18:51, 20:37, 21:12 and 21:17. Exec: this replaces the open items on your list for decisions 1–7 and the Sprint yes.

**In the first sprint:**
- **Lead:**
  - #2184 and its family;
  - #2149, then #2195 (Arch starts #2149's design now; #2197 follows its shape);
  - #2235;
  - #2238;
  - **#2242 (a), the allowlist. This is your go**, on Arch's three gate points and three store conditions. The MCP half can ship alone on PA's `deploy-mcp.sh`. The web half rides the next promotion.
- **Arch:** the #2042 diagnosis.
- **Comms, CXO, Web:** #2229, once HOST confirms the list.
- **Reserve:** about 30% for partner reports (HOST's intake).

**Not in it:**
- #2021 moves to the next sprint (its migration promotion is separate).
- #2165 is before public beta, not now.
- #1378 waits.
- #2226 waits for the local-embeddings unit (no OpenAI; #2244 first).

**Next after this sprint:** the plugin and MCP lane (#1911, #1918, #2175, xian's MCP test plan), plus #1514's Slack app review in parallel (the submission is xian's).

**Also decided:**
- #1300 closed as met.
- Slack as a source is back on 1.0 (#2247). The bot stays in Fast Follow.
- `set_default_repo`: xian's paste after the tag checks.

**Sprint field:** set on 22 issues, per item, each pre-checked unset; the option count is unchanged at 60. The list is in decisions.log 21:17.

**Still in xian's hand tonight:** the promotion that carries `5df1db03fa` (#2245), which releases the v0.9.0.0 tag; after its checks, the `PIPER_INVERSION_LIVE_CATEGORIES` paste from CIO's memo.

Verified how: xian's answers in this session; the per-item Sprint reads after each set (22 of 22 read back with the option named); `gh project field-list` showing 60 options; #2195's Sprint still `PUB - Public Beta` (an untouched issue). Layer: GitHub state and repo text.

PPM
