
# Cross-Pollination Brief — May 30, 2026

PM ratified a cohort-wide discipline change Thursday afternoon: session log entries now ride with each commit rather than a 30-minute clock. Comms surfaced the rule, CIO updated the shared agent instruction file, and immediately had a catch-and-correct moment — committing the CLAUDE.md change without a paired log entry, then filing the trailing entry honestly. That same day, Comms deployed a mechanical editorial-calendar reconciliation script; its first run caught two calendar-to-file mismatches the manual sweep had missed. After GitHub Support cleared the 24-day Actions trigger freeze reported in the May 28 brief, three PM workflows hard-failed at startup — `upload-artifact@v3` is now deprecated and auto-fails. And Janus's two-month session (Mar 30 → May 29) closed with a formal handoff and a structural insight about how duty cycles must adapt to agents with existing automated tasks.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Session logs now ride with the commit — PM replaced the 30-minute clock rule with event-based discipline

**From:** `piper-morgan-product/CLAUDE.md` (commit `d5b242c`); `dev/2026/05/29/2026-05-29-1232-comms-code-opus-log.md`; `dev/active/cycle-log-cio-2026-05-29.md` (Fire 7)
**Relevant to:** Klatch (Calliope — her duty-cycle discipline design can inherit this from day one, avoiding the 30-min clock problem entirely); designinproduct (Janus — build the event-based rule into the duty-cycle design for the new session)

The 30-minute log maintenance rule was vigilance-based: agents had to remember when 30 minutes had elapsed. Comms surfaced that PM had already rejected this framing ("who knows when that's passed"), and CIO drafted replacement wording. PM ratified from a dentist's office Thursday at 3 PM: "log update rides with the commit." Now in both sections of the shared agent instruction file. The `log-maintenance-reminder` hook that enforced the old clock rule is being realigned to event-based by Lead Dev.

CIO's own Fire 7 produced a textbook catch-and-correct: the CLAUDE.md edit and a Lead Dev memo were committed without a paired cycle-log update — the agent failed the rule in the same session that landed it. The trailing log entry caught it. That sequence is now a live test case for whether the event-based rule actually shifts behavior.

**Suggested action:** Klatch should fold this into Calliope's duty-cycle design doc (v0.2+) as a first-class discipline. Janus's new session should start with it in place.

---

### 2. A mechanical script catches two editorial-calendar drift items the manual sweep missed — mechanism-over-vigilance validated in the wild

**From:** `piper-morgan-product/dev/2026/05/29/2026-05-29-1232-comms-code-opus-log.md`; `scripts/reconcile-drafts-calendar.py` (commit `1e4d575`)
**Relevant to:** Klatch (Calliope — Klatch has blog content; a reconcile pass would be low-cost to add); designinproduct (Janus — brief pipeline has delivery logs but no equivalent drift-check on source-to-output consistency)

Comms built a reconciliation script with three checks: true orphans (draft file exists, no calendar row), missing draft path (active calendar row, empty file pointer), stale draft path (row points to a file that's gone). First run found two mismatches that the same-day manual sweep had missed: *Permission to Pause* (scheduled for publication but sitting in `drafts/published/`) and *15 Sessions, Fast Recovery* (status=drafted, no path pointer, also in `published/`). Both were flagged for PM/Docs disposition without guessing at publication history.

This is the cleanest real-world test of the team's mechanism-over-vigilance principle: the script caught what disciplined human review missed. The pattern is portable — any project with an editorial calendar and a `drafts/` directory can run an analogous pass.

**Also from Comms:** PM established `git commit -- <explicit paths>` as required discipline on shared `main`. On a shared working tree, other agents' files can be pre-staged in the index; a pathspec-less commit sweeps them in. Using `git commit -- <list>` commits only the named paths regardless of index state. Comms demonstrated this in the same session after a directory-level `git add` accidentally swept in PPM's stranded mail files.

**Suggested action:** Adapt `scripts/reconcile-drafts-calendar.py` for Klatch's editorial structure. All agents on shared `main` should use `git commit -- <paths>`.

---

### 3. upload-artifact v3 now auto-fails GitHub Actions — surfaced after the 24-day trigger unfreeze

**From:** `piper-morgan-product/dev/2026/05/29/2026-05-29-0942-docs-code-opus-log.md` (Docs session, commit `a2f2d58`)
**Relevant to:** any project using GitHub Actions; Klatch (check CI workflows before they become blocked)

After GitHub Support cleared the 24-day scheduled-workflow freeze (May 28 brief), PM's E2E test suite ran for the first time and hard-failed in 7 seconds: GitHub now auto-fails any workflow run referencing `actions/upload-artifact@v3`. Three PM workflows are affected (`e2e-aaxt.yml:298`, `test.yml:415`, `pm034-llm-intent-classification.yml:145,229`). Two were already on v4 and are fine.

The v3→v4 upgrade is not a blind substitution — v4 uses an immutable artifact model (same-name re-upload is no longer allowed). Filed to Lead Dev for judgment.

**Suggested action:** Audit any project's `.github/workflows/` files for `upload-artifact@v3` references. Also: `cache@v3` and `checkout@v3` currently produce deprecation warnings (still functional) and will likely reach the same hard-fail threshold. Address v3 before the freeze masks the failures again.

---

### 4. Janus's two-month session closes; duty cycles must adapt to an agent that already has automated tasks

**From:** `designinproduct/docs/logs/HANDOFF-2026-05-29-janus.md`; `docs/logs/2026-05-29-janus-log.md`
**Relevant to:** Klatch (Calliope — useful contrast when duty-cycle design matures to multiple automated tasks); piper-morgan (the PM cohort's duty-cycle design is now generalizing across structurally different agents)

Janus's session running since March 30 closed Friday with a formal handoff and a structural observation: Janus's duty cycle is a different shape than PM agents' cycles. PM agents had no autonomous behavior before the cycle — the cycle *is* their autonomy. Janus already runs five scheduled cloud routines (daily brief sweep, delivery fan-out, health check, weekly digest, external intelligence scan). Janus's duty cycle is therefore a meta-coordinator: a recurring fire that checks the five existing routines' health, drains accumulated mail, and proactively surfaces anything requiring xian's attention — rather than a fresh autonomy engine.

The handoff also marked the PM-git-push-403 situation as "load-bearing, not occasional." The push to `piper-morgan-product` has been returning HTTP 403 daily since at least May 16; the MCP-push fallback in the Delivery prompt catches it every time. What started as an anomaly is now the functional delivery path. The GitHub auth root cause was never fully resolved; the fallback works, so it has been left in place.

**Suggested action:** When Klatch's duty cycle adds a second automated task, use the Janus meta-coordinator framing: design the cycle to wrap and health-check existing automations rather than compete with them.

---

## Sources Read

- **piper-morgan-product**: `dev/active/cycle-log-cio-2026-05-29.md` (Fires 1–7), `dev/2026/05/29/2026-05-29-0942-docs-code-opus-log.md`, `dev/2026/05/29/2026-05-29-1232-comms-code-opus-log.md`, `dev/2026/05/29/2026-05-29-1228-pa-code-opus-log.md`, `CLAUDE.md`
- **designinproduct** (hub): `docs/logs/HANDOFF-2026-05-29-janus.md`, `docs/logs/2026-05-29-janus-log.md`
- **klatch**: git log checked; most recent commit in window = brief delivery (`0717077`); no new Calliope agent work
- **Secondary sources**: `weather` (2 brief-delivery commits, no narration — skip); `nyt-crossword` (2 status prints + brief delivery, no narration — skip); all others (atlas, globe, cuneo, one-job, optilisten) had empty git log in 48h window

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
