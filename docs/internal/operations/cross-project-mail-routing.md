# Cross-Project Mail Routing

**Status**: Track 1 of the Apr 28 2026 cross-project comms-gap escalation (Exec→Architect), closing
issue #1358. Track 2 (a formal ADR-level protocol) stays deferred — evidence-triggered, only if this
doc's own known-unknowns surface a real failure that a reference doc can't fix.

**Why this exists**: two independent CIO incidents (2026-05-27, 2026-07-04) each re-derived the same
facts about where sibling-project mail actually lives, at real time cost, because there was no
durable place to look them up. Both incidents are named directly in #1358. This doc is that place.

## The one rule that matters most

**Prefer routing through Exec rather than writing directly to a sibling repo** (PM directive,
2026-07-04). Exec is this project's primary point of contact for Janus and has an established
direct relationship. Send cross-project content to `mailboxes/exec/inbox/` and let Exec relay,
rather than reaching into a sibling repo yourself. This is the default, not an absolute rule —
direct writes aren't forbidden if the situation calls for it — but Exec-as-relay avoids exactly the
convention-drift problem this whole doc exists to fix.

## Canonical locations — do not duplicate this table here

`mailboxes/DIRECTORY.md`'s "Cross-project agents (Janus, Klatch, Dispatch) — NOT reached via
`mailboxes/`" section is the **actively-maintained, dated, re-verified** source for the real
filesystem paths (Janus/DinP, Klatch/Daedalus/Calliope, Dispatch), their conventions, and the three
existing `mailboxes/{agent}/` exceptions that are genuinely in use. **Read it there, not a copy
here** — a second table in this doc would drift from the maintained one the moment either changes,
which is the exact failure this doc is meant to prevent. This doc adds the parts DIRECTORY.md's
mailbox-routing focus doesn't cover: the reasoning, the failure history, and the known-unknowns.

## The failure this doc is fixing, named directly

**Incident 1 (2026-05-27, commit `854a792e0`)**: CIO filed Calliope+Janus memos to a CEO-inbox
copy instead of directly into the target repos (`klatch/docs/mail/`, `designinproduct/docs/mail/`)
— guessed at the convention instead of checking it.

**Incident 2 (2026-07-04, commit `7b570547b` + a `designinproduct` commit `4a1463f`)**: CIO created
`mailboxes/janus/` in THIS repo, which was a dead letter — nothing on the Janus side polls a path
inside `piper-morgan-product`. Had to manually verify by reading all three sibling repos directly to
find the real paths, redoing the exact discovery work this doc exists to make a one-time cost.

Both incidents independently re-derived the same three facts (Janus → `designinproduct/docs/mail/`,
Klatch → `klatch/docs/mail/`, Dispatch → `dispatch/mail/`) because nothing durable recorded them
between the first incident and the second, over five weeks apart.

## The general pattern, if you're reaching a cross-project agent for the first time

1. **Check `mailboxes/DIRECTORY.md`'s cross-project section first.** If the agent/project you need
   is already listed there with a verified location, that's your answer — don't re-derive it.
2. **Default to Exec-as-relay** (see above) unless you have a specific reason to write directly.
3. **If writing directly**, the location is an EXTERNAL repo on the local filesystem, not part of
   this one. Use `git -C <path>` for any git operations there, and follow THAT repo's own commit
   conventions — verify by reading its recent `docs/mail/` (or equivalent) commits directly. Do not
   assume this repo's `mail-send.sh` push-to-ref mechanism applies; it doesn't, it's Piper-Morgan-
   specific.
4. **Never create a new empty `mailboxes/{agent}/` directory in this repo** as a way to reach a
   cross-project agent. An empty directory with no prior history and no reader on the other end is a
   dead letter, not a delayed delivery — this is exactly Incident 2 above. If you're not sure whether
   something polls a given path, ask (Exec, or the agent's own team) before writing to it.
5. **If a cross-project agent's location has changed** or you can't find it in DIRECTORY.md, verify
   by reading the sibling repo directly (or asking) rather than guessing — and once verified, update
   DIRECTORY.md's table so the next person doesn't re-derive it a third time.

## Known unknowns (the section the original Apr 30 plan specified)

Named honestly rather than answered speculatively — these are the open questions Track 2 (the
formal ADR-level protocol) would need to resolve if one of them turns into a real recurring problem:

- **Polling cadence is unverified for most sibling projects.** We know Janus and Dispatch have
  confirmed live readers (per DIRECTORY.md's exceptions table), but we don't have a documented SLA
  or expected latency for any sibling project reading its own `docs/mail/` — a memo sent there could
  sit unread for an unknown period with no feedback loop on this end.
- **No confirmed inverse convention.** This doc (and DIRECTORY.md) describe how Piper Morgan agents
  reach OUT to siblings. Whether each sibling project has an equivalent "how to reach Piper Morgan"
  doc on their own side — so THEY don't have the same guessing problem in reverse — is unverified.
  If you're the recipient of an inbound cross-project memo landing somewhere unexpected, that's a
  signal this gap is real; report it rather than assuming it's a one-off.
- **The three-exceptions list (`pard`, `janus`, `dispatch-dinp`) is closed by convention, not by a
  technical guard.** Nothing currently prevents a future agent from creating a fourth
  `mailboxes/{agent}/` directory by habit, re-triggering Incident 2's exact shape. This doc and
  DIRECTORY.md are prose discipline, not a mechanical check — if this recurs a third time, that's
  the evidence Track 2 needs.
- **Reply-via-Exec-relay's throughput is unmeasured.** The 2026-08-25 ratified protocol routes
  Janus/Dispatch replies through Exec by default; whether this creates a bottleneck under volume
  (multiple roles needing Janus contact in the same window) hasn't been tested against real load.

## References

- `mailboxes/DIRECTORY.md` — canonical, actively-maintained locations table (read this first)
- Apr 28 2026 escalation: `memo-exec-to-arch-cc-pa-pm-cross-project-comms-gap-escalation-2026-04-28.md`
- Apr 30 2026 response (this doc's origin, Track 1): `memo-arch-to-exec-cc-pa-pm-cross-project-comms-gap-response-2026-04-30.md`
- Issue #1358 (this doc closes it)
