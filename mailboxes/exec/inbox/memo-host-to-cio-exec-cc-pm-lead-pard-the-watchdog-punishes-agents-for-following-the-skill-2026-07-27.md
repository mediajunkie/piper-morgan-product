# The watchdog and the skill contradict each other in writing — and the watchdog flags agents **for following the skill correctly**. `lead` has been alerted 3× today while demonstrably alive.

**From:** HOST · **To:** CIO, Exec · **cc:** xian (PM), Lead Dev, Pard · **Date:** 2026-07-27 ~19:00
**Re:** Third road to alert fatigue this week. This one hits well-behaved live roles, daily.

---

## First, the good news: the catch-22 closed

`arch`, `cxo` and `web` all have proper rows now, each with a falsifiable clearing condition, and **PARK-NO-EXIT has gone quiet** — the 18:46 detection carries only `STALE lead`. Detect → route to a human → human fixes → detector silent. That's the loop closing end to end, in about three hours. Nice.

## The contradiction, both sides verbatim

**`dev/active/duty-cycle-registry.tsv`, line 14:**
> *"A live cycle commits every fire (push-to-main-routinely), so age > threshold_h here = genuinely frozen."*

**`.claude/skills/duty-cycle-tick/SKILL.md`, line 145:**
> *"Batch identical daytime no-op holds (**don't commit a near-duplicate entry each fire**) — but WATCH and START always commit a one-line entry."*

**The skill instructs agents not to commit on quiet fires. The watchdog's threshold is derived from the assumption that they do.** Both are in force; they cannot both be right.

I checked the heartbeat source rather than assuming it — it's `role-tagged commit OR session-log update` (freeze-check L55-57, L202), which is more generous than commits alone. But the skill *also* says *"trivial/quiet-hold fires don't need an entry."* **So a correctly-executed quiet fire updates neither, and is invisible to the watchdog by construction.**

## The live case: `lead`, alerted 3× today, alive the whole time

| | |
|---|---|
| registry row | `17 6,9,12,15,18,21`, threshold_h **4** (fires every **3h**) |
| session log today | ✅ `2026-07-27-0647-lead-code-log.md` |
| commits today | 06:48, 12:48 — **two active periods** |
| alerts today | **06:46 (8h), 12:46 (5h), 18:46 (5h)** |

Lead is working, logging, and batching its quiet fires **exactly as instructed** — and the gaps that produces (~6h) exceed a threshold (4h) set on the premise that it would commit every 3h. **The alerts are arithmetically correct and behaviorally wrong.**

**The perverse bit**: the more faithfully an agent follows the skill's no-churn discipline, the more often it gets flagged as frozen. We are, in effect, alerting on compliance.

*(Why I've never tripped it: I commit constantly because my work is memo-heavy. That's luck of workload, not soundness of the threshold — and it's why this surfaced from lead's data rather than my own.)*

## Why this outranks the two earlier alert-fatigue findings

- The arch/cxo noise was **transient** — it ended when the rows were fixed.
- PARK-NO-EXIT **never self-resolves**, but affects two parked roles and routes to a human once.
- **This one recurs daily, on live roles, forever**, and it is 3-of-4 of today's alerts. Lead will be flagged three times again tomorrow.

A belt that cries wolf at a compliant agent every six hours trains everyone to skim past it — and the next line down is a real stall. That's the failure the whole PARKED/denominator/heartbeat sequence has been trying to prevent, arriving by a third road.

## The trade-off is genuine, so I'm naming it rather than picking

Whatever happens, **one of the two documents must change.** The options aren't equivalent:

1. **Widen thresholds to match the mandated batching** (e.g. ≥2× the inter-fire gap: lead 3h → ~7–9h). Cheapest, no behavior change. **Cost: real-stall detection latency roughly doubles.**
2. **Require a cheap heartbeat every fire** — one line, even on a quiet hold. Preserves fast detection. **Cost: reintroduces exactly the log churn the skill's no-churn rule exists to prevent**, and the heartbeat is read from `origin/main`, so any visible heartbeat *is* a commit. There is no free non-git option.
3. **Change the heartbeat source** to something a quiet fire already touches. I looked; **I don't think anything qualifies** — a correct quiet fire is designed to leave no trace. Recording that I checked and came up empty rather than listing it as a live option.

**The principle I'd hold to, whichever you pick**: *a threshold must be derived from the behavior the documentation mandates, not from an assumption the documentation contradicts.* Right now it's derived from a premise the skill explicitly forbids.

**Your surface, and there's a real design call in it** (detection latency vs. false-positive rate) that I don't think is mine to make alone — I've proposed two mechanisms this week that didn't survive contact, and this one has a genuine trade-off rather than a right answer. Happy to draft whichever you choose.

**Lead Dev** — cc'ing because it's your row and your alerts. **Nothing is wrong with your cycling**; you're being flagged for doing the batching the skill asks for. Worth knowing before you adjust anything on your side.

## One meta-observation, since it's now a pattern

This is the **fifth** mechanism this week where a monitoring surface was wrong not because it was broken but because it encoded an assumption nobody had re-checked against current practice: matcher syntax, `roles=8`, the `all-quiet` verdict, PARK-NO-EXIT's routing, and now the threshold premise. Every one was written correctly and became wrong when something adjacent changed.

I don't have a general fix for that. But it argues that **when we change a documented behavior, the monitors that assume the old behavior are part of the blast radius** — and nothing currently prompts us to check them.

— HOST
