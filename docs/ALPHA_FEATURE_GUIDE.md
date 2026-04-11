# Alpha Feature Guide (v0.8.6)

**Version**: 0.8.6
**Last Updated**: April 11, 2026

A guide to what Piper Morgan can do in the current alpha release.

---

## What's New in M1 (April 11, 2026)

Piper Morgan just closed its M1 "Foundation" milestone. If you tested an earlier build, here's what changed:

- **Piper feels like a colleague, not a template.** Most natural-language questions now get a real LLM-generated response with context about your work, instead of "I can't do that yet." This is the "conversational floor" — it's now the default path.
- **Setup is provider-agnostic.** The wizard asks you to pick one LLM provider (OpenAI *or* Anthropic) and enter one API key. You no longer need OpenAI specifically.
- **Todo completion actually works.** "Complete todo 1" or "complete the deployment plan todo" now persists the change in the database. A stack of three nested repository bugs was fixed on April 11.
- **GitHub errors are friendlier.** Ask Piper to create an issue before configuring GitHub and you get a clear "GitHub isn't connected yet" message instead of a cryptic error.
- **Fabrication guardrails.** The floor is now constrained against inventing todos, projects, or calendar events when it doesn't actually have that context. If you ask about your todos and you have none, Piper will say so.
- **Portfolio Onboarding wizard is disabled.** The conversational floor handles first interactions instead. (A Gall's Law decision — the wizard was hijacking too many sessions.)

See [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for the full list of fixes and for M2 carryover issues you should know about.

---

## Quick Start

| Task | How |
|------|-----|
| Start Piper | `python main.py` → opens http://localhost:8001 |
| Check system health | `python main.py status` |
| Run setup wizard | `python main.py setup` or visit /setup in browser |
| Set preferences | `python main.py preferences` |

---

## Getting Set Up

### GUI Setup Wizard

The easiest way to get started. Visit http://localhost:8001/setup after starting Piper.

**What it does:**
- Checks system health (Docker, Python, ports, database)
- **Asks you to pick a single LLM provider** from a dropdown: **OpenAI** or **Anthropic**
- Collects one API key for your chosen provider
- Creates your user account
- Optionally collects additional integration keys (Notion, etc.)
- Connects integrations via OAuth (Slack, Google Calendar) from Settings later

**About the provider choice**: you only need *one* provider to use Piper. Whichever you already have an account and key for is fine. You can swap later from Settings.

> **Known wrinkle**: See [#946](https://github.com/mediajunkie/piper-morgan-product/issues/946) — setup may occasionally pick up a stale key from the system keychain. If it does, clear old "Piper" entries from Keychain Access. A consent prompt is coming in M2.

### CLI Alternative

For terminal lovers: `python main.py setup` walks through the same process.

### System Health Check

Run `python main.py status` anytime to verify:
- Database connection
- API key validity
- Integration health
- Performance metrics

---

## Core Features

### Chat with Piper

The main interface. Type naturally and Piper responds.

Piper uses a two-layer approach:

1. **Canonical handlers** run first for specific actions — creating a GitHub issue, completing a todo, fetching your calendar. These execute deterministically when they have what they need.
2. **Conversational floor** handles everything else. It's an LLM with your real context (projects, todos, calendar) assembled into the prompt. Instead of a canned "I can't do that yet," you get a thoughtful response grounded in your actual data.

The floor is the default. Handlers only win when they're confident they can do the concrete thing you're asking for.

**Natural language Piper handles well:**

| Category | Examples |
|----------|----------|
| Identity | "What's your name?" "What can you do?" "Are you working?" |
| Time | "What day is it?" "What did we do yesterday?" "What's on my agenda?" |
| Projects | "What projects am I working on?" "Status of [project]?" "Which should I focus on?" |
| Todos | "List todos" / "list my todos" / "show todos" — all now match the same pattern and return real data (or an honest "no todos" if your list is empty) |
| Actions | "Create a GitHub issue about X" "Give me a status report" "Complete todo 1" |
| Open-ended | "How should I think about this roadmap?" "What would you do here?" — these now reach the conversational floor and get real answers |

**Fabrication discipline**: the floor is instructed not to invent data it doesn't have. If you ask about todos that don't exist, you should get "I don't see any todos in your list right now" — not a plausible-but-fake list. This is a first pass; if you catch a fabrication, please report it (issue #960).

> **Context quirk**: A one-word reply like "OK" or "sure" after a multi-turn exchange may occasionally lose context ([#922](https://github.com/mediajunkie/piper-morgan-product/issues/922)). If Piper seems confused, restate the request fully. A deeper fix is in M2.

### Todo Completion

You can complete todos by number or by name:

- `complete todo 1`
- `complete the deployment plan todo`
- `mark the review todo done`

As of April 11, these actually persist to the database. Previously a three-layer bug meant the handler *looked* successful (23 tests passed) but the write never made it through the repository stack. Fixed.

To verify: complete a todo, reload the Todos view, confirm it's marked complete.

### Interactive Standup

Create standup reports through conversation.

**How to use:**
1. Say "let's write a standup" or type `/standup`
2. Piper asks what you accomplished, what's next, any blockers
3. Review and refine iteratively until satisfied
4. Piper learns your preferences over time

### Portfolio Onboarding

**Currently disabled.** The conversational floor handles first interactions instead. This was a late-M1 decision: the onboarding wizard was hijacking sessions that would have been better served by natural conversation. It may return in a later milestone in a different form.

---

## Managing Your Work

### Lists, Todos, Projects

All three work similarly with full CRUD and sharing:

| Action | How |
|--------|-----|
| View | Click "Your Stuff" → Lists/Todos/Projects |
| Create | Click "+ Create" button |
| Edit | Click item → Edit |
| Delete | Click item → Delete (if you're owner/admin) |
| Share | Click item → Share → Enter email + role |
| Complete (todos) | "complete todo 1" / "complete the X todo" in chat, or check off in UI |

**Sharing roles:**
- **Viewer**: Can see but not modify
- **Editor**: Can modify but not delete or share
- **Admin**: Full access except transfer ownership

### Files

Upload and manage documents.

| Action | How |
|--------|-----|
| Upload | Files page → Upload (PDF, DOCX, TXT, MD, JSON up to 10MB) |
| Download | Click file → Download |
| Delete | Click file → Delete |

Files are user-isolated — you only see your own.

### Lifecycle Indicators

Projects and todos show lifecycle status badges:
- **Active**: Currently being worked on
- **Paused**: On hold
- **Completed**: Done
- **Archived**: No longer relevant

---

## Integrations

### Integration Health Dashboard

**Where**: Settings → Integrations

Check the health of all your connected services:
- Green = Healthy
- Yellow = Degraded
- Red = Failed
- Gray = Not configured

Click "Test All" for a comprehensive check, or test individual integrations.

### Slack

**Setup**: Settings → Integrations → Slack → Connect (OAuth)

**What works:**
- Send messages to channels
- Read channel history
- Receive notifications

### Google Calendar

**Setup**: Settings → Integrations → Calendar → Connect (OAuth)

**What works:**
- View your schedule ("What's on my calendar?")
- Create events
- Check availability

### GitHub

**Setup**: Settings → Integrations → GitHub → Enter PAT token

**What works:**
- Create issues ("Create a GitHub issue about X")
- Search issues
- View repository status
- Update issues

**Friendly pre-flight**: if you ask Piper to create an issue *before* configuring GitHub, you now get a clear "GitHub isn't connected yet — here's how to set it up" message instead of a generic error. (Previously this produced an unhelpful "Something unexpected happened.")

### Notion

**Setup**: Added during setup wizard (API key)

**What works:**
- Create pages
- Search content
- Document analysis ("Analyze this document")

---

## Personalization

### Preferences

Run `python main.py preferences` to set your preferences across 5 dimensions:

| Dimension | What it affects |
|-----------|-----------------|
| Communication | How Piper phrases responses |
| Work style | Task recommendations |
| Decision making | How much guidance vs. options |
| Learning | Explanation depth |
| Feedback | How Piper gives suggestions |

### Learning System

Piper learns from your interactions over time:
- Communication patterns
- Preferred workflows
- Common requests

This is experimental — feedback welcome on whether personalization feels accurate.

---

## Accessibility

Piper is designed to be accessible:

- **Keyboard navigation**: Tab through all UI elements
- **Screen readers**: ARIA landmarks throughout
- **High contrast**: Respects system preference
- **Reduced motion**: Respects system preference
- **Color contrast**: WCAG 2.1 AA compliant (4.5:1 minimum)

---

## Security

### What's Protected

| Data | Protection |
|------|------------|
| API keys | Encrypted in system keychain |
| Passwords | Bcrypt hashed (12 rounds) |
| Sessions | JWT tokens with expiration |
| Resources | Owner-based access control |

### What's Not Yet Protected

- Data at rest (database contents) — **use test data only**
- Full encryption at rest planned for beta

### Audit Logging

All sensitive operations are logged:
- Authentication events
- API key operations
- User actions

---

## Commands Reference

### CLI Commands

| Command | Purpose |
|---------|---------|
| `python main.py` | Start server |
| `python main.py --verbose` | Start with detailed logging |
| `python main.py --no-browser` | Start without opening browser |
| `python main.py setup` | Run setup wizard |
| `python main.py status` | Check system health |
| `python main.py preferences` | Set user preferences |
| `python main.py migrate-user` | Migrate user data |

### Chat Commands

| Command | Purpose |
|---------|---------|
| `/standup` | Start interactive standup |
| `/help` | Get help |

---

## Technical Details

For alpha testers who want to know what's under the hood:

- **Database**: PostgreSQL (via Docker on port 5433)
- **Test coverage**: 6,250+ tests passing (post-Apr 11 dead code cleanup #963)
- **API**: FastAPI on port 8001
- **Auth**: JWT tokens with bcrypt passwords
- **LLM providers**: OpenAI or Anthropic (pick one at setup, swap later from Settings)

---

## See Also

- [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) — What's broken, what's fixed, and what's carried into M2
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — Setup instructions
- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — 2-5 minute setup

---

_Last Updated: April 11, 2026_
