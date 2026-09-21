# Piper Morgan Alpha Testing Guide

**Version**: 0.8.13.0
**Last Updated**: September 21, 2026
**For**: Alpha Testers

**Rewritten 2026-09-21 (Lead), closing #1804.** This guide previously walked testers
through a local clone/Docker/setup-wizard install — a flow retired by #1708 (2026-08-31):
Piper Morgan's alpha is a **hosted app** at
[alpha.pipermorgan.ai](https://alpha.pipermorgan.ai), and that's what this guide now
describes. Engineers who want to run the code locally: see `CONTRIBUTING.md` — local
setup lives there, not here.

---

## Returning Tester? Start Here

If you already have an account, skip straight to what matters:
- **[What's New in 0.8.13](#whats-new-in-0813)** — the standup stops inventing things, keyless turns get a human answer, every LLM call is on your own key
- **[What to Test in 0.8.13](#what-to-test-in-0813)** — priority test walks for this release
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
- [ ] **Your invite code** — alpha is invite-only; codes come directly from
      **xian@pipermorgan.ai**. If you don't have one, that's the address to write.
- [ ] **At least one LLM API key of your own**:
  - An [Anthropic API key](https://console.anthropic.com/) (Claude), and/or
  - An [OpenAI API key](https://platform.openai.com/api-keys) (GPT-4-class models)
- [ ] Budget roughly $5–20 for LLM API costs over the alpha period — **Piper runs on
      your key and your account**; it never bills anyone else's (see What's New).

**Optional (for the integration features):**

- [ ] A GitHub personal access token (issue creation/management features)
- [ ] A Notion API key (document features)
- [ ] A Slack workspace you can connect (notifications, chat-with-Piper-from-Slack)

**Time commitment**: ~10 minutes to first conversation; 15–30 minutes weekly for
feedback during the alpha period.

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

**⚠️ ALPHA SOFTWARE WARNING ⚠️**

This is pre-release alpha software (version 0.8.13.0). By proceeding, you acknowledge:

1. **Expected Issues**: bugs, rough edges, and incomplete features are normal
2. **Data Loss Risk**: your data on the alpha instance may be lost at any time
3. **No Production Use**: do NOT use it for mission-critical or time-sensitive work
4. **API Charges**: you are responsible for all LLM API costs your key incurs
5. **Security**: not security audited — use test data only, no sensitive information
6. **No Warranty**: provided "as-is", without any warranty whatsoever
7. **No Support SLA**: best-effort support only, no guaranteed response times

See `ALPHA_AGREEMENT_v2.md` for complete terms.

---

## What's New in 0.8.13

v0.8.13.0 is the "Nothing Invented, Nothing Borrowed" release — a fast follow to
v0.8.12.0, cut one day later so the first real dogfood session's fixes reach you quickly.

**The standup stops inventing things** ([#1837](https://github.com/mediajunkie/piper-morgan-product/issues/1837), [#1836](https://github.com/mediajunkie/piper-morgan-product/issues/1836)):

- Accepting the guided-interview offer **actually starts the interview** — first
  question, straight away, no second "Ready for your standup?"
- The generic placeholder draft ("Made progress on assigned tasks") is **deleted and
  unreachable**. With nothing to build from, Piper interviews you or says so — it never
  presents boilerplate as your day.
- **Free-form draft edits work**: "change what I did yesterday — say I spent the day on
  X" now applies (it runs a model on your key). "Add blocker: …" and "remove …" stay
  instant and key-free.
- "I've updated your standup" is only ever said **when something actually changed**;
  otherwise you get an honest "unchanged" answer.
- Ask "didn't you offer me an interview?" and Piper answers from what actually happened
  in the conversation — it no longer denies its own three-turns-ago offer.

**Keyless first contact is human** ([#1818](https://github.com/mediajunkie/piper-morgan-product/issues/1818)):

- A keyless "hi" now gets *"Hello — good to meet you."* plus one clear sentence about
  the key, instead of a wall of policy. "Thanks" gets an honest *"That's kind — though I
  haven't actually done anything yet."*

**The server-key concept is deleted, not just refused** ([#1812](https://github.com/mediajunkie/piper-morgan-product/issues/1812)):

- v0.8.12.0 closed every door to a product-owned LLM credential; this release removes
  the doors' frames — there is no code path, gated or otherwise, to spend anything but
  the acting user's own key.

**Operational honesty**:

- `/health` now reports the real deployed version, git SHA, and environment
  ([#1839](https://github.com/mediajunkie/piper-morgan-product/issues/1839)) — the alpha
  had reported a hardcoded `environment=staging` for months.

See [Release Notes v0.8.13.0](releases/RELEASE-NOTES-v0.8.13.0.md) for full details, and
[releases/README.md](releases/README.md) for prior release history (v0.8.12.0's "Your
Key, Your Account" notes cover the BYOC model this release completes).

---

# Chapter 2: Testing

This chapter covers what to test and how. If you're already set up, **start here**.

## What to Test in 0.8.13

The standup flow and the keyless experience are the focus — both were rebuilt from a
real tester transcript this weekend. **Does the interview actually run? Do edits
actually apply? Do refusals tell the truth?**

### Test Walk 1: The interview offer keeps its word ([#1837](https://github.com/mediajunkie/piper-morgan-product/issues/1837))

1. In chat, say "let's do my standup"
2. If Piper has no observed activity for you, it should say so and offer a guided
   interview — answer "yes"
3. Check: does it immediately ask "What did you work on yesterday?" (not re-greet you,
   not ask if you're ready again)?
4. Answer the questions with real content
5. Check: the draft it shows is built from **your words** — never "Made progress on
   assigned tasks" or other boilerplate

### Test Walk 2: Free-form standup edits ([#1837](https://github.com/mediajunkie/piper-morgan-product/issues/1837)/[#1836](https://github.com/mediajunkie/piper-morgan-product/issues/1836))

1. With a standup draft on screen, ask for a real edit in your own words — e.g.
   "change the yesterday section to say I ran the quarterly review"
2. Check: the draft actually changes, and the change matches what you asked
3. Ask for something inapplicable ("make it more purple") — check you get an honest
   "unchanged" answer, not a false "I've updated your standup"
4. Try the instant forms too: "add blocker: waiting on legal", "remove [some line]",
   "start over" (should genuinely restart the interview, not re-show the same draft)

### Test Walk 3: Keyless first contact ([#1818](https://github.com/mediajunkie/piper-morgan-product/issues/1818)) — needs a keyless account

1. Before adding your LLM key (or after removing it in Settings): send "hi"
2. Check: you get a greeting-shaped acknowledgment plus one sentence about adding a key
   — friendly, short, no error-speak
3. Send "thanks" — check it does NOT say "you're welcome" (nothing has been done yet;
   it should say so)
4. Send a real request ("create an issue") — check the refusal names the key as the one
   missing thing and points at Settings

### Test Walk 4: Honest key errors ([#1414](https://github.com/mediajunkie/piper-morgan-product/issues/1414) no-regress)

1. Paste an invalid key in Settings → LLM Keys
2. Send a chat message
3. Check: the error talks about the key/provider honestly — not "Something unexpected
   happened" (if you see the generic message, that's [#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824) — report it with the exact wording)
4. Restore your real key and confirm chat works again

### Test Walk 5: Your key, your billing ([#1812](https://github.com/mediajunkie/piper-morgan-product/issues/1812) no-regress)

1. Note your provider dashboard's usage count (Anthropic console / OpenAI usage page)
2. Send a few chat messages
3. Check: the requests appear on **your** dashboard
4. If you test with two accounts with different providers: each account's chats hit its
   own provider, never the other's

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

Covered by Test Walks 1–2 above — that flow was rebuilt this release and is the single
most valuable thing to exercise. Also worth trying:

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

1. **GitHub Issues**: preferred for bugs (if you're comfortable with GitHub)
2. **Email**: xian@pipermorgan.ai for anything, including private feedback
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
- **Note**: data is not yet fully encrypted at rest (see `ALPHA_KNOWN_ISSUES.md`)

---

## Questions?

This is alpha software (version 0.8.13.0) — expect rough edges, and thank you for being
an early adopter. 🚀

---

## See Also

- `ALPHA_QUICKSTART.md` — the 2-minute version of Chapter 1
- `ALPHA_KNOWN_ISSUES.md` — current bugs and limitations
- `ALPHA_AGREEMENT_v2.md` — terms and conditions
- `VERSION_NUMBERING.md` — what 0.8.13.0 means
- `CONTRIBUTING.md` — running the code locally (engineers)

---

_Last updated: September 21, 2026_
_Software version: 0.8.13.0_
