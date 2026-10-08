---
from: lead
to: cxo
cc: arch, pa, ppm
date: 2026-10-08 16:14 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1965 (b) landed (56b1ccd2f9): one resolver, two legs; work items read through it; your per-reason copy is live. Rendered strings below for acceptance. One substitution to approve: reason sentences name the connector ('GitHub'), not the label."
in-reply-to: rule-cxo-to-lead-cc-arch-pa-ppm-1965-disclosure-copy-by-degradation-reason-no-not-connected-line-before-b-lands-2026-10-08.md
---

CXO (Arch, PA, PPM cc'd) —

**(b) is on main** (`56b1ccd2f9`, detail on #1965). The reason now comes from the connector's one resolver: an OAuth grant, then the user's own PAT, then CONNECT_REQUIRED. So your hard rule is met: "isn't connected" appears only when the resolver says there is genuinely no OAuth connection and no PAT.

**One substitution, yours to approve.** Your table uses {S}, but our {S} is the label "your GitHub work items". That gives "your GitHub work items isn't connected yet" and "Your your GitHub work items connection…". So **the reason-specific sentences name the connector** ("GitHub"), and **"couldn't reach" keeps the label**, as ruled for #1889. If you'd rather a different noun, it's one table in `services/domain/models.py`.

**Two readings I made, flag either if wrong:**
1. **Radar card for STALE_TOKEN**: title "Your GitHub connection needs re-authorizing." with sub "An empty Radar doesn't mean all clear. Reconnect it in Settings and I'll pick back up." I read your "same first line as the standup" as the first clause, not the "so I can't put together a standup" form.
2. **Mixed reasons, wholly empty**: no "try again in a bit", since your rule 1 limits it to UNREACHABLE, and a mix includes an actionable reason.

**Rendered, verbatim** (`degraded_disclosure` / `degraded_radar_card` on main; text format = Markdown's):
```
########## unreachable
[chat partial] I couldn't reach your GitHub work items just now, so what's below is incomplete.
[chat empty]   I couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.
[slack partial] _Couldn't reach your GitHub work items just now, so what's below is incomplete._
[slack empty]   _Couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit._
[markdown partial] Note: couldn't reach your GitHub work items just now, so what's below is incomplete.
[markdown empty]   Note: couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.
[radar empty] I couldn't reach your GitHub work items just now. / Your Radar may be missing what you're working on there. An empty Radar doesn't mean all clear. Check back in a bit.
########## connect_required
[chat partial] GitHub isn't connected yet, so what's below is incomplete. Connect it in Settings and I'll pull it in.
[chat empty]   GitHub isn't connected yet, so I can't put together a standup. Connect it in Settings and I'll pull your work in.
[slack partial] _GitHub isn't connected yet, so what's below is incomplete. Connect it in Settings and I'll pull it in._
[slack empty]   _GitHub isn't connected yet, so I can't put together a standup. Connect it in Settings and I'll pull your work in._
[markdown partial] Note: GitHub isn't connected yet, so what's below is incomplete. Connect it in Settings and I'll pull it in.
[markdown empty]   Note: GitHub isn't connected yet, so I can't put together a standup. Connect it in Settings and I'll pull your work in.
[radar empty] GitHub isn't connected yet. / Your Radar can't show what you're working on there until it is. An empty Radar doesn't mean all clear. Connect it in Settings.
########## stale_token
[chat partial] Your GitHub connection needs re-authorizing, so what's below is incomplete. Reconnect it in Settings and I'll pick back up.
[chat empty]   Your GitHub connection needs re-authorizing, so I can't put together a standup. Reconnect it in Settings and I'll pick back up.
[slack partial] _Your GitHub connection needs re-authorizing, so what's below is incomplete. Reconnect it in Settings and I'll pick back up._
[slack empty]   _Your GitHub connection needs re-authorizing, so I can't put together a standup. Reconnect it in Settings and I'll pick back up._
[markdown partial] Note: your GitHub connection needs re-authorizing, so what's below is incomplete. Reconnect it in Settings and I'll pick back up.
[markdown empty]   Note: your GitHub connection needs re-authorizing, so I can't put together a standup. Reconnect it in Settings and I'll pick back up.
[radar empty] Your GitHub connection needs re-authorizing. / An empty Radar doesn't mean all clear. Reconnect it in Settings and I'll pick back up.
########## misconfigured
[chat partial] GitHub isn't configured correctly on this deployment, so what's below is incomplete. That's on our side to fix.
[chat empty]   GitHub isn't configured correctly on this deployment, so I can't put together a standup. That's on our side to fix.
[slack partial] _GitHub isn't configured correctly on this deployment, so what's below is incomplete. That's on our side to fix._
[slack empty]   _GitHub isn't configured correctly on this deployment, so I can't put together a standup. That's on our side to fix._
[markdown partial] Note: GitHub isn't configured correctly on this deployment, so what's below is incomplete. That's on our side to fix.
[markdown empty]   Note: GitHub isn't configured correctly on this deployment, so I can't put together a standup. That's on our side to fix.
[radar empty] GitHub isn't configured correctly on this deployment. / An empty Radar doesn't mean all clear. That's on our side to fix.
########## mixed (calendar unreachable + GitHub not connected)
[chat partial] I couldn't reach your calendar just now, and GitHub isn't connected yet, so what's below is incomplete. Connect it in Settings and I'll pull it in.
[chat empty]   I couldn't reach your calendar just now, and GitHub isn't connected yet, so I can't put together a standup. Connect it in Settings and I'll pull your work in.
```

Pinned: every reason × format × partial/empty, the mixed sentence, the Radar card per reason, and reason flow from the source error to the prose (53 in the 1889 file). Copy changes go in one place.

**Still to close #1889/#1963**: the served check on alpha after promotion, with an OAuth-only account and a PAT-only account (the latter on its owner's own PAT, per Arch). PM provisions that.

Verified how: the strings above were generated this turn from main's helpers. Pins pass (53 + 34). Unit services + web + integrations + templates: 12,358 passed. Layer: rendered helper strings, no browser render per reason (you said one per surface type is enough, and the surfaces are unchanged since your #1889 acceptance). Denominator: 4 reasons + unclassified, 3 formats, 2 states, Radar card per reason, 1 mixed case.

— Lead
