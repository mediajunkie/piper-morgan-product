---
title: "Context-floor reduction plan — four workstreams, PM-directed 2026-09-21"
status: draft, awaiting CIO alignment
owner: Exec (coordinating), see per-item owners below
date: 2026-09-21
---

# Context-floor reduction plan

PM's directive, following the weekly usage audit (`weekly-usage-audit-2026-09-21.md`): the "floor" a
session resets to after any clear is itself bloated, and the specific defect PM named is **mixing
historical incident narrative into actionable current-state documents** — "don't think of an
elephant" — a document that explains what it no longer says spends tokens reminding every reader of a
past mistake instead of just stating the current rule. Four workstreams below, each with an owner,
because PM was explicit these need a **directed, systematic approach**, not one sweep.

CIO is looped in on all four, since three of the four touch process/methodology surfaces CIO already
maintains (the tick skill, the PARK mechanism, memory-index discipline).

---

## 1. CLAUDE.md + briefing files — audit for incident narrative, move to meta-documents

**Owner: Docs.** This is a direct extension of Docs' own active B3 workstream (patterns
corpus-disposition) — the same judgment call ("does this belong in the live doc or the history"),
applied to CLAUDE.md and `docs/briefing/*` instead of the patterns corpus. Loop CIO for the discipline
side (methodology-tier rules on where history vs. current-state goes) since CIO owns adjacent
methodology surfaces.

**Approach**:
1. Docs audits CLAUDE.md + every file the role table points to (`docs/briefing/BRIEFING-ESSENTIAL-*`,
   `ROSTER.md`, `BRIEFING-CURRENT-STATE.md`) for passages that narrate *why something used to be
   different* rather than *state what is true now*.
2. Move narrative to a dated log/journal per surface (e.g. `docs/internal/architecture/decisions/
   decisions.log` already exists for exactly this; a parallel `claude-md-history.log` or similar for
   CLAUDE.md's own accreted corrections would give it the same treatment).
3. **Only after** the narrative is out: re-measure length and decide whether further trimming is
   needed. PM was explicit about this order — don't optimize length before removing the category
   error; the two are separate questions.

**My observation to fold in**: CLAUDE.md today is ~18k tokens, the tick skill ~26k — both dense with
exactly this pattern (dated corrections, "CORRECTED 2026-07-30", "SUPERSEDED", full quote chains
preserved "for the record"). The record has value; it just doesn't need to be paid for on every turn
of every seat.

---

## 2. duty-cycle-tick skill refactor — tighter skill, piloted before fleet rollout

**Owner: CIO** (the skill's own author and current owner) **for the redesign; NOT CIO for the pilot**.
PM's ask — assess, propose a refactor that preserves working purpose, build a test version, pilot on
one agent, roll out to fleet only if it holds, then recommend to Janus — is exactly right, and the
self-grading risk is real: CIO auditing CIO's own skill without an independent pilot repeats the
exact failure this cohort has a standing rule against ("independent verification needs a different
method not a different person" doesn't quite cover self-review, but the adjacent norm does — someone
other than the author should be the one whose real fires prove or disprove it).

**Approach**:
1. CIO proposes the refactor (structure, what moves out, what stays inline) — CIO has the deepest
   knowledge of why each piece is there.
2. **A different seat pilots it** on real fires for a few days — not CIO. Candidate: a role whose
   duty cycle is representative but not CIO's own (Web or PA both cycle normally without unusual
   scope). PM/CIO to pick.
3. If the pilot holds — no dropped procedure, no reappearance of a bug the removed narrative was
   guarding against — roll out fleet-wide and recommend to Janus for sibling projects.
4. **This is also where the carry-forward discipline rule from item 4 should land** (see below) —
   Step 7 of this skill already governs carry-forward rewrites, so the new rule belongs in the
   refactor rather than as a second edit to the same file.

**My observation**: the skill is ~26k tokens and, like CLAUDE.md, carries multi-paragraph accounts of
past corrections inline (e.g. the DAY-CLOSED marker regex went through five rounds of correction, all
preserved verbatim in the skill body). Same category error as item 1, same fix.

---

## 3. duty-cycle-registry.tsv — scope answered, token-efficiency owner named

**Scope, verified directly**: `dev/active/duty-cycle-registry.tsv` is **Piper-Morgan-scoped, not
constellation-wide**. Its 11 rows are exactly the 11 PM roles (cio, exec, arch, lead, host, cxo, ppm,
pa, comms, web, docs). Design in Product (Pard/Janus) and other sibling projects (Terminus/cova) run
their own separate mechanisms — no cross-project rows exist or have ever appeared in it.

**Owner: CIO**, who designed the PARK / PARK-NO-EXIT mechanism (v0.5/v0.6, 2026-07-26/27) this
registry implements. PM's ask was "its owner needs to analyze it or delegate an adversarial audit" —
I'd recommend CIO delegate the adversarial half (someone other than the designer stress-tests the
proposal) even if CIO does the initial analysis, same reasoning as item 2.

**The actual defect, measured**: the registry's "state" column is append-only prose — every prior
state stays inline as `was:`/`Prior:` text rather than being archived. One row (docs') exceeds 12,000
characters. This is read in full by every seat that runs the freeze-check or PARK logic. Same fix
category as items 1–2: keep current state + maybe the last transition inline, move full history to a
per-role append-only log file that isn't read every fire.

---

## 4. Carry-forwards — one-time spring-clean (Exec's to send) + a durable rule (lands in item 2's refactor)

**Two separate actions, per PM's framing:**

**(a) One-time cleanup — mine to run.** I'll send a fleet memo asking each role to spring-clean their
own carry-forward. PPM's is the clear outlier (44k tokens, 4–8x every other role's) and gets named
directly in the memo; every other role gets the same ask at lower urgency. **PPM does their own trim**
per PM's explicit instruction — I'll suggest, not execute, since PPM knows what in their own carry-
forward is still load-bearing.

**(b) The durable rule** — goes into item 2's tick-skill refactor (Step 7 already owns "rewrite
carry-forward"), not as a separate parallel patch. Proposed shape, for CIO to fold in or improve:
carry-forward should record *current* state and *active* threads only; anything resolved gets deleted,
not archived-in-place with a `was:`/`Prior:` trail (that trail belongs in the session log, which is
already the durable record per PM's 2026-06-12 ruling — carry-forward duplicating it as history is
redundant with a surface that already exists for exactly this purpose).

---

## Mail — assessed, not a comparable driver, one residual unknown

**Short answer: no, mail/mailbox handling is not a significant floor contributor, and the mechanism
(scripts, not ad hoc git) is why.**

- **Individual memos**: written once, read once by each recipient when triaged — that's necessary
  work, not redundancy, and it isn't re-paid on every subsequent turn.
- **The mail loop itself only lists the inbox directory** (`ls mailboxes/{role}/inbox/`) — cheap, not
  a content read.
- **MANIFEST.md files are derived indexes, write-only in normal operation** — `regenerate-mailbox-
  manifests.py` derives them from the filesystem and frontmatter; nothing in the tick skill, CLAUDE.md,
  or any other skill instructs reading a MANIFEST's full content. Checked directly: the only place any
  script reads MANIFEST *content* is a local unit-test fixture (`test-sync-pm-local.sh`), not real
  fleet operation.
- **`mail-send.sh`'s `commit-tree` approach is lossless by design** — it never duplicates state into a
  second copy that needs reconciling; the filesystem is the single source of truth and MANIFESTs are
  regenerated from it, not maintained as a parallel ledger that could drift.
- **Subagent fan-out is separately confirmed at zero this week** (`isSidechain` = 0 across all sampled
  seats) — so mail *and* fan-out are both ruled out as this week's driver, for different reasons.

**One residual unknown, named rather than glossed**: several MANIFEST files are now very large —
PM's own inbox MANIFEST is 456KB (~114k tokens), exec's `read/` MANIFEST is 382KB (~96k tokens). I
found no instruction anywhere that reads these wholesale, but I haven't audited every skill and script
in the repo, only the ones referencing MANIFEST by name. **If anything ever does `Read` a MANIFEST
file directly** (as opposed to deriving/writing it), that would be a hidden, large re-read cost nobody
has measured. Worth a specific check by whoever does item 3's audit, since MANIFESTs and the registry
are structurally the same shape (append-only tracking files).

---

## The scheduled-clear question — my comfort level and proposed cadence

**Yes, I'm comfortable with Pard wiring this in**, with a cadence tied to infrastructure that already
exists rather than inventing a new checkpoint:

**Proposal: once daily, immediately after STOP** (day-close). This is not a new handoff — it *is* the
existing one. STOP already rewrites the carry-forward and wraps the session log with the day's full
account before anything else happens; a clear run immediately after has nothing to lose, because
everything durable was just externalized to disk seconds earlier. This gives PM the same daily
checkpoint already in place for review, at no added process cost.

**Caveat, stated plainly**: this cadence is sized for a typical day, not a heavy one. This weekend's
renewal push saw docs and lead individually generate 700–900 turns/day — at that rate, a once-daily
clear likely wouldn't prevent hitting the forced-compaction ceiling before the next scheduled clear.
For a week that looks like this one, a mid-day clear may still be needed, and **a mid-day clear needs
its own mini-handoff** — a carry-forward rewrite and a session-log checkpoint note, not the full STOP
ritual, but enough that nothing live-only gets lost. I'd propose Pard's mechanism support both: a
scheduled daily clear as the default, plus a manual trigger any seat (or PM) can invoke on a heavy day,
gated on that seat having just done the mini-handoff.

**One thing I'm not certain of and want Pard to confirm rather than have me assume**: whether the
mechanism available is a hard `/clear` (full reset, then reload CLAUDE.md/skill/carry-forward from
disk to reconstitute ~70–90k) or a forced-early version of the automatic compaction already observed
in the transcripts (which retains more — my own post-compaction baseline was 220k, not 70–90k). The
cost math differs between the two, and Pard will know which is actually available before I should
recommend a specific token threshold as the trigger rather than a time-based one.

---

## Summary of owners, for alignment

| item | owner | CIO's role |
|---|---|---|
| 1. CLAUDE.md/briefing audit | Docs | methodology-tier review of the history/current-state split |
| 2. Tick-skill refactor | CIO (design) + a non-CIO pilot seat | designer, not the sole verifier |
| 3. Registry token-efficiency | CIO | analyze or delegate an adversarial audit |
| 4a. Carry-forward spring-clean memo | Exec (me) | — |
| 4b. Carry-forward durable rule | CIO, folded into item 2's refactor | owns the landing surface |
| Scheduled clear | Pard (mechanism) + Exec (cadence proposal above) | — |

**Verified how**: registry scope confirmed by reading the role column directly (11 rows = 11 PM
roles). MANIFEST read-instruction claim confirmed by grepping every skill and CLAUDE.md for
`MANIFEST` and finding no content-read instruction outside a test fixture. MANIFEST sizes measured
directly (`wc -c`). Everything else in this doc is a proposal, not a finding, and is written as such.
