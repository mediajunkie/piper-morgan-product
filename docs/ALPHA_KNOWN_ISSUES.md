# Private Beta Known Issues (v0.9.0.0)

**Version**: 0.9.0.0
**Last Updated**: October 31, 2026

This document helps testers avoid wasting time on things we already know about.

v0.9.0.0 is the first private beta release. It closes the MVP milestone and is about trust in what
Piper tells you: setup works for an invited tester, Integrations and chat replies say what is
true, and a failed read is reported as a failed read. What's below are the rough edges that remain.
For anything not listed, use Send feedback in the app. Each report with the exact wording becomes
a test row.

## Known Issues in 0.9.0

The limits Piper itself can describe to you, in plain words, are in [known-limits.md](known-limits.md): counting issues, milestone questions, overdue todos, sharing, several requests in one message, and the iPad portrait layout. Those rows moved there and are not repeated below. What stays here is for testers: items still being re-checked, and interface notes that do not change what Piper says.

### Connectors

- **Only GitHub and Google Calendar are offered in this beta.** Other connectors are not offered.
- **The MCP connector is private-beta work** (Piper inside Claude and other MCP clients). It is not on the MVP path, so expect it to be rougher than the web app.

### Chat and data

- **"Delete todo 1 and 2"** ([#2025](https://github.com/mediajunkie/piper-morgan-product/issues/2025)) removes only the first, and the second is dropped without a message. Delete them one at a time.
- **Learned-pattern execute route** ([#2208](https://github.com/mediajunkie/piper-morgan-product/issues/2208)) can report a failed action as a success.
- **Preferences on a cached reply** ([#2056](https://github.com/mediajunkie/piper-morgan-product/issues/2056)) are not always applied.

### Interface

- **Switching between chats flashes** ([#1515](https://github.com/mediajunkie/piper-morgan-product/issues/1515)) — the whole screen redraws. Nothing is lost.
- **No reachable control to delete or archive a conversation** in the current navigation ([#1516](https://github.com/mediajunkie/piper-morgan-product/issues/1516)).
- **"Start private session"** in the History slide-out ([#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164)) is hidden in this beta, because it is a display toggle with no backend behavior. If you ever see it, do not rely on it.

### Not for beta use

- **Slack.** The Slack settings page and the Slack socket-mode path are not beta features. The socket-mode path binds every sender to the connector owner ([#1497](https://github.com/mediajunkie/piper-morgan-product/issues/1497), [#1481](https://github.com/mediajunkie/piper-morgan-product/issues/1481)).

---

## Fixed in 0.9.0

If any of these still happens to you, that's a regression. Please report it:

- Setup ending in "Setup Failed" for an invited account ([#2078](https://github.com/mediajunkie/piper-morgan-product/issues/2078)), and Step 1 blocking every new user ([#1875](https://github.com/mediajunkie/piper-morgan-product/issues/1875)).
- The Integrations Test reporting success on a revoked GitHub grant, and the card keeping "Not checked yet" after a successful Test ([#2012](https://github.com/mediajunkie/piper-morgan-product/issues/2012), [#2045](https://github.com/mediajunkie/piper-morgan-product/issues/2045)).
- A failed calendar or GitHub read shown as a free day or "no activity" ([#2182](https://github.com/mediajunkie/piper-morgan-product/issues/2182), [#1965](https://github.com/mediajunkie/piper-morgan-product/issues/1965)).
- Replies saying "Your todo list is clear" while overdue or pending todos exist ([#1985](https://github.com/mediajunkie/piper-morgan-product/issues/1985)).
- A conversation started before adding a key vanishing from the sidebar ([#1913](https://github.com/mediajunkie/piper-morgan-product/issues/1913), [#1838](https://github.com/mediajunkie/piper-morgan-product/issues/1838)).
- A comment on a GitHub issue reporting success when the post failed ([#2152](https://github.com/mediajunkie/piper-morgan-product/issues/2152)).
- Delete and Disconnect reporting success when nothing changed ([#2172](https://github.com/mediajunkie/piper-morgan-product/issues/2172), [#1941](https://github.com/mediajunkie/piper-morgan-product/issues/1941)).

The full list is in [Release Notes v0.9.0.0](releases/RELEASE-NOTES-v0.9.0.0.md).

---

## Needs Testing

These shipped in 0.9.0 and need real-world validation:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Setup as an invited tester** | Wizard finishes, key stored, no "Setup Failed"? | `/setup` with your invite code |
| **Integrations Test** | Card updates status and "last checked"? Revoked grant shows as broken? | Settings → Integrations |
| **Failed reads** | Piper says it could not read GitHub or the calendar, never an empty day? | Chat: standup, radar, agenda |
| **Todos and reminders** | Multi-todo add, "delete that reminder" right after saving one | Chat |
| **GitHub issues in chat** | First "Create an issue", "show me that issue", closing a nonexistent issue | Chat with GitHub connected |
| **Your data** | Hide or delete a chat, Send feedback from inside the app | Chat, History |

---

## How to Report Issues

**What to include:**
```
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
```

- **Private**: email support@pipermorgan.ai. The team reads it, including xian, and it stays with us unless you ask us to share it.
- **Public**: a [GitHub issue](https://github.com/mediajunkie/piper-morgan-product/issues/new). A GitHub issue is public, so leave out anything you would not post on a public page.

---

## See Also

- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — Quick setup
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — What to test and how
- [Release Notes v0.9.0.0](releases/RELEASE-NOTES-v0.9.0.0.md) — Full 0.9.0.0 changelog

---

_Last Updated: October 31, 2026_
