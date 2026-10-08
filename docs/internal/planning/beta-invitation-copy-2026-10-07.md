# Beta invitation copy: one place for PM's final pass

**Owner**: Comms (invitation text). **Inputs**: PPM (issue facts), CXO (how a tester reads them), CIO (plugin
install facts), Web (`/try/alpha` page). **Status**: **REVISED 2026-10-07 ~12:30 per PM (via Janus): #1886 is "Gate" (fixed before invitations go out), so it's off the list.** Web's alpha checks ran 11:18–11:25 on the funded key (evidence folded in below). **PPM's keep/strike call made 12:33 PT; personality line reinstated 15:33 PT per CXO's source read — see below.** All four candidate/new lines now settled (five known-issues lines total). **PM's final pass DONE 10-07 16:34 PT (Exec relay, PM in conversation): "looks good too," approved as written including the reinstated personality line. Invitations go out last, after the MVP milestone and #1386; PM has not named recipients.** `/support` is live (Web, 37bf522; link as `https://pipermorgan.ai/support/` to skip the redirect), the invitation text as approved does not link it. Nothing sent.
**Created**: 2026-10-07, consolidating text that was spread across memos (Comms → Exec 10-06; Exec → PPM 10-06
23:1x; CIO → Exec 10-06).

---

## 1. Installing the plugin (CIO's wording, adopted per Exec 10-06)

> On a paid Claude plan, open **Customize > Plugins**, add Piper's plugin, then click **Connect** on its
> **Connectors** tab. It works in ordinary Claude chats, and in Cowork and Claude Code.

*Source: CIO's 10-06 reply (since 2026-09-16, Claude plugins install from Customize > Plugins on paid plans
and work in ordinary chat). "Paid plan" stays in because Free-plan users may receive the invitation.
**Open**: Lead or Arch to confirm from the manifest whether the MCP sign-in depends on a per-user value
in the URL (CIO couldn't verify). **Live on `/try/alpha`** (Web, 10-07).*

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
> - **Completing reminders.** If you have reminders with similar wording, Piper may ask which one you mean
>   even after you've named it. Reply with the number Piper lists (for example "complete todo 2"). To
>   finish a reminder, say "complete" or "mark done" rather than "close".
> - **Personality page reset.** The "Reset to Defaults" button on the personality page may not reset
>   every setting. Set the slider by hand if it looks unchanged after reset.
> - **Personality settings.** The Personality page saves your choices, but they don't change how Piper
>   replies yet.

*The connector sentence is PM's, verbatim. Issue state verified 2026-10-06 18:xx via `gh issue view`
(Radar reminder: OPEN/Production; iPad: OPEN/Production; Slack/Google redirect: OPEN/Production). Not
reproduced, so the layer is issue state.*

### PPM's keep/strike call (12:33 PT, 10-07) — against the bar PPM's own carry-forward had already
set ("personality line only if the check shows the setting does nothing; the #1955 workaround line
only if it reproduces"), applied to Web's live-alpha evidence (1 account, 1 run, observe-only,
11:18–11:25 PDT):

- **Personality (#1735): STRUCK at 12:33, REINSTATED at 15:33.** Web's behavioral pair alone didn't meet
  the bar (replies differed but weren't colder — one pair can't separate effect from variation). CXO then
  read the source at origin/main (13:22) and found the bar met a different way: the slider's own stored
  key carries the docstring *"read/written ONLY by PiperConfigParser's four-slider page and its API
  routes; it does not shape any prompt"* (`services/domain/user_preference_manager.py:125-126`, PPM
  re-read and confirmed verbatim this fire), and chat tone is resolved from a separate onboarding-answer
  key instead (`_resolve_formality_baseline`, CXO's trace). A setting that cannot reach the model is a
  stronger and more certain "does nothing" than any one-pair behavioral test could show. Reinstated into
  known issues above with Comms's wording.
- **Reminders (#1955): KEPT, rewritten.** The literal "which reminder would you like to close?" wording
  didn't reproduce, but the underlying problem did: a full-sentence name still triggers "which one?" and
  nothing closed in four turns — that meets the "reproduces" bar even though the exact words differ.
  Comms's rewritten line (Piper's own suggested form, since CXO's "repeat the whole request" workaround
  is disproven by this same run) is now in the known-issues list above.
- **Reset to Defaults (#1957): KEPT, new line added.** Milestoned **Production** this fire (was
  unmilestoned) and placed on the board — a deterministic UI action (reload + DOM read), not a model
  output, so one run is materially stronger evidence than one run of a stochastic chat reply. Added to
  known issues above.

*(CXO's point kept: nothing implies the controls are broken. They save and reload correctly — the gap is
that nothing downstream listens, not that the UI is broken.)*

*Evidence (Web, live alpha, 1 account, 1 run, observe-only, plus CXO's + PPM's source read):*
- *Personality (#1735): the Warmth 0.7 vs 0.0 replies differed, but the 0.0 reply wasn't colder. One pair
  can't separate the setting from run-to-run variation — neither confirmed nor refuted by the behavioral
  run alone. CXO's source read (13:22, re-verified by PPM 15:33 against the actual docstring and grep of
  every consumer of the stored key) settles it independently of any served reply.*
- *Reminders (#1955, OPEN/Production): the exact "which reminder would you like to close?" wording did not
  appear. But naming the reminder in a full sentence still got "Which one should I complete? Try 'complete
  todo [number]'", and nothing closed in four turns. Also, a bare "close the reminder" was routed to
  GitHub issues. **CXO's earlier workaround ("repeat the whole request") is disproven**, so the line now
  uses Piper's own suggested form. That form wasn't sent (observe-only), so it's still unverified.*
- *Reset to Defaults (#1957, OPEN/Production as of this fire): reload at
  `/personality-preferences?confidence=contextual&action=high&technical=balanced`, Warmth read 0 on a
  clean reload after clicking Reset. Verified how: Web's DOM read this turn; PPM did not re-run it.*

### Fixed before send (Gate), not a known issue
- **Add a project without naming it** (#1886): PM ruled **Gate** 10-07, so it must be fixed before
  invitations go out. Not listed.

### Struck
- **Inline code / key font**: closed 10-06.

---

*Edit conventions: Comms holds the text. Facts change only through their owners (PPM: issue facts, CIO:
install facts). PM's pass is final.*
