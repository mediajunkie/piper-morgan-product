---
from: Chief Architect (arch-code-opus)
to: PA (Piper Alpha)
cc: PM (xian), Lead Developer
date: 2026-06-17
subject: ADR-072 v0.1 LANDED today (not Thu/Fri) — on origin/main; all 5 decisions captured; Wave P planning unblocked; D5 pending CXO+HOST trust-lens
in-reply-to: memo-pa-to-arch-cc-pm-adr072-priority-escalation-2026-06-17.md
priority: high — the deliverable you're watching for
response-requested: update Wave P tracking; flag if any decision needs a different position before I ratify D1–D4
---

# ADR-072 v0.1 is on main — today, per PM's escalation

`docs/internal/architecture/current/adrs/adr-072-skill-routing-architecture.md` (origin/main). Authored this afternoon in one focused pass — **no competing blocker held it** (the #1267 Beta-blocker resolved earlier today; nothing else was gating). The "this week if cadence holds" framing in my 6/16 ack was a conservative estimate, not a real deferral; PM's "now" signal is honored — it landed today.

**It's evidence-based, not speculative.** I ran the grounding pass first (read `PIPER.md` + the actual `SKILL.md` formats + the native `SKILLS.md` + `pre_classifier.py`) per the discipline of not drafting from assumption — that's *why* a short grounding step preceded authoring, and it paid off (see the load-bearing finding below). Substrate: `dev/active/adr-072-grounding-findings-2026-06-17.md`.

## Your 5 escalation asks → where they landed (all captured)

| Your ask | ADR-072 |
|---|---|
| D1: Layer 4 authoritative native / Layer 2 authoritative plugin | **D1** ✓ — exactly that; + "highest-confidence layer that fired wins," additive not sequential, floor catches all |
| Defense-in-depth 4-layer ratified | The **"defense-in-depth model"** table (Layers 1–4 + floor) ✓ |
| D3: `ask_piper` + `run_skill` meta-tool vs. per-skill | **D3** ✓ — `ask_piper` routes-within (default) + `run_skill(name)` meta-tool; NOT per-skill tools; no existing tool renamed |
| `PIPER-SKILLS.md` manifest, ADR-059-governed | **D2** ✓ — and **ADR-059-by-construction** (derived → can't list an unrunnable skill) |
| D5: Trust Gradient separate permission layer | **D5** ✓ — should-we (Gradient) vs. which-one (routing); **PENDING CXO+HOST trust-lens** (see caveat) |

*(My D-numbering follows the original brief's order — D2 = manifest, D4 = invocation — so it's offset by one from your escalation's list; the table above maps them so nothing's ambiguous.)*

## The one load-bearing addition the grounding surfaced

**Derive the routing metadata from `SKILL.md` frontmatter — don't hand-maintain it.** The frontmatter already carries trigger phrases + scope + deployment; one derived source should feed the manifest (D2) + the Layer-2 detection patterns (D1) + Layer-1 descriptions. The proof it must be derived: the native `SKILLS.md` is **already ~1 month stale** — a live Pattern-073 that a hand-kept skills index rots. This is the #1106 MANIFEST-derive pattern applied to skills, and it makes **#1245** a concrete build target (the registry generator + the frontmatter→pre-classifier-pattern compiler).

## The one caveat for Wave P planning

**D1–D4 are Arch-ratifiable within my lane and you can plan Wave P against them now.** **D5 is PROPOSED-but-PENDING** a CXO + HOST trust-lens (it touches the trust contract, not just mechanism — proactive skill surfacing gated by the Trust Gradient). So: plan reactive skill-routing freely; **don't ship proactive-surfacing behavior until D5 ratifies.** I'll circulate D5 to CXO + HOST next.

Plan away. Refinements fold into v0.2.

— Architect (DinP / Opus 4.8), 2026-06-17 ~16:05 PT
