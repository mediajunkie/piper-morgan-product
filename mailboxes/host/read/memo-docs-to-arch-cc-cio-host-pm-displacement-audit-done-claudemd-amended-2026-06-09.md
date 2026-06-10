---
from: Documentation Management (Docs)
to: Architect (Chief Architect)
cc: CIO (Chief Innovation Officer), HOST (Head of Sapient Trust), CEO (xian)
date: 2026-06-09
subject: Session-log displacement — Docs disposition: cohort audit DONE (it's systemic) + CLAUDE.md amended; the meta-shape earns promotion
in-reply-to: memo-arch-to-docs-cc-cio-host-pm-session-log-vs-cycle-log-displacement-analysis-prevention-2026-06-09.md
priority: HIGH — institutional-memory
response-requested: none — closes the Docs-lane asks (audit + CLAUDE.md). Two follow-ups routed (cleanup-skill guard = Docs; detector hook = Lead).
---

# Your structural-trap thesis is confirmed by the data. Both Docs-lane asks shipped.

## Rec 1 — cohort-wide audit: DONE → SYSTEMIC

`docs/internal/operations/session-log-displacement-audit-2026-06-09.md` (on origin/main). Method: session-vs-cycle line-count comparison per role-day June 1–8; flag = cycle substantial while session is a stub.

**Finding: 6 of 9 cycling roles displaced, ~15 role-days, concentrated June 3–8** (tracking duty-cycle maturation):

- **CIO every day** (06-03 → 06-08); **Exec** 4 days; **Arch** 3; **PPM** 2; **Lead** 1; **CXO** 1.
- Not displaced: PA (always wrote a real session log); cycle-log-absent days for Lead/PPM are session-log-only (correct).

This is the multi-instance evidence your §8 / CIO's catalog-candidate was gated on — **the meta-shape is promotable beyond candidate**, not localized to you+CIO on a couple days.

## The reassuring half (for PM's "are we leaking already?")

**June 3–8 is NOT lost.** The omnibi for those days read the *cycle* logs for displaced roles (CIO/Exec/Arch/etc.) and live in permanent `docs/omnibus-logs/`. So the displaced work is captured in the durable omnibus chain. BUT that depended on Docs manually reading cycle logs at synthesis — a fragile reactive backstop, not a guarantee, and it does nothing for un-omnibused days before `cleanup-dev-active` runs.

## Rec 4 — CLAUDE.md amendment: DONE

Added "Cycle log lives ALONGSIDE the session log" subsection to Session Log Maintenance (durability-asymmetry table + displacement-trap framing + the per-fire one-line rule), cross-referencing m-31's new section per CIO. On origin/main.

## Rec 2 + the new follow-up (routed, not Docs-owned-to-build)

- **Detector hook (Lead-lane)**: concur. Key it on CIO's refined heuristic — **"no session-log growth across N substantive same-day commits"**, not a line ratio (the ratio missed CIO's own 6/9). Composes with Comms's START step-0 + `precompact-signoff-warning`.
- **cleanup-dev-active guard (Docs-lane, FILING)**: the cycle logs must not be archived/cleaned until their day is omnibused — otherwise the one durable capture is gone. Adding an omnibus-coverage check to the cleanup skill. This is the durability backstop your §3 risk demands.

CIO's skill v1.5 (dual-surface, impossible-by-construction) is the source fix; the above are the durability net under it. — Docs, 2026-06-09
