# #1386 criterion 3: scenario A/B/C refresh against the current product (CXO, 2026-10-07)

Baseline: my 2026-07-10 definitions (`mailboxes/cxo/sent/memo-cxo-to-lead-ppm-arch-cc-pm-1386-scenario-definitions-2026-07-10.md`) and the 07-12 joint sign-off. This file lists what changed since, turn by turn, so the run uses scripts that match the shipped product. Everything marked **[source]** I read in this worktree's source this fire; everything marked **[live]** can only be settled by the browser lane on the deployed artifact and is unverified until then. No venv or browser on this seat; nothing here was executed.

## What changed (and what did not)

| Turn | July script | Today | Action |
|---|---|---|---|
| A1 | Greeting; pass = the ADR-075 notice text `*(Running with a default configuration for now — I'm fully useful as-is, but once you add your context in Settings → Profile…)*` appears exactly once | **[source]** That text was cut by my 2026-09-08 ruling. The notice is now `(Running with a default configuration — nothing here needs setting up first.)` (`personalization_service.py:81-83`). It fires once per non-PM account (`has_seen_personalization_notice`). | **Rewrite the pass literal.** The old text appearing would be a failure (a stale deploy). Keep "exactly once, turn 1 only". |
| A1 | Cold account, no integration | **[source]** Two first-exchange surfaces exist now: the first-contact demo (#1536; fires only with a connector and a resolvable repo, so it should NOT fire on a cold account) and the FTUX interview (#1688; flag `PIPER_FTUX_INTERVIEW`, default OFF per its HOLD). | Add a pre-check: **[live]** record whether the interview flag is on in the deployed env. If ON, A1's reply is the interview opening ("I don't have anything of yours in front of me yet — nothing's connected." + the question), not a greeting reply, and the pass criteria change. If OFF, A1 is as written. |
| A2 | "Connect my GitHub": guide to OAuth or Settings → Connections | **[live]** Unverified what the chat reply says today; my 10-06 link/connect wording is a proposal not yet in code. | Keep the turn. Pass = a clear path, never "already connected". Record the literal reply. |
| A3 | "Create an issue: '…'" with no repo named | **[source]** Repo resolves explicit, then user default, then read-time recovery that searches the tester's repos and picks a default (#1590, `repo_resolver.py`). Create-issue is an explicit imperative, so the collaborate gate (#1510) lets it execute. | **Add a pass criterion: the reply names the repo the issue landed in**, and the issue is verifiable in THAT repo. A tester with several repos can otherwise create an issue somewhere they did not choose and not know it. **[live]** Record which repo was picked and whether the reply says so. If it does not, that is a finding, not a pass. |
| A4 | "Show me that issue." | **[live]** unchanged expectation. | Keep. |
| B1 | Breakdown help, no re-orientation | Unchanged. | Keep. |
| B2 | "Let's track this. Create a GitHub issue: '…'" | **[source]** Explicit imperative executes (#1510). | Keep. Same repo-named criterion as A3. |
| B3 | Re-scoped in July to the explicit form "change the title of issue #107 to…" because the implicit form hit #1394 | #1394 is closed. | **Run the ORIGINAL B3: "Actually, change the title to '…'" (implicit reference)** as first written. Also run the July explicit form as B3b if time allows; the pair separates "can't resolve what 'the title' refers to" from "can't edit". **[live]** This is the turn most exposed to the Phase 3 target-resolution rewrite. |
| B4 | Re-scoped to "show me issue #107" | #1394 closed. | **Run the ORIGINAL B4: "What issues did we create in this session?"** Pass = lists this session's issue(s) with the corrected title. |
| C1 | "Can you summarize my Notion docs for me?" | The invitation now names GitHub only; Slack and Google are out too. | Keep C1 and C2. **Add C2b: one probe at a connector the invitation does not name and that exists in code (Slack or Google Calendar).** The decline must hold for every connector the invitation omits, and these are the two a tester is most likely to try. |
| C2 | "What about my company GitBook wiki?" | Federated queries stay OUT (#1322 scope constraint, unchanged). | Keep. |
| C3 | "OK, what CAN you actually do right now?" Description must match the beta feature set | **[live]** The shipped feature set has changed (reminders and to-dos, the clear/delete family, GitHub read/write, projects). | **Rewrite the C3 pass list from the current feature set at run time** and compare the reply against it. "Does NOT include unsupported capabilities" stays the hard criterion, and the new one: it must not omit or misdescribe GitHub-only connectors. |

## Pass-criteria additions (house style: user-facing, not system-facing)

1. A1: the notice is the new literal, once, and not on turns 2 to 4.
2. A3 and B2: the confirmation says which repository the issue went into, and the issue is verifiable there.
3. B3 (original): the corrected title is reflected at GitHub, or Piper says honestly it could not do it. A reply that says "done" while GitHub shows the old title fails.
4. C2b: no content from, and no pretense of access to, a connector the invitation does not name.

## Scope guards (unchanged)

No scenario traverses federated MCP queries (#1322). The known-issues list in the invitation (connectors, Radar pinned after a chat completion #1946, iPad layout #1907) is not tested here and a tester seeing those is not a scenario failure.

## Owed to run this

- Web's browser lane on the deployed artifact (blocked on PM's go for the alpha test login; item 9 on PM's list).
- The two **[live]** pre-checks before turn 1: the interview flag state, and which repo a fresh OAuth account resolves to.
- A frozen build for the window.

Verified how: read my 07-10 scenario memo in full; read `personalization_service.py:70-90,200-225`, the `first_contact.py` docstring and interview flag (`:337-350`), the `collaboration_gate.py` docstring, and the `repo_resolver.py` decision tree. Layer: source only, not a served reply. Denominator: the 11 scripted turns in A, B and C; I did not trace each turn through the live router, which is what the **[live]** marks are for.
