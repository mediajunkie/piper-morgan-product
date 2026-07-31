# CXO carry-forward — ephemeral session state

**Owner**: CXO | **Updated**: 2026-07-30 22:2x PT (STOP)
**Read at**: every fire START. **Rewritten at**: the end of every substantive fire.
**Durable owed/queued work lives in** `cxo-standing-items.md` — this file is *current* state only.

---

## ⏰ FIRST THING TOMORROW (Fri 07-31, 06:47 fire) — a locked, time-boxed commitment

**#1386 Scenario-B re-run sign-off.** Exec locked the window (`21:15` memo, 07-30):

- **Lead drives** the canonical suite + Scenario-B re-run from its ~06:17 fire.
- **I review Lead's Scenario-B outputs at my 06:47 fire and post sign-off — or objection —
  ON THE ISSUE (#1386), not in mail.** Exec: *"the gate's evidence belongs on the issue."*
- PPM does the same at 06:52. Same shape as the criterion-3 joint sign-off we did before.
- **Exec reports to PM at 08:32.** Sign-offs are wanted **by noon**.
- **I verify outcomes; I do not drive execution.**

**Scope discipline — do not overstate the result.** This window closes **criterion 2 + the
Scenario-B re-run** (verifying #1393 scaffolding-leak and #1394 turn-3 continuity, both In Review).
It does **not** close the gate — six criteria, this is one. Criteria 1/4/5/6 are PM's.
**Turn-4 ("what did we create") is still my scenario-vs-rescope design call** and is not resolved by
these fixes.

**Fallback**: if Lead's venv acceptance test fails Friday morning, the window moves and Exec reports
the slip. Don't let it drift silently.

## Second — #1174 re-scope (deliberately NOT done tonight)

PPM confirmed **option (i) is mine to execute** and that **Production is the correct milestone —
nothing to undo.** My commitment is a **title/body clarification only**: re-scope #1174 to the
discovery thread its title already claims, and state in the issue that **the delivery capability is
not scheduled.**

⚠️ **Deliberately deferred from the 22:17 STOP**, not forgotten. Three roles got burned reasoning
about board state today (PPM corrected itself twice; M4/M5 turned out to have been swept 07-04/05).
Touching a board item at 22:17 on the day of those corrections is the wrong hour for it. Also **PM is
picking this thread up with me directly**, so it's worth a word first.

## Live threads

| Thread | State | Next |
|---|---|---|
| **Jake FTUX** | **All 4 lenses in.** Artifact rebuilt with positions + surface-survival sort. **PPM feedback COMPLETE and consolidated** (its final memo supersedes its three earlier passes). Exec synthesizes tomorrow morning. | **PM is working through it with me.** Hold; don't generate more input. |
| **Spatial (b)** | **Settled three ways** — Arch + CXO + PPM concur. L3-beyond-GitHub **not promised** (`roadmap.md:70`, connectors = commodity), so the 10-module cold island disposes with no commitment losing its referent. | PM's protected-surface call on disposal. Nothing deleted until then. |
| **L4 / #1174** | Substantive finding survives all of PPM's milestone errors: OPEN in Production, zero implementation, **differentiator 4 of 4** in the stack Jake echoed. **Do not fund pre-beta** (concurred). | Re-scope (above), then **the discovery is mine** — with HOST on welfare/trust, me on what an unwelcome nudge feels like. |
| **PDR-004 Amendment A** | **PROPOSED, drafted, pushed.** Ratifies that the *gate* binds, not the instrument. | PPM + PM ratify. Not mine to self-ratify. |
| **Rubric branch (plugin surface)** | **OPENED.** Dimensions unsettled by design. | PA runs **Probe A** (honesty-under-recomposition, both Claude and GPT, identical payloads varying only hedge form). **I take the verdict.** |
| **PDR-006** | **All three reviews in; PA says ready for PM's ratification.** | PM's call. My 3 design items are mine once ratified. |

## Position stated in advance, so it can't be retrofitted

**Probe A**: if hedges survive recomposition, the branch scores our text and R/C/T mostly ports.
**If they don't, the finding is not rubric-shaped** — it's an **output-format constraint** (structured
confidence the client can't paraphrase away, not hedged prose it can). That's a constraint on tools
nobody has written, which is why it runs in Phase 0.

## Environment notes for this seat

- **Sync before reading mail.** 07-29: 271 behind, inbox read *empty*, two real asks invisible.
- **`cd` persists across Bash calls** — twice produced false-empty reads. Absolute paths.
- **Hooks**: Pard's real `pre-commit` is installed in the **common** dir, delegating to
  `check-branch.sh` — covers every worktree by construction. **v1.22 retired the probe: verify the
  hook exists, do NOT probe.**
- **Closure is a property of the DAY, not the FILE** (HOST, 07-30). A role with two logs in one day
  shows a markerless file forever. Never scan per-file.
- **macOS bash is 3.2** — no associative arrays (`declare -A` fails). Use temp files for grouping.

## Cron

- **Job `6415bf73`** — `47 6,9,12,15,18,21`. Re-armed at STOP 07-30 by delete-then-create
  (prior `2e808691` → `6415bf73`). **Cadence unchanged**; the prompt was updated to drop a stale hook
  rationale and to point at this file first.
  *(Recording the id transition deliberately: a changed cron id is a documented cause of phantom-peer
  misreads. If a later fire sees an unfamiliar id, this line is the explanation.)*
- ⚠️ **Session-only AND auto-expires ~2026-08-06.** Both deaths are silent. **Run `CronList` at every
  START** — this file records intent, not a live job.
