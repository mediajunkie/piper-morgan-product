# Deployment Pipeline — Plan v0.2 (for PM's ruling)

**Author**: Arch · **Date**: 2026-09-20 (v0.1 morning, v0.2 evening) · **Status**: PROPOSED, nothing
built except §3a's `/health` item, PM-approved same-day (#1839, shipped).
**Tasking**: PM, via Exec — *"define and implement a real deployment pipeline… write down a plan for
how we should start doing it now and then operationalize it."* PM's stated top priority.

**What this is**: a plan to rule on, not a pipeline. PM said the prior expectations *"can be
revised"*, so they are treated as a starting point below, not a constraint.

**v0.2 changelog**: §4 rewritten from "(A) keep the droplet vs (B) collapse it" — a framing PM's own
Exec found was wrong, not merely one option among two — into a completion path, per PM's direct
follow-up ask (*"how do we complete the Fly migration in a nondisruptive way…"*). §4d added, folding
in Pard's two requirements (test-account policy, Web's verification access). §2's security caveat and
§6's item 3 (struck, done) were amended earlier the same day and are unchanged here.

---

## 0. The one-sentence diagnosis

**The build system and the release marker have been tracking different things, and nothing could
answer "what is running" without SSH — so the pipeline didn't fail, it was never observable enough
to fail loudly.**

Verifiable: `.github/workflows/docker.yml` builds on `push: branches: [main]`. The branch that means
"released" is `production`. **Nothing connects them.** An image exists for every main push; the
`production` ref moves only when someone remembers. That is exactly why *"I'm not sure what version
is on alpha"* was an unanswerable question rather than a lookup — and why `production` sat ~4,195
commits stale until today.

---

## 1. What already exists — so we extend rather than rebuild

This is **not greenfield**, and the plan is cheaper because of it. Verified in repo this morning:

| Component | State |
|---|---|
| `VERSION` file + **annotated git tags** | ✅ live — `v0.8.12.0` resolves to `a16f03e44` |
| `docs/releases/RELEASE-NOTES-*.md` | ✅ **current through v0.8.12.0**, cut today. The notes discipline is holding. |
| `scripts/check-release-notes.sh` | ✅ exists |
| `scripts/check-release-parity.sh` | ✅ exists, and **earned by incident #1413** (2026-07-16: a parity claim aged 48 minutes; a later deploy silently dropped a live login fix; beta login regressed for a two-day latent window). Its own header states the principle this plan is built on: *"A parity CLAIM is a statement about a moment; this script makes it a statement about NOW, verified."* |
| `.github/workflows/docker.yml` | ✅ builds images on main pushes |
| Blue-green deploy on the droplet | ✅ **proven today** — old tree preserved at `/opt/piper-old-0.8.10.14`; rollback is two `mv`s and an `up`; ~7 min downtime |
| `docker-compose.staging.yml` | ⚠️ **present** |
| `.env.staging` / `.env.staging.example` | 🔴 **BOTH ABSENT** — so `scripts/deploy_staging.sh`, which requires `$PROJECT_ROOT/.env.staging` at line 12, **cannot run as configured** |
| Staging in CI | 🔴 referenced only by `quarterly-maintenance.yml`; **no deploy workflow mentions it** |

> 🔴 **Finding worth its own line: we have already paid for staging tooling that nothing can run.**
> A staging script, a staging compose file, and a staging verifier exist; the env file they depend on
> does not, and no workflow invokes them. This is the same shape as a hook that looks configured and
> never fires — **presence is not liveness.** Any plan that says "add staging" without saying this
> would be proposing to buy the same thing twice.

---

## 2. The version story — stage vs. environment (Exec asked; it's the crux)

**Three different things currently share two words.** This is most of the confusion:

| Word | Sense 1 — **audience stage** | Sense 2 — **environment/host** | Sense 3 — **git ref** |
|---|---|---|---|
| alpha | early testers | the DigitalOcean droplet | — |
| beta | wider testers | the Fly app | — |
| production | "the real thing" | — | the `production` branch |

So *"production maps to alpha and later to beta"* is a sentence that has to mix two vocabularies to
be sayable — which is a reliable sign the vocabulary is wrong, not the speaker.

**Proposal: separate them permanently.**

- **Environments** are named by *role*, never by audience: **`local` → `staging` → `prod`**. An
  environment is a place code runs.

> 🔴 **AMENDED 2026-09-20 15:5x — this rename is NOT free, and I nearly shipped it as though it
> were.** `PIPER_ENVIRONMENT` already exists with the vocabulary **`development` / `production`**,
> and it has **security-gate consumers that compare against the exact string `"production"`**:
> `services/security/encrypted_types.py:57` (an unset `ENCRYPTION_MASTER_KEY` is *fatal* on the write
> path — #1387; any other value silently restores warn-and-write-**plaintext**),
> `services/auth/jwt_service.py:177` (#1087 fail-loudly), `services/utils/env_hygiene.py:44`.
> **Setting a near-miss like `prod` disarms all three silently.** So adopting this vocabulary is a
> **migration that must change those call sites first**, not a naming decision. I found this by
> checking the consumers of a variable I had already used in shipped code — the same
> enumerate-the-consumers rule I wrote for #1812 the day before, applied a few hours late to my own
> change.
- **Stages** are named by *audience*: **alpha → beta → GA**. A stage is who is allowed in. A stage is
  a property of a *release*, not of a host.
- Today's alpha-testers are served **by the `prod` environment at the `alpha` stage.** When beta
  opens, the same `prod` environment serves the `beta` stage. **Opening beta becomes an access
  decision, not a migration** — which is a significant simplification over "later it maps to beta."

**Consequence for the `production` branch**: under this scheme it stops being the release marker and
becomes redundant with the tag. **Recommendation: retire it**, or demote it to a pure record of
what's deployed. Two refs that mean "released" is how the 4,195-commit drift became invisible.

---

## 3. "How does a change reach a user, and how do we know it did"

### 3a. The single highest-value fix, and it's small

🔴 **Nothing can currently answer "what version is running" without SSH access.** Lead had to read
`/app/VERSION` inside the container. Exec confirmed no unauthenticated version surface exists.

**Every other gate in this plan depends on being able to ask that question cheaply.** A promotion
gate that can't read the current version isn't a gate.

> **Recommendation 1 — expose the deployed version.** `/health` already returns 200 unauthenticated
> and already reports per-service health. Add: **version, git SHA, and build timestamp.** Then "what's
> on alpha" is a `curl`, the attention rollup can carry it automatically, and staleness becomes
> *visible* instead of *discovered two months later*.

⚠️ Scope note: this is the one recommendation I'd ship *before* the rest of the plan is ruled on,
because it is cheap, reversible, and unblocks measurement of everything else. **PM's call, but I'd
take it now.**

### 3b. The promotion unit is a built image, not a branch merge

Today: merge to main → image builds → someone eventually deploys something. The artifact and the
marker are decoupled (§0).

Proposed: **tag → image → promote the same image forward.**

```
main ──(tag vX.Y.Z)──> image:vX.Y.Z ──> staging ──(gate)──> prod
```

The *same artifact* is promoted, never rebuilt per environment. This kills the entire class of
"works in staging, differs in prod," and it makes the parity script's job structural rather than
vigilant.

### 3c. The gates, deliberately few

PM: *"some gating for moving between them."* Matching *"this is not rocket science"*, I propose
**two** gates, both already mostly built:

- **main → staging**: CI green + `check-release-notes.sh` + `check-release-parity.sh` (all exist).
  Automatic. No human.
- **staging → prod**: a **watched** smoke drive on staging — one real user flow, not a `curl` 200
  (m-43: a curl is not a render test). Human says go.

### 3d. When to cut a release

PM: *"a way of deciding when to cut."* The failure was never a bad rule; it was **no trigger at
all**, so "haven't cut in ages" was nobody's alarm.

> **Recommendation 2 — make the *absence* of a cut visible rather than legislate a cadence.** A cut
> happens when a user-facing change is ready; **and** a weekly check reports *product-code drift
> between `prod` and `main`.* Not a deadline — a number that shows up.
>
> **Today that number is 24 commits ahead, of which _0 touch product code_** (`services/`, `web/`,
> `alembic/`, `*.py`, Dockerfile, compose). So alpha is genuinely current in the only sense that
> matters, and the metric already distinguishes "24 behind" from "24 behind that matter" — which a
> naive commit count would not.

---

## 4. The droplet — completion path (AMENDED 2026-09-20 evening, v0.2)

> **This section replaces the original (A)-vs-(B) framing below the line, which was wrong in a way
> worth stating rather than quietly editing away.** I originally posed keeping vs. collapsing the
> droplet as a live choice PM had to make. **Exec's archaeology (verified by me against
> `decisions.log` before I amend anything here) shows it isn't one**: a full Fly.io migration was
> **already decided and executed** — org, app shell, database, Redis→Fly Upstash, ChromaDB to its
> own Fly app — on **2026-07-10, cutover 2026-07-12** (`decisions.log:189,191`, PM+Lead in the #1278
> walkthrough, quoted verbatim). **Every deploy since has gone to Fly. Alpha simply never followed.**
> So "(A) keep vs (B) collapse" was the wrong question — **(B) is finishing a decision already made**,
> and "keep the droplet" isn't a neutral default, it's an unfinished migration wearing the shape of a
> choice.
>
> **There is also a recorded *functional* reason, not just a historical one, that Fly was preferred**:
> `decisions.log:179` (2026-07-09, my own #1382 concur) — *"the droplet has no python-keyring backend,
> so per-user OAuth/slack/calendar keychain ops fail."* We built an encrypted-DB fallback specifically
> to route around a limitation the droplet has and Fly doesn't. The droplet isn't merely older; it's
> the surface that structurally can't do something we need.

### 4a. The design call this unlocks: retire the droplet, don't replace it with a second Fly app

If §2's environment-vs-stage split is adopted, the completion path is simpler than "migrate alpha to
its own Fly deployment." **Alpha and beta stop being two environments and become two *stages* of
access to the same `prod` environment**, which already exists on Fly and has run since 2026-07-12.
Opening alpha on Fly is then an **access-list decision** (who gets in), not an infrastructure build
(where does it run) — exactly the simplification §2 promised, now cashed against a real decision.

**This also removes a real blocker that existed until three days ago**: pre-#1812, alpha's droplet
had its own operator/server-key semantics that differed from beta's. That distinction is now gone —
PM's own account "gets normal-account semantics by default... no system credential concept"
(`decisions.log`, 2026-09-19 ~13:0x). **Alpha and beta are now the same account model**, which is a
precondition for them safely sharing one environment that this plan didn't have when it was written
this morning.

### 4b. What has to happen, phased for zero disruption

PM's two facts from Exec's memo make this the cheapest it will ever be: **zero active users**, and
**cost is explicitly not the driver** (both hosts are affordable; the ask is consolidation, not
savings). That means the phasing below can be sequenced for safety, not speed.

1. **Confirm Fly's `prod` app can serve alpha's access pattern** — an access-list gate (who is
   admitted) in front of the same app beta uses, not a parallel deployment. *(Lead/Pard's call —
   I don't hold Fly credentials and haven't inspected the app's current config.)*
2. **Migrate droplet-local state.** ⚠️ **AMENDED 2026-09-21 — my "very likely near-empty" guess below
   was wrong, and worth leaving visible rather than quietly fixing.** Lead's live recon (09-21,
   `psql` over SSH against both hosts) found the droplet holds **6 real users, registered as recently
   as the day of the recon**, a live unused invite token, and the uploads bind-mount — while Fly's
   own DB is the stale side, 4 users frozen since 07-13. **This is a real data migration, droplet →
   Fly, not a no-op** — the opposite of what "zero active users" led me to infer. "Zero active users"
   was true of *testers on the invite*, not of *the droplet's actual database*, and I conflated the
   two without checking. Superseded original text: ~~Redis, ChromaDB, and the database are already
   on Fly infrastructure per the 07-10 decision... given zero active users, this is very likely
   near-empty.~~ Runbook: `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`.
3. **Cut `alpha.pipermorgan.ai`'s DNS to Fly.** Reversible up to the DNS TTL; the droplet stays warm
   as rollback until step 4 is verified, same blue-green discipline as today's droplet deploy.
4. **Verify on the real domain** — the layered verification plan v0.1 §3c already specifies (a
   watched real-user flow, not a curl), run against `alpha.pipermorgan.ai` now pointed at Fly.
5. **Decommission the droplet.** Only after step 4 passes. This is the step that actually stops the
   spend; everything before it is preparation.
6. **Retire the `production` branch** (§2's proposal) and update any doc/runbook that still names the
   droplet as `alpha`'s host — the *"no single document says so"* finding from §1 applies to this
   migration's own record-keeping too, not only to the pipeline's steady state.

### 4c. What this plan does NOT resolve, named rather than glossed over

- **I have not inspected Fly's current app configuration** — whether it already has volumes/capacity
  provisioned for a second class of traffic, or whether alpha's admission needs its own Fly resources
  inside the same app. That's an empirical question for whoever holds Fly credentials.
- ~~**The actual size of droplet-local user data is unverified.**~~ **RESOLVED 2026-09-21, and I was
  wrong**: 6 real users, not near-empty. See §4b step 2's amendment.
- **This plan does not set a timeline.** PM said no rush twice; nothing above manufactures one.

**Consolidated answer to "how do we complete the Fly migration in a nondisruptive way and put this
class of issue to bed"**: it already IS a completion, not a new migration — the infrastructure exists
and has run for two months; what's missing is an access decision, a DNS cut, and confirming
droplet-local state is truly empty before the last step. The reason it never happened isn't that it
was hard; alpha simply had nobody chasing it the way beta's cutover was chased in July.

### 4d. Two requirements folded in, per Pard's 09-20 memo (the un-owned remainders)

Pard named two inputs this plan must cover rather than leave implicit. Both are requirements on the
*design*, not new design choices — folded here rather than as a parallel document, per Pard's own
scoping.

**Test-account policy, per environment.** Under 4a's collapse, this becomes simpler than it would
have been under two separate environments: **one account model, one test-account policy**, gated by
stage (alpha/beta access list) rather than duplicated per host. Requirements this plan commits to:
- **A cold account is a first-class fixture** — zero seed data, no chat history, no bound connectors,
  available on demand. Web's two stalled verification attempts (09-07, 09-08) were both blocked on
  this not existing; whatever mechanism mints test accounts must produce a genuinely cold one, not a
  reused one.
- **Test accounts exercise the post-#1812 model only** — normal-account semantics, no operator/server-
  key fallback. This is now the *only* model (4a), so there is no longer a legacy path a test account
  could accidentally validate instead.
- **The `connector_bindings.mcp_server_ref` landmine is a named migration step, not an implementation
  detail** — it stores literal per-environment URLs (compose hostname vs. `.internal`), so any
  test-account or DB-state copy between environments needs an explicit repoint step until ADR-070A's
  resolver lands. Section 4b step 2 (state migration) must account for this if any droplet-side
  fixture data is carried forward.

**Web's verification access path.** Pard's finding — *"today the honest answer is: it doesn't [have
one]"* — is confirmed by this plan's own §3a finding (no unauthenticated version surface existed) and
is now **partially resolved**: #1839 (shipped this fire, see §3a) gives Web an unauthenticated
version/health surface per host, satisfying requirement (b) below once `PIPER_ENVIRONMENT` is set per
host (still open — see the #1839 issue). Full requirement set, carried into the gates (§3c):
- (a) **a per-environment access statement for Web** — what it can reach, with what credential, minted
  by whom, on what turnaround. Not yet written; owed as part of operationalizing §3c's gates.
- (b) **a version/health surface Web can read without SSH** — ✅ in progress via #1839.
- (c) **no routine verification gate routes through ad-hoc peer action** — token-minting for Web's
  access must be a provisioned path, not a favor from whoever happens to hold droplet SSH that day.
  This is a **consequence** of 4b step 1 (an access-list gate) done right: the same mechanism that
  admits alpha testers should be the mechanism that provisions Web's verification credential, not a
  separate manual process.

**Not resolved by this plan**: the concrete provisioning mechanism for (a)/(c) above. That's
build-level detail for whoever implements 4b step 1's access-list gate, informed by these
requirements rather than reopening them.

---

## 5. What I'd do first, in order

1. **Expose version + SHA on `/health`** (§3a) — small, reversible, unblocks measurement of
   everything else.
2. **Write down what runs where** — three environments, three providers, one page. It does not exist
   today, and §1 shows what its absence costs.
3. **Close the `.env.staging` gap** (§1) or delete the staging tooling. **Either is fine; the current
   state — present, unrunnable, uninvoked — is the worst of the three**, because it reads as coverage.
4. **Then** ratify §2's vocabulary and §3's gates, and operationalize.

**Nothing above asks to build the pipeline this week**, per Exec's scope note. Items 1–3 are hours,
not days, and each stands on its own if PM rules differently on the rest.

---

## 6. Open questions for PM

1. **§2 vocabulary** — adopt environment-vs-stage separation, and **retire the `production` branch**?
   *(§4a now depends on this: the droplet completion path only simplifies to "an access decision" if
   this is adopted. If PM prefers to keep alpha/beta as separate environments, §4b's phasing still
   works but doesn't get the simplification — flag if that's the intent.)*
2. **§4's completion path** — approve the phasing in 4b (access-list gate → verify state is empty →
   DNS cut → verify live → decommission), or redirect if I've misjudged the risk anywhere.
3. ~~**Recommendation 1**~~ — **DONE, unprompted.** PM approved this same-day via Lead's relay; #1839
   shipped this fire (§3a). Struck rather than left looking open.
4. **Anything more pressing?** Exec relayed PM's invitation to say so. **I don't think so** — but I'd
   flag that #1818 and #1823 are both mid-build and touch first-contact experience, and #1837 (today's
   dogfood transcript) now blocks epic 3's own floor per PPM — so if beta opens soon those compete for
   the same week as this plan's operationalization.

---

**Verified how**: every "exists" claim in §1 checked in the repo this morning — `VERSION` read,
tags resolved (`v0.8.12.0^{commit}` = `a16f03e44` = `origin/production`, so the tag and the deployed
ref agree), release-notes directory listed, `docker.yml` trigger block read, `deploy_staging.sh:12`
read for its env-file dependency, and the absence of `.env.staging`/`.env.staging.example` tested by
file existence. Drift measured with `git rev-list --count origin/production..origin/main` (24) and
`git diff --name-only` filtered to product paths (**0**). **Layer: repo state, static.**
**Denominator: 4 of 4 deploy/release scripts opened; 1 of 1 build workflows read; 0 of 3 live hosts
touched — I hold no credentials, so every claim about what is *running* is Lead's SSH read (alpha
v0.8.12.0, verified in-container today) or Exec's relay, cited as theirs, not re-derived by me.**

**§4/4d verified how (added, v0.2)**: independently re-read `decisions.log` lines 179, 189, 191 at
`origin/main` this evening — the 07-09 #1382 keyring rationale, the 07-10 14:00/14:15 Fly migration
decision, all quoted verbatim above, not taken from Exec's memo on trust. #1812's account-semantics
ruling confirmed by grep against the 2026-09-19 ~13:0x entry. #1839's shipped state confirmed by its
own commit on `origin/main` this session. **Layer: decisions.log + repo state, static. Denominator:
3 of 3 cited decisions.log entries independently re-read; 0 of 1 live Fly app configurations
inspected (no credentials) — 4c states this gap explicitly rather than assuming an answer.**
