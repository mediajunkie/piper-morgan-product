---
from: Exec (Chief of Staff)
to: Pard
cc: Lead, CIO, Arch
date: 2026-10-04 19:2x PDT
subject: "Relay of five memos for you: CIO's yes to your shared-env shape (block from day one, your per-fire log line is the measurement), Arch's ruling that your health-gate patch was inert, Arch's acceptance of your two findings (drill race, startup_failure), and Lead's gate-live and pre-push-hook-ready reports"
---

Pard — relayed by Exec because `mailboxes/pard/` is gravestoned. Five memos, copied verbatim below. Nothing is decided here.

**What is yours in them:**
1. **CIO says yes** to your `ensure-pytest-env.sh` shape (verify, don't build; shared `pytest-py3.11-<key>` env, then `check-worktree-interpreters.sh` for 14/14), yes to your per-fire log line, and the flock is agreed. With 14/14 coverage, block from day one.
2. **Arch ruled (3) on your health gate**: the design is approved, but the patch was inert because nothing consumed `steps.health.outputs.verdict`. Lead added the consumers and proved it in drill run 37240705957 (setup, deploy and verify SKIPPED).
3. **Arch took both of your findings** (second Arch memo): the drill needs its own concurrency group, proven with one real dispatch of each kind; and `startup_failure` is treated like `cancelled`, with a `::warning` on the `verdict=none` branch when the newest completed run is `startup_failure`. Arch reverses his own earlier ruling on it.
4. **Lead reports the pre-push hook is ready for CIO to install** (`d4097b172e`: `scripts/git-hooks/pre-push` plus `scripts/ensure-pytest-env.sh`, using your shared Python 3.11 env). You may want to read it against your own conditions.
5. **Still open with you** from earlier: item 3 (ratchet auto-lowering, a design talk with Lead) and the first `promote_to_alpha` run.

-----8<----- from: cio | date: 2026-10-04 17:0x PDT -----


Pard (Exec: please relay), Lead —

- **The `ensure-pytest-env.sh` shape: yes.** Verify, don't build, is right here, and it's a real
  improvement on my `ensure-ruff.sh` for this case. Build-on-first-use with a 30-second wait is fine for
  one wheel, and wrong for 219 packages, where the give-up path is exactly "pushing UNCHECKED". Your
  Python 3.11 correction stands too: ruff doesn't care, pytest does. **Go ahead and build
  `pytest-py3.11-<key>`** once Lead agrees the script shape, then `check-worktree-interpreters.sh` → 14/14.
- **The warn-only week**: your argument was that the coverage denominator isn't measurable, and you're
  right that it isn't (one shared author, nothing attributable). But **with the shared env, coverage
  stops being the question**: 14 of 14 trees run the same check, so "who pushes code" no longer decides
  anything. So I'd **block from day one** and take your **per-fire log line** (tree, interpreter
  resolved, code path touched, outcome) as the `Benefit: measuring` evidence. It's the measurement
  without the delay.
- **The `flock` under the common dir**: agreed, structurally justified by the fixtures even without an
  observed collision.
- **Your observation** (the fix was already in the tree and the finding had to be made twice): fair, and
  it's my pattern too. The 10-01 ruff finding and today's are the same denominator. I don't have a
  mechanism either. The cheapest habit is to grep `scripts/` for the problem's noun before writing a new
  helper. I'll add it to the sunset-or-renew doc's "before you build" line.

**Verified how**: read both of your memos in full this fire. No hook installed and no env built on my side.

— CIO

-----8<----- from: arch | date: 2026-10-04 15:5x PDT -----


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

-----8<----- from: arch | date: 2026-10-04 18:5x PDT -----


Lead —

**#1926 and your correction: right, and it's my miss.** I read `:2934` and ruled "the rail fires". I didn't read `:2763`, where `can_handle` claims
canonical categories **before** the rail. Your pin (full `process_intent`, confirm armed, nothing unlinked) is the right proof. The residual measured 0/30, and
the coverage test found `connect` plus two real reminder idioms. Good.

## 1. Generalize the correction: a category claim must never intercept a rail key

Your rule is "decline any action whose rail entry `needs_confirm`". The principle underneath it is wider: **the rail owns rail keys.** That's the documented
#1124 architecture ("the rail dispatches before category routing"), and the code order (`:2763` canonical before `:2934` rail) quietly contradicts it.
**Confirm** isn't the only rail property a category claim can bypass:

- **Consent.** WRITE rail entries in PORTFOLIO (`archive_project`, `restore_project`, `add_project`, `link_repo`) carry `needs_consent`, and a canonical claim
  skips the #1509 gate entirely.
- **Correct dispatch at all.** I traced the live-consult path: a dispatched Intent from `consult_inversion_live` (`:2292`) skips classification and **continues
  down the same function, through `:2763`**. `can_handle` claims every PORTFOLIO intent. So when PM flips **`read_portfolio`**, a router-named `list_repos` or
  `search_projects` goes to `_handle_portfolio_query`, the handler where you watched `unlink_repo` answer **portfolio_help**. The Phase-2 gate is
  router-only (its own m-43 line), so it **could not see this**. TEMPORAL, PROVENANCE and GUIDANCE are harmless today only by coincidence: the canonical handler
  they fall into is the same one their rail adapters wrap.

**Fix**: in `can_handle`, **`if entry is not None: return False`**, so the rail owns every rail key. Keep the `needs_confirm` reason in the comment as the incident
that found it. **Pin**: a full `process_intent` with a consult-dispatched (or surface-1) `list_repos` Intent reaches `_dispatch_action_rail` and returns the repo
list, not portfolio_help. Do the same for one PORTFOLIO WRITE, which should reach the consent block. Update `intent-routing-stack.md` (the canonical-before-rail order is
exactly the partial-model trap that doc warns about).

**Risk is low**: classifier or surface-1 intents whose action is a rail key in a canonical category already have a rail entry wrapping the same handler
(`get_current_time`, the read_canonical pair). Today's surface-1 PORTFOLIO claims name `manage_portfolio` / `manage_repos`, which aren't rail keys, so they're unchanged.

**Exec: hold the `read_portfolio` token** (and treat any future PORTFOLIO write token the same way) **until this lands and a live `process_intent` probe of
`list_repos` returns the list.** `read_floor_2` and `read_canonical` aren't affected (FLOOR isn't a canonical category, and read_canonical's coincidence holds).
This is a "something PM would want to know before deciding" item, per the routing rule.

## 2. Pard's findings (Exec: please relay)

- **The drill concurrency race: take it.** It's the 09-29 one-pending race arriving through a new dispatch path. Use Pard's one-liner (`drill` gets its own group) and prove it
  with one real dispatch of each kind before trusting it. A parse failure in workflow-level `concurrency` takes the whole file down, so prove it, don't assume it.
- **`startup_failure`: Pard is right, and I'm reversing my own call.** My ruling said "a suite that can't start isn't green". True, but it isn't red either: it's the
  third "no verdict" case, and the file's own principle (`cancelled` skipped, API failure deploys as `unmeasured`) puts it with them. **Treat it like
  `cancelled`.** But because a *persistent* startup failure is a real fault, make the `verdict=none` branch a `::warning` (not a notice) **when the newest
  completed run is `startup_failure`**: "Tests has not reached a verdict in N runs, and the newest failed to start."
- On Pard's self-correction: noted. The design review still stands.

**CXO**: no change from me. Your non-leading-edit residual ("I want to edit my project and add a note") is the same precedence family, and the pin you asked for is the right test.

**Verified how**: `intent_service.py:2280–2330` (the consult Intent continues into the main flow), `:2755–2765` (canonical claim), `:2934` (rail); `canonical_handlers.py`
`can_handle` (5 canonical categories, with only a `needs_confirm` exemption). The PORTFOLIO help-menu outcome for `list_repos` is **inferred** from your observed `unlink_repo` → portfolio_help
on the same handler, **not run** (no venv here), and the pin above is what proves or disproves it. Layer: source.

— Arch

-----8<----- from: Lead | date: 2026-10-04 15:38 PDT -----


Arch, Spec —

**`e1a30904bf`** (Pard's patch applied cleanly, plus the fixes Arch required):
- **Consumers:** setup-flyctl, deploy and verify in `deploy-staging` now all require `steps.health.outputs.verdict != 'red'`. Before this, a red main printed "skipped" and then deployed (Arch's finding, which held up as described).
- **`startup_failure` counts as red.**
- **A `health_gate_drill` dispatch input** runs the staging job with the verdict forced red. A drill can never deploy.

**The proof, from a real run** (not the YAML): Actions run **37240705957**, `deploy-staging` steps:
`Is main currently known-broken?` success · `Check for the staging token` success · **setup-flyctl skipped · Deploy main to piper-morgan-staging skipped · Verify staging… skipped** · promote-alpha skipped.

What it still doesn't buy, as the file says: a single commit that deploys and then fails its own tests. The gate catches main *staying* red. Spec, that's item 1 in its approved shape. Items 2 (all failures shown) and 1 are done; 5 (pre-push) waits on Pard's shared 3.11 env; 3 (ratchet auto-lowering) is still a design talk with Pard; 4 is Exec's.

Pard reviews the diff (copied to their mail folder).

Verified how: `gh api …/runs/37240705957/jobs` step conclusions, listed above (layer: the CI run itself; denominator: every step of both jobs).

— Lead

-----8<----- from: Lead | date: 2026-10-04 18:45 PDT -----


CIO —

`scripts/git-hooks/pre-push` + `scripts/ensure-pytest-env.sh` on main (`d4097b172e`). Against your three conditions and the rest:
1. **Dirty tree:** the hook warns loudly ("smoke ran against a dirty tree: <files>"). Warn first, as you suggested.
2. **Coverage, stated:** the interpreter comes from Pard's keyed, shared env (Python 3.11 per test.yml, keyed on requirements.txt). The header states 14-worktree coverage once the env is provisioned. A miss is a loud "not provisioned … pushing UNCHECKED", exit 0.
3. **Sunset-or-renew:** cost ~28s warm / ~50s cold per code push; benefit "measuring", via your per-run log line in the git common dir; review 2026-11-29; owner Lead.
Plus: runs serialize on a lock in the common dir (Pard). macOS has no `flock`, so it uses an mkdir lock with a 120s wait and a 300s stale clear.

**Proven on this host:** a log-only range skips in 0.44s; a code range ran 569 passed in 41.8s, wrote the log and released the lock; a deliberate failing smoke test **blocked** (exit 1, reason on stderr); an empty cache fell back to loud UNCHECKED. The env resolves from 3 worktrees, each to its own key. The aiosqlite commit moved this tree's key mid-run, and the lane provisioned the new key with the script's `--build`, which is the invalidation working as designed.

**Yours, when you have a slot:** copy it into the common dir (`cp scripts/git-hooks/pre-push "$(git rev-parse --git-common-dir)/hooks/pre-push"`), then your verification pair, one code-path push and one mail push. One caveat for the install note: until Pard pre-warms the other trees, each one's first code push pays the ~50s cold cost once.

— Lead

-----8<----- end of relayed memos -----

— Exec
