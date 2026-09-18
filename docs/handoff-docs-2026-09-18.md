# Handoff — Docs (Documentation Management), 2026-09-18

**Written for the Amber restart.** Assume you are a fresh or freshly-compacted Docs session with no
memory of the last three weeks. This file plus `dev/active/docs-carry-forward.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

## Who you are and what you own

Documentation Management. Omnibus logs (daily synthesis of every role's session log), mailbox
mechanics and cross-project relay, the blog publish pipeline (proofread + publish + calendar +
syndication), Weekly Docs Audit (Mondays), Monthly Housekeeping (first Monday), doc-currency
tracking. Staff tier, not leadership. Worktrees: product
`~/Development/piper-morgan-worktrees/docs` (branch `claude/docs-cycle`), website
`~/Development/piper-morgan-website-worktrees/docs` (same branch name, different repo — both
Model A). Briefing: `docs/briefing/BRIEFING-ESSENTIAL-DOCS.md`.

## Cron

`57 6,9,12,15,18,21 * * *` — six fires/day. Job `37386761` armed 2026-09-18 ~12:xx PDT (re-armed
after a two-day usage-limit standdown, see below), expires ~09-25. `CronList` at every fire —
session-scoped, dies silently on session exit and at 7 days.

## The single most important thing in flight

**Nothing is mid-build.** The last substantive work (two blog publishes, a two-day omnibus
catch-up, mailbox correspondence with a cross-project agent) all closed out cleanly before this
handoff was written. The nearest thing to "in flight" is routine: **today's own Weekly Docs
Audit-equivalent isn't due yet (next Monday); a sprint closeout memo from Exec is owed by me
(invited, not required — §1 of `docs/handoff-exec-2026-09-18.md`'s companion closeout memo) by
Sunday 09-20 at the latest.** Check `mailboxes/docs/sent/` for whether that's already been sent
before writing a duplicate.

## Recent context you'd otherwise have to reconstruct

- **A usage-limit standdown ran 2026-09-16 ~06:50 through 2026-09-18 ~12:30.** The cohort hit its
  weekly quota; PM suspended all duty cycles except specific scoped exceptions (two blog publishes,
  both by me, on PM's direct authorization). Fully documented in
  `docs/omnibus-logs/2026-09-16-omnibus-log.md` and `2026-09-17-omnibus-log.md` — **both written
  retroactively on 09-18 as a catch-up**, so don't be surprised the "written" date and the "covers"
  date differ on those two files specifically.
- **The omnibus is not optional even on quiet/standdown days.** PM's ruling, relayed via Janus
  (cross-project): "make sure Docs heals any gaps in the record" once back up. A standdown day can
  legitimately warrant a short omnibus, but the day still needs *something* — don't let a quiet day
  become a silent gap.
- **Model allocation this week (PM, 09-18)**: Fable reserved for Lead Developer; everyone else on
  Opus or Sonnet. Choose sub-agent models deliberately — inheriting by omission is what exhausted
  the shared Fable tier and caused the original usage crunch.
- **Amber is restarting today or tomorrow** (the reason this file exists). `amber-fleet.sh resume`
  does `claude --resume <uuid>` per seat — your actual conversation, not a fresh session, unless the
  transcript can't be found, in which case it cold-starts.

## Open items I'm parked on

- **A routing-memo offer to Lead Dev, made 09-13, still unanswered as of 09-18.** Two audit
  clusters (the #1493 timezone-family children #1556/1574/1575/1576/1577/1588, and three
  PM-directed early-August audits #1499/#1522/#1533) have sat with zero progress for weeks. I
  offered to draft a routing memo; PM hasn't confirmed. Not chasing — check
  `dev/active/docs-carry-forward.md`'s "Watch surfaces" section for current status before
  re-offering.
- **A doc-currency bulk-stamp cluster** (14 of 38 operating docs sharing an identical
  `last_verified` stamp — not real currency, a single past operation) is CIO's structural-fix lane
  (#1726), not mine to re-fix. Re-check at the next Weekly Docs Audit, don't re-escalate before
  then.
- **Four issues I filed 09-14** (#1803–#1806, from that week's Weekly Docs Audit) are all sitting
  correctly at owner disposition — none needs Docs action unless an owner asks a question back.

## How this seat gets things wrong — read this part twice

These are mine, earned this week specifically, and the shape is what matters, not the instance:

- **Sync applies to every file read, not just fire-opens.** I reported a draft's frontmatter as
  empty from a 10-commits-stale local read, mid-conversation, because "sync at fire-open" had
  become a ritual I ran once per fire rather than a discipline I applied before every claim. PM
  caught it directly. The fix isn't "sync more" — it's noticing that a claim about file content is
  only as good as the last sync, full stop, regardless of when in the fire you're making it.
- **A cc'd recipient needs a physical copy in their own inbox, not just the relay target's.** I
  made this exact mistake twice in one week, both times on the same shape (a memo to a
  cross-project agent, cc'ing in-repo roles, delivered only to the relay target's inbox).
  `mail-send.sh`'s own warning caught it both times — which means the warning works, but I wasn't
  reading it carefully enough to preempt it. If you cc anyone on a relay memo, deliver to their own
  inbox in the same send, don't rely on the relay target to forward it.
- **An already-actioned memo still needs to move to `read/`, and this is not a "remember harder"
  problem.** I wrote this exact rule down once, then broke it two fires later. The fix that
  actually worked was doing the triage move in the same tool-call batch as reading the memo, not
  as a separately-remembered later step.
- **Verify a timestamp with `date` before writing it, even for something as small as a session log
  header.** I wrote "12:30 PM" in a log filename this same week without checking — the actual time
  was materially earlier. Nothing depended on the exact minute this time, but the discipline exists
  for the case where something will.
- **`draftPath` on the editorial calendar must match the actual archival location at the moment you
  set it, not the location you intend to move the file to next.** I set it prematurely once (before
  archiving), caught it via the validator's own warning before committing, but the near-miss is
  worth naming: the SKILL.md doc I wrote myself says "same pass," and "same pass" means after the
  move, not before it.

## Mechanics worth knowing cold, not rediscovering

- **`mail-send.sh`'s MANIFEST-only warning is a known false positive** — `MANIFEST.md` exists
  permanently in both `inbox/` and `read/` as separate regenerated indexes, so the half-pushed-move
  check always flags it. Verify via `git diff origin/main -- <path>` before treating it as real;
  don't suppress it blindly either, since the *other* warning shape (a genuine cc-delivery gap) can
  arrive in the same batch and looks identical at a glance.
- **Cross-project agents (Dispatch-PM, Janus, Pard, Klatch's agents) are reached via relay-via-Exec
  only** — write the real recipient in `to:`, cc `exec`, deliver to `mailboxes/exec/inbox/`. Never
  create a new `mailboxes/{agent}/` directory; it's a documented dead-letter incident waiting to
  recur.
- **The publish pipeline's split-commit discipline exists for a real, measured reason**: bundling
  the calendar-status update with drafts-folder archival into one commit was directly responsible
  for a Dispatch-PM-reported timing gap (post live, calendar not yet caught up, ~75 seconds).
  Calendar-status first (fast, standalone), archival second, always.
- **Ships publish to `/shipping-news/`, not `/blog/`** — a wrong-path check produces a false "not
  live" report even when the post is fine. Dispatch-PM hit this once and documented it in a
  calendar-row note.
- **This project's own `check-staleness.py` doc-currency detector and `sprint-truth.py` MVP-count
  tool are the only legitimate sources for those two numbers** — never quote either from memory or
  a prior session's carry-forward note; both are cheap to re-run and both go stale within a day.

## Where the rest of the state lives

`dev/active/docs-carry-forward.md` (rewritten every substantive fire, read this first every
session), `dev/active/docs-standing-items.md` (slower-moving durable task list),
`docs/omnibus-logs/` (one file per day, the canonical cross-role record), `dev/active/duty-cycle-registry.tsv` (this role's row: `docs`, `57 6,9,12,15,18,21`).
