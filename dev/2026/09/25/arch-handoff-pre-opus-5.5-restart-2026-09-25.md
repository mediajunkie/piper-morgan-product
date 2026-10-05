# Arch handoff — written as last act before Pard's Opus 5.5 relaunch, 2026-09-25 21:5x PDT

**Why this doc exists**: Pard is relaunching this seat on a fresh binary (2.1.280) to pick up Opus
5.5, deliberately WITHOUT `--resume` (cost/staleness tradeoff, Pard's call). The next instance to
read this has **no transcript, no memory of today** — everything it needs to resume correctly has
to be either here or in the two files this doc points to. Read this FIRST, then the two files below,
in that order.

## Read next, in order

1. `dev/active/arch-carry-forward.md` — rewritten tonight, current as of this handoff. The
   resumption substrate; has today's IN FLIGHT state.
2. `dev/active/arch-standing-items.md` — the task queue; not rewritten tonight (no substantive
   change), still accurate.
3. Today's session log, `dev/2026/09/25/2026-09-25-0657-arch-code-log.md` — the full narrative of
   what happened today, if you want the reasoning behind any of the below, not just the state.

## The mechanism change that makes tonight different from an ordinary STOP

**Your session cron is retired, permanently, not just tonight.** `CronDelete 9995c710` was run this
fire; `CronList` confirmed zero jobs. **Do not re-arm a session-scoped cron going forward** — Pard
migrated this seat's wake mechanism to an external LaunchAgent (same schedule, `27 6,9,12,15,18,21`,
straight from `dev/active/duty-cycle-registry.tsv`, unchanged). If you find yourself about to run
`CronCreate` at some future STOP because the `duty-cycle-tick` skill's text still says to, **don't**
— that instruction predates this migration and hasn't been updated yet. The registry row does NOT
need a cron-id column update for this, since there is no session cron id anymore; the LaunchAgent is
external and isn't tracked there the same way.

**Why this happened**: Pard found proof (not just suspicion) that the old session-cron mechanism
ran consistently +30 minutes late against its own declared schedule, while the LaunchAgent lands
within seconds. Evidence and reasoning: `mailboxes/arch/read/evidence-pard-to-exec-cio-arch-...md`
(today's inbox, now triaged). You do not need to re-verify this before trusting it — it was a
same-seat, same-day, controlled comparison (both mechanisms ran in parallel on this exact seat for
several hours), not an inference.

**If a fire ever reports `INJECT-FAILED` or you otherwise suspect the LaunchAgent isn't reaching
you**: that's Pard's mechanism to debug, not yours to route around by re-arming a session cron as a
workaround. Flag it to Pard/Exec and wait, per the runbook Pard referenced
(`mediajunkie/docs/runbook-moving-a-seat-to-a-new-model.md`).

## Model

You should come up as **Opus 5.5** if the relaunch worked. Pard's own message named a real risk:
a relaunched seat comes up on `settings.json`'s default (Sonnet 5) unless Pard sets it in-session —
**verify what model you're actually running rather than assuming the relaunch's stated intent
succeeded** (per carry-forward standing rule 7: a restart's stated intent is not evidence of its
outcome). If you're not on Opus 5.5, that's worth a one-line flag to Pard/Exec, not a silent
adjustment on your own.

## What's actually open right now (2026-09-25 21:5x), most-recent first

1. **MCP Phase C auth-transport decision — waiting on PM.** I ruled (19:5x tonight): prefer a
   bearer-capable client (Desktop/Code) for the one named alpha tester, keep the OAuth
   authorization server off this sprint's critical path — but if PM's actual tester pick uses
   claude.ai or ChatGPT, there is no bearer fallback for those clients and unit 4 (OAuth AS) has to
   go on critical path instead, no workaround exists. **Nothing to do until PM answers which
   tester/client.** Lead's build plan: `docs/internal/architecture/current/mcp/
   phase-c-build-plan-2026-09-25.md`. My slice doc (corrected tonight for a stale rubric citation,
   CXO caught it): `docs/internal/architecture/current/mcp/phase-c-minimal-alpha-slice-2026-09-25.md`.
2. **#1595 unit 4 (multi-intent under the Inversion) — ruled shape (ii) tonight, not yet built.**
   Sequential dispatch through the existing `_process_intent_internal` rail
   (`services/intent/intent_service.py:1158`), not a second dispatch site inside the orchestrator.
   **Real self-correction happened tonight** — an earlier ruling of mine (shape (a), lean on the
   #1763 gate) was found VACUOUS by Lead's dispatched probe: the orchestrator's `can_handle` set and
   the consult's emitted rail-key categories are disjoint, 0 of 127 rail keys could ever clear it. I
   verified the gate was safely wired; I never checked it could fire non-empty. Read
   `docs/internal/architecture/decisions/decisions.log`'s two 2026-09-25 entries on #1595 (18:27 and
   19:5x) for the full trail if this comes up again — **don't re-derive it, the reasoning is already
   written down.** Open design surface named but NOT solved: cross-sibling sequencing when one
   requires a #1190 confirm pause. If Lead asks about that, it's new work, not something to infer
   from tonight's ruling.
3. **#1772 residual — CLOSED by CXO's ruling tonight, nothing owed by you.** Ruled (b): build the
   post-compose scope guard rather than accept a ~10% residual. My only stake (endorsing (b) as
   architecturally sound) is done. Watch only, if it comes up.
4. **m-55 (A Name Is Not a Definition) — filed today, Emerging.** Watch for a second author hitting
   the same shape (a name/glyph/docstring read as a decision already made, when the real definition
   is one hop away) — that's the Proven-bar signal, not something to manufacture yourself.
5. **Bets 001–003, Q5 denominator — both still awaiting PM, unchanged from before today.** Not
   re-nudging; tracked in carry-forward.

## The one honest thing to say about tonight as a whole

Today had a real, self-caught pattern: I ruled two things (the #1818 spend-gate design, days ago;
the #1595 Q2 shape, tonight) where I verified a mechanism was **correctly wired** and stopped there,
without checking whether it could ever **produce a result**. Both were caught — one by me, one by a
dispatched probe — but the pattern is worth carrying forward as a checklist item, not just a
memory: when verifying a gate or predicate before ruling something safe, ask not just "is this wired
correctly" but "does anything in the actual population of inputs ever satisfy the branch I'm
counting on." m-55 names the sibling shape (a name vs. its definition); this is closer to m-48's
family (a proxy for the check is not the check) but I haven't filed it separately — flagging it here
in case a second instance makes it worth its own entry, so it isn't lost between now and then.

**Verified how (this handoff itself)**: every claim above cites the specific file/commit/decisions-
log-entry it's drawn from, written in the same fire the events happened in, not reconstructed from
memory after the fact. This is the moment for that discipline to matter most — nobody reading this
cold can cross-check against my memory, only against what's actually written down.
