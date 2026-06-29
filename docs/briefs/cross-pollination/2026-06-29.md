# Cross-Pollination Brief — June 29, 2026

Sunday into Monday: both primary projects are running lean through a quota reset Wednesday. The real findings today are two corrective ones. PM's Belt-0 auto-foreground watchdog — reported June 28 as a working cure for stalled duty-cycle sessions — failed its first real-world test: macOS throttles individual background windows even when the app is foregrounded, so the watchdog's core action didn't reach the stalled sessions. Belt-0 is now disabled; the off-machine cure is being reframed as spawn-fresh, not wake-existing. Separately, Klatch's weekly external scan flagged a Claude Code behavioral change (2.1.195) that any agent team using hyphenated hook matchers should check.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Foregrounding a macOS app does not reach its background windows — off-machine cure reframed as spawn-fresh

**From:** PM CIO (`dev/2026/06/28/2026-06-28-0337-cio-code-opus-log.md`; commits `8bc01cc28`, `2dec301c6`)
**Relevant to:** Klatch (same multi-window duty-cycle model)

The June 28 brief reported Belt-0 — `open -b <bundle-id>` — as a working auto-foreground watchdog for stalled PM duty-cycle sessions. First real-world validation yesterday disproved it. The watchdog fired four times on stalled roles (exec, arch, cxo, ppm), but none of them resumed: macOS and Chromium throttle **background windows** even after the app itself is frontmost. The `open -b` primitive brings one window forward; it cannot selectively reach each role's separate window. When those sessions resumed, it was via PM's direct engagement — not the watchdog.

CIO's documented conclusion: Belt-0's detection and nudge backstop work correctly; only the auto-resume step failed. `open -b` is the wrong tool for multi-window resumption — it's too coarse.

This reframes the off-machine cure from "foreground the existing session" to **spawn-fresh**: a launchd job (or equivalent) that launches a headless `claude -p` process with the duty-cycle prompt, independent of whatever background windows are suspended. The cure needs to not depend on a suspended session's window at all. CIO has scoped a B1 spike (launchd + `claude -p`) and a B2 fix (Mac Mini as an always-on host, which arrived); pending PM's decision on whether to build B1 or wait for B2 to arrive.

Correction note: the self-validation worked exactly as intended — the watchdog was exercised in real conditions before any reliance was placed on it, caught the failure, and generated an honest spec update and disable rather than a false sense of coverage.

**Suggested action (Klatch):** If Klatch's duty-cycle ever needs a resume cure for backgrounded sessions, the `open -b` path is already ruled out for multi-window setups. The valid arch is spawn-fresh (new headless process, not wake-existing). Iris's in-app scheduled-task shape (which CIO initially cited as a model) is also in-app — same backgrounding limit — so it doesn't serve as a standalone cure either.

---

### 2. CC 2.1.195 changed hook matchers from substring to exact-match — audit settings.json if you use hyphenated names

**From:** Klatch external intel scan (`docs/intel/2026-06-29-sweep.md`, commit `fe1422b`)
**Relevant to:** PM (cohort settings.json files), DinP (Janus/Themis settings)

Claude Code 2.1.195 (released June 26) fixed hook matchers: tools and agent names with hyphens (e.g. `code-reviewer`, `mcp__brave-search`) previously matched via substring and now require exact-match. Any hooks configured with hyphenated matchers that relied on prefix or substring matching may silently stop firing after this update.

The external scan noted that no `.claude/settings.json` was found in Klatch's repo root (agents use personal Claude Code settings), so team members should verify their own settings after updating. The same applies to PM's cohort: if any hooks target hyphenated tool names or agent slugs, they should be audited for exact-match compliance.

**Suggested action (all teams):** After updating to CC 2.1.195+, scan personal settings.json for hook matchers containing hyphens (look under `hooks[*].matcher`). Confirm the hooks still fire as expected with a direct test call — don't assume substring behavior still works.

---

## Sources Read

- **Klatch** — git log (48h): external intel scan `docs/intel/2026-06-29-sweep.md` (CC 2.1.195, SDK v0.106.0, Vite 8.1 stable, Salesforce MCP); release notes draft `docs/releases/composition-beta-release-notes-DRAFT.md`; cadence-lean memos (Daedalus↔Calliope). No new product decisions or technical work post-beta-gate.
- **Piper Morgan** — CIO session log `dev/2026/06/28/2026-06-28-0337-cio-code-opus-log.md` (Belt-0 first-real-stall failure + disable + off-machine scope); Lead Dev session log `dev/2026/06/28/2026-06-28-0823-lead-code-opus-log.md` (#1322 sim-transport dead-code retirement, PRs handler cutover to OAuth connector); commit log (48h).
- **DinP hub** — Janus close-out `docs/logs/2026-06-28-janus-log.md` (website Phase-1 merged + live, brief-history audit, thin-trigger fix, Mac Mini bought); Themis commits (copy-on-build clean, letter queue rotation).
- **Globe** — cross-pollination brief delivery only (commits `d42657e`, `029a1f2`); no new Tessera narrative.
- **nyt-crossword** — automated daily status commits (print/remarkable/fetch); no narrative content; skipped.
- **atlas, cuneo, weather, one-job, optilisten** — quiet (no commits in 48h window).

---

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answer incoming**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate? The question isn't about a specific client — different clients have different content needs — but the shape of *what proves Klatch is ready for a real-world cross-tool context-portability use case* is the same regardless. Possible answer-shapes: a screen recording of a composed klatch, a one-page doc for a client audience, a minimal working MCP demo, or simply "wait until Iris's composition gesture ships and the demo writes itself." Knowing which direction we're headed might back-pressure the UX critical path usefully.

[Read the full question →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*