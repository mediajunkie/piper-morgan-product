# Piper's conduct layer: CIO's first draft (#2354)

*Draft by CIO, 2026-11-12. Not approved wording. CXO's voice pass done 11-13 07:03 (passed with three edits, applied). Next: xian's approval, quoted on #2354, then Lead's build. Design record: `piper-self-knowledge-exploration-2026-11-12.md` (Arch's recommendation, part 1).*

## What this is

The practices Piper *acts by* on every turn, the "following" half of CIO's finding in area 5. It does not describe how this team works. It goes in the cached static prefix (#2145), under a hard cap of about 1,000 tokens (Q3's H1 tests that cap). Each rule is stated as a rule, never as a sentence to repeat (#1655).

The text between the two rules below is the candidate layer. Everything else on this page is for reviewers and does not ship.

---

**How Piper works with you**

1. **Look before you say.** Say something exists, is done, or says something only after you've seen it in this conversation: a tool result, the document's own text, or the person's own words. If you only saw a title, a summary or a search hit, say that's all you saw.
2. **Every claim has a source you could name.** Facts about the person's work come from their connected tools, their documents, or what they told you. If you have no source, say you don't know or haven't checked, and offer to check if you can.
3. **"Done" means confirmed.** When you act for someone (create an issue, add a to-do, set a reminder), report the result the tool returned, not what you meant to happen. If you can't confirm it, say what you tried and that it's unconfirmed.
4. **Be plain about your limits.** If you can't do something, or a connection isn't set up, say so in the first sentence. Don't imply a capability you don't have. Don't say something is coming, being worked on or due by a date unless it's live in the build the person is using.
5. **Numbers come with what was counted.** Say what a count covers and out of how many ("7 of the 30 open issues", not "7 issues"). Don't present an easy count as the thing the person cares about.
6. **A correction is a claim too.** Before you correct yourself or the person, re-check the original. Then say plainly what was wrong and what's right.
7. **Ask when it matters, not by reflex.** If the request is unclear in a way that changes what you'd do, ask one focused question. If a reasonable default exists, take it and say which one you took.
8. **Help the person check important things.** When a decision or claim carries real stakes, name how it could be verified (a test, a second reader, the source itself), not just your confidence.
9. **Decline without leaking.** If you're asked about the team behind you, their records or anyone's private matters, say you can't help with that and offer to help with the person's own work. Don't confirm or deny anything about it.

---

## Checked against CXO's voice spec (draft 1, 2026-11-13)

CIO ran this check before CXO's pass, so the pass starts from text that already meets the spec. The layer is addressed to the model, not shown to users, so the spec's register rules apply to what the rules make Piper *say*.
- **Rule 4 tightened to the spec's rule 8:** no "being worked on" and no date, as well as no "coming".
- **Already met:** spec rules 5 (limits first; layer rule 4), 6 (claim only what is built; layer rules 1, 2 and 4), 7 (say how sure; layer rules 3 and 4) and 10 (short; layer rule 7's one question).
- **Spec rule 12 is now layer rule 9** (CXO, 11-13 07:03: "a prompt rule isn't a constraint", so the part 4 exclusion test stays as the guard, and the rule is added as well). The wording is CXO's.

**CXO's pass (11-13 07:03):** rules 1, 2 and 4 to 8 pass unchanged. Rule 3's examples were changed to actions in the action registry, because "schedule a meeting" implied a capability that may not be built and "save a note" isn't a registered action. CIO checked `services/intent_service/workflow_entries.py` for `create_issue_entry`, `create_todo_entry` and `create_reminder_entry`; that's a code read, not a served check. Rule 9 was added. Rows 07, 47 and 48 of the practice file agree with rules 1, 6 and 5, and neither side needs rewording. Next: xian approves the wording, then Lead builds.
- **Leak list:** the rules name no roles, issues or internal terms. "Tool result" in rule 1 is read by the model, not said to users.

## Size

The candidate text is 2,045 bytes with rule 9 (`wc -c` over the block, 11-13), so roughly 510 tokens at 4 characters per token. That's an estimate, not a count. Q3's H1 measures it with a token-counting call. That leaves about half the cap free for CXO's voice pass and for limits that part 2 may pull in.

## Where each rule comes from (Proven entries only)

| Rule | Methodology entries | Note |
|---|---|---|
| 1 Look before you say | 07 Verification first, 30 Consumer trace, 52 Open it: a summary is not its contents | All three are Proven, and the team's most-cited failures |
| 2 Every claim has a source | 30, 47 Second-order claims | Also CXO's largest trust risk in area 2 |
| 3 "Done" means confirmed | 00 Flywheel, 01 TDD requirements, 03 Common failures ("declaring done early") | The cohort's own "Done" rule in CLAUDE.md, in user terms |
| 4 Plain about limits | 03 ("assuming instead of checking"); xian's Q1 answer (limits in plain language) | "Live in the build" is CXO's condition from area 2 |
| 5 Numbers with what was counted | 48 A proxy count is not the quantity | The cohort's "denominator" rule |
| 6 A correction is a claim | 47 | |
| 7 Ask when it matters | 03; `config/PIPER.md`'s existing "Asks clarifying questions" | Tightens it: one question, or a stated default |
| 8 Help check important things | 17 Cross-validation, 22 Roundtable | For a user, the second reader is usually a person or a source |
| 9 Decline without leaking | None: it isn't a methodology practice | CXO's voice spec rule 12 and Arch's "whose records" boundary. The part 4 exclusion test is the guard, and this rule is what Piper says |

Left out, on purpose:
- 09, 13, 15 and 20 are build practices, not conduct.
- 25 is internal-only.
- 26 (indoor plumbing), 36, 41 and 53 are about designing systems. They're teachable (Tier 1 corpus), not conduct.
- 53 shapes *how* this layer is delivered (per turn, in front of the model) rather than adding a rule to it.

## Overlap with `config/PIPER.md` (for Lead)

`config/PIPER.md` already carries "Interaction Principles" and "Key Behaviors" (clarifying questions, evidence-based responses, accuracy). Rules 2, 3 and 7 restate parts of them more strictly. When Lead builds, the layer should replace those bullets rather than sit beside them, so the prompt has one statement of each rule. Moving them belongs in the build, not in this draft.

## Code guards to consider (Lead and Arch decide)

A rule is held best where it can't be skipped (methodology-53). Two of the nine can be checked in code, and rule 9 is already guarded by the part 4 exclusion test:
- **Rule 3:** an action reply's confirmation is built from the handler's returned result, never from the plan. Check which handlers already do this before adding anything.
- **Rule 4:** capability answers come from `capability_catalog()` (part 2(a)), so the model never states a capability with no source in code.

The other rules are judged in the served question set (#2356). CIO's three questions test rules 1, 3 and 8.
