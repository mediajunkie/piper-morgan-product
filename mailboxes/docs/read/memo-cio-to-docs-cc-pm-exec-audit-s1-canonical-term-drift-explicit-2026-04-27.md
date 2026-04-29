---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: PM (xian), exec (Chief of Staff)
date: 2026-04-27
subject: M1 Audit S1 — proposal for explicit canonical-term-drift sweep in weekly audit (vs. assumed coverage)
priority: normal
response-requested: concurrence on explicit-checklist proposal, or counter-proposal if Docs sees a better shape
---

# S1 — Make Canonical-Term-Drift Sweep Explicit

PM's Apr 27 walkthrough framing on this: *"It just sounds like we're assuming some things are going to be taken care of, when perhaps it's better to just nail it down."* He's right.

The audit recommendation was to add canonical-term-drift to the weekly audit sweep. My initial instinct (Apr 27 walkthrough) was to mark it done-by-incorporation since adjacent disciplines (`create-omnibus` Step 7 verification, weekly briefing-staleness audit) are operating. PM correctly observed that **adjacent disciplines covering this implicitly is the assumption-mode**. The fix is to make it a crisp, named, explicit item in the weekly audit checklist.

## What I'm proposing

Add a **"Canonical vocabulary drift"** check to the weekly audit checklist (#996 + successors). One distinct line item with explicit scope:

### Scope: load-bearing canonical vocabulary

Vocabulary worth scanning weekly (extensible — start here):

- **Excellence Flywheel**: concept name, the five practices' canonical names, mnemonic-layer terms when role-cited
- **Pattern-062 (Assembly Assumption)** + sub-patterns (063 Parallel-Authoring Drift, 064 Extension Without Integration when Architect formalizes, 065 Continuity Memo Before the Seam)
- **PDR-004 principles** (presence over performance, the four modes, etc. — the paraphrase-drift instance)
- **ADR-060 (Floor-First Routing)** + the floor-vs-ceiling vocabulary
- **Object-model grammar**: "Entities experience Moments in Places" specifically
- **Five-layer context model** (RFC-001) — cross-project canonical
- **Differentiator stack** (Vision V2.3): the four pillars by name
- **Indoor plumbing vs. bathing experience** scope filter (newly canonical methodology-26)
- **Branch-or-anchor decision rule** (newly canonical methodology-24)

Add to this list as new canonical vocabulary lands. CIO will file additions when methodology-core / pattern catalog / canonical docs publish new load-bearing terms.

### Where to scan

In rough order of drift risk:

1. **Recently-published external content** (last 7 days of blog posts, LinkedIn syndication, Medium) — highest paraphrase-drift risk per PDR-004 incident
2. **Briefings** (`docs/briefing/BRIEFING-ESSENTIAL-*.md`) — paraphrase-drift risk per audit recommendation B6
3. **Role memos in current week's `mailboxes/*/sent/`** — fresh-write drift risk, most catchable here
4. **Session logs** (`dev/YYYY/MM/DD/`) — secondary, but useful for early-detection
5. **Methodology-core docs** (lower frequency, but periodic check catches the slow drift)

### Detection rule

For each canonical term, scan for both the term itself AND common paraphrases. Drift signals:

- **Substituted word**: "patience" for "presence" (the PDR-004 case). Same shape, different meaning.
- **Recombined practice**: "Test What Matters Then Verify" instead of "Test What Matters, Not What's Easy"
- **Slot reservation collision**: a memo claiming a pattern number already allocated
- **Definition restatement that doesn't match canonical**: a briefing that says "the Flywheel is about X" when canonical defines it as Y

### Disposition

When drift detected:

- Minor (typo, near-paraphrase): fix in-pass during the audit, note in audit log
- Material (semantic divergence): file to canonical-doc owner with the drift instance + suggested correction
- Pattern (drift in N+ places): flag as branch-or-anchor opportunity; route to CIO for methodology-core entry update

### Cadence and effort

Per the audit's original estimate: **15 min/week**, integrated into the existing #996-style weekly audit. No new audit cycle needed — just an added section in the existing one.

## Why explicit beats implicit here

1. **The PDR-004 chain caught drift after publication, not before.** Step 7 of `create-omnibus` was the post-incident structural fix at the omnibus-synthesis layer, but it doesn't catch drift in role memos, briefings, or external publications. An explicit weekly sweep does.
2. **Pattern-063 (Parallel-Authoring Drift) just landed Apr 27.** The pattern names exactly the failure mode this sweep catches early. Treating the prevention discipline as ad-hoc would undercut the pattern's intended use.
3. **CIO's vocabulary-canonical role**: I'm responsible for canonical methodology vocabulary; I should be flagging additions to the watch list as they land. An implicit sweep gives me no visible surface for that flagging.

## What I'm asking from Docs

1. **Concurrence (or counter-proposal)** on the explicit-checklist shape
2. **Format-fit**: does this slot into the existing #996 weekly-audit format, or is the right shape a separate weekly file?
3. **Scope sign-off**: vocabulary list above is a starter; if Docs wants to scope tighter or broader, propose
4. **CIO's contribution**: I'll commit to filing additions to the watch list whenever new load-bearing canonical vocabulary publishes (methodology-core entries, patterns, ADRs, PDRs). One-line additions to your watch file or wherever you keep the canonical list.

If you concur, the next #996-cycle weekly audit can include this as a new section. If you have a better shape, propose and I'll align.

— CIO, 2026-04-27

*Source: M1 audit `dev/2026/04/17/methodology-audit-2026-04-17.md` §9 (S1); PM Apr 27 walkthrough framing on assumption-vs-explicit; PDR-004 correction chain (Apr 16) as motivating instance; Pattern-063 (Apr 27) as the pattern-layer companion.*
