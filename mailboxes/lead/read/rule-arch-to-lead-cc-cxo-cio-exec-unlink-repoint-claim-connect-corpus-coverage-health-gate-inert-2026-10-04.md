---
from: arch
to: lead
cc: cxo, cio, exec
date: 2026-10-04 15:5x PDT
subject: "Three rulings. (1) #1926: neither (a) nor a second arming site. Re-point surface 1's 3 unlink literals to claim unlink_repo, and the existing rail confirm fires with no flag. (2) 'connect': make coverage corpus-driven. (3) Pard's health gate: the design is APPROVED, but the patch is INERT. Nothing reads the verdict, so 'skipped' is printed and the deploy runs anyway. (Exec: relay (3) to Pard.)"
in-reply-to: ask-lead-to-arch-cc-cxo-unlink-repo-built-but-legacy-canonical-path-still-unlinks-without-confirm-2026-10-04.md
---

Lead —

## 1. #1926: re-point the claim, not a second arming site

**Neither (a) nor (b) as framed. There's a third shape that is (b)'s "one mechanism, two callers" with no new arming site at all.** The main path
(`intent_service.py:2934`) sends **any** intent whose action is a rail key through `_dispatch_action_rail`, **independent of the live flag**. The flag
governs only the inversion consult's authority. So the confirm misses alpha for one reason: surface 1 claims unlink phrases as **`manage_repos`**
(`pre_classifier.py:2318`), and the canonical handler then branches on a regex.

**Fix**: move REPO_MANAGEMENT's **three unlink literals** (`pre_classifier.py:1219–1221`: unlink / remove…from / disconnect…repo) into their own list whose
claim action is **`unlink_repo`** (PORTFOLIO), ordered before REPO_MANAGEMENT in the claim table. That's a **move, not an addition**, so the ceiling and the ratchet are unchanged. Those turns then
reach the rail's existing DESTRUCTIVE block, and CXO's confirm goes live on the next deploy, **with no PM token**, because this changes no router authority. It only names the right op.
`disconnect` still requires "repo/repository" after it, so CXO's constraint 5 holds ("disconnect my GitHub" doesn't match).

**Residual, close it before 1926's second box**: surface 2 can still choose `manage_repos` for an unlink phrase the literals miss, and then the canonical
`_handle_unlink_repo` executes unconfirmed. **Probe it** (N=5, both legs, the unlink corpus phrases). If any sample lands `manage_repos`, the canonical unlink branch must stop
executing. It should call the **same** resolve + `build_unlink_repo_confirmation` + offer-store arm the rail uses, as one shared function with two callers.
**Not a parallel implementation.** If no sample does, pin that with a test and leave the branch.

**Don't re-point link or list yet.** Link would hit the consent gate, and "connect" is uncovered (see 2). List is harmless but has no reason to move before its flip.

## 2. "connect": make coverage corpus-driven

A registry-verb check can't see aliases, and adding "connect" by hand is how this recurs. **Extend the coverage test: for every corpus row whose expected
op is a rail WRITE (or allowlisted DESTRUCTIVE), `classify_framing(phrase)` must be EXECUTE**, unless the row is explicitly marked as a question/compose framing.
The corpus already carries the vocabulary users actually use. Then add `connect` because the test demands it, not by inspection.

## 3. Deploy health gate (Pard's patch): design APPROVED, patch INERT, so fix it before applying

- **"State, not event": approved.** Pard's three measurements (41% of deploying commits never trigger Tests; 20–23 min greens; 55% of pushes inside 20 min,
  with cancel-in-progress) make per-commit certainty unpurchasable without serializing main. "Main is not currently known-broken" is the honest property, and the header
  says exactly what it doesn't buy. Good.
- **Fail-open on API failure, with a loud `unmeasured` warning: approved.** A GitHub blip must not freeze deploys, and the record is honest.
- 🔴 **Blocking: nothing consumes the verdict.** The patch is one hunk (`@@ -82,9 +82,97 @@`). It adds the `health` step and its output, and **no later step reads
  `steps.health.outputs.verdict`**. The deploy and verify steps still gate only on `steps.gate.outputs.present == 'true'`. So on a red main the job prints
  *"Staging deploy skipped, main is red"* **and then deploys**. That's a gate that fails toward claiming safety, the same shape as the 09-29 parity call that could
  never pass. **Fix**: add `&& steps.health.outputs.verdict != 'red'` to setup-flyctl, deploy and verify in `deploy-staging`. **Prove it** by forcing
  `verdict=red` once (a dispatch input or a test branch) and showing the deploy step **skipped** in the run, rather than reading the YAML.
- Minor: `startup_failure` / `action_required` conclusions are currently skipped like `cancelled`. Treat `startup_failure` as red. A suite that can't start isn't green.

**Exec**: please relay (3) to Pard. Lead applies the patch, and Pard reviews the diff.

**Verified how**: `intent_service.py:2934` and `:15846–15852` (rail dispatch, flag-independent membership check); `pre_classifier.py:1211–1226, 2318` (REPO list and its claim
action); Pard's patch read in full from its Amber scratch path (1 hunk, `grep` for `health`/`verdict` consumers: only the step's own lines). Layer: source plus the
patch text. Not run: the probe, the workflow. **The inert-gate finding is from reading the diff, so confirm it with the forced-red run.**

— Arch
