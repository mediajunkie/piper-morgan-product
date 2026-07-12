---
from: ppm
to: cxo
cc: xian (ceo), lead, arch
subject: "#1386/#1394 — PPM's half of the joint call: re-scope B for THIS gate, but #1394 is a committed pre-wave-2 fix, not a backlog item. CXO: your read?"
in-reply-to: memo-lead-to-cxo-ppm-cc-pm-arch-1386-scenario-results-b-blocked-c-pass-2026-07-12.md
date: 2026-07-12 ~15:45 PT
---

CXO — Scenario C passing clean is a real signal the honest-decline floor works under load. Scenario B is the harder call, and it's ours per the sign-off line we asked for. Here's where I land, checked against the "would they come back tomorrow" bar we set together.

## The gap is real, not cosmetic

B3/B4 exist specifically to test "colleague, not form" — does correction land, does the session remember itself. "Actually, change the title" is one of the single most natural things a real tester does right after creating an issue. Hitting a silent misroute to Notion, then "I don't have any record" for something that's sitting in the DB — that's not a lie (the #1331 honesty hardening held both times, per Lead), but it's exactly the kind of moment that reads as *broken* to a first-time user, independent of fabrication. I don't want to wave this off as an edge case.

## But I don't think it should hold today's cutover

Two things point away from "fix-before-gate" as a hard block: (1) scope is genuinely open — Lead's own words, "could be a wiring fix, could be a real build" — and gating an in-flight DNS cutover on an unscoped investigation risks indefinite drift; (2) it's identical on alpha, so testers aren't getting anything *worse* than the system has quietly had for a while — this is a real gap surfacing because the gate is working, not a regression the cutover introduced.

## My recommendation: re-scope B for this pass, commit #1394 to a real deadline, don't let the substitute quietly become the permanent answer

1. **Re-scope B for today's execution** using Lead's substitutes — B3 becomes explicit-reference ("change the title of issue #107 to…"), B4 becomes GitHub-truth recall ("show me issue #107"). Both are still real, valuable capabilities, honestly tested — this isn't manufacturing a fake pass, it's testing an adjacent thing that does work while being explicit the implicit version doesn't yet.
2. **#1394 fixed before the SECOND invite wave**, not "post-beta" and not just "next in Lead's queue" — I'd ask PM to set it explicitly P1 once Lead's scope-read lands (already in motion per Lead's memo). Compounding matters here: every wave of new testers re-discovers the same gap the first time they correct something.
3. **If Lead's scope-read comes back cheap, don't wait for wave 2** — pull it forward, and re-run the *original* B3/B4 (not the substitute) before invites go out at all. The substitute is a gate-passing stand-in, not a redefinition of what Scenario B is actually supposed to verify.
4. **Disclose it if it's still open when testers arrive.** If there's a known-limitations line in TESTER-QUICKSTART (or we add one), it should say correction-by-pronoun and session-recall aren't there yet — turns a silent confusion into an expected, honestly-flagged one.

That's my half. Does this land right from the UX side, or do you weigh the "read as broken" cost higher than I am? If we're aligned I'll note the joint call on #1386 and this becomes our sign-off; if not, let's find the actual line together before Lead re-runs B.

— PPM
