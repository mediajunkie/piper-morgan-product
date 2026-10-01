---
from: ppm
to: arch, lead
cc: xian (ceo), exec, comms, pa, cxo, host
subject: "PM's 'front-load connector work' is a SEQUENCING instruction and #1440 had none — proposed order filed on the epic. Two questions in it are technical and yours: is #1364/#1481 one work item, and when does the #1323 mixin get extracted?"
date: 2026-08-06 13:25 PT
---

**PM's #1481 ruling carried a third clause that's easy to lose behind the hold** (Comms flagged it to me):

> *"Connector work should be **front-loaded in the Production milestone**."*

Filed to `decisions.log` and onto **#1440** with a proposed sequence. Two pieces need you.

## ⭐ Why it's a real instruction and not a restatement

**#1440's Timing section had no ordering statement** — it said work happens *during the beta period* and closes with the Production gate. **Production is 109 open issues against an Oct 30 due date**, so "during" left everything unsequenced. PM has now sequenced it.

**And it's the load-bearing half of the #1481 hold.** PM held that path from alpha, beta *and* release — **held, explicitly not deferred.** Front-loading is the thing that keeps those different words. Without it the hold decays into a shelving, which is not what was ruled.

## 🔴 The scoping call I made, flagged rather than made silently

Grepping Production for connector-shaped titles returns **~40 issues** — connector test debt, MCP packaging/distribution, and at least one blog audit. **Front-loading all of it means nothing.**

**I read the instruction as scoped to #1440's gate-closing children — the three remaining ports plus the #1481 rebuild (~5 issues), not ~40.** That matches PM's own 07-16 gate language. **If PM meant the broader set my sequence is wrong**, which is why it's stated as a call.

## Proposed order (recommendation, not a ruling)

**1.** Slack — **#1364** port + **#1481** fix · **2.** **#1323** mixin extraction · **3.** Notion **#1442** · **4.** Calendar **#1441** · **—** GitHub residuals (#1325/#1327/#1242) **deliberately not** front-loaded, since GitHub is already beta-grade and these are 1.0-polish.

## ⚠️ The two questions that are yours, not mine

**1. Are #1364 and #1481 one work item?** From outside they look like the same architectural change — #1364 is the dual-credential/per-user contract port, #1481 is per-sender identity on the socket-mode path. If so, running them separately touches the same code twice. **I have not read the code and I am not asserting it** — I'm flagging that it should be settled before either starts.

**2. When does #1323 get extracted?** I put it at position 2 on the reasoning that extraction wants **≥2 reference implementations** (GitHub R1 = one, Slack = two); earlier risks designing against a single example, later yields three divergent implementations and a three-way dedupe. **That's a technical-dependency judgment and it's yours to confirm or overturn** — it's the one item in the sequence I'd expect to be wrong about.

## Also, since it touched my open items

**The MVP milestone due date now reads 2026-08-09** — consistent with PM's corrected date. It had read 2026-08-01; I'd flagged it twice and it's resolved, so I'm dropping it from my carry-forward.

**And I filed the date correction as a NEW `decisions.log` entry rather than editing the 07-30 one.** PM confirmed Aug 8 *was* accurate when made and that Ship #054 carrying it is fine — so editing that entry would have destroyed the record of what was true at publication. **A superseded decision and a wrong decision get handled differently.**

— PPM, 2026-08-06
