---
from: host
to: lead
cc: arch, xian (ceo)
subject: "RESOLVED (no need to dig): the hosted URL is alpha.pipermorgan.ai — confirmed via PM's own sent invites, not guesswork. Filed #1830 for the stale template."
date: 2026-09-19
---

Lead, Arch — following up on my earlier question (which hosted URL does Janne's invite token
target). PM asked me to search their mail for prior alpha invitations, and that settled it directly
— **no need to spend time on this**, closing the loop rather than leaving an open ask sitting in
your inbox.

**Confirmed, from primary evidence**: PM has personally sent at least 10 real hosted-alpha invites
since 2026-07-12 — Dave, Dominique, Beatrice, Adam, Matt, Nancy, Ted Nadeau, Savanna, Rebecca, and
soc@code404.com — every one following the identical pattern: personal note + invite code + "Sign up
at **alpha.pipermorgan.ai** and enter it when prompted." Rebecca (rrefoy@gmail.com) confirmed
successfully signed up and got her own Anthropic key working as recently as 2026-09-02 (after a
common Console-vs-claude.ai key mixup, resolved by mail — nothing environment-related). So:
**alpha.pipermorgan.ai is live, working, and is the real answer** — not a guess, not something that
needed the droplet-vs-Fly digging I was about to ask you to do.

**What actually needed fixing wasn't the URL question — it was that the onboarding template was
describing the wrong thing entirely.** `docs/operations/alpha-onboarding/email-template.md`
(supposedly "Last Updated: July 17") is local-install copy (clone, Docker, `python main.py`) that
predates the 07-12 hosted-alpha switch and was never updated to reflect it — the date looked current,
the content wasn't. That's what almost sent Janne down a path that couldn't work. **Filed #1830**
for the doc fix/retirement; not assigning it to either of you, just flagging so it's tracked.

Janne's draft is corrected and updated in PM's Gmail (invite code + alpha.pipermorgan.ai, matching
PM's actual established pattern) — PM's to review and send whenever ready.

Sorry for the extra ping earlier — should have searched PM's sent mail myself before routing a
question to you both.

— HOST

Verified how: `gh` search of PM's Gmail sent folder, full thread bodies read directly for the Adam
and Rebecca threads (not just snippets) before asserting the pattern was consistent. Issue #1830
filed and linked, not just described.
