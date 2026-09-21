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

## What's New in 0.8.13

A fast follow to v0.8.12.0 — cut one day later so the first real dogfood session's fixes
reach testers quickly. Theme: **nothing invented, nothing borrowed**.

**The standup stops inventing things** (#1837, #1836) — accepting the guided-interview
offer actually starts the interview; the generic placeholder draft ("Made progress on
assigned tasks") is deleted and unreachable; free-form edits ("change yesterday to say I
ran the quarterly review") genuinely apply; "I've updated your standup" is only said when
something actually changed; and Piper no longer denies an interview offer it made three
turns earlier.

**Keyless first contact is human** (#1818) — a keyless "hi" gets *"Hello — good to meet
you."* plus one clear sentence about adding a key, instead of a wall of policy. "Thanks"
gets an honest acknowledgment, never a "you're welcome" for work that never happened.

**The server-key concept is deleted, not just refused** (#1812 complete) — there is no
code path, gated or otherwise, to any credential but yours. Every LLM call bills the
acting user's own key, or refuses honestly.

**`/health` tells the truth** (#1839) — real deployed version, git SHA, and environment,
replacing values that had been hardcoded for months.

See [Release Notes v0.8.13.0](releases/RELEASE-NOTES-v0.8.13.0.md) for full details.

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

## Testing Focus for 0.8.13

**What's Stable** (light testing recommended):
- ✅ Login/authentication; invite-gated account creation
- ✅ Lists, Todos, Projects management (chat todos are real; the REST `/api/v1/todos` endpoint is still mocked, #1427)
- ✅ Files upload/download/preview/tagging
- ✅ GitHub connector reads (issue summaries, repo resolution)
- ✅ Per-user API keys, encrypted at rest

**Where to Focus Testing** (these need your attention):
- 🔍 **The standup interview**: say "let's do my standup", accept the interview offer —
  does it immediately ask about yesterday? Is the resulting draft built from YOUR words
  (never boilerplate)?
- 🔍 **Free-form standup edits**: ask for a real change in your own words — does it
  apply? Ask for an inapplicable one — do you get an honest "unchanged" instead of a
  false success?
- 🔍 **Keyless first contact** (if you can spare a keyless moment): "hi" and "thanks"
  before adding a key — friendly acknowledgment plus one key sentence, no error-speak?
- 🔍 **Key honesty no-regress**: remove your key, try a chat turn — a clear "add your
  own key" message? Re-add — does everything resume?

## What's Working in 0.8.13

✅ **Conversational AI**:
   - LLM-grounded responses in Piper's voice, drawing on your work context
   - Guided standup interview that actually runs, drafts built only from your words, free-form draft edits (#1837)
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

- **Full Guide**: [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — deeper testing
  walkthrough (rewritten 2026-09-21 for the hosted flow; the two docs now agree).
- **Known Issues**: [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) (bugs and status)
- **Legal**: [ALPHA_AGREEMENT_v2.md](ALPHA_AGREEMENT_v2.md) (terms and conditions)
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.13.0 means)

---

## Remember

This is **alpha software** (0.8.13.0). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT_v2.md` for details.

**Testing Focus**: Does the standup interview keep its word — and its drafts to YOUR words? Do edits honestly apply or honestly decline? Is every keyless/key-error message human and true? Does chat spend YOUR key only?

---

**Happy testing!** 🚀

_Last Updated: September 21, 2026_
