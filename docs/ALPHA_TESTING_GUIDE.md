# Piper Morgan Alpha Testing Guide

**Version**: 0.8.14.0
**Last Updated**: September 23, 2026
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
- **[What's New in 0.8.14](#whats-new-in-0814)** — your preferences persist, every clock face is on your zone and labeled, the agenda shows real times, one-line add-project, honest GitHub-write outcomes
- **[What to Test in 0.8.14](#what-to-test-in-0814)** — priority test walks for this release
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

This is pre-release alpha software (version 0.8.14.0). By proceeding, you acknowledge:

1. **Expected Issues**: bugs, rough edges, and incomplete features are normal
2. **Data Loss Risk**: your data on the alpha instance may be lost at any time
3. **No Production Use**: do NOT use it for mission-critical or time-sensitive work
4. **API Charges**: you are responsible for all LLM API costs your key incurs
5. **Security**: not security audited — use test data only, no sensitive information
6. **No Warranty**: provided "as-is", without any warranty whatsoever
7. **No Support SLA**: best-effort support only, no guaranteed response times

See `ALPHA_AGREEMENT_v2.md` for complete terms.

---

## What's New in 0.8.14

v0.8.14.0 is the "On Your Clock" release — a fast follow to v0.8.13.0, cut two days later,
and the first release deployed to the consolidated host (alpha.pipermorgan.ai has been
served by Fly since 2026-09-22 — the one-time re-login you were asked for was that move;
your data came across intact).

**Your preferences survive restarts** ([#1574](https://github.com/mediajunkie/piper-morgan-product/issues/1574)):

- Timezone, reminder settings, working mode, and the calendar-setup offer used to live in
  server memory and silently reset on every deploy — the "why does it keep asking me?"
  class. They now persist per user.

**Every clock face is yours, and labeled** ([#1576](https://github.com/mediajunkie/piper-morgan-product/issues/1576), [#1575](https://github.com/mediajunkie/piper-morgan-product/issues/1575), [#1577](https://github.com/mediajunkie/piper-morgan-product/issues/1577), [#1556](https://github.com/mediajunkie/piper-morgan-product/issues/1556)):

- Standup exports, the agenda, and "what's my day look like" answers render in **your**
  timezone with the zone shown ("3:00 PM PDT") — never a bare "4:27 PM" and never the
  server's UTC clock.
- "Today" and "yesterday" are your calendar days; free-time blocks are computed on your
  clock. After 5pm Pacific you no longer get tomorrow's day.
- The agenda had been printing "TBD" for everyone with a connected calendar — a key
  mismatch, not a missing meeting. Fixed, and the "Focus Time Available" section is
  reachable again.

**Add a project in one line** ([#1856](https://github.com/mediajunkie/piper-morgan-product/issues/1856)):

- `add project One Job with repo Design-in-Product/one-job` creates and links the project
  in one turn. Leave the name out and Piper tells you the exact line to type and how to
  cancel — never the same canned question twice.

**Honest outcomes on GitHub writes** ([#1858](https://github.com/mediajunkie/piper-morgan-product/issues/1858)):

- Closing an issue that doesn't exist now says *"There's no issue #99999 in owner/repo —
  nothing was changed"* instead of *"it may or may not have gone through"*. The uncertain
  wording is reserved for genuinely unverifiable cases.

**Fixes and honesty, continued**:

- The preferences pages work again ([#1864](https://github.com/mediajunkie/piper-morgan-product/issues/1864)) — every `/api/v1/preferences/*` route had
  errored since its auth dependency landed.
- One "Add to Slack" path instead of four ([#1499](https://github.com/mediajunkie/piper-morgan-product/issues/1499)).
- One valid key from any provider is enough to start, and a bad key gets one of four
  specific explanations ([#1823](https://github.com/mediajunkie/piper-morgan-product/issues/1823), [#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824) — shipped in 0.8.13, first deployed here).
- Counts tell the truth: a list that hit the API page cap reads "100+", never an invented
  exact number ([#1778](https://github.com/mediajunkie/piper-morgan-product/issues/1778)).

See [Release Notes v0.8.14.0](releases/RELEASE-NOTES-v0.8.14.0.md) for full details, and
[releases/README.md](releases/README.md) for prior release history (v0.8.13.0's "Nothing
Invented, Nothing Borrowed" notes cover the standup-interview rebuild this release inherits).

---

# Chapter 2: Testing

This chapter covers what to test and how. If you're already set up, **start here**.

## What to Test in 0.8.14

Time and persistence are the focus — every clock face was audited and 27 of 50 were
wrong or unlabeled. **Is every time on YOUR clock? Do your settings stay set? Does the
agenda show real times?** (0.8.13's standup walks still apply — they're in
[releases/README.md](releases/README.md)'s history if you want to re-run them.)

### Test Walk 1: Your timezone, everywhere ([#1576](https://github.com/mediajunkie/piper-morgan-product/issues/1576), [#1577](https://github.com/mediajunkie/piper-morgan-product/issues/1577))

1. Under Settings → Preferences, set your timezone (pick one that is NOT UTC)
2. Ask "what time is it for me?" — check the answer names your zone ("PDT", not bare)
3. Export or view a standup — check every timestamp carries a zone label and matches
   your clock
4. If you can, test after 5pm Pacific: ask "what's on today?" — check "today" is YOUR
   date, not tomorrow's (UTC has already rolled over)

### Test Walk 2: Preferences persist ([#1574](https://github.com/mediajunkie/piper-morgan-product/issues/1574))

1. Change a preference (timezone, reminder time, working mode) and dismiss the
   calendar-setup offer if it appears
2. Log out, log back in — still set?
3. Come back after the next deploy (or tomorrow) — still set? The offer stays dismissed?
   If anything reset, that's the bug this release claims to have fixed — report exactly
   which setting.

### Test Walk 3: Agenda shows real times ([#1576](https://github.com/mediajunkie/piper-morgan-product/issues/1576), [#1575](https://github.com/mediajunkie/piper-morgan-product/issues/1575)) — needs a connected Google Calendar

1. Connect Google Calendar under Settings → Integrations (note: the connect flow itself
   still redirects via the old host, [#1852](https://github.com/mediajunkie/piper-morgan-product/issues/1852) — if it fails, report it and skip this walk)
2. Ask "what's my agenda today?"
3. Check: meetings show real times in your zone — never "TBD"
4. Check: a "Focus Time Available" section appears with free blocks that end at YOUR
   end of day (18:00 in your zone), not the server's

### Test Walk 4: Add a project in one line ([#1856](https://github.com/mediajunkie/piper-morgan-product/issues/1856))

1. Say `add project Test Project with repo <your-github-user>/<a-repo-you-own>`
2. Check: one turn — created and linked, with a confirmation naming both
3. Say `add project with repo <owner>/<repo>` (no name) — check Piper gives you the exact
   line to type and how to cancel, and doesn't ask the same canned question twice
4. ⚠️ Known: if Piper *asks* "Want me to add it now?" and your "yes" goes nowhere, that's
   [#1855](https://github.com/mediajunkie/piper-morgan-product/issues/1855) — use the imperative one-liner instead and report the wording you saw

### Test Walk 5: Honest GitHub writes ([#1858](https://github.com/mediajunkie/piper-morgan-product/issues/1858))

1. With GitHub connected: "close issue 99999 in <owner>/<repo>" (a number that doesn't
   exist)
2. Check: *"There's no issue #99999 in owner/repo — nothing was changed"* — not "may or
   may not have gone through", and nothing else in the repo touched
3. Ask a question-shaped one — "did issue 42 get closed?" — check it READS, never closes
   ([#1794](https://github.com/mediajunkie/piper-morgan-product/issues/1794))

### Test Walk 6: Honest key errors ([#1823](https://github.com/mediajunkie/piper-morgan-product/issues/1823), [#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824))

1. Paste an invalid key in Settings → LLM Keys, send a chat message
2. Check: one specific sentence about the key/provider — not "Something unexpected
   happened" (if you see the generic message, report the exact wording)
3. Restore your real key and confirm chat works again — with only ONE provider's key set,
   chat should still work ([#1823](https://github.com/mediajunkie/piper-morgan-product/issues/1823))

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

This is alpha software (version 0.8.14.0) — expect rough edges, and thank you for being
an early adopter. 🚀

---

## See Also

- `ALPHA_QUICKSTART.md` — the 2-minute version of Chapter 1
- `ALPHA_KNOWN_ISSUES.md` — current bugs and limitations
- `ALPHA_AGREEMENT_v2.md` — terms and conditions
- `VERSION_NUMBERING.md` — what 0.8.14.0 means
- `CONTRIBUTING.md` — running the code locally (engineers)

---

_Last updated: September 23, 2026_
_Software version: 0.8.14.0_
