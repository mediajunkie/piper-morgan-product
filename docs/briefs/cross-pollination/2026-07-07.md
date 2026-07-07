
# Cross-Pollination Brief — July 7, 2026

One clear technical finding today from Klatch's automated intelligence sweep: Sonnet 5's new tokenizer produces roughly 30% more tokens from the same input as Sonnet 4.6, meaning any system whose context or compaction behavior depends on token counts will behave differently under Sonnet 5 than it was designed to. Piper Morgan and One Job had active development days but no insights that clear the cross-pollination bar.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Sonnet 5's tokenizer change means count-based thresholds fire sooner — audit before migrating

**From:** Klatch (Argus, automated intel sweep #15, `docs/operations/attention-rollup.md` v20)

**Relevant to:** Any project that uses token counts to gate context compaction, memory triggers, session limits, or cost controls

Klatch's compaction threshold (160K tokens, calibrated during Step 9 against Sonnet 4.6 behavior) will be reached in approximately 77% as many turns when a user is on Sonnet 5 — roughly 23% sooner per session. The same input produces ~30% more tokens with the new model's tokenizer. For Klatch this is a lower-urgency item before v1.0, but it lands on the Step 11 (memory architecture) design checklist.

The broader lesson: when a new model ships with a changed tokenizer, count-based thresholds calibrated for the old model are silently miscalibrated for the new one. This class of issue appeared before with Opus 4.7 (+35% tokenizer impact, documented in Klatch's `docs/mail/read/argus-to-daedalus-opus-4-7-impact-2026-04-29.md`) and now reappears with Sonnet 5. It won't announce itself as a bug — it will just mean sessions compact, truncate, or hit limits faster than intended.

**Suggested action:** Before migrating any multi-agent system to Sonnet 5, identify every threshold that is calibrated in token counts rather than semantic terms (context window fractions, compaction triggers, rate-limit guards, session-budget checks) and verify whether the threshold still makes sense given ~30% higher token output from the same content. If you don't have Opus 4.7's migration history as a precedent, this brief is that precedent.

## Sources Read

- **Klatch** — `docs/operations/attention-rollup.md` v20 (Sonnet 5 tokenizer finding); commit log for context on model additions and SDK bump
- **Piper Morgan** — commit log; `dev/2026/07/06/2026-07-06-0622-lead-code-log.md` (Slack connector port, ADR-075/076 ratification, Claude Code Insights triage)
- **One Job** — commit log; `development/coral-logs/2026-07-06-coral-log.md` (rc.5–rc.7 development arc); `docs/R1.2-CHAIN-DESIGN.md`

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
