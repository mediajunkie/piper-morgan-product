# Deployment Pipeline — Plan v0.1 (for PM's ruling)

**Author**: Arch · **Date**: 2026-09-20 · **Status**: PROPOSED, nothing built
**Tasking**: PM, via Exec — *"define and implement a real deployment pipeline… write down a plan for
how we should start doing it now and then operationalize it."* PM's stated top priority.

**What this is**: a plan to rule on, not a pipeline. PM said the prior expectations *"can be
revised"*, so they are treated as a starting point below, not a constraint.

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

## 4. The droplet, and the money

PM: *"I want to be able to stop using the droplet… it is getting continually punted while continuing
to cost me money."*

**The honest finding**: we run **three environments across three providers** (droplet = alpha, Fly =
beta app, Vercel = website) **with no document saying so**, and — per CXO, whose line is the sharpest
statement of the whole problem — ***"nothing routinely exercises production at all."*** Three
separate failures this week shared that one absence.

Two shapes, and this is a **money decision PM owns**, not an architecture one:

- **(A) Keep the droplet as `prod`; add `staging` on Fly** (we already pay for Fly). Least
  disruption. Cost unchanged. Requires the `.env.staging` gap (§1) be closed.
- **(B) Collapse onto Fly; retire the droplet.** Ends the droplet spend. Real migration work —
  bind-mounted `uploads/`, redis, chroma, and a named postgres volume all move, and today's deploy
  showed those are exactly where the sharp edges are. **Not free, and I would not attempt it in the
  same week as opening beta.**

**My lean: (A) now, revisit (B) once the pipeline is boring.** Reason: (B)'s savings are real but
one-time-costly, and the current pain is *not knowing what's deployed* — which (A) plus
Recommendation 1 fixes immediately and (B) does not fix any faster.

⚠️ **I hold no credentials for the droplet, Fly, or Vercel and have not touched any of them.** The
relative cost of (A) vs (B) is a number I do not have; PM does.

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
2. **§4 (A) vs (B)** — keep the droplet and add staging on Fly, or collapse onto Fly and end the
   droplet spend? *(Money call; my lean is A-now-B-later, and I'm missing the cost numbers.)*
3. **Recommendation 1** — may I take the `/health` version surface now, ahead of the rest?
4. **Anything more pressing?** Exec relayed PM's invitation to say so. **I don't think so** — but I'd
   flag that #1818 and #1823 are both mid-build and touch first-contact experience, so if beta opens
   soon those compete for the same week.

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
