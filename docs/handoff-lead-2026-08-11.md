# Handoff — Lead Developer — 2026-08-11 (Amber stand-down, macOS 26.6 reboot)

Written 06:2x PT during Pard's stand-down. Session is expected to resume intact; **this document
assumes it does not.** Everything below is what a cold start needs to be survivable.

---

## 1. Identity and seat

- **Role**: Lead Developer (`lead-code`). Briefing: `docs/briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md`.
- **Worktree (Model A, stable, reused)**: `~/Development/piper-morgan-worktrees/lead` on
  `claude/lead-cycle`. Never work from the shared checkout.
- **Session logs**: `dev/2026/08/09/2026-08-09-0647-lead-code-log.md` and
  `dev/2026/08/10/2026-08-10-0647-lead-code-log.md` — **both closed out**. A resumed or cold session
  on 08-11 starts a NEW log at `dev/2026/08/11/`.
- **Carry-forward**: `dev/active/lead-carry-forward.md` — current as of 21:50 PT 08-10. The cron
  prompt's inline queue text is STALE by construction; trust the carry-forward and this file.

## 2. State at stand-down — the one-paragraph version

The MVP sprint's buildable surface is **drained**. Nine cuts were assembled across 08-09/08-10;
**eight are deployed** (Fly v48), and the **ninth is staged on `origin/main` at `31a09b331`,
awaiting PM's deploy word — it has NOT been deployed.** Zero agents are out. Working tree clean,
nothing unpushed. Eight consecutive full sweeps show only the one long-standing backlog failure.

## 3. 🔴 THE SINGLE MOST IMPORTANT THING TO PICK UP

**The ninth cut is staged and unshipped.** It contains the fixes for what PM hit on their 08-10
evening test:

- **#1590** — root cause of "nothing about GitHub": PM's account has GitHub connected but **no
  default repo**, and `apply_default_default_if_unset` (#1314) was wired ONLY into the OAuth
  callback. Every GitHub read returned empty for such accounts (Radar included — ten resolver
  warnings in PM's three-minute window, read from live `fly logs`). The resolver now self-heals at
  read time, once per user per 300s, guard stamped BEFORE the first await.
- **#1589** — the greeting claimed "a clear day ahead" against four real events and rendered a UTC
  instant ("2:09 am") as a local clock face. Fixed as an honesty rule: **no zero-claim without a read
  that can establish zero**; synthetic whole-day free-blocks never render.

**Deploy procedure (verified working from this seat):** `fly` CLI on Amber is authenticated as
`xian@pobox.com`, so the Lead seat CAN deploy on PM's explicit word — PM authorized this 08-10 and
it was used for cuts 5–8.

```bash
scripts/sync-pm-local.sh                       # fast-forwards PM's checkout
cd /Users/xian/Development/piper-morgan-product
git merge-base --is-ancestor 31a09b331 HEAD    # MUST print nothing/succeed before deploying
fly deploy
```
⚠️ **Verify the deploy the right way**: `/health` returns 200 from the OLD version while the machine
is still replacing. Confirm with `fly status` (machine `started`, checks passing) / `fly releases`,
not with a curl alone. This nearly produced a false all-clear on 08-10.

## 4. PM's retest list

The tracker artifact is PM's primary source of truth:
`dev/active/honest-mvp-ledger-2026-08-08.html` → https://claude.ai/code/artifact/fbb9edcf-9839-44d7-bb0d-55f28cd689c7
(republish the same file path to update the same URL). Accepted items render struck-through per PM's
08-10 request. After the ninth cut deploys, PM's retest is: **start a fresh conversation** — the
first-contact demonstration should show their actual GitHub issues, and the greeting should make no
calendar claim it cannot support.

## 5. Standing PM directives (still binding)

1. **Fundamentals-first**, and a **moratorium on piecemeal routing fixes** — no new pre-classifier
   patterns or extraction tweaks outside the Understanding-Layer Inversion. Routing failures become
   **corpus** entries (#1559, #1579 are examples). Handler-branch and rail-key fixes ARE sanctioned
   (#1431 / #1560 patterns).
2. **Milestone sequence is MVP → Production → Fast Follow.** "Not MVP" never defaults to Fast Follow.
   Production = required for PUBLIC beta, worked in the PUB sprint. (PM correction 08-09,
   memory-pinned, decisions.log.)
3. **Test-support artifacts require verify-first** — never hand PM a command, seed, or test step
   without reading the schema/route/template it touches. This lapsed twice and PM noticed both times.
4. **Board hygiene**: milestone and project board are separate systems; file → milestone → add to
   board in one motion. PM added the auto-add workflow ask to their own queue (UI-only; the API
   exposes no create mutation — verified).

## 6. Open decisions and who owns them

- **PM**: deploy word for the ninth cut. Nothing else is blocking.
- **PM (#1510 fork)**: whether working-mode is declared or inferred. **Three things now consume this
  answer** — #1591's invitation persistence, the standup preference capture, and #1509. Do not let
  any of them grow a local preference store (PPM + CXO both ruled this).
- **PPM**: #1591 spec (standup Production half). CXO's three invitation properties are already on the
  issue: report first and complete · invitation after and cheap to decline · **declining changes
  nothing else**.
- **Exec**: the amended Sep 1 contract. **My discovery-rate contract was unfalsifiable** (raw rate
  can't distinguish "we fixed it" from "PM tested less"); it now reads against **new-class rate**.
  **I owe**: filing-time `Class:` tags and a written-down class vocabulary
  (`docs/internal/operations/`) — the failure families exist across five audit docs but nowhere
  consolidated. Not started.

## 7. Next build work, in order

1. **Understanding-Layer Inversion, Phase 1** — the only substantial unstarted MVP item.
   Arch's GO with conditions: **per-category corpus gate** (never aggregate), **registry-derived**
   canonical grammar, and narrowing only the ~14 AGREE rows **each citing its probe row**. Effect
   enum and rail hygiene landed first, as sequenced. Proposal:
   `docs/internal/architecture/current/understanding-layer-inversion-proposal-2026-08-08.md`.
   **Deliberately quality-banked to a fresh session** — that is the named trigger, not a deferral.
   When the judge corpus stands up, **add the fabrication cases to it** rather than building a second
   instrument (Arch's floor-honesty contract spec, 08-10).
2. **#1572** per-user timezone umbrella — the time audit's root (supply is 0%; every user-typed clock
   time is interpreted on the server's UTC clock). `docs/internal/operations/time-handling-audit-2026-08-10.md`.
3. #1423 / #1522 audit tails; #1592 (credentials.json ERROR noise on Fly).

## 8. Cohort context worth not re-deriving

- **The failure family of the fortnight is "one label, two objects"** — CXO counts seven instances.
  Also live: fabrication (five per-surface guards, never generalized — Arch's contract spec is the
  generalization), imagined-interface tests, absences narrated as facts (#1589/#1590 are both this).
- **Sweep command shape matters**: `-m "not llm"` (llm-marked tests fail keyless and look like
  regressions) and, when overriding addopts, KEEP `--import-mode=importlib` or ~20 files collide.
  Judge full-suite results with `scripts/check_fullsuite_backlog.py`, not by eye.
- The known sweep failure is `tests/unit/services/place/test_place_service.py::TestGitHubPlace::test_github_place_has_name`
  — backlog line 49, pre-existing, verified by stash-and-rerun. Do not chase it.

## 8b. Mail arriving during stand-down (06:47 fire — READ, deliberately NOT drained)

Left in `mailboxes/lead/inbox/` on purpose: the mailbox is the durable carrier, and a resumed or cold
session should drain it normally. Two items, neither needing action before the reboot:

- **PPM → CXO/Lead — the empty-standup gap (recorded on #1591 so it cannot be lost).** CXO's three
  invitation properties hold *when there is data*; PM named the exception first. *"Demonstrate, then
  ask requires something to demonstrate. An empty report is not a demonstration — it is a null result
  wearing a report's format."* The empty case is governed by **#1536 item ③** instead (fail honestly,
  no fabricated demonstration): **there IS data → demonstrate then ask; there is NONE → fail honestly
  and offer, invitation first.** Two rules, discriminator = whether the read produced anything.
- PA → HOST/Comms/CIO: fifth casing variant confirmed and fixed (cohort lane, not Lead's).

## 9. Sign-off state

- Working tree clean; `git log origin/main..HEAD` empty at time of writing.
- Both session logs closed with summaries and the #974 memory-eval section.
- No agents running; no background work to lose.

— Lead Developer, 2026-08-11
