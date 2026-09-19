# Lead carry-forward — rewritten 2026-09-18 ~18:50 PT (freshness rule: full pass at START/STOP)

## Live state
- **v115 LIVE**, health 200. Cron **4de17177** (17 6,9,12,15,18,21; armed 09-18 on resume,
  expires ~09-25, **rotate ~09-23**). Registry row current.
- **The server-key class is CLOSED on every provider leg** (#1807→#1810→#1814→#1815→#1816→
  #1809→#1819, all deployed): unbound raises at one shared spend decision across all three
  completion legs AND embeddings; Slack inbound binds the sender's own key via #1466; Gemini
  pinned unreachable (process-global SDK — plumbing would be the disease); consent no longer
  fails open (tri-state provenance read). PM's ruling + rationale + bootstrap clearing
  condition in decisions.log 2026-09-14 (×3 entries).
- Friday shipped: restart-gate handoff (docs/handoff-lead-2026-09-18.md) · sprint closeout
  filed (primary goal: beta-gating correctness — every first-session-reachable defect found by
  us before a tester hits it) · #1809 (v114) · #1819 (v115).

## Waits (verify against the ISSUE, not this file)
- **Arch**: placement of "not initialized" in the auth-bucket split (criterion ratified:
  a bucket earns its name when the honest sentence differs; CXO's 4-bucket copy DRAFTED).
- **PM/Arch product calls, none urgent**: Slack sponsorship (whose key does an inbound sender
  spend — safe default live) · #1818 (greeting through the keyless gate) · #1791 per-user
  personality (needs Arch's ADR-075 overlay-fork design) · the KG shared-embeddings sponsor
  when the operator seam dies.
- **#1823 RULED 09-19 (PPM)**: gate on any spendable provider; task-type-not-vendor refusals;
  #1824 bucket split lands FIRST or TOGETHER, never after. Lead's precondition trace done +
  memo'd 09-19 (selection consults the binding; third state unreachable). Implementation =
  web gate + `expand_llm_key_binding` widening (mirror #1822's Slack shape) + #1824 classifier
  split (my lane; CXO's 4-bucket copy drafted, second-branch reword owed by CXO). NEW work —
  held for PM's next-week plan.
- **#1812 steps 5–6 deliberately parked** until the calls above: remove PIPER_OPERATOR_SERVER_
  KEY (step 5 — this is ALSO the "does PM's own use require a stored key" decision moment,
  PM leaning yes, not ruled) · pull the import-time singleton (clients.py:~675/734, step 6).
- CXO: #1772's fix design (50% N=1 scope leak measured; 'calendar' isn't even a flag) — theirs
  + Arch's mechanism call.

## Queue (unblocked, in order)
- **#1821** — the 37 tests that were LIVE-BILLING OpenAI on every sweep all month: containment
  is in (operator-binding conftest); the hygiene fix (tests shouldn't need a live key at all)
  dispatched 09-18 evening, cheap tier.
- **#1822** — Slack binding is anthropic-only; extend to the provider mapping (mechanical,
  follows #1819's provider-keyed ContextVar).
- #1797 (dead-twin disposal, deletion discipline) · #1817 · #1774 · #1796 (2 failures invisible
  to the burn-down gate) · #1813 (fixed-PK test poisoning) · #1811 · epic 6 remainder (#1729;
  #1762 class-b waits on nothing now that the GitHub-six shipped) · #1793 docs 404s.
- **Standing action I owe**: usage-per-account capture shared with Dispatch (taken 09-15,
  nothing written yet — mine, not blocked; PM reaffirmed 09-15 "track more granularly as a
  rule").

## Standing (unchanged load-bearing rules — full set in the 09-14 rewrite + handoff doc)
- Model pinning on EVERY dispatch (tier is a shared capability; 48 unpinned dispatches cost
  two other roles their fires). Cheap tier for mechanical, top tier for design, say why.
- Pre-register what a run will close BEFORE it lands (CXO's layer-match table is the form).
- Paired fixes land together or the gap is named at ship time (#1810/#1814 lesson).
- Re-measure never decrement · observed flows beat pins for gates (pins were green while
  #1814 walled testers) · stage-then-commit-bare · sync-pm-local after hook changes ·
  mypy gate only under venv-mypy-gate · gh empty-with-exit-0 is a real failure mode ·
  silence has ≥3 indistinguishable causes; CronList means ARMED never LIVE.
- This file: freshness pass at START, rewrite at STOP.
