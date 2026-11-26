---
status: scaffold
kind: user release note (not a blog post)
issue: 2439
window: 2026-10-31 to 2026-11-25 (beta builds)
owner-of-words: xian
scaffold-by: Comms, 2026-11-26
---

# What changed: first entry (SCAFFOLD, for xian's words)

**What this is.** Facts for the first entry of a user-findable release note (issue 2439, from F12 in the 10-23 Production map review; gate: public beta). It isn't prose. xian picks the lines and words them; Comms fact-checks the result. Where it lives and how users reach it are Web's and CXO's call.

**Reader.** A beta user who last used Piper a few weeks ago. What would they notice?

**Sourcing.** Every line below comes from the beta build line in `docs/briefing/BRIEFING-CURRENT-STATE.md` at the briefing commit named, read at that commit, plus the issue title. Comms checked 6 of the cited commits against their lines on 11-26 and all 6 matched. Comms then checked all 31 issue-to-line pairs used below: 31 of 31 match. The full list (63 user-visible issues, 22 excluded) is summarized in the 11-26 Comms log.

**Before anything goes out: a served check on every line used.** Each row says what its build line said about a signed-in check: **read served**, *not checked yet*, or *silent*. Only 2415, 2416, 2418 and 2419 have a recorded served read. Every line xian keeps gets a served check first (Comms asks Web for the signed-in reads, or reads it in the seat browser). That's the rule for public copy: claim only what the product does today, checked where users see it.

**Copy holds that apply.** No data-ownership claim (PDR-102). No backup or data-safety claim (#2157 is open). Invitations are on hold (PDR-008), so this goes to users who already have access, through HOST's Readiness lane if it's mailed at all.

---

## Candidate lines, grouped by what a user notices

### 1. Piper says so when it couldn't check (the honesty work)

Suggested heading idea only: "When Piper can't check, it says so."

| What a user notices | Issue | On beta from | Briefing source · what the line says about a served check |
|---|---|---|---|
| A failed GitHub read is said once, with one cause, not repeated in different words | 2417 | 11-22 | d65a32983e · line: not read signed in yet |
| If the GitHub connection has gone stale, chat says what to do next instead of a success-styled message | 2188 | 11-04 | 5fab886b61 · line silent |
| Closing or reopening an issue when GitHub can't be reached says why and doesn't ask a question it can't act on | 2437 | 11-25 | 1f097d6494 · line silent |
| When Piper answers with words instead of making a change, it no longer records that as done | 2399 | 11-25 | 68c08bf8c9 · line silent |
| Asking how a project is going with GitHub down gets one GitHub line plus the project's todos, not a guess | 2415, 2416 | 11-23 | 73f5462725 · **read served** (e1a803b8ba) |
| "What integrations do I have?" names only what this beta offers. Slack and Notion aren't offered as available | 2418, 2419, 2245 | 11-22 (2245 from 11-01) | 4ac9cbc159, 2511ab06f7 · **read served** for 2418, 2419 (64237d7642); 2245 line silent |

### 2. Todos and projects

| What a user notices | Issue | On beta from | Briefing source · what the line says about a served check |
|---|---|---|---|
| "add a task: …" adds the todo, and adding one is confirmed in a single sentence | (no #), 2427 | 11-23 | 73f5462725, e1a803b8ba · line: served reads asked of Web |
| "Add a task to <project>" attaches it to that project | 2297 | 11-20 | cbb8f46f51 · line: not checked signed in |
| Asking for todos by project, without naming one, gets "which project?" | 2413 | 11-22 | 753429f2e0 · line: not read signed in yet |
| "Complete them" with nothing specific asks which one and completes nothing | 2328 | 11-10 | f1ef65ae51 · line silent |
| Todos list in priority order (high first) and are called todos, not reminders | 2293, 2219 | 11-06 | b08488b10a · line silent |
| Adding a project with a name you already use is caught | 2314 | 11-06 | 5f1ed96404 · line silent |

### 3. Integrations page and GitHub connection

| What a user notices | Issue | On beta from | Briefing source · what the line says about a served check |
|---|---|---|---|
| The GitHub card says which GitHub account is connected | 2279 | 11-04 | 5fab886b61 · line silent |
| Disconnecting GitHub revokes Piper's access at GitHub too, and the disconnect line says what stays valid there | 2178, 2407 | 11-05, 11-19 | 7345cb9808, 2e360ec153 · 2178 line silent; 2407 line: not checked signed in |
| A stale GitHub connection shows a reconnect line on its settings page | 2430 | 11-24 | 2a140c9b19 · line silent |
| A failed Test shows a reason, and a card that couldn't be checked keeps that reason | 2401, (no #) | 11-17, 11-18 | 0aab4847b7, e817c1fefa · line: not checked signed in |
| GitHub connects through the published GitHub App | 2342 | 11-12 | 43ec0dbed8 · line silent |

### 4. Account, setup and error pages

| What a user notices | Issue | On beta from | Briefing source · what the line says about a served check |
|---|---|---|---|
| One password rule at sign-up, reset and change, stated in full on the page | 2438 | 11-25 | 022b7ab879 · line silent |
| Account Settings shows your email | 2259 | 11-04 | 1dd5e261d9 · line silent |
| The beta's address is beta.pipermorgan.ai; the old alpha address forwards there | 2282 | 11-05 | a946e416b9 · line silent |
| Refused requests show a plain page or sentence, not raw server text | 2431, 2432, 2433 | 11-24 to 11-25 | 8fd8546ab6, dfb970c177, 68c08bf8c9 · line silent |
| Error messages ("Failed to…") are rewritten in plain words | 2434 | 11-25 | 68c08bf8c9 · line silent |
| The LLM keys page no longer offers a Gemini key | 2366 | 11-13 | 9c705a10dd · line: served rows are open |

---

## Hold: don't claim these until a served check says so

The build line itself says these weren't checked by a signed-in user yet, or the line is too thin to word a claim from.

- 2374, 2375, 2376 (GitHub App repositories, the install step, the token form). Line: "Their served rows are open." The connector half also needs xian's MCP deploy.
- 2274 (Anthropic key step: subscription vs API access), 2268 (setup wizard's repo line), 2271 (archive pick's created date), the todo cap line, 2294 (no-reminders statement). Line: "served rows are open."
- 2345 (sign-in state kept across restarts): the served read is xian's F.4 connect.
- 2379, 2414: line says "Not checked signed in" / "Not read signed in yet".
- 2315, 2316 (todo picks by name): line says only "go out in the 07:00 window" on 11-07; no later line confirms the promotion.
- 2333, 2367, 2368, 2386, 1551, 2283, 2288: the line's wording is too thin to say what a user sees.

## Questions for xian

1. Audience and timing: publish the note only at the public beta (F12's gate), or give current beta users this first entry now?
2. Shape: one entry for the whole window, grouped as above, or dated entries per week?
3. Voice: does the honesty group lead? Users would feel it most, and it's the Production sprint's point.
