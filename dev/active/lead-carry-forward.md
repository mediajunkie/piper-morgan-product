# Lead carry-forward — rewritten 2026-09-23 21:2x PT at STOP (resolved threads deleted, history lives in the session logs)

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
- **Audit Cluster 1 COMPLETE; #1533 CLOSED (blind 0, ratcheted); #1522 all four legs live.**
  Cluster 2 remainder: #1499 open only for two Arch-held items (ui.py exception class,
  `/api/admin/*` deprecation window); SlackWebhookRouter is the Socket-Mode processor only now.
- **#1855 layer 1 LIVE** (five openers incl. `Do you want me to…?`); **layer 2 (real arming)**
  is the next floor build once layer 1 has a live turn behind it — design records
  `revise_draft()` as the second free-prose surface to cover. Epic 3 floor work rides this.
- **Code Quality green since 21:2x 09-23** after three stacked causes (format, I001, mailbox
  filename gate). Keep it: `ruff check .` + `ruff format --check .` tree-wide before every push;
  memo filenames ≤180 chars INCLUDING `mailboxes/xian (ceo)/inbox/` when PM is a recipient.
- **Open defects I own**: #1871 (standup skill's Slack leg calls a nonexistent method — real,
  live AttributeError) · #1870 (key-validation siblings + classifier drift) · #1868-class
  done. Both unblocked; #1871 first.
- **Deploy path (§4e)**: Pard volunteered the build (PM unblocked 09-23); PM names the builder.
  Until built: alpha deploys by PM's hands. Closes #1849 when it lands.

## Waits (verify against the ISSUE, not this file)
- **Arch**: #1499 ui.py exception class + `/api/admin/*` deprecation window · #1841+#1854+#1860
  corpus lane · #1832 GO · #1800 scope · #1843 acceptance ruling (w/ CXO). (Ruled today, done:
  #1863, #1499 Class 2, #1855 L1 + fifth opener, #1522 legs.)
- **PM**: v0.8.14.0 deploy keystroke · test card rows 1–2 (then 3–6) · Web's alpha invite ·
  #1845 rule ratification · staging retry (with Pard).
- **CXO**: #1772 fix design · #1859 design question. (Ruled today, done: #1855 contract,
  datetime copy 1–3.)
- **HOST**: nothing pending (audit line shipped; offered a second pass if wanted).
- **Pard**: §4e CI deploy path; staging retry.
- **Web**: retests + render sweep report (blocked on the invite).

## Queue (unblocked, in order)
1. **#1871** (standup skill Slack delivery — real defect, small) · **#1870** (validator siblings).
2. **#1855 layer 2** design → build (with Arch; `revise_draft()` seam included).
3. Epic 3 floor items behind layer 2 · #1841/#1854 re-run after the corpus learns.
4. Step 11 on the ~09-29 clock (droplet decommission, `production` retirement, deep docs
   sweep, Themis via Pard); rotate cron ~09-28.

## Cron / registry
**Recurring cron 470fd4e1 armed 2026-09-23 21:2x at STOP** (`17 6,9,12,15,18,21 * * *`;
expires ~09-30, rotate ~09-28). The delete-and-swap book-end worked end-to-end today: recurring
deleted 13:2x for the drain → one-shot backstop d83f2df6 → fired 21:17 → STOP → re-armed. Same
practice next time: never delete without creating the backstop in the same breath.

## Standing (unchanged)
Model pinning + logged tier on every dispatch · pre-register closures · paired fixes together ·
stage-then-commit with EXPLICIT PATHSPECS (`git commit -- <paths>`) after reading `git diff --cached --name-only` — lanes stage too · explicit paths · verify pushes on origin/main · m-43 layer + m-44
denominator · "Verified how:" on completion claims · masked bearer forms only · `date` before
any timestamp · sync-pm-local at idle · this file: freshness pass at START, rewrite at STOP.
