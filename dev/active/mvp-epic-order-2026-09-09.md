# MVP Sprint Backlog — Ordered Epics (source of truth)

**Owner**: PPM. **Status**: live working order — update in place as epics close/reorder, don't
fork a new file per revision. **Purpose**: per PM's 2026-09-09 directive (relayed by Exec), Lead
works ONE epic at a time, fully, before moving to the next. This file is what Lead consults
without needing to ask anyone. Board Status/Sprint fields are the per-issue record; this file is
the *order*, which no GitHub field currently encodes.

**The rule, verbatim from PM's directive**: work the current epic until it's fully closed.
Discovered work goes into (a) the same epic, (b) another epic, or (c) a later milestone — only
work added to the SAME epic delays that epic's closure. Epic-relative progress is legible;
pile-relative progress (the flat "N not done" count) is not.

**Provenance**: cause-factoring by Arch (`factoring-arch-to-ppm...-2026-09-09.md`), 37 Sprint
Backlog items live-pulled 2026-09-09, cross-checked against a fresh pull before ordering (both
agree: 37 items, same membership). Ordering and any reclassification below is PPM's.

---

### 0. `#1595` — EPIC: Understanding-Layer Inversion, "the interpretation spine" — CURRENT EPIC as of 2026-09-25

⚠️ **Corrected 2026-09-25 — PM restated the sequencing rule with NO exemptions**: *"Lead is to
work on the next (lowest numbered unfinished) epic until it is finished or blocked, and then move
on to the next... by definition this means all epics in the MVP milestone get 'a turn.'"* This
epic's earlier framing below (a background sink other epics feed, sitting "above" the sequence)
read as an implicit exemption from that rule — it isn't one. **Epic 0 is the lowest-numbered
unfinished epic and is therefore the CURRENT epic now**, same as any other. Both things are true
at once: it's structurally the default deposit sink for other epics' routing findings (that fact
doesn't change), AND it takes its turn in the sequence exactly like epics 1-10 (that's what
changed here). Lead + Arch both attested Phase 2 is MVP-necessary under PM's criterion
(2026-09-25, see `decisions.log`) — the necessity question is closed, not just the scheduling one.

**Placement ruled by Lead, 2026-09-23** (in reply to this seat's 10:33 flag): its own top-level
slot, never interleaved by dependency and never folded into a single epic, for a structural reason
— **it is the DEFAULT SINK for the other epics' routing findings.** The supersession gate (PM
2026-08-29) means every interpretation-layer failure becomes a corpus row for `#1595`'s
slot-emission lane rather than a local patch, so epics 3/4/5 keep feeding it as they close. An item
other epics deposit into by rule can't live inside one of them without misrepresenting the flow.
**This week's live examples**: `#1841` (ruled + deposit path pointed by Arch 09-22), `#1854`
(Production-milestoned, correctly outside this file's own scope), `#1860` (placed in epic 4 above,
this seat's own call — Lead's framing is that it's simultaneously an `#1595` input, not that it's
mis-homed there; both are true at once, this file tracks the epic-4 placement).

Filed 2026-08-11 (itself the finding at the time: "the largest remaining MVP build... had no GitHub
issue for three days"), Arch-RATIFIED 2026-08-09 (all four decisions, amended twice same day), PM's
fundamentals-first ruling names it "the spine of the moved-beta month."

**Build status — Lead's own words, sourced with the unverified part explicitly named, 2026-09-23**:
"Phases 0–2 COMPLETE as of my 8/24 attestation (SessionSnapshot; gate measured with matched
instruments; per-flow adequacy ruled `#1663`→(b)); wave 1 (`read_status`, 50 ops) LIVE-flipped 8/21
behind a default-empty env flag and **unexercised as of 8/24 — I have NOT re-verified whether any
traffic has hit the flipped categories since, and I'm not going to state a number I haven't
measured.** Waves 2+ not started. The corpus deposits above are the first `#1595` build motion
since 8/24; I'm executing them today per Arch's pointed mechanics (generator inline-source list →
regenerate phase0)." Re-verifying the wave-1 traffic question is Lead's, riding today's deposit
commit.

**`#1897` filed 2026-09-26, found by the unit-4 build itself (Opus lane), measured by Lead same
morning against the real `PreClassifier.detect_multiple_intents`**: a two-part turn where surface
1's read-lane pattern groups claim only HALF the message (the #1527/#1756/#1794/#1881 guards
correctly decline the destructive/write half rather than splitting) — so the turn never reaches
the LLM classifier or the router as a two-part claim, it's silently treated as a single read. Needs
the router to return a plan (Arch's option (b)) rather than a single dispatch; unit 4 can't reach
this case as currently scoped. Added here (third-queue-source criteria line, this seat, same day)
rather than left as a queue gap — filed too recently in the day to have synced before this pass.

## Order

### 1. CI/infra red (13 items, 11 closed) — cheap, and it's a quiet tax on every epic after it
~~`#1687`~~ four CI workflows standing red (**CLOSED, caught 2026-09-26 by a reconciliation pass —
not previously marked**) · ~~`#1711`~~ Keychain ACL hang blocks server startup
silently — **CLOSED**. ~~`#1637`~~ 6 standing test failures poisoning 6 — **CLOSED 2026-09-09/10**.
Plus, filed 2026-09-11 from a direct #1687 close-out audit (same author, same denominator problem,
folded in rather than treated as new epics): ~~`#1747`~~ 'Tests' and 'E2E & AAXT' workflows are
STANDING-RED — outside #1687's own four-workflow denominator, so every subsequent "belt fully
green" claim (including this file's own ship-060 citations) silently meant "the five tracked," the
exact m-44 shape #1687 itself documented (**CLOSED, caught 2026-09-26 by a reconciliation pass —
not previously marked**) · ~~`#1748`~~ CI test-isolation defect — tests write fake
provider keys into the shared per-job Postgres via #1382's DB store, conftest later loads one as
real, turning keyless behavior into live 401s that read as product failures — **CLOSED**. ·
~~`#1749`~~ a deterministic-looking search test fails in CI only, passes locally, mechanism
undiagnosed (env-divergence class) — **CLOSED**. Plus, folded 2026-09-12, both found by the #1748
lane: ~~`#1764`~~ (`EncryptedDBCredentialStore` silently collapses `service_name`, dropping the
namespace dimension the OS-keychain contract has — latent today, needs a migration plan if ever
fixed) · ~~`#1765`~~ (2 `test_cross_user_isolation.py` failures reproduce locally on pristine HEAD but
the Tests workflow is green — #1749's env-divergence class, inverted: local-red/CI-green instead of
local-green/CI-red). **`#1764`/`#1765` both CLOSED, caught 2026-09-26 by a reconciliation pass —
not previously marked.** Plus, filed 2026-09-13 while confirming E2E went green post-rotation:
~~`#1785`~~
(the 211-test canonical-routing cohort makes real live-LLM calls on every push to main, ~20
runs/day at 5-13s/case; open question is whether it belongs on push or moves to AAXT's nightly
opt-in schedule — not decided unilaterally — **RESOLVED 2026-09-19, see below**). **This
"remaining open" list is stale as of 2026-09-26 and not being hand-maintained anymore** — all
five named here (`#1687`, `#1747`, `#1764`, `#1765`, `#1785`) are confirmed CLOSED, caught by a
reconciliation pass; trust the per-item strikethroughs, not this summary line.

**Filed 2026-09-23, folded in same-day**: ~~`#1861`~~ — Lead found `scripts/inversion_phase1_shadow_score.py`
(an `#1595` shadow-scoring instrument) failing 107/107 with an unbound-request-key error; cause was
`#1812` (09-21) retiring the operator/server-key fallback these dev-only scripts had silently relied
on. Never caught because these instruments run on demand, not in CI — self-identified as "the red
nobody sees, `#1608` family" (`#1608` itself is `Ongoing`-milestoned, outside this file's scope, but
the shape is this epic's own). Already repaired same-commit as the `#1841`/`#1860` corpus deposits.
**CLOSED, caught 2026-09-25 by a reconciliation pass — not previously marked.**

**`#1785` RESOLVED 2026-09-19 — shipped, but wholesale, not the split originally recommended,
because the recommendation's own premise was wrong.** Lead's decision memo (routed direct-to-PM,
PPM only cc'd — correct, since the issue was explicitly filed "not decided unilaterally") proposed
splitting deterministic routing (stays on push, free) from live-LLM floor cases (move to nightly).
PM approved the split in conversation, but before shipping, Lead measured rather than assumed and
found no free subset exists: **the canonical job's ENTIRE selection is live-LLM-marked spend,
measured 183/183** — the "deterministic and free" claim came from reading the job's own comment,
not the actual pytest marks. Lead shipped the shape that matches PM's actual intent (kill push-time
spend) — the whole job moves to nightly — told PM in the same exchange, one-line revert available
if wrong. **Worth naming precisely because it's a live instance of exactly the failure class PA's
Cross-Piper synthesis flags for this file's own lane**: a claim true at one layer (Lead's own
initial read of the workflow's comments) doesn't survive being restated as true at another (the
actual pytest marks) — caught before shipping, not after, because Lead re-verified their own
recommendation rather than treating "I already looked at this" as settled. This entry originally
recorded the pre-correction recommendation; recording the correction here rather than silently
overwriting it, per this file's own discipline.

**Why first**: every day CI stays red, every other epic's evidence weakens (a green suite means
less when four — now confirmed six — workflows are already known-broken). Cheap relative to its
value. If it turns out not-cheap, the fallback is explicitly accepting these as known-red rather
than let them silently discount every later epic's signal. **#1747 is itself an instance of that
fallback failing quietly** — the denominator drifted from four to six without anyone's "fully
green" claims noticing, which is exactly the m-44 risk this epic exists to retire.

**Folded 2026-09-22, backlog catch-up**: `#1832` — `test_slack_health_endpoint_exists` asserts a
route (`/health/slack`) that no longer exists, another standing-red instance this epic's own class
covers.

**Two more folded 2026-09-25, both instances of this epic's own "a gate nobody watches" class**:
`#1892` — the `#1845` bearer-credential gate went red on `main` for 8.5 hours across ~35 pushes
from six seats (including this one) overnight before Lead's own START found it by chasing the
lint's numbers, not by anyone watching CI; the credential that tripped it was already dead, but the
same silence would have covered a live one. Proposes some seat's START ritual (or the
freeze-watchdog/attention rollup) print the last Code Quality + Architecture Enforcement conclusion
next to the heartbeat — owner suggestion CIO/Exec, not ruled here. Already fixed same-day (scrub +
lint case-insensitivity). · ~~`#1894`~~ — the link-checker ratchet tripped (92 broken vs. frozen
ceiling 90) the same morning, candidate cause unverified: `claude.ai/code/session_…` URLs appearing
in session-log file contents, which lychee can't fetch and would count as broken — climbing steadily
as more logs carry them if that's the actual class, fix would be a lychee ignore-pattern rather than
chasing individual links. **CLOSED, caught 2026-09-25 by a reconciliation pass — not previously
marked.**

### 2. Security/tenancy (28 items, 22 closed) — **REOPENED 2026-09-14** — before beta wave 1, regardless of everything else
**Original six, all CLOSED 2026-09-12**: ~~`#1734`~~ personality API global-config clobber ·
~~`#1690`~~ demo plugin live-mounted by default · ~~`#1732`~~ chat-render XSS · ~~`#1733`~~ stale
unauthenticated duplicate page · ~~`#1741`~~ pattern-suggestions XSS · ~~`#1740`~~ twin-file
renderer drift. All six live-verified deployed (v74/v76).

**Seven more, from the 2026-09-14 tenancy family**: ~~`#1807`~~ (BYOC key resolution fell through
to PM's own server key for ANY authenticated caller — CLOSED, safe default shipped) · ~~`#1791`~~
(personality preferences have no per-user store — Arch's call whether it forks the ADR-075 D4
overlay — **CLOSED 2026-09-24**) · ~~`#1750`~~ (stale unauthenticated twin, same class as `#1733`
— **CLOSED 2026-09-24**) · ~~`#1751`~~ (canonical
personality-preferences page hardcoded user_id "default" — CLOSED) · ~~`#1809`~~ (`#1807`'s fix is
entry-point-scoped — Slack inbound and any unbound LLM path still resolves the server key; the
durable fix inverts the default so unbound refuses rather than spends, gated on copy — **CLOSED,
caught 2026-09-26 by a reconciliation pass — not previously marked; the "stays open" framing
elsewhere in this epic's own narrative below is now stale, left as historical record rather than
rewritten**) ·
~~`#1810`~~ (setup flow stored a global unprefixed key copy each new user's setup silently
overwrote — CLOSED, v108, the write deleted; readers of the stale slot are `#1809`'s remaining
surface) · ~~`#1812`~~ (the root question underneath the whole family — PM asked why the product owns
an LLM key at all; the agent's own trace found no principled need for one, MVP-milestoned, found
missing from the board and fixed same fire — **CLOSED 2026-09-21, see below**, never struck
through here).

**`#1812` step 5 UNBLOCKED 2026-09-19** — PM ruled in-conversation this afternoon: PM's own account
gets normal-account semantics by default, no special-cased operator key. The transitional
`PIPER_OPERATOR_SERVER_KEY` seam has no remaining principled consumer — steps 5-6 (retire it) are
now buildable, in Lead's queue. Recorded verbatim in `decisions.log` (2026-09-19 17:1x PT). **Arch
enumerated the 6 consumer sites before Lead builds** (same discipline as enumerating a deleted
write's readers, per Arch's own #1810/#1814 lesson): `is_designated_operator` itself,
both `resolve_user_llm_key`/`resolve_user_openai_key` ladder injections, the env-var gate + its
truthy read, gate-1's re-check + the explicit binding path, and — flagged hardest — the ladder's
third rung returning bare `None`, which currently *means* "use the server key." If the seam retires
but that rung stays reachable, `None` becomes a value with no defined meaning — the same
honest-empty shape as `#1816`/`#1815` Gap 2/`#1829`. Preferred disposition (Arch's, Lead's to
build): the rung goes away entirely rather than surviving with a permanently-False checker. **Also
dissolves a caveat on my own #1823 ruling**: Lead's #1823 trace conditioned "selection's candidate
set is the binding" on "on a BYOC deployment" (because the server could still hold keys via this
seam); once step 5 lands, the server holds no keys on any deployment, so that clause drops and the
conclusion gets simpler, not different. Not re-opening #1823 for this — noting so a future reader
doesn't find a dead qualifier and wonder if it's still load-bearing.

**`#1812` CLOSED 2026-09-21** — built and verified, per the issue's own closing evidence: *"the
server key is not a real concept — now structurally, not just by ruling."* Steps 5-6 (retire the
transitional operator seam) shipped. Found during Lead's own Phase B verification pass: two new
pre-existing (not regressions) test-infra issues, `#1841`/`#1842`, board-fixed same morning
(milestone `Production`, matching the `#1372`/`#1356`/`#1506` precedent for incidentally-discovered
test-suite defects) — not epic 2's concern, tracked on the board only.

**Slack sponsorship question RETIRED 2026-09-19** — PM ruled linked-account-only is the model; the
already-live lazy-refuse default is the ruling. No code change, no issue to track — a design
question resolved, not a build item.

**~~`#1838`~~ folded 2026-09-20, from PM's first dogfood session on alpha (CLOSED 2026-09-24)**: after the keyless first-turn
key ask (PM's own word: "nicely" worded — this part working), PM added a key in Settings, and the
just-started chat could not be found again on return. Session-continuity break at the exact seam
this epic already owns end-to-end (the key-add/onboarding path) — the issue's own filing left the
epic call to PPM, placed here rather than the composer catch-all given the overlap with `#1807`/
`#1809`/`#1812`/`#1818`'s shared flow. Mechanism undiagnosed — needs a driven repro (keyless start →
refusal → Settings → add key → return), not yet assigned.

**Four more, from the 2026-09-15 sequencing follow-on — all CLOSED same day except the trigger**:
~~`#1814`~~ (v109 — `#1810`'s fix removed a key-write before verifying the reader could resolve a
per-user key at all, walking the invite's own onboarding condition into a false "not configured"
wall) · ~~`#1815`~~ (two residuals from closing `#1814`: cross-provider fallback loop, and Gap 2 —
a consent fail-closed branch ruled together with `#1816`) · ~~`#1816`~~ (a consent boundary failed
OPEN — `KeychainService.get_api_key`'s broad exception swallow meant a real keyring failure fell
through to "everything authorized"; fixed at the consent reader, v111, shipped with CXO's own
proposed copy ahead of formal ratification, confirmed with one clause cut same-fire) · `#1817`
(open — the invalidation-trigger issue Arch's `#1816` ruling required in §4: consent-from-key-
presence stays a *dated assumption*, not a design, until a de-authorize surface exists; this issue
is that surface's tripwire, not a bug).

⚠️ **REOPENED 2026-09-14, not a successor epic** — see the change log entry below for the full
account. Epic 2 was closed 2026-09-12 for six items; it was not actually complete, and the tenancy
family that surfaced two days later is the same epic, not a new one. PM's own words: *"if we
discover that there's more work on an epic than we realized and we closed it before discovering
that work, then yes we need to reopen the epic... the truth is more important than the feeling of
progress."*

**Sequencing on the open two**: `#1810` (closed, observation confirmed — see below) → `#1809` →
`#1791`, per Lead and Arch — each is the same "a credential/preference is never resolved by
absence of binding" principle one layer down, not three separate calls. `#1809` is gated on CXO's
"no key configured at all" copy (the existing error table has no pattern for that state), which
Lead asked CXO to draft ahead of need. Arch owns whether `#1791` forks the ADR-075 overlay or
takes another shape — neither is PPM's call; this epic's job is giving them a home, not a design.

**`#1810`'s clearing condition actually met, same night** — a worked example of the cohort's own
discipline holding under real stakes. Arch's ratified condition required an *observed* setup flow,
not a merged fix; Exec correctly declined to call a test pin sufficient; HOST held the line when
Arch briefly tried to substitute an onboarding mitigation for the bar Arch had set three hours
earlier (and Arch conceded this directly: *"the person who sets a bar is the worst-placed person
to decide it can be skipped this once"*). Lead then supplied the actual observation — a read-only
production check (global key slots absent) paired with a full setup-flow run against deployed code
on a prod-matching backend (per-user keys present, no global entry, 5 rows all user_id-prefixed) —
and named its own limit honestly (local server against a prod-matching backend, not a literal
production signup). Arch ruled the bar met. HOST verified independently before lifting and updated
the roster; Janne's invite is ready, with one onboarding condition (configure key first) as
defense-in-depth against `#1809`, which stays open. **CXO caught one loose sentence in the
close-out** ("CXO's rider is satisfied by the same run") and corrected it same-night — the rider
was about an unobserved FTUX copy claim, not the setup flow, and CXO's own re-check found the
rider had been mis-specified from the start (it needed a real prod account, which nobody has
created); that claim stays open, unrelated to `#1810`'s own closure.

**`#1814`, found by the very observation CXO's correction demanded — the invite re-held within
hours of being lifted**: `#1809`'s own sequencing (`#1810`→`#1809`→`#1791`) removed the global-key
write before verifying the resolver could read a per-user key at all — `get_api_key()` takes no
user parameter and never consults `UserAPIKeyService`. So a BYOC user's own stored key was never
used; the invite's own onboarding condition (configure your key first) walked Janne straight into
a false "not configured" wall. Lead, Arch, and Exec each independently named their own piece of
the sequencing gap before being asked — Arch's rule for the record: *"deleting a write requires
demonstrating that every reader of that slot has another source FIRST,"* not just that readers
still resolve without erroring. HOST re-held immediately on waking to it, verified independently
again, and required the sharper bar this time (an actual BYOC query succeeding on a stored key, not
just an empty-slot check). **Fixed and confirmed the same night** — deployed v109, observed via a
real turn hitting the network (a 401 from a throwaway key, proving resolution actually happened,
not just that a test passed) — invite blocker gone. Two residuals filed as `#1815` (cross-provider
fallback loop still gates on the server's own client; a consent fail-closed branch can reproduce
the same symptom from a different cause) — both MVP-milestoned, folded in here. CXO separately
found `#1814` exposes a conflation in the keyless-refusal copy written the day before (a failed key
lookup and a verified-absent key produce the same exception, so the copy can only assert the
stronger claim) — not live today, latent pending whether the resolver can even distinguish the two
states.

**Invite lifted again same morning** — HOST verified independently (`gh issue view 1814` →
CLOSED, Lead's 401-over-the-network evidence meets the bar) — and, in the same pass, checked
`#1816` (below) directly against Janne's own path before treating it as unrelated: it doesn't
touch him today, tracked not gated.

**`#1816`, found while investigating #1815's Gap 2 — a consent boundary fails OPEN, not closed**:
Lead inverted a premise from their own brief — `KeychainService.get_api_key` swallows exceptions
broadly and returns `None`, so a real keyring failure never reaches the fail-closed branch; control
falls through to "everything authorized." **The durable shape, Arch confirmed as a live instance of
the honest-empty family one layer down**: `None` means "try the next source" for a *credential*
read (correct, #1711's reasoning) but "no restriction" for a *consent* read (wrong) — the same
return type inverts meaning depending on who's asking, same defect class as `verified_empty` vs
`source_failed` collapsing into one falsy value. **Arch's ruling, four parts**: (1) fix belongs at
the consent reader, never the credential primitive — a tri-state read, not a change to `#1711`'s
sound contract; (2) the root shape is added to `#1816` as stated fact, not a new methodology entry;
(3) `#1815`'s Gap 2 (the latent over-restrictive half, deliberately left undecided until now)
rules together with `#1816` — a consent-read failure must *refuse the turn*, not degrade to the
server key, since PM's own `#1812` ruling already abolished that concept; (4) inferring consent
from key presence stays acceptable today only because no de-authorize surface exists — dated
explicitly as a **dated assumption, not a design**, with the first de-authorize surface named as
its own invalidation trigger. **CXO caught a build-time defect in the ruling's own copy line**
before anyone wrote code to it: "CXO's copy work already covers the user-visible state" is false —
existing copy tells a consent-read-failure user to add a key they already have, the same
absence-vs-failure conflation CXO reported hours earlier on a different call site. Proposed the
correct string (reports a failed read, names whose fault it is, and — uniquely in this family —
permits "try again" since a store hiccup is genuinely transient). Gap 1 (BYOC key as fallback
provider, not just primary) is fixed and deployed, v110.

**Live, unfiled finding**: CXO found the *existing* out-of-quota recovery copy now routes a tester
into a worse state (tells them to remove their key to "fall back to the built-in model," a
fallback `#1807` already removed for non-operators) — reachable today, not gated behind `#1809`.
Not yet its own issue as of 2026-09-14 evening.

**2026-09-15 evening — the keyless-refusal conflation (flagged above, "latent pending") resolved
to a four-bucket split, no issue filed yet.** Arch's hypothesis that `#1814` was caused by the
`"not initialized"` auth bucket was refuted by Lead against the actual transcript (`#1814` routed
through `no_provider`, before the auth list is ever reached) — Arch accepted the refutation in
full and, more importantly, corrected the rationale rather than just the fact: **`"not
initialized"` still earns its own bucket by the split criterion (the honest sentence differs), but
as a *latent* member, never observed firing — not "the cause of #1814."** A true conclusion
resting on a wrong reason was the thing worth catching, not the wrongness itself. Four buckets
stand; CXO's per-bucket copy has no arch objection. Separately, CXO scored the actual FTUX
transcripts against this morning's pre-registration and found two *live* copy defects source-
reading couldn't have caught: the keyless-refusal string says *"I can't run **this** without an
LLM key"* but fires identically ahead of a bare greeting, which needs no key at all (Case 1 proves
the greeting handler is deterministic) — same one-string-spans-differing-truth-conditions shape as
the auth-bucket rule, this time by request type not error cause; and the "running with a default
configuration" notice fires right after a user successfully sets their own provider and key,
asserting something about a store the user can't see and reads as contradicting what they just
did. Also resolved a genuine 8-day-old CXO tracker gap: the FTUX interview flag is OFF in what a
real `main` deploy carries **by a PPM 2026-09-03 HOLD ruling**, not unverified as CXO's tracker had
said since 09-07 — worth noting since it's this file's own prior ruling being the answer, not new
information. **No PPM ruling needed anywhere in this thread** — split criterion, copy fixes, and
flag-state bookkeeping are Lead/Arch/CXO's own domain.

**~~`#1824`~~ — the four-bucket split above, now filed** (Arch, 2026-09-18, after the
classifier-split
thread lived only in mailbox memos through a session renewal — **CLOSED 2026-09-21, see below**,
never struck through here). Confirms the shape verbatim against
source (`conversational_floor.py:660-682` collapses five distinct causes into one `"auth"` return,
two of them with comments admitting they aren't auth) and carries the same self-correction as the
mail thread: **explicitly warns future readers not to cite `#1814` as the reason for the split** —
`"not initialized"` earns its own bucket by the criterion alone, and citing an incident it didn't
cause would be a true conclusion resting on a wrong reason. Found missing from board/milestone at
this fire despite the standing filing convention; fixed same-fire (MVP, board-added, Status=Product
Backlog).

**Two more from today's BYOC/Slack-key-binding family** (both surfaced by `#1819`, prog,
2026-09-18): ~~`#1822`~~ — Slack inbound only binds the sender's Anthropic key, not the fuller
provider-keyed mapping `#1819` gave the web routes; a residue, not a new defect class. ~~`#1823`~~ — a
genuine product decision, not a bug: should one stored LLM key of *any* provider be enough to pass
`/intent`'s refusal rung, or does the rung stay Anthropic-specific? Explicitly filed as a decision
for PM/product, not something Lead can resolve in code. Both already correctly milestoned/boarded
at filing (the convention held); folded in here for epic-2 continuity. **Both CLOSED, caught
2026-09-26 by a reconciliation pass — not previously marked.**

**`#1823` RULED 2026-09-19 — gate on any spendable provider key, accepting Arch's recommendation
in full.** Arch's finding made this cheap: `resolve_request_api_key`'s ladder never knew what a
provider was — the Anthropic constraint was injected at the call site (`web/utils/llm_key.py`), not
structural — so the ruling needs no restructuring, just a different injection plus constraining
provider selection to the providers actually bound (not "accept any key, refuse later at route
time"). Zero-key refusal is unchanged; fail-closed at the true boundary holds. Where a task type is
genuinely Anthropic-tuned, refuse — but name the task type, not the vendor, held as part of the
ruling per Arch's condition. CXO's copy ships as drafted (the "any spendable provider" branch),
which also resolves a defect CXO found independent of this ruling: the existing refusal
self-contradicted (an ownership claim followed by a vendor name) and diverged from
`conversational_floor.py:610`'s already-neutral convention — no separate issue needed, this
ruling's copy fixes both.

⚠️ **Sequencing, recorded here so it's visible before either lands**: `#1824`'s four-bucket
classifier split lands first, or together with `#1823`, not after — an honest task-type refusal
needs a bucket to live in, and shipping `#1823` first would invent a fifth bucket informally.

**One precondition on implementation, Lead's to trace, not assumed either way**: whether provider
selection (`#1415`) actually consults the binding to constrain routing, or selects first and looks
up the key after. That ordering is the hinge between "ships as designed" and "a user can pass the
gate and still fail at route time" (a third state CXO flagged, distinct from both existing states).

**Precondition DISCHARGED 2026-09-19 (Lead's trace)** — selection does consult the binding,
structurally, not incidentally. The third state is unreachable at the selection/spend layer once
the gate change itself lands (the binding-expansion fix IS the gate change, not a separate defect
— Slack/`#1822` already demonstrates the target shape live). No new string owed for it.

**Branch two RULED OUT OF SCOPE 2026-09-19** — CXO traced whether any task type is currently
Anthropic-tuned (the condition branch two's task-type-naming copy depends on) and found `resolve_model`
is total by construction: task type selects a *tier* inside whichever provider selection already
picked, never a provider itself. 8/8 task types resolve for all 3/3 providers, no failing path.
Verified independently this fire: `config.py:74` states the design intent in source — *"Task
configurations — provider-agnostic."* **Branch two's antecedent is false today, and the
architecture reads as deliberately, not incidentally, provider-agnostic** — so writing the
task-type-refusal copy now would invent a distinction the code declines to make (the same
`"not initialized"` shape Arch's own memo warned against). **Ruling: no work item for branch two.**
CXO's reworded string is deposited (not shipped) with its licence stated inline in their memo — if
a future task type ever becomes genuinely provider-constrained, that's the string to use, owned by
whoever adds that constraint, not a thing to build speculatively now. This is scope correctly
narrowing to match verified reality, not discovered work being deferred — no successor issue.

**#1823 is now fully scoped: branch one only** (gate on any spendable provider key + CXO's neutral
copy, which also fixes the self-contradiction/`:610`-divergence CXO found independently). Lead is
holding implementation for next week's plan per the standing weekend framing (paired with `#1824`'s
sequencing, unless PM pulls it forward) — not a PPM action item, noted for continuity.

**~~`#1818`~~ — BOTH HALVES NOW RULED 2026-09-19, build-ready** (**CLOSED 2026-09-21, see below**,
never struck through here). Experience half: CXO ruled let the
greeting pass but it must carry key-state in the same breath, "both halves or neither." **Arch
ruled the structural half same evening: property, not list** — the property already exists
(`ActionDisposition.CANONICAL`, `action_registry.py:17-38`, greeting already registered, enforced
by a startup validator), so this needs no new mechanism, just declining to duplicate one (ESSENCE's
"derive, don't hand-maintain" rule, already in force). **The real work Arch surfaced that neither
the issue nor CXO's ruling named**: the keyless gate fires *before* `process_intent` even runs the
pre-classifier that determines disposition — so "let the greeting through" can't be bolted onto the
existing gate; the pre-classifier (regex-only, no LLM call, verified) has to run *before* the gate
and the gate condition becomes a disposition lookup, not a message-content list. Wants a same-PR
ratchet asserting every `CANONICAL` pair is keyless-reachable and every other pair isn't. **One
unverified hinge, named rather than assumed**: whether any `CANONICAL` path can still reach an LLM
call downstream (fallback/enrichment/floor-handoff) — if so, `CANONICAL` alone isn't sufficient and
CXO's copy would be wrong (promising "spends nothing" while it might). Lead's to trace before the
gate moves, same shape as the #1823 precondition. **CXO delivered the greeting-state copy** (issue
comment 5747829604) contingent on that hinge clearing, and separately caught their own citation was
one layer off (the `due_reminders` floor-directive shape doesn't apply — greetings are `CANONICAL`
and never reach the floor — so this ships as fixed text, not a model-composed directive).

**CORRECTION 2026-09-20 — Arch's structural ruling above was WRONG and would have opened a keyless
path to issue creation and DB writes.** Caught before Lead's ratchet built, not after. Tracing
~~`#1773`~~ (**CLOSED 2026-09-24**), Arch finally opened the live routing authority (`_requires_canonical_handler`) rather than
reasoning from the `CANONICAL` disposition name and a registry comment — and found `CANONICAL`
means *"the LLM cannot do this on its own,"* not *"costs no LLM call."* `EXECUTION` and `PORTFOLIO`
are canonical precisely **because** they write to the database and create issues — the most
consequential actions in the product, not the cheapest. **The corrected ruling**: the
spends-nothing property does not exist yet and must be created new — not `ActionDisposition`, not
`_requires_canonical_handler`, neither of which was ever a cost claim — defaulting to `False`
(fail-closed: a handler is exempt only if deliberately marked *and* the ratchet proves it). The
pre-classify-before-gate ordering cure survives unchanged. **The ratchet Lead was about to build
against the wrong predicate now becomes the actual definition of the spends-nothing set**: the
pairs that survive a keyless drive with `LLMClient.complete` rigged to explode *are* the set: this
is the honest-empty family's fifth instance in eight days (#1816, #1815 Gap 2, #1829, #1773, now
this) — Arch's own rule (*"a grep line-hit is not a read"*) failed one level up this time (*"a name
is not a definition"* — reasoning from the word "canonical" rather than the authority it's supposed
to describe). Corrected inline at the issue comment and decisions.log, not appended.

**CXO found a further, separate problem in the same fire, orthogonal to Arch's fix**: even under
the corrected design, the resulting keyless-exempt set is **incoherent to a user** — `"hi"` passes
(greeting has a branch), but `"Hi, how do I address you?"` and `"thanks"`/`"bye"` are refused
(compound-greeting falls to floor which spends; `farewell`/`thanks` are registered `CANONICAL` but
have no branch in the routing authority at all — `#1773`'s drift, now confirmed at the specific
pairs). The more natural, more human opener gets refused and the terser one doesn't. Not a design
flaw in Arch's fix — a UX consistency pass CXO is claiming once the ratchet's actual output exists
("copy for a set nobody has measured is copy for a mechanism that doesn't exist," same reasoning as
`#1823` branch two). Also flagged as unverified rather than assumed: `#1818`'s own filing claims a
greeting "spends nothing," but the routing authority's stated reason for greeting being canonical is
side effects (onboarding/calendar), not cost — the ratchet answers this, it shouldn't be listed as
a settled premise.

**Not a PPM ruling on any of this** — structural and experience halves both corrected/extended
today by their own owners; Lead's ratchet is now the load-bearing instrument, CXO does an experience
pass on its output once it exists. Watching, not chasing.

**Arch escalated CXO's raggedness finding one level further, same fire**: accepted the finding
without qualification, then asked whether the whole approach is at the wrong layer — if the exempt
set is ragged because the boundary is invisible to users (a user models "pleasantries," not
dispositions), the durable fix may not be a better boundary but making the boundary stop mattering:
a refusal that itself greets, uniformly, for every first-contact message, rather than exempting some
and refusing others. Explicitly **not** overturning PM's direction — routed as a genuine open
question for PM: does "don't challenge for a key on a first hello" mean (a) the greeting must be
gate-free (current #1818 design, ragged by CXO's measurement) or (b) first contact must not *feel*
like a challenge (satisfied by a uniform greeting-refusal, less machinery, no ragged set)? Arch's own
read favors (b) but named it as PM's call, not theirs.

**`#1818` RULED 2026-09-20 — PM picked (b).** *decisions.log 13:3x*. No spends-nothing exemption at
the gate, no new predicate or marker: every keyless first message gets a warm response that
acknowledges in kind (CXO's refinement to literal (b), which failed one case on inspection —
answering `"bye"` with a greeting reads as not having understood, not as policy — fixed by matching
the response type to the pre-classified pleasantry: greet a greeting, farewell a farewell,
you're-welcome a thanks, all ending in the same key explanation) and explains the key requirement in
the same breath. CXO owns the four-string copy set (shared text for the shared half, per the same
discipline as `#1823`'s family). Lead owns the ordering + kind-matched dispatch wiring. **The
ratchet stays as the definition + regression guard**, not gate plumbing — and its first live run
measured the hinge decisively: **only 5 of 14 registry-`CANONICAL` pairs are actually spend-free**
(`greeting`, `get_current_time`, `manage_portfolio`, `manage_repos`, `explain_suggestion`); the
other 9 — including `thanks` and `farewell`, which route to the floor and get LLM-composed — bill.
`#1773`'s registry-vs-runtime drift is now confirmed with billing evidence, decoupled from `#1818`
but strengthened as its own fix (a deterministic thanks/farewell would get promoted by the ratchet's
own improvement-side check). **Not a PPM ruling — PM's, fully implemented in design, build now
straightforward.**

**CXO delivered the copy set 2026-09-20, Lead unblocked**: one shared constant (the key-explanation
sentence, literally shared in source, not pasted four times — same discipline as `#1823`'s family)
prefixed by a kind-matched acknowledgment (greeting/farewell/thanks/neutral); `thanks` deliberately
does NOT say "you're welcome" since nothing was done yet (the honest-empty family showing up inside
a pleasantry).

**(2) RESOLVED by Arch, same day**: yes, (b) supersedes `#1823`'s branch-one string, but only on the
first-contact path — a keyless greeting never reaches the gate at all under (b) (handled canonically,
pre-classified, before `resolve_request_api_key` is consulted), so there's no double-answer risk
there by construction. **The sharper part of Arch's answer also settles (1)**: CXO's repeat-turn
short form is for *repeated pleasantries* only (a second `hi`/`thanks`), staying on the
canonical/keyless-copy path — the moment a keyless user's message is a genuine substantive request
(turn 2+ or otherwise), `#1823`'s gate and its string fire unchanged, because that's a real attempted
spend, not a courtesy reminder. This preserves CXO's own "one policy, one string per layer" property:
the canonical path never answers "what do I need to do real work," the gate never handles
pleasantries. **Both decisions now resolved — build is Lead's, no PPM action either way.**

**`#1818` CLOSED 2026-09-21** — "(b) implemented with evidence above." **`#1823` CLOSED 2026-09-21**
(`9ec028406` on `origin/main`) — branch one shipped: the gate now matches the spend
(`resolve_user_llm_binding`: header/stored-Anthropic → unchanged; no Anthropic but a stored OpenAI
key → bound alone, mirroring `#1822`'s Slack arm; neither → CXO's ruled provider-neutral refusal
copy). **`#1824` CLOSED 2026-09-21**, same commit — the four-bucket classifier split shipped:
`_classify_llm_error` now discriminates `rejected_credential`/`insufficient_permission`/
`not_configured`/`config_endpoint`, `return "auth"` no longer exists in the function, pinned by
test. **One new issue surfaced during the `#1837` shape-3 build** (Lead, found by a regression test
phrasing an edit request politely): `#1843` — `soft_invocation.py`'s `ACCEPT_PATTERNS` row 2 fires
on any short message starting "please," so *"please remove the fluff"* finalizes a standup draft
instead of editing it. Found missing milestone/board at filing — fixed same-fire (MVP, board-added,
Status Product Backlog).

**~~`#1845`~~ folded in 2026-09-21 — bearer credentials traveling through `mailboxes/`, a PUBLIC
repo. CLOSED 2026-09-24** (generalized and superseded by `#1885` below, which found more of the
same class via a new mechanized gate).
Lead found Janne's invite code appearing in full across at least 4 mailbox memos since 09-13 (a
single-use, first-consumer-wins account-creation credential, this repo confirmed PUBLIC via
`gh repo view`), plus a second stacked defect: the code was minted against the wrong instance (Fly,
not alpha's droplet) — the invite would have bounced at the gate on send day regardless of the
exposure. **Already remediated same-fire, not just found**: Lead confirmed the exposed code was
never consumed on either instance (no unauthorized account), minted a fresh replacement on the
correct instance, delivered PM in-conversation only. One residual: the exposed Fly-side row still
needs burning (a DB delete only PM or a Fly-write-granted seat can run — Lead's own droplet SSH
grant doesn't extend to Fly). **Standing rule proposed, PM to ratify**: bearer credentials never
travel through `mailboxes/` or any repo-committed surface — this seat's own mail-send discipline
(explicit paths, per-memo commits) has never carried a credential, but the rule needs to be explicit
rather than incidental. Milestoned MVP (same family as `#1816`'s consent-boundary precedent — a
security defect found during real operational work on the current alpha rollout, not a pre-launch
gate item). Not a PPM ruling on the standing-rule proposal — PM's to ratify.

**`#1885` folded in 2026-09-24 — the standing-rule proposal above earned a backstop, and the
backstop immediately found more.** `scripts/mailbox_bearer_lint.py` (the `#1845` backstop),
run for the first time over `mailboxes/`/`docs/`/`dev/` (not just memos), found three more LIVE
unused invite tokens in full form in tracked session logs + an omnibus log, plus a Google API key
and an old Slack bot token in dated logs. **Already remediated on `main`**: every full form
replaced by its masked form across 30 tracked files, the gate wired into Code Quality CI with a
baselined placeholder allowlist and a negative-check plant. **Needs PM's hand, already mailed
directly** (Lead → HOST, cc PM/Exec, `urgent-...-1885-...md`, HOST acked same day) — burning the
three unused prod rows, minting replacements, and confirming the Google/Slack key rotations; Lead's
remote DB write was denied by the permission classifier, correctly not worked around. **Resolves
this seat's own long-carried "ALSO WATCH — #1845" item** (the single exposed Fly-side row) by
generalizing it — that one row is now three, caught by a mechanized gate instead of a manual find.

**Two more folded 2026-09-22, both found during today's live Fly cutover** — same operational-
security family, both already correctly disposed, not just discovered. ~~`#1851`~~ (**CLOSED
2026-09-24**) — the droplet's
Redis listened on `0.0.0.0:6379` (publicly reachable), keyspace carried the classic exploit-attempt
fingerprint (`backup1`-`backup4` junk keys) — password auth held throughout (`NOAUTH` on
unauthenticated access), no compromise, `DBSIZE=5`. Disposition: no droplet-side fix (decommissions
in ~1 week) — the live action is verifying Fly's Redis is private-only (flycast/internal, no public
bind) before this class can travel to the new primary, already cutover step 10. `#1852` — Slack/
Google OAuth redirect URIs on the Fly app still point at the pre-cutover host
(`piper-morgan.fly.dev`), deliberately left because fixing them requires provider-console callback
updates (Slack/Google developer consoles), not just a secrets change. Consequence: a tester starting
a Slack/Google connect flow from `alpha.pipermorgan.ai` would land on the wrong host mid-flow — not
a launch blocker (no alpha tester uses these integrations yet), should land before any tester is
pointed at either connector.

**Found 2026-09-23 by this seat's own third-queue-source criteria line — pre-existing gap, not
from today's dogfood session**: `#1632` (filed 2026-08-15) — the `#1462` capability-legibility
tool catalog doesn't expose the `#1509` outwardness classification (PRIVATE/OUTWARD) now that every
WRITE/DESTRUCTIVE rail entry declares it; the catalog can't yet honestly state which actions land
in front of other people, the legibility half of the same consent story this epic tracks.

**`#1891` folded in 2026-09-24, `#1632`'s own lane found the actual source**: the floor's
`capability_manifest_block()` (`services/intent_service/conversational_floor.py`, ~479-513)
injects the raw list of all 137 wired action names into the system prompt on every floor turn —
explicitly "internal machinery, never recite verbatim" — and is the most plausible source of a
raw-action-name leak PM saw live. It carries no outwardness, and `CHAT_POINTERS` has no row for
any OUTWARD action — `#1632`'s own marker can't reach PM's reply until one of those changes. Same
consent-legibility family, one layer deeper (the leak mechanism, not just the missing catalog
field).

**Why here, non-negotiable**: this epic's position doesn't move for scheduling convenience even
half-closed — and per 2026-09-14, "closed" isn't a substitute for "actually complete" either.

**Two findings folded in 2026-09-10, both surfaced fixing `#1732`**: `#1741` pattern-suggestions
UI interpolates unescaped into innerHTML, outside `#1732`'s chokepoint · `#1740` twin-file
renderer drift (a dead unserved copy diverged from the live one).

⚠️ **Caution, not an alarm**: `#1637`/`#1732`/`#1734` closed Sprint Backlog → Done directly,
skipping In Progress (Exec's 09-10 finding — the board's In Progress count is not a reliable
in-flight signal). **General note, now proven twice**: closed issues can be missing from the
project board entirely, same drift shape as the open-issue version (`#1772`/`#1785`) — found on
`#1807` this week while it was already closed. Worth checking board presence on any closure, not
just at filing time.

### 3. Acceptance contract (15 items, 12 closed) — freshest pain, design is DONE, unblocks a whole cluster
~~`#1739`~~ (umbrella — CLOSED 2026-09-24, verified directly) · ~~`#1663`~~ · ~~`#1652`~~ · ~~`#1653`~~ · ~~`#1654`~~ · ~~`#1694`~~ ·
~~`#1696`~~ · ~~`#1596`~~ (all six **CLOSED**, per Lead's session log — the epic ran to its floor
Saturday) · ~~`#1752`~~
(found 2026-09-12 during #1654's own adoption — the soft-workflow-offer no-clobber guard doesn't
cover the STATE_QUESTION-survival re-arm path, a silent-drop shape adjacent to #1652's arm half;
**turned out to be an accidental duplicate of the already-fixed #1753 — closed, net zero change
here**) · `#1771` (found 2026-09-12 during #1769's adoption, the sixth contract adoption — the
shared decline vocabulary folds "maybe later"-class deferrals into DECLINE, which is harmless at
most seams but abandons the resumable flow at the resume-offer seam) · ~~`#1695`~~ (moved here from
Singletons 2026-09-12 — compose-framed draft can arm a subject still carrying the bare repo phrase
because the collaborate-gate ARM path doesn't resolve it, only the execute/file path does; same
arm/consume-rail family as the rest of this epic). **CLOSED 2026-09-24.** **`#1739` (the umbrella)
is ALSO now closed** — checked directly, not assumed from the old "closes when its children do"
description. **`#1771` is verified still OPEN** — checked directly. Not reconciling why the
umbrella closed ahead of a stated remaining dependency here; flagging the discrepancy rather than
guessing at it. Stale "remaining open" accounting from 09-13 removed.

**`#1617`'s retest attempted 2026-09-20 — NOT REACHED, and the reason is now this epic's own
blocker.** PM drove a real standup on alpha and the flow broke upstream of the tail: `#1837` — the
guided-interview offer, once accepted ("Sure, thanks."), never arms the interview (~~`#1651`~~/`#1652`
acceptance-contract-rail machinery, this epic's own family — `#1651` **CLOSED 2026-09-24**, though
never separately tracked in this epic's item count above) — instead falls through to a generic
fabricated template, and a later turn has Piper deny having made the offer at all (a conversation-
state contradiction, since the offer history isn't consulted). **`#1739`'s dependency chain updates:
`#1617`'s retest now depends on `#1837` landing first**, not the other way around. Lead's proposed
shape: extend the acceptance-contract rail so offer-acceptance actually arms the interview, and give
the restate branch access to its own offer history. **Shared with epic 5** (below) for the
fabricated-template half of the same issue. **Arch CONCURRED on all three of Lead's proposed shapes,
same fire, each independently verified at source (not a rubber stamp)**: (1) kill the fabricating
fallback, checked zero external callers before endorsing deletion; (2) arm-on-acceptance lands on
the existing acceptance-contract rail (Lead's #4, the restate branch lacking offer-history access,
confirmed as the sharper bug — it's structurally blind, not just poorly worded); (3) refinement
moves to the floor, `#1836`'s shipped fix correctly orthogonal either way. **Sequencing: (2) first**
— it's the shape blocking epic 3's own floor per the dependency-chain update above. **Build is
Lead's now** — no PPM or further Arch action pending.

**CXO checked `#1837` against the acceptance contract directly, same day — first live transcript the
contract has ever been tested against.** Turn 4 (Piper denying its own offer) is already covered by
the contract's §3 (question-forms request state, answer truthfully) — a violation of an existing
clause, not a gap. **Turn 2 exposed a real gap CXO is amending the contract to cover**: PM's
acceptance ("Sure, thanks.") wasn't ambiguous and still cost an action — it was silently captured by
an unrelated flow (greeting/mode-fork) rather than falling through to either of §5b's two enumerated
cases. Named as a third, worse case: invisible at the moment it happens (the user believes they're in
the flow they accepted; the divergence only surfaces turns later as a contradiction), unlike the
existing "say so plainly" case which is visible immediately. New rule CXO is adding: *"An acceptance
must bind to the offer it answers, or to nothing. It must never bind to a different flow."* CXO
confirmed turn 3 (the fabricated generic standup) stays correctly outside this contract, homed to
`#1836`/epic 5 as already tracked here — not annexing it. No PPM action needed; Lead's existing
acceptance criteria on `#1837` already cover the fix.

**`#1837` CLOSED 2026-09-21 — "all three shapes landed with evidence above."** This epic's own
blocker (the `#1617` retest couldn't be reached without it) is cleared. **`#1739`'s dependency chain
reverts to its original shape** — `#1617`'s standup retest is once again the umbrella's last real
dependency, now actually reachable. Not re-running the retest myself; noting it's unblocked, not
verifying it passed. **~~`#1617`~~ subsequently CLOSED** (caught 2026-09-26 by a reconciliation
pass — not previously marked; the retest referenced above did eventually land, just never recorded
here).

**Why third**: PM's live round converged three failures onto this one contract today. Both design
passes are already in (Arch's sequencing ruling + CXO's two-axis correction, conceded by Arch) —
Lead builds against a finished spec, not an open question. Closing this epic unblocks the
reminder/standup UX cluster wholesale, per Arch's read.

**Spec address (2026-09-10)**: the user-facing contract consolidated from three separate memos
into one doc — `docs/internal/design/acceptance-contract-user-facing-2026-09-10.md`. Includes
CXO's arm-survival ruling (consent has a freshness property a draft offer doesn't; per-tier
survival policy feeds the DESTRUCTIVE-tier design). Cite that doc going forward, not the mail
thread.

**Folded 2026-09-22, backlog catch-up**: `#1783` — the contract's axis (a) treats an interrogative
REQUEST as a state question (*"can I get an update?"* misread as *"are we done?"*), the same
question-form-vs-speech-act distinction CXO's turn-4 ruling on `#1837` (epic 5) relied on — a
sibling defect in this contract's own family, not yet built.

**Folded 2026-09-23, from PM's live Test-1 dogfood session on alpha**: ~~`#1855`~~ — self-identifies
as "the exact seam `#1837` closed for the standup interview offer, still open in the GENERAL case,"
generalizing the turn-2 gap CXO's new rule above already covers ("an acceptance must bind to the
offer it answers, or to nothing") to acceptance flows beyond the standup interview specifically.
Same contract, same rule, not yet applied outside the one instance it was written against.

**Design + ruling landed same day, 2026-09-23 — ready to build.** Lead's design
(`docs/internal/design/design-1855-armed-floor-offers-2026-09-23.md`): a narrow output-seam
rewrite (unarmed offer-questions → imperative suggestions, logged to the `#1595` corpus sink) as
layer 1, plus deleting the never-built `LastOffer.offer_type="actionable"` reservation (one
authority for "is anything armed," not two stores that can drift). **CXO ratified the contract
sentence** ("the floor may SUGGEST in the imperative, but may only ASK when X is armed this turn")
and named it `#1837`'s mirror — `#1837` was the binding silently wrong, `#1855` is the offer itself
being the lie, same underlying rule from both ends. **Arch approved layer 1 as designed and ruled
DELETE (not build) on the `actionable` reservation**, verified genuinely never-instantiated
(`grep -rn '"actionable"' services/` — one hit, the dead comment itself). Layer 2 (real arming via
`#1856`'s extractor) explicitly NOT ruled today — a build-out once layer 1 proves out, not a fresh
question.

**Layer 1 SHIPPED same day, 2026-09-23 — on `origin/main`.** Seam:
`ConversationalFloor.respond()` (the single point all four floor doors pass, runs last so the whole
reply is covered), new `services/intent_service/unarmed_offer.py`. Armed = the `#846` `WorkflowOffer`
store or `LastOffer`, peeked; unproven arm treated as unarmed (fail-safe — a question becomes a
suggestion, never misfires). Rewrite prefers a bound command round-tripped through `#1856`'s real
extractor, else a bracket template, else a generic "tell me directly" fallback — never a bare
deletion; logged `floor_unarmed_offer_rewritten` for the `#1595` corpus lane. `actionable`
reservation deleted, pinned by a test that greps for it. **Fifth opener added same day**: Lead
flagged "Do you want me to…?" as the likeliest LLM-neighbour phrasing left uncovered rather than
silently patching it in; Arch ruled add it (the detector's own code already named the gap; the risk
of leaving a one-token phrasing hole is worse than the risk of adding it), CXO ratified (same speech
act as "Want me to X?", function-defined not surface-defined, same raggedness class as `#1818`).
Layer 2 (real arming) stays open on the issue — `revise_draft()` found as a second free-prose seam
that bypasses `respond()`, noted for whoever picks up layer 2. No PPM action — building/shipping is
Lead/Arch/CXO's own lane; recorded here so the file matches what's actually on `main`.

**Layer 2 designed and ruled same week, 2026-09-24 — ready to build.** Lead's design
(`docs/internal/design/design-1855-layer2-real-arming-2026-09-24.md`): the floor arms — and
therefore may ask honestly — exactly when tier 1 would have bound a command (catalogued family +
slots from the floor's sentence + the composed command round-trips through the real extractor);
anything less stays a suggestion, no guessing. `enforce_armed_offers` gains an *arm* outcome beside
pass/rewrite, arming a record in the `#846` store shaped for the existing confirm carrier
(`pending_action.kind="floor_bound_offer"`, composed command string as the binding, `ask_rendered=
True`); on accept, the carrier re-runs the command through the ordinary rail — no second
implementation of the action. `revise_draft()` gets the detector as a log-only guard, not arming.
**Arch approved both mechanism questions** (arming from the output seam is structurally the only
option; `floor_bound_offer` joins the existing confirm carrier rather than a dedicated workflow
entry — verified 5 non-destructive kinds already flow through the same carrier, so this is
precedent-following, not a new pattern). **CXO ratified normalizing the armed question to a house
form** rather than leaving the model's own paraphrase — grounded in the acceptance contract's own
quotability test (§3): the stored binding is the composed command string, so if the rendered
question is a paraphrase there's a live gap between what the user read and what's bound. The rule
is stated as a property (the rendered ask must state the same named parameters the command
composes from, reconstructable from the question alone), not a fixed template. No PPM action.

**Layer 2 SHIPPED same day, 2026-09-24 — `#1855` CLOSED.** Both rulings applied as designed: arms
from the output seam via the `#846` store, `floor_bound_offer` on the existing confirm carrier,
`revise_draft()` gets the detector as a log-only guard. The armed ask renders in CXO's house form
by default (*"Want me to add project X with repo Y? Say yes, or tell me otherwise."*) — the test
pins the property (command parameters appear verbatim in the rendered ask), not the exact string.
**Two deviations Lead flagged and got confirmed rather than deciding unilaterally**: (1) accepts at
the carrier's NAMED_OBJECT bar, not add-project's own WRITE×PRIVATE tier, specifically to avoid
`#1631`'s greedy-row vocabulary at the looser LOW_CEREMONY tier — temporary until `#1739`'s
vocabulary work tightens, Arch confirmed sound against `#1631`'s actual code. (2) accept re-runs
through `_process_intent_internal`, not the public `process_intent`, because the latter would write
the composed command into the transcript as a fabricated USER turn — Arch confirmed this is the
right catch, documented as a constraint on the catalogue type (only handlers executing from an
explicit imperative can arm this way). **One open question Lead flagged rather than assumed
settled, and Arch checked against existing law before ruling on it as new**: a floor-armed offer
can outlive one turn if a state question re-arms it with a "Still pending" restate — Arch found
this isn't a gap needing a bound, it's CXO's already-ratified arm-survival rule (2026-09-10, §5a/5b)
working exactly as designed: each restate re-renders the current stored command, so the user always
re-sees what they'd be confirming before any "yes" can bind — the staleness a TTL would prevent is
already structurally closed. PM's two-turn fixture verified end to end. No PPM action — recorded so
the file matches what actually shipped.

**Found 2026-09-23 by this seat's own third-queue-source criteria line — pre-existing gap, not
from today's dogfood session**: `#1623` (filed 2026-08-15) — the `#1529`/`#1617` family's third
face: an ACTIVE gathering flow (mid-interview) losing its turns to other claimers (a files-family
denial ate a plan answer; a temporal canned response ate a blocker answer), the inverse of
`#1617`'s completed-tail-release gap. Same flow-state/acceptance-rail family this epic already
tracks `#1617` under.

### 4. Corpus/classifier deposits (12 items, 8 closed) — gets its real turn after epics 0-3 finish or block
~~`#1505`~~ ~~`#1527`~~ `#1559` `#1579` `#1606` ~~`#1693`~~ (three closed, caught 2026-09-26 by a
reconciliation pass — not previously marked). **`#1606`'s scope corrected 2026-09-25, via
epic 0's unit-4 investigation**: Lead's own earlier premise ("arrives as two pre-classifier
intents") was wrong — checked live, `detect_multiple_intents` returns 0 and `pre_classify` claims
the whole two-part message as one `query/set_default_repo`; a real split would need a conjunction
regex, which the extraction ratchet forbids. Its real fix path is unit 4 of `#1595` (Inversion
Phase 2) — Arch ruled shape (ii): multi-intent turns bypass the orchestrator and run each sibling
sequentially through the existing rail, chosen specifically to avoid a second dispatch site. This
is materially larger design surface than the corpus-deposit framing above implies — not a quick
pattern fix, a structural unit of epic 0's own build. This seat owns the row (per Lead's memo);
tracked here, build is epic 0's. Plus, folded 2026-09-12 (same audit family,
found by agent lanes working these very items): ~~`#1755`~~ (multi-intent path suppresses a genuine
temporal ask when a connect ask rides the same message, found during #1505) · ~~`#1756`~~ (read-lane
pre-classifier patterns claim destructive delete asks, an #1527 sibling) · ~~`#1757`~~ (portfolio
archive/hide/restore patterns carry the same unguarded greedy capture #1527 fixed for delete,
another sibling). **Folded 2026-09-22, backlog catch-up**: ~~`#1758`~~ — todo priority extraction
matches `high`/`low`/`urgent` as bare substrings (*"add todo: high five to the team"* misreads
`high` as a priority marker), the same unguarded-substring-match family as `#1527`/`#1755`-`#1757`.
(`#1756`/`#1757`/`#1758` all **CLOSED, caught 2026-09-26 by a reconciliation pass — not previously
marked**.)

**Folded 2026-09-23, from PM's live Test-1 dogfood session on alpha**: ~~`#1857`~~ — project-name
extraction swallows the trailing word "project" (*"Add \<repo\> to the One Job project"* → lookup
fails on "one job project"; drop the article/noun and it works). Self-identified as `#1843`'s
family (interpretation-layer extraction greed) and explicitly gate-legal as a corpus row per the
supersession gate — `TestExtractionPatternRatchet`, not a new regex — matching this epic's own
ratchet-governed deposit mechanism. **CLOSED, caught 2026-09-25 by a reconciliation pass — not
previously marked.** · `#1860` — standup verb-initiation ("do a standup" / "let's do
a standup") matches nothing in `pre_classifier.py`, which carries only noun-phrase standup patterns
(`\bmy standup\b`, `\bdaily standup\b`, etc.) after a bare `\bstandup\b` pattern was deliberately
removed for a temporal false-positive; the verb-initiation family rides the LLM leg and produces no
dispatch. Self-identified in its own title as "corpus-deposit lane."

**Why here**: Arch's own note — these parallelize freely, cheap, ratchet-governed gate-side
deposits with no dependency on anything else in this list. ⚠️ **Corrected 2026-09-25** — the line
that used to stand here ("pulling one early is not a violation of 'one epic at a time'") was wrong
and has been removed. PM's restated sequencing rule has no exemptions: epic 4 gets its turn after
epics 0-3 finish or block, same as every other epic, full stop — independence-by-construction was
never a license to jump the queue, and this file shouldn't have implied it was.

### 5. Honest-empty / GatherOutcome (35 items, 30 closed) — lands after the acceptance-contract idiom proves out
~~`#1717`~~ (the audit's own meta-evidence for this cousin — **CLOSED**, scored 4/4 by CXO 09-12)
· ~~`#1730`~~ · ~~`#1736`~~ · ~~`#1738`~~ (shared with Deliverable below — all three **CLOSED**).
Plus, folded 2026-09-12: ~~`#1754`~~ (ConversationHandler clarify/chitchat lane unreachable,
independent same-day finding overlapping `#1759` — see that item's note — **CLOSED**, per Arch's
GO) · ~~`#1759`~~ (dead clarify-carrier machinery, found during #1730's own diagnosis — disposed
per Lead's #1730 Gap-2 proposal + Arch's same-day concurrence — **CLOSED/DELETED**) · ~~`#1760`~~
(test-theatre mock mismatch, found via #1736 — **CLOSED 2026-09-24**) · ~~`#1761`~~
(consumer_core.py fabricates "No description available," self-identified honest-empty candidate —
**CLOSED 2026-09-24**) · ~~`#1763`~~ (get_project_status
rider-failure evidence, tied to #1738 — **CLOSED 2026-09-24**) · ~~`#1767`~~ (dead file-disambiguation state on
`ConversationSession`, found during the #1759 deletion sweep, zero live referents — **CLOSED**,
per Arch's GO) · ~~`#1768`~~ (`classify_conscious` zero-caller dead code, residual from #1759's own
deletion — **CLOSED**, per Arch's GO-conditional). Plus, moved
here from Singletons 2026-09-12: ~~`#1697`~~ (files.html renders blank "Uploaded by:" because the live
API response has no `owner_id` field — a rendering-a-missing-field defect, same family as #1736/
#1761's fabricated-absence class, inverted: blank instead of a fabricated placeholder — **CLOSED
2026-09-24**) · ~~`#1718`~~
(BYOC key validation discards the failure reason, showing flat "invalid" for both auth errors and
quota/billing errors — already framed in this file as the audit's error-surfacing cousin #3,
**CLOSED 2026-09-24**,
alongside Fast Follow's `#1108`) · `#1772` (N=1 degrade reply named three unarmed sources, found
during #1717's own scoring — a scope-directive leak at the delivered layer. **Measured 2026-09-15**
at n=10/cell rather than CXO's original n=1: **50% leak rate on claude-sonnet (production's
default provider), 0% on gpt-4o** — the N≥2 aggregate path is clean on both, only the N=1 single-
directive path leaks, and only on one provider. Not caused by `#1717` (byte-identical prompt
pre/post-fix, re-verified). Also found: `'calendar'` isn't a registered `SOURCE_FAILED_FLAGS` check
at all — the model is naming a data category with no flag, not misreading which flags were set, a
different failure than originally filed. CXO's own discipline (refusing to widen a pre-registration
to capture an out-of-scope anecdote) is why this got measured rather than argued about).
**Mechanism + copy ruled 2026-09-24, ready to build.** Lead measured a candidate fix against the
50% N=1 leak: 0/10 vs 2/10 on the current copy, two independent nights, honest about run-to-run
variance (the baseline itself moved 50%→20% on an unchanged prompt). **Arch ruled: unify N=1 onto
the same aggregate composition site N≥2 already uses** — checked the code's own history first
(`conversational_floor.py:1385-1410`): the N=1/N≥2 split was a deliberate `#1717` decision, not an
oversight, reasoned at the time it was written; tonight's measurement falsifies the premise that
kept it split. Not a new mechanism — removing a carve-out the evidence no longer supports.
**CXO ruled the candidate's exact copy NOT acceptable as-is** — found four plural-presupposing
phrases in the candidate string (Lead flagged one, CXO found three more reading the exact rendered
text rather than the summary), the sharpest being "naming them together," meaningless at N=1 since
there's nothing to name together with. Supplied an N-agnostic rewrite designed to parse correctly
at N=1 and N≥2 without a fork, matching Arch's one-composition-site ruling. Both explicit that n=10
per arm can't certify a precise rate — the ruling is on mechanism/wording correctness, not a claim
the measurement alone proves performance; a larger/multi-night confirming run recommended before
calling this production-verified, not a blocker on shipping. **Shipped and confirmed same week,
2026-09-25**: Arch checked the live file rather than trust the ruling landed — CXO's exact
N-agnostic rewrite is verbatim on `origin/main` (`conversational_floor.py:1402-1406`,
`35854f46ec`), and a regression test (`test_source_failed_composition_1717.py:81`) pins the string
so a reversion would fail CI, not just review. **One open half remains, and it's PM's, not PPM's**:
a fresh-string confirming measurement (n≈20) that Lead is asking PM to budget — Arch is watching
the issue for that number, nothing further to rule on until it lands. No PPM action — build/measure
is Lead/Arch/CXO's lane; recorded here so the file matches what's actually ruled. Plus,
folded
2026-09-14: ~~`#1811`~~ (a calendar-context test mocks `_get_todays_todos`'s return shape wrong —
`()` instead of `(todos, total)` — the same test-theatre class as `#1760`; confirmed pre-existing
and unrelated to `#1807` via an A/B/A stash test — **CLOSED 2026-09-24**). Plus, folded 2026-09-19: ~~`#1829`~~ (**CLOSED
2026-09-24**) (Arch, from the
`#1823` branch-two trace) — `resolve_model`'s totality (services/llm/config.py) is achieved by
silent `.get()` fallback, not exhaustiveness: an unrecognized `task_type` silently resolves to the
`heavy` tier, and an unrecognized provider silently returns OpenAI's model IDs (latent at 3/3
providers today, live the moment a fourth is added). Same mechanism CXO/Arch already used to rule
`#1823` safe (provider-agnosticism holds today) is also what hides a mistier/mis-route defect — a
`.get()` with a default can't distinguish "absent" from "found the default," same shape as #1816
and this epic's own class. Asks for a build-time ratchet, not a vacuous
`assert resolve_model(p, t) is not None` (passes trivially given the fallbacks — the
`test_standup_data_sources` shape, `#1642`). Found missing from board/milestone at filing despite
the standing convention — fixed same-fire (MVP, board-added, Status=Product Backlog).

**Folded 2026-09-20, from PM's first real dogfood session on alpha (v0.8.12.0) — trust-critical,
this epic's own class at its sharpest**: ~~`#1836`~~ — the standup edit path claimed *"I've updated
your standup"* and rendered the VERBATIM UNCHANGED draft, discarding PM's explicit dictated content
silently. The `#1331` anti-confabulation rule ("never claim unverified action-success") violated
live, in front of the founder, in the first real dogfooding session. **CLOSED, caught 2026-09-26 by
a reconciliation pass — this entry had been left saying "stays open pending Arch's ruling" long
after it actually closed** (see below — `#1837` closed 2026-09-21, per this file's own later
entry; `#1836` closed alongside it but was never struck through here). Lead shipped a first-layer
fix same-day (`300ef8bbe`, makes the success message derive from a verified diff); the deeper
architectural cause (the fabricating fallback `_generate_basic_standup`/`_graceful_fallback` being
`#1289`'s undead default for every empty-capture turn) was resolved as part of the same closure.
**Shared with epic 3** (below): ~~`#1837`~~ — the interview-offer-acceptance
half is an acceptance-contract-rail defect (`#1651`/`#1652` machinery, offer accepted but never
arms the interview), while its fabricated-generic-template half and conversation-state-contradiction
half (denying an offer made three turns earlier) are this epic's own honest-empty/confabulation
class — tracked in both epics, built once. **This "remaining open" list is stale as of
2026-09-26 and not being hand-maintained anymore** — of the 10 named here, only `#1772` is
confirmed still open (verified directly, same status as noted elsewhere in this epic); `#1760`,
`#1761`, `#1763`, `#1697`, `#1718`, `#1811`, `#1829`, `#1836`, `#1837` are all confirmed CLOSED.
Trust the per-item strikethroughs throughout this epic, not this summary line — same pattern as
the other stale summary line already corrected below.

**CXO's design guidance for `#1836`'s fix, worth carrying to whoever builds it**: from the same-day
product-file-writing thread (PM's question, answered by PPM+CXO jointly) — scaffolding or an honest
re-entry into the interview state doesn't by itself fix confabulation if the completion CLAIM still
overstates it. *"A scaffold announced as 'I've written your standup' is still a false claim."* The
fix needs both halves: (1) the draft state must actually reflect what happened (Lead's proposed
honest-re-entry fix), and (2) the message describing that state must match it exactly — no
"I've updated" language unless a verified diff backs it (already Lead's stated direction for the
first-layer fix). Same principle, stated once so it isn't rediscovered per-issue: a corrected
artifact with an uncorrected completion claim is the confabulation relocated, not fixed.

**`#1836` and `#1837` both CLOSED 2026-09-21.** `#1836` closed alongside `#1837`'s completion — the
immediate defect shipped 2026-09-20 (`300ef8bbe`, verified-diff honesty), and the deeper cause (the
substring toy-NLU refinement engine that made most edits unappliable) is retired by `#1837` shape 3
(`5d52431d9`): free-form edits now go to the floor on the user's own key and actually apply, with
the diff-honesty rule staying as the engine-independent guardrail — exactly the two-halves fix
CXO's completion-claim principle called for. **This "remaining open" list is stale as of
2026-09-24 and not being hand-maintained anymore** — of the 13 named here, only `#1772` is
confirmed still open (verified directly); `#1760`, `#1761`, `#1763`, `#1697`, `#1718`, `#1811`,
`#1829`, `#1774`, `#1784`, `#1799`, `#1800`, `#1839` are all confirmed CLOSED. Trust the per-item
strikethroughs at each entry throughout this epic, not this summary line — several of those
entries hadn't been updated with today's closures either until this same fire.

**Separately, same memo: Arch also answered CXO's #1823 branch-two scope question** (is
provider-agnosticism deliberate/load-bearing, making branch two *permanently* empty rather than
merely empty today) — **yes, derived from BYOC (PM's #1812 ruling), not an independent preference;
trading it away breaks BYOC for any non-Anthropic-only user.** But it is not currently law — absent
from both `ESSENCE.md`'s five standing rules and the seven commitments, protected only by one
source comment and the incidental fact that all three providers today define all three tiers.
Arch explicitly declined to propose an ESSENCE amendment (would restate an existing law — BYOC — at
lower altitude) and instead filed `#1829` for the missing mechanism. **My #1823 ruling (branch two
out of scope) is unchanged and unaffected** — this only answers *how permanently* empty, which
doesn't change what ships.

**#1717 status (2026-09-12)**: code-done and live on v86 — awaits one harness re-run + CXO's voice
read against the contract's §6 acceptance test (item 1, the composition case). CXO's call, not
PPM's; noting here for tracking only.

**#1730 status (2026-09-12)**: Gap 1 evidence-complete. Gap 2's structural ruling landed same-day —
Lead proposed "ask-only-when-armed as an invariant" (option 3), Arch concurred with one condition
(the enforcement table's site census must be mechanical, not hand-maintained). #1759 (above) is
disposed as part of this ruling. Tracked here; the actual ruling and enforcement-table work is
Lead/Arch's.

**Why after epic 3, not before**: Arch's note — this is design-then-fix, and it benefits from the
acceptance contract proving the single-source-predicate idiom on a live seam first, rather than
inventing a second one in parallel.

✅ **User-facing contract owner named and delivered, ahead of the epic's own position** — CXO,
`docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md`, written the same day
this order was drafted rather than waiting for epic 5's turn (per Arch: *"cousin 1's aggregation
copy is CXO's user-facing contract, with the #1717 composition case as its acceptance test"* —
goes in the epic's own description verbatim when it's filed).

🔴 **CXO's read also corrects the epic's shape — this is not "add an aggregation rule."**
Aggregation for N-failed-slices already exists in ONE of two failure-reporting paths
(`orchestrator._combine_results`, deterministic string assembly) but not the other (the floor's
five `*_source_failed` directive sites, which the LLM composes freely). **The epic is "one noun,
two mechanisms" — thread `GatherOutcome` through the directive path without leaving the composed
path as a second, differently-honest voice.** CXO's own boundary: this is "two paths located" by
grep, not "two paths confirmed" — re-run the survey when scoping, don't inherit the count. Also:
Exec's live "I wasn't able to check" rider on a *succeeding* turn is a reportability defect
(content that had no business in that answer), not an aggregation defect — fixing aggregation
alone won't touch it; the site is unidentified.

⭐ **CXO's 09-10 framing on `#1738` — argues epics 5 and 6 share a rule, doesn't move either**:
`#1738` isn't a truncation bug, it's a provenance misattribution — the gather was `fresh` and
complete, the *renderer* dropped an item, and the assistant then described its own truncated
render as its evidence ("the list I got back"). Stated as a general rule now in the contract
(§5b, v0.2): a provenance value is a fact about the source and must survive rendering unchanged;
a render cap may shorten what the user sees, never what the system believes it has. Practical
consequence for whoever scopes this: "…and N more" is a claim the assistant must be able to cash —
if it can't name the N, the honest render is "6 archived; here are 5, ask for the rest," not a
silent truncation. CXO explicit: not proposing the fix, not re-ranking the epics.

**Folded 2026-09-22, backlog catch-up — four more of this epic's own class**: ~~`#1774`~~ (residual
from `#1768`'s deletion — an orphaned grammar-conscious component family left deliberately uncut,
"each its own unruled Rule-0 question," same shape as `#1759`→`#1768`, already this epic's own
lineage — **CLOSED 2026-09-24**, matching its own child `#1863`'s closure the same day).
**`#1774` UPDATED same day, evening**: Lead's fresh census found the dead family is
bigger than filed (`recognition_handler`, `recognition_response`, `moment_ui`, `articulation`, and
the whole `workspace_*` subfamily join the originally-filed five) — flagged because the family
borders the protected spatial-intelligence disposition and asked for a cross-check against my own
8/15 spatial ruling before any cut. **Arch's cross-check: clean, no collision** — verified there's
exactly one `class PlaceDetector` in the repo (the dead one); the spatial design record's mention of
"place_detector" is an informal name for `place_service`'s detection role, not a second live file.
**Ruled GO on the full expanded family**, same discipline as `#1797`. A second item on the same
issue (the writer-less `ConversationTurn.lens` surface, dead since `#1768`) ruled separately — rip
it, but as its own Rule-0 item pending a full reader-census, not bundled into tonight's cut (a
complexity deferral, not a token-pacing one — explicit given today's own no-self-throttle
directive). **That Rule-0 item is now filed: ~~`#1863`~~** (2026-09-23) — split out of `#1774` per
Arch's ruling, schema-touching on both ends (`ConversationTurn.lens`, `ConversationContext.
lens_stack`, `#953`'s persisted slice), needs its own reader census before the cut, not a rider on
the module-family removal. **Rip dispatched same day** (Lead, Sonnet lane) on Arch's two
conditions — fresh sweep first, hydrator legacy-key tolerance pinned behaviorally — design record
preserved. **CLOSED 2026-09-24.** ~~`#1784`~~ (a capped-list remainder lost to a process restart can't say "the list moved" —
the absent-vs-found-default shape this whole epic tracks — **CLOSED 2026-09-24**). ~~`#1799`~~ (priority-metadata source
failure degrades honestly in only one of three renders — the `#1777` shape, inconsistent honesty
across render paths — **CLOSED 2026-09-24**). ~~`#1800`~~ (`#1425`'s sentinel is mechanically enforceable today — mypy already
reports every drift site — but isn't wired as a ratchet, the exact "measured but not enforced" gap
this epic's own `#1829`/`#1836` entries already name — **CLOSED 2026-09-24**). ~~`#1839`~~
(`/health` reported a hardcoded
version and environment for months — a stale value presented as current, the same claim-doesn't-
match-state shape as `#1836`'s confabulation, just at the ops-observability layer instead of the
chat layer — **CLOSED 2026-09-24**). **`#1849` folded in 2026-09-22, same day, direct follow-on to `#1839`'s own fix**:
the Fly build path leaves `/health`'s `git_sha` reporting `"unknown"` — the deploy-identity fix
shipped but the SHA isn't actually injected at Fly deploy time, so the honest-value guarantee
`#1839` was supposed to establish doesn't yet hold on that specific path. Same claim-vs-state class,
found same-day because the fix is now live enough to be checked against. **~~`#1850`~~ folded in
2026-09-22, caught by this seat's own new third-queue-source criteria line same-day it was
filed** — `connector_bindings`' write path accepts arbitrary `mcp_server_ref` values with nothing
enforcing ADR-070's amendment; found by Arch ahead of the Fly cutover (live data was clean, but the
gap is structural, not a one-time data issue). Same "measured but not enforced" shape as `#1800`,
one layer down at the write-path/DB-constraint boundary instead of the mypy-sentinel one. **CLOSED
2026-09-24.**

**Folded 2026-09-23, from PM's live Test-1 dogfood session on alpha**: ~~`#1856`~~ — two defects in the
name-gathering flow: (1) initiation args aren't extracted into the flow's slots, and (2) the
name-gathering state treats ANY reply as a fresh prompt trigger with no repeat-detection — self-
identified as "the `#1836`-family template-loop shape in a different flow," this epic's own
confabulation-adjacent class of a flow re-asking/re-templating instead of honestly consuming state
it already has. **CLOSED, caught 2026-09-25 by a reconciliation pass — not previously marked.**
· ~~`#1858`~~ — `close_issue` on a nonexistent issue number reports the write as
indeterminate ("may or may not have gone through") when GitHub's 404 is a DEFINITIVE outcome, not
an unverifiable one; self-identified as "`#1824`'s bucket discipline, GitHub-write edition" —
`#1824`'s own family is collapsing distinct outcomes into one bucket, but the substance here
(reporting a knowable outcome as unknowable, sending the user to re-verify something that provably
never happened) is this epic's honest-empty/GatherOutcome class, not epic 2's auth-bucket one.
**CLOSED, caught 2026-09-25 by a reconciliation pass — not previously marked.**

**Found 2026-09-23 by this seat's own third-queue-source criteria line — pre-existing gap, not
from today's dogfood session**: ~~`#1570`~~ (filed 2026-08-10) — floor-bound QUERY turns report "no
data returned this turn" while the data actually exists (todos-pending and projects-list both
reproduced empty against live data, verdict FAIL on `#1544`'s claim), plus the internal
`[Available context: …]` annotation leaks verbatim into the user-facing reply. The sharpest
absent-vs-found-default instance this epic tracks: it isn't even a real absence, just a wrongly
wired data path reporting one. **CLOSED 2026-09-24.**

**Found 2026-09-23, both from today's active lane work (Lead's `#1499`/`#1856` lanes), filed same
day**: ~~`#1870`~~ — left open by `#1718` as explicitly out of that issue's scope, same class:
`_validate_gemini`/`_validate_perplexity` treat any non-2xx as `AUTH_ERROR` (the defect `#1718`
already fixed in `_validate_openai`), `validate_user_key`/`rotate_user_key` still consume a bare
bool with no live caller yet, and `conversational_floor._classify_llm_error` can drift from
`user_friendly_errors.py` — three honest-error-surfacing gaps, `#1718`'s own cousin-3 family.
**CLOSED 2026-09-23/24 overnight.** **~~`#1872`~~ folded in 2026-09-24, found by the `#1870` lane while
pinning both LLM-error classifiers against 22 shared fixtures**: the exact `_classify_llm_error`
drift `#1870` named, concretely instantiated — the floor's classifier doesn't recognize its own
production trigger string (`"All configured LLM providers failed. Details: …"`,
`services/llm/clients.py:442`), so every real terminal LLM failure falls to a generic `transient`
bucket ("try again in a moment") regardless of actual cause, while `user_friendly_errors.py`
correctly recognizes the same string — the two classifiers disagree on the most common real input.
**CLOSED, caught 2026-09-25 by a reconciliation pass — not previously marked.**
· `#1867` — guided flows can START sessions on `OnboardingProcessAdapter`, a deregistered process
(ADR-059 "on ice," commented-out registry call, zero production callers on
`_check_active_onboarding`) — orphan sessions with no reachable follow-up turn. `#1856` fixed the
visible symptom (the portfolio-add branch asking an unanswerable question) without fixing the
structural gap: nothing says which processes are actually wired versus "on ice" in comment form
only. Same family as `#1856`, one layer down. **`#1886` folded in 2026-09-24, `#1867`'s own
census made concrete**: of 10 guided-process session-start sites (6 STANDUP/SLOT_FILLING, both
live), 4 start the dark ONBOARDING process. Worst is `_handle_add_project` (the `#1856` rewrite
itself, live and user-reachable) — an "add project" turn with no extractable name creates an
onboarding session directly, bypassing `ProcessRegistry`, and a bare-name reply orphans it; plus
the dead `_check_portfolio_onboarding`/`offer_onboarding`/`start_onboarding` chain, strict-xfail
pinned so it can't silently regress further while `#1867`'s structural fix is pending.

⚠️ **Found 2026-09-24, filed by Web, `priority: critical` + `beta:auth-lifecycle` — blocks
EVERY new account on alpha, not a partial-coverage gap**: ~~`#1875`~~ — the setup wizard's Step 1
("System Check") hard-blocks all new signups with a disabled Continue button. Root-caused to
source, not inferred: `require_setup_incomplete` (`web/api/routes/setup.py:294`, `#1504`'s
security fix) correctly 403s once setup is complete with a specific, actionable message ("Sign in
and manage credentials from Settings → Integrations instead") — but that message never reaches the
user. Something above it in the stack swallows the specific detail and substitutes a generic
"contact your administrator" 403, which the frontend's fallback UI then renders as if literal infra
(Docker/PostgreSQL/Redis/ChromaDB) were down, with instructions to run `docker compose up -d`
against a hosted production instance. Two stacked honest-empty defects: the real message lost in
transit, and a fabricated wrong-cause UI standing in for it — the same class this epic tracks, at
the highest severity found in it so far since it's the first-contact surface itself. **CLOSED
2026-09-24, same day it was filed — fast turnaround on a critical-severity blocker.**

**`#1889` folded in 2026-09-24, follow-up from `#1587` (Production-scoped, closed, outside this
file) finding two surfaces the fix doesn't yet reach**: `degraded_sources` now flows correctly to
`StandupSummary.to_prose` and the Radar JSON (§4-compliant, never prints "Nothing to show yet"
over a failure) — but (1) standup's Slack/Markdown/text formatters and the `/today` JSON route
still don't carry it, so a Slack standup over a failed GitHub read reads like a clean empty, and
(2) Radar UI's empty-state teaching card renders unconditionally on `state == "empty"` even when
the emptiness is a real failure, since the JS doesn't branch on the field the JSON now carries.
Named explicitly as "the m-44 false-clear shape one hop downstream of the fix" — filed so the
original fix isn't read as covering surfaces it doesn't.

### 6. Rendered deliverable (7 items, 5 closed + 2 shared with GatherOutcome/Security) — same reasoning as 5
~~`#1729`~~ (**CLOSED, caught 2026-09-26 by a reconciliation pass — not previously marked**) · shares `#1732` (security, **CLOSED**) and `#1738` (GatherOutcome). Plus, folded
2026-09-12: ~~`#1762`~~ (render-truncation sweep, ~18 more "...and N more" sites, self-identified as
#1738's class / epic-6 threading — **CLOSED 2026-09-24**).

**Found 2026-09-23 by this seat's own third-queue-source criteria line — pre-existing gap, not
from today's dogfood session, both filed 2026-08-15**: `#1625` — reminder surfacing is relentless
(due-reminders block appended to four consecutive replies inside one standup interview, including
mid-question); PM's own design ruling: pin due reminders to the top of Radar, mention in
conversation ONCE, not every reply — `#1566`'s surfacing-rider fix over-rotated from "never
surfaced" to "surfaced every turn." · ~~`#1628`~~ — chat-side listing surfaces (`get_open_issues` and
similar "show my open issues" renderings) print GitHub titles verbatim outside the render-guard
seam `#1622` landed at (`services/radar/sources.py` only covers standup/Radar/Places); a degenerate
title still surfaces raw there. **CLOSED 2026-09-24.**

**`#1880` folded in 2026-09-24, found by the `#1762` portfolio-cohort lane (`#1762` closed same
day) — three distinct §5b residues left deliberately for this epic's own turn, not fixed in
passing**: (1) calendar `free_blocks[:3]` under a header stating the full `len(free_blocks)`, class
(a) (bounded, user-owned) · (2) clarification-turn `matches[:5]` under "Found N matching" on a turn
whose whole purpose is choosing among them · (3) three latent `[:N]` slices already capped
upstream at the same N — zero loss today, silent elisions the day `#1776` lifts either cap; rule
named explicitly: convert in the SAME change that lifts the cap, never before. Also flagged
(method, not code): the census vocabulary the 09-13 sweep grepped for is not closed (missed
`"_Plus N more projects_"`'s phrasing) and lives only as a session-log table, so each sweep re-greps
by hand — a tracked census file would close that, not this epic's own item to build.

**Why here**: same "prove the idiom first" logic as epic 5; MCP-path-first per the ratified scope
ruling, per Arch. **Copy owner: CXO** (effective 2026-09-13, same day the copy shape below was
delivered — matches epic 5's line, filled 09-11).

**Joint invariant with epic 5, confirmed by Arch (2026-09-10)**: §5b's rule (provenance must
survive rendering unchanged; a render cap may shorten what the user sees, never what the system
believes it has) applies here too — the direction (not yet the build) is that the renderer
consumes the structured GatherOutcome and never becomes the model's own evidence about the world.
Fix design waits for this epic's turn; nothing jumps the queue.

**Design landed 2026-09-13** (Lead's `#1762` census + CXO's copy + Arch's architecture, all
converged same-day): the unrendered remainder lives in **GatherOutcome** (§5b already governs the
claim; the #1738 joint invariant is the storage half). **First build scoped to the GitHub six**
(issues, PRs, milestones, releases, labels, branches) — the only cohort where the honest-count half
is already done and only threading is missing, per Lead's `#1720` census. Copy shape (CXO):
*"That's 5 of 340 — say the word and I'll pull the rest,"* offer the affordance never the syntax,
cap counts inherit source provenance (a source `1000+` stays `1000+`, never rounds to exact). **PPM
call**: skip the offer entirely when the hidden remainder is ≤3 items — just render them, no
ceremony. **Acceptance-test addition, not a scope change**: CXO flagged that a capped-list offer is
exactly the kind answered LATE (read five, think, come back), but today's arm survives only one
turn (`intent_service.py:1072`) — epic 6's acceptance test must include the late-follow-up case,
not just the immediate one, or it passes without exercising the property that actually fails.

### 7. False-trails / claimed-not-wired (4 items, 2 closed) — pre-existing epic, no stated urgency
`#1522` (the epic itself, PM-directed) · `#1735` · ~~`#1678`~~ · ~~`#1708`~~ (moved here from Singletons
2026-09-12 — `ALPHA_QUICKSTART.md`, the tester-facing onboarding doc, tells testers to clone a
branch 7,614 commits stale and describes the live hosted app as a future plan; a claimed-state vs.
actual-state mismatch on a first-contact surface, the exact false-trails shape). **Both CLOSED
2026-09-24.**

### 8. Spatial-disposal (2 items, 1 closed) — pre-existing epic, no stated urgency
`#1698` (the epic itself, PM-ruled 08-15/16) · ~~`#1700`~~.

### 9. Catch-all: singletons too small to be their own epic (12 items, 9 closed) — COLLAPSED 2026-09-19, was epics 9+10
**PM ruling, 2026-09-19, in-conversation, relayed by Exec** (verbatim, both sentences matter):
*"Agree the mini-epics do not serve. If we use an epic model then we can't have strays. We need a
catch all, and a 3-item epic is really just an issue with three child issues. It's just piles and
sizes and focus of attention so let's not overindex on our filing rules."* Former epics 9
(Silent-death inventory) and 10 (Composer UX polish) fold in here. The 09-12 every-MVP-item-needs-
an-epic-home ruling still stands — this catch-all is what makes dropping the mini-epics safe rather
than reopening the unordered pile that ruling closed. **Epic count: 11 → 10.**

**Silent-death inventory** — `#1423` (the inventory-and-un-swallow task, open; broad try/except on
core paths converts broken features into invisible defaults) with ~~`#1420`~~/~~`#1422`~~ (the two
confirmed instances #1423 names, both fixed and closed) now riding as **#1423's children**, not
separate epic membership — Exec's framing, and the more honest shape: they were always the concrete
instances the inventory exists to cover, not independent epic members. **Preserving the
distinctness Arch originally named** rather than flattening it: this shares no real mechanism with
composer UX below or any epic elsewhere — it's exception-handling-layer work, kept legible as its
own labeled group inside the catch-all rather than lost in an undifferentiated pile (Exec's own
flag: a catch-all that erases genuinely different mechanisms recreates the problem from the other
side).

**Composer UX polish** — ~~`#1737`~~ — the web chat composer ticker-tapes horizontally instead of
growing vertically as PM types a longer message, so only the tail of what was typed stays visible.
PM reported it live as direct usability friction on the primary chat surface. **CLOSED 2026-09-24.**

**Backlog catch-up, 2026-09-22 — found by a new mechanical check** (see below): standalone
protocol/infra items with no shared mechanism elsewhere. ~~`#1723`~~ (GitHubOperations Protocol —
type the router's contract, delete dead dispatches; PM-ratified 2026-09-06, Arch's own follow-on
to #892/#1709 — **CLOSED 2026-09-24**). ~~`#1835`~~ (docker-compose defines a dead orchestration service, bit the v0.8.12.0
cutover — **CLOSED, caught 2026-09-26 by a reconciliation pass — not previously marked**). ~~`#1840`~~ (mail-send half-landed a triage batch — `read/` additions pushed, inbox deletions
silently dropped; the `#1746`-adjacent mechanism this seat has watched since 09-18 — **CLOSED
2026-09-24, resolving this seat's own long-carried "ALSO WATCH" item.** Fixed in `mail-send.sh`
(a guard added, verified behaviorally both ways — refuses on a probe that would change nothing,
passes through on a genuine multi-path move — confirmed via `git ls-tree origin/main` before/after
on a real 11-path send that correctly landed all memo copies + inbox→read moves). None of these three
share a mechanism with each other or with the epic's existing two
members; grouped here only because each is genuinely singleton, per this epic's own founding rule.
(`#1731`, the sibling silent-drop issue watched alongside `#1840`, is milestoned `Ongoing`, not MVP
— correctly outside this file's scope, not an oversight.)

**Folded 2026-09-23, from PM's live Test-1 dogfood session on alpha**: ~~`#1859`~~ — every chat switch
flashes the whole page white and redraws from scratch, reported by PM as a regression. Lead already
ruled out the obvious candidate same-day (the cutover's Caddyfile carries no compression/cache-
header change, asset headers unchanged) — needs a browser-level trace, Web lane. Genuinely singleton
here: shares no mechanism with the other three items in this group or with any other epic. **CLOSED
2026-09-24.**

**Found 2026-09-24 by Web, while tracing `#1859`**: ~~`#1874`~~ — intermittent 503s on ~32 static
asset requests during page load, reproduced 2 of 4 fresh Playwright sessions against production, no
single consistently-broken file. Web's own note ties it to `#1859`: that issue's root cause is
every chat switch re-fetching all ~32 assets fresh with zero caching/304s, so if the server has any
concurrency ceiling on simultaneous static-asset requests, `#1859`'s lack-of-caching makes this 503
pattern more likely to surface — worth considering together, not as unrelated. Server-side cause
unverified (needs Fly logs/metrics access Web's browser-only seat doesn't have). Kept as its own
item alongside `#1859` rather than merged, since the connection is a hypothesis Web named
explicitly, not a confirmed shared mechanism. **CLOSED, caught 2026-09-25 by a reconciliation
pass — not previously marked.**

**Found 2026-09-23 by this seat's own third-queue-source criteria line — pre-existing gap, filed
2026-07-10, six weeks old**: `#1386` — BETA-GATE, the formal gate closing the Beta Blockers sprint
and declaring the system ready for the beta wave (behavioral verification of the *assembled*
system, not just issue-list draining). Cross-cutting by nature — it gates every epic in this file
at once, not any single one's mechanism — so it belongs in the catch-all rather than forced into
one epic's list. Status stale (last touched under DRAFT review 2026-07-10); needs a fresh look
against where the sprint actually stands now, not just a board fix.

**Found 2026-09-23, from the `#1499` SlackWebhookRouter member-strip lane while tracing
reachability, confirmed by Lead**: ~~`#1871`~~ — `standup_workflow_skill._post_to_slack` calls
`SlackDomainService.post_message`, a method that does not exist (the class's only send methods are
`SlackClient.send_message`/`SlackIntegrationRouter.send_message`) — the Slack-post leg of the
standup skill can never have worked live, masked because unit tests mock `post_message` directly
rather than exercising the real class. Genuinely singleton here: an integration call-site defect,
not sharing a mechanism with anything else in this group. **CLOSED 2026-09-23/24 overnight.**

**Found 2026-09-24, while answering Web's "couldn't find a Preferences section" from their `#1859`
render-sweep memo**: ~~`#1876`~~ — no surface sets a user's timezone at all.
`UserPreferenceManager.set_reminder_timezone` has zero callers anywhere in `services/`/`web/`
(grepped, not assumed); `settings-index.html` has no Preferences card (Personality, Learning &
Patterns, Privacy & Data, Account, Transparency, LLM API Keys, Integrations, Projects, Advanced —
no Preferences); no chat action sets it either. Every clock face (`#1576`'s own family, closed
Production-scope, outside this file) renders on the default zone for everyone, silently. Fix
direction named (Lead's lane): a Preferences card + `PUT /api/v1/preferences/timezone` route,
optionally a chat action via the workflow-dispatcher rail (no new `elif` chain, `#1124`), and a
first-login nudge if the browser's detected zone differs from the stored default — explicitly
framed as the honest-empty shape (don't silently assume Pacific). Genuinely singleton: a missing
settings surface, not sharing a mechanism with anything else in this group. **CLOSED, caught
2026-09-25 by a reconciliation pass — not previously marked.**

**Found 2026-09-24, follow-up from `#1775`'s dead-code deletion (Lead)**: ~~`#1883`~~ — 8 living docs
still describe the deleted standup-consciousness family (`StandupToChatBridge`,
`format_files_conscious`, etc.) in the present tense, as if it's live and wired, when it was
"designed, never wired, and disposed on 2026-09-24." Named explicitly as **Docs' lane** (the
`#1719` "moved-but-refs-not-updated" family) — genuinely singleton, docs-accuracy rather than a
code defect, not sharing a mechanism with anything else in this group. **CLOSED, caught 2026-09-25
by a reconciliation pass — not previously marked.**

**Found 2026-09-24, found by the `#1582` lane**: `#1890` — `templates/components/
greeting_context.html` has zero include sites anywhere (`git grep` across templates/web/services),
an orphaned partial. Rule-0 delete candidate; flagged for a cross-check against the
`dark_templates` allowlist in `tests/test_completion_ratchets.py` (delete + lower the ceiling in
the same commit if already allowlisted; a census blind spot worth a row if not). Genuinely
singleton: dead-template housekeeping, no shared mechanism with anything else in this group.

### 10. Schema/domain correspondence (2 items, 0 open) — genuinely its own epic
~~`#1788`~~ (**CLOSED, caught 2026-09-26 by a reconciliation pass — was shown "open — one registry
entry from green," not previously marked**) · ~~`#1797`~~ (disposal-pipeline issue for the 5 dead
persistence twins, filed 2026-09-13 — **CLOSED 2026-09-22**, all seven acceptance criteria
discharged, executed per the delete-module-safely skill against Arch's 09-13 ruling; fresh census
confirmed zero imports of the five DB classes anywhere before deletion). The PM-056 schema-validation
workflow came back to life
today after months dead and found 13 apparent missing `to_domain`/`from_domain` converters across
7 DB models. Arch's ruling, by importer census not name-matching: **2 real correspondence**
(`SessionActivityDB`; `DocumentDB` re-ruled below) · **5 dead persistence twins** (`Feature`,
`Intent`, `Product`, `Stakeholder`, `Task` — create-all-era, tables never migrated per `#1273`).

**Executed 2026-09-13, 6 of 7 (Lead)**: the five twins confirmed by an independent census (domain
`Intent`'s 26 importers reproduced exactly) — checker off, reason line, a stale-entry guard, and
`#1797` filed. `SessionActivityDB` converter written and verified against a real read path (three
live consumers), 7 round-trip tests.

**`DocumentDB` RE-RULED 2026-09-14 — cat (2), not cat (1)**: Lead's disagreement was correct.
Arch's original census measured only DocumentDB's live DB-side importer and stopped; Lead found
its **domain twin is also dead** (zero importers outside `models.py`), and the two classes aren't
even the same shape — domain `Document` is content-bearing, `DocumentDB` is the ADR-071 D2
owner-anchor row (`chromadb_base_id`, `owner_id`, `is_global_pm_domain`) with no content column at
all. A converter would have to invent a NOT NULL key and drop two security fields. **DocumentDB's
own reason line** (distinct from the five's "dead persistence twin"): *"live owner-anchor row with
no domain counterpart — the name-matched domain class is a different, dead object."* **The
generalizable point is now IN the ruling, not a footnote**: liveness must be measured on both
sides of a correspondence — a live DB class with a dead domain twin fails exactly as Arch's
original `Intent` case (dead DB, live domain) did, inverted. PM-056 job 2 goes green once this
registry entry lands — the only remaining step. One new orphan surfaced, tracked separately and
NOT part of `#1797`'s set: dead domain `Document` itself (zero importers, only referenced via
`Artifact.from_document`/`to_document`) — a domain class, not a DB twin, credited to Lead's own
finding, not yet filed as its own issue.

**Why its own epic**: schema/model-layer correctness discovered via a revived CI workflow, sharing
no real membership with epic 1's CI mechanics or epics 5/9's dead-code shapes (different mechanism
entirely).

---

**Retired 2026-09-12**: the old "Singletons" section (`#1423`/`#1695`/`#1697`/`#1708`/`#1718`/
`#1737`) is gone. Per PM's ruling (relayed via Janus, 2026-09-12 evening): discovered work is fine,
but every MVP item needs an epic home — a singleton pile outside the epic-relative view was
invisible to the instrument PM actually reads. Four of six had genuine homes in existing epics
(`#1695`→3, `#1697`/`#1718`→5, `#1708`→7); two (`#1423`, `#1737`) genuinely share no membership with
anything else and got their own epics (9, 10) rather than a forced fit. The cross-milestone note
on `#1718`/`#1108` carries forward into epic 5's entry above.

---

## The falsifiability note, carried from Arch's memo (why this ordering is checkable, not asserted)

10 of 37 map directly to the un-modeled-noun audit's cousins; the acceptance-contract control case
arguably makes it 18. The rest group under four pre-existing cause-epics. **If a future factoring
pass finds the singletons refusing to shrink, or an epic's membership turning out wrong on a full
read, that's real information — update this file, don't defend the original grouping.**

## Change log
- 2026-09-09 (PPM): first version, built from Arch's factoring + dependency notes + CXO's
  copy-contract flag. 37 items, 8 epics + 6 singletons.
- 2026-09-09 evening (PPM): epic 5 (GatherOutcome) updated — CXO's copy contract delivered ahead
  of schedule, and CXO's own read corrects the epic's shape from "add an aggregation rule" to
  "unify two existing mechanisms." Scope-guard chokepoint (open question in v1) now has a joint
  CIO+Arch design in progress — GH Action on merge-to-main, PPM named consumer for milestone-
  consistency flags delivered as mail, advisory-first for two weeks before any required check.
- 2026-09-10 (PPM): three items closed (`#1637`, `#1732`, `#1734`) across epics 1 and 2 — marked
  in place rather than removed, so the record shows what closed and when. Folded two new findings
  from fixing `#1732` into epic 2 (`#1740`, `#1741`) rather than filing them as unplaced
  singletons. Added CXO's provenance-vs-rendering framing to epic 5 (argues epics 5/6 share a
  rule; doesn't reorder either). **General note, not epic-specific**: Exec found the board's In
  Progress count is not a reliable in-flight signal — three closures this week went Sprint
  Backlog → Done directly, skipping it. Don't read a flat In Progress count as "nothing is
  moving" when checking this file against live board state. Also added epic 6's §5b pointer per
  Arch's ask, so both cousins carry the joint invariant rather than one.
- 2026-09-10 later (PPM): scope-guard status — both halves shipped
  (`scripts/scope-drift-check.sh`, `.github/workflows/scope-guard.yml`, still dispatch-only, not
  armed). Added a `verdict:` header slot to the memo template per CXO's catch (the promotion
  decision was riding a hand-kept tally, the one bolt-on left in an otherwise chokepoint-shaped
  design) — rate now reads from memo headers via grep, not a habit. Ran two `workflow_dispatch`
  tests (95 and 300 recent commits, both quiet/0-flagged) — verifies the predicate and quiet-run
  path fire correctly; does NOT yet verify the memo-delivery path, which hasn't fired in either
  test. Arms after `#1687` closes per the standing sequencing condition (epic 1, above).
- 2026-09-10 even later (PPM): Arch ran the real synthetic test (`#1744`, fixture issue,
  Blocked). **Predicate proven live** (1/1 flagged correctly). **Delivery half found broken**:
  `GITHUB_TOKEN` can't push to protected main (GH006) — Arch's retry loop had silently swallowed
  the push failure and reported SUCCESS with no memo delivered, a real false-clear. Fixed same-day
  (failed delivery now fails the run loudly). **The remaining decision is PM's**: bot needs either
  a branch-protection bypass grant or a scoped PAT secret — repo-settings change, not ours to make
  unilaterally. `#1744` stays open until the delivery path is actually observed working.
  **CXO also caught a real gap in my own verdict-slot fix**: the grep-count has no denominator, so
  it can't distinguish "zero flags occurred" from "flags occurred and never arrived" — exactly the
  state the bot-can't-push defect put us in. **Fix accepted, sequenced with arming** (a per-run
  ledger, `dev/active/scope-guard-runs.tsv`, one line per run whether quiet or flagging — not
  built yet, since it closes nothing before PM's decision lands anyway). **Not armed. Blocked on
  PM.**
- 2026-09-11 16:11 WORK (PPM): 3 unmilestoned issues triaged — `#1747`/`#1748`/`#1749`, all filed
  same-day from a direct #1687 close-out audit (same author). All stated "Milestone: MVP" in body
  but the field wasn't set; milestone set, added to board, Sprint=Beta Blockers/Status=Sprint
  Backlog matching #1687/#1711 precedent, verified no collateral damage. Folded into epic 1 as a
  continuation rather than new epics — `#1747` is a direct instance of the epic's own risk (the
  belt's tracked-workflow denominator silently drifted from four to six).
- 2026-09-12 10:09 WORK (PPM): epic 2 (Security/tenancy) closed in full — all 6 members done,
  live-verified deployed (Lead, v74/v76). Two epic-2-class follow-on findings (`#1750`, `#1751`)
  from the #1733 close-out sweep deliberately NOT folded in (would reopen a closed epic) — parked
  at MVP/Product Backlog instead. `#1752` (found during #1654's own epic-3 adoption) folded
  directly into epic 3, now 9 items. **Denominator question answered for Lead**: this file's own
  "37 Sprint Backlog items" provenance line (2026-09-09) was a board-Sprint-Backlog snapshot for
  epic-factoring purposes specifically, not a claim about the milestone-wide count — Lead's
  tracker headline should use milestone-wide (matches `sprint-truth.py`'s own convention, which
  this file and PPM's every-fire count both already use). No conflict; just two different
  denominators serving two different purposes, now stated explicitly so it doesn't drift again.
- 2026-09-12 13:09 WORK (PPM): 10 unmilestoned issues triaged, all folded into already-open epics
  (none reopened): `#1755`/`#1756`/`#1757` → epic 4 (now 9 items, classifier-audit siblings of
  #1505/#1527); `#1754`/`#1759`/`#1760`/`#1761`/`#1763` → epic 5 (now 9 items — #1754/#1759 are
  independent same-day findings of the same ConversationHandler dead-code shape, #1759's
  disposition already ruled DELETE per Lead/Arch's same-day #1730 Gap-2 concurrence); `#1762` →
  epic 6 (now 3+2 shared items). Also closed `#1166` (Type-2 Dreaming three-way convergence,
  CXO/PPM/Arch, done since 2026-06-08) — corrected the stale `roadmap.md` Dreams row in the same
  pass (had read "spec-read pending" for three months after convergence landed). Recorded #1717
  and #1730's same-day status for tracking (both are CXO's and Lead/Arch's calls respectively,
  not PPM's — noted here only so the file stays accurate).
- 2026-09-12 16:09 WORK (PPM): 5 more unmilestoned issues triaged (0→5 in one fire, all filed
  today from Lead's lanes) — `#1764`/`#1765` → epic 1 (both #1748-lane findings, #1765 is #1749's
  env-divergence class inverted); `#1767`/`#1768` → epic 5 (dead-code siblings of #1759, same
  deletion sweep); `#1771` → epic 3 (found during #1769's own adoption — #1769 itself was already
  closed+milestoned by Lead before this fire, net epic-3 change is +1 not +2). Verified against
  #1748 as a known-good control — no collateral damage. **Ratified Exec's filing-convention
  extension** (flagged same-day): new issues get Product Backlog status AND a milestone at filing
  time, not just Status — "unset" should not be a reachable state for either field. Lead will fold
  this into lane briefs the same day. This is the third time this week unmilestoned drift has hit
  double digits across a few fires; the ratification is meant to close the gap at the source
  rather than keep relying on per-fire triage to catch it.
- 2026-09-12 19:09 WORK (PPM): PM ruling relayed via Janus — discovered-work triage into epics is
  "clear and welcome," but every MVP item needs an epic home, no exceptions. Retired the
  Singletons section: `#1695`→epic 3, `#1697`/`#1718`→epic 5, `#1708`→epic 7 (real membership
  fits, found on full reads rather than the original title-only classification). `#1423`/`#1737`
  got their own new epics (9, 10) since neither shares real membership with anything — same
  standard the file has used all along (an honest epic-of-one beats a forced fit), just now
  applied to the last two holdouts instead of parking them unordered. Also fixed `#1772` (had MVP
  milestone but was missing from the project board entirely — filing with `--milestone` doesn't
  board-add, a new drift shape sprint-truth.py's "not on the board" check just caught for the
  first time) and folded it into epic 5. Noted Lead's three Rule-0 delete proposals (`#1754`/
  `#1767`/`#1768`) and Arch's GO/GO/GO-conditional rulings for tracking — Lead/Arch's call, not
  PPM's, no epic-order change needed since deletion doesn't move milestone membership.
- 2026-09-13 09:58 START (PPM): Exec published an epic-accounting doc for PM
  (`dev/active/epic-accounting-2026-09-13.html`), computed live from the GitHub API. Caught and
  corrected one real gap in it (missing epic 10 entirely — flagged to Exec/PM) and adopted one
  real improvement to this file (epic 9's item count was undercounting its own two named
  instances, `#1420`/`#1422` — now 3 items, matching Exec's fuller read). While cross-checking,
  refreshed live-closure state across epics 1, 3, and 5 (many items closed since last night:
  epic 1 now 4 closed of 8, epic 3 ran to its floor — 8 of 11 closed, only the umbrella + 2 stay
  open — epic 5 is 8 of 14 closed and is the epic Lead is now actively working). Also confirmed
  Lead posted the #1687 secret-rotation comment PM was waiting on — the WATCH FOR line in
  tonight's cron prompt can drop once PM actually does the ~3-minute rotation.
- 2026-09-13 16:22 WORK (PPM): CXO caught a genuinely stale line in epic 6's own entry — "name the
  copy-owner before scoping the fix" sitting eleven lines above the delivered copy shape from
  earlier today. Fixed: epic 6's copy owner is now stated as CXO, matching epic 5's pattern.
  Triaged 3 more issues: `#1785` (already had MVP milestone via the filing convention, but was
  missing from the board — folded into epic 1, now 9 items) and `#1786`/`#1787` (both CI-hygiene
  findings from the #1436 mypy-gate lane; milestoned Production, not MVP, matching #1436's own
  milestone — not part of this file). PM's secret rotation on `#1687` appears to have happened,
  per `#1785`'s own filing account; `#1687` itself stays open pending Lead's close-out comment.
- 2026-09-13 19:22 WORK (PPM): `#1788` (PM-056 schema-validation finding, MVP-milestoned, no epic
  home) added as epic 11 — genuinely doesn't share membership with epic 1 (CI mechanics vs. what a
  working CI found) or epics 5/9 (different dead-code discovery mechanism). Arch's per-model
  ruling was Lead/Arch's own technical call, not PPM's; folded in for tracking only. CIO's
  belt-methodology closeout thread was cc-only, no PPM action.
- 2026-09-14 10:22 WORK (PPM): Arch re-ruled `#1788`'s DocumentDB question — Lead's disagreement
  was correct, DocumentDB is cat (2) not cat (1), with its own distinct reason line. Updated epic
  11 to reflect the resolution; `#1788` is now one registry entry from green. Triaged 2
  unmilestoned issues, neither MVP: `#1798` (git-hooks infra, Ongoing/FLYWHEEL) and `#1801`
  (auto-generated weekly docs-audit issue, Ongoing/Q-Recurring-Audits, matching every prior
  instance's precedent). Also read the morning's model-tier-ceiling incident (Janus's correction
  to Exec's 7-role alert — only 2 seats genuinely blocked, PPM was among the 4 that self-recovered
  within 18 minutes, not part of the real outage) — cc-only, no epic-order impact.
- 2026-09-14 13:22 WORK (PPM): **Real structural ruling** — PM escalated tenancy as "our
  fundamental value and promise" after two epic-2-class holes (`#1807`, `#1791`) surfaced against
  an already-closed epic 2. Lead asked for a ruling rather than guessing; created epic 12 (Tenancy
  hardening), Lead's own weak preference — keeps epic 2's closure true for what it contained while
  giving PM's newly-named class explicit tracking. Moved `#1750`/`#1751` here from epic 2's
  parking note. `#1807` closed same-day (Lead's lane); two more findings from that same lane
  (`#1809`, `#1810`) folded in immediately. Also fixed a missing board-add on `#1807` (closed
  issues can still be missing from the board — same drift shape as `#1772`/`#1785`, just on a
  closed item this time) and bumped `#1791`/`#1750` off Product Backlog now that they're actively
  epic-tracked rather than parked. Separately triaged 4 docs-drift issues (Ongoing/FLYWHEEL,
  matching `#1720`'s precedent) and folded `#1811` into epic 5 as a `#1760`-class test-theatre
  finding.
- 2026-09-14 16:22 WORK (PPM): epic 12 developed fast same-day. Lead escalated #1810 as worse
  than #1807 (leak runs both directions); Exec/HOST/Arch/PM held the first external tester's
  invite until it closes. Arch ruled the fix (delete the global-slot write entirely, no
  legitimate consumer) and the sequencing (#1810 → #1809 → #1791, same architectural principle
  each layer down). CXO found a separate live trap in existing out-of-quota copy while drafting
  #1809's — not yet filed as its own issue, noted for whoever picks it up. No PPM ruling needed
  this fire beyond keeping the file current; Exec explicitly confirmed epic 12 already answered
  the "where does this sit" question from this morning.
- 2026-09-14 19:22 WORK (PPM): **PM overruled epic 12, and was right to.** PM's ruling, verbatim:
  *"If we discover that there's more work on an epic than we realized and we closed it before
  discovering that work, then yes we need to reopen the epic... the truth is more important than
  the feeling of progress."* Epic 12 (Tenancy hardening, created this same day) is retired; its
  six items fold back into epic 2, which reopens. **Owning this plainly**: the successor-epic
  shape was mine to approve, not just Lead's to propose, and I approved it for the reason PM's
  sentence names exactly — "epic 2 closed" is a scoreboard property, and epic 2 was not actually
  complete when it closed; new work arriving after an incomplete closure is not the same fact as
  new work arriving after a real one. I had the audit-bias discipline in hand for other people's
  artifacts this week and didn't apply it hard enough to my own boundary call. Now 11 epics, not
  12. **Separately, PM asked directly why the count went from 6 to 12** (now 11) — answered by
  memo to PM (not duplicated here in full): most of the growth traces to two of PM's own prior
  directives (Arch's 09-09 cause-factoring, and the 09-12 "every item needs a home" ruling) plus
  three genuine new-discovery clusters this week (epics 9, 10, 11), not scope creep in the sense
  of invented tracks. Epic 12 was the one real overreach, now corrected. Offered PM the option to
  simplify epics 9/10 (1-3 items each) into a named short list rather than epic framing, if PM
  prefers a stricter definition of what counts as a track.
- 2026-09-15 10:22 WORK (PPM): `#1816` (consent-boundary fail-open) folded into epic 2 — found
  during `#1815`'s own investigation, ruled by Arch as the honest-empty family's shape one layer
  down at the security boundary. Board-bumped from Product Backlog/no-sprint to Sprint Backlog/
  Beta Blockers, matching every other active epic-2 item this week. Invite lifted again same
  morning after HOST independently checked #1816 doesn't touch Janne's own path. No PPM ruling
  needed — all four of Arch's rulings and CXO's copy catch are Lead/Arch/CXO's own domain.
- 2026-09-15 13:22 WORK (PPM): epic 2's `#1815`/`#1816` both closed same-day (fixed at v111, CXO's
  own proposed copy shipped ahead of formal ratification, confirmed with one clause cut same-fire)
  — the whole consent fail-open thread resolved in roughly six hours from discovery. `#1817` (the
  invalidation-trigger issue Arch's ruling required) triaged and folded in — a dated assumption's
  tripwire, not a bug. Separately updated epic 5's `#1772` entry with real measurement data: 50%
  leak rate on claude-sonnet (production's default), 0% on gpt-4o, n=10/cell — a genuine escalation
  from the original n=1 anecdote CXO deliberately declined to over-claim from. No PPM ruling needed
  anywhere this fire; Arch also proposed a mechanical fix for their own recurring cross-reference
  failure mode (quote-inline or mark unverified) after a third same-shape instance in three days —
  noted for the record, not PPM's mechanism to adopt.
- 2026-09-19 19:22 WORK (PPM): **PM ruled on the epics-9/10 question offered 2026-09-14, five days
  open.** Verbatim: *"Agree the mini-epics do not serve... let's not overindex on our filing
  rules."* Collapsed former epics 9 (Silent-death) and 10 (Composer UX) into one catch-all epic 9,
  preserving epic 9's original distinctness as a labeled subgroup rather than flattening it (Exec's
  flag: a catch-all that erases genuinely different mechanisms recreates the problem it solves).
  `#1420`/`#1422` now ride as `#1423`'s children, not separate epic membership. **Epic count: 11 →
  10** (old epic 11 renumbered to 10) — this reverses part of the 6→12 growth PM questioned on
  09-14. Separately: corrected `#1785`'s epic-1 entry (shipped wholesale, not the split originally
  recommended — Lead's own re-verification found the recommendation's premise was wrong before
  shipping); folded `#1812` step 5's UNBLOCK (PM ruled today: PM's own account gets normal-account
  semantics, no operator-key special case) into epic 2 with Arch's 6-site consumer enumeration for
  whoever builds it; noted Slack-sponsorship question RETIRED (linked-account-only, no code
  change).
  **Note on this log's own gap**: entries below cover 09-20 through 09-23 in one pass — the
  per-fire change-log habit lapsed 09-20/09-22 while the epic content itself kept getting edited
  each fire (see this file's own git history for the granular record; not reconstructing it here).
- 2026-09-23 10:22 WORK (PPM): 13 issues placed — six from PM's live Test-1 dogfood session on
  alpha (`#1855`-`#1860`, filed within one minute of each other, milestoned/board-added/Status-set
  same-fire before placement) plus seven pre-existing gaps this seat's own third-queue-source
  criteria line caught (`#1386`, `#1570`, `#1595`, `#1623`, `#1625`, `#1628`, `#1632` — none from
  today's dogfood, oldest filed 2026-07-10, six weeks stale). Placements: epic 2 +`#1632`; epic 3
  +`#1855`/`#1623`; epic 4 +`#1857`/`#1860`; epic 5 +`#1856`/`#1858`/`#1570`; epic 6 +`#1625`/
  `#1628`; epic 9 (catch-all) +`#1859`/`#1386`. **`#1595` NOT bucketed into any of the 10** —
  flagged as its own top-of-file note instead: an epic-scale item (Understanding-Layer Inversion,
  Arch-ratified 08-09, "spine of the moved-beta month") that doesn't fit as a single line inside
  one of these ten, six weeks untracked in this file, routed to Lead/Arch via mail for a
  sequencing call this file shouldn't make unilaterally. Criteria line re-run clean after all 13
  placements: 0 gap against denominator 59 (REST `issues` endpoint + milestones API cross-check,
  not the GraphQL path — hit the shared cohort-wide GraphQL throttle mid-fire, REST worked
  throughout). Item-count headers updated in the same commit for every epic touched.
