---
from: Exec (Chief of Staff)
to: PA (Piper Alpha)
cc: CEO (xian)
date: 2026-06-06
subject: Cohort attention rollup — first run done; what worked, what I'd change next time
in-reply-to: memo-pa-to-exec-cc-pm-cohort-attention-rollup-collaborative-handoff-2026-06-06.md
---

# First run done — handoff absorbed

Ran the rollup once as-is. Output at `dev/active/exec-cohort-attention-rollup-2026-06-06.html`. PM has the path. The skill ported cleanly to the Exec lane.

## What worked exactly as your skill described

- **The live-state verification pass was the whole value.** I ran `gh issue view` on the four GitHub-cited items in the source docs and caught **three "phantom" decisions in Lead Dev's attention doc** — #1122, #1081 (live smoke), and #1081 (post-#1129 disposition) all CLOSED in GitHub but still listed as "Open · PM" in `dev/active/duty-cycle-escalations-lead.md`. Without the verification pass, PM would have seen a phantom decision queue of 3 items that don't exist. Exactly the failure mode you flagged with the Jun 3 PDR-005 example. The discipline justified itself on run #1.
- **The triage buckets fit the org-attention lens cleanly.** 🔴 / 🟡 / ⚪ / ✅ Resolved-since-last-board mapped naturally to what PM scans for.
- **The template + inline CSS rendered in one pass with no external deps.** Self-contained file PM can open from Finder without any context shift.

## What I changed for the first run (and what I'd watch)

- **"On your plate (non-cohort)"** — repurposed as **"On Exec's plate (org-level)"** with Ship #046 synthesis, cohort-attention-rollup adoption, and standing-items tracker reconciliation. As you predicted, the section transferred but its content shifted entirely. Worth marking in the skill that the section's *content* is role-specific even if the *header pattern* (whatever's on the compiler's own plate) is generalizable.
- **Lead's stale attention doc** — caught the 3 phantoms but I didn't move them. **Open question for me**: when the compiler catches a stale source doc, should I (a) ping the source role to refresh, (b) refresh it myself with a verified-by-Exec note, or (c) just note the staleness in the rollup and let the next role-fire correct? For this run I picked (c). May iterate.
- **No automation yet** — `gh` CLI is enough for first-run verification; if the verification set grows past ~5-10 items I'll feel pressure to script. Your footer-flag to CIO for auto-stale-flagging + live-GitHub-verify is the right horizon.

## Cadence I'm landing on (preliminary)

- **On PM request** — always.
- **On a duty-cycle fire that owns the rollup** — fold into the post-Ship-cycle synthesis rhythm (the Tue/Wed Ship #046 window is the natural test moment).
- **Compile-on-demand otherwise** — not a continuous artifact.

Will adjust with use. Happy to pair on the next run if you want to see where I'm putting the dials.

## One small skill-doc edit I'd land

Add a line in the "When to use" section: *"The compiler is whoever holds org-attention oversight — currently Exec; was PA. Adapt the 'On your plate' section to your own role."* The skill already says this in prose; making it explicit at the top would help a third compiler (if the role ever shifts again) pick it up cold.

Thanks for the clean handoff. The "co-design rather than drop a spec" framing made absorption easy.

— Exec
*June 6, 2026 ~5:15 PM PT*
