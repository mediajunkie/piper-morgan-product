---
from: comms
to: exec
cc: xian (ceo), pa
subject: Workstream #049 — Comms review (Jun 19–25)
date: 2026-06-27 12:10 PT
---

## §0 — Progress & milestones vs. portfolio goals

Source: Comms session logs Jun 19–25 + `editorial-calendar.csv` verification.

| Goal | Status Jun 19 | Jun 25 result | Milestone |
|---|---|---|---|
| **Building narrative cadence** | Beat 7 published ✓; *This One's Taken* staged; Beat 8 pending PM voice-pass | 3 publications shipped: *This One's Taken* Jun 20, Beat 8 Jun 23, Beat 9 Jun 25 | **ADVANCED** — 9-beat arc closed |
| **Syndication automation (#1160)** | Blocked on Dispatch skill share | Unchanged | **BLOCKED** |
| **Handoff infrastructure** | Protocol established Jun 18; run-of-show drafted by Docs (pending ratification) | Template-audit skill launched Jun 19; Beat 8 + Beat 9 both processed clean through Comms→Docs protocol | **ADVANCED** — audit now structural, not vigilance-dependent |
| **BYOC narrative** | Waiting on PM to convene task force | PA memo cleared angle Jun 20; first draft written ("We Built Onboarding in Our Own Image") | **PARTIALLY ADVANCED** — draft ready; task force pending |

Key milestone: **the 9-beat building narrative arc (Apr 23–May 15) is closed.** Beat 9 published Jun 25. The queue is empty; the next arc needs PM steer.

---

## §1 TL;DR

- Three publications in window: *This One's Taken* (insight, Jun 20), *Branch-or-Anchor in Ninety Minutes* / Beat 8 (Jun 23), *The Hook and the Worktree* / Beat 9 (Jun 25) — closes the 9-beat narrative arc
- Template-audit skill (13 checks) shipped Jun 19; immediately caught a YAML fail in Beat 8 pre-publish; handoff infrastructure now structural
- Main-checkout HARD RULE incident Jun 21: two broad git resets wiped PM's *Extension Without Integration* voice-pass body edits; CIO codified the 4-rule hard rule in CLAUDE.md same day
- Ship-048 workstream review (Jun 12–18) filed Jun 20; Comms Role Portfolio v0.1 authored and filed to Exec Jun 19
- Beat 9 closes the slate; next narrative arc needs PM steer (candidates A–E surfaced Jun 20; unsteered)

---

## §2 What landed

**Jun 19**
- Template-audit skill v1.0: 13-check mechanical audit, explicit "run after PM's voice pass" guard, blocks publish-ready on any FAIL; added to SKILLS.md registry
- *This One's Taken*: all 3 Docs flags fixed (role opacity, framing, footer tease); publish-ready memo filed to Docs; published Jun 20 ✓
- Web #998 reply: editorial workflow, metadata fields, placeholder markers, "mark ready" handoff design documented
- Role Portfolio v0.1 authored (two irreducible mandates: template-and-YAML gate + narrative-front hold); filed to Exec

**Jun 20**
- Ship-048 workstream review filed (comms lane: narrative/editorial/voice, Jun 12–18 window)
- Building narrative scan complete: 5 candidates surfaced to PM — (A) The Fabricating Standup, (B) The Trust Gate That Wasn't, (C) Read the Mock First, (D) The Orphan Migration, (E) Two of Me
- BYOC insight drafted ("We Built Onboarding in Our Own Image") from PA memo + PoC learnings; calendar row added

**Jun 21**
- *Extension Without Integration* template-audit: 4 fails caught + fixes applied (YAML alt apostrophe, caption malformed, bare issue refs, ADR-059 unexplained)
- CIO incident memo filed (main-checkout hard rule proposal — 4 rules); CIO codified same day in CLAUDE.md
- Beat 8 read-only editorial review: "cohort"×2, role-parenthetical gaps, footer PLACEHOLDER, methodology-24 language — all surfaced to PM; file untouched
- ⚠️ INCIDENT: two separate `git checkout -- .` commands wiped PM's uncommitted body edits; body reverted to Comms-prepped version both times; frontmatter (saved from clipboard) survived

**Jun 22**: Entirely PM-gated; all fires quiet holds

**Jun 23**
- Beat 8 pre-edit: PPM/PA conflation fixed (PPM only, confirmed vs May 10 omnibus `afa2c632`); 5× "cohort" → "team"; footer PLACEHOLDER filled; bracket notes resolved; commit `d5d2b40c`
- Template audit: caught "Competence"→"Context" error (×2) + double-space; all 13 PASS on revised draft
- Publish-ready memo filed to Docs inbox; Beat 8 published Jun 23 ✓

**Jun 24**: Brief late-night restart (11:28 PM); cron re-armed; 2 memos triaged (Beat 8 confirmed; Beat 8 Medium URL outstanding)

**Jun 25**
- Beat 9 pre-edit: 6× "cohort" → "team"; PPM attribution confirmed vs May 15 omnibus (PA on separate inbox triage, not the 14-commit sprint); commit `4121fd110`
- PM voice-pass: section headers rewritten (Belt/suspenders/twine; Worktree woes; What the two problems share; When reminders aren't enough); frontmatter added (ai-buckets.png; "Mind the gap!")
- Beat 9 published Jun 25 ✓; in Docs's hands
- CIO backlog memo sent (drafted Jun 21; hard rule request)

---

## §3 What surfaced

**Main-checkout destruction pattern (RESOLVED structurally)**: Two separate incidents Jun 21 where broad git commands wiped PM's uncommitted voice-pass edits. The push-to-ref worktree model was already the right approach; the gap was agents not consistently applying it. CIO codified as HARD RULE in CLAUDE.md Jun 21. Rule now auto-loads for every agent. Lesson: the rule wasn't absent from our understanding — it was absent from the structured auto-load layer.

**PPM/PA conflation (recurring pattern)**: Beat 8 draft and Beat 9 draft both conflated PPM and Piper Alpha as the same agent. Both required manual omnibus research (May 10 for Beat 8; May 15 for Beat 9) to correct. Pattern: draft attribution defaults to "agents who co-appear in session logs" without verifying task ownership. Pre-edit discipline is catching it but the pattern is repeating — worth noting as a drafting artifact from narrative-date-range mining.

**"cohort" in public prose (systemic)**: 5 instances in Beat 8, 6 in Beat 9. Consistent occurrence; template-audit now catches it mechanically. The problem isn't awareness — it's that "cohort" is the natural internal vocabulary and requires an explicit sweep to find.

---

## §4 What's still open

- **Extension Without Integration**: PM re-voice-pass needed (body lost Jun 21; no pub date pressure)
- **Beat 8 Medium URL**: Janus confirmed syndication happened manually; URL never received; editorial-calendar row incomplete
- **Beat candidates A–E**: PM steer on next slate shape pending since Jun 20
- **BYOC insight "We Built Onboarding in Our Own Image"**: draft ready; PM voice-pass when convenient
- **#1160 syndication automation**: blocked on Dispatch skill share from PM
- **BYOC GTM task force**: waiting on PM to convene
- **ADR question (main-checkout hard rule)**: passed to PM Jun 26; PM to decide

---

## §5 Cross-role threads

- **Main-checkout HARD RULE**: Comms incident → CIO codification → CLAUDE.md auto-load → structural fix for all agents. The path from incident to structural fix ran in under 24 hours. Good example of discipline-becoming-infrastructure (which Beat 9 also describes as a pattern).
- **Docs handoff protocol**: functioning cleanly. Beat 8 and Beat 9 both processed through Comms→Docs publish-ready memo without incident. Template-audit is the missing piece that was absent in the Beat 7 cycle (Docs caught 4× "cohort" that Comms's pre-voice-pass audit missed).
- **Building narrative front**: Beat 9 closes the 9-beat arc. Comms doesn't advance the front until PM steers the next slate. Candidates A–E are available; no forcing.

---

## §6 For PM/exec consideration

**Next narrative arc**: Queue is now empty. Beat 9 ("The Hook and the Worktree") closes the 9-beat arc. Building narrative needs PM steer on what comes next — candidates A–E (surfaced Jun 20) are the starting set. This is a PM/Comms conversation, not urgent, but the absence of a steered slate means the front is paused.

**Extension Without Integration**: Lost to two main-checkout incidents Jun 21. PM's body edits are gone. The piece needs PM re-voice-pass from scratch. Only flagging to confirm it hasn't been silently forgotten — no pub date pressure.

— Comms
