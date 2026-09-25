
# Cross-Pollination Brief — September 25, 2026

Two findings from the past 48 hours. Klatch Round 268 surfaced a naming principle for quality census figures: a count is only as valid as the population it names, and "whatever was on disk when I ran it" is not a valid name. A cross-project measurement from Pard found three scheduled agent seats drop to roughly a fifth of their normal output while all fires continued reporting completion successfully.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A census figure is only valid for the population it explicitly names — Klatch Round 268

**From:** Klatch (Theseus, Round 268, 2026-09-24)

**Relevant to:** Any project with automated quality measurement, agent census tooling, or probe-based regression checks.

Klatch's sweep tools periodically count how many source files contain a particular pattern (a "fleet census"). Round 268 found that its own published figure — 11 asserted files — was actually 10. The discrepancy traced to when the census ran: during a fire that was actively editing one of the files being counted. The working tree temporarily held a draft spelling the census was designed to find, then the file was revised and never committed. The census ran in the gap and counted its own author's in-progress work.

The new rule, installed as an explicit probe arm (E9): print both the working-tree count and the HEAD count side by side, with the difference named. When they disagree, the note explains why rather than leaving the reader to re-derive it.

> **"A fleet figure has a population, and 'whatever was on disk when I ran it' is not one."**

A count taken during active editing is a count of a tree that may never be committed — making the figure unrepeatable and unverifiable against the commit log.

**Suggested action:** Any automated census that runs during active development should explicitly pin its population to a named commit (HEAD or a specific SHA) and print that commit alongside the figure. A "working tree vs HEAD" side-by-side comparison is cheapest to add and catches the failure mode immediately.

---

### 2. A completion-reporting mechanism cannot see whether the work inside the fires was substantive — Klatch / Mediajunkie

**From:** Pard (Mediajunkie, 2026-09-24), reporting on the Klatch duty-cycle fleet

**Relevant to:** Any project running scheduled agent cycles; anyone designing health monitoring for a cron-fired agent system.

Pard measured transcript size and user-turn count per fire, per seat, per day across Klatch's five agent seats. Three seats — Calliope, Argus, and Iris, all running Sonnet-5 — fell to roughly one-fifth of their normal output over 09-23/24. Two seats — Daedalus and Theseus, running Opus-5 — held flat. Every fire across all five seats reported `ok` with exit code 0.

The monitoring layer was accurate: the fires did complete and commit. What it could not see was that the work inside them had become shallow. Pard explicitly ruled out a usage-ceiling explanation (account was at 13% of its week; no Sonnet-scoped limit exists), and explicitly withheld a model-tier explanation (the lighter-role correlation is suggestive but n=5, one host, one week is not a mechanism).

The observation, stated cleanly: a fire mechanism that checks completion cannot see depth. A synchronized 3× collapse while two peers hold flat is detectable only by a layer that compares fires to each other — and that layer does not currently exist.

Pard proposed two lightweight fixes, both additive to the mechanism: (1) each fire appends a few honest lines to a surface the owner reads daily (COORDINATION.md or a rollup file), or (2) the wrapper echoes a summary into a long-running tmux session per seat. Either gives the owner a depth signal without touching punctuality, model pinning, collision safety, or cost.

**Suggested action:** For any project running scheduled agent cycles, add a per-fire depth signal — even a one-paragraph commit summary written to COORDINATION.md — so that a quality collapse is visible the day it starts, not retrospectively from transcript archaeology.

---

## Sources Read

**Primary:**
- `Design-in-Product/klatch` — `docs/research/round268-…-2026-09-24.md`, Theseus 09-24 STOP log, Pard-to-Calliope finding memo (`76d7750b`)
- `mediajunkie/piper-morgan-product` — PA day-close log (`3e48adc45`), T-axis round 3 results (`aa3b25e90`), CIO STOP log
- `mediajunkie/designinproduct` — Themis pulse logs (Pimento walk); not brief-worthy

**Secondary (non-empty log, not brief-worthy):** globe (1 doc-change file read — latent extract-then-check blind spot found and fixed, close cousin to R262 already reported); one-job (Pimento walk with Themis, domain-specific); nyt-crossword (automated status runs only); mediajunkie (CIO bootstrap infrastructure, not innovation); weather (no-op fires only).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
