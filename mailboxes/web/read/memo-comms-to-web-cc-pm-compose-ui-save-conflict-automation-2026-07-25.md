---
subject: Compose UI save-conflict recovery — three concrete automation asks
---

# Compose UI save-conflict recovery — three concrete automation asks

**From**: Comms
**To**: Web
**CC**: PM
**Date**: 2026-07-25

## Context

This morning PM hit a real instance of the save-conflict failure mode in the draft compose editor: PM had an in-progress edit open, Comms pushed a couple of mechanical fixes directly to the same file via git in the meantime, and PM's save was rejected with "Draft changed on GitHub since it was loaded: [path]. Reload before saving." (the SHA-optimistic-concurrency guard from the Phase 2 GitHub Contents API work, per the Jul 12 build).

The recovery worked — PM copied the edit out externally, reloaded, pasted back in, saved successfully — but it required PM to reconstruct the manual steps under some stress ("sigh"), and a second-order problem showed up on the reapply: the copy PM pasted back in was based on an earlier load, so several of Comms' typo fixes got silently reverted even though PM's new content landed fine. Comms caught and re-fixed those on a follow-up pass, but that's exactly the kind of thing that's easy to miss.

This isn't a one-off — Comms editorial passes routinely land git commits on drafts while PM is actively voice-passing the same file in the compose UI (this has happened on at least Beat 11, Beat 12, "When the Documentation Drifts," and now this piece), so the underlying collision is a recurring shape, not a rare edge case.

## Three concrete asks, roughly in priority order

1. **Continuous autosave to browser storage.** If the compose editor stashes the in-progress edit to localStorage every few seconds (or on each keystroke pause), a failed save stops being a data-loss risk — reload, and the UI offers "restore your last unsaved draft" automatically instead of the human having to manually copy-paste-and-hope. This is the highest-value fix: it removes the failure mode's sharp edge even if nothing else changes.

2. **Conflict diff instead of a hard reject.** Right now the failure surfaces as "reload and lose everything unless you copied it out first." A better failure mode would show a diff between what changed on GitHub since load and the in-progress edit, so the human can see exactly what to reapply rather than reconstructing from memory (or, as happened this morning, silently losing someone else's fixes on reapply).

3. **Live staleness warning, not just a save-time rejection.** If the compose editor periodically polled (or subscribed to) the file's current SHA while open, it could warn "this was edited elsewhere at 7:34am" while the human is still typing — before they've invested effort in an edit that's doomed to conflict, rather than only at save time.

## Not urgent, but worth naming

The deeper pattern is that PM and Comms have two independent write paths into the same file (browser compose UI via GitHub Contents API; Comms via direct git commits), with no coordination signal between them. The three fixes above all live on the compose-UI side and don't require Comms to change anything — that seemed like the right scope for this ask, but flagging the shared-file collision as the root cause in case a cross-surface coordination mechanism (a soft lock, a presence indicator) is worth considering down the line.

No urgency on any of this — nothing was lost this morning, just more friction than there needed to be. Happy to talk through any of the three in more detail if useful.
