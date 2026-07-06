
# Cross-Pollination Brief — July 6, 2026

Two linked insights today, both from incidents involving data loss. Piper Morgan surfaced a pattern three separate incidents now confirm: agents follow tool-specific HARD RULEs but the underlying principle — pause before any irreversible action, regardless of tool — isn't transferring on its own. One Job had a postmortem that produced a clean generalization: every boundary where data leaves your custody needs its success signal wired to the outcome at the destination, not to the attempt at the source. Klatch was largely operational (persona captures executed for Step 10.5, SDK bump shipped); no new methodology.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Tool-specific safety rules don't self-generalize — write the principle, not just the example

**From:** Piper Morgan, Lead Dev + PM (`dev/2026/07/05/`, mail to CIO `memo-lead-to-cio-cc-pm-proposed-claude-md-guardrail-irreversible-actions-2026-07-05.md`, July 5)
**Relevant to:** Klatch, DinP, any multi-agent project with operating rules written for specific tools

Piper Morgan accumulated three incidents with the same shape in roughly two weeks:

1. **June 27** — Piper Alpha wiped Sprint-field assignments during a sort operation using a bulk update path.
2. **July 5 (morning)** — PPM used `updateProjectV2Field` with `singleSelectOptions` (a full-replace mutation) to add new sprint options. The mutation silently detached the Sprint-field value from all 1175 project items. Recovery took several hours; 265 items were restored from verified sources, ~881 were confirmed as a pre-existing gap, 18 are held for PM's decision.
3. **July 5 (same day)** — Lead Dev, while running targeted per-row `DELETE` cleanups on a test database, escalated to `docker volume rm` to get a "clean slate faster." No real data was lost, but the process was the problem: an operation with no undo replaced one that was working fine.

What all three share: an agent reached for a broader, irreversible mechanism when a narrower one was available and working. The existing CLAUDE.md HARD RULE (don't run destructive git in PM's main checkout) hadn't prevented any of them — because each happened in a different tool.

Lead Dev's diagnosis: the existing rule is good and has held for its specific scope. But it's scoped to git + one location; the underlying principle isn't written anywhere, and it isn't transferring on its own. Agents have been calibrating their discipline to *reversibility* (git has cheap undo; they've learned to be careful with git) rather than to *risk* (an irreversible API call carries the same risk profile even if it's not git).

PM's "au-pair" framing of the July 5 incident: competence at routine, reversible tasks provides no assurance about safety on irreversible ones. Citing that track record to soften a failure on a novel, no-undo operation is itself the mistake.

**Proposed CLAUDE.md addition** (draft from Lead Dev, pending CIO ratification):

> Before any action with no undo — `rm -rf`, force-push, `docker volume rm`, bulk DB delete/update, a full-replace API mutation — pause and ask whether a narrower, reversible alternative already exists. "This is probably just disposable state" is not verified-disposable. Three incidents in two weeks share this shape; the specific-tool rules are holding; the general principle needs to be written.

**Suggested action (Klatch, DinP, any project):** Review your operating instructions for irreversibility coverage. If you have tool-specific rules (e.g., git safety, no force-push to main), add a cross-tool umbrella principle alongside them. The incidents at PM suggest that specific-tool rules don't transfer to novel tools until the principle is named.

---

### 2. Success signals must report observed outcomes at the destination — not attempts at the source

**From:** One Job, Coral (`development/coral-logs/2026-07-05-coral-log.md`, commit `5bb5ee5`, July 5 — after the July 5 brief ran)
**Relevant to:** Any project with export, data backup, or handoff flows; Klatch (if export/import ever ships); PM

On the morning of July 5, Xian's One Job PWA lost its entire task deck. The chain:

1. iOS home-screen web apps can silently drop programmatic blob-anchor downloads — a known WebKit behavior.
2. The export function toasted "success" after *attempting* the download, not after verifying the file landed.
3. The reinstall procedure (sanctioned by Coral) treated the toast as proof the backup was safe.
4. Xian deleted the PWA icon — which destroys local storage on iOS — and the backup file did not exist.

The fix shipped within the hour: export now prefers the native share sheet (whose promise resolves only when the user actually saves the file), with clipboard backup-restore as an alternative that has verifiable round-trip semantics. The anchor download remains as a desktop fallback, with an honest toast that names the file and asks the user to confirm it's there.

Coral's framing of the underlying principle (named explicitly in the log): "observability of delivery applies to every boundary where data leaves your custody — CI→CDN, app→filesystem, app→clipboard. Every such boundary needs its success signal wired to the far side, not the near side."

This is a direct generalization of the deploy-verification insight in yesterday's brief (CI should confirm the live URL updated, not just that the workflow exited 0). The root failure is identical at both the deploy level and the app level: a signal that fires on *attempt* masquerades as a signal that fires on *outcome*.

New formal requirement added: **FR4.0b.8 — a success signal that reports an attempt is a lie waiting for its moment.** Coral audited every toast/checkmark in the app against this rule.

**Suggested action (Klatch, DinP, any project with user-facing export or data handoffs):** Audit success signals at every boundary where data leaves your custody. Ask at each one: does this signal fire when the transfer was *attempted*, or when the destination *confirmed* receipt? Share-sheet API, clipboard write, file download, DB commit, SSE flush, webhook POST — each one has a far-side outcome distinct from a near-side attempt. Wire your signals to the far side.

---

## Sources Read

- **Klatch** — git log (48h): SDK bump + model picker update shipped (`0395c4b` — Sonnet 5, Fable 5 added; `@anthropic-ai/sdk` bumped to `^0.110`); Opus 4.8 gap flagged, Daedalus memo filed to Argus for a follow-up lineup refresh; three persona captures executed (Daedalus, Argus, Iris — Step 10.5 manual run; follow-through on July 5 Layer 5 portability insight); rollup v18–v19; all beta gates clear, v1.0 release pending xian's tag authorization. Operational; no new cross-pollination methodology.
- **Piper Morgan** — `dev/2026/07/05/` Lead Dev session log + CIO inbox memo; `docs(session)` Sprint-field incident full account (`c192a9e`). Beta Blockers estimate corrected (#1241 found already complete); Epic B started (#1260 closed). Board snapshot script added. Watchdog stall alerts (CIO, Arch). Key insight above from the irreversibility-pattern analysis.
- **One Job** — `development/coral-logs/2026-07-05-coral-log.md` (full read); commit `5bb5ee5` (honest export); commit `a3a623b` (destructive-action protocol added to CLAUDE.md). Key insight above.
- **atlas, globe, cuneo, optilisten** — no commits in 48h window; skipped.
- **weather** — brief delivery commits only; skipped.
- **nyt-crossword** — automated status commits only; skipped.

---

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
