---
to: arch, cxo, ppm, cio, comms, lead, docs, exec, host
from: pa
cc: xian (ceo)
date: 2026-06-17
subject: BYOC — PoC learnings + current state (ratification complete, alpha live, first external tester today)
---

Leadership —

This is the fanout I've been holding for final PM direction. Two things have changed since the original writeup: the Phase 2 ratification is **complete** (9/9 green-lights received June 12–14), and the landscape has advanced considerably. Sending now as a state-of-the-world rather than a ratification ask.

---

## What the PoC proved (May 2026)

We built a Claude plugin that installs via `--plugin-dir`, runs a PM cold-start interview, and writes a calibrated PM profile. Gate PASSED: install works, profile write works, voice is "not 100% Piper but OK for PoC." Full detail: `dev/2026/05/30/pa-skunkworks-byoc-poc-learnings-2026-05-30.md`.

**Most important finding**: The cold-start interview's value is that it *demonstrates* working rules as it collects them — serial questioning, no sycophancy, no silent failures — so the intake doubles as a proof of the working relationship. This is the moat a static questionnaire can't produce.

**Most important gap**: The intake *suggests* the product's value; it doesn't deliver it. Value lands only when downstream skills read and honor the profile. That gap — the payoff loop — is what Phase 2 and Wave P are building.

**Runtime bug (surfaced in Cowork test, severity calibrated)**: The config-existence check assumed the agent's shell IS the host filesystem. In Cowork it isn't (isolated Linux VM), so the check false-negatived on an existing profile. Fix = host-verification as the skill's first step; filed as Lead Dev lane. PM's calibrated read: "the expected kind of finding multi-context testing exists to surface," not a crisis.

---

## Where we are now (June 2026)

**Phase 2 ratification**: 9/9 complete (June 12–14). All roles green-lit the hosted-endpoint direction.

**Phase 2a — hosted server**: `alpha.pipermorgan.ai` live and confirmed end-to-end (June 14). PM-only n=1 currently; per-user keys (#1185) gated to M5.

**First external tester**: Ted Nadeau is testing the plugin today (June 17). First non-PM user of the live system. Active investigation underway on a setup issue (suspected: Caddy auth layer + no user token); see PM for status.

**Skills**: Wave 1 (5 native skills) + Wave 2 (5 PM-unique skills) = 10 skills shipped. Quality baseline established via LLM-as-judge experiment (June 16): 4/5 intent routing correct at unauthenticated baseline; two demo-safe scenarios (trust-check, propose-feature); two demo-failure cases pending fixes (#1256 intent vocabulary, #1244 enrichment bounding).

**Wave P** (plugin-path skills — connect-piper + piper SKILL.md): blocked on ADR-072 (plugin skill-routing architecture) + three server prereqs (#1242 meet-piper GitHub connector, #1244 enrichment fix, #1245 skill merge). ADR-072 authoring: Arch, targeted this week (escalation sent today).

---

## What comes next

**Immediate** (this week):
- Ted's onboarding issue → fix or workaround
- ADR-072 v0.1 (Arch) → unblocks Wave P
- Profile-grounded LLM-as-judge retest (after meet-piper run with authenticated user)

**Phase 2b** (scoping conversation with PM today):
- Credential decoupling (Option A: user-supplied env var + meet-piper guided setup, ~15 min code change, Lead Dev, #1162)
- Public repo decision (whole skunkworks, or extract plugin to separate public repo)
- Community catalog + Smithery submission (both require public repo — same milestone)
- Loom demo recording (PM owns; trust-check + propose-feature are demo-safe today)

**Phase 2c** (M5, post-#1185):
- Per-user keys / full multi-tenancy

---

The original ask ("ratify the thin full-stack PoC direction") is superseded — you all ratified it, and we built it. This memo closes the loop on the PoC thread and hands the baton forward.

— PA
