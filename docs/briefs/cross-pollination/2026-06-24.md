---
date: 2026-06-24
status: substantive
sources_checked:
  - piper-morgan
  - klatch
  - mediajunkie
window: "~48h (June 23–24, 2026)"
---

# Cross-Pollination Brief — June 24, 2026

Mediajunkie shipped `beta.mediajunkie.com` yesterday — a fully-operational RAG system over the blog corpus, migrated from local Mac compute to a droplet in a single session. PM's Architect articulated "derive-don't-maintain" as a formal design principle across three ADRs and an entity-model spec. And all three projects independently converged on the same meta-principle: represent what the system actually knows and can actually do, not what you'd prefer it to seem like.

*Note: automated sweep trigger offline during xian's account migration. Manual sweep by Janus.*

---

## Key Insights

### 1. Mediajunkie: Local RAG + droplet-exposure pattern is live and reusable

**From:** Mediajunkie (`logs/2026-06-23-pard-log.md`)
**Relevant to:** Piper Morgan, Klatch

Pard built and shipped a RAG pipeline over the mediajunkie blog corpus, then migrated from local Mac compute to a cloud stack (Together AI Llama-3.3-70B + serverless e5 embeddings) in the same session. Live at `https://beta.mediajunkie.com`.

The reusable exposure pattern: **droplet nginx as public front door, reverse-proxying to local compute via a self-healing reverse SSH tunnel.** Once on the cloud stack, the droplet becomes the full compute surface.

Practical lessons: context window size is a deployment decision (`num_ctx=128K` → CPU spill on M1 Air; cap to 4096 → 100% GPU). Together AI is Cloudflare-fronted (needs browser UA). e5 serverless caps at 512 tokens per document.

### 2. PM: "Derive-don't-maintain" formalized as Architect signature pattern

**From:** PM (Ship #048, ADRs 070–072)
**Relevant to:** Klatch, Mediajunkie

Three ADRs this week share a design principle: derive outputs from canonical sources so vocab and registry can't drift by construction. ADR-072 derives skill-routing vocabulary from SKILL.md frontmatter. The Architect is now asking whether users' drifting artifacts should be derived the same way.

Klatch relevance: Daedalus's EntityManager (AAXT R42) is the same design question — can EntityManager vocabulary be derived from a registry rather than maintained in parallel spec + implementation?

### 3. PM: MEMORY.md compression solves silent truncation

**From:** PM CIO (Ship #048)
**Relevant to:** Klatch

MEMORY.md compressed 42KB → 22KB, back under the silent-truncation threshold. Agents were reading the memory surface incomplete without knowing what was cut. Fix is mechanical compression. methodology-30 (Consumer-Trace Verification) promoted to Proven simultaneously.

Klatch: audit byte-count of frequently-read agent surfaces (Calliope's rollup is the most-read candidate).

### 4. Cross-project: honest provenance as shared principle

**From:** all three projects

PM: D1 design theme — "Watch not Blockers"; trust-gating must surface itself.
Klatch: blog false-claim corrections — UI unreleased; xian is the only user.
Mediajunkie: RAG calibration — small model on constrained hardware degraded; fix was right-sizing, not papering over it.

Shared discipline: build to what the system can actually do; surface limitations; prefer honest silence over false confidence.

---

## Emerging Patterns

**Manual operations as a forcing function for process clarity.** Automated trigger was offline but the manual sweep ran fine from the process spec — intended behavior.

**Single-session full-stack migrations.** Pard's session: local Mac compute → always-on droplet with Together AI in one run.

---

## Background Changes

- PM watchdog alerts: account migration caused multiple role-silence events (expected, not a production issue)
- Klatch: Calliope 6/24 START; AAXT R42 in progress; Iris design reviews merge-ready
- PM Beat 8 published; Ship #048 draft awaiting xian voice-pass
- Mediajunkie: `beta.mediajunkie.com` live; corpus tooling stable

---

## Sources Read

**Piper Morgan:** `docs/public/comms/drafts/weekly-ship-048-draft-2026-06-19.md`, git log (30 commits)
**Klatch:** `docs/operations/duty-cycle/cycle-logs/cycle-log-calliope-2026-06-23.md`, git log (12 commits)
**Mediajunkie:** `logs/2026-06-23-pard-log.md`
