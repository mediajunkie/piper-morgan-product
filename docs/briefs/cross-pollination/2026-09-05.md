
# Cross-Pollination Brief — September 5, 2026

Two findings today, both about the gap between what a measurement instrument can see and what it reports — one from a newly-shipped monitoring tool, one from a performance benchmark where two agents measured the same endpoint and got different numbers.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A new monitoring instrument has no history — "never happened" is the wrong phrase for "no data yet"

**From:** Piper Morgan (Exec finding, CIO design response)
**Relevant to:** Klatch (duty-cycle monitoring), any project shipping a new checker or dashboard

Piper Morgan's Exec flagged a defect in a `last-invoked` marker that shipped the same day: it reported *"last invoked: never — writer has not been called even once"* for Docs, who had 20 heartbeat commits including one from the previous day. The marker directory was created that morning; Docs just hadn't fired in the roughly three hours since it existed.

The same failure appeared in a second instrument the same day: `sprint-truth.py` reported that an `awaiting-decision` label *"doesn't exist"* — when it existed, just applied to zero issues. Both instruments reported absence-of-data-in-their-window as absence-of-the-event.

CIO's fix: on a missing marker, derive the actual last invocation from `git log --grep="hb(<role>)" -1` (the same convention already used in `age_of()`) rather than saying "no marker yet." This preserves the three-case taxonomy — genuine "never" stays available and true when there's no marker AND no `hb()` commit history — instead of adding an "unknown" bucket that people will learn to skim. A provenance flag (`derived vs. observed`) prevents backfilled values from being mistaken for direct writes.

Exec named the generalization: *every new instrument has a cold-start period where absence-of-data and absence-of-event are indistinguishable, and the natural phrasing of absence is exactly wrong during it.* The fix pattern is always the same: when you say "never," check whether you mean "not since I was installed."

**Suggested action:** When shipping any new monitoring instrument, include a cold-start check: before emitting "never" or "doesn't exist," query whatever history exists independently of the instrument itself (git log, another table, an older file) to distinguish no-record-yet from no-event-ever. The check costs one query and prevents a false-clear that gets quoted into reports.

---

### A measurement discrepancy between two agents was explained by a code change that landed between their runs — not a measurement error

**From:** Klatch (Theseus, Round 153)
**Relevant to:** Piper Morgan (performance benchmarking), any team running comparative performance probes

Klatch's Daedalus measured a session-scanner cold-browse at 1477 ms. Theseus, a few rounds later, measured the same endpoint at 2164 ms — a 47% gap both agents recorded as unexplained. The standard hypotheses (two-corpus memory pressure, corpus drift) were both tested and eliminated.

Theseus closed the gap by checking the commit timestamps: Daedalus's measurement was at 09:23, and a cap change (`FINGERPRINT_LINE_CAP` 1500 → 50,000) landed at 10:18. The two agents were not timing the same build. Round 143 had already priced that cap change in isolation at +645 ms; 1477 + 645 = 2122, within 2% of 2164. Residual: 15 ms, inside noise.

A related discipline that closed the same gap: Theseus proved the cap-patched arm ran against the *patched* code by verifying the observable effect, not just the file change. The cap-1500 arm returned exactly 11 capped sessions; 11 files over 1500 lines were independently counted on disk. Text-matching proves a file changed; only an observable outcome proves the server being timed adopted the change. Daedalus had already applied this discipline in his own probe arm that week — Theseus noted taking it directly from that source.

**Suggested action:** When two measurements of the same function produce significantly different results, check the git log between the two measurement timestamps before assuming instrument or environment error. Also: when writing a probe arm that patches a function to test a specific condition, verify the patch took effect by checking an observable outcome (a count, a changed response, a different error), not just that the file on disk changed.

## Sources Read

- **Klatch**: `docs/logs/2026-09-04-1047-theseus-opus-log.md` (Rounds 148, 150, 153); `docs/browse-cold-figure-gap-2026-09-04.md`; `docs/import-large-session-2026-09-04.md`; Theseus team mail
- **Piper Morgan**: Exec→CIO finding memo (last-invoked cold-start); CIO reply (fix design); `docs/omnibus/2026-09-04`
- **One Job**: `development/coral-logs/2026-09-05-coral-log.md`; `docs/PWA-RECOVERY-PLAN.md` (white-screen diagnosis, boot watchdog plan)
- **Mediajunkie**: `logs/2026-09-04-pard-log.md` (Phase 0 run sheet; OneJob strategic direction shift)
- **Globe, Weather, Cookie Monster**: brief delivery only (cross-pollination 09-04), no new agent narration
- **Atlas, Cuneo, Optilisten, nyt-crossword**: no commits in window

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
