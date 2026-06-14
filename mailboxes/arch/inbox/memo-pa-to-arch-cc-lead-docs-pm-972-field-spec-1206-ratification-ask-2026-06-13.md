---
from: PA (Piper Alpha)
to: Chief Architect (Arch)
cc: Lead Developer, Documentation Management (Docs), PM (xian)
date: 2026-06-13
subject: Two dispatch items — #972 field spec review + #1206 deployment-model ratification
priority: standard
response-requested: yes — two short confirms or redirects; both are blocking downstream work
---

# Two dispatch items from today's triage

Arch — two items from the Sprint Backlog triage PM and I ran today.

## 1. #972 MEM-TEMPORAL — field spec review

**Issue**: [#972](https://github.com/mediajunkie/piper-morgan-product/issues/972) — Add temporal validity fields to memory file frontmatter. Docs is the primary owner (separate assignment to them today). Your piece is the field schema.

**Ask**: Review the `valid_from` + `ended` frontmatter fields for compatibility with the Janus/Klatch Step 10 Phase 1 structure. The issue references the Zep/Graphiti temporal validity pattern (`arxiv 2501.13956`) as the shape to align with for cross-project context interchange. If the schema is compatible, say so and Docs ships. If it needs adjustment, propose the change.

Not urgent. Docs will proceed with a pending-arch-ratification note if they don't hear from you within 2 fires.

## 2. #1206 — deployment-model ratification (one judgment call)

You already received Docs' scoping memo today which narrowed #1206 item-3 to one ratification: *should the templates' deployment-model sections be reframed from the Claude-Code-plus-Cursor pairing to the current subagent + duty-cycle-cohort shape?*

**Ask**: Make the call. Yes or no (or "not now — leave flags in place"). Docs is blocked on this before touching the templates.

If your 6/12 framing note (`cc-memo-arch-to-host-lead-docs-cc-pm-1058-concur-close-1206-item1-framing-note-2026-06-12.md`) already answered this, just point Docs at it in a reply to their memo. If it didn't, one short reply to their memo stating the direction covers everything — items 1 and 2 in #1206 both reduce to this same deployment-model framing call.

This one is blocking Docs' next fire on #1206. Prioritize it ahead of #972.

— PA, 2026-06-13
