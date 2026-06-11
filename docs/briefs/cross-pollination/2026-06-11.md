# Cross-Pollination Brief — June 11, 2026

PM resolved how the hosted beta will handle user API keys: a four-rung resolution chain where server-stored-encrypted — the beta plan — is the endgame fallback built first, not a detour. A long-standing GitHub integration bug was diagnosed and fixed: every personal-access-token attempt had been returning HTTP 500 since last November's MCP migration, because the old tests mocked the broken layer and passed, hiding the production failure. And PM's Piper Alpha role migrated to a new account and model (Sonnet 4.6), with a local-vs-cloud cron experiment confirming the cron substrate choice before the handoff. Klatch is quiet today.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. BYO-key credential design resolves: four rungs where the beta plan is the endgame fallback, built first

**From:** PM PA session log `dev/2026/06/10/2026-06-10-0712-pa-code-opus-log.md`; commit `c67dad2` (#1185 converged design); commit `e4b93ca` (#358 revised); June 10 live design walk-through with PM
**Relevant to:** Klatch (if multi-user or per-entity credential storage comes up); DinP (PM public positioning)

PM and PA walked through the BYO-key architecture live on June 10 and converged on a four-rung resolution chain, ordered from most-BYO to honest-decline:

1. **Host-side inference** (true endgame): the user's own Claude host runs inference; PM's server never sees the key. The BYO-colleague/skill-broker model — braintrust converged, post-beta v1.1.
2. **Key passed per request, never stored** (resilient optional layer): the plugin passes the key in-memory only. May persist even after rung 1 ships, as a fallback at other integration layers.
3. **Server-stored encrypted** (the beta rung): the fallback when no BYO key is present. This rung *is* #358 — see below.
4. **Honest offer to configure** (the bottom; never a shared instance key): branches into "configure natively" (lands at rung 3) or "help the user set up their own harness" (lands at rungs 1–2).

The key design finding came from reading the actual issue rather than relying on memory: #358's description claimed an `encryption.py` file in `services/security/` that doesn't exist — the issue was materially stale. The corrected framing: #358 IS the server-stored rung by construction. On a Linux droplet there is no macOS keychain, so encryption-at-rest is the enabling floor for hosted per-user secrets, not compliance polish on top of them. Server-stored-for-beta is the endgame fallback rung built first, not a detour.

A structural principle also landed: **storage capability ≠ acquisition policy**. The encrypted store can hold the full user-secret set (LLM key + all integration keys), but acquisition is need-scoped and just-in-time — the user offers a connection, or Piper asks only when a request needs it.

**Suggested action:** Klatch — the "storage capability ≠ acquisition policy" distinction is worth building in explicitly if multi-entity or per-user credential storage ever comes up. The pattern prevents "can hold all secrets" from silently becoming "asks for all secrets at setup."


### 2. GitHub PAT validation had been returning HTTP 500 for every token since the MCP migration — old tests masked it

**From:** PM Lead Developer commits `6e5229f` (#1192c fix, ~230 LOC) and `2271591` (#1187 floor wiring, ~290 LOC); June 10
**Relevant to:** Both projects (test-fidelity pattern at migration seams); PM (#1187 summarize-fetch now unblocked)

The GitHub settings endpoint (`POST /api/v1/settings/integrations/github/save`) had been returning HTTP 500 for every personal-access-token — valid or invalid — since the MCP migration last November (#198). The cause: the migration left `test_connection` unimplemented on both the MCP adapter and the spatial fallback, so any call raised `AttributeError`. The existing tests mocked `router.test_connection()` to return a happy dict, so they passed while the real endpoint was failing in production. This is the test-theatre failure mode at its most expensive: passing tests, broken feature.

The fix bypasses the adapter entirely. A new `services/integrations/github/token_validator.py::verify_github_token` validates PATs directly via `GET https://api.github.com/user` (the canonical GitHub check: 200 → username, 401 → invalid token). Both the save and status endpoints now use it. The commit notes: "no router/adapter dependency, can't re-orphan" — the fix is structurally resistant to the same failure mode that created the bug.

This unblocks #1187 (summarize-fetch floor wiring for `summarize github issue #N`), which is now code-complete but inert until the full #1192 integrations-last-mile lands a production-native repo-resolution path. The two slices are correctly sequenced.

**Suggested action:** Both projects — when a feature area goes through a structural migration (Klatch's MCP server work, PM's MCP migration), the migration seam is the highest-risk location for test-theatre: the old adapter gets mocked, the new adapter never gets tested. A cheap canary that exercises the actual production code path — not a mock of an intermediate layer — is worth adding explicitly at any migration boundary.


### 3. PA role migrates to Sonnet 4.6 as pioneer agent; local-cron substrate confirmed by A/B test

**From:** PM PA session log (migration handoff section); commits `51fde84` (handoff), `52bb503` (windowed cron), metrics log `bae428d` and `852d9ee` (A/B debrief + migration design); June 10 evening
**Relevant to:** DinP (Janus's own account/model transitions; cron substrate choice); Klatch (Calliope Phase 1 cron substrate)

PM directed two things on June 10: run a local-vs-cloud cron A/B experiment first, then migrate agents back to the main account. Results:

**A/B experiment** (PM ran `RUN-THIS.html`): local + `CronCreate` confirmed as the right substrate. The experiment settled an open question about whether cloud-side scheduling alternatives were worth switching to — they aren't. Calliope Phase 1 and any future DinP cycle agents can treat local `CronCreate` as the confirmed choice.

**PA migration** (pioneer agent): the Piper Alpha role — a key coordinating role for the BYO arc — migrated from Opus 4.8 on the DinP-account worktree to Sonnet 4.6 on the DinP account. PA is the pioneer agent for the re-migration wave; CIO drafts the subsequent agents' handoff context once PA's migration lands clean. The handoff was clean: inbox zero, carry-forward fully updated with successor brief, cron deleted (successor arms fresh with the PM-ratified windowed schedule `42 6,9,12,15,18,21 * * *` — no midnight–4 AM fires).

The windowed cron was itself a June 10 ratification: PM confirmed that overnight no-op fires between midnight and 4 AM are pure cost, so the cron was narrowed to daytime+evening hours only, and the pattern was adopted into the cron-shape-experiments registry as the PA-lane default.

**Suggested action:** DinP — Janus's June 9 account-migration episode (usage cap → surplus account) is structurally the same event type. The PM handoff pattern — carry-forward accuracy + cron deleted for successor to arm fresh — is worth formalizing as a one-page DinP account-transition runbook so the next cap/migration event doesn't require ad-hoc reconstruction. Klatch Calliope — the A/B result (local+CronCreate confirmed) closes the substrate question; the windowed-cron pattern (no overnight no-op fires) is worth evaluating for Calliope's Phase 1 if overnight fires are producing cost without value.


## Sources Read

- **piper-morgan-product**: PA session log `dev/2026/06/10/2026-06-10-0712-pa-code-opus-log.md` (migration handoff section); `dev/active/pa-carry-forward.md` (full); `dev/active/pa-1185-multi-tenant-byo-key-investigation-2026-06-10.md` (converged design section); commits `c67dad2` (#1185), `e4b93ca` (carry-forward), `6e5229f` (#1192c), `2271591` (#1187), `51fde84` (migration handoff), `52bb503` (windowed cron), metrics `852d9ee` + `bae428d`; CIO cycle log `dev/active/cycle-log-cio-2026-06-10.md` (fires 1–8)
- **klatch**: one commit in 48h window (brief delivery only); no substantive agent activity; not listed in `sources_checked`
- **Secondary repos (atlas, globe, cuneo, one-job, optilisten, nyt-crossword)**: no narrative activity in 48h window; nyt-crossword has automated status-only commits

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*