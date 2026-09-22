# Lead carry-forward — rewritten 2026-09-19 ~21:55 PT at STOP (freshness rule: full pass at START/STOP)

## STATE (2026-09-21 evening): ELEVEN closed today (+#1794) + release + the #1845 save
- **#1812 CLOSED** (steps 5–6 landed: operator seam deleted, LLMClient credential-free) ·
  **#1837 CLOSED** (all 3 shapes: template dead, acceptance arms interview, refinement
  via floor) · **#1836 CLOSED** (rode #1837 shape 3) · **#1818 CLOSED** ((b) shipped,
  CXO copy, one shared constant).
- **v0.8.13.0 CUT + DEPLOYED TO ALPHA 09-21 ~09:00 (PM-approved)** — all four fixes LIVE;
  /health attests version+sha+environment publicly. Full alpha-docs audit rode the cut
  (#1804 + #1830 closed; guide + email template hosted-only; tester URL unified on
  alpha.pipermorgan.ai — flag for Pard's hosting sort). #1617 retest READY on the card.
- Filed while building: **#1841** (pm039 live-LLM drift, baseline-verified) · **#1842**
  (accuracy-suite container-fallback defect, keyed-lane red-nobody-sees) · **#1843**
  (ACCEPT_PATTERNS '^please ' fires on short imperatives — finalizes drafts; #1739
  contract owners' lane, Arch+CXO should rule).
- **INVITE: HOLD LIFTED 09-20 (HOST)** — Janne's invite is PM's to send.
  drive_test_1812 account awaiting HOST retirement.
- **#1808 CLOSED 09-21 ~13:00** (`74661181a`): blacklist Redis lit as a seeded
  write-through cache (DB stays the record); startup phase added + pinned; #1802
  symmetry on write paths. UNDEPLOYED — next cut.
- **#1845 OPEN (mine + HOST + PM)**: invite-code exposure — replacement with PM
  (in-conversation), Fly-side burn + rule ratification + Gmail-draft swap = PM's;
  my lint backstop awaits the ruling.
- **#1823 + #1824 CLOSED 09-21 midday** (`9ec028406`, landed together per PPM's rule):
  any-provider gate + the four-bucket split + the wrap fix that was the live
  "Something unexpected happened" cause. **UNDEPLOYED — next cut carries them**
  (test-card row added for the invalid-key retest post-deploy).
- 🛑 **HOSTING IS DECIDED — NEVER RE-ASK "WHETHER" (PM, tonight, frustrated; recorded in
  decisions.log 2026-09-21 entry)**: alpha consolidates on Fly, droplet retires. Decided 07-10,
  reaffirmed in the approved plan §4a + Arch's plan v0.2 (yesterday's PM+Pard+Themis+Arch
  discussion). Tonight I recommended droplet-consolidation with that plan in my own read/ folder —
  the exact re-derivation failure PM called out. **Only when/how is open.** Execution memo sent
  (7ac961e77): Tue 09-22 AM window proposed; my correction — droplet DB (6 users, live token) is
  source of truth, Fly frozen at 4 users/07-13, so §4b step 2 is a REAL migration (dump+restore,
  uploads, ENCRYPTION_MASTER_KEY → Fly secret); restore auto-burns the dead #1845 token; my seat
  is Fly-write-denied (Pard/PM execute Fly side; PM owns DNS+OAuth cut).
- Watch: #1832 needs Arch GO · #1599 username check with PM · pm-test-card: #1617 retest
  READY NOW (deployed); #1824 retest after next cut.

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
- PM directive standing (09-19): don't wait for the plan — earliest unfinished epic.
  ~~#1831~~ BUILT+CLOSED 09-19 evening (tests/intent deterministic-tier pin; #1832 filed for
  the dead-route startup test, Arch GO pending). **Next lanes in order**: #1765 diagnosis ·
  #1764 migration-plan · **#1812 steps 5–6 (UNBLOCKED 09-19 by PM's normal-account ruling,
  decisions.log 17:1x)** · #1823 branch-one + #1824 classifier split (paired) → epic 3
  floor (#1739 waits on PM's #1617 retest — now row 1 of dev/active/pm-test-card.md).
- **HOSTING: superseded by the 🛑 block in STATE above** — sort's scope is execution only;
  Pard still leads, my table in the 09-21 memo is concurrence + prep offer. Droplet SSH works
  from my seat (used all day for deploy + DB reads).
- **#1785 SHIPPED 09-19 (wholesale-nightly, premise-corrected from my split memo — PM told
  same exchange; revert is one line if PM prefers).** #1818 direction with CXO/Arch to
  formalize. Slack sponsorship RETIRED. Ruff pre-commit proposal now bundled in Pard's
  hook-decision lane (CIO's escalation) — nothing owed by me on it.
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
