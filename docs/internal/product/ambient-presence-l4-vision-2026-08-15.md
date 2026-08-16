# Ambient presence (L4) — PM's vision and phasing, 2026-08-15

**Status**: PM's product direction, given in conversation while ruling on the spatial-intelligence
committed-theory review. This is vision and phasing, not a build spec — PM explicitly did not
commit to shipping the full capability in beta. Companion to
`docs/internal/architecture/current/spatial-intelligence-layer-map-and-costed-options.md` (Arch,
2026-07-30), which named L4 as "not built anywhere" and the fourth of four roadmap differentiators
riding on zero implementation.

## The core principle — PM's own words, close to verbatim

**A notice from Piper must not duplicate an existing notification the user already gets from
somewhere else** — not a Calendar event reminder, not a GitHub app notification, not anything a
native integration already does well. Two things are legitimate instead:

1. **Fill gaps where a notification is needed but nothing currently provides one.**
2. **Provide *synthesized* notifications** — the thing PM calls "the Radar," essentially: timely
   briefings, reminders, and insights built from *combined signals*, surfacing when something has
   changed in a key project assumption. The equivalent of a batched-up attention check-in, where the
   user can y/n, approve, or write a targeted response to a decision that's blocking further
   autonomous work or task completion.

**The value is Piper initiating an interaction the user appreciates and might not have triggered on
their own in time** — without requiring the user to already be logged into the web app watching for
it. Genuinely proactive, not a louder version of what already exists.

**Explicitly not a beta commitment.** PM: *"Not saying we ship this in the beta but that is how I
imagine it."* This document exists so the vision survives as a real reference rather than living
only in a chat transcript.

## Phasing, as PM ruled it

- **MVP**: at minimum, a "coming soon" / false-door placeholder experience for alpha users — even
  if the full shape isn't figured out yet, a placeholder issue naming the intent is enough to start
  from. PM: *"if not even a minimal down-payment possible for MVP, then at least a false door /
  coming soon type version of the experience... even that can be a placeholder issue till we all
  figure out what that is."*
- **Beta**: a feasible Phase 1, even if limited to discovery work only (interruption ethics — when
  is an unrequested nudge welcome — is answerable on paper and doesn't require L4 to exist; this is
  PPM's proposed #1174 rescope, HOST's lane).
- **Production milestone**: a concretely buildable next phase, scoped once Phase 1's discovery work
  and Lead's cost estimate (for a monitoring-loop pilot, still outstanding as of this writing — see
  the layer-map doc's "What is still open" §2) are in.
- **Roadmap**: the rest of the vision above — synthesized cross-signal briefings, the full
  approve/respond interaction model — tracked as future direction, not yet scoped.

## Open, not yet actioned as of this writing

- The exact shape of the MVP "coming soon" placeholder — genuinely undecided, tracked as a
  placeholder issue rather than guessed at here.
- Lead's L4 monitoring-loop cost estimate, still outstanding.
- CXO's caveat from the layer-map review stands and should inform any pilot choice: GitHub is the
  cheapest *technical* pilot for a monitoring loop but possibly the wrong *experiential* one, since
  GitHub's own notifications already do that job well. Notion or Calendar may prove the "genuinely
  new" value better, precisely because they lack strong native signal today.
