# Alpha Known Issues (v0.8.8)

**Version**: 0.8.8
**Last Updated**: June 20, 2026

This document helps alpha testers avoid wasting time on things we already know about.

v0.8.8 covers four closed milestones: M1 Foundation, M2 Conscious Floor, M3 UI Coherence + Integrations, and D1/RECONNECT. The D1 gate closed at 252/252 canonical regression tests passing. What's below are the rough edges that survived those gates.

---

## Recent Improvements (Fixed in D1/0.8.8)

These are the changes alpha testers are most likely to notice. If something on this list still seems broken for you, please report it.

### Piper no longer fabricates when it doesn't know

The Conscious Floor (M2) replaced the template fallback with an LLM-grounded response assembled from your actual context — blocked items, active sprint, recent activity. When Piper doesn't have context, it says "I don't have enough context for that" instead of generating a plausible-but-invented response. This is a significant honesty improvement; please report any fabrications you encounter.

### BYOC credential layer

You can now store your API keys (OpenAI, Anthropic, Notion, etc.) in your macOS keychain via Settings → Integrations. No more editing config files or re-entering keys after restarts. Known rough edge: the Settings UI sometimes requires re-pasting despite the key being saved server-side — see #1105 below.

### Navigation renamed to match reality

History is now Radar. Collections is now Lists. The labels in the nav now match what the features actually do.

### Radar is the default home

The Radar view (blocked items, priority surfacing, recent activity) is now the default workspace instead of a hidden tab. Compose autosave also landed — your draft survives navigation away.

### Files experience rebuilt (M3)

Full file management: search by name/type, in-browser preview, bulk download as zip, drag & drop upload, freeform tags with search.

### Slack inbound rebuilt (M3)

Inbound Slack messages now route to Piper via Socket Mode (Socket Mode was the fix for the inbound regression that started Oct 2025). Outbound, DMs, and @-mentions continue to work.

---

## Known Issues

### Blocking

_None currently at P0._

### Annoying (tester-facing)

| Issue | Description | Workaround |
|-------|-------------|------------|
| [#1105](https://github.com/mediajunkie/piper-morgan-product/issues/1105) | Settings UI sometimes requires re-pasting API key even when saved correctly server-side | Restart the server after saving — keychain read works correctly on restart |
| [#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164) | "Start private session" toggle in History slide-out is UI-only — no backend behavior | Cosmetic; don't rely on it |
| [#1216](https://github.com/mediajunkie/piper-morgan-product/issues/1216) | "What have you learned about my workstyle?" claims a seed-vs-real distinction the system can't actually make | Report these — they're honesty gaps |
| [#1256](https://github.com/mediajunkie/piper-morgan-product/issues/1256) | Stakeholder-update queries occasionally misclassify as update_document_query | Rephrase as "write a stakeholder update for..." if response feels off |

### Security / multi-tenancy (being worked)

| Issue | Description | Status |
|-------|-------------|--------|
| [#1241](https://github.com/mediajunkie/piper-morgan-product/issues/1241) | Some content not fully anchored to user auth — multi-tenancy completeness audit | Architect-owned; being investigated. Use test data only. |

---

## RECONNECT Carryover (Being Worked)

These are known architectural rough edges tracked for the RECONNECT sprint:

| Issue | What You Might See | Status |
|-------|-------------------|--------|
| [#1226](https://github.com/mediajunkie/piper-morgan-product/issues/1226) | Connector repo-resolution is fragile — config has no stable home | RECONNECT-WS1 scope; architectural refactor planned |
| [#1270](https://github.com/mediajunkie/piper-morgan-product/issues/1270) | Documents/Files object model is a nav band-aid — `/documents` and `/files` collapsed under one nav item | D2 scope; the nav label works but the object model distinction is deferred |

---

## Partially Complete

| Feature | Status | What Works | What Doesn't |
|---------|--------|------------|--------------|
| **BYOC credentials** | Partial | Keys stored in keychain; server reads them correctly | Settings UI re-paste bug (#1105); macOS keychain only |
| **Data encryption** | Partial | API keys encrypted in keychain, passwords bcrypt-hashed | Data at rest not fully encrypted; use test data only |
| **GitHub OAuth** | Not started | PAT token auth works | OAuth connect flow planned for a future release |
| **History privacy toggle** | UI stub only | Toggle renders correctly | No backend — doesn't do anything yet (#1164) |

---

## Needs Testing

These features are complete in 0.8.8 but need real-world validation:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Conscious Floor** | Ask Piper things it shouldn't know — does it say "I don't have enough context" or does it fabricate? | Just chat normally |
| **BYOC credentials** | Enter API keys in Settings, restart the server — do they persist? | Settings → Integrations |
| **Radar** | Are your blocked items, priorities, and recent activity surfaced on home? | Default home view |
| **Compose autosave** | Start typing, navigate away, come back — is the draft still there? | Home chat compose area |
| **Files bulk download** | Upload 3+ files, checkbox-select them, download as zip | /files |
| **Slack inbound** | If Slack is connected, send Piper a message — does it arrive and respond? | Slack DM to Piper bot |
| **Floor honesty** | Ask "what todos do I have?" with no todos — does Piper say it doesn't see any, or invent some? | Fresh account, no todos |

---

## What Works

- **Conversational AI**: LLM-grounded floor for unmatched queries; antecedent resolution ("it" / "that"); honest refusal when context is missing
- **Files**: Search, preview, bulk download, drag & drop upload, freeform tags
- **Integrations**: Slack (inbound via Socket Mode, outbound, DMs, @-mentions); GitHub (issue summarization, repo resolution, lifecycle); Notion (append_blocks, URL unfurling); Calendar
- **BYOC & Settings**: API keys in macOS keychain via Settings UI; Radar as default home; nav renamed
- **Setup & Onboarding**: GUI setup wizard, system health checks, API key validation, user account creation
- **Core Infrastructure**: Multi-user, JWT auth, bcrypt passwords; PostgreSQL, Redis, ChromaDB; 252/252 canonical regression passing

---

## Planned for Next Sprints

| Sprint | Focus | Status |
|--------|-------|--------|
| RECONNECT | Connector refactor — config stability, repo-resolution hardening | Next up |
| M4: Trust + Learning | Learning system, trust gradient, preference persistence | Backlog |
| M5: Distribution + Polish | Registration flow, priority engine, polish | Backlog |
| Beta (0.9.0) | Target: July 4, 2026 | — |

---

## How to Report Issues

**What to include:**
```
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
```

- **GitHub Issues**: [Create new issue](https://github.com/mediajunkie/piper-morgan-product/issues/new)
- **Email**: Reply to your onboarding email for private issues

---

## See Also

- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — Quick setup
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — What to test and how
- [Release Notes v0.8.8](releases/RELEASE-NOTES-v0.8.8.md) — Full D1 changelog

---

_Last Updated: June 20, 2026_
