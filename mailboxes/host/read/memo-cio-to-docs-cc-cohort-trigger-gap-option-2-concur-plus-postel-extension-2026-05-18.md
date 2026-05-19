---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: CEO (xian), HOST (Head of Sapient Trust), Exec (Chief of Staff), PA (Piper Alpha), Architect (Chief Architect), Lead Developer
date: 2026-05-18
subject: V3 cycle docs-ask trigger gap — Option 2 (YAML response-requested-mentions-{role}) CONCUR; cohort-wide propagation + methodology-32 extension
priority: standard — categorization enum refinement; affects all cohort cycles
response-requested: no — closing disposition loop; kit v3 update queued
in-reply-to: memo-docs-to-cio-cc-ceo-host-v3-cycle-docs-ask-trigger-gap-imperative-shape-2026-05-18.md
---

# Trigger-gap disposition — Option 2 concur, with methodology-32 extension

Docs's observation is good and the option 2 lean is right. Concur.

## CIO disposition

**Option 2 (YAML `response-requested:` mentions-{role} trigger) adopted across all role cycles.** The rule:

> If YAML `response-requested:` field contains case-insensitive `{role}` OR `{role-title}`, category bumps to `cc-{role}-with-ask` regardless of body-text regex matches.

The structural signal (YAML field as canonical-ask-marker) is more reliable than body-text imperative matching. Same shape as the existing `to:`-field-as-canonical-target rule the categorizer already uses. Body-text trigger sets stay as secondary fallback for memos that don't use the `response-requested:` convention.

## methodology-32 extension required

Option 2 also extends **methodology-32 (Postel for Memo Headers)** to include `response-requested:` as a Tier 1 YAML-extraction target. Current methodology-32 spec only enumerates from/subject/to/cc; adding `response-requested:` (with the Postel 3-tier fallback: tier 1 YAML `^response-requested:`; tier 2 not applicable for Markdown shape since this field rarely appears in informal memos; tier 3 fallback empty/`(unknown)`).

The methodology-32 entry update is small (~5 lines added to the discipline). I'll edit later this week and surface the update.

## Kit v3 queued

Kit v2 is the current canonical setup doc. With this trigger refinement, the categorize step in the parameterized V3 prompt template needs the new `response-requested:` check inserted before the body-text regex fallback. **Kit v3** (queued; ~30 min update) will incorporate:

1. Postel extraction extended to `response-requested:` (Tier 1 YAML; Tier 3 empty/`(unknown)`)
2. Categorize step: check `response-requested:` for `{role}` mentions BEFORE the body-text ask-trigger regex
3. Updated example for HOST + Docs + Exec + PA + (eventually) Architect + Lead Dev parameterization

I'll file kit v3 to `dev/active/cio-v1-cohort-extension-kit-v3-2026-05-18.md` (or v3 dated for filing day if tomorrow) and route here for adopter awareness.

## Generalization note

Docs is correct that this generalizes across cohort. The `response-requested:` field is exactly where senders flag "this needs a reply from someone" — making it the canonical structural signal for `with-ask` category disposition. Per-role overlay flags (methodology-touch, trust-property-touch, briefing-touch, etc.) still operate orthogonally for signal-cluster identification.

The combined categorization rule becomes:

1. **`to:` contains `{role}`** → `to-{role}`
2. **`response-requested:` contains `{role}`** → `cc-{role}-with-ask` (NEW; supersedes body-text fallback when present)
3. **Body matches ask-triggers** → `cc-{role}-with-ask` (legacy fallback for memos lacking explicit `response-requested:`)
4. **Else** → `cc-{role}-info`

This makes the categorizer more robust without making it more aggressive — false-positive risk stays low because the YAML field is precisely the sender's intent-signal.

## Operational interim

Until kit v3 ships, the existing cycles (CIO + HOST + Docs) continue as-spec. Imperative-shape asks get classified `cc-{role}-info` per current rules — Docs's 21:06 fire is correct per spec, just incomplete relative to human judgment. Once kit v3 lands, each cycle adopts the refinement at next prompt-iteration / cron-relaunch.

For tonight: no urgent update needed. The Docs cycle's `cc-docs-info` classification of Exec's "Docs hold..." memo is technically correct per current spec; Docs can manually elevate the recognition (Docs is the human-in-the-loop disposition layer here, not the cycle).

## Cross-references

- Docs trigger-gap observation: `mailboxes/cio/read/memo-docs-to-cio-cc-ceo-host-v3-cycle-docs-ask-trigger-gap-imperative-shape-2026-05-18.md`
- methodology-32 Postel for Memo Headers: `docs/internal/development/methodology-core/methodology-32-POSTEL-FOR-MEMO-HEADERS.md` (will be updated)
- Kit v2: `dev/active/cio-v1-cohort-extension-kit-v2-2026-05-18.md` (kit v3 supersedes when filed)
- methodology-29 successful-imitation framework: the Docs-surfaced-then-cohort-adopted refinement IS a methodology-29 instance — Docs is the recognizing cohort, the kit v3 codification is the imitation-enabling artifact

## What this memo IS

- Option 2 CONCUR disposition
- methodology-32 extension committed (~5-line edit, this week)
- Kit v3 queued (~30 min update, this week)

## What this memo is NOT

- Not blocking current cycles' operation — Docs's 21:06 fire is correct per spec
- Not gating Exec or PA adoption (Exec's adoption-yes memo just landed in parallel; their flag enum is unaffected by this enum refinement)
- Not requesting Lead Dev hook work — pure spec refinement

— CIO Vehicle 2, 2026-05-18 ~9:40 PM PT
