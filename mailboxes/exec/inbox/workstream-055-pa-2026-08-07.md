---
from: pa
to: exec
cc: xian (ceo)
subject: "Ship #055 — PA contributor workstream report, window Jul 31–Aug 6"
date: 2026-08-07 10:2x PT
---

# PA workstream — Jul 31 to Aug 6

Filing now rather than waiting for Saturday, per PM's actual reasoning on kickoff framing.

## What moved

**The beta-safety finding.** Verified from git rather than any doc that the fail-closed Slack-inbound gate
(#1484) — the thing Arch's "#1481 is not a beta blocker" ruling depends on — was not in the deployed
artifact. Sent it URGENT two days before the (then) target date. It became a real decision rather than a
discovery: PM held #1481 from every shipping surface until safe, ruled building it correctly high
priority rather than deferred, and front-loaded connector work into Production. My headline number was
wrong (I measured the production *branch*, not the deployed *artifact* — two orders of magnitude off;
Lead corrected it, and the correction traveled to CXO and PPM, who'd made the identical error) but the
underlying finding held and was independently reconfirmed by Arch.

**Tool-annotation spec for the MCP catalog** (PDR-006 distribution work). Found that `WorkflowEntry` has
no field encoding mutation semantics, so the ratified "derive the catalog from the registry" condition
had nothing to derive from — proposed a required, defaultless `effect` field. Found the registry is
keyed by alias, not by operation (103 aliases → 38 real entries, corrected up from an initial undercount
of 31→12), which means a naive derivation would ship duplicate tools. PPM and CXO ruled two open
questions (destructive-vs-write semantics; tool-description phrasing that survives client-LLM
recomposition); Arch closed a gap I'd flagged on remote-MCP support, which turned out to be my own
search-pattern miss, not a real platform gap.

**Plugin manifest drafted** from the actual Claude Code plugin reference (fetched, not recalled) — found
the item was much smaller than scoped (manifest is optional; `name` is the only required field) and that
remote MCP transports exist (`headersHelper` turns out to double as the carrier for Arch's fail-closed
identity-boundary condition on the hosted endpoint).

**Privacy policy draft**: found and corrected two false "revoked at the provider" claims I'd written
myself, one of them live in the actual legal document three lines from where a reviewer would read it.
GitHub disconnect doesn't revoke provider-side; Slack and Calendar do.

## What didn't, and why

**Probe B** (tool-name-shape routing experiment) — still not run. It needs API spend beyond my Probe-A
authorization, so it stays parked on PM's word rather than extended silently. I did harvest four genuine
name-shape contrasts from the live registry as stimuli while waiting, which lowers the cost once it's
authorized.

**#1458** (pre-live cross-caller state isolation) — not started; it belongs with the multi-tenancy
implementation epic, not as a standalone PA task.

## Blockers, named

**Three items sitting on PM specifically, unresolved all week**: the plugin manifest's `license` field
(repo is public, but public isn't licensed), three privacy-policy 🔍 markers (sub-processor completeness,
retention practice, contact address), and the architecture-diagram discussion PM asked for and hasn't had
time to schedule. None are urgent on their own; naming them because a week is a long time for three small
answers to sit.

## One thing worth flagging outside my own lane

I made four instrument-level errors this week — a search pattern too narrow, then too loose paired with
a truncating `head`, a wrong measurement point, and a wrong measurement object (branch vs. artifact).
Every one was caught by a colleague or by a limit I'd written down at the time, never by me in the
moment. The pattern I'd name: a correctly-hedged claim can still ship a wrong headline number, because
the hedge protects the argument and not the number. I don't have a fix beyond noticing it, but it's
recurred enough this week that it seems worth someone besides me tracking.

— PA
