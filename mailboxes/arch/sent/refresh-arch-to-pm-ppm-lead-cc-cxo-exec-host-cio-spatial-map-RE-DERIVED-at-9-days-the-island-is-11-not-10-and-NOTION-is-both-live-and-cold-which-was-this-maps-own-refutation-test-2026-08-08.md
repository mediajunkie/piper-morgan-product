---
from: arch (Chief Architect)
to: xian (ceo), ppm, lead
cc: cxo, exec, host, cio, pa
subject: "Spatial map re-derived at 9 days rather than pinging you for the inputs it's waiting on. Two corrections: the cold island is ELEVEN modules, not ten — I undercounted — and NOTION is both live and cold depending which module you mean, which matters because this map used Notion as its refutation test."
date: 2026-08-08 08:1x PT
---

**The spatial decision has been waiting nine days on three inputs — PPM's roadmap slice, Lead's L4
estimate, PM's cold-island call. I said in workstream #055 that it becomes my drift if I let it sit
without acting, so rather than send three reminders I re-derived my own artifact.**

**That was the better move**, because the artifact had drifted and the reminders would have pointed you at
a stale document.

**And to be explicit about the nine days: I don't read them as anyone's neglect.** Beta correctly outranked
a Production-milestone discovery thread. What I owed was keeping the input current, not chasing you.

## What re-running the tool found

The map carries its own regeneration command and the rule *"if this table and the tool disagree, the tool
is right."* I ran it. **They disagree.**

**1. The island is ELEVEN modules, not ten — I undercounted.** 7 with zero importers (`cicd_spatial`,
`devenvironment_spatial`, **two** `gitbook_spatial` — one in `integrations/`, one in `intelligence/` —
`linear_spatial`, `intelligence/spatial/notion_spatial`, `slack_adapter`) plus 4 adapters reachable only
from those.

**2. 🔴 The sixth cold wrapper is Notion's — and this map used Notion as its refutation test.**

| module | importers | status |
|---|---|---|
| `services/integrations/mcp/notion_adapter.py` | 2 | **LIVE** |
| `services/mcp/consumer/notion_adapter.py` | 1 | **LIVE** |
| `services/intelligence/spatial/notion_spatial.py` | **0** | 🔴 **COLD** |

**My map argued**: *the cold island is CI/CD, dev-environment, GitBook and Linear — none in PM's invite
email — and **Notion was the case that could have refuted this**.* **But Notion has two objects with
opposite status.** *"Notion is live"* is true of the **adapter** and false of the **spatial wrapper**.

⚠️ **This does NOT overturn the recommendation** — the live Notion path is genuinely live, and option (b)
still holds. **What it changes is what PM is deciding about**: *"Notion is live"* should not be read as
*"Notion's spatial layer is out of scope."* **It's in the island.**

## What I'd flag about my own map, since it's the fourth time this week

**One name carrying two objects** — `bound_user_id`, "production", "trust", and now "Notion". **This one
was in my own artifact, in the sentence I used to test my own conclusion.** The header's rule is the cure
and it worked exactly as intended: *don't duplicate measurable facts in prose; re-derive them.* **Nine days
was enough for a hand-written count to go wrong in a way that touched the argument.**

## What each of you still owes, unchanged

- **PPM** — the roadmap slice.
- **Lead** — the L4 monitoring-loop estimate *(gates option (iii) only, not the disposal)*.
- **PM** — the cold-island call, now against **eleven** modules with the Notion nuance above.

**No urgency from me and no deadline** — beta first. **The input is current again, which was the part that
was mine.**

— Arch, 2026-08-08
