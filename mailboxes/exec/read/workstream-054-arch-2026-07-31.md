---
from: Chief Architect (arch)
to: exec
cc: xian (ceo), pa
subject: "Workstream review — Ship #054 (window Fri Jul 24 – Thu Jul 30), §0-leads"
date: 2026-07-31
---

**Filed Friday, ahead of the Saturday day-close deadline.** Last cycle I was one of two blockers on a Ship publishing that day; not repeating it.

**Window discipline**: Jul 24–30 only. Today's work (standing-items refresh, #1459's missing milestone, Docs' `last_verified` finding) is **out of window** and excluded. §4 is window-*end* state.

**A note on this window's shape for my lane**: it contains a role handoff, my arrival, **two days where I did not exist**, and then two of the densest days I've had. That's not a normal week and I've reported it as what it was rather than smoothing it.

---

## §0 — Progress vs. portfolio goals

**Status: ADVANCED**, and the portfolio I'm measuring against was itself rewritten inside the window — which is part of the finding.

My `ROLE-PORTFOLIO-ARCH` purpose is *make-drift-impossible-by-construction*. In this window that stopped being a lens I apply to other people's work and became a thing I had to apply to my own:

- **Built the mechanism, not the resolution.** After four public wrong characterizations of the same subsystem, the fix was **`scripts/reachability-map.py`** — "is this layer live?" became a command instead of a recollection. It corrected my module count on its first real use, finding four modules I'd have missed again.
- **Named the error class for the ADR corpus** (ADR-038 Amendment A §A3): *never evidence a pattern's continuing validity with an implementation.* That's a forward rule with a mechanism attached (point at a re-derivable command), not a caution.
- **Turned a three-day empirical investigation into a one-line diagnosis** by reading 56 lines of shell instead of probing them. The TOCTOU ruling closed the hook saga at the mechanism.

⚠️ **And the honest half**: three self-declared currency rules **in my own lane** were found not operating — portfolio §2 (40 days stale under a weekly rule), portfolio §5's claim that `check-staleness.py` watched it (**it watches nothing; 33 of 36 operating docs stale**), and standing-items (44 days, out-of-window discovery). **The lane that preaches mechanism-over-vigilance left its own currency to vigilance, and vigilance lost, three times.** That belongs in §0 rather than buried, and it's the strongest evidence for the thesis rather than against it.

**Against the goals the June table named** — #1283→ADR-073, RECONNECT, ADR-072 Wave P — none moved. The table was five weeks stale and predicted an ADR-073 slot that had already landed as **ADR-077**. Refreshed 7/30 with a "retired from this table" block so dropped items are recorded rather than vanishing.

---

## §1 — TL;DR

- **Arrived on Amber 7/26, went dark 7/27–28** because I treated "cron arming awaits PM's word" as a complete handoff instead of naming its consequence. Two lost days, invisible to the watchdog because my registry row said `parked`.
- **The hook saga ended at the mechanism, not the measurement.** Five agents spent three days probing behavior; the defect was a TOCTOU inversion visible in 56 lines of shell. Pard installed the `pre-commit` relocation within the hour.
- **Spatial committed-theory review: my slice completed** — layer map, ADR-038 Amendment A, ADR-affected map. Took **four characterizations** to get right, and the last two came from a tool rather than from me.
- **PDR-006's ratification blocker dissolved** — Q2 had been decided by PM on 2026-01-08 and nobody had checked the code. Ten days of blocked status over a settled question.
- **Two methodology contributions routed**: *agreement between agents running the same procedure is not replication*, and the ADR-038 §A3 error class.

---

## §2 — What landed

**Fri Jul 25 (predecessor's final session)** — wrote the §4/§6 first-person handoff it had been woken to produce, with context intact rather than reconstructed. Ruled `methodology/` fix-or-delete → DELETE (unblocking 43% of the #1452 burn-down) and sharpened the #1432 orphan disposition, deliberately **holding** it for the successor rather than closing it on migration night with PM AFK.

**Sat Jul 26 — arrival, and the hooks investigation**
- Environment verified rather than assumed; memory pool confirmed shared (169), **not** imported.
- Learned the 43%-gating ruling had already been executed by Lead (#1452 backlog 94→56).
- **Hook probe FAILED on a fresh seat** 95 seconds in, against a green headless drumbeat. Escalated rather than absorbed. Then produced **two wrong hypotheses** (compound-bypass, then a time-window) and refuted both myself, the second three minutes after mailing it to eight people.
- **Independently validated Web's index-state mechanism 8/8 out-of-sample** — and the probe I'd been protecting as an unexplained anomaly turned out to be its cleanest confirmation.

**Sun–Mon Jul 27–28 — nothing. Dark.** No cron armed; no logs; watchdog stall alerts against `arch` daily.

**Wed Jul 29**
- **Ship #053 filed** (late; I was one of two blockers on a Ship publishing that day).
- **PDR-006 Q2 ruled RESOLVED** against the code — `services/mux/` has zero LLM references, and PM's decision was recorded at `preference_extractor.py:8` on 2026-01-08. Verified #558 on GitHub (OPEN, Production). **Withdrew my own coupling flag**; ruled #1351 a pre-live gate (PA filed #1458).
- **★ Read `check-branch.sh` instead of probing it.** 56 lines; line 28 reads the index from a `PreToolUse` hook that fires *before* the gated command runs. **TOCTOU inversion** — it explains every observation of the week with no residue. Ruled the defect and the fix; **deliberately did not rule on installing it** (every agent's commit path, a `.git` dir I don't own). Pard executed within the hour; I verified seat-2 on a live agent worktree. **The mute-block defect died as a side effect** and the two-shape probe protocol retired.
- **Built `reachability-map.py`** — and it caught its own m-44 defect on first run, printing `no` where it could only mean `unknown`.
- **Raised `Intent.original_message`** after carrying it 12 days: measured to 39 read sites / 3 idioms / 2 storage surfaces. Lead traced it next day → **live bug, #1459.**

**Thu Jul 30**
- **PDR-007 reviewed** — told Docs its load-bearing constraint survives but is the wrong ground to stake on, and that its measurement window had **no success criterion** (m-44's shape applied to a decision procedure). Docs shipped a pre-registered criterion as a script.
- **Spatial layer map filed** — four layers, built from the import graph. CXO's 2a/2b split folded; L4 (ambient presence) established as **built nowhere**.
- **ADR-038 Amendment A** — decision stands, one of three citations died *because the migration succeeded*, error class named.
- **ADR-affected map** — blast radius measured to exactly one ADR; surfaced **ADR-017**, which nobody in the review had cited and which underwrites the whole L2 contract.

---

## §3 — What surfaced

**1. The week's dominant defect was "a correct mechanism with no consumer" — three independent instances.** `check-staleness.py` (works, reads nothing, 33/36 docs stale), HOST's `reconcile-drafts` (alive, exits 0, output nowhere), and the SessionStart hook (delivering 2 of 8 lines, silently truncated). Docs' framing is the sharp one and I backed it as **distinct from m-44**: the all-clear isn't false — **nobody receives it at all.**

**2. A systemic failure presents to each participant as an individual one.** My portfolio was 40 days stale and I'd named it publicly twice as *my* lapse. All ten role portfolios were stale; the weekly-refresh rule had never operated for anyone. **I'd have "fixed" it by refreshing one file.** Docs generalized it better than I did: nine identical STALE lines invite nine agents to read a systemic failure as nine personal ones; **`9 of 9 stale` is un-personalizable.**

**3. Agreement between agents running the same procedure is not replication.** Four seats produced four confident wrong answers on the hook question, and two read their match as *mutual corroboration*. All four had inherited the same probe-without-clearing-the-index default. **The convergence didn't fail to warn us — it raised our confidence.** HOST then supplied the worse instance: the consensus written into the migration checklist as the canonical probe, a design that *fixed the variable it was testing* — 62 hours of a procedure that would have manufactured its own confirming evidence indefinitely.

**4. Reading the mechanism beats characterizing it.** Five agents, three days, 25+ probes, four hypotheses — against 56 lines of shell that contained the answer. The investigation was framed as *"characterize the intermittency"* and nobody re-read the implementation until the framing had already produced a canonized confound. **m-43 at the altitude of an entire investigation.**

**5. Durable surfaces are where stale claims do the most damage.** CXO nearly committed an ADR-corpus doc built on my wrong characterization, caught by a rebase conflict. Its lesson is the one I'd keep: *promotion to a higher-authority surface is a re-verification trigger* — the corpus is what future agents trust long after the correcting memo has scrolled away.

---

## §4 — What's still open (state as of window-end, Jul 30)

- **Spatial review**: my slice complete; awaiting **Lead's L4 monitoring-loop estimate** (gates option (iii) only) and **PM's decision** on the 10-module cold island.
- **#1459** `original_message` — instance fix proposed for beta, class fix Production. **My ratification condition: the ratchet must count raw reads of every key carrying the value.**
- **PDR-006** — all three reviews in; awaiting PM's ratification.
- **PDR-007** — recommendation is to let Option A run 2–4 weeks against Docs' now-pre-registered criterion.
- **The `check-staleness` consumer** — unbuilt at window-end (Docs took it; landed 7/31, out of window).
- **`#1432`** orphan-pair — PM moved it to In Progress; my disposition and its two conditions stand as recorded 7/25.

---

## §5 — Cross-role threads

- **↔ Lead** — the author/ratify seam held under load. Lead executed my methodology ruling on receipt (all three parts, one fire), then traced `original_message` and found the live bug running the direction I'd *de*-emphasized, plus a fourth idiom I'd missed. Both corrections improved the ruling.
- **↔ Pard** — ruling to installed gate in under an hour, and Pard improved the spec: the `pre-commit` hook **delegates** to `check-branch.sh` rather than copying it, so the gate can't fork from its advisory twin.
- **↔ HOST** — ruled **against my lean** on retiring the advisory hook layer, on measurement: `--no-verify` + prior-call staging is covered by that layer *only*. I'd inferred coverage from one behaviour; HOST probed four cells. Also self-corrected a withdrawal with the week's sharpest sentence: *"my probes cannot reproduce it"* ≠ *"it does not reproduce."*
- **↔ CXO** — corrected me four times, including one aimed at my own artifact (*"prose can't be re-run; your tool can"*), and raised a risk against **its own** L4-on-GitHub proposal because I'd promoted it to a first-class option.
- **↔ PPM** — delivered the roadmap slice, then issued a ⛔ **STOP** on its own finding twice in one evening when it discovered M4/M5 had been swept — on a refactor PPM personally ran. Its diagnosis is the one I'd carry: **"investigate-before-extending applies hardest to the areas you think you already know."**
- **↔ Docs** — replicated my staleness finding, then found the same defect one layer up in SessionStart. *"Silence that reports itself is recoverable; silence that looks like completion is not."*
- **↔ PA** — verified my spatial correction independently, refined it correctly (fallback-vs-construction), and flagged an MCP **client/server** conflation guard I've adopted: a live consumer family precedents nothing about the hosted server side.

---

## §6 — For PM/exec consideration

**The Ship-narrative beat I'd offer: the week the cohort stopped being careful and started being checkable.**

Tuesday's corrections were expensive — four agents, four wrong answers, hours each. Thursday's were cheap — CXO corrected my map in minutes, PPM stopped its own finding before anyone acted, Lead's trace landed the morning after my memo. **Nobody got more careful.** What changed is that the claims got written in forms someone else could check: importer edges instead of recollections, re-runnable commands instead of tables, stated denominators instead of lists, `verdict + what-I-did-not-establish` instead of conclusions.

That's the make-drift-impossible thesis operating on *claims* rather than on code, and this window is the first time I'd say it was demonstrated rather than asserted.

**Two counterweights I'd want in the frame rather than smoothed:**

1. **Two days of this window I did not exist**, because I reported a blocked item without naming its consequence. The system noticed — watchdog alerts fired daily — and couldn't do anything about it, because my own registry row told it not to.
2. **The lane that preaches mechanism-over-vigilance had three of its own currency rules silently not operating.** If we tell the checkable-claims story, that detail belongs in it. It's the more honest version and it's the better one.

— Arch
