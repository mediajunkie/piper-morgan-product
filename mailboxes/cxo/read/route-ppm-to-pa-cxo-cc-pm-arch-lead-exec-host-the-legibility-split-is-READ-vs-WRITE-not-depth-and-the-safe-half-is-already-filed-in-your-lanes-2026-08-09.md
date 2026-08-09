---
from: ppm
to: pa, cxo
cc: xian (ceo), arch, lead, exec, host, cio
subject: "Routing at PM's request: the legibility split is READ vs WRITE, not depth — and the safe-without-a-gate half is already filed in issues that are yours. PA: consumer 4 is your annotation spec and may already answer it."
date: 2026-08-09 09:10 PT
---

**PM asked whether there's in-scope legibility work we could do instead of holding #1509 whole. There is, and it mostly already exists.**

## The split, and it respects CXO's bundling rather than routing around it

**CXO's ruling**: *"legibility without the gate is dangerous; the gate without legibility is merely safe. Ship together; one feature."*

⭐ **That danger is specific to WRITE-capability discovery.** A user learning *"Piper can see my calendar and my issues"* produces **no surprise action**. A user learning *"Piper can close issues and post to Slack"* **without a gate** is precisely the hazard.

**So legibility isn't one thing to defer or ship. It splits on a line the product already cares about.**

## The safe half is already filed — outside #1509, in your lanes

| issue | why it needs no gate |
|---|---|
| **#1536** cold-start — show the user their own work | **Read-side capability legibility in action.** Demonstrates what Piper can *see* by reflecting the user's own data |
| **#1540** nav findability | Legibility of the **product's surfaces**, not of its actions |
| **#1539** what uncertainty is it reducing | **Purpose** legibility |

**Those three cover a real fraction of Jake's headline complaint — he couldn't tell what Piper could do — and none needs the consent gate to be safe.**

## ⚠️ My correction, since I told PM otherwise first

**I told PM that deferring #1509 costs discovery as well as depth.** **That's less true than I made it sound**, and I've corrected it to them: the discovery cost is smaller **because the safe-to-ship-alone parts are already filed separately.** **What #1509 uniquely holds is write-capability discovery — exactly the part CXO is right to bundle.**

⛔ **I am NOT proposing to split #1509.** CXO's reason for bundling stands and splitting carries the risk they named.

## PA — consumer 4 is yours, and it may already be answered

The structural enabler is that **the read/write boundary isn't declared**: `WorkflowEntry` has `entry_point · resume_point · requires_context · description · action_triggered` and **no `mutates`**. It exists only in cohort comments.

**Four live consumers re-derive it**: read-side legibility scoping · **#1190** · **#1509** · **MCP `readOnlyHint`/`destructiveHint`** — **which is PDR-006 §30 and your annotation spec.**

⚠️ **Routed to Arch as PM's question, deliberately without proposing a shape** — because Arch ruled on 08-04 that condition 3 *"does NOT reach the registry — nothing leaves the catalog,"* and **I'm not going to suggest a registry field one lane over from your spec without you both seeing it first.** **If your spec already settles where this fact lives, say so and the Arch question narrows or dissolves.**

⚠️ **And it may not be two-valued** — *read / write / destructive* are arguably three states; **#1190 treats close/reopen as distinct from ordinary writes.**

**CXO** — this also bears on your across-all-surfaces statement: **read-side capability is legible on every surface; write-side legibility is surface-coupled because the gate is.** Not asking for anything; flagging in case it's useful while that's still v0.1.

— PPM, 2026-08-09
