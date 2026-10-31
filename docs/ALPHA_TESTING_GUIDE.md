# Piper Morgan Alpha Testing Guide

**Version**: 0.9.0.0
**Last Updated**: October 31, 2026
**For**: Private Beta Testers

**Rewritten 2026-09-21 (Lead), closing #1804.** This guide previously walked testers
through a local clone/Docker/setup-wizard install — a flow retired by #1708 (2026-08-31):
Piper Morgan's alpha is a **hosted app** at
[alpha.pipermorgan.ai](https://alpha.pipermorgan.ai), and that's what this guide now
describes. Engineers who want to run the code locally: see `CONTRIBUTING.md` — local
setup lives there, not here.

---

## Returning Tester? Start Here

If you already have an account, skip straight to what matters:
- **[What's New in 0.9.0](#whats-new-in-090)** — setup works for an invited tester, Integrations and chat replies say what is true, and Piper tells you when it could not read something
- **[What to Test in 0.9.0](#what-to-test-in-090)** — priority test walks for this release
- **[Troubleshooting](#chapter-3-troubleshooting)** — if something isn't working

---

## Quick Navigation

| Section | Description | Start Here If... |
|---------|-------------|------------------|
| **[Chapter 1: Setup](#chapter-1-setup)** | Account creation, your LLM key, optional connections | You're setting up for the first time |
| **[Chapter 2: Testing](#chapter-2-testing)** | Test scenarios, features to explore | You have an account and want to start testing |
| **[Chapter 3: Troubleshooting](#chapter-3-troubleshooting)** | Common issues and solutions | Something isn't working |

---

# Chapter 1: Setup

Piper Morgan runs as a hosted app — **there is nothing to install**. Setup is three steps:
an account, your LLM key, and (optionally) your tool connections.

## What you need

- [ ] A modern browser
- [ ] **Your invite code** — the private beta is invite-only; codes come directly from
      **xian@pipermorgan.ai**. If you don't have one, that's the address to write.
- [ ] **At least one LLM API key of your own**:
  - An [Anthropic API key](https://console.anthropic.com/) (Claude), and/or
  - An [OpenAI API key](https://platform.openai.com/api-keys) (GPT-4-class models)
- [ ] Budget roughly $5–20 for LLM API costs over the beta period — **Piper runs on
      your key and your account**; it never bills anyone else's (see What's New).

**Optional (for the integration features):**

- [ ] A GitHub personal access token (issue creation/management features)
- [ ] A Notion API key (document features)
- [ ] A Slack workspace you can connect (notifications, chat-with-Piper-from-Slack)

**Time commitment**: ~10 minutes to first conversation; 15–30 minutes weekly for
feedback during the beta period.

## Step 1 — Create your account

1. Go to **[alpha.pipermorgan.ai/setup](https://alpha.pipermorgan.ai/setup)**
2. Choose a username and password, and enter your email
3. Enter your **invite code** — account creation is invite-gated; the form won't
   proceed without a valid, unused code
4. Log in at [alpha.pipermorgan.ai](https://alpha.pipermorgan.ai)

## Step 2 — Add your LLM key (the one required step)

Piper can't answer anything substantive until it has a key of yours to run on:

1. Open **Settings → LLM Keys**
2. Paste your Anthropic and/or OpenAI key and save
3. If you add both, you can pick a default provider; either alone works

Until you do this, Piper will tell you so honestly — a keyless "hi" gets a greeting and
a pointer to Settings, and a keyless request gets a refusal that names exactly what's
missing. That's by design (see What's New): **no key, no spend, no borrowing**.

## Step 3 (optional) — Connect your tools

In **Settings → Integrations**: GitHub (personal access token), Notion (API key),
Slack (OAuth). Each is optional; core chat, lists, files, and standups work without any.

## Important Disclaimers — Please Read

**⚠️ PRIVATE BETA SOFTWARE WARNING ⚠️**

This is private beta software (version 0.9.0.0). By proceeding, you acknowledge:

1. **Expected Issues**: bugs, rough edges, and incomplete features are normal
2. **Data Loss Risk**: your data on the alpha instance may be lost at any time
3. **No Production Use**: do NOT use it for mission-critical or time-sensitive work
4. **API Charges**: you are responsible for all LLM API costs your key incurs
5. **Security**: not security audited — use test data only, no sensitive information
6. **No Warranty**: provided "as-is", without any warranty whatsoever
7. **No Support SLA**: best-effort support only, no guaranteed response times

See `ALPHA_AGREEMENT_v2.md` for complete terms.

---

## What's New in 0.9.0

v0.9.0.0 is the first private beta release and the one that closes the MVP milestone. It was
cut on 2026-10-31, after v0.8.14.0 (2026-09-23). Theme: **trust in what Piper tells you**. Most
of the 361 issues closed since 0.8.14 are cases where Piper said something that was not true or
did not say something that was. Each now has a fix, and many have a regression test pinned to
the exact wording that failed.

**Setup works for an invited tester** ([#2078](https://github.com/mediajunkie/piper-morgan-product/issues/2078), [#1875](https://github.com/mediajunkie/piper-morgan-product/issues/1875), [#2089](https://github.com/mediajunkie/piper-morgan-product/issues/2089), [#2176](https://github.com/mediajunkie/piper-morgan-product/issues/2176)):

- The wizard no longer ends in "Setup Failed" for an invited account. The account is created
  and your keys are stored.
- Step 1 no longer blocks every new user, and the hosted app no longer shows the local System
  Requirements check for Docker, Postgres, Redis and Temporal.
- The wizard no longer shows Slack and Google Calendar app-credential forms to a new tester.
- A server-side encryption problem is no longer reported as a "Validation error" on your API
  key ([#2125](https://github.com/mediajunkie/piper-morgan-product/issues/2125)), and current Anthropic keys are no longer refused ([#1978](https://github.com/mediajunkie/piper-morgan-product/issues/1978)).
- A conversation you start before adding a key stays in your sidebar ([#1913](https://github.com/mediajunkie/piper-morgan-product/issues/1913), [#1838](https://github.com/mediajunkie/piper-morgan-product/issues/1838)).

**Integrations say what is true** ([#2012](https://github.com/mediajunkie/piper-morgan-product/issues/2012), [#2029](https://github.com/mediajunkie/piper-morgan-product/issues/2029), [#2045](https://github.com/mediajunkie/piper-morgan-product/issues/2045), [#2071](https://github.com/mediajunkie/piper-morgan-product/issues/2071), [#2148](https://github.com/mediajunkie/piper-morgan-product/issues/2148)):

- The Integrations Test for GitHub no longer reports "connection successful" on a revoked
  grant, and the GitHub settings page no longer shows Connected for one.
- After a successful Test, the card updates its status, its "last checked" line and the
  "healthy" count. The Test result is per account.
- An expired sign-in is no longer shown as an integration failure, and the page headline no
  longer says "All Systems Healthy" for an OAuth connection that has never been tested.
- A GitHub account with a dead connection can recover from Settings, and Disconnect works.
- Calendar connect no longer says "Calendar Connected" when you left Google's consent screen
  without finishing.
- Chat reads events from a Google Calendar that Settings reports as healthy, and GitHub reads
  in chat use your own account's grant.

**Piper tells you when it could not read something** ([#2182](https://github.com/mediajunkie/piper-morgan-product/issues/2182), [#1965](https://github.com/mediajunkie/piper-morgan-product/issues/1965), [#2072](https://github.com/mediajunkie/piper-morgan-product/issues/2072), [#2076](https://github.com/mediajunkie/piper-morgan-product/issues/2076)):

- A standup or radar view no longer shows a failed calendar or GitHub read as a free day or
  "no activity".
- Replies no longer say "Your todo list is clear" or "nothing urgent" while overdue or pending
  todos exist.
- "What changed since yesterday?" and "What changed in the past hour?" explain the window they read.

**Todos, reminders, projects and GitHub issues in chat**:

- "Add three todos for the launch: draft brief, book venue, send invites" works ([#2094](https://github.com/mediajunkie/piper-morgan-product/issues/2094)).
- "Delete that reminder" right after a reminder is saved targets that reminder ([#1987](https://github.com/mediajunkie/piper-morgan-product/issues/1987)).
- A project's Remove button and "delete my project" do what they say ([#1912](https://github.com/mediajunkie/piper-morgan-product/issues/1912), [#1930](https://github.com/mediajunkie/piper-morgan-product/issues/1930)).
- A new user's first "Create an issue" no longer goes to an auto-picked oldest repository with
  issues disabled ([#2205](https://github.com/mediajunkie/piper-morgan-product/issues/2205)), and "Show me that issue" right after creating one shows it ([#2115](https://github.com/mediajunkie/piper-morgan-product/issues/2115)).
- A comment on an issue no longer reports success when the post failed ([#2152](https://github.com/mediajunkie/piper-morgan-product/issues/2152)), and closing a
  nonexistent issue says so and changes nothing ([#1941](https://github.com/mediajunkie/piper-morgan-product/issues/1941)).

**Feedback, privacy and your data**:

- Send feedback is reachable from inside the app, including the setup wizard and error pages ([#2096](https://github.com/mediajunkie/piper-morgan-product/issues/2096), [#2156](https://github.com/mediajunkie/piper-morgan-product/issues/2156)).
- You can hide or delete a chat ([#2065](https://github.com/mediajunkie/piper-morgan-product/issues/2065)), and the privacy page's 14-day deletion promise has an
  erasure path behind it ([#2064](https://github.com/mediajunkie/piper-morgan-product/issues/2064)).
- The API key Remove dialog states that backups keep a copy for a limited time ([#2167](https://github.com/mediajunkie/piper-morgan-product/issues/2167)).

**In this beta**: the connectors offered are GitHub and Google Calendar only. A hosted MCP server
at mcp.pipermorgan.ai ships too, as private-beta work that is rougher than the web app.

See [Release Notes v0.9.0.0](releases/RELEASE-NOTES-v0.9.0.0.md) for full details, and
[releases/README.md](releases/README.md) for prior release history.

---

# Chapter 2: Testing

This chapter covers what to test and how. If you're already set up, **start here**.

## What to Test in 0.9.0

Trust is the focus. **Does setup finish for you? Does every status you see match what is
really happening? When Piper cannot read something, does it say so?** Send the exact wording
of anything that looks wrong. Each report becomes a test row.

The six walks below are suggested scenarios built from this release's fixes. They have **not yet been walked** by the team, so treat a surprise as a finding, not as your mistake.

### Test Walk 1: Setup as an invited tester ([#2078](https://github.com/mediajunkie/piper-morgan-product/issues/2078), [#1875](https://github.com/mediajunkie/piper-morgan-product/issues/1875))

1. Create your account at `/setup` with your invite code and run the setup wizard
2. Check: the wizard finishes without "Setup Failed", and your key is stored
3. Check: you do not see the local System Requirements check or Slack and Google Calendar
   app-credential forms
4. Start a conversation before adding a key, then add one. Check the conversation is still in
   your sidebar

### Test Walk 2: Integrations say what is true ([#2012](https://github.com/mediajunkie/piper-morgan-product/issues/2012), [#2045](https://github.com/mediajunkie/piper-morgan-product/issues/2045), [#2148](https://github.com/mediajunkie/piper-morgan-product/issues/2148))

1. Under Settings → Integrations, connect GitHub and Google Calendar and run Test on each
2. Check: the card updates its status and "last checked" line, and the "healthy" count follows
3. If you can, revoke the GitHub grant on GitHub and run Test again. Check it reports the
   connection as broken, not successful
4. Start the Google Calendar connect and leave Google's consent screen without finishing.
   Check Piper does not say "Calendar Connected"
5. Ask "what's my agenda Thursday?" and check it honors the weekday

### Test Walk 3: Failed reads are reported ([#2182](https://github.com/mediajunkie/piper-morgan-product/issues/2182), [#2076](https://github.com/mediajunkie/piper-morgan-product/issues/2076), [#2173](https://github.com/mediajunkie/piper-morgan-product/issues/2173))

1. Ask for a standup or "what's on my radar" while GitHub or your calendar cannot be read
   (for example with a revoked grant)
2. Check: Piper says it could not read the source, rather than showing a free day or
   "no activity"
3. With no GitHub username set, check the reply does not list every open issue as your own work
4. Ask "what changed since yesterday?" and check the reply explains the window it read

### Test Walk 4: Todos and reminders ([#2094](https://github.com/mediajunkie/piper-morgan-product/issues/2094), [#1987](https://github.com/mediajunkie/piper-morgan-product/issues/1987), [#1985](https://github.com/mediajunkie/piper-morgan-product/issues/1985))

1. Say "Add three todos for the launch: draft brief, book venue, send invites"
2. Save a reminder, then say "delete that reminder". Check it removes the one you just saved
3. With some overdue todos, ask for your todos. Check Piper never says the list is clear
4. ⚠️ Known: "Delete todo 1 and 2" removes only the first ([#2025](https://github.com/mediajunkie/piper-morgan-product/issues/2025)). Report anything beyond what the Known Issues page lists

### Test Walk 5: GitHub issues in chat ([#2205](https://github.com/mediajunkie/piper-morgan-product/issues/2205), [#2115](https://github.com/mediajunkie/piper-morgan-product/issues/2115), [#1941](https://github.com/mediajunkie/piper-morgan-product/issues/1941))

1. As a first action, say "Create an issue" and check Piper asks about the repository rather
   than choosing one for you
2. Right after creating one, say "Show me that issue" and check it shows the issue
3. Say "close issue 99999 in <owner>/<repo>" (a number that does not exist). Check Piper says
   there is no such issue and nothing was changed

### Test Walk 6: Your data ([#2065](https://github.com/mediajunkie/piper-morgan-product/issues/2065), [#2096](https://github.com/mediajunkie/piper-morgan-product/issues/2096))

1. Hide or delete a chat and check it leaves your sidebar
2. Use Send feedback from inside the app, including from the setup wizard or an error page
3. Check Settings does not promise Export or delete actions the page lacks

### Basic Functionality Tests

1. **Basic Chat**: "Hello, what can you help me with?"
2. **Task Creation**: "Add a todo: Review Q3 metrics"
3. **Information Query**: "What tasks do I have?"
4. **File Upload**: upload a PDF or DOCX (max 10MB) and ask for analysis
5. **Document Summary**: "Summarize the document I just uploaded"
6. **Multi-User Privacy**: if testing alongside someone else, verify you can't see each
   other's data

---

## Exploring Piper's Features

All URLs below are on the hosted app — e.g. `https://alpha.pipermorgan.ai/lists`.

### Lists, Todos, and Projects

1. **Create a List**: go to `/lists` → "Create New List" → name it "Alpha Testing
   Tasks" → verify it appears
2. **Edit and Delete**: open your list, edit the name, then try deleting one (should
   confirm first)
3. **Repeat for Todos and Projects** (`/todos`, `/projects`) — the three resource types
   should behave consistently

### File Management

1. **Upload**: `/files` → upload or drag-and-drop (PDF, DOCX, TXT, MD, JSON; max 10MB)
2. **Download** and **Delete**: both from the file's row
3. **Privacy**: files are private to you — another tester should never see them

### Interactive Standup Assistant

Worth trying alongside the walks above (suggestion chips such as "nothing" and "skip" now
appear, [#2027](https://github.com/mediajunkie/piper-morgan-product/issues/2027)):

- Abandon a standup mid-conversation ("not now") and confirm your next message routes
  normally
- Ask "are we done with that standup?" mid-flow — you should get an honest status
  answer, not a surprise finalization

### Authentication

1. **Logout**: user menu (top right) → Logout → verify redirect to login
2. **Login again**: your data (lists, files) should all still be there

### Sharing & Permissions (advanced — needs two accounts)

1. Share a list: open it → "Share" → another tester's email → role "Viewer" or "Editor"
2. Verify the viewer can see but not edit; the editor can edit
3. Conversational forms work too: "share my Alpha Testing Tasks list with [email] as
   editor", "who can access my Alpha Testing Tasks?"

---

# Chapter 3: Troubleshooting

### Login & account issues

**Invite code rejected?** Codes are single-use and exact — check for copy/paste
whitespace. If it still fails, yours may already have been consumed; email
**xian@pipermorgan.ai** for a fresh one.

**Forgot your password?** Email **xian@pipermorgan.ai** — there's no self-serve reset
in the alpha yet.

**Can't reach the site?** Check `https://alpha.pipermorgan.ai/health` — if it doesn't
return a healthy JSON response, the instance is down; please report it.

### Key & chat issues

**"Piper runs on an LLM key of your own…" on every message?** You haven't added a key
yet (or it didn't save) — Settings → LLM Keys. This message is working as intended for
keyless accounts.

**Honest key error after adding a key?** Verify the key works in your provider's own
console; regenerate it if in doubt. Anthropic keys start `sk-ant-`, OpenAI keys `sk-`.

**"Something unexpected happened"?** That generic message on a key-shaped problem is
itself a bug we're hunting ([#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824)) —
please report the exact message and what you did.

**High API costs?** Piper uses GPT-4-class/Claude models. Watch your provider dashboard;
concise-preference settings reduce token use.

### Feature issues

**Standup seems stuck?** Say "start over" (genuinely restarts now) or "not now" (lets
go of the conversation). If a standup ever shows content you didn't say, that's a
serious bug — please report the transcript.

**File upload fails?** Formats: PDF, DOCX, TXT, MD, JSON; max 10MB; you must be logged
in.

**Sharing fails?** The other account must already exist, and you must own the resource.

---

## Providing Feedback

We need your feedback to improve! Please report:

### What to Report

- Bugs and crashes (with the exact error message)
- Anything Piper said that turned out to be untrue — false claims are our top-priority
  bug class, even when they're polite
- Confusing flows, missing features you expected, performance problems
- Successful workflows that delighted you (genuinely useful signal)

### How to Report

1. **Private**: email alpha@pipermorgan.ai. It goes to the alpha team and stays there unless you ask us to share it.
2. **Public**: a [GitHub issue](https://github.com/mediajunkie/piper-morgan-product/issues/new), for anything you are happy to have public. A GitHub issue is public, so leave out anything you would not post on a public page.
3. **Weekly check-in**: optional 15-minute calls available

### Helpful Feedback Format

```
WHAT I TRIED: [specific action, ideally the exact message you sent]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result / exact reply text]
ERROR MESSAGE: [if any]
SEVERITY: [blocker/major/minor]
```

---

## Privacy & Data Collection

- Your LLM API keys are stored encrypted (AES-256-GCM field encryption) on the alpha
  instance and used only to make your own requests; they are never shown back or shared
- Your files, lists, todos, and projects are private by default; sharing requires an
  explicit grant from you
- Error logs may be reviewed by the team to fix bugs
- This is a small, curated alpha — the operators can technically access the instance's
  database; don't put anything sensitive in it (see the disclaimers above)
- **Note**: not everything is encrypted field by field. Your chat messages, conversation context, uploaded artifact content and API keys are. Todos, projects, profile and preference data are stored as ordinary database columns

---

## Questions?

This is private beta software (version 0.9.0.0) — expect rough edges, and thank you for being
an early adopter. 🚀

---

## See Also

- `ALPHA_QUICKSTART.md` — the 2-minute version of Chapter 1
- `ALPHA_KNOWN_ISSUES.md` — current bugs and limitations
- `ALPHA_AGREEMENT_v2.md` — terms and conditions
- `VERSION_NUMBERING.md` — what 0.9.0.0 means
- `CONTRIBUTING.md` — running the code locally (engineers)

---

_Last updated: October 31, 2026_
_Software version: 0.9.0.0_
