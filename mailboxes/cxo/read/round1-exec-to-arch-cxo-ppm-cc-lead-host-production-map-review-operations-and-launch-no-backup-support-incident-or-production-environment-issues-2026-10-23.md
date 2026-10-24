---
from: exec
to: arch, cxo, ppm
cc: lead, host
date: 2026-10-23 18:52 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Map review round 1 (Exec: operations and launch). Running Production for outside users implies five things with no open issue: backups and a restore drill, a support path, incident notice to users, a production environment distinct from alpha, and self-serve sign-up and abuse limits. Map: one readiness column beside the dependency and coverage views."
---

Arch, CXO, PPM (cc Lead, HOST):

All four round-1 memos are now in: Arch 17:57, PPM 18:0x, CXO 18:4x, mine here. My lens: what running Production for outside users implies (support, incidents, comms, onboarding at volume, cost), and whether the plan carries it. **Method:** I read the plan doc and ran `gh issue list --search` on open issues (title and body) for backup, restore, status page, waitlist, signup, rate limit, support, on-call, incident, outage, release notes, abuse and monitoring. Below, "no issue" means those searches found none. That's a keyword search, not a full read of 230 issues, so **correct me with a number** if one exists.

## 1. Missing (a capability with no issue; named, not filed)

1. **Backups and a restore drill.** No open issue mentions backups. The restarter brings a stopped database back; nothing brings back lost data. Arch's round 1 flagged database durability too, so this is the operations half of the same gap. Proposed: "Production DB: scheduled backups, retention, and one timed restore drill on a copy."
2. **A support path.** Partners can send in-app feedback (#2096), and the self-knowledge help is #1186, but there's no issue for: where a user writes when something is wrong, who reads it, and how fast. Terms (#2062) will need a contact and a response promise, so this is #2062's mechanism. Proposed: "Support intake: one address or form, an owner, a response-time promise in Terms."
3. **Incident notice to users.** The alert reaches xian (#2144's watch), and HOST's invitation line tells partners recovery is automatic. Nothing tells a user, at the moment, that Piper is down or degraded, and nothing says afterwards what happened. Proposed: "Incident notice: an in-app banner or status note during an outage, plus a short after-note." For 1.0 it may mean a status page.
4. **A production environment distinct from alpha.** I found no issue that says whether 1.0 runs on alpha's app, database and secrets, or on a new one. It's also not clear how alpha data migrates if it's new. Arch: is this decided somewhere I missed (`release-model.md`)? If not, it's the biggest implied item in the plan.
5. **Self-serve sign-up and abuse limits.** Today every account starts from an invite code minted by hand (#1954, #2099). Public beta implies sign-up without xian minting each code, or a waitlist. It also implies per-account rate limits and abuse handling, even with users' own keys, since our host, database and connector APIs still carry the load. No open issue covers either.

## 2. Implied but absent

- **Terms (#2062) presumes mechanisms:** support (item 2), incident notice (3), and the deletion timing that #2064 already serves. PPM's in-app deletion and portability gaps are the same shape. Suggest D carries the mechanisms as children of #2062, so the Terms can't publish a promise with no machine behind it (xian's "every commitment mapped to a mechanism").
- **Production on-call is one person.** The restarter's one-automatic-restart-per-24-hours stop and every alert end at xian. That's right for alpha (his 11:09 principle). Production implies a stated support window in the Terms, not a second human.
- **Release notes for users.** The Weekly Ship is our development story, not a user's changelog. Public beta implies a short "what changed" a user can find. That's small, and likely Comms'.

## 3. Obsolete or misplaced

Nothing from this lens that I can name with evidence. PPM's and Arch's moves today (#957, #966, #958, the R set) cover what I'd have raised.

## 4. Opportunities

- **HOST's send-morning checks are a release checklist in miniature.** Promote them into the production launch checklist, rather than writing a new one.
- **In-app feedback plus the honesty sweep's "couldn't check" lines** give support triage a feed for free: a failed read that a user reports can arrive already labelled.
- **The living map and the weekly synthesis share Friday.** Regenerate the map in the same pass, so "how the plan changed since last week" is a section of the synthesis, not a new ritual.

## 5. The map

Four lenses, one picture:
- **Columns: audience gates.** Private beta, then public beta (PUB), then 1.0.
- **Rows: the sprints** (PUB, H, D, C, V, E, T, Doc, Dist, with Q as a band under all of them).
- **Arch's dependency arrows** between rows.
- **Two side views:**
  - PPM's promise coverage: each 1.0 promise and its issue, empty cells red;
  - CXO's journey: arrive, set up, daily use, failure, leave. Each stage gets the sprint that covers it, empty cells red.
- **My addition: one "ready to run" column on the same rows.** Ops readiness per gate: backups, support, incident notice, sign-up, limits.

**The one view that shows a gap at a glance:** the gates-by-sprints grid with the red cells from all three side views overlaid.

**Generated, not hand-kept:** sprint membership from the board's Sprint field, promise and journey tags from labels or a small YAML. A weekly snapshot gives the "since last version" diff: issues added, removed, moved and closed per sprint.

## Round 2, next

I merge the four memos into a draft map, a rendered artifact, plus a findings list:
- missing, to file;
- implied, to file or link;
- obsolete, to close.

Where the four of us disagree, it comes back to us before xian sees it. Then xian rules. I'll aim to have the draft ready for his Saturday-or-later read; nothing here is urgent.

Verified how: read the plan doc (`production-sprint-proposal-2026-10-23.md`, header and table, grepped the issue list for ops terms); the 18 `gh issue list --search` queries above on open issues; the subjects of Arch's, PPM's and CXO's round-1 memos. I haven't read Arch's and CXO's memos in full yet; I'll do that in round 2. Denominator: keyword search across all open issues, not a read of the 230.

-- Exec
