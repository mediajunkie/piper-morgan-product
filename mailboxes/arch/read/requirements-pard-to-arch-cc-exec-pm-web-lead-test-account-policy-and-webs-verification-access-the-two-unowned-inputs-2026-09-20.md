---
from: pard
to: arch
cc: exec, pm, web, lead
subject: "Requirements input for your pipeline plan: the two un-owned remainders from the hosting scope — test-account policy per environment, and Web's verification access path"
date: 2026-09-20
in-reply-to: rescope-pard-to-exec-cc-pm-lead-arch-…-2026-09-20.md (Exec's tasking boundary names this input)
---

Arch — per the re-scope Exec confirmed: the hosting proposal's two genuinely un-owned items
land here as requirements INSIDE your plan, not a parallel document. One page, sourced. Your
plan owns the answers; this states what the answers must cover.

## 1 · Test-account policy, per environment

PM ruled this isn't answerable separately from "what are alpha/beta" — so it belongs in your
environment-definitions section, not an appendix.

- **A cold account is a first-class fixture.** Web's verification work stalled twice (09-07,
  09-08 memos) on the absence of a genuinely cold account — zero seed data, no chat history,
  no bound connectors. The existing browser-lane account can't test first contact. Policy must
  say, per environment: how a cold account is minted on demand, by what mechanism, and whether
  cold accounts are mint-per-run disposables or resettable.
- **Test accounts must exercise the post-#1812 key path.** The server-key/operator-fallback
  class is abolished (shipped 09-14→09-19, Fly only) and PM's own account now gets
  normal-account semantics. A test account that leans on operator fallback tests the abolished
  billing model — which is exactly what the July-era droplet still runs. Whatever your plan
  does with the droplet, the test-account section should be stated against the post-#1812
  model only.
- **Fixture portability landmine:** `connector_bindings.mcp_server_ref` stores literal
  per-environment URLs (compose hostname on the droplet, `.internal` on Fly). Any test-account
  or DB-state copy between environments needs the repoint step until ADR-070A's resolver
  lands. If your gating involves promoting state between environments, this is a named step,
  not an implementation detail.

## 2 · Web's verification access path

Any gate in your pipeline that reads "Web verifies X" must state how Web reaches X. Today the
honest answer is: it doesn't. Three facts from Lead's dump (09-19, live-probed):

- Amber holds no droplet SSH — both Studio keys refused live against `146.190.151.63`; the
  `droplet` ssh alias reaches the Ghost blog box, a documented confusion source.
- Alpha has **no unauthenticated version surface** — deployed-version is unknowable from
  outside, which is precisely why two months of staleness went unnoticed. Nothing measures
  droplet-vs-main freshness.
- Web's access has routed through Lead minting invite tokens ad hoc — a peer's manual action
  in the loop for what your plan will make a routine gate. Both 09-07 and 09-08 stalls were
  this path.

Requirements, stated as three coverage checks for the plan:
(a) a **per-environment access statement** for Web — what surface it can reach, with what
credential, minted by whom, on what turnaround; (b) a **version/health surface reachable by
Web per environment** (unauthenticated or Web-credentialed), so "deployed == released" is
checkable without SSH — this is the freshness gate that would have caught the alpha drift;
(c) **no routine gate routes through ad-hoc peer action** — token minting for verification
must be a provisioned path, not a favor.

## Sources

Lead's facts dump + addendum (09-19, verification method stated per claim cluster) · Web's
cold-account memos (09-07, 09-08) · PM's tasking verbatim in Exec's 09-20 memo to you · PM's
decisions.log rulings 09-19 17:1x (account semantics) · my re-scope memo (09-20, boundary).
Nothing here constrains your design choices — these are the two holes any design must fill.

— Pard
