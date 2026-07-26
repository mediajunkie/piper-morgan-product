# Orientation note — Web, migrating to Amber / pipermorgan.ai

**⚠️ NOT A HANDOFF.** Your predecessor's session went dark **2026-07-19**; Exec's "prepare handoff memos" ask went out **7/21** and is still unread in your inbox. **Assembled by CIO from artifacts — nothing here is your predecessor's words or reflection.**

---

## Your predecessor closed cleanly, and left the tidiest record of the group

`dev/2026/07/19/2026-07-19-0652-web-code-fable-log.md` carries a **`DAY-CLOSED` marker** and is written as a **timestamped table** — arguably the most legible last-state of any dark role. Read it first. `dev/active/web-carry-forward.md` is also **current to 7/19**, so you have two fresh, agreeing views.

## What's live

- **413 upload bug — diagnosed and fixed.** PM hit a 413 on a routine 3.2MB image. Traced precisely: `bodyParser.sizeLimit` (`'4mb'`) was measured against the **raw request body**, while the app-level check compared the **original file size** — so base64 expansion put real uploads over a limit the app thought they were under. Worth understanding rather than just noting; it's the kind of mismatch that recurs.
- **PM approved three cleanup items, and asked for a staleness review of the Publishing tooling.** ⚠️ **Check whether that review ever happened** — the session went dark the same day. Before deleting the Medium workflow your predecessor cross-verified via the GitHub API and confirmed `.github/workflows/update-blog-posts.yml` — that verify-before-delete instinct is the standard to match here.
- **Docs' Phase-B backfill completed** — `draftPath` applied to the calendar CSV for 8 of 9 ships (only #040 has no recoverable source, legitimately). Verified against the actual commit rather than taken on report.
- **PM praise worth knowing about**, since it names a principle: a delayed message landed citing the compose editor's **agent-discoverability of edits via git** — the human-first / agent-aware-interfaces idea. That's a design value to keep carrying, not just a compliment.

⚠️ Six days stale and unverified.

## The one boundary that trips people

**Web works in the `piper-morgan-website` repo — not the product repo.** Product front-end (templates, `web/static/js` in `piper-morgan-product`) is **Lead/CXO's lane**, not yours. This has been misattributed more than once, including by CIO. If someone hands you product-repo front-end work, check the repo before accepting the lane.

## Your substrate

| Artifact | State |
|---|---|
| `dev/2026/07/19/2026-07-19-0652-web-code-fable-log.md` | **read first** — closed cleanly, table format |
| `dev/active/web-carry-forward.md` | **current to 7/19** |
| `mailboxes/web/inbox/` | **6 unread**, including the handoff ask |
| **Memory** | **shared and populated (~168) — verify, do not import** |

## Environment

Same verification as earlier migrants. Non-obvious ones: **currency check** (`git rev-list --count HEAD..origin/main` → expect 0); **verify hooks behaviorally** — a PASS names `check-branch.sh`, a permission-classifier denial is *inconclusive*, and the hook is **advisory, not a control**; **write your own registry row** in `dev/active/duty-cycle-registry.tsv` right after arming your cron; **Pard's mail is a separate repo** needing its own fetch.

**One extra for you**: your lane spans two repos, so confirm which checkout your worktree actually points at before your first substantive commit.

**★ Your in-session hooks check is the SECOND datapoint, not the first** *(Pard's addition)*. The provisioner now runs `amber-agent verify-hooks` headlessly before your standup, and a same-day PASS is required before you're launched. So **expect your own check to pass** — it's confirmation, not discovery. **Escalate loudly if it doesn't**, because a disagreement between the headless proof and your in-session result is itself a finding worth stopping for.

## What's genuinely missing

Its **lessons**, its **load-bearing-vs-commodity** self-assessment, and its read on the Web↔Docs↔Comms publishing seam — the part least visible in artifacts. Forming your own and writing them down is the highest-value early act.

---

*Assembled by CIO 2026-07-25 from the 7/19 session log, carry-forward, and mailbox state. Completes the set of five (arch, cxo, pa, ppm, web). Route corrections to CIO.*
