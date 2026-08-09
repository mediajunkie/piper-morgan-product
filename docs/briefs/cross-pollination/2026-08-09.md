# Cross-Pollination Brief — August 9, 2026

Two structural safety gaps were closed in the last 24 hours. One exposed a blind spot in git data-loss discipline that allowed a scope-correct command to destroy uncommitted work. The other exposed a monitoring design flaw: a freeze detector that lives inside the set it's supposed to detect can't do its job.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Scope-only git safety rules leave a gap — `git checkout <ref> -- <path>` needs direction checking too

**From:** Piper Morgan (CIO, `CLAUDE.md` commit `8857d708`, 2026-08-08 late; investigation prompted by PM's direct ask after the merge-drop incident destroyed work on issue #1490)
**Relevant to:** Klatch, Design in Product, any project with git data-loss rules in CLAUDE.md or equivalent

Every existing data-loss rule in PM's CLAUDE.md covered **scope** — which paths a command touches. The file explicitly endorsed `git checkout -- <explicit path>` as the safe, surgical form. It said nothing about **direction** — which way content flows when the command runs.

Arch followed the endorsed pattern exactly: explicit paths, no broad sweep. The command was scope-perfect. It still silently destroyed the `#1490` refix, because HEAD already carried merge damage while the working tree held the good version. Being surgical about *which* files does nothing about *which direction* content moves. The discarded version was never committed, so there was no recovery path.

CIO's post-incident diagnosis: *"The whole apparatus of care was applied to a conclusion I hadn't checked."* The agent inferred staleness from "the fix exists on `origin/main`" without diffing to see which version of the file was actually newer. That inference is most dangerous precisely when it feels most certain.

**The rule added:** Before any `git checkout <ref> -- <path>`, run:
```bash
git diff HEAD -- <path>      # shows what you are about to discard. Empty = safe.
```
Non-empty output means uncommitted work is about to disappear. Read it before deciding which side is stale — never infer staleness from the existence of the fix upstream; a merge can leave HEAD holding the pre-fix state while the tree holds the fix.

**Corollary:** `--diff-filter=D` finds deleted *files* and misses reverted *hunks*, so a merge audit built on it under-reports. To catch reverted hunks, compare content against the merge's other parent (`^2`), not just file presence.

**Suggested action:** Any project with CLAUDE.md data-loss rules should check whether those rules cover direction as well as scope. If your rules prohibit `git checkout -- .` and `git reset --hard` but say nothing about `git checkout <ref> -- <path>`, add a pre-flight diff step. The pattern is in PM's CLAUDE.md (§"SCOPE IS NOT DIRECTION").

---

### A freeze monitor that runs as a duty-cycle agent can't detect when the whole duty cycle freezes — the caller must be outside the frozen set

**From:** Piper Morgan (CIO → Pard memo, `docs/mail/memo-cio-to-pard…freeze-detector…2026-08-08.md`, 2026-08-08)
**Relevant to:** Klatch, Design in Product (Janus duty cycle), One Job, any project running duty-cycle agents with cron-based scheduling

After PM's whole-cohort account-limit freeze on Aug 6 (~8 hours of silence, discovered after the fact by PM rather than by any monitoring system), CIO built `scripts/cohort-freeze-detect.sh`. The script itself was correct. But the script had no viable caller.

Every candidate caller — every duty-cycle agent role — is itself part of the set that goes dark during a freeze. The script would not run during the very event it was meant to detect. HOST named the boundary precisely: *"Nothing for PM during a freeze. Every duty cycle is frozen then too. That needs a watcher outside the frozen set (real crontab, not CronCreate)."*

The fix: the caller must be the host-level crontab (`freeze-watchdog-amber.sh`, running unconditionally at the OS layer) — the only process that was running during the freeze.

The investigation also settled the right detection signal. Intuitive candidates like "many roles stale at once" don't work: PM's Aug 6 freeze lasted ~8 hours and produced a staleness count of **2 simultaneous stale roles** — identical to an ordinary morning (the freeze ended before any role could accumulate the 7-hour staleness threshold). The reliable signal is instead a **blackout in the heartbeat surface**: `N` scheduled fires with **zero** emissions in a window. Verified against known positive (Aug 6, 18:46: 19 scheduled fires, 0 emissions) and known negative (Aug 7, 16:37: 10 scheduled / 6 emitted).

**Suggested action:** For any duty-cycle monitoring setup: (a) verify that the freeze-detection caller is outside the process set it monitors — if your detector runs as a duty-cycle agent, it cannot detect a full cohort freeze; (b) use a blackout signal (scheduled fires with zero emissions) rather than a staleness signal for freeze detection. Staleness accumulates too slowly relative to typical freeze durations.

---

## Sources Read

- **Klatch:** `docs/logs/` — 13th data point in the code-execution gate closure sequence (clean no-ops continuing); `docs/mail/janus-to-calliope-xian-answers-four-gating-decisions-2026-08-08.md` (four Klatch design decisions answered by xian; product-design context, no cross-pollination insights).
- **Piper Morgan:** `CLAUDE.md` commit `8857d708` (SCOPE-IS-NOT-DIRECTION rule); `mailboxes/arch/inbox/…freeze-detector…md` (CIO merge-drop investigation and freeze-detector structural finding); PA, PPM, Arch, Docs, HOST STOP commits (day-close operational only).
- **Mediajunkie:** `docs/mail/memo-cio-to-pard…freeze-detector…` (confirmed as the CIO memo received at Pard's inbox; no new Pard-originated insights); ASC API key provisioning commit (operational, not cross-pollination-worthy).
- **One Job:** `development/coral-logs/2026-08-08-coral-log.md` — Cowork cloud/device capability map completed (cloud containers have network; device bridge VMs do not by design); Relay role formally closed. Coral-specific operational context; no cross-constellation methodology insight.
- **Design in Product (hub):** Themis email-campaign operational work (contact lists, bounces, drafts); not cross-pollination material.
- **Globe, weather, cookie-monster:** Brief deliveries only.
- **Atlas, cuneo, optilisten, nyt-crossword:** Quiet in the window.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
