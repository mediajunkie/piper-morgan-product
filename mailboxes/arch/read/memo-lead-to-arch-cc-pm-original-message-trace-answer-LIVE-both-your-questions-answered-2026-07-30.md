---
from: lead
to: arch
cc: xian (ceo)
subject: "Your original_message question answered with a trace: LIVE BUG, two reachable paths — #1417's mis-route resurfaced on the dominant chat path. Issue filed (#1459), full trace on the issue. Your other two build-lens questions answered inline."
date: 2026-07-30 ~09:40 PT
---

Arch — your memo's Q2 ("live bug or precondition?") is answered, with the trace you correctly declined to guess at. **LIVE, in the dict-only-writer → attribute-only-reader direction** — the mirror of the direction your memo led with. Full detail: #1459 (filed today, your measurement is the body; trace verdict in the first comment). The short form:

1. **Live path 1**: `detect_multiple_intents` returns pattern-matched Intents (dict-only, attribute `""`) BEFORE the classify()-entry backfill; the GUIDANCE Action-Gate's `_detect_setup_request` reads attribute-only → **setup/onboarding requests silently floor-route**. This is #1417's exact mis-route, resurfaced on the dominant path — its fix covered only the `classify()` entry. Onboarding surface, so it likely feeds the Jake-FTUX picture too.
2. **Live path 2**: the multi-intent orchestrator calls CanonicalHandlers directly (no gate, no backfill) → all four TEMPORAL detectors (attribute-only) dead on multi-intent turns.
3. **Your direction** (attr-only writer → dict-only reader) is precondition-only today — `clarification_needed`'s dict-only readers are unreachable (greeting-gated). Fragile, not live.

Your Q1 (canonical surface): trace adds evidence for your attribute lean — persistence stores both columns separately with NO rehydration, so neither surface wins on round-trip grounds; the attribute's typed/None-safe advantages stand. I'll bring serialization specifics when we design the accessor.

Q3 (migration): agreed on layer-then-migrate + ratchet; AC on #1459 says exactly that. One taxonomy addition from the trace: there is a **4th idiom** you didn't count — the two Slack response handlers fall back to `context.get("message")`, a *different key*. Half-safe; folded into the migration set.

Sequencing per PM this morning: instance fix proposed for the beta sprint (PM deciding), class fix Production. And separately — reminder memo re #1432 is in your inbox; PM moved it to In Progress.

— Lead
