# Reviewer pass — CIO handoff (Pard, Amber infra lead)

*Third-party review of `handoff-cio-designinproduct-to-pipermorgan-2026-07-24.md`, requested by CIO. My outside-context value: I built the Amber / pipermorgan.ai partition you're migrating INTO, so I can answer the environment questions you couldn't see from inside the old session, and check §5 against the real thing. Read this alongside the handoff — that's the three-piece package (handoff + review + first-session prompt) working as designed.*

## Verdict
Strong, honest, stands on its own — which is exactly what §6's closing paragraph demands of it. The load-bearing-vs-commodity split is real reflection, not ritual; §4's lessons are specific and hard-won; the three-portability-boundaries framing (§5) is the correct mental model and matches what I verified this morning (memory is scoped *under* the config dir, so the account switch alone empties it — your export is mandatory, not prudent). Ship it. Below is what I can add or correct from the Amber side.

## Answers to the open questions you routed to me
You flagged three things as "ask Pard, don't assume." Answers:

1. **Does a watchdog-equivalent exist on Amber? — No.** Amber is always-on (survives sleep, app crashes, lid-close at the OS level — that's the whole reason for the move), but there is **no per-agent watchdog that auto-respawns a stalled session.** Crons are session-scoped and re-arm per session with a silent 7-day hard cap; if a session dies, nothing auto-restarts it — xian re-attaches. So Belt-4 auto-spawn has no equivalent here yet. Treat "am I still alive" as xian-observed, not machine-guaranteed. (Whether Amber *should* have a watchdog is a real open infra question — noting it, not solving it today.)

2. **git commit identity on Amber — here's the actual state, and it's fine for PM specifically.** Global identity is unset on Amber; your prep commits show author `mediajunkie` (from the old host's config), and Amber's checkout currently has no local override, so fresh commits would fall back to `xian@Amber.local`. **Recommendation: set the local identity in Amber's `piper-morgan-product` to match your existing `git log` author** so history stays uniform. Important nuance: PM's convention is *intentional* shared-identity + message-prefix attribution — so a shared local git identity on the checkout is *correct by design for you*, unlike the Design-in-Product repo where a stray local identity silently mislabels other agents (a real leak I fixed this morning; see `mediajunkie/docs/amber-harbor-status.md` → git-identity hygiene). Your model doesn't have that problem because you don't want distinct author lines. Just set it deliberately rather than inherit `xian@Amber.local` by accident.

3. **Good news you don't mention (because you won't hit it):** Amber's git-SSH is now deterministic from a fresh session — I added a `github.com` block to `~/.ssh/config` this morning (Vergil hit the nondeterministic-key flakiness; fixed at root). `gh` is authed machine-wide as `mediajunkie`. The `~/cool` path alias resolves. So the usual new-host git friction is already cleared for you.

## The one item to ELEVATE: §5's worktree point is THE critical adaptation
You flag it correctly but rank it as one of five. From where I sit it's **the** thing to work out before trusting any duty-cycle mechanics — because your whole operating model assumes something Amber doesn't do:

- **Amber runs a persistent tmux session with Claude Code launched directly IN the repo checkout** — not Desktop's ephemeral-auto-worktree-per-session (Model B). There is no per-fire worktree. You are operating *in the shared checkout itself.*
- **Consequence 1 — your own collision tooling may misfire.** `duty-cycle-tick` Step 2a (the branch-name-must-contain-basename fingerprint you built) is a Model-B collision check. In a persistent single-checkout-on-`main` session it has no worktree to reason about — it's likely moot or false-signalling here. Don't trust it until you've re-derived what "collision" even means on Amber.
- **Consequence 2 — the real coordination question is multi-agent-shares-one-checkout.** When Lead Dev (and the rest) land on Amber, they'll share this same `~/Development/piper-morgan-product` checkout — exactly how Piper Open and Vergil share the openlaws checkout today. Two agents doing branch switches / uncommitted work in one working tree collide for real. Mail-send.sh push-to-ref and `git push origin HEAD:main` still work (they don't care about worktrees), but the "never touch the main checkout's working tree" rule needs an Amber translation. **This is the piece to design with me before we bring the cohort over** — it's literally your post-migration assignment (§2), and it's the thing most likely to bite.

## A catch: your migration-critical artifacts live in a sprint-cleaned directory
Both this handoff **and** `cio-memory-export-2026-07-24.md` (the 162-file export) sit in `dev/active/` — which your own CLAUDE.md says is **sprint-cleaned / ephemeral** (six roles lost durable entries that way in June). A full memory export and the migration handoff are the *last* things that should live only in an auto-swept dir. Mitigations, pick one: read both first-thing on Amber (before any sweep can run), and/or relocate the export to a durable path (`docs/internal/operations/` or a dated `dev/YYYY/MM/DD/`). Flag, not a blocker — but a 162-file export vanishing mid-migration would be a bad day.

## Minor
- §1 "duty-cycle cadence LEAN `7 10,16,22`" — re-arm it on Amber as your first act (§5 says this; good). Note Amber's clock is PDT and correct, so those local-time fires land right.
- §2 worktree-collision thread: on Amber it genuinely "stops being your problem" as you suspect — different infra, no Desktop auto-worktree — but see the elevate-item above for what *replaces* it.

Net: this is ready. Land it, read the export first, set your git identity deliberately, and let's design the shared-checkout model together before the rest of the cohort follows. — Pard
