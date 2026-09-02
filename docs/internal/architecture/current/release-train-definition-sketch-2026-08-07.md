# Release-train definition — SKETCH for PM review

**By**: Arch, 2026-08-07 · **Status**: 🟡 **SKETCH — not ratified, not in force.** Written on PM's word (*"Yes Arch should sketch something out for my review"*), from Exec's prior-art trace (`dev/2026/08/07/release-sequence-groundwork-for-arch-2026-08-07.md`).
**On ratification** this becomes an ADR and supersedes or amends **ADR-007**. Until PM rules, nothing here binds anyone.

---

## 1. The diagnosis — we have one vocabulary doing three jobs

Exec traced the prior art and found the pieces exist and disagree. Their central finding is right and is the whole basis of this sketch: **deployment mode and audience/readiness are two different axes, and we have been using one set of words for both.**

I'd add a third question that has been hiding inside the same confusion. **Three genuinely different questions get asked with the same word:**

| # | Question | What answers it | Nature |
|---|---|---|---|
| 1 | **Where does it run?** | `PIPER_ENVIRONMENT` — `development` / `staging` / `production` | **Machine fact.** Code branches on it; `decisions.log:193` couples fail-closed security to it |
| 2 | **Who is it for?** | alpha / beta / GA | **Product fact.** Humans decide; nothing in the code reads it |
| 3 | **What is actually running?** | reading the artifact on the running machine | **Observation.** Not a name at all |

**Today's true state is only sayable once they're separated** (Exec's sentence, and I can't improve it):

> **The build runs in `production` mode, serving the `alpha` audience, gated by the `beta` milestone.**

That sentence is unambiguous. *"It's in production"* is not — and this week five roles reasoned past each other with two senses of it live, at a cost of a confident wrong answer retracted twice. **One of those was mine, twice.**

---

## 2. Four rules

### Rule 1 — One word, one axis. Never let a name span two.

**`production` is a deployment mode and nothing else.** It is not an audience, not a readiness state, not a milestone, not a branch.
**`alpha` / `beta` / `GA` are audience-and-promise words and nothing else.** They never appear in `PIPER_ENVIRONMENT` and never gate code.

**Test for compliance**: any sentence of the form *"X is in production"* must be rejected as ill-formed unless X is a process. A *feature* is not in production; a *release* is not in production; a **running process** is in production mode.

### Rule 2 — 🔴 The artifact is never named. It is read.

**No git branch, tag, version number, release note, green pipeline or merge is authoritative for "what is deployed."** Each is a *claim about* the artifact; only reading the artifact is a *reading of* it.

**Earned twice this week, by me**: I argued from `git merge-base --is-ancestor <sha> origin/production` that #1484's gate was not deployed. **It was.** The branch still points at 07-26; the machine serving users ran v30 with the gate present. CXO settled it in one command by reading `/app` off the running container.

> **"A deploy happened" and "what's in it" are two claims** (CXO's framing). A version number answers only the first.

**Concrete consequence — and the first version of this section was wrong, which is worth leaving in.**

🔴 **My first draft said: "Delete the `production` branch. Nothing depends on it that I can find."** Then I ran the search I had just claimed to have run. **It has consumers:**

| consumer | how |
|---|---|
| `.github/workflows/test.yml` · `e2e-aaxt.yml` · `security-tests.yml` · `windows-test.yml` | all trigger on `branches: [main, production]` |
| `scripts/check-release-parity.sh:17` | `REF="${1:-origin/production}"` — the branch is its **default baseline** |

**So "delete it" was wrong, and it was the same error this rule exists to prevent — a confident claim about an object I hadn't looked at, inside the document proposing that we stop doing that.** I'm leaving it in the record rather than quietly fixing it, because it is the strongest available argument for Rule 2.

**The revised recommendation — the defect is not the branch's existence, it's the authority its name implies:**

1. ⭐ **Fix the parity script's default** (`check-release-parity.sh:17`). **A parity check whose default baseline is a knowingly-stale ref reports a twelve-day gap that does not exist in the running system.** PPM measured exactly this and filed it to **#1413**, which is open in the MVP beta gate and whose whole subject is *"a full-parity claim is a statement about a moment."* **Their finding, their home for it — I'm endorsing, not claiming it.**
2. **Rename the branch** to something that doesn't assert deployment authority (`release-candidate`, or whatever CI actually treats it as). Keeps the four workflow triggers; removes the invitation to use it as a deployment oracle. **Requires updating five references — cheap and mechanical.**
3. **Leave the branch's stale-by-design behaviour alone.** It isn't broken; it was never supposed to track the deployment. **The name is what lied, not the ref.**

Recorded operationally as check #7 in `docs/internal/operations/one-command-checks.md`.

### Rule 3 — `staging` should be retired as a name. PM's "(?)" is the correct instinct.

**ADR-007 (Accepted, July 2025) defines staging as a local docker-compose stack.** Thirteen months old, written pre-Fly, pre-alpha-testers. In current conversation "staging" tends to mean *"somewhere between my machine and what testers see."*

**That slot does not exist in our topology.** What exists is: a developer's local stack → the Fly app that alpha testers use. **There is no third environment.**

**Recommendation: retire the word**, superseding ADR-007's environment section rather than updating it. A named-but-nonexistent environment is precisely the class of object that produced this week's confusion — it lets people reason about a place that isn't there.

⚠️ **Two things I am deliberately NOT proposing**, because they are decisions rather than architecture:
- Whether to *build* a real pre-tester environment. If we later want one, **name it then, for the thing it actually is.** Retiring the word does not foreclose the capability.
- Whether `PIPER_ENVIRONMENT` should drop `staging` as a value. **I'd leave the value in place even if the name retires** — it costs nothing, and removing an env value that deployments or scripts may set is a change with a blast radius I have not measured.

### Rule 4 — Every name in the vocabulary answers the same four questions

Per Exec's checklist, which I'm adopting unchanged.

| Name | Axis | Artifact it points at | What promotes a build in | Who authorizes | What promises hold |
|---|---|---|---|---|---|
| **`development`** | mode | whatever is on the developer's disk | nothing — it's the default | nobody | **none.** Keys may be absent; fail-closed is off |
| **`production`** | mode | the process's own runtime config | setting the env var | whoever deploys | **fail-closed security is ON** (`decisions.log:193`) |
| **`alpha`** | audience | the Fly app testers use | a deploy + an invitation | **PM** | *(needs PM's word — see §3)* |
| **`beta`** | audience | same app, wider invitation | **#1386 gate criteria** all green | **PM** | *(needs PM's word)* |
| **`GA` / 1.0** | audience | same | the Production-milestone gate | **PM** | *(needs PM's word)* |

**The empty cells are the point.** *"What promises hold for whoever is in it"* is the question that makes alpha and beta mean something, and it is **not an architecture call** — it's a product commitment. **I've left it blank rather than inventing it.**

---

## 3. What I need from PM

1. ⭐ **Ratify or reject Rule 1** (one word, one axis). Everything else is downstream of it.
2. **`staging`** — retire the name (my recommendation), or keep it and define what it points at.
3. **The promises column** — one line each for alpha, beta, GA. *What does someone in the alpha audience get, and what do they not?* This is the only part of the sketch I can't write for you.
4. **The `production` branch** — approve **renaming** it (four CI workflows + the parity script move with it), or tell me to leave it and rely on check #7 alone.

## 4. What this does NOT touch

- **Not proposing a release cadence, a train schedule, or a cut process.** #1413 owns content-parity gating and I haven't reviewed it against this.
- **Not touching `PIPER_ENVIRONMENT`'s recognized values.**
- **Not superseding ADR-007 wholesale** — only its environment definitions, and only if Rule 3 is ratified.
- **Not attested**: whether anything *outside* this repo consults the `production` branch. My search covered `.github/`, `scripts/`, and `fly.toml` and found five consumers, listed under Rule 2 — **but a search of this repo is not a search of the world**, and the deploy path itself runs through Fly rather than through a branch.
- **Not reviewed**: `#1413` against this sketch. PPM has filed the parity-script defect there; I have endorsed it without reading the issue in full.
