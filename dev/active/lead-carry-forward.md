# Lead carry-forward — rewritten 2026-09-18 ~18:50 PT (freshness rule: full pass at START/STOP)

## Live state
- **v116 LIVE on Fly**, health 200 (deployed 09-19 morning). ⚠️ alpha.pipermorgan.ai (the
  droplet, the actual tester surface) likely runs a JULY cut — no droplet deploy since the
  07-12 cutover found in any log; version-read + upgrade plan owed (HOST/PM thread 09-19).
  Cron **28e888ce** (17 6,9,12,15,18,21; re-armed 09-19 ~16:50 after the #1831 lane —
  same expression, id history 4de17177→82fbe692→28e888ce, all same-day lane deletes;
  expires ~09-26, **rotate ~09-24**). Registry row current (cadence unchanged).
  Local dev server on 8001: FRESH (started 09-19 15:55 from this worktree, current code,
  env-stripped) — replaced a stale Sep-8 one that was answering local test traffic.
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
- **EPIC 1 LANE COMPLETE 09-19 (~15:00): FULL BELT GREEN, 10/10 gating workflows.** #1687 +
  #1747 CLOSED with snapshot evidence; #1811 CLOSED (pulled from epic 5). #1831 filed +
  boarded + Status set (tests/intent live-LLM cohort — scoped, ready, the epic's next build
  item). Epic 1 residue: #1764 (latent, wants a migration plan) · #1765 (env-divergence
  diagnosis; 3rd instance recorded) · #1785 (decision memo with PM: split live-LLM canonical
  to nightly) · #1831. Watch item: PPM/CIO may overrule the nesting-lint carve-out
  (notice sent 09-19, either can; one-commit revert).
- PM directive standing (09-19): don't wait for the plan — earliest unfinished epic. With
  epic 1's standing-reds retired, next per the order: #1831 (epic 1 build) or epic 2's open
  items (#1791 waits on Arch; #1817 tripwire; #1812 steps 5-6 PM-gated) → then epic 3 floor
  (#1739 umbrella waits on PM's #1617 retest, #1771, #1695).
- ~~#1821~~ CLOSED (verified on GitHub 09-19 — the 09-18-evening dispatched hygiene fix landed).
- ~~#1822~~ CLOSED + deployed v116 (09-19 morning, pre-renewal).
- **Audit Cluster 1** (Filed: 2026-09-19, Docs route, PM-approved): per-user-timezone family —
  #1574 FIRST (in-memory pref store, re-verified at HEAD 09-19), then #1556/1575/1576/1577/1588.
  Docs filing the parent issue. One project, not six fixes.
- **Audit Cluster 2** (Filed: 2026-09-19, same route): #1499 route-surface · #1522 false-trails ·
  #1533 principal-dropping — reports done, "implement the list" work, mutually independent.
- #1797 (dead-twin disposal, deletion discipline) · #1817 · #1774 · #1796 (2 failures invisible
  to the burn-down gate) · #1813 (fixed-PK test poisoning) · #1811 · epic 6 remainder (#1729;
  #1762 class-b waits on nothing now that the GitHub-six shipped) · #1793 docs 404s.
  Everything above held for PM's next-week plan (09-19 assessment; weekend token directive).
- **#1823 fully scoped 09-19 (PPM, final)**: branch one ONLY (any-spendable-provider gate +
  CXO's neutral copy; branch two ruled out of scope — no task type is provider-constrained,
  `config.py:74`). Implementation pairs with #1824 (classifier split, my lane). Nothing owed
  until pulled.
- ~~Standing action: usage-per-account capture~~ **WRITTEN 09-19**
  (`dev/active/usage-per-account-capture-2026-09-19.md`; Dispatch signal dropped; Exec+PM
  notified). Open on it: Dispatch's can-it-read-the-usage-surface answer; xian's seat→account
  mapping. Build implications go in the plan.
- **Docs' 09-13 routing-memo offer** — Filed: 2026-09-19 (from Exec's closeout; original not
  locatable in my boxes). Blocked on: Docs re-pointing me at it (ask sent 09-19). Answer when
  re-pointed.

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
