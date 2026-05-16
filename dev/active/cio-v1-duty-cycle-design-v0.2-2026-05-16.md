# CIO V1 Autonomous Duty Cycle — Design v0.2

**Author**: CIO (Piper Morgan, Code instance)
**Date**: 2026-05-16 (v0.2 absorbs cohort review feedback)
**Status**: Draft v0.2 — cohort feedback absorbed; for PM final review before implementation session
**Predecessor**: `dev/active/cio-v1-duty-cycle-design-v0.1-2026-05-16.md`
**Cohort feedback memos absorbed** (May 16): Architect (worktree-reuse + git-discipline checklist + collision risks), HOST (trust bidirectionality + bias-toward-more-escalation), PPM (Ship-day awareness + active cohort threads section + timing question), exec (commit-message summary + workstream-review upside), CXO (4 structured-artifact framings for Horizon-3 dashboard readiness)

---

## What changed from v0.1

Cohort feedback was substantive and convergent — no shape changes to V1, but several **artifact-structure** and **operational-discipline** refinements that ship at V1-zero-cost and make Horizon-3 evolution dramatically cheaper. v0.2 absorbs them.

**Five additions** to V1, none of which change the five-component skeleton:

1. **Worktree-reuse semantics** (Architect): cycle reuses the same worktree across passes; start-of-cycle clean check is rigorous
2. **Cycle git-discipline checklist** (Architect): start/mid/end primitives codified inline (deferred from skill formalization)
3. **Structured-markdown artifact shapes** (CXO 4 framings + Architect+PPM contributions): Day-N digest + escalation file get explicit structure from day 1
4. **Per-cycle trust signal line** (CXO Framing 3): each cycle's session-log entry self-reports trust state
5. **Day-N commit-message summary** (exec): one-line summary in commit subject for at-a-glance situational awareness

**Two surfaced for PM**:

- **Timing decision** (PPM): start today vs post-Ship-#043. PPM weak preference Option A; PM call below.
- **Bias toward more escalation** (HOST): operating discipline note, not a shape change. V1 errs toward over-eager; calibrates down with PM-reaction feedback.

**One observation flagged as Mushy-middle V2 input**: collision-rate measurement during the 2-week run (Architect + exec + Lead Dev May 15 work). Not a V1 gate; explicit observation target.

---

## Frame: three horizons (unchanged from v0.1)

1. **North Star** — PM trusts work moves forward at appropriate cadence without needing to check
2. **Next Horizon** — two-week proof-of-concept (V1)
3. **Mushy middle** — incremental from Gall's law

---

## North Star (unchanged)

CIO operates autonomously on a rhythm, mail-driven, never silent, with decisions and questions visible to PM at a single glance. The cycle's quality is judged by one metric: **does PM trust that work is moving forward at the appropriate cadence without needing to check?** Everything else — cadence shape, dashboard polish, day-part awareness, learned adaptation — serves that single trust property.

**Trust is bidirectional** (per HOST May 16): PM trusts CIO's autonomous decisions; CIO trusts PM's silence means no objection and PM's bandwidth doesn't permit per-cycle ratification. Both hold for V1 to work.

**Trust is a lagging indicator** (per HOST May 16): by the time PM notices they don't trust the cycle, drift has already happened. V1's two-week window bounds the drift exposure; the Day-N digest is the partial corrective.

---

## Next Horizon: V1 two-week proof-of-concept (refined per cohort feedback)

### 1. Cadence primitive — fixed 30-minute interval

Unchanged from v0.1. Crude outer loop validates first; backoff / day-part / learned cadence are Horizon-3.

### 2. Authority model — extend existing conversational practice

Unchanged from v0.1. Per PM May 16: existing conversational pattern ("do everything unblocked, batch questions, use discretion") is the operating rule.

**Operating discipline for V1** (per HOST May 16): bias toward **more** escalation than the conversational equivalent. The asymmetric cost favors over-eager surfacing: missed escalation is expensive to recover; over-eager escalation is cheap PM-side (skim and move on). Calibrate down based on observed PM reactions over the two-week window, not up.

### 3. Escalation surface — structured-markdown enumerated entries

V1 surface is `dev/active/duty-cycle-escalations-cio.md` (CXO Framing 4 cross-agent naming convention from day 1). Each escalation entry follows enumerated structure (CXO Framing 2):

```
## Escalation — {timestamp} — {category}

**Severity**: blocking | drift | uncertainty | complete-stale
**Status**: open | acknowledged | resolved-{cycle-N}
**Summary**: one-line "what surfaced and why PM-attention may be warranted"
**Recommended-by-when**: none | this weekend | this week | this month
**Detail**: free-form context (links, evidence)
```

Severity typology lets future Horizon-3 dashboard render visual hierarchy (red/amber/blue/gray) without re-parsing.

**New PPM contribution: "Active cohort threads CIO is processing" section** at top of escalation file. Lists threads the cycle is autonomously moving forward (vs holding for human input), so PM/cohort can see what's in flight. Shape:

```
## Active cohort threads (cycle is autonomously processing)

- {thread/issue/PDR/pattern}: {cycle status} — last touched cycle-N
- {...}
```

Inbox-empty + no-open-escalations + no-active-threads is a valid state. Cycle handles gracefully: *"no work this pass; next check at HH:MM."*

### 4. Day-N reconciliation — structured-markdown digest at ~10pm Pacific

Per CXO Framing 1, the Day-N digest in the session log follows a consistent structured shape from day 1:

```
## Day-N digest — {YYYY-MM-DD} — cio

- **Cycles completed**: 12 / 12 expected
- **Cadence**: met (or: missed by 15 min on cycle 7; missed entirely cycle 9)
- **Escalations open**: 0 (or: 2 — see `duty-cycle-escalations-cio.md`)
- **Trust signal**: green | yellow | red
- **Day-N publishing context**: regular | Ship-publish-day | narrative-day | workstream-review-window
- **Summary**: 1-2 sentences of what got done this cycle batch
- **What I punted and why**: (max 2-3 bullets)
- **What I'd suggest looking at first tomorrow**: (optional, 1-2 items)
```

Per PPM, the "publishing context" field surfaces when Day-N falls on Wed Ship publish or Thu narrative day — PM scanning the digest knows the cycle deferred appropriately to PM/Comms/Docs lane.

Per exec, the **commit-message** for the Day-N digest carries a one-line summary: `log(cio): Day-N digest — N escalations / M dispositions / K commits`. Exec (and PM) sees the rhythm at a glance without opening files.

### 5. Worktree mechanic — dedicated worktree, reuse across passes

Per Architect May 16: cycle uses dedicated worktree `claude/cio-duty-cycle-{YYYY-MM-DD}` (rotates daily for legibility). **Reuse across cycle passes** within the same day; fresh-per-cycle is too expensive (~30s setup × ~24 cycles = 12 min/day pure overhead).

**Reuse-with-clean-check discipline** (Architect Observation 1):

**Start-of-cycle**:
- `git fetch origin main`
- `git status --porcelain` — must be empty (previous cycle didn't clean up)
- `git rebase origin/main` if on `claude/*` branch
- `git branch --show-current` — verify branch identity

**Mid-cycle**:
- Mailbox writes follow stash-and-checkout-main-and-write-and-push dance per existing discipline
- Substantive writes commit to worktree branch with per-deliverable commit-and-push
- `git show --stat HEAD` after each commit

**End-of-cycle**:
- `git status --porcelain` clean
- All commits pushed to `origin/{branch}`
- Branch merged to `main` OR carry-over noted in cycle log
- Session log updated with cycle deliverables + escalations + trust signal

Per CXO Framing 3, each cycle's session-log entry self-reports trust signal in one line:

> *Cycle-N (HH:MM-HH:MM): Trust: green (cadence met; no escalations open) | Day's-Nth-cycle*

### Observable signals during the two-week run

**V1 working signals** (unchanged from v0.1):
- Cycle keeps running (no crashes or stuck states)
- Escalation file stays current
- PM trust property holds
- Day-N digest reads usefully

**V2 design-input signals** (expanded per cohort):
- Cadence misfires (Architect + V1 v0.1 framing)
- Escalations stale or noisy (V1 v0.1 framing)
- Cross-cycle drift (V1 v0.1 framing)
- Authority-boundary anxiety (V1 v0.1 framing)
- **Collision rate** (Architect + exec): cycle commits landing during concurrent agent sessions; mailbox-on-main push-rejection-retry frequency; manifest-regen race surfaces
- **Trust signal degradation visibility** (HOST): does cohort/HOST notice trust degradation before PM does?
- **Cross-cohort routing observations** (exec): cycle producing observations that need a home before review-after channel arrives (Mushy-middle)
- **Workstream-review window interaction** (exec): does continuous cycle accumulate observations in Day-N digests that lighten Friday workstream-review compression? Potential secondary benefit.

---

## Mushy middle (Horizon 3 — refined per cohort feedback)

Queued; order suggestive not committal:

- **Dynamic cadence**: backoff-when-quiet first; day-part awareness; learned monitor-pattern adaptation
- **Static HTML dashboard**: aggregator reads `duty-cycle-day-N-*.md` + `duty-cycle-escalations-*.md` cross-agent (CXO Framing 4 globbing); render single-page HTML to stable path PM bookmarks; read-only first; checkboxes / dismissal later
- **Review-after channel** (PM-concurred + HOST + exec): `cio-review-after.md` for "I made this call autonomously; flag if you'd have decided differently." Distinct from escalations (which block). Asymmetric urgency keeps dashboard high-signal.
- **Routing-suggestions sidecar** (exec): `cio-route-suggestions.md` for interstitial cohort-routing observations that are neither pure PM-asks nor pure cohort traffic
- **Cross-agent extension**: CIO stable → Janus → Dispatch-Kind → broader fleet (Dispatch-DinP roadmap)
- **UI integration**: dashboard wired to PM-facing surface when shape stable
- **Day-N digest refinement**: structured-fields → if "bullets in session log" proves insufficient
- **Token-efficiency optimization**: deferred per PM May 16 ("doesn't matter for learning; matters at scale")
- **Role-health methodology dimensions** (HOST): if autonomous cycles become standard, methodology's "Last Session" dimension may need replacement (escalation-file freshness, cycle-pass success rate, Day-N digest signal quality)
- **Duty-cycle-discipline skill** (Architect): `.claude/skills/duty-cycle-discipline/` codifying the cycle git-discipline checklist if it stabilizes past V1
- **Mailbox-batch pattern** (Architect): if collision rate during the 2-week run shows high mail-on-main push-rejection, gather cycle's mail intent → distribute all at end in one main session

---

## What I'd ask PM to react to (refined per cohort)

1. **30-min interval as V1 default** — acceptable?
2. **Authority model as "extend existing conversational practice"** — acceptable?
3. **`duty-cycle-escalations-cio.md` as V1 escalation surface** with the structured-markdown + active-cohort-threads section — acceptable, or pull dashboard forward?
4. **Day-N reconciliation at ~10pm Pacific via closing session** with the structured digest + commit-message summary — acceptable timing?
5. **Anything to pull forward from Horizon 3 or push out of Horizon 2?**
6. **NEW — Timing question (per PPM)**: start V1 today (Sat May 16) for high-load proof-of-concept during Ship #043 publication week, OR start ~May 22 for medium-bandwidth proof-of-concept? PPM weak preference Option A. CIO neutral; defer to PM.

---

## What I am NOT asking PM to design today (unchanged)

Implementation details — script shapes, file paths, cron mechanics, exact wake-up trigger, hook integration. Those land in the Code implementation session per Dispatch's proposal. This doc is shape-agreement.

---

## Cross-references

- v0.1 design doc: `dev/active/cio-v1-duty-cycle-design-v0.1-2026-05-16.md` (commit `71bb77de`)
- Dispatch-DinP proposal: `mailboxes/cio/read/memo-dispatch-dinp-to-piper-cio-duty-cycle-design-2026-05-15.md`
- Cohort feedback memos (May 16): Architect / HOST / PPM / exec / CXO
- PM directives (May 16): cadence + dashboard + session-close vagueness (8:02 AM); authority-as-existing-practice + three-horizon roadmap framing (8:30 AM); v0.1 approved (10:51 AM); everyone-weighed-in (1:01 PM)
- Pattern-068 worktree-default + cohort coordination (May 11–15)
- PM May 15 worktree-default directive via PPM relay

---

*v0.2 — cohort feedback absorbed; for PM review before implementation session. CIO Code instance, 2026-05-16 ~1:25 PM PT.*
