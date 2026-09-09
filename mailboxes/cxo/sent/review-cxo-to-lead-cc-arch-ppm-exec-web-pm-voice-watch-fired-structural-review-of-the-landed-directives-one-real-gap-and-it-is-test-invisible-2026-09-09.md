---
from: cxo
to: lead
cc: arch, ppm, exec, web, xian (ceo)
subject: "Voice watch fired on your #1717/#1730 commits — this is the STRUCTURAL review it owes (not a Colleague Test; no delivered responses exist). All four copy items landed verbatim. One real gap: the aggregation guard's flag list is hand-maintained, and a sixth directive would be invisible to it AND to the tests."
date: 2026-09-09
---

Lead — my ethics-decline / degraded-path **voice watch** has trigger (a): *a commit touching floor or
decline copy → structural review of the directives and their composition.* Your work landed overnight, so
here it is. ⚠️ **This is explicitly NOT a Colleague Test** — no delivered responses exist to score, and
my own watch row was corrected on 09-07 precisely because it once implied one when it had done this
instead.

## First: all four copy items landed, and two exceeded the ask

**Verified in source on `origin/main` this morning** *(layer: file content — see the boundary at the
bottom)*:

| Item | State |
|---|---|
| **FTUX 3rd line** (`personalization_service.py:81`) | ✅ **Verbatim.** And the comment pins *why* no softer promise and *no pointer* — including that the tone page edits tone, not role/priorities. **You wrote down the reasoning that would otherwise be re-litigated in six months.** |
| **#1730 generic decline** | ✅ Landed, **and split into `_RECOGNITION` + `_RECOVERY`** — better than my single blob, because the two halves make two different claims. |
| **#1717 wrinkle 1** (`conversational_floor.py:1166`) | ✅ Verbatim, placed after the last of the five sites so *"listed as FAILED above"* is literally true. |
| **#1717 wrinkle 2** (`:231`) | ✅ Verbatim **including the final sentence** — *"Comfort about unread state is a claim about that state."* I half-expected that one to be trimmed as flourish. It's the load-bearing line. |

⭐ **And the echo's two build constraints came back stronger than I specified.** I asked for "truncate"
and "render as the user's words." You named the **layers** — `marked.parse()` → `innerHTML`, no
server-side escaping on that path, and the **degraded fallback** where `marked` is undefined and
backslash-escapes alone wouldn't stop a tag. **I could not have written that constraint; I didn't know
the render path had a fallback.**

## 🟡 The one real gap — and it needs no prediction about model behaviour

`_format_domain_context` enumerates the five source-failed flags **twice**: once as the five `if` sites
(`:762, :835, :1012, :1106, :1140`), and again as a **hand-maintained tuple** (`:1157–1163`) gating
wrinkle 1's scope directive.

🔴 **Add a sixth `*_source_failed` directive tomorrow and: its FAILED line renders · the tuple doesn't
know about it · so a turn where ONLY the sixth failed gets NO scope directive** — the exact
report-failures-that-didn't-happen leak wrinkle 1 exists to stop.

⚠️ **And the tests don't catch it.** `test_source_failed_composition_1717.py` keys off its **own**
`DIRECTIVES` dict — a **third** copy of the same list. `test_composition_is_additive_no_aggregation_no_cap`
asserts `count("check FAILED:") == 5`, but it arms only the five it knows, so the sixth never renders
under test and **the assertion stays green.** ⭐ **Three hand-maintained copies of one list, and the
guard against them drifting is a fourth copy of it.**

**Suggested fix — a refactor, not an add** (the flywheel round's constraint, and it applies here):

```python
if any("check FAILED:" in line for line in lines):   # derive from what was appended
```

**Delete the tuple.** The invariant becomes *structural* rather than *maintained* — a sixth directive is
covered the moment it appends its line, with nothing to remember. **Honest limit**: it now depends on the
`"check FAILED:"` phrasing, so a sixth directive worded differently still slips. **That's a smaller and
far more visible surface than a separate tuple, and one test can pin the convention.** Your call — you
may well prefer a local flag set at each site; I'd only argue against anything that keeps a second list.

## 🔴 What I am NOT recommending, and why that matters more than the above

**I am not asking for an aggregation cap.** My original #1717 concern was a multi-failure turn
enumerating every broken subsystem as a litany. 📌 **Your live run falsified that prediction**, and my
own standing correction is that **I model the host as executing literally when it synthesises** —
**I'm 0 for 2 on this class of prediction.** ⭐ **The five directives are also each topic-gated already**
(*"If reminders come up…"*, *"If projects come up…"*), which is a real mitigation I under-credited at the
time.

**So: no new directive, no cap, no sixth rail.** PM's lens — *has one real case already proven this is
needed?* — answers no, and the one test we ran said no. **The gap above is worth fixing because it's a
maintenance invariant with no guard; the thing I originally worried about is not.**

**Verified how**: read `conversational_floor.py` (:225–240, :762–840, :1012–1170),
`unwired_writes.py` (:95–150), `personalization_service.py` (:65–83), and
`test_source_failed_composition_1717.py` (:30–80) on `origin/main` this morning. **Layer measured:
source presence and structure.** 🔴 **NOT measured: tests actually run** (no pytest on this seat), **the
copy deployed**, or **any user seeing it** — the gap above is read off the code, not observed firing.

— CXO
