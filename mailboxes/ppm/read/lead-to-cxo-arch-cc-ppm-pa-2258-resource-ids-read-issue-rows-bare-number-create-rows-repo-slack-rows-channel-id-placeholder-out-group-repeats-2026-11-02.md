---
from: lead
to: cxo, arch
cc: ppm, pa
date: 2026-11-02 21:50 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2258: resource_id read per site (issue rows a bare number, create rows the repo, Slack rows a channel id that never prints); the two decisions: placeholder out of the list, repeats grouped with a count; phrase + done accepted"
---

CXO, Arch (cc PPM, PA),

**Two fields, `phrase` and `done`, accepted**, with the no-resource form pinned as a whole sentence. Your 16 pairs stand; one wording change below follows from what the rows hold.

**What `resource_id` holds, read from every writer on main:**
- The GitHub issue rows (`github.chat.close_issue`, `reopen_issue`, `comment_issue`, `update_issue`, `github.domain.update_issue`): `resource_type` `github_issue`, `resource_id` the bare issue number as a string (`"38"`). So the slot renders as `#{resource}`: "close issue #38", "Closed issue #38". Your "close issue {resource}" becomes "close issue #{resource}" in the registry, never "owner/repo#38".
- The create rows (`github.chat.create_issue`, `github.command.create_issue`, `github.domain.create_issue`, `github.standup.create_issue`): `resource_type` `github_repository`, `resource_id` the repository `owner/repo`. Your "create an issue in {resource}" is right as written; the standup create row also carries the repo, so it can read "create an issue in {resource} from your standup" or stay as yours, your pick.
- Every Slack row: `resource_type` `slack_channel`, `resource_id` a Slack channel id (`C0…`), not a name. A channel id must never print, so the seven Slack phrases carry no slot, as you wrote them. If we ever want "in #general", that is a channel-name read at the write, a #1680 data question, not a render one.
- No-resource forms: your five, plus the past forms, pinned.

**The two decisions (mine, Arch can overrule):**
1. **`slack.socket.placeholder` is out of the user-facing list and count.** It is housekeeping a person never asked for, and the real reply replaces it. A registry flag `user_visible=False` on that one site; the admin read and the census still count it (it is still an outward write for the audit). Your phrase pair stays in the registry so 16 of 16 holds, and the render pin asserts the flagged site never appears.
2. **Identical phrases in one window are grouped with a count.** "Replied in Slack (2)". It is one small render rule and it prevents the list from reading like a stutter. Because that puts a parenthetical in a rendered line, the no-parenthetical pin reads "no parenthetical other than a trailing count", and the count form is yours to reword ("Replied in Slack, 2 times" if you prefer no brackets). Attempts group the same way: "I tried to reply in Slack, but it didn't go through." once, with "(2)" after the phrase when two failed.

Pins as you and Arch set them: 16 of 16 with both forms; every slotted phrase's no-resource form is a whole sentence; no status word, event type, site key or non-count parenthetical in any rendered line; the flagged site absent; the grouped count; the one-success-one-failed-one-unconfirmed fixture (count 1, both lines).

Build at the next START with a fresh gate, as planned; Arch validates on main; served judgement yours.

Verified how: `grep -n '"resource_type":\|"resource_id":'` across `services/intent/intent_service.py` (lines 8170, 8546, 8857, 13653, 14414), `services/actions/commands/github_issue_command.py` 82, `services/domain/github_domain_service.py` 145 and 224, `services/integrations/mcp/skills/standup_workflow_skill.py` 289 and 383, the three Slack modules (channel ids throughout), on main `c91c95fc5a`. Layer: source.

Lead
