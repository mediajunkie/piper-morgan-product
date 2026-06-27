# Proposal — retire the reflexive PM cc; route PM-attention through Exec

**STATUS: PROPOSED** (PM agreed to the *moderate direction* 2026-06-27; this doc is the concrete shape, pending PM approval-to-circulate → cohort ratification → pilot). Not in effect yet.
**Author**: Exec · **Date**: 2026-06-27 · **Drivers**: PM (xian) + Exec

---

## Problem

PM's `mailboxes/xian (ceo)/inbox/` is hundreds-deep (680+ unread). The reflexive "cc xian" on memos **does not get PM's attention** — it's an append-only graveyard PM doesn't read. Worse, real questions/decisions get buried in cc'd memos and stall the sender until PM happens to reach them directly. The cc has become noise that *masquerades* as "PM informed."

Meanwhile, Exec already IS the attention layer (the cohort-attention board + question-extraction + decision-relay). The cc is dead weight on top of a mechanism that already works.

## Principle

**Exec is PM's attention proxy, not his authority proxy.** Exec routes, triages, surfaces, and relays — Exec never decides in PM's name. PM makes every call; he just makes it from a clean queue (the board) instead of a graveyard.

## The change (moderate — NOT eliminating the inbox)

**Deprecate reflexive `cc xian`.** When an agent has something for PM, it picks an intent instead of cc-ing:

| Intent | Route | What Exec does |
|---|---|---|
| **FYI** (milestone, published artifact, status PM may want to know) | to Exec | folds into the board's awareness section; no PM interrupt |
| **needs-decision** (a call only PM can make; sender is gated) | to Exec | extracts to the board's decisions bucket **and** surfaces directly to PM in conversation; relays PM's answer back |
| **time-critical / personal** (security, external commitment, genuinely urgent) | **direct to PM** (reserved channel) | — (this is the Janus "escalate directly on time-critical" rule, preserved) |

**What is preserved (deliberately — this is why it's moderate, not radical):**
- **The xian inbox stays** — as (a) the durable record ("PM was informed of X" via sent-mirrors + git history remains provable) and (b) the escape hatch. Exec is a single point of failure (it has stalled — watchdog flagged it 6/27); PM must never lose the ability to dig directly. We de-emphasize the inbox; we don't remove it.
- **The time-critical direct channel stays.** The rule is "stop reflexive cc," not "never contact PM."
- **Exec's bidirectional duties** (now standing, PM-confirmed 6/27): pull = extract PM-questions from the cohort; push = relay PM's in-conversation decisions to gating agents.

## Pilot (so we don't flip a cohort-wide habit blind)

1. **PM approves this shape** → Exec circulates to the cohort for ratification (explicit responses required, per ratification discipline).
2. **2-week pilot**: `cc xian` becomes *discouraged/optional*, not yet removed. Agents try the FYI/needs-decision/time-critical routing. Exec runs the board as PM's single surface.
3. **Exec watches for fall-through** — anything that needed PM and didn't reach him. Reports weekly.
4. **If clean → ratify + codify** in CLAUDE.md (Mailbox Discipline) + `branch-worktree-mailbox-discipline.md` + role briefings, and make `cc xian` the exception not the default.
5. **Only after the proxy has earned it** do we revisit PM's stronger "eliminate the inbox entirely" idea.

## Open question for PM

Approve this shape to circulate for cohort ratification? (Or adjust the taxonomy / pilot length first.)
