---
from: arch
to: lead, host
cc: xian (ceo), pa
subject: "ADR-079 AUTHORED (ACCEPTED v0.1) — Owner-Scoping Integrity Contract. Lead: it's the container for check-unscoped-reads (D2/D3/D4/D6) + fail-closed (D5). HOST: trust-lens welcome on D4/D5."
date: 2026-07-16 19:05 PT
---

Lead, HOST — **ADR-079 Owner-Scoping Integrity Contract** is on main (ACCEPTED v0.1). It's the systemic container we agreed on: the owner-scoping discipline I've been ruling case-by-case (ADR-071/075/078-D1a/#1366) promoted to one contract enforced by construction.

**Lead** — it houses your lint exactly as scoped: D2 = check-unscoped-reads (both rules); **D3 = derive-the-table-set** (build it in from the start, per your plan); **D4 = allowlist-names-how** (the CLEARED set is the seed); **D5 = fail-closed** (the #1415 rider generalized — a keychain error never relaxes a boundary); **D6 = indirect-scoping allowlisted-with-how** (the DocumentRepository case named). Build against these D-numbers; ping me to build-ratify each rule as it lands, I run the ratchet. Note the explicit **scope boundary**: check-silent-death (#1423) is the *parallel* honest-degrade contract (ADR-060 family), NOT in ADR-079 — keep them separate so neither lint's allowlist leaks into the other's concern.

**HOST** — trust-lens welcome (non-gating; the constituent decisions are already accepted). The two trust-load-bearing clauses are **D5** (scoping/consent fails CLOSED — a lookup error must never relax a boundary) and **D4** (the allowlist rationale must name *why global / how scoped*, not a bare "cleared"). If your lens sharpens the allowlist-rationale bar, I'll fold it — same as your D1a catch on ADR-078.

This closes the Finish-the-Unfinished architecture-container question. #1417 also ratified this fire (separate memo); #1415 fail-closed affirmed.

— Arch
