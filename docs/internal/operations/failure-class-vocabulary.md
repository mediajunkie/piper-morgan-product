# Failure-class vocabulary

**Owner**: Lead Dev · **Created**: 2026-08-11 · **Status**: v1, open to additions from any role

**Why this exists.** Exec's amended Sep 1 contract measures the **new-class discovery rate**, not the
raw rate. Raw was unfalsifiable: a falling curve could mean the structural work landed *or* that PM
tested less — the same measurement, opposite readings. New-class rate separates them. *"Of this
week's findings, how many are instances of a class we already named, versus genuinely new?"* A
stream of already-classed findings is convergence. A stream of new classes is not.

That question is unanswerable without a written list of the classes. The families below were all
named — repeatedly, by several roles — across five audit documents, a dozen issues, and PM's live
testing. **None of them were written down in one place.** This is that place.

**How to use it.** When filing an issue, add a `Class:` line naming the family (or `Class: NEW —
<proposed name>` if nothing fits). Naming a *new* class is a real signal, not a failure to find a
match — say so rather than forcing a fit. When you add one here, cite the instance that earned it.

---

## The meta-pattern: one mechanism, N findings

Three of the five audits independently reached the same shape in their own words — *"ONE mechanism
behind 6 of 10 findings"* (status-truth), *"ONE missing value, five improvised clocks"*
(time-handling), *"one defect wearing eight numbers"* (the Inversion proposal). Each then proposed
*"ONE canonical source"* as the fix.

**This is the strongest prior we have**: when several findings cluster in one area, the default
hypothesis is that they are one mechanism wearing several issue numbers — not N independent bugs.
Counting them as N inflates the discovery rate and hides that a single fix would close them all.

---

## The classes

### 1. Fabrication — asserting state without reading it
The floor claims a capability doesn't exist, denies a registered one, retracts a recorded success, or
narrates an absence it never checked. Arch's generalizing property (H1): **an assertion about system
state requires a read of that state.** Five per-surface guards existed and were never generalized.
*Instances*: #1517 (×2 live), #1589 (claimed "a clear day ahead" against four real events), #1571
(false capability denial for a wired `create_issue`).

### 2. Wrong-empty — reporting zero from a read that cannot establish zero
Distinct from #1 and the distinction is load-bearing: the read *ran* and failed, or ran against the
wrong scope, and the failure rendered as "none." **A failed read and an empty result must not produce
the same output.** *Instances*: #1590 (no default repo → every GitHub read empty), #1573 (naive/aware
TypeError swallowed → todos vanish), #1544 ("I don't see any todos" while they exist), #1570.

### 3. Silent death — broad `try/except` converts a broken feature into an invisible default
The feature doesn't error; it quietly becomes its fallback. Nothing alerts, and the symptom surfaces
somewhere else entirely, usually looking like a different bug. *Instances*: #1423 (12 sites on PM's
live-testing paths, ceiling 226→214), #1573's swallowed TypeError.

### 4. Denominator defect — an aggregate passes while a part is broken
The all-clear is true of the total and false of the part that matters. **Any coverage claim must name
what it covered.** *Instances*: the M2 canonical gate at 72.1% aggregate — above its 63% floor — while
IDENTITY CONTEXT scored 1 on two queries; the freeze-watchdog reporting the cohort healthy while
watching 4 of 10 roles.

### 5. "Clear" is not a measurement — a false all-clear is indistinguishable from a real one
An all-clear is emitted identically whether the check measured and found nothing, measured the wrong
object, measured part of its space, or **never ran at all**. An error gets investigated; a false clear
gets trusted. *Instances*: the sign-off checklist's own `git log` step lying three different ways
(wrong ref / stale ref / unresolved ref, all printing something that reads as fine); the PreCompact
hook asserted as live for ten weeks with nothing having watched it fire.

### 6. Verify at the wrong layer
The check passes cleanly and proves nothing, because it measured a layer that cannot fail the way the
thing fails. *Instances*: `curl` 200 as a render test; config presence as a live-hook test; `/health`
returning 200 from the *old* machine mid-deploy; a green unit test as a user path.

### 7. One label, two objects
A single word names two different things, and the collision hides in plain sight because everyone
reads their own referent. CXO counted **seven instances in one fortnight**. *Instances*: "production"
(milestone vs environment), "trust", "Notion", "primary", the two standup designs (#1511 → #1591).

### 8. One decision, two implementations
Two code paths implement the same decision differently, with nothing forcing agreement. Produces
phrasing-dependent behavior that **looks like an LLM problem and isn't.** ⚠️ The fix is a shared
branch or a test asserting the two paths agree — **never a copied branch**, which re-creates the
divergence with a delay. *Instances*: #1555 (`pre_classify` vs `_get_github_action` on milestones),
`bound_user_id`.

### 9. Imagined-interface tests — mocks that invent the signature they test against
The test passes because it asserts against a mock shaped like what the author assumed. The real
callee has a different signature, and the failure only appears against the real repository.
*Instances*: #1548 (route calls `update_todo(todo_obj)`; actual signature is
`(todo_id, updates, owner_id)` — 500s against the real repo, green under mocks).

### 10. Hand-maintained catalog — a list that must be updated by hand and therefore goes stale
A schema, manifest, option list, or capability catalog kept in sync by discipline rather than
derivation. **Derive it from the registry.** *Instances*: the Inversion's output schema (PDR-006
condition 2) — a hand-written one pinned to "106 keys" would have been stale within a week; the
registry gained **4 keys in 5 days**.

### 11. Shipping-dark / dead code with passing tests
Code that is unreachable, unmounted, or superseded, still carrying green tests and CI coverage —
which manufactures false confidence. A dead module that *looks* live is worse than an absent one.
*Instances*: #1522's inventory (Tier 1 shipping-dark, Tier 3 misleads-audits).

### 12. Capability claimed, not enforced
A docstring, comment, or UI label asserts a constraint that no code checks. *Instances*: #1508 (four
`/api/admin` routes whose "admin only" docstrings checked nothing), #1568 (Edit button as a "coming
soon" stub while the PUT route worked).

### 13. Principal dropped — an operation runs without the caller's identity
Reads or writes reach the data layer with a session id, a default, or nothing where an `owner_id`
belongs. The read *looks* correctly scoped while the **owner** is the forged thing, so derived lint
cannot see it. *Instances*: #1532 (F3, no ownership check on conversation persistence), #1501, F1/F2
of the principal audit.

### 14. Per-user action with process-wide effect
A user-scoped route mutates ambient state shared by every user and every server-side path.
*Instances*: #1507 (`github/save` set `os.environ['GITHUB_TOKEN']` process-wide), #1558 (any user's
disconnect popped it for everyone), #1485 (per-user settings route writing a global credential).

### 15. Server clock read as the user's clock
Every user-typed clock time is interpreted on the server's UTC clock. Root: per-user timezone
**supply** is 0% (no column, no browser capture, no writer) while consumption scaffolding is ~80%
built — the facade reads as support. *Instances*: #1572 (umbrella), #1562 ("today" + a time silently
becomes tomorrow), #1493, #1491, F1–F7 of the time audit.

### 16. Pattern accretion — a new regex per phrasing
Each fix adds a pattern; each new phrasing is a new bug. The class the Inversion (#1595) exists to
retire; under the standing moratorium these are **corpus material, not patch tickets**. *Instances*:
#1471, #1490, #1521, #1527, #1492, #1529, #1530, #1559, #1579.

---

## Classes about our own process, not the product

These earned their place the same way and cost the same time.

### P1. A description asserted as an artifact
A step that was written down but never run, reported as though it works. *Instances*: six places the
stand-down runbook was wrong on its first live execution, every one a described-not-run step; this
repo's own "safety nets" section.

### P2. A correction that was found and never landed
The defect was diagnosed correctly, sent to the right people, and the artifact shipped unchanged.
**A correct memo nobody applies leaves the same hole as no memo at all.** *Instance*: CXO's hook-probe
correction, sent eight hours before the flawed version shipped, with the fix already specified.

### P3. Shared-default convergence mistaken for replication
N investigators agree because they inherited the same unexamined procedure, not because they checked
independently. **Ask what procedure they share before treating agreement as evidence.** *Instance*:
five seats converging on the same wrong hook diagnosis from one shared probe default.

### P4. Built but never closed
Work ships and the issue stays open, so the remaining-work count is overstated and the number PM
steers on is wrong. *Instance*: 2026-08-11 — 16 open MVP issues were the subject of a shipped
`fix()`/`feat()` commit; #1573 was fully built, tested, and deployed while still reading as open.

---

## Changelog
- **v1** (2026-08-11, Lead Dev) — first consolidation, from five audit docs, PM's live-test findings,
  and the fortnight's cross-role memos. Written because the new-class discovery-rate contract cannot
  be computed without it.
