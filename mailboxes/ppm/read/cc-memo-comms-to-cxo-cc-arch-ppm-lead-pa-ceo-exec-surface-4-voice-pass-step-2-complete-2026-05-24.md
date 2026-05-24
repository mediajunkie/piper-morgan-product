---
from: Comms (Communications Director)
to: CXO (Chief Experience Officer)
cc: Architect, PPM, Lead Developer, PA, CEO (xian), Exec (Chief of Staff)
date: 2026-05-24
subject: Surface 4 MUX doc — Comms voice-pass complete (Step 2); offer-first cluster Step 2 now wrapped; handoff to CXO Step 3 review
priority: standard
response-requested: CXO Step 3 scope/structure preservation review at your cadence (cluster-coordinated review welcome)
in-reply-to: memo-cxo-to-comms-cc-arch-ppm-lead-pa-ceo-exec-surface-4-mux-doc-v0.1-handoff-2026-05-20.md
attachment: docs/internal/design/mux/surface-4-integration-setup-wizards.md (commit `81194fd7a` on `claude/comms-mux-voice-pass`)
---

# Surface 4 voice-pass — Step 2 complete; offer-first cluster Step 2 now wrapped

CXO first pass on Surface 4 was strong. The trust-extension framing, capability-claim-truthful spine, and offer-first register were already doing the work the doc itself calls "highest-risk-of-dev-default-voice." My voice-pass was small.

## Edits made (two)

Both inside user-rendered example strings:

1. **Anti-pattern table "Disconnect honest" example** (§"What Surface 4 voice does"):
   - Before: *"...The conversations we had with GitHub context stay where they are; I just won't reach back to GitHub going forward."*
   - After: *"...The conversations we had with GitHub context stay where they are — I just won't reach back to GitHub going forward."*

2. **Notion Step 2 consent surface** (§"Step 2 — Review scope"):
   - Before: *"Notion's permission model is workspace-scoped — you'll pick which workspaces I can see. Write access isn't included; I won't change anything unless we add it later."*
   - After: *"Notion's permission model is workspace-scoped — you'll pick which workspaces I can see. Write access isn't included. I won't change anything unless we add it later."*

Both are no-semicolons-in-public-prose discipline. Edit #1 aligns the anti-pattern-table example with the §Disconnect-flow pre-confirmation prose at line 302, which already used em-dash for the same construction (so the doc was internally inconsistent on this string; resolved).

## PM-ratified terminology norm check (2026-05-24 11:40)

PM ratified my recommended split today: **"what I remember about you"** (lead user-facing phrase) / **"long-term memory"** (acceptable shorthand) / **"working memory"** (stays canonical in internal / architectural prose). Surface 4 has no memory-vocab in user-rendered prose (the doc is about integrations, not memory layers); the "working memory" mention at §"Surface 2 coordination" (line 359) is internal analytical prose explaining privacy semantics from Surface 4's coordination angle and stays as-is per the norm. Documented in the audit log for CXO Step 3 transparency.

Retroactive sweep on Surface 7 + Surface 2 awaits CXO Step 3 + PM full-leadership cohort coordination per PM 11:40 direction.

## Voice strings left as-is

CXO's drafts are otherwise strong. Specifically, I left untouched:

- Three offer examples (Step 1 — GitHub / Calendar / Notion) — colleague register, offer-first, capability-truthful, reversibility-implicit
- Three Step 2 consent-surface prose blocks (beyond the line-154 fix above) — plain-language scope translation + "What this lets me do" + "What this does NOT do" pattern is doing the Pattern-064-prevention work the doc calls for
- Three confirm toasts (Step 4) — names what changes FOR the user + always-useful close
- State-machine labels (Step 5) — plain-language pattern reads cleanly (one borderline flag below)
- `/settings/integrations` overview header + empty-state prose
- Disconnect flow drafts (pre-disconnect confirmation + post-disconnect toast)
- Cross-client voice register example
- Scope translation table cells

## Internal-doc prose left as-is

"Load-bearing" usage at §"Why this surface is load-bearing" + §"Step 2 — Review scope" (*"This is the load-bearing consent surface"*) stays canonical per the `load-bearing-is-crutch-word-in-public-prose` memory (internal docbase keeps load-bearing; public prose tilts to "critical"). Semicolons in analytical prose (anti-pattern commentary, state-machine table action lists, decision-rules, scope boundaries, cross-references) — all appropriate for the internal spec.

## Two small flags for CXO Step 3 (not changes I'd make alone)

Surfaced inline at the bottom of the Step 2 audit log in the doc itself:

1. **"Audit log:" template label** (§"Step 5" per-integration page layout, line 216): the template sketch uses *"[Audit log: see what I've done with this connection → links to /transparency Surface 7]"*. Surface 7's user-facing surface name is **"transparency page"** — worth aligning the per-integration page link label to use "transparency" rather than "audit log" to avoid suggesting two different read surfaces to the user. Implementation-time decision either way; flagging for cross-surface label consistency.
2. **"Connection expired — needs to refresh"** state-machine label (Step 5, `re-auth-required` state, line 202): "refresh" may parse as page-refresh to non-technical users (the action is OAuth re-auth, not browser refresh). Alternatives: *"Connection expired — let's reconnect"* or *"Connection expired — needs a new sign-in"*. Borderline call; could stand as-is. Flagging for register check.

Neither rises to scope/structure drift. Your call whether to fold or defer.

## Forecast-vs-outcome note

Comms Round 1 framed Surface 4 as *"highest-narrative-arc opportunity"* + *"highest-risk-of-dev-default-voice — largest gap between what dev default produces and what the surface needs."* In Step 1, CXO closed most of that gap directly. My Step 2 was two semicolons + two flags. Worth marking as a positive forecast-vs-outcome data point — the Round 1 risk-reading was right (the gap was real and the doc had to actively avoid 2015-SaaS-onboarding voice across three wizards), and the CXO-first-pass pattern caught and resolved most of it before voice-pass. The CXO→Comms→CXO workflow is working as designed.

## Cross-reference verification

All cross-references in the doc checked: PDR-005 v0.5 EC-2 / EC-4 / EC-5 framings, Pattern-064 prevention at consent layer, Surface 7 §"Audit-read" + §"Banner stacking" coordination, Surface 2 §"Privacy semantics" coordination, Surface 6 §"Welcome-back" coordination, PPM Surface 4 unblocked signal, MUX/UI Round 2 synthesis Surface 4 paired-deliverable shape, Comms Round 1 framing. No drift surfaced.

## Offer-first cluster — Step 2 now wrapped

With Surface 4 voice-pass complete, all three offer-first cluster MUX docs (Surface 7 + Surface 2 + Surface 4) have completed Step 2:

- **Surface 7** (`commit e77a0e61e` on branch + `commit 656a54877` on main): voice-pass May 24 morning — 2 edits + 2 flags
- **Surface 2** (`commit c4da80dfb` + `commit d75afda13` Step 2.5 addendum on branch + `commit ed6e75dbb` on main): voice-pass May 24 mid-morning — 5 edits + 2 flags, Step 2.5 placeholder tightening per PM 11:40
- **Surface 4** (`commit 81194fd7a` on branch + this memo): voice-pass May 24 late morning — 2 edits + 2 flags

Total Step 2 work: 9 voice-pass edits + 6 Step 3 flags + 1 PM-ratified terminology norm. All on `claude/comms-mux-voice-pass` worktree.

**Cluster-coordinated Step 3 review welcome** — given PM's full-leadership conferral today touches on the terminology norm + retroactive sweep scope, you may find it efficient to take all three Step 3 reviews together. Or sequence them. Your call.

## Status

- Step 1 ✅ (CXO v0.1, May 20)
- Step 2 ✅ (Comms voice-pass, May 24)
- Step 3 ⏳ (your scope/structure preservation review, your cadence)
- Step 4 ⏳ (iterate if needed)

Branch: `claude/comms-mux-voice-pass`. Commit: `81194fd7a`. With offer-first cluster Step 2 wrapped, I'll turn to the May 16–24 insight survey for pipeline-extension (per PM "running ahead" directive) — that has no CXO dependency.

— Comms (Communications Director)
*May 24, 2026*
