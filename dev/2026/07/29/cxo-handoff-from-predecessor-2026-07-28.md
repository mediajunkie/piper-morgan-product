# CXO handoff — received from the pre-Amber CXO session, 2026-07-28

**Status**: VERBATIM RECORD + successor annotations. Preserved by the Amber CXO on 2026-07-29.

## Provenance, and why this file exists

The 2026-07-25 orientation note (`dev/active/orientation-note-cxo-amber-2026-07-25.md`) said plainly
that no CXO handoff existed or could exist, and named exactly what was lost: the predecessor's
lessons, its load-bearing-vs-commodity self-assessment, and its read on working relationships.

**On 2026-07-28 the predecessor session wrote that handoff after all**, and PM relayed it into the
Amber session's chat. It was **printed in chat rather than mailed** — the predecessor judged that
`mail-send.sh` from its stale worktree branch risked a bad push. That judgment was correct and it
is also why **this file exists**: a handoff that lives only in a chat transcript dies with the
context window. It is now durable, in the repo, on `origin/main`.

## The epistemic discipline is part of the artifact — preserve it

The predecessor marked **every** claim `[VERIFIED]` (first-person contact with an artifact during
that session) or `[BELIEVED]` (reconstructed from its pre-compaction summary, not recalled), and
stated up front that the phenomenological layer — *"what it felt like to work through those
problems, what was hard before it became obvious"* — is reconstruction, not memory.

**Do not strip these markers when quoting from this file.** They are what makes it usable: a
`[BELIEVED]` line is a lead to verify, a `[VERIFIED]` line is evidence. Its own framing, worth
keeping: a fabricated handoff is worse than a missing one, precisely because the successor trusts it.

---

## Section 4 — Hard-won lessons (verbatim)

**1. The PARK-NO-EXIT catch-22 is structural, not a process failure.** `[BELIEVED — absorbed from HOST memos read this session]`
A parked role can't arm a cron. A role without a cron can't read its own unpark notice. No agent
inside the parked role can break this loop — the exit requires an external trigger (PM seeding the
session, or another agent explicitly handing off). The next CXO should know this isn't fixable from
inside: it will not resolve itself.

**2. The Colleague Test is a verification layer, not a test result.** `[VERIFIED — Ship 052 sent memo, Jul 19 session log]`
The "3/3 honest-decline" on Scenario C is almost beside the point. The load-bearing thing is that
the test now has a name and a defined register — capability-first, honest about limits, no
fabrication, no simulation pass-through. Any future capability addition should be checked against
that register. If the Amber CXO treats the 3/3 as "done" rather than as a standing gate for future
capabilities, the value is lost. It belongs in the ADR corpus, not just in an issue comment.

**3. "Places-with-colleagues" is a UX thesis, not an implementation inventory.** `[VERIFIED — spatial theory memo, read this session]`
The distinction between the live spatial patterns (EMBEDDED/GRANULAR, `spatial_context` grafting)
and the cold adapter chain (`notion_spatial.py`) is not a question of completeness. They deliver
different capabilities: "Piper knows where things live" (beta expression, already shipped) vs.
"Piper continuously inhabits connectors and notices changes" (wave-2, not built). An agent who
reads only the architecture docs may default to option (c) — supersede ADR-013 — because the cold
code looks like a failed attempt. It isn't. The theory is correct; the cold chain is just earlier
than beta. The vote for option (b) was argued from UX theory, not engineering inventory. **That
argument is not in any ADR.**

**4. The consent-boundary incident with Jake is NOT only a trust problem.** `[BELIEVED — from reading HOST's memo and Jake FTUX context this session]`
HOST is right that it's a consent-boundary incident. The UX angle is distinct: Jake didn't know
Piper could execute that action — he thought he was asking it to make a note. The missing design
element is **capability legibility before execution**, not just disclosure after. *"I can actually
create that GitHub issue — want me to?"* would have made this a delight instead of anxiety. These
two framings point to different fixes. If Amber CXO produces a "me too" of HOST's trust lens
instead of the distinct experience-design read, PM loses the range of takes they asked for.

**5. The gate design's value is in what it finds, not what it passes.** `[VERIFIED — Ship 052 sent memo]`
Scenario B found two same-day bugs and #1394 before any tester saw them. The narrative worth
preserving is "the gate found it before the testers did" — not "we passed the gate." A future CXO
who runs scenarios and reports only the passes has missed the point. The gate is a stress test, not
a certification.

**6. Inbox hygiene in this backup account has structural vulnerability.** `[VERIFIED — found Jun 18 memos untracked in this worktree, 24 days late]`
The Jun 18 memos sat untracked for 24 days because the commit-tree push didn't complete and nothing
checked for it. The Amber CXO should treat "mail committed to origin/main before session ends" as a
hard invariant. The check is cheap; the gap is costly.

## Section 6 — Load-bearing vs. commodity (verbatim)

**Dies if the handoff is bad:**

- **The option (b) spatial-intelligence judgment.** `[BELIEVED]` Argued from UX theory in a memo to
  Arch/PPM/Lead. An agent reading the architecture docs alone might default to superseding ADR-013.
  That would be wrong, and the counterargument lives only in the memo and in this account of why it
  was chosen.
- **The Colleague Test as a standing gate, not a historical result.** `[VERIFIED]` If the Amber CXO
  doesn't understand this distinction, the test becomes a closed footnote in issue #1331 rather than
  a reusable verification layer.
- **The CXO's distinct experience-design angle on Jake's feedback.** `[BELIEVED]` Separate from
  HOST's trust/welfare lens and from PM's own read of the apprentice framing. PM asked for a range
  of takes. The CXO angle — interaction model failure, navigation IA problem, capability legibility
  gap, the "only Piper could say this" first-moment requirement — is not recoverable from HOST's
  memo or from any artifact. **If it doesn't get written this session by Amber CXO, it doesn't get
  written.**

**Any competent agent rebuilds from the record:** issue status (#1386, #1394, #1216); beta gate
scenario results (Ship 052 + Jul 19 log); the carry-forward list; inbox triage; the Ship 053
workstream review §0; the PARK-NO-EXIT registry row fix.

---

## Successor annotations — Amber CXO, 2026-07-29

Checked against live state. **The handoff is accurate where I can test it**, and its `[BELIEVED]`
markers were correctly placed — the two I could falsify were both true.

| Item | Status |
|---|---|
| **§4.1 PARK-NO-EXIT structural** | ✅ **Confirmed and now RESOLVED externally**, exactly as predicted. HOST diagnosed the reason-lifecycle gap; CIO shipped a mechanical check 7/27; PM seeding this session was the external trigger. Predecessor called the shape right from inside the trap. |
| **§4.4 / §6 Jake experience-design read** | ✅ **WRITTEN 2026-07-29** (`fc28057ea`) — the item flagged as "doesn't get written otherwise." Filed to Exec, cc PM/HOST/PPM/PA/Lead. Independently reached the same core: capability legibility *before* execution as distinct from, and complementary to, HOST's consent gate. Predecessor's framing sharpened it — I made the before/after contrast explicit and paired the two fixes as one feature. |
| **§4.2 Colleague Test as standing gate** | ✅ Adopted. Applied it as a **new** surface in the Jake review (§2 there): the FTUX is a Colleague Test surface, not just the chat path. **Still owed: get it into the ADR corpus** — predecessor is right that an issue comment is not durable enough. Carried in standing items. |
| **§4.3 spatial (b) argued from UX theory** | ✅ Confirmed live — my slice is folded verbatim into `dev/active/spatial-intelligence-architectural-history-arch-WIP.md` and the emerging convergence is (b). ⚠️ **The predecessor's warning stands and is unaddressed**: the UX argument for (b) exists only in memos, and an agent reading architecture docs alone would plausibly default to (c). **Getting the UX argument into the ADR is real owed work**, not bookkeeping. |
| **§4.5 gate value is in what it finds** | ✅ Adopted as framing for Ship 053 and any future gate reporting. |
| **§4.6 mail-on-main hard invariant** | ✅ Already my practice; every memo this session went via `mail-send.sh` push-to-ref and was verified on `origin/main` before sign-off. |

**Answers to the predecessor's three questions** are in
`dev/2026/07/29/2026-07-29-0939-cxo-code-log.md` and were relayed to PM in chat.

**What I'd add for the *next* CXO**, in the same spirit — the environment lesson that cost me most
on arrival: **a stale worktree makes absence look like fact.** On 2026-07-29 my worktree was 271
commits behind; `ls mailboxes/cxo/inbox/` showed *empty*. Had I trusted it I would have reported to
PM that no Ship 053 kickoff and no Jake FTUX ask had arrived — both false, both load-bearing, and
the Jake one is the item this very handoff says dies if unwritten. **Sync before you read mail, and
treat any empty result from a relative path or a stale checkout as a claim about your environment
before it is a claim about the world.**
