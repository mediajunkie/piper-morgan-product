# Task-loaded procedures for every Piper: candidate list (#2358)

*CIO, 2026-11-13 (combined with PPM's list the same evening), after xian accepted Arch's revised tier boundary (Exec 01M7BW10QM). This is a proposal and nothing ships from it. #2358's acceptance says "PPM and CIO propose; xian or Exec confirms the first few". PPM adds to this list or cuts from it. Each confirmed item is rewritten in user register (never copied), goes through CXO's voice pass and the #2356 leak checks, and must meet #2357's H4: at most 1,500 tokens, loading on at least 90% of matching turns and at most 10% of others.*

## What's already shipped (no new work)

`piper-draft-issue`, `piper-draft-spec`, `piper-sprint-plan`, `piper-stakeholder-update`, `piper-synthesize-feedback`, `propose-feature`, `trust-check`, `compost-review`, `update-piper`.

## How the candidates were picked

I read the 36 entries in `.claude/skills/` (35 skills plus the runbook) and kept a skill only if all three hold:
1. A person running their own product work would ask for it in their own words.
2. Its useful core doesn't depend on the team's machinery (mail, session logs, duty cycles, the blog pipeline).
3. It carries a Proven practice from `docs/tier1/practice.md`, so the procedure and the teachable row agree.

The source size is the team skill's `SKILL.md` size. Each rewrite has to fit in 1,500 tokens (about 6,000 bytes), so the large ones are cut to their core.

## Combined with PPM's list (#2358 comment, 11-13 18:00)

PPM and I picked the same seven team skills independently. On the first three:
- We agree on `close-issue-properly` and `discovered-work-capture`.
- PPM's third is `cohort-attention-rollup`, "what needs my decision?". Mine was `query-github-board`.
- I take PPM's. "What needs my decision?" is a question a person actually asks, and the earlier draft of this page was wrong to fold it into `piper-stakeholder-update`, which faces outward. Its source is 38,154 bytes, so the rewrite keeps only the core: sort the open items into needs you, drift and fine, after checking each against live state.
- `query-github-board` may be better as a code guard than a procedure (PPM). That's Arch's call, so it stays a candidate.

**Proposed first three:** `cohort-attention-rollup`, `close-issue-properly`, `discovered-work-capture`. The person's own GitHub connector already serves all three.

## Task-shaped Proven entries (CIO's half)

Most Proven entries are conduct, so they belong in the conduct layer (#2354) and the practice rows. These four have a task shape: a person asks Piper to run them, with steps and an output. None has a team skill behind it, so each would be written new from its practice row.

| Procedure (user's words) | Proven entry | What Piper does | Practice row |
|---|---|---|---|
| **"Let's do a quick retro on this"** | 00 | Asks what went well, what didn't, and the one or two things to do differently, then writes them where the person will see them before the next similar piece of work. | Write down what you'd do differently |
| **"Get everyone's view before we decide"** | 22 | Drafts a short question for each person or area, collects the answers separately (it never shows one answer to the next person), then sets the views side by side with where they agree and differ. | Hear everyone before you merge views |
| **"What should we build and what should we reuse?"** | 26 | Goes through a plan or spec piece by piece and marks each as ordinary plumbing (reuse or buy, naming what exists if known) or the thing that makes the product different (build). | Build what makes you different, reuse the rest |
| **"We're automating this step, what are we losing?"** | 41 | Before a step is automated, lists what people do by hand around it today (checks, notes, who gets told), and asks which of those the automation keeps, which need writing down, and which are being dropped on purpose. | When you add automation, look at what it replaces |

Of these, I'd put the retro first. It's short, fits well under 1,500 tokens, and pairs with `compost-review`, which already ships.

## All other candidates

| Procedure (user's words) | From team skill | Note |
|---|---|---|
| "Check this draft's facts before I send it": each number, name and claim traced to a source, or marked unverified | `narrative-verification` (the fact-check core only) | Carries "Read it before you rely on it". Pairs with `piper-stakeholder-update`. |
| "How many are open / where does the sprint stand?": counted from the board, paged to the end, "N of M" | `query-github-board` | Procedure or code guard: Arch's call. |
| "Are the docs still true after this release?" | `doc-sync-sweep` | Only for people whose docs are in a connected repo. |
| "Check the plan against the issue before we start" | `audit-cascade` | 10,041 bytes, so it needs a hard cut. |
| "Move these tickets to the next sprint without breaking the board" | `assign-sprint-safely` | Held until Piper has a write tool for board fields. Before then it would describe something Piper can't do (conduct rule 4). PPM lists it as not a candidate, and I agree for now. |

## Left out, and why

| Team skills | Why |
|---|---|
| `check-mailbox`, `create-session-log`, `create-omnibus`, `deliver-mail`, `duty-cycle-tick`, `cleanup-dev-active`, `update-current-state` | They run the team's own machinery. |
| `draft-blog-post`, `draft-weekly-ship`, `continue-narrative`, `publish-to-blog`, `update-calendar`, `template-audit` | The project's own publishing pipeline and voice. |
| `brief-coding-agent`, `ab-a-isolation`, `delete-module-safely`, `cut-release` | Engineering inside this codebase. |
| The `piper-*` skills, `propose-feature`, `trust-check`, `compost-review`, `update-piper` | Already shipped. |

## Open points

- **Who writes each rewrite.** I'd draft each from the team skill, since the practice rows are already in user register. CXO voice-passes, and Arch or Lead says how a procedure is registered so it loads on matching turns.
- **Overlap with the practice rows.** A procedure says what Piper does on the task, and a practice row says what Piper teaches when asked. Where both carry the same practice, the wording should agree, as with the conduct layer.

Verified how: listed `.claude/skills/` at origin/main 11-13 (35 skills plus `SKILL-CREATION-RUNBOOK.md` and `SKILLS.md`) and read each skill's description line. Sizes are `wc -c` of each `SKILL.md`. #2358's acceptance and Arch's boundary table were read in full this hour. Not checked: how Piper registers and loads a shipped procedure today. That's Arch's or Lead's read, and it decides whether H4's load rates can be measured.
