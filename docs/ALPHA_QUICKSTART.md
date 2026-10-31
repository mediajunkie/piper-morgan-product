# Piper Morgan Beta - Quick Start

**Rewritten 2026-08-31 (PPM), per #1708 and PM's in-conversation ruling ("yes I bless the plan").**
This doc previously told testers to build a local copy from an abandoned branch. It doesn't
anymore — see the note below for what changed and why.

**For**: Beta testers who want to try Piper Morgan.
**For engineers who want to run the code locally or contribute**: see `CONTRIBUTING.md` — local
setup now lives there, not here.

> ℹ️ **What changed, and why (2026-08-31)**: this doc used to send testers to clone a `production`
> branch that turned out to be **7,614 commits behind `main`** and not a real deploy source
> (`.github/workflows/docker.yml` builds on `main`), and called the hosted app a "planned for 2026"
> future feature. Neither was true — ESSENCE v1.0 (ratified) names the live web-chat app as the
> current surface, and it's what the existing alpha testers are actually on. **The fix is the
> surface change below, not a corrected clone command**: testers use the hosted app; local install
> is now an engineer path in `CONTRIBUTING.md`, pointing at `main`, never `production`. Full record:
> #1708.

⚠️ **If you hit issues, see `ALPHA_TESTING_GUIDE.md` for comprehensive troubleshooting.**

---

## Getting Started

Piper Morgan runs as a hosted app — there's nothing to install. Go to
**[beta.pipermorgan.ai](https://beta.pipermorgan.ai)** and log in.

*(URL updated 2026-10-31 to the beta host, matching your invite email.)*

New tester? The beta is invite-only. Codes come directly from xian, by email. With
your invite code in hand: go to
**[beta.pipermorgan.ai](https://beta.pipermorgan.ai)**, choose "Create your account"
(the form asks for the invite code), log in, then add your own LLM key under
**Settings → LLM API Keys** (an Anthropic key — Piper runs on *your* key and can't
answer substantive requests without one).

That's it — no clone, no Docker, no Python version to check. **Time to first use: however
long it takes to log in and paste a key.**

---

## What's New in 0.9.0

The first private beta release, cut 2026-10-31 after v0.8.14.0 (2026-09-23). The MVP milestone
closed with it. Theme: **trust in what Piper tells you**. Most of the 361 issues closed since
0.8.14 were cases where Piper said something that was not true, or did not say something that
was. Each now has a fix, and many have a regression test pinned to the exact wording that failed.

**Setup works for an invited tester** (#2078, #1875, #2089, #2176) — the wizard no longer ends in
"Setup Failed", Step 1 no longer blocks new users, and the hosted app no longer shows the local
System Requirements check. Current Anthropic keys are no longer refused (#1978).

**Integrations say what is true** (#2012, #2029, #2045, #2071, #2148) — the Integrations Test no
longer reports success on a revoked GitHub grant, the card updates after a successful Test, the
result is per account, and Calendar connect no longer says "Connected" when you left Google's
consent screen. Chat now reads a Google Calendar that Settings reports as healthy (#2092).

**Piper tells you when it could not read something** (#2182, #1965, #2072, #2076) — a failed
calendar or GitHub read is no longer shown as a free day or "no activity". Replies no longer say
"Your todo list is clear" while overdue or pending todos exist (#1985, #1990).

**Todos, reminders, projects and GitHub issues in chat** — "Add three todos for the launch: ..."
works (#2094), "delete that reminder" targets the reminder you just saved (#1987), a project's
Remove button does what it says (#1912), and a new user's first "Create an issue" no longer goes
to an auto-picked repository with issues disabled (#2205). Closing a nonexistent issue says so
and changes nothing (#1941).

**Feedback and your data** — Send feedback is reachable from inside the app (#2096, #2156), you
can hide or delete a chat (#2065), and the privacy page's 14-day deletion promise now has an
erasure path behind it (#2064).

Also new: a hosted MCP server at mcp.pipermorgan.ai (private-beta work, rougher than the web
app) and an Admin Invites page for minting and revoking invite codes (#2081).

See [Release Notes v0.9.0.0](releases/RELEASE-NOTES-v0.9.0.0.md) for full details.

---

## Want to run it locally instead?

Local install is now an **engineer/contributor path**, not a tester one — see `CONTRIBUTING.md`
for the full setup (Python, Docker, Postgres, the setup wizard). Point at `main`, never
`production` (that branch isn't a deploy source and drifts stale — see `release-model.md`).

---

## First Commands to Try

### Via Chat Interface
```bash
# In Piper's chat interface:
"Hello, what can you help me with?"
"Add a todo: Test Piper Morgan"
"What tasks do I have?"
"Upload a document and summarize it"
```

### Via UI Features

After logging in at [beta.pipermorgan.ai](https://beta.pipermorgan.ai):

1. **Lists Management** → Click "Lists" → "Create New List"
   - Add list name and description
   - Try sharing with another user (if multi-user testing)

2. **Todos Management** → Click "Todos" → "Create New Todo"
   - Full CRUD operations

3. **File Upload/Download** → Click "Files" → Upload a file
   - Supports: PDF, DOCX, TXT, MD, JSON (max 10MB)
   - Download and delete files

4. **Daily Standup** → Click "Standup" → "Generate Standup"
   - AI-powered standup generation (2-3 seconds)

5. **Logout** → Click user menu (top right) → "Logout"
   - Token revocation and logout working

6. **Permission Management** → Try conversational commands:
   - "share my project plan with alex@example.com as editor"
   - "who can access my shopping list?"

---

## Testing Focus for 0.9.0

**What's Stable** (light testing recommended):
- ✅ Login/authentication; invite-gated account creation
- ✅ Lists, Todos, Projects management
- ✅ Files upload/download/preview/tagging
- ✅ Per-user API keys, encrypted at rest
- ✅ The standup interview and free-form draft edits (carried from 0.8.13 and 0.8.14)

**Where to Focus Testing** (these need your attention):
- 🔍 **Setup**: as a new invited tester, does the wizard finish without "Setup Failed" and keep
  your key? Does a conversation you start before adding a key stay in your sidebar?
- 🔍 **Integrations**: run Test on GitHub and Google Calendar. Does the card update its status
  and "last checked" line? Does a revoked grant show as broken, not Connected?
- 🔍 **Failed reads**: if GitHub or your calendar cannot be read, does Piper say so instead of
  showing a free day or "no activity"?
- 🔍 **Todos and reminders**: "add three todos for the launch: a, b, c", "delete that reminder"
  right after saving one, and a "show my todos" reply when some are overdue.
- 🔍 **GitHub issues in chat**: your first "Create an issue", "show me that issue" right after
  creating one, and closing an issue number that does not exist.
- 🔍 **Your data**: hide or delete a chat, and use Send feedback from inside the app.

Send the exact wording of anything that looks wrong. Each report becomes a test row.

## What's Working in 0.9.0

✅ **Setup and sign-in**:
   - Invited accounts are created and keys stored through the setup wizard (#2078)
   - Invite-gated account creation, with invite codes minted and revoked from an Admin Invites page (#2081)

✅ **Integrations (GitHub and Google Calendar)**:
   - Test results are per account and update the card (#2071, #2045)
   - Disconnect works, and a dead GitHub connection can recover from Settings (#2017, #2018)
   - Chat reads events from a healthy Google Calendar, and "agenda Thursday" honors the weekday (#2092, #2091)
   - GitHub reads in chat use your own account's grant (#2123)
   - Other connectors are not offered in this beta

✅ **Conversational AI**:
   - Replies say when a source could not be read, instead of reporting an empty day (#2182, #2076)
   - "What changed since yesterday?" explains the window it read (#2140, #2143)
   - Guided standup interview, with suggestion chips and a greeting that matches the hour (#2027, #2079)

✅ **Todos, Lists & Projects**:
   - Create, delete and manage todos, reminders and projects in chat and in the UI
   - The Lists page shows the right item count (#2171)

✅ **GitHub issues in chat**:
   - Create, show, comment and close, with failures reported as failures (#2152, #1941)

✅ **Your data**:
   - Hide or delete a chat, Send feedback from anywhere in the app, and a deletion path behind the privacy page (#2065, #2096, #2064)
   - Uploaded-file writes no longer fall back to plaintext when the encryption key is missing (#2061)

✅ **Files**:
   - Upload, download, and in-browser preview, search, filter and tags

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for current limitations.

---

## Getting Help

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — deeper testing
  walkthrough (rewritten 2026-09-21 for the hosted flow; the two docs now agree).
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Terms**: [pipermorgan.ai/terms](https://pipermorgan.ai/terms/) (plain-language terms)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.9.0.0 means)

---

## Remember

This is **private beta software** (0.9.0.0). Expect bugs. Don't use for production. You're responsible for API costs. See the Terms at https://pipermorgan.ai/terms/ for details.

**Testing Focus**: Does setup finish for you? Does every integration status match what is really happening? When Piper cannot read something, does it say so?

---

**Happy testing!** 🚀

_Last Updated: October 31, 2026_
