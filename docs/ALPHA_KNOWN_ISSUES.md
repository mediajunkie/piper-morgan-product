# Alpha Known Issues (v0.8.6)

**Version**: 0.8.6
**Last Updated**: April 11, 2026

This document helps alpha testers avoid wasting time on things we already know about.

Piper Morgan just closed its M1 "Foundation" milestone on April 11 after five rounds of user acceptance testing. Several things that used to be rough are now much better — and a few things that surfaced during UAT are being carried into M2 for deeper fixes. Both are documented below.

---

## Recent Improvements (Fixed in M1)

These are the changes alpha testers are most likely to notice. If something on this list still seems broken for you, please report it — it means our fix didn't fully land.

### Piper now talks like a colleague, not a template

Most natural-language queries that previously produced canned "I can't do that yet" responses now get a real, LLM-generated answer with context about your projects, todos, and calendar. Ask Piper something conversational and you should get a conversational reply.

This is called "floor-first routing" internally. It means the conversational floor is the default, and specific handlers only intercept when they have something concrete to do (create an issue, complete a todo, etc.).

### Setup wizard works with OpenAI **or** Anthropic

The setup wizard now asks you to pick **one** LLM provider from a dropdown (OpenAI or Anthropic) and enter a single API key. Previously OpenAI was effectively required. Either provider is fine — pick whichever one you already have a key for.

### "Complete todo" actually completes the todo

Saying "complete todo 1" or "complete the deployment plan todo" now persists the completion in the database. Previously the response sometimes *said* it was completing the todo but the change didn't stick. Three nested repository bugs were fixed on April 11.

### GitHub error path is now friendly

If GitHub isn't configured yet and you ask Piper to create an issue, you now get a clear "GitHub isn't connected yet — here's how to set it up" message instead of a generic "Something unexpected happened."

### Piper won't make up data it doesn't have

Earlier in M1, the conversational floor could occasionally fabricate todos, projects, or calendar events when it didn't have real context. That's now constrained — for example, asking "what are my todos?" when you have none will get "I don't see any todos in your list right now" instead of a plausible-but-fake list.

This is an initial guardrail. A deeper pass is planned for M2 (see #960 below).

### "List todos" now works without "my"

Saying "list todos" or "show todos" is now treated the same as "list my todos" / "show my todos". Previously the shorter phrasings could slip past the pattern matcher and produce hallucinated results.

---

## Known Issues

### Blocking

_None currently. All M1 gate blockers resolved April 11._

### Annoying

| Issue | Description | Workaround |
|-------|-------------|------------|
| [#696](https://github.com/mediajunkie/piper-morgan-product/issues/696) | Settings uses hardcoded user ID | Settings changes work but may not attribute to correct user in audit logs |
| [#697](https://github.com/mediajunkie/piper-morgan-product/issues/697) | Intent service uses hardcoded user ID | Chat works but user context not fully preserved |
| [#922](https://github.com/mediajunkie/piper-morgan-product/issues/922) | Single-word affirmations like "OK" after a multi-turn exchange may lose context | If Piper seems confused by a one-word reply, restate the request fully |
| [#946](https://github.com/mediajunkie/piper-morgan-product/issues/946) | Setup may occasionally pull a stale API key from the system keychain | If setup seems to be using a key you didn't just enter, remove old Piper entries from Keychain Access |

**Impact**: These issues affect smoothness but not the core loop. Workarounds exist for each.

### Cosmetic

_None currently tracked._

---

## M2 Carryover (Being Worked)

These are known rough edges that survived M1. They're tracked and scheduled for M2 work — you may encounter them during testing.

| Issue | What You Might See | Status |
|-------|-------------------|--------|
| [#922](https://github.com/mediajunkie/piper-morgan-product/issues/922) | A one-word "OK" / "yes" / "sure" after a long exchange sometimes gets treated as a fresh message | Partial fix landed (conversation continuity foundation). Deeper fix in M2. |
| [#946](https://github.com/mediajunkie/piper-morgan-product/issues/946) | Setup may pull a stale key from the keychain without asking | Consent prompt coming in M2. |
| [#947](https://github.com/mediajunkie/piper-morgan-product/issues/947) | Two internal LLM pathways exist side by side | Being consolidated in M2. Mostly invisible to you unless errors look inconsistent. |
| [#960](https://github.com/mediajunkie/piper-morgan-product/issues/960) | Floor occasionally phrases things with more confidence than it should (e.g. hedging near the edges of fabrication) | First guardrail landed in M1; hardening continues in M2. |
| [#961](https://github.com/mediajunkie/piper-morgan-product/issues/961) | Some routes may still reach the floor without full context | Audit planned for M2 — may surface more fabrication risks to fix. |

If you see something that looks like one of these, a quick note ("this feels like #960") is extremely helpful.

---

## Partially Complete

These features exist but have rough edges. Expect some friction.

| Feature | Status | What Works | What Doesn't |
|---------|--------|------------|--------------|
| **Data Encryption** | Partial | API keys encrypted in keychain, passwords bcrypt-hashed | Data at rest not fully encrypted. Use test data only. |
| **GitHub OAuth** | Not started | PAT token auth works | OAuth connect flow planned for future release |
| **Advanced Privacy** | Basic only | Owner-based access, sharing works | Granular controls planned for beta |

---

## Needs Testing

These features are complete but need real-world validation from alpha testers:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Conversational Floor** | Does Piper's natural-language response feel grounded and useful? Does it ever fabricate? | Just chat normally — ask about your work, your day, your projects |
| **Todo Completion** | Completing todos by name and by number — does it persist? | "complete todo 1" / "complete the X todo" then reload the Todos view |
| **Provider-Agnostic Setup** | Try setup with OpenAI. Try setup with Anthropic. Both should work. | `python main.py setup` or visit /setup |
| **GitHub Pre-Flight** | Ask Piper to create a GitHub issue *before* configuring GitHub — error message should be friendly | Fresh account, no GitHub PAT, say "create a github issue about X" |
| **Interactive Standup** | Does iterative refinement feel natural? | Say "let's write a standup" |
| **Learning System** | Does Piper adapt to your communication style over time? | Use for a few days, note any personalization |
| **Lifecycle Indicators** | Do status badges appear correctly on projects/todos? | Check Projects and Todos views |
| **Accessibility** | Keyboard navigation, screen reader support | Tab through UI, test with VoiceOver |
| **Integration Health** | Does the dashboard accurately reflect your integration status? | Settings → Integrations → Test All |

> **Note**: Portfolio Onboarding (conversational project setup on first "Hello!") is currently **disabled** by design. The conversational floor handles first interactions instead — a Gall's Law decision made late in M1 because the wizard was hijacking sessions. It may return in a later milestone.

---

## What Works

For detailed feature documentation, see [ALPHA_FEATURE_GUIDE.md](ALPHA_FEATURE_GUIDE.md).

**Summary by category:**

- **Setup**: GUI wizard (provider dropdown + single key), CLI wizard, system health checks
- **Authentication**: Login/logout, JWT tokens, password security
- **Integrations**: Slack (OAuth), Google Calendar (OAuth), GitHub (PAT), Notion (API key), Health Dashboard
- **Core UI**: Lists, Todos, Projects, Files — all with CRUD and sharing
- **Chat**: Conversational floor for natural language + canonical handlers for specific actions. If you ask something Piper doesn't have a specific handler for, you still get a real, context-aware response instead of a template.
- **Todo Completion**: Now persists to the database (fixed April 11)
- **Accessibility**: WCAG 2.1 AA compliant, keyboard nav, high contrast mode
- **Quality**: 6,303+ automated tests passing

---

## Planned for Beta

Brief overview. See [roadmap](internal/planning/roadmap/roadmap.md) for full details.

| Milestone | Focus | Status |
|-----------|-------|--------|
| M1: Foundation | Floor-first routing, provider-agnostic LLM, lifecycle basics | ✅ Closed Apr 11 |
| M2: Conscious Floor + Action Handlers | Guardrail hardening, LLM pathway consolidation, action handler coverage | 🎯 In planning |
| M3: Skills | Core skills library, multi-agent coordinator | Backlog |
| M4: Documents | Unified document processing, file browser | Backlog |
| M5: Polish | Registration flow, priority engine | Backlog |
| M6: Distribution | Release packaging | Backlog |

---

## How to Report Issues

### Before Reporting

1. Check this list — is it already known?
2. Gather context: `python main.py status > status.txt`

### What to Include

```
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
```

If it looks like one of the M2 carryover items above, mentioning the issue number helps us triage faster.

### Where to Report

- **GitHub Issues**: [Create new issue](https://github.com/mediajunkie/piper-morgan-product/issues/new)
- **Email**: christian@[domain] for private issues
- **Weekly Check-in**: Discuss during scheduled calls

---

## Testing Focus

**Please focus on:**
- Setup experience — does the single-provider wizard feel clear? Did your chosen provider work?
- Natural-language chat — does the conversational floor feel grounded, or does it ever fabricate?
- Todo workflows — create, list, complete, reload — does completion stick?
- GitHub error paths — what happens when you try GitHub actions before configuring GitHub?
- Daily workflows — what feels natural vs. clunky?
- Integration points — if you use GitHub/Slack/Notion/Calendar
- Performance — any lag or delays?
- Overall feel — delightful or frustrating?

**Please report:**
- Blockers (can't use at all)
- Frequent annoyances (happens repeatedly)
- Delightful surprises (what worked great!)
- Missing expectations (thought it would do X)
- **Fabrications** — anytime Piper tells you about a todo, project, or event that doesn't actually exist

---

## See Also

- [ALPHA_FEATURE_GUIDE.md](ALPHA_FEATURE_GUIDE.md) — What's available and how to use it
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — Setup and usage instructions
- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — Quick 2-5 minute setup

---

_Last Updated: April 11, 2026_
