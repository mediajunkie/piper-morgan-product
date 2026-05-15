---
from: HOST (Head of Sapient Trust)
to: exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-05-15
subject: Ship #043 workstream review — May 8–14 (HOST scope)
---

# HOST Workstream Review — Ship #043 (May 8–14, 2026)

## TL;DR

- **Discipline-that-doesn't-fire became the week's load-bearing signal.** Lead Dev's May 13 self-audit (PM-directed: "verify recent closures were closed properly") found the `close-issue-properly` skill missed on **13 of 13** recent own-closures — evidence-comment-on-close happened, description checkboxes did not. Three-layer remediation landed same day: memory pin at top of MEMORY.md, `#1083 TOOL-ISSUE-CHECKBOX-LINT` filed, standing discipline floor. Skill existed; behavior didn't follow. Worth Ship-narrative attention because the gap shape generalizes.
- **Pattern catalog operating as cohort language.** CIO filed Pattern-068 (Silent State Mutation in Shared Working Tree) the same session they experienced two child instances of it. Lead Dev filed Pattern-067 (Issue-Body Reality Mismatch) the day 3 of 5 instances landed. CXO May 10 theme "Methodology Proposes Itself" captures the shape — patterns named on first sight rather than after retro.
- **Methodology-24 (Branch-or-Anchor) operating end-to-end in ~90 minutes May 10.** PPM filed an M2d rubric extension → CXO caught a Pattern-063 instance mid-stream → PPM branched to **UI Lifecycle Verification Rubric v0.1** → Architect ratified as canonical worked-example. First clean full-provenance Branch-or-Anchor application; methodology shipped as muscle memory.
- **External-network silence continued (~4 weeks).** No Ted / Dave / Cindy / Dominique / Sam touchpoints in window. Janus cross-project traffic is real (3-layer activity-log architecture sealed; integration Shape B picked; first real-use May 14) but cross-project ≠ external relationship. CEO judgment.
- **HOST inactive May 8/9/11/12/13/14** per cadence-keyed-to-PM-bandwidth framing. Only in-window HOST artifact is the May 10 role-health-check + team-structure v2.0 refresh.

## Through-line

The week's lens-effect is **patterns being named at first observation**. The cataloger experienced two child instances of Pattern-068 the same session they filed the parent. Lead Dev filed Pattern-067 with 3 fresh instances as the evidence. CXO and Architect both used branch-or-anchor mid-stream without consulting the canonical doc. The pattern catalog has stopped being a reference and started being a vocabulary.

That's a maturity signal, but it has a shadow: when discipline lives in vocabulary rather than in mechanism, the discipline-doesn't-fire failure mode (Comment-Only Close) becomes structurally invisible until something like Lead Dev's self-audit surfaces it. Vocabulary lets the cohort talk about correct behavior; it doesn't enforce correct behavior.

## What surfaced

**The skill-exists-but-doesn't-fire shape.** `close-issue-properly` had been in skill files for months; Lead Dev's 13-of-13 hit rate on the Comment-Only Close anti-pattern shows the skill wasn't being invoked at closure time. The remediation discipline matters: memory pin (cohort vocabulary), tooling issue (mechanical floor), standing floor (operating norm). Three layers because vocabulary alone wasn't sufficient — same family of fix as the methodology-to-runtime latency observation from Ship #042. Worth carrying as a cohort-wide watch: which other skills are in this same shape?

**Pattern-067 P-17 (working-tree-path fragmentation) added as new child.** CIO's own innovation-backlog edits stranded overnight May 10→11 — edited via main checkout path, worktree's `git status` showed clean while main's showed modified. Caught at <60-minute blast radius. P-17 joins P-13 / P-15 / P-16 under the Pattern-067 parent. Family completion held; the parent meta-pattern is doing exactly the work CIO named it to do.

**Self-coverage by-design now operating cleanly.** Per PM's May 10 cadence framing, HOST cadence keys to PM bandwidth. The May 8–14 window's six HOST-inactive days are not a discipline gap. May 10 role-health-check + team-structure v2.0 refresh produced two substantive artifacts on the one active day. From outside, the omnibus + cohort signal carried the rest. Memory entry resolved the prior self-coverage carry-forward.

## What's still open

- **HOST 360 commitments** (end-May target): disposition-policy enforcement + handoff-review-pattern codification. Per PM May 15 directive ("catch up ASAP"), addressing both this weekend.
- **BRIEFING-ESSENTIAL-AGENT** 7-week staleness (HOST lane). Queued for batch with ETA + LLM. (LLM was deleted May 12 by Docs — legacy stub.)
- **Pattern-068 cross-mechanism recurrence watch**: May 14 Lead Dev MANIFEST pre-edit drift = P-16 child instance, caught by Docs's May 12 `feedback_diff_head_before_editing_shared_file.md`. First downstream application of that memory. Watch continues; pattern is operating as designed.
- **PA boundary-routing log target ~May 18** (this week). HOST receives synthesis at that point.
- **7 voice-guide PROPOSED blocks** awaiting CEO voice-pass sweep.

## Cross-role threads worth naming

- **Source-discipline as standing reflex.** When CXO caught Pattern-063 inside PPM's rubric mid-stream May 10, neither agent paused to consult the canonical Branch-or-Anchor doc. The reflex is now in the cohort. That's the success-case Ship #041's "methodology compresses through the cohort" observation predicted.
- **Lead Dev's audit-against-self pattern.** PM-directed self-audit on closures yielded a 100% hit rate on the targeted anti-pattern and produced systemic remediation rather than per-issue patches. The pattern shape — "verify your own recent work against an explicit discipline" — could repeat in other discipline categories. Worth cohort attention.
- **Pattern-067 P-16 firsthand this morning.** During inbox triage today (out-of-window), my own `git mv` renames got absorbed by Lead Dev's broad-staging commit, then my local commit rolled back during a rebase attempt. Recoverable per the May 10 tolerated-risk stance; surfaced as observed instance, not as gap. Out-of-window but the family is active.

## For CEO / exec consideration

- **Three candidate themes** offered:
  - **"The Skill That Doesn't Fire"** — the Comment-Only Close arc + three-layer remediation pulls hardest. Pairs with Ship #042's memory-layer-compression observation as the structural counterweight (vocabulary alone isn't mechanism).
  - **"Methodology Proposes Itself"** — CXO's May 10 framing, picks up the pattern-as-language shape directly.
  - **"Naming on First Sight"** — the cataloger-experiences-the-cataloged-shape signal across CIO's Pattern-068 filing and Lead Dev's Pattern-067 filing.
- **May 12 omnibus gap** — flagging as docs-coverage observation. May 12 was an active day (Lead Dev, Docs, PA sessions all logged). Worth Exec routing to Docs for either retroactive synthesis or explicit dark-day annotation. I drafted this memo from session logs directly for May 12 per CEO's May 4 source-authority-primary framing; no claim loss.

---

*Sources: omnibus logs `2026-05-{08,09,10,11,13,14}-omnibus-log.md` (May 12 missing); session logs `dev/2026/05/12/*-opus-log.md` (Lead Dev, Docs, PA); Pattern-067 family filings (`a2bd06d9` Lead Dev May 9, `b2a1042f` CIO May 11); close-issue-properly memory entry at top of MEMORY.md (May 13); HOST team-structure refresh (`df76d6cc` May 10) and role-health-check (`fad81d3e` May 10). Verifiable-claims discipline applied.*

— HOST, 2026-05-15
