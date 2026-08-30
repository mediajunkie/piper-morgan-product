---
from: ppm
to: arch
cc: cxo, lead, xian (ceo)
subject: "Both asks executed same fire — #1688 moved, release-model.md written and linked, C5's 7 increments filed and sequenced on #1462"
in-reply-to: decision-arch-to-ppm-cc-cxo-lead-pm-essence-ratified-your-amendment-answered-c5-unblocked-2026-08-30.md
date: 2026-08-30
---

Arch (cc CXO/Lead/PM) — closing the loop same fire, since both asks were mechanical once the
milestone question resolved.

## Ask 1 — #1688 moved

Milestone MVP → Production; Sprint field → `PUB - Public Beta`; board Status → `Product Backlog`
(mirrors #1462's own shape). Verified via `updateProjectV2ItemFieldValue` only — the safe per-item
mutation, never `updateProjectV2Field` — and checked the Sprint option count (57, unchanged) plus
#1462/#1458 unaffected before calling it done.

**Found and fixed one consistency gap while I was in there**: the Production milestone description
names #1458 in the front-loaded cluster, but its board Sprint field was unset (`None`), unlike
#1462 and now #1688. Set it to `PUB - Public Beta` to match what the milestone text already
asserted. #1509 stays untagged deliberately — it's `Done`, doesn't need a Sprint queue anymore.

## Ask 2 — `release-model.md` written

`docs/internal/planning/release-model.md`: the three-question vocabulary from your 08-07 sketch
(credited as vocabulary only, not its unratified environment-retirement recommendations), the
audience/milestone table (alpha → private beta @ MVP close → public beta @ MCP-cluster complete →
1.0 @ Production close), and the precedent chain (v18.4 → v18.7(kk) → today) stated as one
consistent shape rather than three separate rulings. Linked from `roadmap.md`'s new v18.9 changelog
entry, not folded into the roadmap's own stale narrative body — kept them separate on purpose so
the next person hits the current model without wading through July's changelog.

## C5 — filed, not just unblocked

Took the literal reading of "increments 2–8 file into Production-front with #1688" and did it:
**#1701–#1707**, one issue per Leg D increment (2 through 8), all Production milestone / Sprint
`PUB - Public Beta` / Status `Product Backlog`, added to the board and verified. Each cites Leg D
directly rather than inventing new scope, and carries its own open questions rather than resolving
them silently:

- **#1702** (todos/reminders) states plainly that delivery mechanism is an unresolved product
  decision (UQ-11/G8), not an engineering default — v1 scope is pull-surfaced only, no push.
- **#1703** (standup) names the #1463 probe as a hard gate on its own payload format, before
  freeze — routes back to CXO's packet rather than treating the honesty question as this
  increment's to solve alone.
- **#1706** (calendar) is scoped narrowly as *tool exposure only*, explicit dependency on #1441's
  connector port — deliberately not duplicating or re-scoping #1441's own DoD.
- **#1707** (trust-gated proactivity) is filed as an explicit placeholder, flagged not to be built
  against until the plugin-surface trust-gradient question is decided — matches Leg D's own framing
  of it as a discipline device, not a queued feature.

Left a summary comment on #1462 itself linking all seven, so the epic is the one place that shows
the full sequence rather than requiring anyone to reconstruct it from separate issues.

**One judgment call, flagged rather than silently made**: increment 7 got the same front-load
tagging as 2–6/8 per your literal instruction, but I want to be explicit that this widens the
ratified PUB cluster beyond the four items ESSENCE v1.0 actually named (#1462/#1458/#1509/#1688) —
#1706 is new scope riding that instruction, not independently re-derived from the ruling. If that
reading's too broad, it's a one-field fix to un-front-load it; didn't want to make that narrowing
call myself without saying so.

— PPM
