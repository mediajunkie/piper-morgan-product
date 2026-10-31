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

### Connectors

- **Only GitHub and Google Calendar are offered in this beta.** Other connectors are not offered.
- **The MCP connector is private-beta work** (Piper inside Claude and other MCP clients). It is not on the MVP path, so expect it to be rougher than the web app.

### Chat and data

- **Issue counts and "most recent"** ([#2185](https://github.com/mediajunkie/piper-morgan-product/issues/2185)) — "You have 261 open issues" can count issues assigned to you across all repositories, archived ones included, and "most recent" is not sorted.
- **Milestone questions** ([#2184](https://github.com/mediajunkie/piper-morgan-product/issues/2184)) — a question about a milestone's issues can be answered with the wrong issues, because no read lists a milestone's issues yet.
- **"Delete todo 1 and 2"** ([#2025](https://github.com/mediajunkie/piper-morgan-product/issues/2025)) removes only the first, and the second is dropped without a message. Delete them one at a time.
- **Struck-through overdue todo** ([#1961](https://github.com/mediajunkie/piper-morgan-product/issues/1961)) — a "show my todos" reply can strike through an open overdue todo, which makes it look done.
- **Sharing fails** ([#2166](https://github.com/mediajunkie/piper-morgan-product/issues/2166)) — sharing a todo, list or project from the UI fails with an error.
- **Multi-part messages** ([#2041](https://github.com/mediajunkie/piper-morgan-product/issues/2041), [#2030](https://github.com/mediajunkie/piper-morgan-product/issues/2030)) — a write offer or a question from one part can be lost or shown as plain text. Send the parts as separate messages.
- **Learned-pattern execute route** ([#2208](https://github.com/mediajunkie/piper-morgan-product/issues/2208)) can report a failed action as a success.
- **Preferences on a cached reply** ([#2056](https://github.com/mediajunkie/piper-morgan-product/issues/2056)) are not always applied.

### Interface

- **Switching between chats flashes** ([#1515](https://github.com/mediajunkie/piper-morgan-product/issues/1515)) — the whole screen redraws. Nothing is lost.
- **iPad Safari in portrait** ([#1907](https://github.com/mediajunkie/piper-morgan-product/issues/1907)) — a new chat can show an empty gray panel with the composer pushed off screen.
- **No reachable control to delete or archive a conversation** in the current navigation ([#1516](https://github.com/mediajunkie/piper-morgan-product/issues/1516)).
- **"Start private session"** in the History slide-out ([#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164)) is a display toggle with no backend behavior. Do not rely on it.

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

- **Private**: email alpha@pipermorgan.ai. It goes to the team and stays there unless you ask us to share it.
- **Public**: a [GitHub issue](https://github.com/mediajunkie/piper-morgan-product/issues/new). A GitHub issue is public, so leave out anything you would not post on a public page.

---

## See Also

- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — Quick setup
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — What to test and how
- [Release Notes v0.9.0.0](releases/RELEASE-NOTES-v0.9.0.0.md) — Full 0.9.0.0 changelog

---

_Last Updated: October 31, 2026_
