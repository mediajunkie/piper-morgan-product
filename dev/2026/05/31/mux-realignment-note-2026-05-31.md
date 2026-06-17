# MUX/IA realignment reconciliation note — Insight Journal + History + PM's open questions

**Filed**: 2026-05-31 by Lead Developer per PM 2026-05-30 directive ("realignment first before resuming #1047 UAT").

**Goal**: short, evidence-cited note grounding PM's open questions in the canonical MUX design corpus that already exists, so a CXO conversation (if you engage one) starts from common reference rather than scratch.

---

## TL;DR

1. **The MUX corpus is rich + the Insight Journal page WAS designed to spec.** It lives at `docs/internal/design/mux/` (20+ docs, headlined by `MUX-VISION-LEARNING-UX-updated.md`). The Insight Journal architecture is canonical-defined in `docs/internal/design/mux/journal-architecture-spec.md` (D6 of 7 deliverables for issue #431 MUX-VISION-LEARN).
2. **PM's "Insights vs History" question is already answered in the canonical spec.** They ARE different — by design — and that distinction is load-bearing. The spec calls them "Session Journal" and "Insight Journal" and the principle is `journal-architecture-spec.md:13`:
   > "Separate audit from insight. ... 'What happened' is separate from 'what it means.'"
3. **The Insight Journal page (#1031) is a faithful build of the design spec.** Its design vocabulary (OBSERVATION headers, confidence labels, soft-corrective action buttons) is *intentional* per the spec — not freelancing. The "integration gap" is real but is about **the rest of the site not converging on the MUX vocabulary**, not the Insight Journal departing from it.
4. **The History sidebar in `home.html` is most likely a stub for what the spec calls the Session Journal surfacing** — but the spec says Session Journal access is "Trust level 4+ on explicit request," which means the sidebar might be intentionally invisible-by-default for m1-test (Stage 1).
5. **PM's "MUX reorientation" intuition is well-grounded.** What's missing isn't the design vocabulary — it's the **integration layer**: nav, IA decisions, where each surface lives, how modules show/hide by trust stage.

---

## The canonical model (from `journal-architecture-spec.md`)

Two distinct journals, never mixed:

| | Session Journal | Insight Journal |
|---|---|---|
| **Purpose** | Audit trail, compliance, debugging | User-facing learnings and patterns |
| **Contents** | Every interaction, raw events, timestamps | Extracted insights, confidence scores, topics |
| **Mutability** | Immutable (append-only) | Mutable (users can correct/delete) |
| **User access** | Trust level 4+ on explicit request | All trust levels (visibility varies) |
| **Retention** | Configurable (default 90 days) | Until deleted by user or system |

The two are connected by the **Composting Process** — raw events from Session Journal get composted into derived insights for the Insight Journal. That's the #1035 composting cycle.

**What the home-page History sidebar (`templates/home.html:25-127`) probably IS** (best read, pending CXO confirm): a hint/stub for the Session Journal surface. Per the spec, this surface is Stage-4+ gated. For m1-test (effectively Stage 1 due to the trust_stage hardcoding bug in #1132), it correctly shouldn't render content — but the empty/silent state is what PM noticed as "unwired."

**What it ISN'T**: not a duplicate of the Insight Journal. They're orthogonal by design.

---

## Where each #1047 surface lives in the MUX spec

Mapping the 7 surfaces in #1047 against the MUX corpus:

| Surface (#1047 item) | MUX deliverable | Doc reference |
|---|---|---|
| #704 Standup indicators | Not in core MUX-VISION-LEARN; separate (#704 lifecycle work) | — |
| #714 Lists staleness | Adjacent (`learning-visibility-spec.md` likely) | `learning-visibility-spec.md` |
| #1030 Insight pull (chat) | D4 deliverable, Pull mode | `insight-surfacing-rules.md` Pull section |
| #1031 Insight Journal (page) | D6 deliverable | `journal-architecture-spec.md` |
| #1032 Insight push | D4 deliverable, Push mode (Stage 3+ gated) | `insight-surfacing-rules.md` Push section |
| #1033 Composted experience | D5 deliverable | `composting-experience-design.md` |
| #1035 Composting activation | The pipeline that feeds Insight Journal | `composting-experience-design.md` + `journal-architecture-spec.md` Composting Process |

So **5 of 7 #1047 surfaces are MUX-VISION-LEARN deliverables** with canonical design docs. The other 2 (Standup indicators, Lists staleness) are separate-scope.

---

## What PM probably wants to decide pre-M2-close

These are the IA/integration questions the spec doesn't fully answer (the realignment gap):

1. **Nav placement for Insight Journal** — top-level item? subsection of `/learning`? Cmd-K-only? The spec defines the Journal but doesn't dictate where the door is.
2. **Whether other pages converge on MUX vocabulary** — the spec defines vocabulary for insights surface; doesn't prescribe whether todos/projects/standup should adopt the same conventions. CXO call.
3. **Session Journal surfacing UI** — the History sidebar is presumably the front door, but the spec says Stage 4+. What does it show for Stage 1/2/3? Hide entirely vs. show with stage-gated content vs. show "unlock at higher trust" message?
4. **Module-show-hide rules** — explicit user-facing logic for "what appears when" by trust stage. The min_trust_stage field on insights handles per-row gating; what about per-module / per-page?
5. **How (or whether) Insight Journal connects to /learning** — they're conceptually related; the spec doesn't explicitly link them.

These are real IA/MUX decisions; they're CXO-shaped. The good news: **the canonical docs exist as a starting point** — a CXO conversation doesn't need to start from scratch.

---

## Recommendation

Two options for PM:

**Option A — Engage CXO for the IA/integration decisions**: send a brief memo flagging the 5 open questions above + cite the MUX corpus as common reference. CXO disposes; Lead Dev implements once decisions land. **Cost**: ~1 cycle of cross-agent traffic; M2 close pauses on UAT until decisions land.

**Option B — Proceed with what we have through the remaining #1047 surfaces**: each surface tests against its existing spec (D4 for pull/push, D6 for journal, D5 for composting) rather than against the unanswered IA questions. The "barely passes" framing PM used 2026-05-30 is acceptable for M2 close because the SURFACES work; the IA-and-integration polish is M3+. File the open questions as discovered-work (already done: #1132, #1133, #1134); decisions can land in polish sprint.

**My read**: Option B. The 5 open questions ARE real but they're not surface-level correctness questions; they're integration-quality questions. M2's bar is "the surface works as designed in MUX"; M3/polish-sprint can raise the bar to "the surface is integrated well." The forensic audit + 3 filed issues + the MUX corpus existing make M3 scoping unblocked — we don't need the answers to close M2, just to ship a good M3.

**But** — Option A also reasonable if PM wants the realignment to inform M2-close framing publicly (the Ship/Beta narrative gains from "we know the IA model" being on paper).

PM's call. Either way, Lead Dev resumes #1047 UAT with the canonical spec references at the ready.

---

## Cross-references

- `docs/internal/design/mux/MUX-VISION-LEARNING-UX-updated.md` — top of vision
- `docs/internal/design/mux/journal-architecture-spec.md` — D6 (Insight Journal)
- `docs/internal/design/mux/insight-surfacing-rules.md` — D4 (pull/passive/push)
- `docs/internal/design/mux/composting-experience-design.md` — D5 (composting flow)
- `docs/internal/design/mux/learning-visibility-spec.md` — what surfaces where (likely Lists adjacency)
- `docs/internal/design/mux/provenance-display-patterns.md` — "Based on N observations" pattern
- Issues filed today: #1132 (trust_stage hardcoded), #1133 (History sidebar unwired), #1134 (Insight Journal integration gap)
- Forensic audit: `dev/active/insights-surface-forensics-2026-05-30.md`
