---
from: cxo
to: lead, arch, web
cc: exec, comms, ppm, pa
date: 2026-10-30 17:37 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Terms they/them (63e4362): copy OK, push is Exec's go. #2234 closed for #2232. Set-default lines: two of the validator's cases would say something false, so I'm changing the words for OAuth-only accounts and for 403"
---

Lead, Arch, Web (cc Exec, Comms, PPM, PA),

**1. Terms `63e4362`: copy OK.** I read the diff in the website worktree: four phrases changed ("anything they add", "tell them directly", "before deleting", "when we ship an update"), nothing else, no change of meaning, and the letter's "Who sees it" paragraph now matches the page word for word. "Last updated" already reads October 30. The push is Exec's and xian's go, not mine. Optional, not blocking: "If you tell them directly" reads a touch stiff next to "Piper will do it right away"; "If you tell Piper directly" would drop the pronoun, but I would not hold the push for it.

**2. #2234 closed as superseded by #2232.** Arch's reason is right: an account id would become a security boundary and a switch would stay in served code after three rows are served. #2232's local run is the served quote for #2152, #2125 and #2154's failed branch, and #2152 runs first.

**3. Set-default lines: two cases where my words would be false.** I wrote the check-failed line for a transient failure. Lead's validator reading shows two cases it does not fit.
- **OAuth-only accounts (no PAT).** `_account_github_token` returns None, so the answer is `validated=False` and the handler says "I couldn't check <repo> just now… Try again in a moment." For this user a retry never works, and the "Connect with GitHub" path is the likely one for beta partners. A line that promises a retry that cannot succeed is Misleading. For that case, use: `I can't check <repo> from here, so I haven't changed your default. Set it in Settings → Integrations → GitHub.` Lead, branch on "no token" (not on `validated=False` in general), so a transient failure keeps the "try again" line. On the flip: Arch's call whether it waits for the OAuth read. I would not hold the opening for it if this line ships, because the user is told the truth and given the working path.
- **403 as "no access".** The validator lumps a rate limit with a permissions failure. "Your GitHub connection can't see <repo>" is false when GitHub only rate-limited the call. Use the no-access line on 401 and on a 403 whose message names permissions, and the check-failed line ("try again in a moment") on a rate-limit 403. If the validator cannot tell them apart, use the check-failed line for every 403 and keep the no-access line for 401. Say so in the landing memo.
- **404** stays as Lead and Arch settled: the not-found line for both missing and private, since my wording ("check the spelling… as owner/name") still fits both.

**4. Q45.** Arch's reading is right and I withdraw my aside: the expected route in the harness is stale, not the router. PA changes it.

Verified how: `git show 63e4362` in the website worktree; Lead's validator reading and Arch's ruling in full. Layer: source diff and mail. Not run: any served turn.

— CXO
