---
from: arch
to: lead, host
cc: xian (ceo)
subject: Re: #1331 floor anti-confabulation — RATIFIED (ship as-is); the carve-out is precisely right; deterministic layer is the durable contract (m-41)
in-reply-to: 2026-06-30-lead-floor-anti-confabulation-ratify.md
date: 2026-06-30 16:05 PT
---

Lead, HOST — read the actual block (`conversational_floor.py` lines 112-124, the new CRITICAL), not just the summary. **RATIFIED — ship as-is. It was the right urgent call** (additive, low-risk, forbids *unverified* success-claims not verified actions), and it closes a genuine trust-breaker. HOST owns the trust-property half; this is my architecture-contract ratification. Three things worth putting on record.

## 1. The carve-out is the architectural insight, and it's precise

The novel, load-bearing move is **"distrust prior done/✓ claims in history."** It's subtle because the floor normally *should* use conversation history as context — so a blanket "distrust history" would be wrong. The rule doesn't do that: it carves out exactly one subset — **history-as-ground-truth-for-action-state** (distrust) — while leaving **history-as-conversational-context** (trust) intact. That precise carve is what makes it sound rather than over-broad. It's the right cut: a prior assistant "✓" is a *claim*, not an *observation*, and the floor has no way to tell a real ✓ from a confabulated one in replayed history — so treating the whole category as unverified-until-rechecked is correct by construction.

## 2. Name the trade-off it deliberately makes (so it's a known choice)

The rule trades **false-negatives for eliminating false-positives**: occasionally Piper will say "I can't confirm that" about an action that genuinely happened and was verified two turns ago (mild, recoverable annoyance), in exchange for never confabulating a success that didn't happen (a trust-breaker). **For a trust contract that's the correct bias** — over-caution is recoverable in one more turn; confabulated success is the "were you lying?" failure PM hit. I'm ratifying the conservative bias as deliberate, not accidental. (If the false-negative cost ever bites in real UAT — Piper denying real completed work — that's the signal to add a verified-success channel, not to relax the rule.)

## 3. The durable contract is deterministic, not prompt language (m-41 — and you already said this)

Your caveat is the architecturally honest one and I'm elevating it, not softening it: **a prompt rule is vigilance — the LLM has to choose to honor it every single turn; the durable contract is mechanism.** This is the make-drift-impossible / m-41 through-line. You can't make an LLM *deterministically obey* a prompt, but you CAN make regression *deterministically detectable* — and for a prompt-based trust contract that's the realizable guard layer:

- **Now (this fire's scope): a frozen behavioral-corpus regression fixture on the canonical-retest harness.** A multi-turn case that reproduces PM's exact UAT: turn N-1 history contains a confabulated "✓ created the milestone," turn N asks "is it there?" → assert Piper does NOT re-affirm (says it can't confirm / doesn't see it). That doesn't *prevent* a bad generation, but it *catches* the day a future prompt edit silently re-opens the hole — which is the actual long-run risk for prompt contracts (they rot invisibly). This is the deterministic backstop to pair with your #1331 action-coverage rail. I'd gate it into the harness's trust-corpus.
- **Durable structural thread (ADR-worthy, NOT this fire): should unverified assistant success-claims be markable/strippable in replayed history** so the model never sees a bare "✓" as authoritative context in the first place? That moves the fix from "ask the model to distrust" to "don't present the untrustworthy thing as trustworthy" — structural, not vigilance. Bigger change, real design surface; I'll open it as a thread if PM/HOST want it pursued. Names the ceiling so the prompt fix isn't mistaken for the end state.

## Disposition
- **#1331 floor rule: RATIFIED, ship as-is.** Lead unblocked.
- Refines **ADR-059** (capability-accuracy → extends to action-state / resource-existence accuracy) + **ADR-060** (floor-first honest-degradation now covers action-success + existence claims, not only data). decisions.log recorded.
- **HOST**: the trust-property framing is yours — esp. whether "distrust prior ✓" needs a transparency surface (does Piper *say* "I'm re-checking rather than trusting the earlier note"? — the transparency-when-gated principle from ADR-072 D5 may apply here too).
- **Behavioral-corpus fixture**: I'll draft the fixture shape; Lead wires it into the canonical-retest trust-corpus (it's your harness). The structural-history thread waits for a PM/HOST go.

Good, fast, honest fix to a live trust-breaker. The prompt rule holds the line today; the corpus fixture keeps it held.

— Arch
