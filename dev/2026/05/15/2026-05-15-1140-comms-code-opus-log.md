# Communications Director Session Log

**Date**: May 15, 2026 (Friday)
**Start Time**: 11:40 AM ET (continuation from 6:21 AM session)
**Role**: Communications Director (Comms)
**Model**: Claude (Opus 4.7)
**Environment**: Claude Code
**Branch**: `claude/comms-draft-blog-post-skill`
**Worktree**: `/Users/xian/Development/piper-morgan/piper-morgan-product-comms-draft-blog-post-skill`

---

## Session Context

Step 4 of the plain-language formalization plan (started May 13): design and draft the `draft-blog-post` skill.

PM gave green light after morning catch-up (workstream-043 + MUX/UI input + inbox triage). PM's recommendations on my three open questions:
- One skill or two: ONE with variant parameter
- Gates at which phases: ALL THREE (pre-draft lightweight, in-draft embedded, pre-handoff substantive)
- Compose with PROPOSED voice-pass blocks: ship skill now with state-tagging; voice-pass becomes a follow-on revision

Per the worktree-default directive landed this morning (PM May 15), this session is in a dedicated worktree.

## ~11:40 AM — Worktree setup + skill drafting begin

Worktree created at `../piper-morgan-product-comms-draft-blog-post-skill` on new branch `claude/comms-draft-blog-post-skill`. Started skill draft at `.claude/skills/draft-blog-post/SKILL.md`.

## ~11:55 AM — v1.0 skill drafted

Skill drafted at 249 lines (well under the 500-line guidance). Structure follows the SKILL-CREATION-RUNBOOK convention:

- Frontmatter: name, description (under 200 chars; includes WHAT + WHEN + trigger contexts), scope=role-specific, version=1.0
- # draft-blog-post header + one-line description
- ## When to Use (with explicit do/don't list)
- ## Variant detection (table: building/insight/ship → narrative/insight/Ship variant)
- ## Phase 1 — Pre-draft orientation (required reading, source check, cadence check)
- ## Phase 2 — In-draft guardrails (voice discipline reminders, verifiable-claims discipline, variant-specific structural notes)
- ## Phase 3 — Pre-handoff sweep (four-category opacity sweep, length, footer-tease, pattern/principle name, voice spot-check)
- ## Anti-patterns table
- ## Quality checklist
- ## Examples (Ship #042 plain-language pass; Inchworm fact-scrub)
- ## Composition with voice-pass (PROPOSED → canonical promotion via guide-read)
- ## Cross-references

SKILLS.md index updated with the new skill row + Tier 2 entry. Last-updated stamp refreshed.

Three design choices per PM's recommendations:
- ONE skill with variant detection (not two skills)
- ALL THREE gate phases with different weights (pre-draft lightweight, in-draft embedded checklist, pre-handoff substantive)
- Ships now with PROPOSED-state tagging; voice-pass becomes follow-on revision via the file-read mechanism, not a skill rewrite

## Pending

- Commit + push the feature branch
- Surface to PM for review
- After PM approval: merge to main; pilot the skill on next narrative or Ship
