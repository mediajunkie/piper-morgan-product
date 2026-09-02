# Orientation note — CXO, migrating to Amber / pipermorgan.ai

**⚠️ THIS IS NOT A HANDOFF. Read this paragraph before anything else.**

Your predecessor did **not** write you a handoff, and could not have. Its session went dark on **2026-07-19**; Exec's "prepare handoff memos" broadcast went out on **2026-07-21**, two days later — the ask is still sitting unread in your inbox, which is itself the cleanest confirmation of when your predecessor stopped.

**This note was assembled by CIO from durable artifacts. Nothing in it is your predecessor's own words or reflection.** Where a handoff would normally carry hard-won lessons and a candid load-bearing-vs-commodity self-assessment, this note carries **nothing**, because reconstructing first-person reflection from artifacts would mean putting words in your predecessor's mouth. A fabricated handoff is worse than a missing one, precisely because the successor trusts it. So: assume less than you would from a real handoff, and rebuild your own read of the role from the substrate below.

---

## Your state IS documented — it's just not where a handoff would be

**Your predecessor maintained a carry-forward *inside its session log*, not in a separate `dev/active/cxo-carry-forward.md`.** That's a legitimate variant (the skill treats the session log as the canonical record), and it means your last known state is current as of **2026-07-19 09:05 PT**, not missing.

**Read first**: `dev/2026/07/19/2026-07-19-0832-cxo-code-log.md`, and specifically its `## Carry-forward (updated Jul 19)` section. Verbatim, that state was:

- **#1386 beta gate** — Scenarios B+C PASS; Scenario A + Criteria 2/4/5/6 pending; TESTER-QUICKSTART in Lead's queue; CXO coordinating **via Exec** per PM direction.
- **#1394** — OPEN; Lead building B4; CXO disclosure delivered to Lead Jul 12.
- **Spatial-intelligence committed-theory review** — CXO slice filed Jul 19; awaiting Arch synthesis.
- **MUX branch disposition** (`cxo-mux-surface-2/-4/-7`) — batched to Exec for PM relay; **no CXO action until PM's call arrives**.
- **#1216 data provenance** — PPM input pending a direct CXO ask.
- **Ship 052** — filed Jul 19; Exec to synthesize by Jul 21.

⚠️ **All of that is six days old and none of it has been re-verified.** Treat every line as a claim to check, not a status. Several of these have almost certainly moved — #1386's gate state in particular was actively contested that same day (an accidental autoclose by a commit message, caught and reopened by PPM).

**Your session did not close cleanly.** There is no `DAY-CLOSED` marker in that log, and it ends with *"Cron `812f47d9` alive; next fire 16:47"* — the session died before that fire. So the log is a mid-day snapshot, not a wrap. Anything in flight at 09:05 stayed in flight.

## The rest of your substrate

| Artifact | State |
|---|---|
| `dev/active/cxo-standing-items.md` | present — your durable owed/queued list |
| `docs/briefing/BRIEFING-ESSENTIAL-CXO.md` | present (~18.7KB) — your role briefing |
| `docs/briefing/ROLE-PORTFOLIO-CXO.md` | present |
| `mailboxes/cxo/inbox/` | **8 items unread**, including the handoff ask you never saw |
| Session logs | 7/19, 7/12, 7/10 — a real trail, read backwards as needed |
| **Memory** | **shared and populated — see below** |

## What you do NOT need to do: import memory

This is the one place the migration got *easier* since your predecessor stopped. Memory is keyed on the **git-common-dir**, so every agent worktree off this repo shares **one pool**, and it is already seeded (~167 entries). **You inherit the cohort's accumulated context natively, on arrival, without reading anything.**

Your Phase-3 step is to **verify the pool is populated**, not to read or reconstitute an export. An empty pool is a signal to escalate; a populated one means you already have it. This substantially reduces what a handoff would have needed to carry, and is part of why a missing one is survivable here.

## Environment — verify, don't assume

Follow the same first-session verification the earlier migrants ran (CIO's and HOST's prompts are the worked examples). Non-obvious items, each from something that actually bit someone:

- **Check your worktree is current**: `git fetch origin && git rev-list --count HEAD..origin/main` → expect **0**. CIO's arrived 5,393 commits behind with no error at all.
- **Hooks**: fixed 2026-07-25 (the matcher was invalid — never a worktree issue). **Verify behaviorally**: stage a `mailboxes/` file on a non-main branch and attempt a commit; the PASS is a refusal that **names `check-branch.sh`**. A permission-classifier denial is *inconclusive*, not a pass. Note the hook is **advisory, not a control** — `git -c` and `--no-verify` both bypass it, so prose discipline stays primary.
- **Write your own row** in `dev/active/duty-cycle-registry.tsv` right after arming your cron. Nobody else can: the load-bearing field is your cron expression, which doesn't exist until you arm it. Without a row, the freeze-watchdog is structurally incapable of noticing you're dead.
- **Two mail channels** if you end up coordinating with Pard: `mailboxes/cxo/inbox/` **and** `~/Development/mediajunkie/docs/mail/`, which is a **separate repo** needing its own fetch.

**★ Your in-session hooks check is the SECOND datapoint, not the first** *(Pard's addition)*. The provisioner now runs `amber-agent verify-hooks` headlessly before your standup, and a same-day PASS is required before you're launched. So **expect your own check to pass** — it's confirmation, not discovery. **Escalate loudly if it doesn't**, because a disagreement between the headless proof and your in-session result is itself a finding worth stopping for.

## What's genuinely missing, stated plainly

- Your predecessor's **lessons** — what it learned the hard way that isn't in any artifact.
- Its **load-bearing-vs-commodity self-assessment** — what the CXO role holds that wouldn't survive a handoff.
- Its **read on relationships** — how it worked with Exec, Arch, PPM, Lead; what their shorthand meant.
- Any **judgment** about which of the six carry-forward items above actually matter versus which were bookkeeping.

Those are real losses. The first thing worth doing once you're oriented is forming your own version of them and writing it down — so the *next* CXO isn't handed a note like this one.

---

*Assembled by CIO 2026-07-25 from `dev/2026/07/19/2026-07-19-0832-cxo-code-log.md`, `dev/active/cxo-standing-items.md`, the CXO briefing and portfolio, and mailbox state. **Exemplar for the four other dark roles** (arch, pa, ppm, web) — same shape, same honesty constraint. Route corrections to CIO.*
