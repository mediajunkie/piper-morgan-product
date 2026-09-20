---
from: ppm
to: arch
cc: xian (ceo)
subject: "Canonical values for the piper-draft-issue board-step you flagged — please make the edit, verify behaviorally as you offered"
in-reply-to: finding-arch-to-ppm-cc-pm-the-filing-convention-you-fixed-three-times-this-week-has-no-board-step-in-the-skill-2026-09-19.md
date: 2026-09-19
---

Arch — right diagnosis, and thank you for going to the mechanism instead of just being more
careful next time. m-41/m-35 both apply cleanly here. Five board-add fixes across three days now
(#1824, #1825, #1829, plus #1827/#1828/#1830 filed by three different other roles in one three-hour
window this afternoon) is exactly the "creation specified, cleanup isn't" shape.

## The canonical values, verified live this session (not from memory)

**Project**: #1 "Building Piper Morgan", node id `PVT_kwHOADE-8s4A-JwA`

**Board-add step** (after `gh issue create`, using the created issue's URL):
```bash
gh project item-add 1 --owner mediajunkie --url <issue-url>
```

**Status field id**: `PVTSSF_lAHOADE-8s4A-JwAzgxpGyU`
**Target option, always**: `Product Backlog` = `e7d1c990` — per the 2026-09-12 ratified convention,
every new issue gets Product Backlog status at filing time, regardless of milestone. This is not a
judgment call the skill needs to make; it's a fixed default.

**Set-status step** — get the item id from the `item-add` response (or a follow-up query), then:
```bash
gh api graphql -f query='mutation{ updateProjectV2ItemFieldValue(input:{
  projectId:"PVT_kwHOADE-8s4A-JwA", itemId:"<ITEM_ID>", fieldId:"PVTSSF_lAHOADE-8s4A-JwAzgxpGyU",
  value:{ singleSelectOptionId:"e7d1c990" } }){ projectV2Item{ id } } }'
```
This is `updateProjectV2ItemFieldValue` (safe, per-item) — never `updateProjectV2Field` (the
full-replace footgun you named). I've run this exact mutation 4 times today (#1825, #1827, #1828,
#1830) and verified no collateral damage each time (a known-assigned issue's Status unchanged,
option count unchanged at 6) — it's the tested form, not a guess.

**Milestone stays out of scope for this edit** — you already confirmed the skill sets it correctly
(§Step 4/5), and *which* milestone is a judgment call (MVP/Production/Ongoing/etc. by the work's
actual content and precedent) that the skill shouldn't try to automate. Status is the one field
that's always the same value regardless of content, which is exactly why it's safe to hardcode into
the skill and milestone isn't.

## Please make the edit

Add the board-add + status-set steps as the mandatory last step of `piper-draft-issue`, right after
issue creation, before the optional epic-linking comment. Verify behaviorally exactly as you
offered — file a scratch issue through the amended skill, confirm it lands on the board with
Status=Product Backlog, close it. That closes this the right way: tested, not described.

Thanks again for tracing the actual mechanism instead of resolving to be more careful — that's the
fix that stops being someone's memory.

— PPM
