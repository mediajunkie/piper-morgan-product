# Lead carry-forward — rewritten 2026-09-12 ~15:10 PT (freshness rule: full pass at START/STOP)

## Live state (receipts, Saturday 09-12 — the big drain day)
- **v92 LIVE** (19 deploys today, deploy-by-default, each verified releases+health; v75's
  "failed" was a flyctl wait-timeout mid-pull — use `--wait-timeout 600`; old machine never
  stopped serving). MVP milestone measured **46 open at 14:00** — up from 37 because PPM
  triaged 12 discovered-today filings INTO epics (discovery visible, not hidden).
- **CLOSED TODAY (27)**: + evening: 1769 1770 (adoption chain) · 1717 (CXO 4/4) · 1748 1749
  (CI guard-line before/after) · 1752 dup. Morning/afternoon: 1690 1741 1733 1740 (epic 2 → FULLY CLOSED) · 1652 1653 1654 1753
  1663 1696 1596 (epic 3 builds done) · 1505 1527 1693 (epic 4 drained; 1559/1579/1606
  deposited, honestly open) · 1736 1738 (closed on FULL-STACK LIVE REPLAYS of PM's verbatim
  v70 turns) · 1759 (dead clarify-carrier deleted, −1082) · 1766 + 1730 (ask-only-when-armed
  INVARIANT: ruled + deleted + ENFORCED — TestUnarmedAskSiteRatchet, mechanical AST census,
  22-row measured shrink-only baseline, tripwire proven both directions) · 1752 (dup) ·
  May-era backlog burn-down (58 rows remain).
- **Biggest find**: #1749's "CI flake" was a PRODUCTION BUG — keyed deploys searched history
  by TITLE ONLY (encrypted preview/topics vs server-side ILIKE). Fixed per #1305's own
  pattern, deployed v89, ciphertext-at-rest pin.
- **Ratchets now 58** (census class +4). Extraction ratchet 567 unchanged all day.

## Waits (verify against the ISSUE, not this file) — DOWN TO PM'S TWO as of 18:45
- ~~CXO voice read~~ DONE: 4/4 PASS pre-registered → #1717 CLOSED; leak finding → #1772.
- ~~CI Tests run~~ DONE: guard line verbatim in green run 34724432842 → #1748 + #1749 CLOSED.
- **PM ~5 min**: (a) 90-second natural standup → #1617 (then the #1739 umbrella can close);
  (b) ~3-min Anthropic repo-secret rotation → E2E green → #1687 + #1747 close with the full
  7-green snapshot.

## Queue (PM pre-authorized; one lane at a time)
- (1769 + 1770 both CLOSED + deployed — v91/v92; the adoption chain is fully paid down.)
- NEXT: #1754 chitchat ruling proposal to Arch (evidence posted by the 1759 lane) · #1768
  classify_conscious Rule-0 proposal · #1767 second dead clarification mechanism (needs
  ruling) · epic 6: #1762 truncation sweep + #1729 doc-summary render · singletons per PPM
  order · 1579-surfaced builder-dedupe ruling (HAND_ROW expected silently discarded; REVIEW
  bucketed under QUERY) — Lead/Arch, still queued.
- **#1751 is MORE than cosmetic per PPM** — real multi-tenancy bug on the CANONICAL
  personality page (#1419/#1734-adjacent, PUT admin-gate limits blast radius); take when
  epic-2-class work resumes, never as cleanup.
- Older queue (pre-epic, still valid): Web's test credential (unblocks 1512/1568/1578/1581
  browser closes) · 1677/1488 close-out on PM's transcript · #1689 native dialogs ·
  #1659/#1660 file residues · pre-claim shadow probe · #1522 fresh-scan-then-delegate ·
  config-validator stub disposal.

## Standing
- Supersession gate · push-after-reading · merge-BEFORE-inbox-ls · deletion = fresh sweep
  never recall · RE-MEASURE never decrement · tracker republish + git commit = ONE unit,
  same block · log-entry headers use $(date +%H:%M) substitution NEVER a typed time · no
  sed on this file without grep-verifying the EXACT phrase (a near-miss phrase "verified"
  a deletion that hit a different line today) · ENCRYPTION_MASTER_KEY = base64-32 not hex ·
  jest needs --config tests/frontend/jest.config.js (bare npx jest fails 9/9 in node env) ·
  prod curl can't see mounted-vs-unmounted (auth 401s before routing — startup logs or
  route-table pins) · the keyless illusion: conftest loads the real key from Keychain, so
  local env-strip is never keyless (the 1748 guard now bounds the CI side).
- Cron 28c6042f (expires ~9/16, **rotate ~9/14**). This file: freshness pass at START,
  rewrite at STOP.
- **RATIFIED 09-12 (PPM)**: every new issue gets Product Backlog status AND a milestone AT
  FILING — fold into every lane brief. 1717/1748/1749 closed this evening (CXO 4/4 + CI
  guard-line before/after); #1772 filed (CXO's N=1 leak, measure-before-design). Waits are
  down to PM's two items + the 1739 umbrella behind the standup.
