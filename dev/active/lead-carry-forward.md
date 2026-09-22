# Lead carry-forward — rewritten 2026-09-21 ~22:00 PT at STOP

## ⭐ TOMORROW (Tue 09-22) IS MIGRATION DAY — first fire 06:17 = execution start
- **Runbook**: `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md` (read it FIRST —
  Pard amended the gating note 21:2x, I amended steps 2+4 at 21:5x). Window PM-APPROVED. Exec
  confirmed the GO explicitly.
- **FIRST CHECK AT START — PM's path A/B answer** (Pard's seat is classifier-gated for Fly writes
  + droplet SSH; mine for Fly writes): (A) = narrow Bash allow rules on Pard's seat, Pard drives
  (my recommendation, surfaced to PM in-conversation at STOP 09-21); (B) = PM keystrokes, Pard
  preps verbatim. Look in: tonight's in-conversation reply → mail → decisions.log. **If no answer
  by ~08:30, escalate by mail cc PM — the window needs it by 09:00.**
- **My steps (either path)**: pre-freeze — confirm step 1 (Fly deploy of current main) + step 2
  (ALWAYS-set master key from droplet, never compare — my amendment) happened; then announce →
  `docker compose stop app` → dump + 2 tars on droplet → scp to Amber
  `~/migration-staging-20260922/` (OUTSIDE repo, chmod 700 — user data) → hand restore to
  executor → verify (user count ≥6, invite token NCBN…65FH present iff unused, /health identity on
  alpha.pipermorgan.ai post-DNS, pm-test-card #1617/#1824 retests = the watched verification) →
  aftermath (droplet warm ~1 week; then decommission + retire `production` branch + docs sweep).
- **Restore auto-burns #1845's dead Fly token** (row doesn't survive). HOST roster updated 09-21
  (replacement recorded from PM's sent mail). Watch Janne's registration (droplet baseline 6
  users) — he rides the dump whenever he lands.
- **The undeployed set (#1823/#1824, #1808, #1778/#1781/#1782, #1794) reaches testers via
  runbook step 1's Fly deploy** — no separate droplet cut needed anymore.

## 🛑 HOSTING IS DECIDED — NEVER RE-ASK "WHETHER"
decisions.log 2026-09-21 entry (citation trail: 07-10 decision, 09-20 plan §4a PM-approved, Arch
plan v0.2 from the PM+Pard+Themis+Arch discussion, tonight's reaffirmation). Only when/how was
open; when/how is now the runbook. Droplet primacy was migration debt, not a decision. I re-derived
against the record on 09-21 and PM had to correct it — the decisions.log entry is the fix; don't
repeat the shape.

## STATE (09-21 close): ELEVEN closed + release + invite crisis closed + migration staged
- Closed today: #1812 #1818 #1836 #1837 #1823 #1824 #1808 #1778 #1781 #1782 #1794. Filed: #1841
  #1842 #1843 #1845. **v0.8.13.0 cut + released + deployed to droplet** with full alpha-docs audit
  (#1804 #1830 closed); /health attests version+sha+environment.
- Invite crisis CLOSED on my side: exposed+wrong-instance code dead (never revived — ruling held),
  replacement minted on droplet, PM sent corrected email, HOST recorded from sent mail. Residue:
  #1845 rule ratification (then my token-shape mailbox lint; HOST second reviewer) — Fly-side burn
  now rides the restore.
- Cron **6e295f4f** (17 6,9,12,15,18,21; STOP-rotated 09-21 ~21:55 from 20ee93bc, same expression;
  expires ~09-28, **rotate ~09-26**). Registry row updated with id.

## Waits (verify against the ISSUE, not this file)
- **PM**: path A/B (above, time-boxed) · #1599 username check · #1845 rule ratification.
- **Arch**: #1832 GO (dead-route startup test) · #1800 scope ruling · #1843 ACCEPT_PATTERNS ruling
  (with CXO, #1739 contract owners) · "not initialized" bucket placement.
- **CXO**: #1772 fix design (+Arch mechanism call) · #1824 second-branch reword.
- **Docs**: routing-memo re-point (asked 09-19).

## Queue (unblocked, in order — after migration day settles)
- Next cut **v0.8.14** — from Fly-deployed state post-migration; cut-release skill Phase 5
  (production branch) changes when the branch retires (runbook step 11).
- Epic residue: #1765 env-divergence diagnosis · #1764 migration plan · #1841 (pm039 drift) ·
  #1842 (accuracy-suite container fallback) · #1813 · #1796 · #1797 · #1817 · #1774 · epic 6
  remainder (#1729, #1762 class-b) · #1793 docs 404s.
- **Audit Cluster 1** (Filed: 2026-09-19): #1574 first, then #1556/1575/1576/1577/1588. **Cluster
  2** (Filed: 2026-09-19): #1499 · #1522 · #1533. Both Docs-routed, PM-approved.
- Criteria line (third queue source): new issues in the current sprint milestone — open each with
  `gh issue view` before writing a row.

## Standing (unchanged; full set in 09-14 rewrite + handoff doc)
- Model pinning on EVERY dispatch, logged with the dispatch entry · pre-register what a run will
  close · paired fixes land together · stage-then-commit-bare · explicit paths only · verify
  pushes on origin/main · m-43 layer + m-44 denominator on every claim · "Verified how:" on
  completion claims · sync-pm-local at idle · re-check anomalous readings once · never bearer
  credentials in repo/mailbox surfaces (masked forms only).
- This file: freshness pass at START, rewrite at STOP.
