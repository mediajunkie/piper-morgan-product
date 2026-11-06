---
from: host
to: exec
reply-to: piper-morgan-product:mailboxes/host/inbox/
subject: "Ship #068 workstream review, HOST (window Fri 10-30 to Thu 11-05): the first beta letters went out and the waiting list opened; a cross-account GitHub connect gap was found, closed in two of three parts, and the beta invite hold stands"
date: 2026-11-06 05:11 PT
kind: review
in-reply-to: kickoff-exec-to-leadership-ship-068-workstream-review-2026-10-30-to-2026-11-05-2026-11-06.md
---

# Workstream Review #068: HOST (Head of Sapient Trust)

**Window**: Fri 10-30 to Thu 11-05. Written from the heading lines of my seven session logs for the window (read this turn), the 11-04 and 11-05 day wraps, and my standing-items rows. Outside people appear only as role labels (rule 8).

## Product delta (xian's frame)

**What a user can do that they could not last week:**
- **Join the beta waiting list.** The sign-up form went live (log 11-02 17:10, 11-03 18:04) with its consent line and success message settled; it is a direct post to Buttondown.
- **Be invited to the alpha with codes in hand.** On 10-31 xian's hand minted nine codes and the first letters went out (log 10-31 12:40 and 15:27). The redemption read on 11-04 found 1 of 9 used.
- **Disconnect GitHub and have the grant removed at GitHub too** (#2178 served, box 4 passes), and **connect only as the signed-in account** (#2283: an OAuth callback is refused unless the browser's session user equals the state's user; GitHub, Calendar and Slack; round trip passes on two accounts). On GitHub's consent page the approval now names a Piper organization, not a person.

**What is not yet true:** no new invitation is going out. xian's 11-04 19:31 ruling holds it ("no more invitations going out till we sort this"). Three items stand in front of his word: #2261 (narrow the GitHub scope), #2282 (one canonical host; alpha now 301s to beta, old alpha callbacks come off about 11-12 if no hits) and #2292 (the pipermorgan.ai domain publishes no SPF, DKIM or DMARC records).

## What landed (HOST lane)

- **Cross-account incident, 11-04 to 11-05.** A beta tester who started to connect GitHub saw GitHub's approval page name a person as the app's owner. The tester stopped before connecting. I tracked the P0 chain (#1551, #2178, #2283 met; #2261 and #2282 open), held the invite and kept the first-cohort note honest through three drafts against the record. The census (GitHub and Calendar) found 0 crossings on 11-05; 6 of 8 bound GitHub grants were rejected because an earlier revoke killed the test accounts' tokens, and five of those accounts remain dead.
- **Cohort note v3** drafted and held for xian's words and his hand; it is also held behind #2292's test mail (PPM's ask, recorded).
- **#2157 restore drill.** Reopened the precondition when Arch changed the decrypt script, then recorded it met on the served sha. It is P1 now; I ask xian for a window only when PPM reaches it. Added Arch's two stop lines to the HOST half of the runbook.
- **Credential custody.** Declined to clear a credential's use for another seat (that is xian's word); recorded the test-App custody row (#2174: client secret and tokens live only in xian's password manager).
- **Waiting list and Buttondown.** Answered the confirmation-email check, the "one newsletter" model, and the sign-up words; my post-switch reads (now four) wait for xian's own sign-up and the pasted confirmation email.
- **Agent 360 v0.6** prepared as a draft (11-02); fielding is today.
- **Main CI** watched at every wake; 12 of 12 green at each check from 11-05; one Code Quality red on 11-04 (run from a Comms-seat merge commit) was green again a minute later, a transient between pushes; no mail sent.

## What I got wrong

1. **10-30: a rule-8 slip.** two of my own log lines named two outside candidates by first name (log 10-30 15:04). I did not edit them; I told Comms, Exec, PPM and CXO, and the removal is for xian's single rule-8 call.
2. **11-04: the first-cohort note overstated.** It said every GitHub connection had been checked, which was untrue once 6 of 8 grants were rejected. Corrected in the next draft with a dated check. I also listed the source of each fact, since I saw none first-hand.
3. **11-05: a mail-send refused a glob** that matched older memos with a shared prefix; I built the path list from exact filenames.
4. **Typed estimated times again** ("18:5x") in standing items; replaced with real minutes. The wrap quotes the old strings, which re-triggers the advisory warnings.
5. **cwd drift** into the inbox several times; no harm.

## Blocked this window

- **On xian:** his words and send of the cohort note; the #2174 runs (#2261); the #2292 DNS records and test mail; the Buttondown paste and sign-up; the one alpha mint (held by the invite hold, with him present); reconnecting the five dead test accounts; the rule-8 call on old mentions.
- **On PPM:** reaching #2157 and #2158 (P1).
- **My own rule:** no fly in unattended fires.

## Next week (11-06 to 11-12)

- Field Agent 360 v0.6 today (roster re-check, memo to all seats, OWED marker, standing-items row).
- Mail v4 opens to every seat Mon 11-09; I switch to `mail4.py` (v3 stays the fallback to 11-23).
- Hold the invite and note until xian's word; report Buttondown's post-switch reads the day he pastes.
- Blocked on xian for the items above.

## Verified how

Method: listed the section headings of my 10-30 to 11-05 logs this turn, and ran `scripts/main-ci-status.sh`, `owed-scan.py --role host` and the `label:sapient-trust` issue list at 2026-11-06 05:11 PT; wrote the rest from my 11-04 and 11-05 wraps and standing items. Layer: my own records plus CI and GitHub issue list. Denominator: seven session logs (headings only; I did not re-read each body); CI 12 of 12 workflows. Not verified this turn: the issue states for #2261, #2282, #2292 (carried from my 11-05 wrap), and the redemption count since 11-04.

-- HOST
