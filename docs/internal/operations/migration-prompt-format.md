---
title: Agent Migration Prompt Format — the canonical handoff/bootstrap template
status: CANONICAL (CIO, 2026-06-18) — codifies the format used across the May–June migration wave (9 cohort pairs) + validated cross-project by Janus (Design in Product)
owner: CIO (migration-discipline lane)
last_updated: 2026-06-18
last_verified: 2026-06-18
valid_from: 2026-06-18
---

# Agent Migration Prompt Format

**Why this doc exists:** the format below was applied across ~9 cohort migrations (PA, Exec, Lead, HOST, Comms, Docs, Web, Arch, CXO; May–June 2026) and lived only *implicitly* in the individual handoff/bootstrap pairs — extracted-by-instinct each time, never designed once. Janus (sibling project) requested it 2026-06-16, drafted Janus's migration in it, and confirmed two of its rules earned their place immediately (below). This codifies it as a reusable, designed artifact — cohort **and** cross-project.

## The shape: TWO prompts, not one
A migration is a session handoff across an account/model boundary. Two prompts do two jobs — **keep them separate** (conflating them is how state gets lost):
1. **BEFORE / HANDOFF** — pasted into the **outgoing** session. Makes it *capture → clear → push → report* so nothing is stranded. Output = confirmation the old session is safely closed.
2. **AFTER / BOOTSTRAP** — pasted as the **first message** to the **incoming** session. Re-anchors the persona, points at durable state, lists the first concrete tasks. Output = a report-back confirming the new session is operational.

## HANDOFF (before) — required fields
1. **Migration-intent preamble** *(most load-bearing)* — "you're moving accounts/model; do NOT preserve your old operating-model variant; re-anchor on canonical." The wave's #1 failure was the **variant-preservation trap** (a session carrying forward a stale way-of-working it should have dropped — see m-41). Name it explicitly.
2. **Update continuity surfaces** — rewrite the read-at-session-start state to current (carry-forward / standing-items / pulse-log / backlog — whatever the role's durable state surfaces are).
3. **Close the logs** — day-close to the durable record + the grep-able `<!-- DAY-CLOSED: {date} -->` marker.
4. **Clear the cron** — CronDelete the active duty-cycle job so it can't fire orphaned (the successor re-registers it — see bootstrap).
5. **Commit + push EVERYTHING** — verify nothing stranded (`git status` clean; right branch; `main..HEAD` empty). Run-and-read, don't assume.
6. **Report back** — 1-line continuity recap + open threads handed off + the **non-obvious residue** (next).

### The non-obvious-residue field (the one files don't carry)
"What I'd tell a colleague covering my desk tomorrow that isn't written anywhere": in-flight judgment, the half-formed thread, tacit operational muscle-memory. For a role whose state already lives in durable files, the rest of the handoff is light and **this** is the load-bearing field — give it a named, required slot so it's designed, not extracted-by-luck.

## BOOTSTRAP (after) — required fields
1. **Role identity** — who you are, account, model (confirm the exact version/tag at launch — accounts/models churn).
2. **Canonical operating-pattern pointers** — the single source of truth + a conflict rule ("where this brief and an older doc disagree, the canonical doc wins").
3. **Pre-work re-validation** — `date` + `git branch` (or role equivalents) before acting.
4. **Steps** — open session log → read continuity → mailbox/inbox sweep → **re-register the cron** → token row → report-back.
5. **Inherited blocked-tasks slot** — the "do this first thing on the new account" items (a staged task blocked until the new environment exists). *Validated by Janus 6/18: gave a previously-homeless blocked task (floating in a log's PENDING section) a designed home — the extracted-vs-designed difference in one concrete case.*
6. **Recovery-playbook pointer** — for inherited muscle-memory (manual-fallback procedures, etc.): point at the playbook, don't re-derive it.
7. **PM-gated note** — what needs PM ratification vs what's pre-authorized.
8. **Report-back checklist** — session-log path · cron (id + expr + first-fire) · mailbox (X/Y) · one new-environment observation · resumed threads.

## Two load-bearing rules (both Janus-validated 6/18)
- **Cron expression as a literal CONSTANT in the bootstrap.** Embed the exact expression + fire-prompt, NOT "re-register your usual cron" / "it was {id}-shape." The self-heal re-arms from the prompt — a remembered/approximate expression silently drifts the cadence. *(Janus: "exactly the drift-prone recall you warn against — embedding the literal expression + the exact fire-prompt is strictly better. Adopting.")*
- **The inherited-blocked-task slot** (bootstrap field 5) — gives staged-blocked items a designed home instead of letting them float in a log section where they get lost.

## Provenance + reuse
- **Extracted from** the May–June 2026 cohort wave (9 pairs in `dev/active/{role}-{migration-handoff,bootstrap-brief}-*.md`); the "what every bootstrap carries" lessons list in `dev/2026/06/19/cohort-plan-of-record-2026-06-12.html` §5 is the in-wave precursor to this doc.
- **Validated cross-project** by Janus (Design in Product, 2026-06-18) — the format transferred to a different substrate (local-cron-on-host, state-in-durable-files) with only context-fitting, not structural change.
- **Reuse**: cohort future migrations (model changes, account moves) + cross-project. Fit the load-bearing fields to context; don't drop them.

— CIO, 2026-06-18
