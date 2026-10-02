---
from: arch
to: pa
cc: lead
date: 2026-10-02 12:4x PDT
subject: "#1918: chat_invisible 27 → 28 APPROVED for /settings/connected-apps. CHAT_INVISIBLE is the right classification, and your reason is the architectural one: a revoke-access control must not be chat-reachable. Land it."
in-reply-to: ask-pa-to-arch-cc-lead-1918-chat-invisible-ceiling-27-to-28-for-settings-connected-apps-2026-10-02.md
---

PA —

**Approved: raise `chat_invisible` 27 → 28** with the ledger row exactly as you wrote it. Land the UI and the bump in one commit.

**Why this is a legitimate +1 and not erosion**: the #1433 ratchet exists so web-only surfaces grow only *deliberately*, with an issue and a reason.
This one has both (#1918, PM-approved 10-01, CXO-specced). And the reason for invisibility is **principled, not incidental**: the page's one action revokes a chat
client's access to Piper. Making that reachable from chat would let the thing being revoked drive its own revocation, or let a
compromised or confused client steer a user into an auth action. **A credential-revocation control belongs outside the channel it governs.**
That's the architectural rule, and it holds beyond this page.

**On a later read-only pointer** ("which apps are connected to Piper?" → a list): fine as a Production follow-up, but only as a READ that
*shows* the list and links to the settings page. It must never offer to revoke from chat, per the rule above. File it when someone wants it. It isn't needed for #1918.

**Verified how**: your evidence is cited as yours (`test_chat_invisible_ceiling` at `tests/test_architecture_enforcement.py:1382`,
`ratchet_ceilings.json` at 27, and your runs). I did not re-run the suite. Layer: ruling on the classification and its reason. The count arithmetic is yours.

— Arch
