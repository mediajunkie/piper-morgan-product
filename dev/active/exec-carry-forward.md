# Exec Carry-Forward

**Updated 2026-08-31 21:1x PDT (STOP)** — PM-gated section re-derived from live carry-forwards.
**The header date moves with every edit**, which is the actual content of the rewrite-whole rule: the
failure was never patching, it was a frame that stayed still while the content moved.
**Session log today**: `dev/2026/08/31/2026-08-31-0902-exec-code-log.md`
**Role**: Chief of Staff (Exec) · Amber · Model A worktree · branch `claude/exec-cycle` · upstream
`origin/main` (verified correct) · cron `32 8,20`, job `b55d60bf`
**⚠️ Arm-date NOT recorded** (gap found 08-30). Earliest evidence of this id is 08-29 → worst-case
expiry **~09-05**. **Rotate proactively at the 09-03 START** rather than discover absence. Record the
arm-date at every future re-arm — `CronList` does not return creation time, so it is unrecoverable.

---

## 🔴 STEP ONE, EVERY FIRE — PM DIRECTIVE 2026-08-28

**Run `scripts/duty-cycle-freeze-check.sh` at the top of every fire, before mail, before anything.**

⚠️ **NOT `cohort-freeze-detect.sh`.** Two similar names, different questions:
- `cohort-freeze-detect.sh` — *is the COHORT frozen?* rc=0 whenever ANY role is alive. **Structurally
  incapable of reporting an individual dark role.** This is what I used to run.
- `duty-cycle-freeze-check.sh` — *is any INDIVIDUAL role stale?* Per-role hours + missed fires against
  each row's own cadence. **This is the one that answers PM's question.**

**Earned**: arch/cio/host sat dark 30–33h and I reported Ship #058 as "7 of 10, three haven't filed" —
framing three dead sessions as slow correspondents. **Always state the denominator** ("11 of 11 rows,
0 stale"), never "all clear."

⚠️ **Known blind spot, not fixable at this layer** (CIO, 08-29): a session parked on a **modal
rate-limit dialog** is ALIVE and produces output-silence — identical signature to death. Every
instrument we own reads git/filesystem state, so none can distinguish them. PM unsticks via tmux.
Open question routed to PM: is there a non-interactive mode that makes the rate-limit case **fail**
rather than **prompt**? A session that dies cleanly is visible to everything we have.

## 🔴 ROLLUP RULES — PM DIRECTIVE 2026-08-29 (now skill Step 2b)

1. **The board IS the flag.** Nothing counts as flagged for PM unless it's on the rollup. A commit
   message saying "flagging to PM," a 🟡 in a carry-forward, a memo's closing line — none of these are
   flagging. *(Earned: the Apache copyright line sat 16 days inside a commit message. PM ruled in
   seconds once surfaced.)* **Step 1's source set is a floor, not a ceiling** — sweep for items
   flagged in passing anywhere.
2. **Every decision item carries a FIRST-SEEN date; >~1 day unaddressed ESCALATES.**
   ⭐ **The reasoning inverts the natural read**: an aged item usually means *the board
   under-described it*, not that PM deprioritized it. The docs-tree plan waited 18 days and PM ruled
   instantly once told it was a yes/no about one directory. **Age is a signal about MY framing —
   re-describe before re-listing.**

## Active threads

| Thread | State | Next |
|---|---|---|
| **Ship #058** | v0.1 drafted, audit-clean, delivered | PM voice pass **Tuesday** (PM's call, stated). Publish **Wed 09-02**. ⚠️ Comms + Docs face a **compressed same-day turn** — give Comms a Monday heads-up. |
| **PM/Lead test round** | **8 of 16 done, paused 08-29**; pre-classifier narrowing + fix batch deploying | ⚠️ **Split denominator**: if the deploy landed between test 8 and 9, the halves measure different systems. Don't let "16 tests" read as one run. **Take results from Lead's or PM's account — do NOT infer which items the 8 covered.** |
| **Architectural review** | Ran 08-29. ESSENCE.md v0.1; PM ratified: Inversion flips live on chat, **all NEW build → MCP/BYOC**, **web-chat = maintenance mode** | Trifecta reads due **Wed 09-02** — CXO and PPM both filed **08-30, early**. CXO raises a structural tension between commitments 3 and 6. Arch synthesizes disagreements to PM by **09-03**. My workstream state rides Arch's weekly review; **methodology-core disposition = workstream B3**. |
| **In Review bucket** | 27 items, split 3 ways and briefed to Lead | Web verified 4 through the real UI (2 closable, 2 XSS escaped-no-exploit). Lead has the 6 deterministic ones. ~12 need PM's live conversational testing. |

## PM-gated, on the board — re-derived live 2026-08-31, not carried forward

★ **First application of PM's aging rule.** The rule says an aged item usually means *the board
under-described it*, so the work is **re-describing, not re-listing**. Doing that surfaced that most
of last week's queue resolved — and that two items I'd have re-listed were already closed.

| Item | Age | State |
|---|---|---|
| **BYOC/marketplace listing copy v4** | 1d | 🔴 **WITH PM.** Converged 08-30 after PPM answered a 20-day-open question by checking #1440's actual contract: "issues" and "documents" hold, "conversations" and "people" don't (no population mechanism for "people" exists at all). CXO narrowed "documents" to Files-page PDF uploads only. Web verified live with the browser-lane account. **Carries a live condition**: if #1659 doesn't land before the listing ships, cut to "issues" alone rather than let a stranger's first `.txt` upload error out. |
| **Probe B — API spend** | ~1d | 🔴 **Small, concrete, with a real downstream.** Do situation-shaped tool names route worse than object-shaped? **B's answer decides which of the 12 canonical tool names we pick**, so it precedes the catalog rather than sitting beside it. PA correctly refuses to extend PM's Probe-A "yes you may" silently. |
| **Trifecta's three PM decisions** | new | Arch synthesizes to PM by **09-03**. The one in PA's lane, in Arch's own framing: *"a question about what beta IS, which is yours."* Arch and PPM both lean option (a). |
| **BYOC marketplace NARRATIVE (blog piece, NOT listing copy)** | 🔴 **23 DAYS — ESCALATES** | Comms drafted three angles 08-08 and asked PM to pick A/B/C **or say deprioritize**; no answer since. Comms' steer: B (*"distribution is a product decision, not a marketing one"*), A as an optional on-ramp. **Two distinct BYOC items are on this board — this is the blog narrative, NOT the listing copy v4 above.** Comms' own note: their standing-items file kept the pre-correction framing the whole time, so it read as "still gathering direction" when the real state was "waiting on a pick." Surfaced by CIO's new aging audit. **A deprioritize is a perfectly good answer.** |
| **Beat 4 vs Ship #058 — Tuesday collision** | new, but decide EARLY | Sep 1 is Beat 4's scheduled pubDate (`status=drafted`, needs PM voice pass + art) — **the same Tuesday morning PM committed to Ship #058's fresh-writing pass.** One voice pass, two claims. Slipping Beat 4 is fine and likely; **the failure mode is PM triaging under time pressure at 9am between two half-done drafts.** Options: Ship first + Beat 4 slips a day or two, or Beat 4 first + Wednesday's Ship publish gets tighter. |
| **"Flip it"** | — | Not waiting on PM — **it's a trigger PM holds.** Lead has Arch's ratified staged plan loaded; PM is mid-round at 8 of 16. |

**Closed since the last board, verified rather than assumed** (a dropped item is not a resolved one —
Comms had rewritten their carry-forward, so I checked their logs): Beat 6's quote — closed 08-30, PM
confirmed "date" was correct, PM's own original typo · insight pool — PM reviewed with Comms 08-29 ·
plugin `license` — answered `Apache-2.0` · docs-tree flattening, CIO's four, GitHub adapter,
CXO floor/ethics + §4 column — all ruled 08-29/30.

**PM availability**: longer response cycle **Mon 08-31** — vacation-ish. **Voice pass Tuesday**,
publish Wed 09-02. Nothing above is worth interrupting a vacation for; all of it is fresh.

## Standing rules for this file

★ **REWRITE WHOLE, NEVER PATCH.** Adopted 2026-08-30 after this file went **36h stale with a header
claiming 08-27** — while I was asking Lead to fix exactly that in theirs. Lead's diagnosis, which is
the right one: *"my updates were surgical string-replacements on specific rows — each edit true, none
touching the stale frame around them."* **A partial update reads as a full one to every later reader,
including me.** Rewrite-at-STOP makes freshness one atomic act.
Freshness pass belongs in START and STOP, not in intent.

## Standing corrections to myself — all four from 08-28/29, same family

**Every one was a claim put in front of PM without running the check that would have settled it, in
the same turn.**

1. **Put CXO's floor/ethics watch to PM as a live ask** — PM had ratified its split 13h earlier. An
   *asks* section is a live-state claim by definition, even inside a window-scoped report.
2. **Called #1656 an unstarted CRITICAL blocker with three issues behind it** — it was fixed the day
   it was filed. I had *just* proven the board unreliable, then read four more rows off it and built
   a narrative from titles.
3. **Read causation into "they were ALSO disconnected from remote control"** — PM never claimed the
   event caused it. It had been off for a week. The word "also" carried a reading I supplied.
4. **Reported "(no LICENSE file at repo root)"** — false. `ls LICENSE* COPYING*` aborted in zsh on the
   unmatched glob and my `||` fallback fired. **A fallback branch triggered by a command failure is
   indistinguishable from a real negative result.** Check the exit path, not just the output.

## What I own that others rely on

Cohort attention rollup (skill + artifact) · Ship kickoff → internal report → public draft → publish
· cross-project relay (real recipient in `to:`, cc exec, deliver to `exec/inbox/`; I relay into the
sibling repo) · recording PM's in-conversation rulings durably — **`decisions.log` + the affected
role's inbox, not just chat.**

## Verified this fire

CIO's `cohort-position.sh` "Last Active" inversion — **I found it 08-29, CIO fixed it same night, and
I re-verified behaviorally rather than accepting the memo**: all four sampled roles now match ground
truth exactly, and the column names its own source. CIO disclosed the residual limitation
(untagged commits still won't match) rather than hiding it.
