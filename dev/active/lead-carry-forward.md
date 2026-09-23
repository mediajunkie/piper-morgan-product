# Lead carry-forward — rewritten 2026-09-23 ~14:5x PT (post-v0.8.14.0 cut; resolved threads deleted, history lives in the session logs)

## LIVE THREADS

- **v0.8.14.0 "On Your Clock" CUT 09-23 14:3x** — tag + GitHub release at `5912d6749a`;
  `production` deliberately NOT advanced. **Deployed ≠ cut: alpha still serves v0.8.13.0 +
  09-21 closures until PM's keystroke** (Pard's sheet; build from current `origin/main`, not the
  tag — the a1599admin guard fix is later). Test card rows 3–6 wait on that deploy.
- **Alpha is Fly-served (cutover 09-22, complete).** Droplet stopped-warm = rollback until
  **step 11 decommission ~09-29 (MINE)**: decommission + retire `production` branch + deep docs
  sweep + tell Themis (via Pard). Runbook:
  `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`.
- **Staging (`piper-morgan-staging`) stood up 09-23 by PM; first deploy failed at a1599admin
  (FLY_APP_NAME proxy) → FIXED `907d0f87e7`** (guard keys on the users table's state). Retry
  is PM/Pard's; expected `alembic current` = `l1466slack` there (unverified). Latent hole
  noted on #1599 (from-scratch rebuild → PM never gets is_admin; cure = runtime bootstrap).
  **Pard's inbox is `~/Development/mediajunkie/docs/mail/` — `mailboxes/pard/` is gravestoned
  and mail-send hard-refuses it.**
- **Test card** (`dev/active/pm-test-card.md`, artifact ALxfaRpLn5wjBVUPjzLvbi, v5): rows 1–2
  live now (#1824 invalid-key, #1822 OpenAI-only Slack — fake-Anthropic-only → web; real-OpenAI-
  only → Slack; restore); rows 3–6 post-deploy (#1858, #1574, #1576 family, #1856). Web still
  needs an alpha invite minted by PM (Fly-DB write; my seat denied) for browser retests + the
  #1859 white-flash trace.
- **Audit Cluster 1 COMPLETE 09-23** (#1574 #1556 #1575 #1577 #1588 #1576). Cluster 2: #1522 —
  all four ratchet legs live (routers 4, shadow files 6, dark templates 19, dark assets 10;
  disposal of the 29 pinned items = Rule-0 with Arch); #1499 non-deletion half landed, Class 2
  six routers + shadow files + ui.py class + /api/admin deprecation with Arch; #1533 — 1 of 33
  suites done, batch 2 (re-census + top 5) in a Sonnet lane at time of writing.
- **Deploy path (§4e)**: Pard volunteered the build (PM unblocked 09-23); PM names the builder.
  Until built: alpha deploys by PM's hands. Closes #1849 when it lands.
- **Time family tail**: #1868 (GUIDANCE time-of-day onto the user's clock) in a Sonnet lane;
  #1869 CLOSED (Slack faces; zone ruling in decisions.log 14:39). Three datetime copy
  decisions with CXO.

## Waits (verify against the ISSUE, not this file)
- **Arch**: #1863 lens Rule-0 GO (census delivered) · #1499 Class 2 disposal · #1522 pinned-set
  disposal · #1855 design (w/ CXO; `docs/internal/design/design-1855-armed-floor-offers-2026-09-23.md`) ·
  #1841+#1854+#1860 corpus lane · #1832 GO · #1800 scope · #1843 acceptance ruling (w/ CXO).
- **PM**: v0.8.14.0 deploy keystroke · test card rows 1–2 (then 3–6) · Web's alpha invite ·
  #1845 rule ratification · staging retry (with Pard).
- **CXO**: three datetime copy decisions (09-23 memo) · #1772 fix design · #1859 design question.
- **Pard**: §4e CI deploy path; staging retry.
- **Web**: retests + render sweep report (blocked on the invite).

## Queue (unblocked, in order)
1. Land the running lanes (#1868, #1533 batch 2) — review, commit, close/evidence.
2. **Epic 3 floor** (unblocked by #1739) — after #1855's ruling; check epic contents at pickup.
3. #1533 batches 3+ (denominator from batch 2's re-census) · #1841/#1854 re-run after the corpus
   learns · #1522/#1499 disposals once Arch rules.
4. Step 11 on the ~09-29 clock.

## Cron / registry
**Recurring cron DELETED for the 09-23 drain; one-shot STOP backstop `d83f2df6` armed for
21:17.** At that fire: STOP ritual, then re-arm the recurring `17 6,9,12,15,18,21 * * *`
(delete-then-create, CronList-verify exactly one), update the registry row with the new id +
arm date. Rule-1 book-end (PM 09-23, CIO shipped duty-cycle-tick v1.39 delete-and-swap): a
deleted cron is always paired with a one-shot backstop, and idle always restores the recurring.

## Standing (unchanged)
Model pinning + logged tier on every dispatch · pre-register closures · paired fixes together ·
stage-then-commit-bare · explicit paths · verify pushes on origin/main · m-43 layer + m-44
denominator · "Verified how:" on completion claims · masked bearer forms only · `date` before
any timestamp · sync-pm-local at idle · this file: freshness pass at START, rewrite at STOP.
