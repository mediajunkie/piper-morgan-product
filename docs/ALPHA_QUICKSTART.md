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
**[piper-morgan.fly.dev](https://piper-morgan.fly.dev)** and log in.

If you don't have login credentials yet, you're likely a new tester — email
**xian@pipermorgan.ai** to get set up. Alpha testing is currently a small, curated group (per
`ESSENCE.md`, ~11 testers), so access is arranged directly rather than through self-serve signup.

That's it — no clone, no Docker, no Python version to check. **Time to first use: however long it
takes to log in.**

---

## What's New in 0.8.11

This release is a systematic sweep through half-finished corners of the product: four parallel audits over the whole codebase, fixes for every serious problem they found, and build-time guards so the same classes of bugs can't quietly return. What you'll feel as a tester: **Piper stops lying** — about your data, about its capabilities, and about what went wrong.

**Personality questionnaire works again** (#1422) — Your questionnaire answers now actually shape Piper's tone: warmth, confidence, level of detail. A database column lost in an earlier migration had been silently discarding them. Prior answers were unrecoverable, so re-answer the questionnaire once after updating.

**Your LLM provider choice is respected** (#1415) — Provider selection is now per-user. One user's setup can no longer pin the whole instance to their provider — your default provider and authorized list are yours alone.

**Greetings answer your actual question** (#1416) — "Hi! How do I address you?" gets the question answered. Only pure pleasantries get the short greeting response.

**"Connect my GitHub" gets real guidance** (#1417) — Asking to connect GitHub or another tool now points you at Settings → Integrations with real instructions, instead of a wrong generic decline.

**No more false "there is nothing" claims** (#1425) — Status, agenda, and priority answers now distinguish "I couldn't check" from "genuinely empty." If the todo lookup fails, Piper says "I couldn't check your todos just now" — never a false "no pending tasks."

**Honest error messages for API-key problems** (#1414) — When your LLM key is missing, invalid, or out of quota, Piper says so instead of "Something unexpected happened."

**Session memory** (#1394) — Ask "what did we create this session?" and Piper recalls it from a real ledger of session activity. Follow-ups like "update the title" resolve to the issue you just created.

**Also in this release** — Owner-scoping fixes so searches and defaults can't leak across users (#1420, #1421, #1434); list/todo metadata that actually persists instead of being silently discarded on save (#1435); and an end to false capability denials — Piper no longer claims it can't accept file uploads or set reminders when it can (#1426).

See [Release Notes v0.8.11.0](releases/RELEASE-NOTES-v0.8.11.0.md) for full details. (Deploying an
update yourself? See `CONTRIBUTING.md` — migrations are an operator step, not a tester one.)

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

After logging in at [piper-morgan.fly.dev](https://piper-morgan.fly.dev):

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

## Testing Focus for 0.8.11

**What's Stable** (light testing recommended):
- ✅ Login/authentication
- ✅ Lists, Todos, Projects management (chat todos are real; the REST `/api/v1/todos` endpoint is still mocked, #1427)
- ✅ Files upload/download/preview/tagging
- ✅ GitHub connector reads (issue summaries, repo resolution)
- ✅ Per-user API keys, encrypted at rest

**Where to Focus Testing** (these need your attention):
- 🔍 **Questionnaire → tone shift**: Re-answer the personality questionnaire, then chat — does Piper's tone actually reflect your answers?
- 🔍 **Your own provider**: Set your own LLM key and provider in Settings → LLM Keys — does chat use your provider? (Check your provider's usage dashboard.)
- 🔍 **Greeting + question**: Send "Hi!" plus a real question in one message — does the question get answered?
- 🔍 **Connect guidance**: Try "connect my github" or "can you connect my slack" — do you get real setup guidance pointing at Settings → Integrations?
- 🔍 **Honest status claims**: Ask for your status, agenda, or standup — are the claims about your todos and issues honest? "I couldn't check" is correct when a lookup fails; a false "nothing found" is a bug.
- 🔍 **Session recall**: Create an issue in chat, then ask "what did we create this session?" — does Piper recall it?

---

## If Something Breaks

### Can't log in / forgot your password?

Email **xian@pipermorgan.ai** — accounts are provisioned directly for this small a tester group,
so there's no self-serve password reset yet.

### Something else looks broken?

Check [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) first — it may already be tracked. If not,
report it (see "Getting Help" below).

*(Running a local copy and hit a setup problem instead? That's `CONTRIBUTING.md`'s
troubleshooting section, not this one.)*

### UI Navigation

After logging in at [piper-morgan.fly.dev](https://piper-morgan.fly.dev):

- **Home** → `/` (chat interface)
- **Lists** → `/lists`
- **Todos** → `/todos`
- **Projects** → `/projects`
- **Files** → `/files`
- **Standup** → `/standup`
- **Settings** → `/settings` (preferences, integrations)
- **User Menu** (top right) → Logout, profile settings

---

## What's Working in 0.8.11

✅ **Conversational AI**:
   - LLM-grounded responses in Piper's voice, drawing on your work context
   - Greeting + question handled together — your question gets answered (#1416)
   - Honest answers when a data source fails — "I couldn't check" instead of a false "nothing found" (#1425)
   - Honest error messages when your LLM key is missing, invalid, or out of quota (#1414)
   - Session memory: "what did we create this session?" recalls what you actually did (#1394)

✅ **Todos & Lists (via chat and UI)**:
   - Create and manage todos conversationally — chat todos are real and persist
   - List/todo metadata persists correctly (#1435)
   - Note: the REST `/api/v1/todos` endpoint is still mocked (#1427) — use chat or the UI pages

✅ **Personalization**:
   - Personality questionnaire shapes Piper's warmth, confidence, and depth (#1422)
   - Per-user LLM provider selection — your default and authorized providers are yours (#1415)
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
   - Multi-user support with owner-scoped data access, tightened this release (#1420, #1421, #1434)
   - JWT auth, bcrypt passwords
   - PostgreSQL via Docker (port 5433), Redis, ChromaDB
   - Smoke gate: 565 tests green at release cut

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for current limitations.

---

## Getting Help

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — deeper testing walkthrough.
  ⚠️ **Not yet audited for the hosted-primary change** (that doc still assumes local install in
  places) — if it contradicts this one on how to get started, trust this doc and flag the
  discrepancy.
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Legal**: [ALPHA_AGREEMENT_v2.md](ALPHA_AGREEMENT_v2.md) (terms and conditions)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.11.0 means)

---

## Remember

This is **alpha software** (0.8.11.0). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT_v2.md` for details.

**Testing Focus**: Does the questionnaire actually change Piper's tone? Does chat use YOUR provider? Do greetings with a question attached get the question answered? Are status and agenda claims honest? Does session recall work?

---

**Happy testing!** 🚀

_Last Updated: August 31, 2026_
