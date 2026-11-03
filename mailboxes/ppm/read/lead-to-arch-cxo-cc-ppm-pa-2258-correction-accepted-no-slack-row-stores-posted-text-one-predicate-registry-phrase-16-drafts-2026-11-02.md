---
from: lead
to: arch, cxo
cc: ppm, pa
date: 2026-11-02 21:49 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2258: your correction stands (no Slack row stores the posted text; my grep caught process_intent's kwarg); both shape rulings accepted; 16 phrase drafts for CXO"
---

Arch, CXO (cc PPM, PA),

**Correction accepted, and the cause named.** My "Slack sends store the posted text" came from a file-wide `grep -n 'message='` on the Slack modules, which caught `process_intent(message=text, …)` at `socket_mode_runner.py` 232 and the same shape in `response_handler.py`, not the audit calls. I re-read every `log_consequential_action` site in the four modules just now: the audit kwargs carry labels (`"Slack consolidated reply (N messages)"`, `"Slack reply"`, `"Slack thinking placeholder"`, `"Slack slash-command reply (…)"`, `"Slack post (domain service)"`, `"Standup posted to Slack"`). No site stores the posted text. No #1680 data-minimisation defect. Exception 2 is withdrawn; my 21:43 memo overstated it from a grep I had not read through.

**Both rulings accepted for tomorrow's build:**
1. One predicate for "an action Piper took", used by successes and attempts alike: `event_type == CONSEQUENTIAL`, `action` a registered site key, `details.nested_in` absent. Logins, key events, mints and ethics rows stop rendering as changes; that is a change to today's success list too, and the right one.
2. The phrase comes from the registry: a new `ConsequentialSite` field (imperative, CXO's words, optional `{resource}` slot from the row's `resource_id`); the render never prints `message`; pin 16 of 16 beside the instrumented assertion; a render test over every site's row asserts no event type, status word, site key or parenthetical. No shape-based text rewriting.

**The 16 drafts for CXO to edit** (imperative, as they would read after "I tried to …"; `{resource}` is the row's `resource_id`, an issue number for the GitHub rows, which I will confirm per site when I touch the writer):

| site | phrase |
|---|---|
| github.chat.create_issue | create an issue in {resource} |
| github.command.create_issue | create an issue in {resource} |
| github.domain.create_issue | create an issue in {resource} |
| github.standup.create_issue | create an issue from your standup |
| github.chat.close_issue | close issue #{resource} |
| github.chat.reopen_issue | reopen issue #{resource} |
| github.chat.comment_issue | comment on issue #{resource} |
| github.chat.update_issue | update issue #{resource} |
| github.domain.update_issue | update issue #{resource} |
| slack.domain.post_message | post to Slack |
| slack.response.individual | reply in Slack |
| slack.response.consolidated | reply in Slack |
| slack.socket.reply | reply in Slack |
| slack.socket.placeholder | start a reply in Slack |
| slack.socket.slash_reply | answer your Slack command |
| slack.standup.post | post your standup to Slack |

For the create rows `{resource}` is whichever of repository or new issue number the writer records; if it is the issue number the phrase becomes "create issue #{resource}", and I will say which when I read the writer. A row without a `resource_id` renders the phrase with the slot dropped ("close an issue").

Build order unchanged: the next START, after CXO's edits (or with these drafts if CXO says they stand), whole landing gate, Arch validates on main, #2258 stays open for CXO's served judging.

Verified how: read `services/integrations/slack/socket_mode_runner.py` 205–235 and `services/integrations/slack/response_handler.py` 340–360 on main `bbf6f6108f`; a regex pass over the four modules' `log_consequential_action` calls found no `message=` inside any of them (the kwargs ride `_audit_kwargs`); the 16 keys and client methods read from `services/security/consequential_sites.py`. Layer: source.

Lead
