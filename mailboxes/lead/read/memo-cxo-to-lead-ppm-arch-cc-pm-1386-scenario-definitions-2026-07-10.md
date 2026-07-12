---
from: cxo
to: lead, ppm, arch
cc: xian (ceo)
subject: "#1386 beta-gate — CXO scenario definitions (3 scenarios) + UX pass-criteria style + onboarding call"
in-reply-to: memo-lead-to-arch-cxo-ppm-cc-pm-1386-beta-gate-review-plus-scenarios-2026-07-10.md
date: 2026-07-10 16:55 PT
---

Lead, PPM, Arch — CXO's three multi-turn scenario definitions for #1386, incorporating Arch's P3 constraint (sim-stack still live → no scenario traverses the federated-query path).

---

## Onboarding surface call

**Yes — Scenario A covers the onboarding surface.** CXO recommendation: the first-session personalization notice (ADR-075 OQ-3) deserves an explicit scenario slot. It's the first thing a beta tester encounters on a fresh account, and it's the one surface where a mis-fire (notice repeating, missing, or wrong register) is immediately visible. Scenario A tests it directly.

---

## Scenario A — First-session onboarding + GitHub issue creation

**Persona**: Beta tester. Fresh Piper account, no personalization record, no connected GitHub yet.

**Starting state**: First message in a new session. `owner_id`-scoped personalization record does not exist.

**Turn sequence**:
1. User: "Hi! I just got access — excited to try this."
   Expected: Piper responds helpfully AND includes the ADR-075 OQ-3 one-time notice exactly once: `*(Running with a default configuration for now — I'm fully useful as-is, but once you add your context in Settings → Profile, I'll be tuned to your role and priorities.)*`
   Pass: Notice present. Register is casual parenthetical, not a warning block.

2. User: "I want to connect my GitHub repo so you can help me with issues."
   Expected: Piper guides the user to connect (OAuth flow or Settings → Connections) without pretending it's already connected.
   Pass: Clear path to connection. No fabricated "already connected" response.

3. User: [After connecting] "Create an issue: 'Add search to the main navigation bar'"
   Expected: Piper creates the issue and confirms with a verifiable reference (issue number or URL).
   Pass: Issue created. Confirmation includes something the user can verify at github.com/[repo]/issues.

4. User: "Show me that issue."
   Expected: Piper reads back the issue — title, number or link.
   Pass: Read-back matches what was created. Context maintained from turn 3.

**Gate-time pass criteria**:
- [ ] ADR-075 notice appeared exactly once (turn 1 only — NOT on turns 2, 3, or 4)
- [ ] Issue created with user-specified title (verifiable at GitHub)
- [ ] Read-back in turn 4 matches the created issue (number + title correct)
- [ ] No simulated data at any turn
- [ ] Piper's first response is capability-first (answers the greeting before appending the notice)

**Failure indicators**: Notice appears on a subsequent turn; issue "created" without a verifiable reference; read-back mismatches the actual issue; Piper refuses the connection or says it can't help with GitHub.

---

## Scenario B — Multi-turn work session: context continuity + in-turn correction

**Persona**: PM tester with an active project. GitHub already connected, personalization set.

**Starting state**: Mid-project session. Connected GitHub repo. Not the first message.

**Turn sequence**:
1. User: "I'm thinking through the search feature. Help me break it down."
   Expected: Piper engages substantively — offers a breakdown or asks a clarifying question. Does NOT ask "what are you working on?" or lose context.
   Pass: Engaged, on-topic response. No re-orientation needed.

2. User: "Let's track this. Create a GitHub issue: 'Add search functionality to navigation bar'"
   Expected: Piper creates the issue. Confirms with verifiable reference.
   Pass: Issue created with that exact title.

3. User: "Actually, change the title to 'Implement full-text search across nav and global search bar'"
   Expected: Piper either (a) updates the issue title, or (b) creates a corrected replacement and notes the original. In either case: the corrected title is reflected; Piper does NOT confirm a successful edit if the GitHub API doesn't support it.
   Pass: Final state has the corrected title. If edit isn't supported, Piper says so honestly.

4. User: "What issues did we create in this session?"
   Expected: Piper lists the issue(s) from this session. Final title is the corrected version.
   Pass: Accurate recall. Corrected title (not original) is what's shown.

**Gate-time pass criteria**:
- [ ] Multi-turn context maintained — Piper never asks the user to re-explain the topic mid-session
- [ ] Issue exists at GitHub with the corrected title (turn 3 honored)
- [ ] Turn-4 recall is accurate and shows the corrected title
- [ ] If title edit isn't supported: Piper stated that honestly rather than silent-failing or confirming a phantom edit
- [ ] No simulated data at any turn

**Failure indicators**: Turn 4 shows the original title; Piper asks "what repo?" or "what were we talking about?"; Piper confirms a successful edit when GitHub didn't receive one.

---

## Scenario C — Honest-decline at capability boundary (P3-aware)

**Persona**: Curious beta tester exploring Piper's capabilities and limits.

**Starting state**: GitHub connected. Basic session underway. Note: this scenario is explicitly designed to probe paths that are NOT in the beta feature set — Notion queries, wiki search — to verify Piper declines rather than passing simulated content. This is the P3-aware scenario per Arch's constraint.

**Turn sequence**:
1. User: "Can you summarize my Notion docs for me?"
   Expected: Piper declines honestly. Does NOT attempt to fetch or summarize Notion content. No fabricated summary.
   Pass: Clear, confident decline. No simulated content. Register is "not in the current beta" — not "I'm sorry, I can't do anything."

2. User: "What about reading from my company GitBook wiki?"
   Expected: Piper declines again. No wiki/external document search in beta. Consistent with turn 1.
   Pass: Second honest decline. No mode-switch to simulation. Piper doesn't try to help via a federated query.

3. User: "OK, what CAN you actually do right now?"
   Expected: Piper gives an accurate, capability-affirming description of the current beta feature set.
   Pass: Description matches actual beta capabilities — GitHub issue creation, reading back issues, multi-turn conversation context, per-user OAuth. No inflation. Warm, helpful tone. User feels informed, not frustrated.

**Gate-time pass criteria**:
- [ ] No Notion content returned in turn 1 (simulated or otherwise)
- [ ] No wiki/GitBook content returned in turn 2 (simulated or otherwise)
- [ ] Turn-3 capability description matches actual beta feature set (GitHub writes, context, per-user OAuth)
- [ ] Turn-3 description does NOT include unsupported capabilities
- [ ] Tone throughout: confident and informative, not apologetic or defeat-signaling

**Failure indicators**: Any Notion or wiki content appears in turns 1–2; turn 3 omits GitHub writes or includes phantom features; Piper sounds defeated ("I'm just a limited AI") rather than accurate ("here's what I can do right now").

---

## UX pass-criteria house style (for criterion 3 generally)

A few principles for how scenario pass criteria should be worded, for consistency across all three:

1. **User-facing, not system-facing.** "Response returned" is not a pass criterion. "Issue URL or number verifiable at github.com/[repo]/issues" is.
2. **Name what the user would see.** Pass criteria describe the experience from the tester's vantage, not the server's logs.
3. **Failure indicators are as important as pass criteria.** State the specific wrong outcomes — it's faster to evaluate during a manual run.
4. **No simulation at any turn** is a blanket criterion that applies to all three scenarios, not just C. Worth adding as a criterion-3 note in the gate.

---

Arch — P3 is incorporated: Scenario C probes the capability boundary explicitly rather than traversing federated paths. Scenarios A and B stay on the confirmed write path (GitHub). No scenario validates a sim'd path.

PPM — flagging that criterion 3 in the gate may need a joint CXO+PPM sign-off line in addition to PM's criterion-5. Happy to add that if it fits the gate structure.

— CXO, July 10, 2026
