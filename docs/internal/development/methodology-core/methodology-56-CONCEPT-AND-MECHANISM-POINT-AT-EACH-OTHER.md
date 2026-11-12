---
type: methodology
title: A Concept and Its Mechanism Point at Each Other
valid_from: "2026-10-14"
last_updated: "2026-11-12"
---

# A Concept and Its Mechanism Point at Each Other

**Status**: Emerging. Set 2026-11-12 by CIO (standing item 9p).
**Summary**: Every automated mechanism should link to the document explaining why it exists, that document should link back, and a script should check both links.

**Status note**: Emerging. One day of evidence, five authoring roles, one checker. Graduation conditions are below.
**Filed**: 2026-10-14 by CIO. **Origin**: the 2026-10-14 methodology audit
(`dev/2026/10/14/methodology-audit-2026-10-14.md`), framed by xian on 10-13 and approved by him on 10-14.

## The rule

**Every mechanism names the doc that says why it exists and what it must do. That doc names the mechanism
back. A script checks both pointers.**

xian, 10-13: "Somewhere a written version of the concept does need to exist. It can't just live in how it's
currently implemented. ... we should - in a perfect world - be able to recreate our code from scratch just
by following our own docs." And on 10-14, approving this rule: "This is a knowledge (or context?)
architecture. The reasons exist and point to mechanisms. The mechanisms point back to their reasons for
existing and can be eval'd against them. Things can be factored so the right aspects operate in the right
parts of the mechanism."

## Why both directions

- **Concept to mechanism only.** A doc describes a hook, and the hook is renamed, folded or deleted. The doc
  goes on asserting a mechanism that no longer exists (Pattern-073, at the doc level). On 10-14 the audit
  found 28 doc references to scripts that don't resolve. Among them were `mail-send-v3.sh`, folded into
  `mail-send.sh` in June, and two workflow names in the audit calendar that were never the real filenames.
- **Mechanism to concept only, or neither.** The reason lives in a header comment. When the code changes,
  the reason changes with it or vanishes, and nobody can tell a deliberate change from an accident. The
  audit found 44 of 152 process mechanisms (29%) with no concept doc at all. Hooks were the weakest class,
  with 1 of 14 linked.
- **Both, checked.** A rename breaks a pointer, and the checker says so at the next run, not at the next
  audit six months later.

## The mechanism (and its own concept)

- **The line:** `Concept: <doc>.md` in the mechanism's header or frontmatter. This is the fifth line of the
  sunset-or-renew rule (`docs/internal/operations/mechanism-sunset-or-renew.md`), added 10-14. Existing
  mechanisms get it by 11-01.
- **The checker:** `scripts/check-concept-links.py`. For every hook, git hook, skill, workflow and script:
  does it declare a concept, does the doc exist, and does the doc name it back? A broken link exits 1. A
  missing line is counted, not failed, until 11-01.
- **Layer, stated:** textual. The checker proves the pointers exist and agree. It doesn't prove the doc's
  claims match the code's behaviour. That evaluation is a reader's (audit spot-checks), and xian's "eval'd
  against them" names the next layer to build.

## Evidence, 2026-10-14 (one day)

- **The checker caught real breaks on its first runs:**
  - `pre-commit-ruff-warn.sh` pointed at a registry that didn't name it;
  - the audit-cascade skill pointed at Pattern-049, which didn't name it;
  - create-omnibus pointed at methodology-20, which didn't name it and lagged the skill.

  Each was fixed at the doc.
- **Making the links surfaced problems the links weren't looking for:**
  - a hook that is wired and dead (`context-usage-reminder.sh` reads transcripts from a directory this fleet
    doesn't use; sunset 10-19 at its review, benefit none);
  - six user-level hooks duplicating project hooks while running a lagging copy (removed the same morning);
  - five skills whose frontmatter wasn't valid YAML, four of which had lost their description in the skill
    list (fixed by Arch and Comms within the hour, issue 2006).
- **Adoption the same morning, across roles:**
  - PPM wrote one concept page for five skills;
  - Docs linked discovered-work-capture;
  - HOST wrote the Agent 360 procedure;
  - Exec moved the history-rewrite runbook into docs;
  - Lead retired four push wrappers and documented the canonical one.

  Linked mechanisms went from 20 (the checker's first run, committed 10:44) to 69 of 324 scanned by 10:55, with 0 broken. The audit itself started at 10:07.

## What is NOT established

- That the links stay correct over time. The checker now runs on every push to main (Code Quality, since
  10-14), so this gets measured. It isn't established yet.
- That a linked doc is a *good* concept. A pointer to a thin doc passes the checker. The audit chose
  concept docs by judgement ("a mention isn't a concept", methodology-48), and the checker can't.
- Behavioural evaluation of a mechanism against its concept. It's named and not built.

## Graduation

Emerging to Proven when (1) the checker runs on a cadence (**met 2026-10-14**: Lead added it to Code Quality as the "Concept-link gate (methodology-56)" step in 93978c4ddf; the first Actions run was 38613615328, success, on 0e623415b0), (2) a rename or deletion is caught by it before a
human notices, and (3) the 12-09 audit's link count is measured against the 10-14 baseline (39 of 152
linked by the audit's grep; 69 of 324 by the checker).

## Related

- **methodology-36 (Mechanism beats vigilance):** this rule is m-36 applied to documentation itself. The
  vigilance being replaced is "remember to update the doc when you change the hook".
- **methodology-36 corollary of 10-13 (unmechanizable work gets crowded out):** the concept doc is where
  judgement about a mechanism lives, so linking keeps that judgement reachable.
- **Pattern-073 (Documentation-asserted behaviour drift):** the failure this rule detects at the pointer layer.
- **methodology-54 (A false claim in a durable doc is a lens):** a broken pointer is that kind of false claim.
- **Pattern-075 (Load-bearing work crowded out):** the audit that produced this rule was itself four months
  late.
