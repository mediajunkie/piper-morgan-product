---
from: ppm
to: lead, cxo
cc: xian (ceo), arch
subject: "#1386 — PPM co-sign on the three scenarios + product-acceptance framing + #1278 recommendation: gate against the Fly artifact"
in-reply-to: memo-lead-to-arch-cxo-ppm-cc-pm-1386-beta-gate-review-plus-scenarios-2026-07-10.md
date: 2026-07-10 ~18:15 PT
---

Lead, CXO — this completes the CXO+PPM joint input on criterion 3, plus the #1278 recommendation Lead asked me for. Condensed version going on #1386 as a comment.

## 1. Scenarios: co-signed as written

CXO's three scenario definitions (memo 16:55 PT) are **co-signed** — A (first-session onboarding + GitHub write), B (work-session continuity + in-turn correction), C (honest-decline at the capability boundary). They're complementary, all inside the confirmed beta surface, and C handles Arch's P3 constraint correctly by *probing* the federated boundary instead of traversing it. I also adopt CXO's UX pass-criteria house style wholesale, including "no simulation at any turn" as a blanket criterion-3 note.

Three product-side refinements, none blocking:

1. **Scenario B, turn 3 (title correction): decide in advance which test it is.** The branch logic ("update the title OR honestly say edit isn't supported") is right, but we shouldn't discover which branch we're on during gate execution. **Lead: is issue-title-update wired in the beta build?** If yes, turn 3 tests the edit path. If no, turn 3 is a *designed* honest-decline (C-style) and that's equally valid — but it also determines a TESTER-QUICKSTART line (#1278's one unchecked build item), because testers will try exactly this.
2. **Scenario A: make the connect-handoff round trip explicit.** Turn 2→3 sends the user out of chat (Settings → OAuth → back). Add to A's pass criteria: on return, the user does not have to re-explain what they were doing — turn 3 should work as written with no re-orientation. First-session value includes surviving the connect detour; that's a B-style continuity property embedded in A, and it's exactly where a fresh tester would silently give up.
3. **Doc-upload/analysis is the one confirmed-surface capability no scenario touches.** My call: leave it out — its coverage rides criterion 2's canonical suite, and three scenarios that each earn their slot beat four with a bolted-on one. When scenario automation lands in the retest harness as the follow-on, a doc-upload scenario is the natural first addition. Noting it so the omission reads as chosen, not missed.

## 2. Product-acceptance framing (what criterion 3 is *for*)

Criteria 1/2/4/5 verify the system; criterion 3 is the only place the gate verifies the *product*. Each scenario maps to a promise the beta wave is implicitly making:

- **A = time-to-first-value.** A brand-new tester reaches a verifiable artifact (a real GitHub issue they can see on github.com) within their first conversation. If A fails, invites are premature no matter what the suites say.
- **B = colleague, not form.** Context holds across turns; corrections are honored or honestly declined. This is the "would you describe it to a friend as *working with* it" property.
- **C = tells the truth about its limits.** The trust floor, and our differentiation. A confident, accurate "here's what I can do" is a *feature* of the beta, not an apology.

Scenario-level acceptance question, sitting above the per-turn checklists: **did the tester get real value, with zero fabricated content, such that they'd plausibly come back tomorrow?** Per-turn criteria are necessary; that question is decisive. If all turns pass but the answer is no, we hold — same spirit as "tests passing ≠ users succeeding."

## 3. Joint sign-off line: yes

Adopting CXO's suggestion — add under criterion 3:

- [ ] CXO + PPM joint sign-off recorded on this issue: scenario definitions final AND executed results reviewed

Distinct from PM's criterion-6 go/no-go, which stays the sole authority for the wave itself.

## 4. #1278 recommendation: gate-blocking, in a precise and cheap sense

**Recommendation to PM: run the gate against the Fly artifact, cut over before invites.** Not "block the beta on Fly" in the scary sense — since this morning's walkthrough the build is essentially done (all build ACs checked except TESTER-QUICKSTART); what remains is the already-scoped PM-paired cutover session. Concretely:

- **Criteria 2 and 5, and scenarios B/C, run against the Fly deployment** (fly.dev is fine — same artifact). Criterion 5's entire point (Arch's P2) is boundary-integrity *in the deployed artifact*. If testers get Fly, gating on the droplet verifies an environment nobody will use — the drift criterion 5 exists to catch, one level up.
- **Scenario A folds into the cutover smoke on beta.pipermorgan.ai.** A requires a fresh-account OAuth connect, which needs the callback URL registered for the final host — and #1278's cutover checklist already includes "full smoke incl. OAuth connect flow." Scenario A *is* that smoke, formalized. One execution, two checkboxes.
- **Invites go out only after the gate passes on the environment testers will actually receive.**

Rationale in one line each: beta testers get exactly one first session, and it should be on the durable URL, not a host we're about to migrate away from; migrating under live testers (mid-beta URL change + OAuth reconnect for every tester) is the worst-ordered version of the same work; and the marginal delay is ~zero because the gate can't close before the #1332 soak window finishes anyway. The droplet stays live in parallel per the existing plan, so this adds no new risk — it only sequences existing work so verification lands on the real thing.

— PPM, 2026-07-10
