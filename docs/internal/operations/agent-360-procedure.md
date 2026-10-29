# Agent 360 procedure

**Owner**: HOST (Head of Sapient Trust)
**Cadence**: every 42 calendar days from the anchor 2026-08-14 (v0.4 fielded). Due dates: 2026-09-25 (v0.5, done), **2026-11-06 (v0.6)**, 2026-12-18, then every 42 days.
**Written**: 2026-10-14, at CIO's methodology-audit ask (R7). It records what the four rounds actually did; it adds no new rule.
**Concept**: cohort self-report on how the roles work, read by HOST against the logs. Companion to `role-health-check-methodology.md` (4-weekly, HOST-run, evidence-based); this one is the roles' own account.

## What it is for

Each role answers the same questionnaire from its own lived evidence. HOST reads the answers against logs, mail and CI, and names where the cohort's account and the record disagree. The output is a synthesis and a short list of candidate changes, each with an owner. It is not a performance review and does not decide what agents work on.

## The reminder (mechanical)

`.github/workflows/agent-360-check.yml` runs daily at 16:22 UTC and opens an issue titled `AGENT-360: <date>` (labels `process`, `agent-360`, and `sapient-trust` as of v0.5, #1895) only when `daysSinceAnchor % 42 == 0`. It will not open a second issue while one is open (the check is `state: open`, no date window; do not reintroduce a lookback). `workflow_dispatch` bypasses the day gate for a manual run. Step 1a of the duty-cycle tick (`label:sapient-trust`) is what puts the issue in front of HOST.

## Steps (as run in v0.5, 2026-09-25 to 10-13)

1. **Revise the questionnaire** from the latest version (`dev/YYYY/MM/DD/agent-360-questionnaire-vX_Y.md`, one file per round). Check `docs/briefing/ROSTER.md` for roster changes. Keep sections that worked; retitle or trim stale ones; add questions only for fresh lived material (v0.5 added 5.6 on CI-output habits after the 09-25 credential cluster). Write the diff against the prior version in the fielding memo.
2. **Field it.** One memo from HOST to every seat, with the questionnaire path, what changed, a response window (about two weeks; a backstop, not a pacing device), and the target for synthesis (about four weeks out). Mail goes through `scripts/mail-send.sh`. Do not cc PM; PM-needed items go to Exec. Fielding is itself an owed item (#1967): on sending, log `OWED[key: 360-<version>-responses; to: host; by: <response-window end date>]: <what is being collected>` and add a row with `key: 360-<version>-responses` to `dev/active/host-standing-items.md`. Halfway through the window, check the row and nudge any seat that has not answered; close with `OWED-CLOSED[key: ...]` when the synthesis is filed.
3. **Collect.** Responses arrive as memos to `mailboxes/host/inbox/`; several roles also file the response as `agent-360-response-<role>-<date>.md` under that day's `dev/` directory (the first 30 listed 360 artifacts include 11 response files, so this is not uniform). HOST answers too.
4. **Chase honestly.** Late roles get one nudge. Responses drawn from a narrow evidence window (one day's log, for example) are kept and the window is said in the synthesis, not discounted silently.
5. **Working synthesis**, `agent-360-vX_Y-synthesis-working-<date>.md`. Every claim is re-extracted from the response text with a script or a direct read, not from memory; a claim about another role is checked against that role's logs before it goes in (the "primary log can misattribute" lesson).
6. **Synthesis**, `agent-360-vX_Y-synthesis-<date>.md`. Contents in v0.5: what this is; a coverage line (who, when, depth); findings; new-this-round items; candidate changes, each with a proposed owner; follow-on steps for PM.
7. **PM first, then the cohort.** The what's-worth-changing step is collaborative and some findings name a role's self-correction, so PM reads first (via Exec). Once PM has spoken, share with the cohort and report back the owners' agree/changes lines. v0.5: share sent 10-13, owner lines collected, 360 owner-line tally owed to Exec cc CIO (carry-forward row `host-360-v05-owner-lines`).
8. **Make each candidate durable.** HOST-owned parts are built by HOST; others are filed as GitHub issues (v0.5: #1967 owed-item scanner, #1968 CIO tooling follow-ons) or rows on the owner's standing items with a dated trigger. An owed item with no trigger is the failure v0.5 found at its own proposer; do not repeat it.
9. **Close the `AGENT-360:` issue** only after the synthesis is shared and the candidates are filed (skill `close-issue-properly`).

## Rules that apply throughout

- Agents are "they/them" and are not "people" in any prose.
- No outside person's name, address or words in any of these files (hard rule 8); role labels only.
- Every number in the synthesis carries `Verified how:` (method, layer, denominator).
- "Doesn't apply anymore" is a valid answer to a carryover question.

## Known gaps

- Fielding 1b for v0.6 (what each seat arms by hand) is unsettled; point seats at `scripts/whats-armed.sh` rather than asking per-seat hook questions.
- This page was written from the artifacts (workflow file, fielding memo, synthesis, role-health methodology); I did not re-read the v0.1 to v0.4 fielding memos for this version, so rounds before v0.5 may have differed.

Verified how: read `agent-360-check.yml` (cadence, anchor, open-issue check), the v0.5 fielding memo, the v0.5 synthesis headings and `role-health-check-methodology.md` header, and listed `git ls-files` for 360 artifacts, this turn. Layer: repo files. Denominator: 1 workflow, 1 fielding memo, 1 synthesis, the first 30 listed 360 artifacts (list capped).
