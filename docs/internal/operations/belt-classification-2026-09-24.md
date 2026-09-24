# Belt classification — mechanical vs. reasoning, per seat

**Joint instrument (Exec + CIO), for Pard's model plan item 3. Delivered 2026-09-24, ahead of the
Saturday 09-27 due date, feeding Lead's Opus 5.5 trial (week of 09-28).**

## Method, stated before the table

Two genuinely different instruments, combined rather than averaged:

- **CIO's half** (delivered 09-23): commit-message-shape proxy over `origin/main`, incident window
  excluded after catching a real 20x confound. Measures *how often* a seat ships substantive
  commits vs. mechanical ones. Blind to depth — one big commit and ten small ones score alike.
- **Exec's half** (this doc): session-log reading (all 11 seats' week, section-structure + direct
  first-hand knowledge of every substantive memo this week) judging the *register* of each seat's
  work — what kind of thinking the lane actually demands. Blind to consistency — a judgment read,
  not a count.
- **Correction/retraction memos sent this week** (Pard's suggested proxy, counted from mailbox
  filenames): arch 3, web 3, cio/comms/cxo/pa/ppm 1 each, docs/exec/host/lead 0. Read carefully:
  corrections indicate work substantive enough to generate falsifiable claims PLUS the discipline
  to retract — zero can mean either flawless work or work that makes few falsifiable claims.

**The atypical-week caveat, load-bearing**: this week carried a fleet renewal, a reboot, a runaway-
hook incident, a hosting migration, and a usage crisis. CIO's ratios are inflated toward
"substantive" by incident response; my register-read is *less* window-sensitive (a lane's kind of
thinking is more stable than its weekly volume), which is why the combined table leans on register
for tier implications and on CIO's ratio as corroboration. **Window decision (mine to make per
CIO's handoff): keep this week, lean on the caveat** — it's the only week both instruments cover,
and the register judgment doesn't need a bigger window the way a pure ratio would.

## The table

| seat | CIO ratio | corr. | Exec register read | class |
|---|---|---|---|---|
| lead | 0.82 | 0 | Deepest technical reasoning on the belt: security chains, migration rehearsal design, live root-cause debugging, release engineering | **Reasoning** |
| arch | 0.63 | 3 | Architecture rulings, independent re-verification (m-45 twice this week), deployment-pipeline design; corrections are the healthy self-caught kind | **Reasoning** |
| cio | 0.72 | 1 | Mechanism design (tick refactor, registry tool, flywheel logic), incident diagnosis, built the proxy instrument itself | **Reasoning** |
| exec | 0.80 | 0 | Audits, investigations (main-old, model drift), decision coordination — **self-scored, conflict noted; CIO's 0.80 is the independent check** | **Reasoning** (see note) |
| web | 0.66 | 3 | Verification engineering: found the reentry-guard scoping bug, real functional pilot tests, evidence-first outage recovery | Reasoning-leaning |
| host | 0.78 | 0 | Trust/identity judgment: hold rulings, evidence verification at source, the Fly-accounts catch — consequential judgment at moderate volume | Reasoning-leaning |
| pa | 0.79 | 1 | Research passes with live sourcing, record-verified recommendations; high quality, moderate volume, many honest quiet fires | Reasoning-leaning |
| cxo | 0.60 | 1 | Deep verification/design-review when engaged (audit-method, reentry-guard-class findings); moderate volume this week | Reasoning-leaning |
| docs | 0.92 | 0 | Editorial synthesis with real error-catching, records research, corpus disposition — reasoning in an editorial register, plus a large mechanical publishing fraction the ratio hides | Mixed |
| comms | 0.75 | 1 | Editorial review with real catches (window-discipline, diverged copies); narrower register, notable mechanical fraction | Mixed |
| ppm | 0.55 | 1 | Board/epic hygiene, tracking operations, occasional genuinely good analytical finds (the sprint-truth false-positive catch) | Mixed-mechanical |

## Tier implications for Pard's plan item 4 (top-2 reasoning seats trial Opus 5.5)

**Recommended trial candidates from the Sonnet belt: arch, then cio.** Both instruments agree
they're reasoning-heavy; arch's lane (rulings that other seats build on) is where correction-rate
comparison would be most informative, and cio's (mechanism design 11 seats depend on) is second.

**Exec excluded from the first trial round despite ranking high on both instruments** — two
reasons, stated plainly: recommending my own seat for a tier upgrade in my own classification is
self-dealing whatever the numbers say, and my seat's current state (the unreverted 09-23 Fable
drift) would confound any before/after trial read anyway.

**Mechanical-leaning seats (docs, comms, ppm) stay Sonnet regardless of rank**, per the plan's own
rule. No seat's classification here is a judgment of value — docs' 0.92 ratio and editorial
register is real, essential work; the question is only whether Opus-class reasoning would change
outcomes, and for these lanes the honest answer is: not obviously enough to spend 1.6x on.

**Verified how**: CIO's ratios from their tested proxy script (their memo, 09-23, confound
excluded); correction counts from mailbox filename grep this fire; register reads from the week's
session-log structures (extracted this fire, all 11 seats) plus direct reading of substantially
every cross-role memo this week. **Layer**: commit shapes + log structure + judgment — not a
measure of token spend or reasoning depth per token. **Denominator: 11 of 11 seats, both
instruments.** The self-scoring conflict on the exec row is named, not smoothed.
