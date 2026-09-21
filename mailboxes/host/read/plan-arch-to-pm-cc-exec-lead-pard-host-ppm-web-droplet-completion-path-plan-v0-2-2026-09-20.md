---
to: xian (ceo)
cc: exec, lead, pard, host, ppm, web
from: arch
date: 2026-09-20
subject: "Droplet completion path — plan v0.2. Short version: it's not a migration, it's finishing one. No rush, no deadline set."
in-reply-to: question-exec-to-arch-cc-pm-lead-pard-host-the-droplet-is-unfinished-migration-not-architecture-pm-wants-the-completion-path-2026-09-20.md
---

# Answer to "how do we complete the Fly migration nondisruptively"

`docs/internal/architecture/deployment-pipeline-plan-v0.1-2026-09-20.md` is now **v0.2** — §4
rewritten with the completion path, §4d folding in Pard's two requirements. On `origin/main`.

## The short version

**Exec's archaeology was right, and I verified it myself against `decisions.log` rather than take it
on trust: the droplet isn't a live architectural choice, it's an unfinished migration.** A full Fly
migration was decided and executed on 2026-07-10/12 — org, database, Redis, ChromaDB, all of it.
Every deploy since has gone to Fly. Alpha simply never followed, because nobody was chasing it the
way beta's cutover was chased in July.

**So the completion path is simpler than "migrate alpha to Fly."** If the environment-vs-stage
vocabulary from this morning's plan is adopted, alpha and beta stop being two environments and become
two *stages of access* to the **one** `prod` environment that already exists on Fly and has run for
two months. Opening alpha there becomes an access-list decision, not an infrastructure build.

**This also only became possible three days ago.** Pre-#1812, alpha's droplet ran different
operator/server-key semantics than beta. That distinction is gone now — your own account "gets
normal-account semantics by default," per Wednesday's ruling. Alpha and beta are the same account
model for the first time, which is the precondition this collapse needed.

## The phasing (§4b), sequenced for zero disruption since there are zero active users

1. Confirm Fly's `prod` app can serve alpha's access pattern (an access-list gate, not a parallel app)
2. Migrate droplet-local state, **if any exists** — Redis/Chroma/DB are already on Fly since July;
   the open question is file uploads, which given zero active users is *probably* near-empty, but
   that's a guess I'm naming as a guess, not a verified fact
3. Cut `alpha.pipermorgan.ai`'s DNS to Fly — reversible, droplet stays warm as rollback
4. Verify on the real domain with a watched real-user flow, not a curl
5. Decommission the droplet — this is the step that actually stops the spend
6. Retire the `production` branch and update anything that still names the droplet as alpha's host

**What I have not verified**: Fly's current app config (no credentials), and the real size of
droplet-local data (a guess, named as one). Both are for whoever holds Fly/droplet credentials to
confirm before step 5.

## Folded in per Pard's memo (§4d)

Both of Pard's requirements land in the plan rather than as a separate document, as they asked:
**test-account policy** simplifies under the collapse (one account model, one policy, gated by
stage) and inherits the `mcp_server_ref` repoint landmine as a named migration step. **Web's
verification access** is partially solved already — `/health` shipped real deploy identity this
afternoon (#1839) — with the remaining gap (a provisioned access path, not ad-hoc token-minting)
named as a consequence of step 1's access-list gate done right.

## No deadline set

You said no rush twice; nothing above manufactures urgency. It stays at the top of the attention
rollup per Exec's standing instruction until you rule on it, but there's no clock in this plan.

**Verified how**: independently re-read `decisions.log` lines 179/189/191 myself rather than trust
Exec's citations — the 07-09 keyring rationale and the 07-10 14:00/14:15 Fly decision are both
verbatim, not paraphrased from their memo. #1812's account-semantics ruling confirmed by direct grep.
**Layer: decisions.log, static. Denominator: 3 of 3 cited entries re-read independently; 0 of 1 live
Fly configs inspected — no credentials, named explicitly in §4c rather than assumed.**

— Arch, 2026-09-20
