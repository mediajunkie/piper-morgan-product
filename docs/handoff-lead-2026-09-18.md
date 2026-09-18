# Handoff — Lead Developer (lead) — 2026-09-18

For a successor with no memory of the last three weeks. Everything here is sourced from
`origin/main`. Read CLAUDE.md and `dev/active/lead-carry-forward.md` first — this file only
carries what they don't.

## Genuinely in flight (breaks if nobody picks it up)

- **The #1812 server-key deletion, steps 4–6.** PM ruled the server key "not a real concept,
  not to be supported in any sense" (decisions.log 2026-09-14, two entries incl. the
  business-model rationale and the falsifiable bootstrap clearing-condition). Done: #1810
  (global write removed), #1814 (per-user key actually read), #1815/#1816 (fallback + consent
  fail-open). Remaining, sequenced ON THE ISSUE: Slack-inbound key resolution, removal of the
  PIPER_OPERATOR_SERVER_KEY transitional seam, and the import-time singleton at
  `services/llm/clients.py:675` — the root that made a keyless-owner key seem necessary.
- **The auth-bucket split** (`_classify_llm_error`, `conversational_floor.py:~654`). Ruled:
  split, don't sharpen the copy. Criterion (Arch): a bucket earns its own name when the honest
  user-facing sentence differs. CXO's four-bucket copy is DRAFTED (their 09-15 memo, lead/read);
  Arch owes placement of `"not initialized"`. Do not ship CXO's sharpened bad-key sentence
  before the split — their own conditional failed (the bucket catches 403/forbidden,
  not-initialized, model-not-found, and bare 404s).
- **#1818** — should a zero-cost deterministic greeting pass the keyless gate? Filed with both
  sides argued; CXO/Arch to rule. Not urgent: the copy is now true either way (v113).

## Cron

Job id at standdown: `22689706`, expression `17 6,9,12,15,18,21 * * *`. DELETED 2026-09-16 per
PM's standdown; re-arm on resume and update the registry row (`dev/active/duty-cycle-registry.tsv`
line ~81 — Exec parked it centrally with the expression preserved). Crons are session-scoped:
7-day auto-expiry, and they survive sign-out but do not FIRE while signed out.

## Parked / waiting, and since when

- CXO voice-read consequences on #1772 (50% scope-leak on anthropic N=1; measured 09-15) —
  mechanism is Arch's, copy CXO's.
- #1791 per-user personality (PM: fundamental value; needs Arch's ADR-075 overlay-fork design).
- #1817 (consent-inference invalidation trigger), #1797 (dead-twin disposal), #1809.
- Usage-per-account capture shared with Dispatch — I took this as a standing action 09-15;
  nothing written yet.

## How this seat specifically gets things wrong (highest-value paragraph)

1. **Claiming something was satisfied "along the way."** I closed CXO's rider as "satisfied by
   the same run" without checking the lane had captured it. It hadn't, and the FTUX observation
   that followed caught a tester-facing blocker (#1814). The shape: a byproduct claim costs
   nothing to make and is the least likely to be checked. Pre-register what a run will close
   BEFORE it lands (CXO's layer-match table is the worked example, 09-15).
2. **Sequencing halves of a paired fix.** #1810 (stop the write) shipped without #1814 (teach
   the reader) — turning a billing leak into a functionality wall. If a fix has a producer half
   and a consumer half, they land together or the gap is named at ship time.
3. **Decrementing instead of re-measuring.** Tracker counts, "ratchets passed" with a
   denominator that silently excluded the failing gate (the mypy-gate miss, 09-13), timestamps
   typed from memory. The mechanical fixes are in the carry-forward Standing section; keep them.
4. **Tier inheritance on dispatch.** My 48 unpinned fan-outs exhausted the Fable ceiling and
   two OTHER roles paid (09-14). Pass `model:` explicitly on every Agent dispatch; the policy
   and its quality-watch caveat are in the carry-forward.
5. **Two lanes in one worktree.** I did it once (09-14); the lanes survived by their own
   discipline. One lane at a time.

## Cohort facts easy to get wrong cold

- `main.py` is the entry point, not `web/app.py`. Prod deploys from the MAIN checkout
  (`git pull && fly deploy`), never from this worktree.
- `scripts/run-sweep.sh ratchets` runs the mypy gate under `venv-mypy-gate/` — NEVER the dev
  venv (over-reports ~75 phantom errors; the guard refuses if the venv is absent).
- `gh` can return EMPTY with exit 0 in the sandbox; verify by reading back.
- The compound `git add && git commit` bypasses the sweep hook (PreToolUse timing). Stage in
  one call, commit bare in the next.
- A push to origin/main does NOT make a hook fix live; the main checkout must sync
  (`scripts/sync-pm-local.sh`).
- Silence has three causes that look identical (dead / signed-out / ceiling-refused); the belt
  cannot distinguish them. `CronList` non-empty means ARMED, never LIVE.
