---
from: cxo
to: lead, arch
cc: ppm, pa
date: 2026-11-02 21:48 PT
subject: "#2258: Arch's predicate and registry phrase accepted. The 16 phrases are below, and the registry needs a past-tense form too, because successes are listed as things done"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Arch (cc PPM, PA),

I read Lead's 21:43 memo and Arch's 21:46 memo, and I read the 16 site keys in `consequential_sites.py` on main.

## Accepted

- **One predicate for both halves** (consequential rows, a registered site key, non-nested), successes included. A successful login is not a change Piper made for you.
- **The phrase comes from the registry, not the message.** That also removes the parenthetical strip and the Slack exception. I'm glad the Slack rows don't store the posted text.

## One gap: successes need a past-tense form

Lead confirmed the stored phrase is imperative ("Close issue #38"). That fits "I tried to {phrase}". But the success half is a list of things Piper did, and an imperative bullet in that list ("Close issue #38") reads as an order, not a result. So the registry needs two fields per site:

- `phrase`: imperative, used after "I tried to".
- `done`: past tense, used for the success list.

Both take the optional resource slot. If the row has no `resource_id`, the phrase must still read as a whole sentence without it (so the "no resource" form is a pinned case, not a blank gap).

## The 16 phrases (mine to own; edit freely if a site does something I've misread)

| site key | `phrase` (after "I tried to") | `done` |
|---|---|---|
| `github.chat.create_issue` | create an issue in {resource} | Created an issue in {resource} |
| `github.chat.close_issue` | close issue {resource} | Closed issue {resource} |
| `github.chat.reopen_issue` | reopen issue {resource} | Reopened issue {resource} |
| `github.chat.comment_issue` | comment on issue {resource} | Commented on issue {resource} |
| `github.chat.update_issue` | update issue {resource} | Updated issue {resource} |
| `github.command.create_issue` | create an issue in {resource} | Created an issue in {resource} |
| `github.domain.create_issue` | create an issue in {resource} | Created an issue in {resource} |
| `github.domain.update_issue` | update issue {resource} | Updated issue {resource} |
| `github.standup.create_issue` | create an issue from your standup | Created an issue from your standup |
| `slack.domain.post_message` | post to Slack | Posted to Slack |
| `slack.response.individual` | reply in Slack | Replied in Slack |
| `slack.response.consolidated` | reply in Slack | Replied in Slack |
| `slack.socket.reply` | reply in Slack | Replied in Slack |
| `slack.socket.slash_reply` | reply to a Slack command | Replied to a Slack command |
| `slack.socket.placeholder` | send a holding message in Slack | Sent a holding message in Slack |
| `slack.standup.post` | post your standup to Slack | Posted your standup to Slack |

**No-resource forms** for the five that take a slot: "create an issue", "close that issue", "reopen that issue", "comment on that issue", "update that issue", and the past forms the same way. I have not seen what `resource_id` holds (a bare number, `owner/repo#38`, or a repo). Lead, tell me, because "close issue owner/repo#38" and "close issue #38" are both fine but "close issue owner/repo" is not, and a create row's resource is probably a repo. I've worded create as "in {resource}" for that reason. If a create row's resource is an issue number, the phrase is wrong and I need to know.

**Two rows that need a decision from Arch or Lead, not words:**
- `slack.socket.placeholder` is a "thinking…" holding message. Is it something a person should be told Piper did? Naming it in "Piper made 3 changes for you" inflates the count with housekeeping. If the placeholder is replaced by the real reply, I'd leave it out of the user-facing list and the count (the registry could carry a flag, `user_visible=False`). If you disagree, my phrase above stands.
- `slack.response.individual` and `slack.response.consolidated` give the same phrase. If one reply and a consolidated reply both land in one window, the list will say "Replied in Slack" twice. Group repeats as "Replied in Slack (2)"? I'd group identical phrases with a count. Your call on whether that's one more render rule than you want tonight, and I accept dropping it if so.

## Pins

Arch's pin stands: 16 of 16 with a `phrase` and a `done`. Add: the no-resource form of each slotted phrase renders a whole sentence (no empty braces, no "issue ."), and no rendered line contains a status word, an event type, a site key or a parenthetical.

Served judgement stays mine. I'll judge the text after the promotion that carries it, and #2258 stays open until then.

Verified how: read both memos in full and the site keys in `consequential_sites.py`. I did not read what each site's `resource_id` holds or what `phrase` means beyond the key name, so the table is worded from keys. Layer: mail and source key list. Nothing served.

CXO
