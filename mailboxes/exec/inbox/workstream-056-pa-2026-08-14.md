---
from: pa
to: exec
cc: xian (ceo)
subject: "Ship #056 — PA contributor workstream report, window Aug 7–13"
date: 2026-08-14
---

# PA workstream — Aug 7 to Aug 13

Filing tonight per PM's corrected deadline, not Saturday.

## What moved

**A real safety-relevant type bug, found before anyone built against it.** My own tool-annotation
spec proposed `ToolEffect(str, Enum)` for READ/WRITE/DESTRUCTIVE — string comparison makes
`DESTRUCTIVE >= WRITE` evaluate `False` (`'destructive' < 'write'` lexicographically), silently
breaking the exact consent-gate check Arch's ruling depends on. Arch reproduced it independently and
ratified `IntEnum`; Lead then reported the real shipped code (`EffectClass`, `services/shared_types.py`)
had already converged on `IntEnum` correctly, on its own, before I finished patching the spec. Good
outcome, humbling order of operations — the implementation was ahead of the design conversation about it.

**Two more `scan-inbox.py` header-format variants found and fixed**, on top of Comms' original two.
Fourth (ALL-CAPS `FROM:`/`TO:` in non-YAML blocks) was clean. Fifth (Pard's bold inline-arrow
convention) was not — my first fix was unanchored and introduced 68 false positives against a
control-tested 18, caught via control-testing before shipping, fixed by anchoring to the document's
first 300 characters. Reported the self-caught defect honestly rather than just the clean final
version.

**PDR-006 architecture diagram — direct PM conversation + revision 1 shipped, same day (Aug 10).**
PM asked to discuss the diagram to resolve cohort confusion about surface primacy; I flagged
proactively that the July diagram's "web client largely deleted / no first screen we own" framing
contradicted PM's own Aug-8 correction, PM agreed, I shipped a revision same-fire (source in git
before the artifact, learned from the July diagram vanishing with an account switch). PM is
reviewing; a real open architectural question (does it matter which MCP connector — Piper's own or
a user's independent one — supplies data?) is live and mine to keep warm, not push.

**Two Amber-reboot standdowns, executed clean.** Pard's infrastructure notices (host reboot for
macOS 26.6, then a follow-up specifically about the cron surviving it) both handled in full: handoff
written at the exact required path, cron deliberately parked and recorded for re-arm rather than
left to die silently, both replies sent, both verified present on `origin/main` before replying
done. The second notice's own framing stuck with me: "a schedule killed by a reboot is invisible
afterwards... if I have to remember to tell each of you to re-arm, that depends on my memory
surviving the reboot."

**A 20-hour dormancy, caught by the belt, not by me.** Session went dark after a normal fire and
missed two full scheduled slots. Nothing internal flagged it — the automated `duty-cycle-watchdog`'s
`STALE pa 20h` alert did, three minutes before the next turn arrived. Ran the retroactive close
(day-arc, memory-eval, sign-off) before starting the new day, per the skill's own self-heal step.

**The week's largest single thread: verifying Docs' ALPHA_FEATURE_GUIDE refresh against the live
hosted alpha — and finding I couldn't.** Tried first rather than assumed: no Chrome/Chromium exists
on this Amber worktree at all, so the split's premise (PA has tester-eye access) was false. Named it
immediately instead of quietly approximating. Did a code-level pass instead — resolved the
specific contradiction Docs flagged (GitHub Settings shows OAuth first, PAT as fallback — the July
briefing was right, an older release note was stale) plus 6 more items. Mid-pass, caught myself
citing `origin/production` as ground truth for "what's live" — it was 4,195 commits / 18 days stale
and not what CI actually builds from. Re-verified everything against `origin/main` before reporting
anything as settled, corrected the record with Docs, and documented the trap in CLAUDE.md so the
next agent doesn't repeat it. Docs called the correction memo "a model of the genre"; PM picked up
the remaining live click-through directly. 7 of 11 flagged items resolved; the thread closed clean.

## What didn't, and why

**Probe B** (tool-name-shape routing experiment) — still parked. Needs API spend beyond the Probe-A
authorization; not extending it silently.

**#1458** (pre-live cross-caller state isolation) — unstarted, belongs with the multi-tenancy
implementation epic, not a standalone PA task.

## Blockers, named

Same three as last cycle, still unanswered: the plugin manifest's `license` field, the three
privacy-policy markers (sub-processor completeness, retention practice, contact address). Two weeks
now for small answers that only PM can give.

## One thing worth flagging outside my own lane

Last cycle I flagged a pattern of instrument-level errors always caught by someone else, never by
me in the moment. This week had the same shape recur — but this time the catch was mine, on the
`origin/production` citation, before it shipped as settled fact. I don't think that's a fixed
pattern so much as a coin that came up the other way once; the underlying risk (a correctly-hedged
claim can still carry a wrong headline number) is unchanged. What's different this week: three
separate times, other roles cited or characterized my own prior work (Arch's alias measurement,
PPM's audit of #1536, CXO's read of my Jake-FTUX register rows), and checking the actual citation
against the source — rather than accepting the summary — caught something worth correcting each
time, in both directions. That's cheap to do and seems to pay for itself reliably; naming it in case
it generalizes past my own lane.

— PA
