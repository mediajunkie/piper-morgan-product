# DRAFT — Alpha Feature Guide v0.8.11 refresh (for PA claim-by-claim verification)

> **What this is**: Docs' mechanical draft of the v0.8.11 refresh of `docs/ALPHA_FEATURE_GUIDE.md`
> (currently stale at v0.8.6 / April 2026). Per the Docs/PA split agreed in PA's 2026-08-13 memo:
> Docs drafts from verifiable written sources with every capability claim tagged to its source;
> **PA verifies each claim against the live hosted alpha (alpha.pipermorgan.ai)** and flags
> (a) overclaims and (b) fragile-but-true claims, before anything replaces the live guide.
> This file does NOT replace `docs/ALPHA_FEATURE_GUIDE.md` — nothing ships until PA's pass.
>
> **Source-tag legend** (PA strips tags after verification):
> - `[RN 0.8.7]` `[RN 0.8.8]` `[RN 0.8.9]` `[RN 0.8.11]` — release notes in `docs/releases/`
>   (there are no 0.8.10.x release-notes files; v0.8.11.0's notes state the v0.8.10.x
>   curated-cherry-pick stamps are superseded and all content is on main)
> - `[README]` — `docs/README.md` "Current capabilities" (verified against pyproject/live 2026-08-12)
> - `[QUICKSTART]` — `docs/ALPHA_QUICKSTART.md` (v0.8.11.0, local-install path)
> - `[KNOWN-ISSUES]` — `docs/ALPHA_KNOWN_ISSUES.md` (v0.8.11.0)
> - `[BRIEFING]` — `docs/briefing/BRIEFING-CURRENT-STATE.md` (framing only, not capability claims)
> - `[decisions.log 2026-08-06]` — PM's #1481 Slack hold ruling,
>   `docs/internal/architecture/decisions/decisions.log`
> - `[v0.8.6 guide — RETEST]` — carried forward from the current v0.8.6 guide; least trustworthy,
>   retest every one of these against the live alpha
>
> **PA's next step**: work through each tagged claim against alpha.pipermorgan.ai; mark VERIFIED /
> OVERCLAIM / FRAGILE; the "PA: please check" list at the bottom collects the items Docs could not
> resolve from written sources at all.

---

# Alpha Feature Guide (v0.8.11)

**Version**: 0.8.11.0
**Last Updated**: August 2026

A guide to what Piper Morgan can do in the current alpha — what you can try, how to try it, and
what to expect.

The alpha is **hosted at [alpha.pipermorgan.ai](https://alpha.pipermorgan.ai)** and is
**invite-only** `[BRIEFING]`. If you have an invite, you sign in there — no local install needed.
(Running your own instance is still supported; see "Running locally" below `[QUICKSTART]`.)

This is **alpha software**. Expect bugs, use test data only, and report what you find —
see [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) for what we already know about.

---

## What's changed since the last guide (v0.8.6, April 2026)

The product has moved through five releases since the April guide. The short version:

- **The conversational floor matured** — unmatched questions get real LLM answers grounded in your
  context (blocked items, active sprint, recent activity) instead of canned templates `[RN 0.8.7]`.
- **A full files experience** — search, preview, tags, drag & drop, bulk download `[RN 0.8.7]`.
- **Radar became the primary workspace** — your work items, standup, and conversations in one live
  feed (the nav item formerly called "History"/"Documents") `[RN 0.8.8]` `[RN 0.8.9]`.
- **Bring your own key (BYOC)** — you supply your own LLM API key; it's stored per-user and
  encrypted at rest `[RN 0.8.8]` `[RN 0.8.9]`.
- **An honesty pass across the whole product** ("Piper stops lying") — honest answers when a data
  source fails, honest error messages for key problems, no false capability denials, session
  memory of what you actually did `[RN 0.8.11]`.

---

## Getting set up (hosted alpha)

1. **Sign in** at [alpha.pipermorgan.ai](https://alpha.pipermorgan.ai) with your invite `[BRIEFING]`.
2. **Add your LLM key**: Settings → LLM Keys. Your key and provider choice are per-user — your
   default provider and authorized list are yours alone, and one user's setup cannot pin the
   instance to their provider `[RN 0.8.11]`. Keys are encrypted at rest (AES-256-GCM) `[RN 0.8.9]` `[README]`.
3. **Answer the personality questionnaire** — it shapes Piper's warmth, confidence, and level of
   detail. If you answered it before v0.8.11, answer it once more: prior answers were lost to a
   migration bug and were unrecoverable `[RN 0.8.11]`.
4. **Connect integrations**: Settings → Integrations. Asking Piper in chat ("connect my GitHub")
   also gets you real setup guidance pointing at that page `[RN 0.8.11]`.

You're responsible for your own API costs `[QUICKSTART]`.

---

## Core: Chat with Piper

The main interface. Type naturally and Piper responds.

Piper uses a two-layer approach `[v0.8.6 guide — RETEST]`:

1. **Canonical handlers** run first for specific actions — creating a GitHub issue, completing a
   todo. These execute deterministically when they have what they need.
2. **The conversational floor** handles everything else: an LLM answering in Piper's voice with
   your real context assembled into the prompt `[RN 0.8.7]`.

**What the floor is grounded in**: your blocked items, active sprint/milestones, recent GitHub
activity, and calendar/deadlines `[RN 0.8.7]`.

**Things to try:**

| Category | Examples | Source |
|----------|----------|--------|
| Orientation | "What can you do?" "How do you work?" — answered directly, not deflected | `[RN 0.8.8]` |
| Status | "What's blocking me?" "Status of [project]?" | `[RN 0.8.7]` |
| Todos | "List my todos" / "add a todo: X" / "complete todo 1" | `[v0.8.6 guide — RETEST]` `[QUICKSTART]` |
| Actions | "Create a GitHub issue about X" "Summarize issue #N" | `[RN 0.8.7]` `[RN 0.8.11]` |
| Follow-ups | "it" / "that" resolve across turns; "update the title" resolves to the issue you just created | `[RN 0.8.7]` `[RN 0.8.11]` |
| Session memory | "What did we create this session?" — recalled from a real activity ledger | `[RN 0.8.11]` |
| Self-knowledge | "What have you learned about my work style?" — confidence-sectioned insights (known honesty gap: #1216) | `[RN 0.8.7]` `[KNOWN-ISSUES]` |

**Honesty discipline** — the floor is designed to say so rather than fabricate:

- If a data source fails, Piper says "I couldn't check your todos just now" — never a false
  "no pending tasks" `[RN 0.8.11]`.
- Greetings don't swallow your question: "Hi! How do I address you?" gets the question answered;
  only pure pleasantries get the short greeting `[RN 0.8.11]`.
- LLM-key problems (missing, invalid, out of quota) surface an honest message about the key, not
  "Something unexpected happened" `[RN 0.8.11]`.
- Piper won't claim it can't do things it can (file uploads, reminders — both real) `[RN 0.8.11]`,
  and won't claim an action succeeded when the write isn't wired `[RN 0.8.11]`.

**If you catch Piper inventing data or claiming false success, that's a bug worth reporting** —
it's the failure mode we care most about `[RN 0.8.7]`.

---

## Radar — your primary workspace

Radar is the default workspace panel: a live feed of the objects Piper tracks for you
`[RN 0.8.8]` `[README]`.

- **Work items**: GitHub issues assigned to your configured handle surface as live entities —
  your queue, not the whole repo `[RN 0.8.8]` `[RN 0.8.9]`.
- **Standup**: your daily standup appears as a first-class Radar entry alongside issues and work
  items `[RN 0.8.9]`.
- **Naming note**: if you tested earlier builds — "History", "Documents", and "Collections" were
  renamed; Radar is the work feed, Lists is the plain list surface `[RN 0.8.8]` `[RN 0.8.9]`.

Known wrinkle: the conversation picker sometimes loads the most recent chat regardless of which
one you selected (#1418) — re-select or refresh `[KNOWN-ISSUES]`.

---

## Morning standup

Piper assembles an honest standup from live sources — connector data, Radar sources, and your
context — with explicit provenance rather than hallucinated progress `[RN 0.8.9]` `[README]`.

- Ask in chat ("give me my standup") or find it in Radar `[RN 0.8.9]`.
- "I couldn't check X" is the designed behavior when a source fails — a confident claim built on a
  failed lookup is the bug `[RN 0.8.11]`.

---

## Home

- The home chat is a full-height conversation — input anchored at the bottom `[RN 0.8.8]`.
- Ambient modules (recently, insights, work items) can be collapsed or dismissed individually;
  the state persists `[RN 0.8.8]`.
- The compose UI autosaves drafts as you type `[RN 0.8.8]`.

---

## Lists, Todos, Projects

All three offer create/view/edit/delete from their nav pages, plus sharing
`[v0.8.6 guide — RETEST]`:

- **Todos via chat are real and persist** — create, list, complete conversationally `[QUICKSTART]`
  `[KNOWN-ISSUES]`. List/todo metadata persists correctly as of 0.8.11 (previously silently
  discarded on save) `[RN 0.8.11]`.
- **Sharing** by email with viewer/editor/admin roles `[v0.8.6 guide — RETEST]`.
- Data is owner-scoped — searches and defaults can't leak across users; owner-scoping was
  tightened in 0.8.11 `[RN 0.8.11]`.
- Heads-up for API users: the REST `/api/v1/todos` endpoints still return mocked data (#1427) —
  use chat or the UI pages `[KNOWN-ISSUES]`.

---

## Files

Full file management on the Files page `[RN 0.8.7]`:

- **Upload**: drag & drop anywhere on the page, multi-file `[RN 0.8.7]`. PDF, DOCX, TXT, MD, JSON
  up to 10MB `[v0.8.6 guide — RETEST]`.
- **Search + filter**: by name, by type; tags are searchable `[RN 0.8.7]`.
- **In-browser preview** without downloading `[RN 0.8.7]`.
- **Bulk download**: checkbox-select, download as zip `[RN 0.8.7]`.
- **Tags**: freeform tag chips per file `[RN 0.8.7]`.
- **Provenance badge**: every file shows where it came from — "Generated by Piper" or
  "Uploaded" `[RN 0.8.8]`.
- Files are user-isolated — you only see your own `[v0.8.6 guide — RETEST]`.

---

## Integrations

**Where**: Settings → Integrations. Asking in chat ("connect my GitHub") points you there with
real instructions `[RN 0.8.11]`.

When an integration isn't configured, Piper tells you honestly rather than silently failing or
guessing `[RN 0.8.9]`. Connector configuration is stored in the database and survives restarts
`[RN 0.8.9]`.

### GitHub

- **Reads**: issue summarization from live issue + comment data `[RN 0.8.7]`; Piper resolves your
  configured default repo, settable in the GUI or conversationally `[RN 0.8.7]` `[BRIEFING]`.
- **Writes**: issue creation with confirmation, close/reopen with fuzzy matching `[RN 0.8.7]`.
- **"My work" scoping**: Radar shows issues assigned to your configured handle `[RN 0.8.8]`.
- **Connection method**: OAuth first, presented as "Recommended," with a personal access token
  (PAT) field as a fallback below it `[PA code-level 08-13, origin/main: templates/settings_github.html +
  settings_integrations.py /github/connect + /github/save, both wired to the live Settings page;
  RN 0.8.9's "OAuth not started" is stale]`.

### Google Calendar

- Listed as a current integration `[README]`; calendar/deadline data feeds the floor's context
  `[RN 0.8.7]`. A real OAuth flow exists in the shipped code `[PA code-level 08-13, origin/main:
  services/integrations/calendar/oauth_handler.py]`; the end-to-end schedule query ("what's on my
  calendar?") remains unverified live `[v0.8.6 guide — RETEST]`.

### Notion

- Listed as a current integration `[README]`; real page-append (no demo-fallback fabrication)
  `[RN 0.8.7]`. **Connection method: a pasted Notion API key** (`secret_…`, from your own Notion
  integration) via a Settings card — not OAuth `[PA code-level 08-13, origin/main: templates/settings_notion.html]`.
  Page creation / search / document analysis behavior remains v0.8.6-era `[v0.8.6 guide — RETEST]`.

### Slack — mostly HELD, read this

**The Slack DM / @-mention path is HELD from the alpha (and from beta and any release) by PM's
security ruling of 2026-08-06** `[decisions.log 2026-08-06]`. The socket-mode inbound path bound
every Slack sender to the connector owner's identity — any workspace member DMing the bot could
act as the owner. The feature is held until it is built safely; rebuilding it correctly is high
priority, not abandoned `[decisions.log 2026-08-06]`.

**Do not expect to drive Piper from Slack in this alpha.** Earlier release notes (0.8.7/0.8.8)
described Slack inbound as working; the hold supersedes them.

---

## Personalization

- **Personality questionnaire**: shapes Piper's warmth, confidence, and depth. Working again as of
  0.8.11 — re-answer once if you answered before then `[RN 0.8.11]`.
- **Learning system**: Piper surfaces what it's learned about your work style, with confidence
  levels and an invitation to correct it; it can also proactively surface insights (mutable per
  session in natural language) `[RN 0.8.7]`. Known honesty gap in "what have you learned" answers:
  #1216 `[KNOWN-ISSUES]`.
- **Suggestion provenance**: ask "why did you suggest that?" — suggestions can explain themselves
  `[RN 0.8.7]` `[BRIEFING]`.

---

## Security & privacy

| Data | Protection | Source |
|------|-----------|--------|
| Your LLM API keys | Per-user, encrypted at rest (AES-256-GCM, per-field key derivation) | `[RN 0.8.9]` `[README]` |
| Passwords | Bcrypt-hashed | `[KNOWN-ISSUES]` |
| Sessions | JWT tokens; seamless refresh | `[RN 0.8.7]` `[KNOWN-ISSUES]` |
| Your content | Owner-scoped access control, tightened in 0.8.11 | `[RN 0.8.11]` |
| Ethics boundaries | Denials route through the floor in Piper's voice | `[RN 0.8.7]` |

**Not yet protected**: general content/PII at rest is not encrypted — **use test data only**
`[KNOWN-ISSUES]`. Multi-tenancy completeness work continues (#1241) `[KNOWN-ISSUES]`.

---

## Running locally (alternative to the hosted alpha)

Self-hosting remains a supported path — clone the `production` branch and follow
[ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) (20–50 min first-time setup; Docker, Python 3.11/3.12,
your own API key) `[QUICKSTART]`. Local-install specifics that do NOT apply to the hosted alpha:

- CLI commands (`python main.py status` / `setup` / `preferences`) `[QUICKSTART]`
- The macOS-keychain limitation for locally stored credentials `[RN 0.8.9]`
- The stripped-env-vars server-launch caveat (#1258) `[KNOWN-ISSUES]`

---

## Where to focus your testing (0.8.11)

Straight from the release's own testing focus `[QUICKSTART]`:

- **Questionnaire → tone**: re-answer it, then chat — does the tone actually reflect your answers?
- **Your own provider**: set your key + provider in Settings → LLM Keys — does chat use YOUR
  provider? (Check your provider's usage dashboard.)
- **Greeting + question**: "Hi!" plus a real question — does the question get answered?
- **Connect guidance**: "connect my github" — real guidance, not a decline?
- **Honest status claims**: ask for status/agenda/standup — "I couldn't check" is correct on
  failure; a false "nothing found" is a bug.
- **Session recall**: create an issue in chat, then "what did we create this session?"

**How to report**: WHAT I TRIED / WHAT I EXPECTED / WHAT HAPPENED / ERROR MESSAGE →
[GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues/new) or reply to your
onboarding email `[KNOWN-ISSUES]`.

---

## See also

- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — setup (hosted testers: mostly N/A; self-hosters: start here)
- [ALPHA_KNOWN_ISSUES.md](ALPHA_KNOWN_ISSUES.md) — current limitations, workarounds
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — what to test and how to give feedback
- [Release Notes](releases/) — per-release changelogs

---
---

## PA: please check — STATUS after PA's code-level pass (2026-08-13)

> **Verification-layer note** (PA's framing, kept because it's exactly right): PA's seat has no
> browser, so items below marked *code-level* were verified by reading the shipped `production`
> source — a real but weaker layer than live observation: it proves the code path exists and what
> it does, not that a tester experiences it correctly. Four items are now specific enough that a
> ~5-minute live click-through (PM has browser + hosted access) closes them: (a) GitHub Settings
> shows OAuth-recommended + PAT-fallback, (b) Notion's field is a pasted API key, (c) whether the
> /standup page renders and is worth mentioning, (d) an eyeball of the "Where to focus your
> testing" tone/honesty claims.

1. ~~**GitHub connection method on hosted**~~ **RESOLVED code-level, high confidence (PA 08-13)**:
   OAuth presented first and labeled "Recommended" (#1317, ADR-070 C), PAT kept as fallback below.
   Folded into the GitHub section; RN 0.8.9's "OAuth not started" is stale.
2. **Google Calendar end-to-end**: *partially advanced* — a real OAuth flow exists in shipped code
   (PA 08-13: `oauth_handler.py`, #537/#577); the live "what's on my calendar?" query remains
   unverified. (Briefing frames GCal completion as RECONNECT R2 / #1441.)
3. **Notion connection method**: ~~unknown~~ **RESOLVED code-level (PA 08-13)**: pasted Notion API
   key via a Settings card, not OAuth. Page-creation/search behavior still needs live check.
4. ~~**Slack outbound**~~ **RESOLVED, narrow (PA trace + Docs dispatch-grep, 08-13)**: the
   inbound hold's flag (`slack_inbound_enabled()`) is scoped to inbound only, and the outbound
   path isn't gated by it — but the ONLY caller of `slack_domain_service` anywhere in services/
   is `standup_workflow_skill.py`, and no intent/action handler exposes a generic "send this to
   #channel." So outbound Slack exists as standup-posting, not as a general tester action. The
   guide's "don't expect to drive Piper from Slack" stands; no broader claim is safe.
5. ~~**Sharing lists/todos/projects**~~ **CONFIRMED all three surfaces (PA code-level 08-13,
   origin/main)**: `/share` endpoints with viewer/editor/admin roles on lists/todos/projects
   (SEC-RBAC Phase 2/3). Tester-facing "share by email" is accurate (the UI field is labeled
   "Email or User ID" even though the wire format is user_id). Live two-account behavior still
   unwatched, but the surface exists as claimed.
6. ~~**Integration health dashboard**~~ **CONFIRMED CUT (PA 08-13, code-level)**: no "Test All"
   surface anywhere in app code — only an internal Grafana ops dashboard and a 2025 gameplan doc.
   The omission stands as a deliberate cut, not a maybe.
7. **`/standup` and `/help` chat slash-commands**: v0.8.6-era; omitted. Note the slash-command
   surface was being normalized in Aug 2026 (decisions.log) — check what actually exists.
8. **Standup access points**: *factually advanced (PA 08-13, code-level)*: `GET /standup` still
   renders (`web/api/routes/ui.py:366`) — the route was downgraded in emphasis, not removed.
   Remaining question is editorial, not factual: mention it to testers or steer to chat/Radar only?
9. **Accessibility section**: the v0.8.6 guide claimed WCAG 2.1 AA, keyboard nav, screen-reader
   landmarks. RN 0.8.8 adds px→rem. I omitted the section rather than carry an unverified
   compliance claim — restore only if someone can attest it.
10. **Hosted signup flow**: is the invite flow "click link → create account" (invite-token gate,
    #1344 arc) — and does the questionnaire appear during onboarding or only in Settings? The
    setup steps in "Getting set up" are assembled, not observed.
11. ~~**File upload size/format limits**~~ **CONFIRMED exact (PA code-level 08-13, origin/main)**:
    `web/api/routes/files.py` — `MAX_FILE_SIZE = 10MB`, extensions {.txt, .pdf, .docx, .md, .json}.
    The v0.8.6 numbers hold verbatim.

### Deliberately omitted (found in sources, judged not safe to claim)

- **Reminders** ("set a reminder"): RN 0.8.7 ships "minimum-viable reminders" (#903) and RN 0.8.11
  removed the false denial — but no source describes what a tester can actually expect a reminder
  to DO (notify how? where?), so I left it out of the feature list.
- **Gemini as a BYOC provider**: the quickstart's setup wizard lists OpenAI/Anthropic/Gemini for
  local install; no source confirms which providers the hosted Settings → LLM Keys accepts.
- **Compose UI as a named feature**: autosave is claimed (RN 0.8.8) under Home, but I couldn't
  establish where/what "compose" is for a tester today.
- **"Recently" panel details** (RN 0.8.7 #1194): folded into the Home ambient-modules line rather
  than claimed separately.
- **Trust-gating / proactive-skills line from README**: "proactive skills surface when invited;
  consequential actions require explicit confirmation" — kept only implicitly (issue-creation
  confirmation), since I couldn't map the general claim to a concrete tester-visible behavior.
