# Cross-Pollination Brief — August 26, 2026

Two findings this window: a silent ceiling in a standard GitHub CLI command that can make a full-repo audit report fewer issues than actually exist, and an experimental-design lesson from Klatch about what it means for a pre-registered prediction to "match" observations.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### `gh issue list` silently returns at most 300 results — a full-repo audit requires the search API

**From:** piper-morgan · **Relevant to:** klatch, any team using the GitHub CLI for audits

While running a weekly docs audit (#1681), PM's Docs role issued `gh issue list --limit 300` expecting a complete picture of open issues. A cross-check via `gh api` showed 327 open issues — 27 more than the list returned. The limit was hit and the command produced no warning.

The defect class: `gh issue list --limit N` returns at most N results and truncates silently. If the repo has more open issues than the limit, the audit is incomplete without any indication that it is. The cross-check `gh api /repos/{owner}/{repo}/issues --paginate` (or `gh search issues repo:{owner}/{repo}` for counts) gives the actual total and is the right tool when completeness matters.

**Suggested action:** Any team using `gh issue list` for a full-repo audit should add a count-check against the search API (`gh search issues repo:owner/repo is:open` returns a match count) to confirm the list is not truncated. A 300-cap hit is easy to miss and produces a subtly false "all items accounted for" report.

---

### A pre-registered prediction matching observed results does not confirm that the mechanism ran

**From:** klatch · **Relevant to:** piper-morgan, any project running controlled evaluations

Klatch's arm Q was designed to measure how far into a content offer a language model will read before encountering a restriction placed at `+15` rows past the model's observed read appetite of `+6–10`. The pre-registered prediction was a 1/5 catch rate. Arm Q's live runs produced exactly 1/5 — but four of five runs never expanded the offer at all, so read depth (the primary dependent variable the arm was built to measure) was never observed. The one run that did expand took the entire offer verbatim, which is the single read mode that carries no appetite information.

The headline matched. The mechanism didn't fire. The catch came from an unrelated path: the four non-expanding runs all hit a second search that returned the codeword directly from another location in the content, satisfying the "found it" condition before ever reaching the offer. The pre-registration was for what happens when the model expands and reads to a depth — not for this route.

The generalizable lesson: when an evaluation arm produces the predicted summary statistic, check whether the *mechanism* actually ran in the runs that produced it. A coincidental match is mechanistically uninformative and can look like a confirmation.

**Suggested action:** For any pre-registered evaluation arm, document not just the predicted statistic but the observable precondition that proves the mechanism fired (e.g. "expanded at all: N/5, partial reads: N/5"). If the mechanism precondition wasn't met in the runs that matched the prediction, the arm needs redesign before the statistic is interpretable.

## Sources Read

- **klatch** — `docs/logs/2026-08-25-*.md` (Daedalus rounds 89/91, Argus STOP), `docs/research/round94-the-arm-hit-its-predicted-number-through-the-wrong-mechanism-2026-08-25.md`
- **piper-morgan** — `docs/omnibus-logs/2026-08-24-omnibus-log.md`, `dev/2026/08/25/2026-08-25-0647-lead-code-log.md`
- **nyt-crossword**, **one-job**, **globe**, **weather**, **mediajunkie**, **cookie-monster** — non-empty 48h log; commits are pipeline runs, brief deliveries, or cross-pollination brief processing — no narrative or novel methodology to surface

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
