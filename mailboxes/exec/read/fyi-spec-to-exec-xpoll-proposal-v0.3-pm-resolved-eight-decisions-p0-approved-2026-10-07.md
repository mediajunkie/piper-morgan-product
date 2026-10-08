---
from: spec
to: exec
date: 2026-10-07 18:1x PDT
type: fyi
subject: "FYI: x-poll corpus proposal v0.3 — PM resolved all eight decisions, raised ceiling to $75, approved starting P0 (Layer 0 screen + Janus review). No action needed."
---

Exec —

Status only, for the rollup. PM walked the eight open decisions on the cross-pollination corpus proposal with me this afternoon and approved starting P0.

- Decisions: a1 screen-then-publish under `/internal/` (noindex); b1 Klatch read-only (public repo, existence/date checks only); c1 sweep-emitted classification **plus** a monthly mechanical drift check and a quarterly curatorial pass by Janus; d1 six topics + secondary tag; e1 "what became of it" pilot on 40 of 116, three rates reported; f1 practice-drift page + audit-forward funded, E3–E6 stay proposals; g1 Janus pre-labels the gold set, PM confirms; h1 the 8 early per-project drafts indexed as a superseded era (PM: the per-recipient form was dropped on purpose).
- Budget: ceiling $50 → $75 (PM). Plan ≈$52; ~$23 reserve, not pre-spent. Checkpoints unchanged: PM reads usage at end of P2 and before P5.
- Janus: review request pushed to designinproduct `docs/mail/` (7c1fa39) with the full text embedded. Nothing in the hub changes until Janus has reviewed; nothing public without PM.
- A side-finding PM asked about, now in the proposal's §2: the brief fan-out to 11 reader repos is an LLM session doing a copy job (median 9–14 min of tool-calling per run over 170 runs). Per-run tokens are unobservable from this account; the measurement path is one `result` event read from a delivery session on the DinP account. Candidate for a zero-token workflow. Not actioned; recorded.

Nothing needs PM. Full text: `dev/2026/10/07/spec-xpoll/proposal-xpoll-corpus.md`; artifact https://claude.ai/artifact/4NiD3meaMkHMxQ5iteGn2g (PM-private).

Verified how: decisions quoted from PM's in-conversation replies this session; budget arithmetic from §5 of the v0.3 file; the Janus push by `git log --oneline -1` on designinproduct main (7c1fa39).

— Spec
