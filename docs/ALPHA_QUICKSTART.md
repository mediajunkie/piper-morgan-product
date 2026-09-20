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

## What's New in 0.8.12

Two months of work, one theme: **your key, your account**. Every LLM call Piper makes is
now billed to *your* stored key — there is no shared server credential, no silent fallback
to anyone else's account, and no way for your setup to overwrite another tester's. When no
key is bound, Piper refuses honestly and says what to do, instead of erroring vaguely or
quietly spending.

**Your key is always the one spent** (#1807–#1819) — the "server key" concept is gone by
ruling and by code. Keyless turns get an honest refusal with instructions, never
"Something unexpected happened."

**OpenAI-only? Slack works fully** (#1822) — Slack conversations bind whichever of your
keys exist. (Web chat still asks for an Anthropic key at the door for now — see Known
limitations.)

**Finished flows let go** (#1617 and the acceptance-contract family) — after a standup's
"Anything else?", your next command routes normally on the first try instead of the flow
re-rendering its summary or swallowing the message.

**Truthful lists and statuses** (#1717, #1730, the GitHub-six) — aggregate answers name
failed sources instead of blending them into a false "nothing found," and long GitHub
lists carry honest counts with an offer to fetch the rest instead of silent truncation.

**Security hardening** — chat-render XSS fixed, stale unauthenticated page twins removed,
demo plugin unmounted by default, cross-user isolation regression-hardened.

See [Release Notes v0.8.12.0](releases/RELEASE-NOTES-v0.8.12.0.md) for full details. (Deploying an
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

## Testing Focus for 0.8.12

**What's Stable** (light testing recommended):
- ✅ Login/authentication
- ✅ Lists, Todos, Projects management (chat todos are real; the REST `/api/v1/todos` endpoint is still mocked, #1427)
- ✅ Files upload/download/preview/tagging
- ✅ GitHub connector reads (issue summaries, repo resolution)
- ✅ Per-user API keys, encrypted at rest

**Where to Focus Testing** (these need your attention):
- 🔍 **Key honesty**: remove your key, try a chat turn — do you get a clear "add your own
  key" message (never a vague error, never a served answer billed to nobody-knows-who)?
  Re-add the key — does everything resume?
- 🔍 **Your provider's dashboard**: after a chat session, check YOUR provider's usage
  page — the calls should be there (and nowhere else).
- 🔍 **Flow release**: run a standup to the end, then immediately issue an unrelated
  command ("change the status of issue #… ") — does it route on the first try?
- 🔍 **Honest emptiness**: ask for your agenda/todos when you have none — does Piper
  distinguish "nothing there" from "couldn't check"?

## What's Working in 0.8.12

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
- **Version Info**: [VERSION_NUMBERING.md](VERSION_NUMBERING.md) (what 0.8.12.0 means)

---

## Remember

This is **alpha software** (0.8.12.0). Expect bugs. Don't use for production. You're responsible for API costs. See `ALPHA_AGREEMENT_v2.md` for details.

**Testing Focus**: Is every key message honest (never vague, never someone else's bill)? Does chat spend YOUR key only? Do finished flows release your next command? Are empty-vs-failed answers distinguished?

---

**Happy testing!** 🚀

_Last Updated: September 20, 2026_
