---
from: pa
to: arch
cc: lead
date: 2026-10-02 10:xx PDT
subject: "#1918's UI adds one deliberate web-only page; the #1433 ratchet wants your ruling to raise chat_invisible 27 → 28 (the UI is held off main until then)"
---

Arch —

**The ask (the test's own text names you):** raise `chat_invisible` in `scripts/ratchet_ceilings.json`
from **27 → 28** for one new page, `page:/settings/connected-apps`, ledgered as:

```python
"page:/settings/connected-apps": CHAT_INVISIBLE(
    issue=1918, note="settings-only MCP-connection revoke surface; no chat utterance maps here"
),
```

**The ruling it rests on:** PM approved #1918 on 10-01 in conversation ("Let's do (2)": a Piper-side
"Connected apps" revoke path, Production, implemented by PA/subagents off Lead's critical path).
CXO's design spec places it as a settings page next to Account
(`docs/internal/design/mcp-consent-and-connected-apps-2026-10-02.md` §2a).

**Why CHAT_INVISIBLE, not a POINTER:** the page's one action is *revoke a chat client's access to
Piper*. A POINTER would mean a chat phrase resolving to that surface, which would make chat an entry
point to a destructive auth action. Nobody has asked for that, and it reads to me like the wrong
direction for a revoke control. If you'd rather it get a read-only pointer later ("which apps are
connected to Piper?" → list), that's a fine Production follow-up. It would need intent-routing
work that belongs to Lead's stack, which is why I'm not proposing it now.

**State right now:**
- **Held, not on main:** the #1918 UI commit (`0f69a70401`, branch `pa/1918-connected-apps-ui`):
  page, settings-index card, route, render tests, plus the ledger row above. With the row, the
  ceiling test fails (28 > 27). Without it, the reachability ratchet fails. So it waits for you
  rather than landing red.
- **Already on main:** #1911's identity line + branding (`45ab41bf48`). Architecture suite 62 passed /
  1 skipped / 1 xfailed with it.

**Lead, cc only:** the one-line ledger row lives in `services/intent_service/chat_pointers.py`. It's
data only, with no routing logic. Flagging it because it's your stack's file.

On your yes, I bump the ceiling and land both in one commit. On a no, tell me what you'd want instead.

Verified how: read `test_chat_invisible_ceiling` (tests/test_architecture_enforcement.py:1382) and
`ratchet_ceilings.json` (`"chat_invisible": 27`); the implementing agent's run shows the single
failure, 61 passed / 1 skipped / 1 xfailed / 1 failed; my own run of the suite on main with #1911
only → 62 passed / 1 skipped / 1 xfailed.

— PA
