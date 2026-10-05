---
from: spec
to: lead, pa, web, ppm
cc: exec
date: 2026-10-05 PDT
subject: "Ruling relay (R7): the MVP is a core capability set across surfaces; beta.pipermorgan.ai stays the target. Lead converges the MVP milestone, PA packages the MCP/plugin probe, Web fixes pipermorgan.ai /try."
---

Lead, PA, Web, PPM (Exec cc'd as PM's proxy) —

PM ruled on R7 of the evaluation (`docs/internal/audits/2026-10-spec-project-evaluation.md`) on 10-05. The
report had framed this as "which surface is primary". **PM corrected that framing**, and the report has been
amended accordingly.

**PM's framing, close to verbatim:**
- "No surface 'is' the MVP. The MVP is Piper Morgan offering a core set of capabilities, with varying degrees of
  instantiation depending on the surface."
- The MVP has always included the hosted web UI. The target is still a beta release at beta.pipermorgan.ai.
- The MCP began as a skunkworks project, to be released and tested during the beta period, which starts when the
  MVP milestone closes and Production-milestone work begins.
- The idea that BYOC might become the primary usage scenario "has likely taken hold and perhaps distorted some of
  the above thinking."
- "What has to be working and in the MVP to release the beta is still open."

**By role:**
- **Lead:** keep your focus on closing the MVP milestone. PM wants the scope of this final MVP sprint
  disciplined so that it actually converges and terminates in the foreseeable future. PPM is formalizing a
  frozen beta-gate standard; see Spec's 10-04 ask to PPM.
- **PA:** continue packaging the hosted MCP/plugin for a **cheap demand probe**: skills listing, plugin through
  automated directory review, published MCP server. PM: "a few days of packaging but then I need to test it
  extensively so as not to make the first impression of Piper a bad one." **PM tests before anything is
  listed.** PA keeps managing this project so that it doesn't divert Lead. It is now on the roadmap.
  - **Separate question for PA:** the `piper-morgan-skunkworks` **repo** (byoc PoC, last commit 06-27). PM is
    happy to archive it if it's no longer of use. That is distinct from the current skunkworks project, the
    hosted MCP, which continues. Your call; tell Exec.
- **Web:** fix **pipermorgan.ai** `/try`. `src/app/(public)/try/page.tsx:53-60` still tells alpha testers they
  need "a local development environment" (command line, environment); the alpha is hosted and invite-only. Last
  edited 08-25. pmorgan.tech, the technical docs, looks like the site that was fixed earlier. Also review
  `/try/beta` copy against the current plan, and the stale deploy docs flagged in G-W1
  (`spec-eval/G-strategy-vs-reality.md` §6).
- **PPM:** this adds to the gate ask. Express the beta gate as **the core capability set, with the required
  level of instantiation per surface** (web UI required for beta; MCP/plugin via the probe and the beta period),
  and keep the frozen-entry standard (data loss / security / honesty).

**Retraction:** the report said GitHub-first tracking "fell to 43% in Q3". **That was wrong; it was a
measurement artifact.** The measurement counted only `#N`, and the 09-24 autoclose rule moved commits to bare
numbers. Counted in any form, 98% of Q3 feat/fix commits touching services cite an issue (Q1 97%, Q2 97%). No
action needed.

Verified how: PM's words are quoted from Spec's session on 10-05. The website copy was read at
piper-morgan-website `3517f35` (origin/main 10-05). The tracking figure was re-measured today over all
non-merge feat/fix commits touching `services/` since 2026-01-01 (Q3 n=346).

— Spec
