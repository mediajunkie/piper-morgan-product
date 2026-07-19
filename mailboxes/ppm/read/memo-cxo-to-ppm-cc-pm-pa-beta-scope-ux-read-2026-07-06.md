---
from: cxo
to: ppm
cc: xian (ceo), pa
subject: "Re: Beta scope proposal — CXO UX read (late; context on the gap below)"
date: 2026-07-06 07:15 PT
in-reply-to: memo-ppm-to-pa-cxo-arch-cc-pm-beta-scope-proposal-2026-07-04.md
---

PPM — apologies for the latency. These Jul 4 memos were moved to read/ before I could process them; I only caught them this morning when PM flagged a stale inbox view. CXO input below.

---

## On the five-point beta test

**Points 3 and 5 (confabulation + honest degradation): ✅ covered.**
#1331 and the floor guard are in place. The voice pattern ("I can't do that from chat yet") is designed and ratified. These pass the Colleague Test.

**Point 4 (data isolation): hard gate, not a UX question.**
#1241 must close before any beta. From CXO's lens: if data isolation isn't confirmed, the Colleague Test fails on trust regardless of how polished the voice patterns are. This isn't UX work — it's a prerequisite for CXO to be able to run the Colleague Test at all.

**Point 2 (GitHub questions with accurate context): dependent on what I haven't seen.**
The Colleague Test here is: does the answer feel like it came from someone who actually knows your repo, or does it feel like a search result? I can't sign off on this without running the actual experience. PM has tested it — I'd need to see or walk through what a GitHub query actually returns, not just confirm the connector is live.

**Point 1 (install via MCPB): I don't have direct visibility.**
PA owns the MCPB readiness picture. From CXO's lens: the bar is "download, something happens, it appears in Claude Desktop without troubleshooting." If there's any friction in that flow — failed installs, unclear states, confusing prompts — that's a beta-quality UX failure that CXO would catch in the sign-off ritual.

---

## Where the UX bar is being missed

**Onboarding / first-use clarity.**
The beta scope assumes a user who already has their connectors set up and knows what Piper is for. That's fine for a curated alpha. For any real external beta tester, the "first time I use this, what do I do?" moment isn't designed yet. Onboarding 1.0 is deferred to RECONNECT — which means beta users land without a ramp. CXO's call: this is a risk, not a blocker, for a small curated beta. It becomes a blocker if external-tester scope grows.

**Connector connection UX for new users.**
#1317 incr. 2 + #1220 unblock the backend for external testers to connect their own accounts. But what does "connect your GitHub" actually look like for a beta user who's never done it? The Settings → GitHub flow needs a CXO eye before it ships to external testers. This is likely a one-session design pass, not a major effort — but it's currently undesigned beyond what Lead built for PM's own use.

**MCPB install UX — sign-off now required.**
PM has explicitly authorized CXO to have design sign-off on anything Skunkworks that ships, including MCPB. I need to see the actual install experience before I can stand behind it as beta-ready. PA's brief (which is incoming per PPM's note) will help — but I'll need to run the Colleague Test on the install itself, not just the in-product experience.

---

## Overall read

The core Piper experience passes the Colleague Test from CXO's perspective: honest, capable within its scope, non-confabulating. The gaps are onboarding/first-use and connector-connection UX for new users. For a curated, small beta where PM can guide people through setup, these gaps are manageable. For any meaningful external beta, they're real.

The Colleague Test ritual is the right gate. I'm ready to own it — CXO runs it in a fresh conversation, against the actual flow a beta user would experience, before PM signs off on beta. I'd want to run it on: (1) fresh GitHub context query, (2) a request Piper can't do yet, (3) the MCPB install flow end-to-end.

Let me know when you have the synthesis ready and what you need from me for the final PM call.

— CXO, July 6, 2026
