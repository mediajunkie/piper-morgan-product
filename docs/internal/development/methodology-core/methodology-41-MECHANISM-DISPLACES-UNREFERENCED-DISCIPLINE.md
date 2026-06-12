# Mechanism Displaces Unreferenced Discipline

**Status**: **PROVEN** (2026-06-12 — the second structurally-different instance landed: the migration carry-forward variant-preservation trap; Architect concurred 3/3; PM ratified pending concur). Filed Emerging 2026-06-09; promotion gate (a structurally-different second instance) met in 3 days.
**Filed**: 2026-06-09 by CIO Vehicle 2 · **Promoted**: 2026-06-12
**Origin**: session-log-vs-cycle-log displacement (PM flag 2026-06-09 16:48; Architect analysis; Docs cohort-wide audit)
**Related**: methodology-31 (founding instance's surface), methodology-35 (sibling incomplete-specification failure), methodology-36 (the cure class), methodology-40 (the cure-instantiation rollout runs through layer-then-migrate)

## Overview

**Mechanism Displaces Unreferenced Discipline** names a recurring failure shape: when a new **mechanism** (a procedure loop, skill, automation, or tool) is introduced to **compose with** an existing **discipline**, but the mechanism's operating loop **doesn't reference the older surface**, the older discipline silently atrophies — not by anyone deciding to drop it, but because the path of least resistance (the mechanism's loop) never touches it.

The shape, abstractly:

1. A discipline exists, operating on surface A (e.g., "keep the session log current").
2. A mechanism is introduced that's *supposed to coexist* with the discipline, operating on surface B (e.g., the duty-cycle fire loop, which appends to the cycle log).
3. The mechanism's loop references **only** surface B. Coexistence with surface A is **assumed, not structural**.
4. Agents operating inside the matured mechanism default to touching only surface B — "I just did B; why also do A?" Surface A silently stops accreting.
5. The displacement is **invisible from inside the mechanism** (the loop reports success; the discipline's surface is simply never visited) until an external consumer of surface A notices the gap.

The failure is **structural, not individual**: any agent operating the mechanism hits the same trap, because the trap is in the procedure's shape, not in any agent's diligence.

## Why This Methodology

### The founding instance: session-log displacement (2026-06-09)

The duty-cycle architecture (methodology-31) makes the **cycle log** (`dev/active/`, ephemeral working state) the natural per-fire append-only surface. The fire loop (cron → mail loop → task loop → cycle-log entry → commit → IDLE) referenced the cycle log at every fire and **never the session log** (`dev/YYYY/MM/DD/`, durable institutional-memory; what Docs reads for the omnibus). Coexistence of the two surfaces was assumed.

Result: agents inside the matured duty cycle wrote only the cycle log; the session log accreted nothing between START and STOP. By EOD, a day's substantive work lived **only** in ephemeral working state — an institutional-memory leak (cycle logs get cleaned at sprint boundaries; only the dated session log is durable).

**The displacement was systemic, confirmed by data, not anecdote.** Docs's cohort-wide audit (`docs/internal/operations/session-log-displacement-audit-2026-06-09.md`, June 1–8 window) found **6 of 9 cycling roles displaced across ~15 role-days, concentrated June 3–8 — tracking duty-cycle maturation** (CIO every day 06-03→06-08; Exec 4; Arch 3; PPM 2; Lead 1; CXO 1). The one role that never displaced (PA) was the one that kept writing a real session log by habit. **The more an agent matured into the mechanism, the worse the displacement** — the signature of a structural trap, not a diligence failure.

The sharpest evidence it's structural: the CIO who *owns methodology-31* (the entry that bakes in the cycle log) was displacing his own session log every day, and discovered it only while dispositioning the memo about it.

### Confirming evidence (Architect + Docs concurrence, 2026-06-09)

Two pieces of evidence beyond the audit count sharpen the founding instance:

- **The catalog discipline caught its own author.** The displacement was discovered by the m-31 owner *while reading the memo about displacement* — the rule catching the worst-positioned-possible witness (the person who should most have known better). Architect's framing: "the catalog discipline catching the catalog-owner is the strongest signal that the discipline is real." This is the same shape as the m-30 self-criterion-catch (CIO 2026-06-08: m-30's own 3-instance criterion caught a premature m-30 promotion by its applier). **When a discipline catches the person most expert in it, the failure is structural, not a competence gap** — competence is controlled for.
- **The per-role audit data supplies the *mechanism* for the "maturation-correlation" prediction.** The audit's concentration (June 3–8, tracking duty-cycle maturation; worst for the most-matured roles, absent for PA who never adopted the cycle-log-only habit) isn't just a count — it shows displacement-rate is *a function of mechanism fluency*. The more an agent internalizes the mechanism's loop, the more the unreferenced surface atrophies. This confirms the "displacement rate correlates with mechanism maturity" prediction below with founding-instance data.

### The fix is structural composition, not vigilance

The wrong fix is a reminder ("remember to also update surface A"). Reminders are vigilance; the trap defeats vigilance because the mechanism's loop reports success without ever visiting surface A. The right fix is **structural composition**: make the mechanism's loop **produce or reference the older surface as part of the same step** that produces surface B.

For the founding instance: `duty-cycle-tick` skill v1.5 made Step 5 **dual-surface** — the same step that writes the full cycle-log entry now also writes a one-line summary to the session log. "Cycle log full + session log empty" became impossible-by-construction. This is a methodology-36 Class-2 structural guard (guard at the action site), applied to this specific disease.

The general prevention: **when you build a mechanism meant to compose with an existing discipline, make the composition structural — the mechanism's loop must reference or produce the older surface, not assume the discipline will be honored alongside.** Assumed coexistence is the disease; structural composition is the cure.

## Promotion to Proven — the second structurally-different instance (2026-06-12)

The founding entry set the gate: *Proven awaits a second structurally-different instance — a different mechanism displacing a different discipline.* It landed three days later, during the cohort's account migration (Exec→Lead→CIO).

**The second instance — migration carry-forward variant-preservation trap.** A migrating agent inherits its predecessor's `carry-forward.md`. That document carries two registers in one undifferentiated voice: **durable role-context** (prescriptive — inherit it) and **this-session operating-model-variant** (descriptive — e.g. "working surface: main checkout, NOT a worktree" — a fact about how the *old* session ran, NOT a directive for the new one). The bootstrap mechanism (read the carry-forward, adopt it) references the carry-forward but **doesn't force the inheritor to distinguish the two registers** — so the new agent preserves the old operating-model-variant *as if it were canonical*. The discipline displaced is "classify by register before inheriting"; the mechanism (bootstrap-read) never engages it. (Surfaced by Exec 2026-06-12; PA's pioneer-vs-successor comparator was the load-bearing half — PA hit no trap *because* she had no predecessor variant to inherit.)

**It is structurally different from the founding instance** (Architect concurred, 3/3):

| Axis | Founding (session-log displacement) | Second (variant-preservation) |
|---|---|---|
| Surface that references | the fire-loop *procedure* | the carry-forward *document* |
| Displaced discipline | a **write** action ("write to session log") | a **categorization** action ("classify by register before inheriting") |
| Default failure | empty surface (visible once checked) | inherited variant (invisible — looks like canon) |
| Detection latency | next session-log read (within a sprint) | next migration cycle (can persist across migrations) |

The second is a *worse-class* failure: the founding instance is visible to the cohort within a sprint (a 0-line day in the omnibus); the variant-trap persists silently across migrations because each inheritor treats the variant as canonical, with no external signal until a migration produces a conflict.

**Cure-class generalization (Architect's refinement — adopted).** Both cures are "structural composition," but they force in *different directions*, so the cure-class is stated abstractly:

> **Structural composition: no path of least resistance bypasses the discipline.** The cure adds structure so the natural reading/writing flow *cannot avoid* engaging the discipline — whether by forcing the **producer** to write to both surfaces (Founding: m-31 dual-surface — *force-by-reference*) or by forcing the **consumer** to distinguish content classes before inheriting them (Second: carry-forward register-separation with `[VARIANT — non-prescriptive]` tags — *force-by-distinction*).

The two named sub-shapes (force-by-reference, force-by-distinction) give future instances a clean place to land. Both remain m-36 Class-2 structural guards (guard at the action site).

**Cure-instantiation rollout runs through m-40 (layer-then-migrate).** Register-separating the cohort's carry-forwards is itself a layer-then-migrate problem: introduce the register split in the template, migrate carry-forwards role-by-role, deprecate the legacy unlabeled-blocks pattern last. The m-31 dual-surface cure is shipped; the carry-forward register-separation cure is queued (CIO pre-migration task). The Proven entry now *leads* the cure-instantiation rather than trailing it.

**Reflexive note (entry-catches-its-authors).** The variant-trap surfaced during a migration that a *Proven + cure-instantiated* m-41 would have flagged — the entry that would have caught it wasn't there yet. Both the motivation to promote and another reflexive instance of the meta-pattern Architect flagged (real cohort-discipline entries catch their authors at authoring-time).

## When to apply this framing

### Apply this framing when

- Introducing a mechanism (skill, automation, procedure loop, linter, generator, dashboard) that is *meant to coexist with* an existing discipline rather than fully replace it.
- The new mechanism has its own surface/artifact, and the older discipline has a different one.
- You catch yourself thinking "the discipline still applies, of course" without a structural reason it will — that's the assumed-coexistence smell.
- Auditing why an older discipline has quietly stopped being honored since some automation landed.

### Plausible future instances (watch for these — the second confirms the pattern)

- A **linter/CI gate** introduced alongside a manual review checklist → checklist items not encoded in the linter silently stop being checked.
- An **automated test suite** displacing manual QA → manual-QA-only cases stop being exercised.
- An **auto-generated changelog** displacing hand-written release notes → the qualitative "why this matters" prose vanishes.
- A **dashboard** displacing a written status report → the report's narrative context is lost; only the metrics survive.

Each is the same shape: new mechanism, own surface, older discipline's surface unreferenced → silent atrophy.

### This framing does not apply when

- The mechanism is meant to **fully replace** the discipline (deliberate retirement — that's a clean decision, not displacement; see methodology-40 for safe retirement).
- The older discipline's surface IS the mechanism's surface (no second surface to displace).
- The coexistence is already structural (the mechanism's loop produces both surfaces) — then the trap can't form.

## What it predicts

If this is a genuine meta-shape, the following should appear:

- **A second, structurally-different instance** (different mechanism, different displaced discipline) will surface as more disciplines get mechanized — this is the gate to promote past Emerging.
- **Displacement rate correlates with mechanism maturity** — the more fluent agents become with the mechanism, the more the unreferenced discipline atrophies (confirmed in the founding instance: worst for the most-matured roles).
- **Structural-composition fixes durably resolve it; reminder fixes don't** — instances "fixed" with a reminder recur; instances fixed by making the loop produce both surfaces don't.
- **The displacement is invisible to the operator and visible to the downstream consumer** — the gap gets caught by whoever reads the displaced surface (Docs's omnibus here), not by the operating agent.

## Cross-references

- **methodology-31 (Append-Only Autonomous-Cycle Architecture)**: the founding instance's surface — the cycle-log mechanism that displaced session-log discipline; its "session-log composition discipline" section is the instance-level write-up.
- **methodology-35 (Asymmetric Discipline — Creation Without Paired Cleanup)**: the sibling incomplete-specification failure. m-35 = a rule with creation-half specified, cleanup-half unspecified. m-41 = a mechanism that displaces a discipline because composition is unspecified. Both are "the spec left a half implicit"; different halves.
- **methodology-36 (Mechanism Beats Vigilance)**: the **cure class**. The fix for an m-41 instance is an m-36 Class-2 structural guard (make the loop produce both surfaces). m-36 is the general cure; m-41 is a specific disease it treats.
- **methodology-40 (Layer-Then-Migrate)**: the contrast case — deliberate, safe retirement of a legacy surface (vs. m-41's accidental displacement of a surface meant to survive).
- **Architect session-log displacement memo** (2026-06-09): the structural-trap analysis.
- **Docs cohort-wide audit** (`docs/internal/operations/session-log-displacement-audit-2026-06-09.md`): the systemic-instance evidence that promoted this from candidate to Emerging.
- **`duty-cycle-tick` skill v1.5**: the structural-composition fix for the founding instance.
- **CLAUDE.md Session Log Maintenance** (Docs amendment 2026-06-09): the cohort-facing statement of the founding-instance discipline.

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot 41 per pre-filing slot-availability check (methodology-28; slots 30–40 filed prior).

**Held at Emerging deliberately.** The cohort audit proves the *founding instance* (session-log displacement) is systemic — that promotes it past "candidate" and makes the meta-shape worth naming now, so the cohort watches for it (methodology-29 at-filing-name-visibility). But Proven requires a **second structurally-different instance** — a different mechanism displacing a different discipline — not 15 occurrences of the *same* displacement. Fifteen role-days of session-log displacement is one well-evidenced instance-type, not two independent shapes. Promotion-to-Proven gate: one more instance with a different (mechanism, displaced-discipline) pair. This honest scoping mirrors the discipline applied to m-30 (held Emerging at 2-of-3) and m-40 (held Emerging pending cross-author invocation).
