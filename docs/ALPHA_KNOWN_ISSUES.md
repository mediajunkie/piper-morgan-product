# Alpha Known Issues (v0.8.14.0)

**Version**: 0.8.14.0
**Last Updated**: September 23, 2026

This document helps alpha testers avoid wasting time on things we already know about.

v0.8.14.0 is the "On Your Clock" release — a two-day fast follow to v0.8.13.0 and the
first release deployed to the consolidated host (alpha.pipermorgan.ai is Fly-served since
2026-09-22). Your preferences persist, every clock face is in your zone and labeled, the
agenda shows real times, projects add in one line, and GitHub writes report honest
outcomes. What's below are the rough edges that remain.

## Known Issues in 0.8.14 (the honest list)

- **Piper may *offer* something it can't then do** ([#1855](https://github.com/mediajunkie/piper-morgan-product/issues/1855) — design under review). The floor can write "Want me to add X now?" without arming anything, so your "yes" goes nowhere and you get an honest "no result" instead. Workaround: say the imperative form yourself (e.g. `add project X with repo owner/repo`). Report the exact offer wording — each instance feeds the fix.
- **Switching chats flashes the whole page white** ([#1859](https://github.com/mediajunkie/piper-morgan-product/issues/1859), [#1515](https://github.com/mediajunkie/piper-morgan-product/issues/1515)) — cosmetic but jarring; Web is tracing it. Nothing is lost.
- **"do a standup" / "let's do a standup" may not start the flow** ([#1860](https://github.com/mediajunkie/piper-morgan-product/issues/1860)) — "show my standup" and "let's do my standup" do. Each unrecognized phrasing you report becomes a corpus row.
- **Slack and Google *connect* flows redirect via the old host** ([#1852](https://github.com/mediajunkie/piper-morgan-product/issues/1852)) — connecting a new Slack workspace or Google Calendar from Settings may fail; already-connected integrations keep working. Report it and skip the calendar test walk if it bites.
- **Slack-side standup messages still show a raw timestamp** ([#1869](https://github.com/mediajunkie/piper-morgan-product/issues/1869)) — the web faces are fixed; the Slack fallback text isn't yet.
- **A short polite imperative can finalize a standup draft** ([#1843](https://github.com/mediajunkie/piper-morgan-product/issues/1843)): "please remove the fluff" can be mis-read as an acceptance. Workaround: phrase edits without a leading "please", or say "start over".
- **After adding a key in Settings, the chat you just started can be hard to find again** ([#1838](https://github.com/mediajunkie/piper-morgan-product/issues/1838)) — open History and pick it; nothing is lost.
- The REST `/api/v1/todos` endpoint is still mocked ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427)) — chat and UI todos are real.

---

## Fixed in 0.8.14

If any of these still happens to you, that's a regression — please report it:

- **[#1574](https://github.com/mediajunkie/piper-morgan-product/issues/1574)** — Preferences (timezone, reminders, working mode, calendar-setup offer state) persist across restarts and deploys.
- **[#1791](https://github.com/mediajunkie/piper-morgan-product/issues/1791)** — The Personality Preferences page (warmth/confidence/action/technical-depth sliders) is per-user: your save lands in your own account, not a shared file, and no longer needs admin rights. If you never saved one, you get Piper's default voice, not silence. Answers saved under the OLD shared instance file before this release were NOT carried over to any account (there was no way to know whose they were) — re-save your sliders once. (This is separate from your questionnaire answers at onboarding, which were already per-account.)
- **[#1576](https://github.com/mediajunkie/piper-morgan-product/issues/1576) / [#1575](https://github.com/mediajunkie/piper-morgan-product/issues/1575) / [#1577](https://github.com/mediajunkie/piper-morgan-product/issues/1577) / [#1556](https://github.com/mediajunkie/piper-morgan-product/issues/1556)** — Every user-facing time is rendered in your zone with the zone named; "today" is your calendar day; free-time blocks are computed on your clock; the agenda's "TBD" (a key mismatch) and unreachable "Focus Time Available" are fixed.
- **[#1856](https://github.com/mediajunkie/piper-morgan-product/issues/1856)** — `add project <name> with repo <owner>/<repo>` works in one turn; a missing name gets the exact line to type, never the same canned question twice.
- **[#1858](https://github.com/mediajunkie/piper-morgan-product/issues/1858)** — Closing a nonexistent GitHub issue says "There's no issue #N in owner/repo — nothing was changed", not "may or may not have gone through".
- **[#1864](https://github.com/mediajunkie/piper-morgan-product/issues/1864)** — Every `/api/v1/preferences/*` route works again (they had errored since their auth dependency landed); the version footer resolves ([#1499](https://github.com/mediajunkie/piper-morgan-product/issues/1499)).
- **[#1823](https://github.com/mediajunkie/piper-morgan-product/issues/1823) / [#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824)** — One valid key from any provider is enough on web (was: Anthropic required); a bad key gets one of four specific sentences instead of "Something unexpected happened". Shipped in 0.8.13, first deployed here.
- **[#1778](https://github.com/mediajunkie/piper-morgan-product/issues/1778)** — Counts that hit an API page cap read "100+", never an invented exact number.
- **[#1794](https://github.com/mediajunkie/piper-morgan-product/issues/1794)** — "Close issue 42?" phrased as a question stays a read; the destructive rail is never reached from the query lane.
- **[#1499](https://github.com/mediajunkie/piper-morgan-product/issues/1499)** — One "Add to Slack" path instead of four; two dead links removed.

---

## Previously Fixed (0.8.13, September 21)

- **[#1837](https://github.com/mediajunkie/piper-morgan-product/issues/1837) / [#1836](https://github.com/mediajunkie/piper-morgan-product/issues/1836)** — Accepting the standup interview offer starts the interview; the placeholder draft is deleted; free-form edits genuinely apply; "I've updated your standup" only when something changed.
- **[#1818](https://github.com/mediajunkie/piper-morgan-product/issues/1818)** — A keyless "hi" gets a human acknowledgment plus one key sentence.
- **[#1812](https://github.com/mediajunkie/piper-morgan-product/issues/1812)** — Every LLM spend is the acting user's own key or an honest refusal; the server-key seam is deleted from the code.
- **[#1839](https://github.com/mediajunkie/piper-morgan-product/issues/1839)** — `/health` reports the real version, git SHA, and environment.
- **[#1418](https://github.com/mediajunkie/piper-morgan-product/issues/1418)** / **[#1105](https://github.com/mediajunkie/piper-morgan-product/issues/1105)** / **[#1216](https://github.com/mediajunkie/piper-morgan-product/issues/1216)** / **[#1256](https://github.com/mediajunkie/piper-morgan-product/issues/1256)** — Conversation picker loads the chat you clicked; Settings no longer demands a key re-paste; two honesty gaps in workstyle/stakeholder answers closed.

Older history (0.8.11's owner-scoping and honesty fixes: #1422, #1415, #1416, #1417, #1425, #1426, #1414, #1420/#1421/#1434, #1435) lives in [releases/README.md](releases/README.md) and each release's notes.

---

## Known Issues (by category)

### Blocking

_None currently at P0._

### Annoying (tester-facing)

| Issue | Description | Workaround |
|-------|-------------|------------|
| [#1855](https://github.com/mediajunkie/piper-morgan-product/issues/1855) | Piper offers an action it hasn't armed; "yes" goes nowhere | Say the imperative form; report the offer wording |
| [#1859](https://github.com/mediajunkie/piper-morgan-product/issues/1859) | Whole-page white flash on every chat switch | Cosmetic; nothing lost |
| [#1860](https://github.com/mediajunkie/piper-morgan-product/issues/1860) | Some standup-initiation phrasings don't start the flow | "let's do my standup" / "show my standup" |
| [#1838](https://github.com/mediajunkie/piper-morgan-product/issues/1838) | Just-started chat hard to find after adding a key | Open History and pick it |
| [#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164) | "Start private session" toggle in History is UI-only — no backend behavior | Cosmetic; don't rely on it |
| [#1498](https://github.com/mediajunkie/piper-morgan-product/issues/1498) | The live "Good afternoon" banner renders above historical conversations | Cosmetic |

### Security / multi-tenancy

| Issue | Description | Status |
|-------|-------------|--------|
| [#1241](https://github.com/mediajunkie/piper-morgan-product/issues/1241) | Some content not fully anchored to user auth — multi-tenancy completeness | Owner-scoping fixes shipped in 0.8.11 (#1420, #1421, #1434); broader completeness work continues. Use test data only. |

---

## Partially Complete

| Feature | Status | What Works | What Doesn't |
|---------|--------|------------|--------------|
| **Todos REST API** | Mocked | Chat todos are real and persist; Todos UI works | The `/api/v1/todos` REST endpoints still return mocked data ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427)) |
| **Slack** | Partial | Outbound, DMs, @-mentions, standup posts | Standup fallback text shows a raw timestamp ([#1869](https://github.com/mediajunkie/piper-morgan-product/issues/1869)); connecting a NEW workspace redirects via the old host ([#1852](https://github.com/mediajunkie/piper-morgan-product/issues/1852)) |
| **Google Calendar** | Partial | Agenda, free-time blocks, real meeting times (0.8.14) | Connecting a NEW calendar redirects via the old host ([#1852](https://github.com/mediajunkie/piper-morgan-product/issues/1852)) |
| **BYOC credentials** | Complete for chat | Keys stored per-user, encrypted at rest; per-request routing; any single provider suffices; save-time validation distinguishes a rejected credential from no-credits/billing, same honest copy as runtime chat errors ([#1718](https://github.com/mediajunkie/piper-morgan-product/issues/1718), fixed) | — |
| **Data encryption** | Partial | API-key secrets encrypted at rest; passwords bcrypt-hashed | Content/PII at rest not yet encrypted; use test data only |
| **GitHub OAuth** | Not started | PAT token auth works | OAuth connect flow planned for a future release |
| **History privacy toggle** | UI stub only | Toggle renders correctly | No backend — doesn't do anything yet ([#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164)) |

---

## Needs Testing

These shipped in 0.8.14 and need real-world validation:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Your timezone, everywhere** | Set a non-UTC zone; every time you see is labeled with it? "Today" is your date after 5pm Pacific? | Settings → Preferences, then chat / standup export |
| **Preferences persist** | Change a setting, log out/in, come back after a deploy — still set? Calendar offer stays dismissed? | Settings → Preferences |
| **Agenda real times** | Meetings show real times, never "TBD"? Focus blocks end at YOUR 18:00? | Chat: "what's my agenda today?" (needs a connected calendar) |
| **Add project in one line** | One turn with name + repo? Missing name → exact line to type? | Chat: `add project X with repo owner/repo` |
| **Honest GitHub writes** | Close a nonexistent issue — "nothing was changed"? | Chat with GitHub connected |
| **Honest key errors** | Bad key → one specific sentence, not "Something unexpected"? One provider's key alone works? | Settings → LLM Keys, then chat |
| **Invalid-key retest / OpenAI-only Slack** | PM's two pending rows on the test card ([#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824), [#1822](https://github.com/mediajunkie/piper-morgan-product/issues/1822)) | PM |

---

## What Works

- **Conversational AI**: LLM-grounded responses; greeting + question handled together; honest "I couldn't check" on source failures; honest key and GitHub-write errors; session recall; the standup interview and free-form edits
- **Time**: every face in your zone and labeled; agenda with real times and focus blocks
- **Todos, Lists & Projects**: chat todos real and persistent; one-line add-project; metadata persists; owner-scoped
- **Personalization**: preferences persist per user (#1574); questionnaire shapes tone (#1422); per-user provider selection, any one key suffices (#1415, #1823); per-user keys encrypted at rest
- **Files**: upload/download, in-browser preview, search, freeform tags, bulk download
- **Integrations**: GitHub connector reads and honest writes; Slack outbound, DMs, @-mentions; connect-setup guidance (#1417)
- **Core Infrastructure**: consolidated Fly host; multi-user with owner-scoped access; JWT auth with revocation that survives cache restarts (#1808); PostgreSQL, Redis, ChromaDB; smoke gate 534 green at cut

---

## In Progress / Next

- Armed floor offers ([#1855](https://github.com/mediajunkie/piper-morgan-product/issues/1855)) — design with Arch + CXO
- White-flash chat switching ([#1859](https://github.com/mediajunkie/piper-morgan-product/issues/1859), [#1515](https://github.com/mediajunkie/piper-morgan-product/issues/1515)) — Web tracing
- Post-cutover redirect URIs ([#1852](https://github.com/mediajunkie/piper-morgan-product/issues/1852)); droplet decommission ~2026-09-29
- Real `/api/v1/todos` REST surface ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427))
- Beta (0.9.0) is milestone-gated — it ships when the beta criteria are met, not on a calendar date

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
- [Release Notes v0.8.14.0](releases/RELEASE-NOTES-v0.8.14.0.md) — Full 0.8.14.0 changelog

---

_Last Updated: September 23, 2026_
