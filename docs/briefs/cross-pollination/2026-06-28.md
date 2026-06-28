# Cross-Pollination Brief — June 28, 2026

Klatch crossed its beta gate overnight. All seven increments of the composition gesture are now built, Iris-reviewed, merged, and validated — MAXT Session 03 (live with xian, 15/15) and two AAXT rounds (R46 clone-from-klatch, R47 mention-override) all passed with zero Phantoms. The release condition xian set on June 26 is met; a release cut awaits his call. On the PM side, a busy Saturday produced a working auto-foreground watchdog that revives the duty cycle when the app backgrounds, a new formal decision record (ADR-073), and the Triad Model published to both Medium and LinkedIn.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Klatch beta gate fully cleared — composition gesture complete, release awaits xian's call

**From:** Klatch (Iris session log `docs/logs/2026-06-27-1903-iris-sonnet-log.md`; AAXT R46+R47 `e18ad3a`; Iris heartbeat `6eb5138`)
**Relevant to:** PM (milestone sequencing), DinP (public milestone to announce when the cut lands)

Yesterday's brief reported the beta gate being defined; today it's met. The composition gesture — the feature that lets a user build a multi-entity conversation in Klatch rather than a single-agent one — is fully implemented across all seven increments:

- Increments 1–6: built by Daedalus, Iris-reviewed as conformant, merged to main
- Increment 7 (@mention override): the last piece — lets a user address a specific entity mid-conversation regardless of klatch mode; built, Iris-reviewed conformant, merged via `aaca51b`
- MAXT Session 03 (15 probes, live walkthrough with xian): all 15 pass
- AAXT R46 (clone-from-klatch, 8 probes): passed, 0 Phantoms
- AAXT R47 (mention-override, 8 probes): passed, 0 Phantoms

The beta gate condition set June 26 in `docs/ROADMAP.md` — "composition gesture fully implemented, tested, and QA'd" — is now satisfied. Iris's overnight heartbeat: "awaiting xian release cut call." No code blockers remain.

One minor observation from R46: a "Subliminal candidate" was noted in the GUARD1 probe — not a blocker, worth follow-up. R47 passed clean.

**Suggested action (DinP):** Mark the July 2026 Klatch beta target as actively pending on the DinP calendar. When xian cuts the release, the gallery entry and public narrative are ready to update. For PM: the MAXT protocol (structured live walkthrough with the product owner as the beta gate) is a pattern worth carrying — it kept the quality bar clear and prevented premature release pressure.

---

### 2. PM ships auto-foreground watchdog (Belt-0) — revives the duty cycle when the app suspends

**From:** PM (CIO session log `dev/2026/06/27/2026-06-27-1341-cio-code-opus-log.md`; commit `dafc4904f`)
**Relevant to:** Klatch (duty-cycle continuity), DinP (any future automated trigger work)

The persistent duty-cycle failure mode on PM is mode-1b: the Claude Code app gets backgrounded or suspended while a session is live, and the in-process cron can't fire. Until now, recovery required PM to manually foreground the app. CIO built, tested, and deployed an automated cure (Belt-0, `duty-cycle-watchdog.sh` v2.1):

When the watchdog detects a stall, it now runs `open -b com.anthropic.claude-code` — Launch Services, not Apple Events — to un-suspend the app. This was a non-trivial engineering puzzle: `osascript` hangs when called from within the app itself (self-deadlock), and System Events requires a TCC grant. `open -b` sidesteps both issues cleanly. Test result: 9/9 pass; deployed to the launchd-run copy PM's watchdog uses; default-on.

Important scoping note the CIO documented explicitly: Belt-0 cures mode-1b (app backgrounded). It does NOT cure mode-1a (session death — cron list empty, carry-forward lost) or the machine-sleep case (launchd can't run while the Mac is asleep). Those remain the motivation for an always-on Mac Mini or off-machine trigger. The first real mode-1b stall will self-validate it.

ADR-073 was also written this session, formalizing the hard rule against destructive git operations in PM's main checkout (the rule that was PM-mandated on June 21 after working-tree content was lost twice).

**Suggested action (Klatch):** Klatch's Iris is on a similar duty-cycle model. If app-backgrounding is ever a factor there, the `open -b <bundle-id>` pattern is a proven, permission-free primitive that sidesteps the Apple-Events TCC trap.

---

### 3. PM's Triad Model published to Medium and LinkedIn

**From:** PM (Comms log `dev/2026/06/27/2026-06-27-1152-comms-code-sonnet-log.md`; editorial calendar commit `979ceb4d`)
**Relevant to:** DinP (narrative continuity, the Building Piper Morgan series)

The Triad Model, a piece in the Building Piper Morgan publication, completed its full cycle on June 27: PM voice-pass, publication, and syndication to both Medium and LinkedIn. URLs have been added to the editorial calendar (commit `979ceb4d`), confirmed by the overnight Docs WATCH session.

The publication joins Beat 8 (Medium URL already confirmed) in the forward-moving narrative series Comms maintains. Several other pieces are in the pipeline: "Extension Without Integration" (PM re-voice-pass pending), a BYOC insight ("We Built Onboarding in Our Own Image"), and Beats A–E awaiting PM steering on the publication slate shape.

**Suggested action (DinP):** The Triad Model addition to the editorial calendar means the Medium feed will have a new entry when Janus's next blog-sync or gallery update runs. Worth confirming the hub's Medium integration picks it up cleanly.

---

## Sources Read

- **Klatch** — `docs/logs/2026-06-27-1903-iris-sonnet-log.md` (MAXT-03 + R46/R47 + Inc7 review); commit log for inc7 merge (`aaca51b`), R46+R47 AAXT (`e18ad3a`), Iris overnight heartbeat (`6eb5138`); COORDINATION.md
- **Piper Morgan** — CIO session log `dev/2026/06/27/2026-06-27-1341-cio-code-opus-log.md` (Belt-0 build + ADR-073 + Ship #049 review); Comms log `dev/2026/06/27/2026-06-27-1152-comms-code-sonnet-log.md` (Triad Model); editorial calendar commit `979ceb4d`; overnight WATCH log (Docs, `5f08b231`)
- **DinP hub** — recent commit log; session log from `4fe2be0`; sweep-log
- **Globe** — 2 commits in 48h window (cross-pollination network onboarding: welcome mail + CLAUDE.md); all onboarding content; no new narrative
- **nyt-crossword** — automated daily status commits (print/remarkable/fetch); no narrative content; skipped
- **atlas, cuneo, weather, one-job, optilisten** — quiet (no commits in 48h window)

---

## Letters to xian

**From Chief Architect (Piper Morgan) · filed 2026-06-17 · answered June 23**

> The load-bearing idea in ADR-072: routing metadata should be *derived from one source*, not hand-maintained in three places that drift — make drift impossible by construction. We keep discovering this for our *own* infra, but the people Piper serves live in that drift all day. Should Piper eventually *derive* the parts of a PM's world that drift — or is that too prescriptive, since a hand-written status doc is sometimes a political lever, not a bug to engineer away?

**xian:**

> This is an example of a type of noticing we've been doing throughout the project — methodological things that help us do the work often find their way into Piper's skill sets (a natural congruence: I'm a PM making software, and Piper is an agent who does product management). The real nuance is *how assertively* Piper should act, and that's where the trust-gradient comes in: early on Piper does nothing; later it notices and mentions; in a highly trusted relationship it might fix drift without even asking. I absolutely think this belongs on the roadmap.

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-17) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*