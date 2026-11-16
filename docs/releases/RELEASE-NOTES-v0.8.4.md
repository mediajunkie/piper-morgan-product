# Release Notes: v0.8.4

**Release Date**: January 12, 2026
**Release Type**: Feature Release (Sprint B1 Complete, 2 Epics)

---

## Overview

This release completes Sprint B1, delivering two major capabilities: **Integration Settings** (Epic #543) and **Portfolio Onboarding** (Issue #490). Users can now manage all their integration credentials from a unified Settings page, and new users experience a conversational onboarding flow that helps them set up their project portfolio.

**Key improvements in this release:**
- **Integration credential management**: Configure Slack, Calendar, GitHub, and Notion credentials directly in Settings with OAuth flows and secure storage
- **Portfolio onboarding**: Tell Piper about your projects during first meeting, making subsequent conversations more contextual
- **Bug fixes**: Logout 403 errors resolved, OAuth test buttons now use correct tokens, Demo integration disabled by default

**Try it now:** Visit Settings → Integrations to configure your tools, or start a fresh session and greet Piper to experience the portfolio onboarding flow.

---

## What's New

### Epic #543: Integration Settings

**Unified credential management for all integrations**

All integration credentials can now be configured from Settings → Integrations:

| Integration | Configuration Method | Features |
|-------------|---------------------|----------|
| **Slack** | OAuth Connect button | Connect/disconnect, token stored securely |
| **Google Calendar** | OAuth Connect button | Sync preferences, auto-refresh tokens |
| **GitHub** | Personal Access Token | Keychain fallback, repository preferences |
| **Notion** | API Key | Keychain fallback, workspace preferences |

**Issues completed:**
- #576: Slack OAuth credential UI
- #577: Google Calendar OAuth credential UI
- #578: GitHub PAT UI configuration with keychain fallback
- #579: Notion API key UI with keychain fallback
- #571: Calendar sync preferences
- #572: Notion workspace preferences
- #573: GitHub repository preferences
- #544: "Disconnect All" button for bulk management

### Issue #490: Portfolio Onboarding (FTUX-PORTFOLIO)

**Conversational project setup for new users**

When Piper meets a new user (detected via first greeting), it initiates a portfolio onboarding conversation:

```
User: Hello!
Piper: Hello! I'm Piper Morgan, your PM assistant. I notice we haven't
       set up your project portfolio yet. Would you like to tell me about
       the projects you're working on?

User: Sure, I'm working on Piper Morgan and Decision Reviews.
Piper: Got it! I'll remember that you're working on:
       • Piper Morgan
       • Decision Reviews
       Would you like to add more projects, or shall we continue?
```

**Features:**
- Multi-turn conversation with state machine (INITIATED → GATHERING_PROJECTS → CONFIRMING → COMPLETE)
- Extracts project names from natural language
- Creates Project entities in database
- Integrates with existing onboarding detection

### Issue #365: Slack Attention Decay

**Pattern learning for attention models**

Slack message importance now decays over time with configurable patterns. This helps Piper prioritize recent messages over older ones when summarizing activity.

---

## Bug Fixes

| Issue | Fix | Impact |
|-------|-----|--------|
| Logout 403 | Fixed "Not authenticated" error on logout | Users can now log out without errors |
| #562 | Integration Test button uses stored OAuth tokens | Test buttons work correctly after connecting |
| Demo integration | Disabled by default | No longer confuses users with fake "Demo" integration |

---

## Performance & Quality

- **Test Count**: 2,100+ tests (up from 860+ in v0.8.3)
- **New Integration Tests**: Real intent wiring verification (#559)
- **Standup Performance**: Maintained sub-500ms response times

---

## Technical Details

### Commits Included

31 commits since v0.8.3.2, including:
- 8 feature commits (Epics #543, #490, #365)
- 2 bug fix commits
- Documentation and infrastructure updates

### Database Changes

- No schema migrations required
- New Project records created via portfolio onboarding

### New/Modified Files

**Integration Settings (Epic #543):**
- `web/api/routes/integrations.py` - OAuth endpoints
- `services/integrations/*/config_service.py` - Keychain fallback
- `templates/settings-integrations.html` - Credential UI

**Portfolio Onboarding (#490):**
- `services/onboarding/portfolio_handler.py` - Conversation handling
- `services/onboarding/portfolio_manager.py` - State machine

---

## Upgrade Notes

**From v0.8.3.2:**
1. Pull latest: `git pull origin main`
2. No database migration required
3. Restart application

No breaking changes. Existing integrations continue to work.

---

## Known Issues

See [ALPHA_KNOWN_ISSUES.md](../BETA_KNOWN_ISSUES.md) for current known issues.

**Known limitations in this release:**
- Portfolio onboarding currently supports text-based project names only
- GitHub OAuth (vs PAT) planned for future release

---

## What's Next

**Sprint B1 Complete** - All planned work delivered in this release.

**Next Priority: MUX (Modeled User Experience)**

The MUX super-epics represent our UX 2.0 initiative, bringing consciousness-aware interaction models to Piper:
- **Spatial context awareness**: Understanding user's work environment
- **Temporal intelligence**: Calendar-aware interactions
- **Capability discovery**: Piper explains what it can do when asked

**Roadmap:**
- MUX Foundation work begins Q1 2026
- Beta preparation (v0.9 target: April 2026)

**Ongoing:**
- Alpha tester feedback continues to drive improvements
- Capabilities naming standardization in progress

---

## Contributors

- PM: xian
- Lead Developer: Claude Code (Opus)
- Alpha Testers: Thank you to our alpha testing team for their valuable feedback

---

*Release managed by Lead Developer session 2026-01-12*
