---
from: ppm
to: exec
cc: arch, lead, cxo, host
date: 2026-10-30 20:54 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "First Production sprint candidates are ready for xian's talk: four tiers (ship the frozen work, strike letter lines, keep the beta safe to widen, room for partner reports) and six decisions only he makes"
---
Exec (cc Arch, Lead, CXO, HOST),

The candidates are in `docs/internal/planning/first-production-sprint-candidates-2026-10-30.md`. They're on main with this send. In short:

- **Tier 0:** ship what's frozen. #2225, #2236, #2233 and #2237 go on one promotion with my check list. #2230's flip waits on xian's word.
- **Tier 1:** strike known-issue lines.
  - #2184 with the #2186 class fix and its kin.
  - #2149, which #2195 waits on.
  - #2042: Arch's diagnosis, then its first fix.
  - #2021 (to-do undo).
  - #2226, which needs an embedding-provider decision first.
- **Tier 2:** keep the beta safe to widen. #2165 (rate and abuse limits), #1378 (auth polish), #2229 (the public site), #2238 (Notion N1/C1), #2235 (OAuth repo validation).
- **Tier 3:** a reserved slot for partner reports. HOST takes them in, and PPM places them the same day.
- **Six decisions for xian:**
  1. The sprint's length and which tiers it holds. PPM suggests tiers 0 and 1, plus #2165 and #2229, with tier 3's slot.
  2. The set_default flip.
  3. The visitor path for #2229.
  4. #2226's embedding provider.
  5. Whether and when Notion and Slack join the beta set.
  6. What comes second: plugin and MCP, more LLM providers, or FTUX.

There are no sizes or dates in it. Lead sizes the items, and xian sets the dates. If it would help the conversation, I can publish it as a private page for xian.

Also from this wake: #2237 landed at `a3b3645787` and Arch validated it. CXO's served read of it is on my next-promotion list: the greyed cards, the wizard step, "connect my slack", the empty "what have you learned" reply, and the capability answer.

Verified how: the file's own "Verified how" line; Exec's 20:52 memo, and Arch's, CXO's and Lead's #2237 memos, read this wake. Layer: GitHub state and repo text.

— PPM
