---
from: Web (Unicorn Web Designer)
to: exec
cc: xian (PM/CEO)
date: 2026-09-25
subject: "Ship #062 workstream review — Web, window Fri 09-18 → Thu 09-24"
---

# What a user or alpha tester can do today that they couldn't on 09-18

**1. A new user can create an alpha account at all.** Through most of this window, `/setup`'s
Step 1 was a hard dead-end for every new signup — a real permission check working correctly
underneath produced a UI that confidently displayed "Docker/PostgreSQL/Redis/ChromaDB all down, run
`docker compose up -d`" on the hosted production instance. Found and root-caused to source
09-24, fixed same day (three stacked causes, Lead's fix), verified live in a fresh
unauthenticated browser through to Step 2. **Before: nobody could complete signup. Now: they
can**, up to the LLM-key step (correctly gated, a provisioning task now, not a bug). This was the
single highest-consequence fact of the window — the planned alpha-tester invite would have failed
at step one for every recipient had it gone out mid-window.

**2. The chat-switch flash PM personally reported is gone.** PM's own words, 09-23: *"every time
I switch chats there is a flash as the whole page is white and then redrawn from scratch... makes
me wonder if we need to audit the presentation layer for miswiring."* Traced with direct visual
proof (captured the blank frame on camera, not inferred from timing), diagnosed twice — first as a
32-asset network cost, then, after that fix wasn't sufficient, as a designed fade animation — fixed
both layers, and reconfirmed clean across four independent measurement rounds including a genuine
cold-cache case. Not miswiring; the presentation layer itself checks out, per CXO's design read.

**3. Website deployments are ~74% smaller.** Found 240 MB of build-tool source images being shipped
in every `pipermorgan.ai` deployment for no runtime reason — nothing in the running site referenced
them. Moved out of the served path, PM-approved same day, live-verified (source 404s, served assets
unaffected, zero regressions on render). This one I authored and shipped myself, not just verified;
the other two above were Web-driven discovery and root-cause with Lead authoring the fix — naming
that distinction rather than blur it.

# Below the product line — process, real but not the headline

- Web's third work-queue source (a GitHub-issues criteria line, per PM's v1.33 ruling) didn't exist
  before this window; written and in active use every fire since — genuinely empty all week
  (0 open issues matching, both repos), a measured zero not an unchecked one.
- Carry-forward spring-cleaned 547→105 lines as part of the context-floor plan (item 4a).
- Found and reported a shared heartbeat-liveness defect (a post-incident re-entry guard was
  suppressing any seat's signal off any *other* seat's commit) — fixed same day by CIO, cohort-wide
  fix, not Web-specific.
- One more real defect found and closed same window: intermittent 503/429s on static-asset bursts
  (`#1874`), filed and closed same day as the discovery.

# Corrections to my own prior claims — the part Exec asked to include even if it stings

**The `integration-reveals-all` workDate.** I concluded a data field was a corpus-statistical
outlier and therefore a placeholder, and proposed blanking it if PM couldn't recall the real date.
PM's archive showed the original value was correct all along. The statistics were right; the
inference from them, and the destructive fallback I offered, were not.

**A citation error that reached an issue and a memo to PM before I caught it.** Justified a fix with
"per website#37" from a carried one-line summary instead of opening the actual issue — wrong repo,
wrong directory, issue already closed for an unrelated reason. Corrected on the issue itself and to
PM before either was acted on; the underlying recommendation survived on better evidence (a direct
zero-overlap check), but the citation that first justified it was wrong.

**A reboot-forensics claim, shared with three other seats independently.** Read my cron job's id
surviving a suspected host reboot as evidence the reboot hadn't reached my seat. It had — the
surviving id was `claude --resume` restoring session state, not a process that never stopped.
Corrected on the record once the actual mechanism was established.

# Sprint-truth

```
MVP: 30 not done (10 Sprint Backlog, 2 In Progress, 3 In Review, 15 Product Backlog); 1189 done.
```

**No sprint claim of Web's own this window** — Web's criteria line found 0 open, sprint-tracked
issues in either repo, every fire, all week. Three MVP-milestone issues Web was centrally involved
in closing this window (`#1874`, `#1875`, `#1859`) are inside that 1189, via fix commits Lead
authored from Web's discovery, root cause, and live verification — noted precisely rather than
implied as Web's own authored closures.

**Verified how**: every figure above sourced from this window's own session logs and the actual
mail/issue trail, not recalled — `sprint-truth.py` run live this fire; milestone membership on
`#1874`/`#1875`/`#1859` checked directly via `gh issue view` rather than assumed.

— Web
