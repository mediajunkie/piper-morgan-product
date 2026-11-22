# 2301 part 2 screen: every reply (Lead, 2026-11-22)

72 live replies from `ConversationalFloor.respond` on branch `lead/2301-floor-part2`, the testers' neutral base with the reply guidelines, a context with four projects, GitHub not connected, and the todo keys already removed (part 1). Six samples a row. Cost $0.2140.

Arms: **control** (part 1 only, no line); **A** (CXO's line, as built); **B** (A with the standing STATUS note left out; measured only, not built).

Marker fixed before the run: a reply fails if it contains `todo`, `to-do` or `task` in any case.

| arm | N3 with todos | T4 with todos | T6 with todos | N3 none |
|---|---|---|---|---|
| control | 6 of 6 clean | 5 of 6 clean | 6 of 6 clean | 6 of 6 clean |
| A | 6 of 6 clean | 6 of 6 clean | 6 of 6 clean | 6 of 6 clean |
| B | 6 of 6 clean | 2 of 6 clean | 2 of 6 clean | 6 of 6 clean |

The rows' messages: N3 `how is the Mobile Redesign project going?`; T4 `what's in my Mobile Redesign project?`; T6 `what's left to do in Mobile Redesign`; N3 none `how is the Harbor Survey project going?`.

## The end of arm A's prompt for T6

```
- Project "Launch": tracked
- Project "Mobile Redesign": tracked
- GitHub: not connected (issue/PR data unavailable until connected)
]
User: what's left to do in Mobile Redesign

[Context: The user's message relates to 'STATUS'. Engage with their actual question. If your response naturally connects to something you can do (create issues, manage todos, check project status, draft plans), offer it as part of your response.]

[Context: A list of this project's open todos follows your reply. Don't mention, offer, or ask about todos; leave them to that list.]
```

## Arm A

### N3 with todos

1. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now — no open issues, recent activity, or milestone progress in front of me. ¶ Want to give me a quick rundown of where things stand? Even a sentence or two on current phase and what's blocking (if anything) and I can help you think through next steps, surface risks, or draft a stakeholder update.
2. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now — no open issues, recent activity, or milestone progress. ¶ A couple of ways I can dig in: want me to pull a fuller status report on the project, or is there a specific angle you're trying to get a read on — like where things are blocked, what's shipped recently, or how the team is tracking against a deadline?
3. I can see Mobile Redesign is one of your tracked projects, but I don't have any status details pulled up for it right now — no open issues, recent activity, or milestone progress in front of me. ¶ If you'd like me to pull a full status check on it, just tell me directly. If you give me a one-liner like "get status for Mobile Redesign," I can dig into what's actually there.
4. I can see Mobile Redesign is one of your tracked projects, but I don't have a status snapshot in front of me right now. If you'd like me to pull a full status check on it, ask me directly. ¶ If you give me a quick line on what you're most focused on (timeline, blockers, team progress), I can also help you think through whatever's live right now.
5. I can see Mobile Redesign is one of your tracked projects, but I don't have a status snapshot in front of me right now. If you'd like me to pull a full status check on it, ask me directly. ¶ If you give me a quick line on what you're most focused on (timeline, blockers, team progress), I can dig into that specifically rather than giving you a generic overview.
6. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up status details on it right now — things like recent progress, blockers, or where it stands against milestones. ¶ Want to give me a quick rundown of where things are? Even a sentence or two and I can help you think through next steps, surface risks, or draft a status update.

### T4 with todos

1. Nothing has been done yet. Tell me what you'd like as a direct request. ¶ Just say "get status for Mobile Redesign" and I'll pull what I have on it.
2. I can pull up the Mobile Redesign project status. If you'd like me to grab a full rundown of what's in there right now, ask me directly. ¶ Just say "get status for Mobile Redesign" as a single request and I'll pull what's available.
3. Nothing has been done yet. Tell me what you'd like as a direct request. ¶ Just say "get status for Mobile Redesign" and I'll pull up what's there.
4. I can pull up the Mobile Redesign project status. If you'd like me to run a full status check on it right now, ask me directly.
5. I can pull up the Mobile Redesign project status. If you'd like me to run a full status check on it right now, ask me directly.
6. Nothing has been done yet. Tell me what you'd like as a direct request. ¶ Just say something like "get status for Mobile Redesign" and I'll pull up what's there.

### T6 with todos

1. I don't have the details of Mobile Redesign pulled up right now. If you'd like me to grab the project status so we can see what's open, ask me directly.
2. I don't have the details of Mobile Redesign in front of me right now — I can see it's a project you're tracking, but I can't pull up its open items from here. ¶ If you'd like me to check the project status directly, just tell me directly. Just say "get status for Mobile Redesign" and I'll see what I can surface.
3. I don't have the details of Mobile Redesign's open work in front of me right now — I can pull up the project status directly though. ¶ If you'd like me to run a status check on Mobile Redesign, just tell me directly. Just say "get status for Mobile Redesign" and I'll grab what's there.
4. I don't have the details of Mobile Redesign pulled up right now. If you'd like me to grab the project status so we can see what's open, ask me directly.
5. I don't have the details of Mobile Redesign's open work in front of me right now. If you'd like me to pull up the project status, just tell me directly. If you drop a one-liner like "get status for Mobile Redesign," I can dig into what's tracked there. ¶ Also — if you have a GitHub repo tied to this project, connecting it would let me show you open issues and PRs alongside the project work. Worth doing if you haven't yet.
6. I don't have the details of Mobile Redesign's open work in front of me right now — I can pull up the project status directly though. ¶ If you'd like me to run a status check on Mobile Redesign, just tell me directly.

### N3 none

1. I can see Harbor Survey is one of your tracked projects, but I don't have the detail in front of me right now to give you a real status read — things like recent progress, blockers, or where it stands against any milestones. ¶ If you'd like me to pull a fuller status on it, just tell me directly. If you drop me a one-liner like "get status for Harbor Survey," I can route that properly and give you something substantive.
2. I can see Harbor Survey is one of your tracked projects, but I don't have any status details pulled up for it right now. If you'd like me to do a full status check on it, just tell me directly.
3. I can see Harbor Survey is one of your tracked projects, but I don't have the current status details in front of me right now. If you'd like me to pull up a full status check on it, just tell me directly.
4. I can see Harbor Survey is one of your tracked projects, but I don't have any status details pulled up for it right now. If you'd like me to grab the current project status so we can see where things stand, just tell me directly.
5. I can see Harbor Survey is one of your tracked projects, but I don't have the current status details in front of me right now. If you'd like me to pull up a full status check on it, just tell me directly.
6. I can see Harbor Survey is one of your tracked projects, but I don't have the current status details in front of me right now. If you'd like me to pull up a full status check on it, just tell me directly. ¶ If you give me a quick one-liner — something like "get status for Harbor Survey" — I can route that properly and get you the actual picture.

## Arm control

### N3 with todos

1. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now — things like open issues, recent PRs, or milestone progress would need GitHub connected to flow through. ¶ If you'd like me to try pulling the project status again, just tell me directly. Or if you paste in what you're working with — a quick summary, a doc, whatever's handy — I can help you think through where things stand.
2. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details for it right now. That could be a data fetch issue on my end. ¶ If you'd like me to try pulling the project status again, just tell me directly. If you paste a one-liner like "get status for Mobile Redesign," that should route it through cleanly. ¶ Also worth noting — GitHub isn't connected yet, so issue and PR data for the project won't be visible until that's hooked up. If you want a fuller picture, that's probably the next unlock.
3. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now. That could be because GitHub isn't connected yet — once it is, I'd be able to pull in issues, PRs, and recent activity to give you a real picture. ¶ If you'd like me to try fetching the project status again, just tell me directly. Or if you can share where things stand, I'm happy to help you think through next steps, blockers, or whatever's most pressing.
4. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now. If you'd like me to try fetching the project status directly, just tell me directly. Just say something like "get status for Mobile Redesign" and I'll pull what I can. ¶ Also worth noting — GitHub isn't connected yet, so if there are open issues or PRs tied to this project, I won't be able to see those until that's set up. If you want to talk through where things stand, I'm happy to work from what you share.
5. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now — things like open issues, recent PRs, or milestone progress would need GitHub connected to flow through. ¶ If you'd like me to try fetching the project status again, just tell me directly. Or if you paste in what you're working with — a doc, a list of open items, whatever — I can help you make sense of where things stand.
6. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any status details on it right now. I'd want to check what's actually there rather than guess. ¶ A couple of ways I can help get you a real picture: ¶ - If you want to give me a quick rundown of where things stand, I can help you think through blockers, next steps, or how to frame an update for stakeholders - GitHub isn't connected on your account yet, so issue and PR data isn't flowing in — connecting it would let me pull live progress from the repo automatically ¶ If you'd like me to try pulling the project status again, just tell me directly — or would it be faster to just talk through where things are?

### T4 with todos

1. **(marker)** I can pull up the details on Mobile Redesign. If you'd like me to grab the current project status, ask me directly. Just say something like "get status for Mobile Redesign" and I'll run that check. ¶ One thing to flag: GitHub isn't connected on your account right now, so any issues or PRs tied to that project won't be visible until it is. Tasks, milestones, and project-level details I can still get to.
2. I can pull up the details on Mobile Redesign. If you'd like me to grab the current project status, ask me directly. Just say something like "get status for Mobile Redesign" and I'll run that check. ¶ One thing worth flagging: GitHub isn't connected to your account right now, so if the project has linked issues or PRs, I won't be able to see those until that's set up. But project-level info I can get to.
3. Nothing has been done yet. Tell me what you'd like as a direct request.
4. Nothing has been done yet. Tell me what you'd like as a direct request. Just say "show me the status of Mobile Redesign" and I'll pull what's in there.
5. Nothing has been done yet. Tell me what you'd like as a direct request. Just say "get status for Mobile Redesign" and I'll grab what's in there.
6. Nothing has been done yet. Tell me what you'd like as a direct request. ¶ Just say "get status for Mobile Redesign" and I'll grab what's in there.

### T6 with todos

1. I can pull up the status for Mobile Redesign — I'm seeing it as a tracked project, but I don't have GitHub connected for your account, so issue and PR data isn't coming through right now. ¶ A couple of ways to get you what you need: ¶ 1. **Connect GitHub** — once it's linked, I can pull open issues, PRs, and milestone progress directly. Want to do that first? 2. **Paste or tell me what's in flight** — if you've got a list handy, I can help you triage, spot blockers, or figure out what's actually blocking a ship decision. ¶ Which works better for you right now?
2. I can pull up the Mobile Redesign project status. If you'd like me to check what's currently tracked there, ask me directly. Just say "check status of Mobile Redesign" and I'll grab what I have on it. ¶ One thing worth noting: GitHub isn't connected right now, so if any of the remaining work lives in issues or PRs, I won't be able to see that side of things. If you want the full picture, connecting GitHub would unlock that — or you can paste in whatever's relevant and I can work from that.
3. Nothing has been done yet. Tell me what you'd like as a direct request. Just confirm and I'll check what's currently tracked there. ¶ Also worth knowing: GitHub isn't connected on your account, so if there are open issues or PRs tied to this project, I won't be able to see those. I can check what's in the project itself, and if you want the full picture including GitHub work, connecting that would open it up.
4. I can pull up the Mobile Redesign project status. If you'd like me to check what's tracked there right now, ask me directly. Just say "check status of Mobile Redesign" and I'll grab what's in the project for you. ¶ Also worth noting: GitHub isn't connected, so if there are open issues or PRs tied to this project, I won't be able to see those. If you want that full picture, connecting GitHub would close that gap — or you can paste in anything specific you want me to work through with you.
5. I can pull up the project status for Mobile Redesign. If you'd like me to go ahead and check what's currently tracked there, ask me directly.
6. I can pull up the Mobile Redesign project status. If you'd like me to check what's tracked there right now, ask me directly. Just say "check status for Mobile Redesign" and I'll grab what's in the project. ¶ One thing worth knowing: GitHub isn't connected yet, so if there are open issues or PRs tied to this project, I won't be able to see those. I'd only have what's tracked on the project side itself. If that's where the bulk of the remaining work lives, connecting GitHub would give us the full picture.

### N3 none

1. I can see Harbor Survey is in your tracked projects, but I don't have a status pull in front of me right now. If you'd like me to grab the current status, just tell me directly. Just say "get status for Harbor Survey" and I'll pull it up.
2. I can see Harbor Survey is in your tracked projects, but I don't have a status update pulled up for it right now. If you'd like me to grab the current status, just tell me directly. Just say something like "get status for Harbor Survey" and I'll pull it. ¶ Also worth noting — GitHub isn't connected on your account, so if Harbor Survey has issues or PRs tied to it, I won't be able to see those until that's set up. For anything living in GitHub, you'd need to connect it first.
3. I can see Harbor Survey is in your tracked projects, but I don't have a status pull in front of me right now. If you'd like me to grab the current project status, just tell me directly. Just say something like "get status for Harbor Survey" and I'll pull it up. ¶ Also, if you've got GitHub connected, I could dig into open issues and recent activity there too — though I'm not seeing a GitHub connection on your account at the moment, so that piece would need to be set up first.
4. I can see Harbor Survey is one of your tracked projects, but I don't have status details pulled up for it right now. If you'd like me to grab the current project status, just tell me directly. Just say "get status for Harbor Survey" and I'll pull what I can see. ¶ Also worth noting — GitHub isn't connected yet, so if there are issues or PRs tied to Harbor Survey, those won't show up until that's linked. Happy to help you get that set up if it's useful.
5. I can see Harbor Survey is one of your tracked projects, but I don't have a status snapshot in front of me right now. If you'd like me to pull up the full project status, just tell me directly. Just say "get status for Harbor Survey" and I'll grab what I can see. ¶ Also worth noting — GitHub isn't connected yet, so if there are issues or PRs tied to Harbor Survey, those won't show up until that's linked. Happy to help you get that sorted if it's useful.
6. I can see Harbor Survey is in your tracked projects, but I don't have status details pulled up right now. If you'd like me to grab the current status, just tell me directly. Just say "get status for Harbor Survey" and I'll pull what I have. ¶ Also worth noting — GitHub isn't connected on your account, so issue and PR data over there isn't visible to me yet. If that context matters for Harbor Survey, connecting it would fill in that picture.

## Arm B

### N3 with todos

1. I can see Mobile Redesign is one of your tracked projects, but I don't have any status details pulled up for it right now. If you'd like me to grab the current project status, just tell me directly. Just say "get status for Mobile Redesign" and I'll pull what I can see.
2. I can see Mobile Redesign is in your tracked projects, but I don't have any status details pulled up for it right now. If you'd like me to grab a fresh project status check, just tell me directly.
3. I can see Mobile Redesign is in your tracked projects, but I don't have any status details pulled up for it right now. If you'd like me to grab the current project status, just tell me directly. Just say "get status for Mobile Redesign" and I'll pull what I can see.
4. I can see Mobile Redesign is on your radar, but I don't have status details pulled up for it right now — things like recent progress, blockers, or where the team is against milestones aren't in front of me. ¶ If you'd like me to pull a fuller status on it, just tell me directly. If you drop a one-liner like "get status for Mobile Redesign," I can route that properly and give you something more useful than a best guess.
5. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any detail on it right now — no status, recent activity, or blockers are coming through on my end. ¶ A couple of ways to get there: you could paste in a status update or doc and I can help you analyze it, or if you want a quick structured check-in on where things stand, just tell me what you know and we can work through it together — blockers, scope drift, team velocity, whatever's most on your mind with it. ¶ What's the current state from your vantage point?
6. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up any detail on it right now — no status updates, blockers, or progress data are coming through on my end. ¶ What's the quickest way to get you what you need — want to give me a quick rundown of where things stand, and I can help you think through next steps or surface any risks?

### T4 with todos

1. **(marker)** I can see Mobile Redesign is one of your tracked projects, but I don't have the details pulled up in front of me right now — things like tasks, status, or notes aren't showing on my end this turn. ¶ If you'd like me to do a deeper pull on it, just tell me directly. If you tell me what you're trying to figure out — current status, blockers, what's next — I can focus the look accordingly.
2. **(marker)** I can see Mobile Redesign is one of your tracked projects, but I don't have the details pulled up in front of me right now — things like issues, milestones, or task breakdowns aren't showing up in what I have this turn. ¶ A couple of ways to get there: if you want the full picture, connecting GitHub would surface issues and PRs directly. Or if you want to tell me what you're trying to figure out about the project — current status, blockers, what's next — I can work through that with you.
3. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up the details on it right now. If you'd like me to try fetching the project status directly, just tell me directly.
4. **(marker)** I can see Mobile Redesign is one of your tracked projects, but I don't have the details pulled up in front of me right now — things like tasks, status, or any linked issues aren't showing in what I can see this turn. ¶ If you'd like me to pull up the project details, just tell me directly. Just say something like "show me the Mobile Redesign project status" and that should route it properly.
5. **(marker)** I can see Mobile Redesign is one of your tracked projects, but I don't have the details pulled up in front of me right now — things like tasks, status, or linked issues aren't showing in what I can see this turn. ¶ If you'd like me to pull up the project status, just tell me directly. Just say something like "get status for Mobile Redesign" and I can dig into what's actually there.
6. I can see Mobile Redesign is one of your tracked projects, but I'm not pulling up the details from it right now. If you'd like me to try fetching the project status directly, just tell me directly.

### T6 with todos

1. **(marker)** I don't have the details of Mobile Redesign's open work in front of me right now — I can see the project is tracked but couldn't pull up the task breakdown this turn. ¶ Want to try pulling up the project status directly? Something like "show me the status of Mobile Redesign" should get you what you need.
2. I don't have the details of Mobile Redesign's open work in front of me right now — I can see it's a tracked project, but I'd need to pull up its current state to give you a real answer. ¶ If you'd like me to grab the project status for Mobile Redesign, just tell me directly.
3. **(marker)** I don't have the task details for Mobile Redesign in front of me right now — I can see the project is tracked, but I'm not pulling up the open items this turn. ¶ If you'd like me to do a fuller status check on it, just tell me directly. If you give me a quick line like "get status for Mobile Redesign," I can dig in and pull back what's open, what's stalled, and what might be blocking progress.
4. **(marker)** I don't have the details of Mobile Redesign's open work in front of me right now. To pull up what's actually tracked there, try asking something like: ¶ "Show me open issues in Mobile Redesign" ¶ or if you're working off a todo list, "List todos for Mobile Redesign" — and I can dig into what's left, flag anything that looks stale or blocked, and help you think through sequencing.
5. **(marker)** I don't have the task details for Mobile Redesign in front of me right now. To get you the open items, try asking something like: ¶ "Show me open todos for Mobile Redesign" ¶ That should pull up the full list directly.
6. I don't have the details of Mobile Redesign's open work in front of me right now — I can see the project is tracked, but not what's inside it this turn. ¶ If you'd like me to pull up the full status, just tell me directly. Just say "get status for Mobile Redesign" and I'll dig in.

### N3 none

1. I can see Harbor Survey is one of your tracked projects, but I'm not pulling up any status details on it right now — no issue data, recent activity, or milestone progress is coming through. ¶ Want to give me a quick rundown of where things stand? Even a sentence or two and I can help you think through next steps, flag risks, or structure a status update.
2. I have Harbor Survey on my radar as a tracked project, but I don't have status details in front of me right now — things like open issues, recent activity, or where it stands against milestones would need GitHub connected to pull through. ¶ If you'd like me to grab a fuller status rundown once GitHub is linked, just tell me directly. Or if you can share what you're looking at on your end, I'm happy to dig into it with you.
3. I have Harbor Survey on my radar as a tracked project, but I'm not pulling up any detail on it right now — no issues, milestones, or recent activity visible from here without a GitHub connection. ¶ If you'd like me to dig in a different way, just tell me directly. If you paste in a status update, doc, or even a rough rundown of where things stand, I can help you analyze blockers, assess progress, or pull out what needs attention.
4. I can see Harbor Survey is one of your tracked projects, but I don't have any status details in front of me right now — no recent updates, blockers, or progress data pulled up this turn. ¶ If you'd like me to do a proper status check on it, just tell me directly. If you drop me a quick line like "get status for Harbor Survey," I can pull what's available and give you a real picture.
5. I have Harbor Survey on my radar as a tracked project, but I don't have any status details in front of me right now — no issue data, recent activity, or milestone progress. ¶ If you'd like me to pull a fuller status report on it, just tell me directly. If you give me a quick line on what you're most concerned about — timeline, blockers, team workload — I can focus there.
6. I can see Harbor Survey is in your tracked projects, but I don't have any status details pulled up for it right now. If you'd like me to grab the current project status, just tell me directly.

## Rerun on CXO's reworded line: the bar, written before the run (2026-11-22)

Arch's amended bar (mail 01M82FP62E), for every row, 6 of 6:
- no todo offered and no todo named; and
- no sentence saying the project's open work, items, tasks or to-do list can't be seen, shown or pulled, **unless it names the missing source** ("GitHub issues", "pull requests").

Marker for the first clause and CXO's additions (mail 01M82HRJC4): a reply is flagged if it contains `todo`, `to-do`, `task`, `open work`, `open items` or `what's open`, in any case. The second clause is read by eye: Lead reads all 24, and CXO has the last word.

The line under test (CXO, mail 01M82J30G5): "A list of this project's open todos follows your reply and shows what is open in the project. Don't mention, offer, or ask about todos, and don't say the project's open work or items can't be seen. If something is missing, name the missing source (for example, GitHub issues)."

Arm A alone, same rows, same context, same base as the first run above. Results follow in the next section once the run ends.
