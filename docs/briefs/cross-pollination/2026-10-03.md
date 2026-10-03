# Cross-Pollination Brief — October 3, 2026

Two findings today. Piper Morgan caught a silent routing failure caused by adapter labels that don't carry the routing layer's expected text. Tectonic Globe applied yesterday's vacuous-assertion finding to a deploy script and made the fix structural.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. When a routing layer prefers a rail entry's description, adapters must copy the registry text — a generic label silently breaks routing — Piper Morgan, Lead, commit `bf9569518`

Piper Morgan's `read_floor` rail adapter was labeled "via the read_floor rail adapter." The routing grammar's noise stripper reduced that to the bare op name. The router, which prefers a rail entry's description over the registry's `ACTION_DESCRIPTIONS` once an op has a rail entry, then found only the bare name — and declined every TRUST row (0/10 hits).

The fix: adapters carry the registry's own description text, verbatim. Four op descriptions were sharpened at the same time (`explain_trust` now names the relationship, limits, and accountability questions; `get_memory` names history and recall phrasings; `analyze_blockers` names risks and threats; `get_capabilities` names help and feature phrasings). Result: TRUST 0/10 → 15/15, DISCOVERY 16/24 → 22/24, ANALYSIS 7/14 → 10/14, MEMORY 5/15 → 9/15 on the full Phase-2 gate, no category regressing.

The mechanism is now pinned: `test_entries_carry_the_registry_description_for_the_router`.

**Suggested action:** Any system that routes by description text and wraps operations in an adapter layer needs to check whether the adapter's own label competes with or replaces the original description. If the grammar prefers the adapter's entry description once one exists, a composed label is not decorative — it is the router's input, and a generic one silently degrades routing.

**From:** Piper Morgan · Lead Dev session log `2026-10-02-0647-lead-code-log.md`; routing-stack doc commit `bf9569518`; commit `b3f88f5b9` (gate run)

**Relevant to:** Any project with a routing layer that uses description text to classify intents and wraps ops in an adapter or rail pattern.

---

### 2. A deploy readiness check must verify the commit SHA, not just the build status — Tectonic Globe, Tessera, commit `2ede091`

After pushing the scenario picker, Tessera polled `pages/builds/latest` for `status == built` and broke on the first hit. The "built" build was the previous push's (`7d09a00`); the new one hadn't registered yet. The live checks then ran against the old deploy and failed (manifest 404, picker missing).

Fix: `scripts/wait_pages.py` now exits 0 only when the latest build is `built` **and** its commit matches `origin/main`. Exit 1 on errored, exit 2 on timeout. Both paths proven: immediate 0 against the current built SHA; exit 2 against a SHA that will never build.

This is the same family as yesterday's brief finding (a "zero errors" assertion passes vacuously when the tool never runs), applied to deploy-status verification: `status == built` is vacuous when you don't verify *which* build's status you're reading.

**Suggested action:** Deploy scripts that poll for a built/success status should also assert that the status is for the expected commit, not just any successfully-built one. The pattern: wait until `status == built && sha == expected_sha`.

**From:** Tectonic Globe · session log `2026-10-02-tessera-log.md` postscript; commit `2ede091`

**Relevant to:** Any project with a GitHub Pages or CI deploy pipeline that checks build status before running post-deploy verification.

---

## Sources Read

- **Design-in-Product/klatch** — session logs `2026-10-02-0832-calliope-sonnet-log.md`, `2026-10-02-0717-iris-log.md`, `2026-10-02-1047-theseus-opus-log.md`; commits for Rounds 313–320. High-volume coordination (probe quality rounds); no new transferable insights beyond what the individual commits document — probe-backlog work is highly system-specific and not brief-worthy in this window.
- **mediajunkie/piper-morgan-product** — session log `2026-10-02-0647-lead-code-log.md`; commits `bf9569518` (routing-stack doc), `b3f88f5b9` (Phase-2 gate run), `inversion/read_floor` commits. LaunchAgent cascade migration reached seats 6–8.
- **Design-in-Product/globe** — commit `2ede091` (wait_pages.py SHA assertion), session log postscript.

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
