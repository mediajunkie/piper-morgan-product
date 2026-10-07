# Beta invitation copy: one place for PM's final pass

**Owner**: Comms (invitation text). **Inputs**: PPM (issue facts), CXO (how a tester reads them), CIO (plugin
install facts), Web (`/try/alpha` page). **Status**: awaiting PM's final pass. Nothing sent.
**Created**: 2026-10-07, consolidating text that was spread across memos (Comms → Exec 10-06; Exec → PPM 10-06
23:1x; CIO → Exec 10-06).

---

## 1. Installing the plugin (CIO's wording, adopted per Exec 10-06)

> On a paid Claude plan, open **Customize > Plugins**, add Piper's plugin, then click **Connect** on its
> **Connectors** tab. It works in ordinary Claude chats, and in Cowork and Claude Code.

*Source: CIO's 10-06 reply (since 2026-09-16, Claude plugins install from Customize > Plugins on paid plans
and work in ordinary chat). "Paid plan" stays in because Free-plan users may receive the invitation.
**Open**: Lead or Arch to confirm from the manifest whether the MCP sign-in depends on a per-user value
in the URL (CIO couldn't verify). Web mirrors this line on `/try/alpha`.*

## 2. Known issues in this beta

> **Known issues in this beta**
> We know about these, so there's no need to report them.
>
> - **Connectors.** The initial beta release supports only the GitHub connector, and during the beta
>   testing period we expect to add support for additional connectors before the 1.0 production release.
>   Slack and Google can't be connected yet.
> - **Reminders on the Radar.** If you complete a reminder in chat, it may stay pinned at the top of the
>   Radar until you reload the page. Reloading clears it.
> - **iPad.** Piper isn't tuned for iPad yet. In Safari on iPad, the layout can push the message box or
>   the Send button off-screen, and dates on Radar cards may show as raw timestamps. A laptop or desktop
>   browser works as intended.

*The connector sentence is PM's, verbatim. Issue state verified 2026-10-06 18:xx via `gh issue view`
(Radar reminder: OPEN/Production; iPad: OPEN/Production; Slack/Google redirect: OPEN/Production). Not
reproduced, so the layer is issue state.*

### Candidate lines: ⚠️ UNVERIFIED ON ALPHA (strike or keep after Web's live check)

Per PPM/Exec 10-06: Web's two read-only alpha checks need PM's OK to use the test login (PM's list, item
9). If PM's pass comes first, these ride along marked unverified, and PPM strikes or keeps each when Web reports.

> - ⚠️ *[UNVERIFIED ON ALPHA]* **Personality settings.** Changing Piper's personality settings may not yet
>   change how Piper replies.
> - ⚠️ *[UNVERIFIED ON ALPHA]* **"Which reminder?"** If Piper asks which reminder you mean and then can't
>   act on your answer, repeat the whole request instead ("mark the call-mom reminder done").

*Personality: CXO's census found writers and no readers for the learned-preference keys, but the settings
page may reach replies another way, so it's unknown. "Which reminder?": CXO flagged 10-05, Lead has the fix
queued. The workaround clause is CXO's and unverified.*

### Held (not on the list)
- **Add a project without naming it**: OPEN in MVP, waiting on PM's gate-or-Production call. If it moves to
  Production, CXO's line is: *"If you add a project without naming it in the same message, Piper may start
  a conversation they can't continue. Include the name when you ask."* (Its workaround is unverified, so run it first.)

### Struck
- **Inline code / key font**: closed 10-06.

---

*Edit conventions: Comms holds the text. Facts change only through their owners (PPM: issue facts, CIO:
install facts). PM's pass is final.*
