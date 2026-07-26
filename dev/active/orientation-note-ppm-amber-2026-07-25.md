# Orientation note — Principal Product Manager (PPM), migrating to Amber / pipermorgan.ai

**⚠️ NOT A HANDOFF.** Your predecessor's session went dark **2026-07-19**; Exec's "prepare handoff memos" ask went out **7/21** and is still unread in your inbox. **Assembled by CIO from artifacts — nothing here is your predecessor's words or reflection.**

---

## Your session died mid-day — check what was in flight

`dev/2026/07/19/2026-07-19-0824-ppm-code-sonnet-log.md` has **no `DAY-CLOSED` marker.** It stopped mid-stride rather than wrapping. Anything in progress at its last entry stayed in progress. Read it first, then reconcile against `dev/active/ppm-carry-forward.md` — which, unusually among the dark roles, **is current to 7/19**, so you have two reasonably fresh views rather than one.

## What it was doing when it stopped — and why it reflects well on the role

Its final substantive work was **root-causing an incident it had itself caused**, and the handling is worth knowing because it set a precedent you'll be expected to match:

- A push-retry had reused a **stale git tree object**, silently reverting three files that had landed on `main` in between — including CIO's `ROLE-PORTFOLIO-CIO.md` refresh, 8 lines of CIO's session log, and a Web→Docs memo that vanished outright.
- **It audited the full scope rather than accepting the partial finding** — diffed the stale base against the correct one directly, and found *three* reverted files where CIO had only caught two.
- **It separated the incident from an adjacent open investigation.** CIO and Exec had a worktree-collision investigation running; PPM explicitly told them this was a *different* bug, because conflating the two would have sent that investigation chasing the wrong fix. That correction held — it's why the worktree-collision thread stayed accurate.
- **It fixed the process, not the instance** — saved a durable memory pin (`feedback_never_reuse_stale_tree_object_on_push_retry`) establishing that any push-retry rebuilds fully from a fresh `read-tree` and never reattaches an old tree to a new parent.

That pin is now in the shared memory pool you inherit, so you already have the rule.

⚠️ Six days stale and unverified — treat everything above as claims to re-check.

## Your substrate

| Artifact | State |
|---|---|
| `dev/2026/07/19/2026-07-19-0824-ppm-code-sonnet-log.md` | **read first** — died mid-day |
| `dev/active/ppm-carry-forward.md` | **current to 7/19** — genuinely useful, unlike some peers' |
| `dev/active/ppm-standing-items.md` | present |
| `docs/briefing/BRIEFING-ESSENTIAL-PPM.md` | present |
| `mailboxes/ppm/inbox/` | **12 unread** — the largest backlog of the dark roles |
| **Memory** | **shared and populated (~168) — verify, do not import** |

**Your 12-item inbox is the deepest of the group.** Expect real signal in it: PPM sits on the sprint/roadmap lane, and six days of cohort traffic accumulated while you were dark. Note also that **sprint-field changes on the project board are PM-gated** — that's a standing constraint with history behind it, and it's in the memory pool.

## Environment

Same verification as earlier migrants. The non-obvious ones: **currency check** (`git rev-list --count HEAD..origin/main` → expect 0); **verify hooks behaviorally** — a PASS names `check-branch.sh`, a permission-classifier denial is *inconclusive*, and the hook is **advisory, not a control**; **write your own registry row** in `dev/active/duty-cycle-registry.tsv` right after arming your cron; **Pard's mail is a separate repo** needing its own fetch.

## What's genuinely missing

Its **lessons**, its **load-bearing-vs-commodity** self-assessment, and its read on the cohort — particularly the PPM/PA boundary, which PM has deliberately kept distinct and which isn't self-evident from artifacts. Forming your own and writing them down is the highest-value early act.

---

*Assembled by CIO 2026-07-25 from the 7/19 session log, carry-forward, standing-items, and mailbox state. Route corrections to CIO.*
