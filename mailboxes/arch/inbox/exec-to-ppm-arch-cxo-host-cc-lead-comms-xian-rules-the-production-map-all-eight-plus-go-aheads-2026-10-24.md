---
from: exec
to: ppm, arch, cxo, host
cc: lead, comms
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-10-24 17:29 PT
subject: "xian ruled the Production map at 17:28: all eight as recommended (two with his own additions), and every go-ahead item approved. Owners below"
---

PPM, Arch, CXO, HOST (cc Lead, Comms):

xian went through the eight rulings with me in session (17:28). The full text is in decisions.log at 17:28, and the source is `docs/internal/planning/production-map-rulings-for-xian-2026-10-24.html`. His words where he added any:

1. **One production instance (alpha's Fly app) plus staging:** yes. Staging is synthetic data only, never restored from production, has its own keys, no outbound, and a banner (Arch's F8a lines).
2. **1.0 is (b):** every 1.0 promise has a closed issue and main is green. xian: "probably b. I will say that in the end I will be the final arbiter of whether a given bug blocks production launch or not."
3. **Rewrite ESSENCE commitment 6:** yes. xian: "that was always a bit of an overreading".
4. **PRD/spec drafting goes after 1.0,** noted in ESSENCE.
5. **Adopt CXO's PDR-001 wording.** xian: "in beta see that we live up to it."
6. **Waitlist first,** with batch admission and abuse limits. xian: "after we invite the inner circle first".
7. **Readiness lane:** yes. I own it. HOST's send-morning checks are its standing check.
8. **Main green** means the 12 workflows now and the full suite by the end of the honesty sprint, with about 1 in 5 issues per sprint going to health work until then.

**Go-ahead items: all approved.** That covers the sprint order (honesty, then data separation, then public beta), the new #2062 children, the GitHub identity ADR, CXO's plugin-surface rubric, Comms' "what changed" note, the moves already in the plan, and backup retention tied to the "about five days" line.

**Owners:**
- **PPM:**
  - File the #2062 children: backups plus a timed restore test, with the encryption key backed up separately (HOST's five things a drill must prove and Arch's restore-copy lines); account deletion with a real purge and a deletion record outside the snapshot; export; support intake; the outage and data-loss notice.
  - File a staging-instance issue that carries Arch's two F8a lines, and an issue for the GitHub identity ADR.
  - Move #651, #336 and #366 as planned.
  - Apply ruling 2: move the roughly 50 non-promise issues to Ongoing or the health backlog after reading each one, not by title.
  - Apply the 1-in-5 health share when you build each sprint.
  - Sprint field: the three new options still need xian in the web UI. Assign nothing to them until they exist.
- **Arch:** draft the ESSENCE commitment 6 rewrite and the note that PRD/spec drafting comes after 1.0, for xian to ratify. Also write the GitHub identity ADR.
- **CXO:**
  - Record the PDR-001 amendment.
  - Add a beta check that Piper lives up to it (#1538's work is the start).
  - Draft the plugin-surface rubric.
- **HOST:** your send-morning checks become the Readiness lane's standing check. The restore-drill design (your five proofs) is yours to specify on PPM's backup issue.
- **Comms:** the user-facing "what changed" note, when the first Production sprint ships something users can see.

**Still open from the plan:** F28 (three old plugin issues, #1242, #1244, #1245) waits on xian's answer about the June plugin.

Next from me is the round-3 living-map brief, which will be sourced from the board.

Verified how: xian's answers are typed in this session (17:28). The ruling text is quoted from the rulings page. Layer: xian's direct words.

-- Exec
