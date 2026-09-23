# Piper Morgan Alpha - Quick Start

**Rewritten 2026-08-31 (PPM), per #1708 and PM's in-conversation ruling ("yes I bless the plan").**
This doc previously told testers to build a local copy from an abandoned branch. It doesn't
anymore — see the note below for what changed and why.

**For**: Alpha testers who want to try Piper Morgan.
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
**[alpha.pipermorgan.ai](https://alpha.pipermorgan.ai)** and log in.

*(URL updated 2026-09-21: this doc previously pointed at a `fly.dev` address; the alpha
testers' instance — the one invites are issued for — is `alpha.pipermorgan.ai`, matching
`docs/README.md` and your invite email.)*

New tester? Alpha is invite-only — codes come directly from **xian@pipermorgan.ai**. With
your invite code in hand: go to
**[alpha.pipermorgan.ai/setup](https://alpha.pipermorgan.ai/setup)**, create your account
(the form asks for the invite code), log in, then add your own LLM key under
**Settings → LLM Keys** (an Anthropic or OpenAI key — Piper runs on *your* key and can't
answer substantive requests without one).

That's it — no clone, no Docker, no Python version to check. **Time to first use: however
long it takes to log in and paste a key.**

---

## What's New in 0.8.14

A fast follow to v0.8.13.0 — cut two days later, and the first release deployed to the
consolidated host (alpha.pipermorgan.ai has been served by Fly since 2026-09-22; you were
asked to log in again once — that was the move). Theme: **on your clock**.

**Your preferences survive restarts** (#1574) — timezone, reminder settings, working mode,
and the calendar-setup offer used to reset silently on every deploy ("why does it keep
asking me?"). They now persist per user.

**Every clock face is yours, and labeled** (#1576, #1575, #1577, #1556) — standup exports,
the agenda, and "what's my day look like" answers render in *your* timezone with the zone
named ("3:00 PM PDT"). "Today" and "yesterday" are your calendar days, and free-time blocks
are computed on your clock — after 5pm Pacific you no longer get tomorrow's day.

**The agenda shows real meeting times** (#1576) — it had been printing "TBD" for everyone
with a connected calendar (a key mismatch, not a missing meeting). Fixed, along with the
unreachable "Focus Time Available" section.

**Add a project in one line** (#1856) — `add project One Job with repo
Design-in-Product/one-job` creates and links it in one turn. Leave the name out and Piper
tells you the exact line to type.

**Honest outcomes on GitHub writes** (#1858) — closing an issue that doesn't exist now says
"There's no issue #99999 in owner/repo — nothing was changed" instead of "it may or may not
have gone through".

**The preferences pages work again** (#1864) — every `/api/v1/preferences/*` route had
errored since its auth dependency landed. Also: one "Add to Slack" path instead of four
(#1499), and the four honest LLM-key error sentences from 0.8.13 are now actually deployed.

See [Release Notes v0.8.14.0](releases/RELEASE-NOTES-v0.8.14.0.md) for full details.

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

After logging in at [alpha.pipermorgan.ai](https://alpha.pipermorgan.ai):

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

## Testing Focus for 0.8.14

**What's Stable** (light testing recommended):
- ✅ Login/authentication; invite-gated account creation
- ✅ Lists, Todos, Projects management (chat todos are real; the REST `/api/v1/todos` endpoint is still mocked, #1427)
- ✅ Files upload/download/preview/tagging
- ✅ GitHub connector reads (issue summaries, repo resolution)
- ✅ Per-user API keys, encrypted at rest
- ✅ The standup interview and free-form draft edits (0.8.13's focus — carried, not re-tested)

**Where to Focus Testing** (these need your attention):
- 🔍 **Your clock**: set your timezone under Settings → Preferences, then ask "what's my
  agenda today" / export a standup — is every time labeled with YOUR zone? Does "today"
  match your calendar, not UTC's (try after 5pm Pacific)?
- 🔍 **Preferences persist**: change a preference, wait for a deploy (or just come back
  tomorrow) — is it still set? Does the calendar-setup offer stay dismissed?
- 🔍 **Agenda times**: with a connected Google Calendar, do meetings show real times, never
  "TBD"? Does "Focus Time Available" appear?
- 🔍 **Add project in one line**: `add project <name> with repo <owner>/<repo>` — one turn?
  Leave out the name — do you get the exact line to type, not the same question twice?
- 🔍 **Honest GitHub writes**: "close issue 99999 in <a repo you own>" — do you get
  "There's no issue #99999… nothing was changed"?

## What's Working in 0.8.14

✅ **Conversational AI**:
   - LLM-grounded responses in Piper's voice, drawing on your work context
   - Guided standup interview that actually runs, drafts built only from your words, free-form draft edits (#1837)
   - Greeting + question handled together — your question gets answered (#1416)
   - Honest answers when a data source fails — "I couldn't check" instead of a false "nothing found" (#1425)
   - Honest error messages when your LLM key is missing, invalid, or out of quota (#1414, #1823, #1824)
   - Honest outcomes on GitHub writes — a 404 is "nothing was changed", never "may or may not" (#1858)
   - Session memory: "what did we create this session?" recalls what you actually did (#1394)

✅ **Time, on your clock** (new):
   - Every user-facing time carries your zone label; "today" is your calendar day (#1576, #1575, #1577, #1556)
   - Agenda shows real meeting times and focus blocks (#1576)

✅ **Todos, Lists & Projects (via chat and UI)**:
   - Create and manage todos conversationally — chat todos are real and persist
   - Add a project with its repo in one line (#1856)
   - List/todo metadata persists correctly (#1435)
   - Note: the REST `/api/v1/todos` endpoint is still mocked (#1427) — use chat or the UI pages

✅ **Personalization**:
   - Preferences (timezone, reminders, working mode) persist across restarts (#1574)
   - Personality questionnaire shapes Piper's warmth, confidence, and depth (#1422)
   - Per-user LLM provider selection — one valid key from any provider is enough (#1415, #1823)
   - Per-user API keys, encrypted at rest (AES-256-GCM)

✅ **Files**:
   - Upload, download, and in-browser preview
   - Search by name, filter by type, freeform tags
   - Drag & drop multi-file upload, bulk download as zip

✅ **Integrations**:
   - GitHub connector reads: issue summarization from live data, repo resolution
   - "Connect my GitHub"-style questions get real setup guidance (#1417)
   - Slack outbound, DMs, @-mentions (the `/standup` command has known gaps, #1429)

✅ **Core Infrastructure**:
   - Hosted on the consolidated Fly host as of 2026-09-22 (alpha.pipermorgan.ai)
   - Multi-user support with owner-scoped data access (#1420, #1421, #1434)
   - JWT auth, bcrypt passwords; session-token revocation survives cache restarts (#1808)
   - PostgreSQL, Redis, ChromaDB
   - Smoke gate: 534 tests green at release cut

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for current limitations.

---

## Getting Help

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — deeper testing
  walkthrough (rewritten 2026-09-21 for the hosted flow; the two docs now agree).
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Legal**: [ALPHA_AGREEMENT_v2.md](ALPHA_AGREEMENT_v2.md) (terms and conditions)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.14.0 means)

---

## Remember

This is **alpha software** (0.8.14.0). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT_v2.md` for details.

**Testing Focus**: Is every time you see on YOUR clock, with the zone named? Do your preferences stay set across deploys? Does the agenda show real times? Does a one-line add-project work — and does a bad GitHub write say so honestly?

---

**Happy testing!** 🚀

_Last Updated: September 23, 2026_
