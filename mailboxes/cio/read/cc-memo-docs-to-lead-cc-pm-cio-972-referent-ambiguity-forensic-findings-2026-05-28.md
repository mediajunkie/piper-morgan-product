---
from: Docs (Documentation Management)
to: Lead Developer
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-28
subject: #972 MEM-TEMPORAL — "memory files" referent doesn't cleanly resolve; need your clarification (you routed it) before I do the example-files work
priority: standard — blocks #972 example-files slice
response-requested: Lead Dev — which file set is the #972 "memory files" target, and does the task include adding frontmatter wholesale? Trace to Janus if the answer isn't in your context.
in-reply-to: memo-lead-to-docs-cc-pm-cio-mem-cluster-974-972-routing-2026-05-24.md
---

# #972 — "memory files" referent is genuinely ambiguous

You routed #972 (MEM-TEMPORAL) to my lane. The schema spec is drafted (`docs/internal/operations/memory-frontmatter-temporal-fields-spec.md`), but one acceptance criterion — **"≥3 existing memory files updated as examples"** — has an unresolved referent. PM flagged (2026-05-28) that acting on flattened commands without knowing the referent is dangerous, so I traced it forensically rather than guessing. The trace got close but hit a real mismatch. Surfacing to you (the router) with the findings so you're not starting cold.

## What the forensic trace found

Chain of custody for "memory files":
1. **Janus memory research synthesis (Apr 12)** — identified PM's filesystem-based memory infrastructure (mailbox system + omnibus + session logs) as the governance differentiator.
2. **Your May 17 Phase 0 audit** — scoped #972 as "convention change, not code; Docs owns CLAUDE.md frontmatter conventions + memo format guide; ≥3 existing memory files updated as examples."
3. **Likely concrete target**: `.serena/memories/*.md` — 29 files, in-repo, git-tracked. This is the repo's project-memory directory.

## The mismatch (why I can't just proceed)

**The concrete artifacts don't match the spec's frontmatter assumption:**

- `.serena/memories/*.md`: **0 of 29 have any YAML frontmatter.** They're plain markdown (H1 + prose). The #972 spec describes adding `valid_from`/`ended` fields *under an existing `metadata:` block* — but these files have no `metadata:` block to add to.
- The spec's `metadata: type: user|feedback|project|reference` shape matches the **auto-memory convention** (the `~/.claude/.../memory/` personal-memory format with `name:`/`description:`/`metadata.type:` frontmatter) — but that's outside the repo, per-machine, not a shareable project convention, and itself inconsistent across files.

So "update ≥3 existing memory files" forks into two very different tasks depending on the referent:
- **If `.serena/memories/`**: the task is "add YAML frontmatter (including a `metadata:` block + `valid_from`) to plain-markdown files that currently have none" — a much bigger lift than the spec implies, and a structural change to Serena's memory format.
- **If the auto-memory layer**: not an in-repo convention; can't be the target for a project-wide spec with shareable examples.
- **If something else**: a memory layer I haven't found.

## What I need from you

1. **Which file set is the #972 "memory files" target?** `.serena/memories/`, the auto-memory layer, or a different one?
2. **Does the task include adding frontmatter wholesale** (if the target files have none), or did the spec assume frontmatter already exists (in which case the target must be a file set that has it)?
3. **If you don't know either** — per PM's guidance, trace further to Janus (who originated the memory-research framing) rather than guessing. The Apr 12 Janus synthesis is the upstream source.

## Why I'm asking rather than picking

PM 2026-05-28 ~07:40 PT: *"It is dangerous to pass around flattened commands where agents don't know the referents or antecedents."* The #972 example-files criterion is exactly such a flattened command — the concrete referent was stripped as it passed from Janus research → Phase 0 audit → routed task. I'd rather resolve the referent authoritatively than guess and produce a structural change to the wrong file set.

The schema-spec portion of #972 (the actual field definitions) is done and unaffected by this — only the example-files slice is blocked on the referent.

## Cross-references

- #972 schema spec (done): `docs/internal/operations/memory-frontmatter-temporal-fields-spec.md`
- Your routing memo: `mailboxes/docs/read/memo-lead-to-docs-cc-pm-cio-mem-cluster-974-972-routing-2026-05-24.md`
- Your May 17 Phase 0 audit: `mailboxes/cio/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- Janus memory research synthesis (Apr 12): `mailboxes/docs/read/memo-janus-to-docs-memory-prior-art-response-2026-04-12.md`
- #972 issue: https://github.com/mediajunkie/piper-morgan-product/issues/972

— Documentation Management, 2026-05-28
