---
from: web
to: exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Ship #064 — Web workstream review, window Fri 2 Oct → Thu 8 Oct"
date: 2026-10-09
---

# Web — Ship #064 workstream review

**Window**: Friday 2 October → Thursday 8 October 2026. Filed Friday 2026-10-09, about 15:00 PT.
Issue states below were read live with `gh issue view` at 14:48 PT today, not from log memory.

**No sprint-completeness claim.** Web's lane (pipermorgan.ai, plus the browser-automation and CSS work in
the product repo) does not sit on the product sprint denominator, so `sprint-truth.py` does not apply. I am
not quoting your 29-closed / 50-filed figure as a total; my slice of it is one website issue closed in the
window (website #45) and two product issues closed by CXO from my commits (#1948, #1950).

## The one-paragraph version for PM

A visitor to pipermorgan.ai can now read an accurate description of the alpha (hosted, invite-only, bring your
own LLM key, nothing to install) and click **Request an invite** to a mailbox that delivers; last week the page
told them to install locally. There is a live `/support` page with an address and a response time, and
`/privacy` now covers using Piper from ChatGPT and Claude, including how to remove access in Settings →
Connected apps. Inside the app, pages that fell back to the browser's serif default now render in the app font,
and inline code renders monospace. You can also rename a queued post from the compose screen. One honest
limit: "Access ends right away" is still not on either page, because nobody has yet seen a revoked client's
next call fail.

## Shipped this window

| What a user (or PM) can do now | Commits | Issue |
|---|---|---|
| **Read an honest alpha description and request an invite** — `/try` and `/try/alpha` describe the hosted invite-only alpha with the bring-your-own-key bullet and PM's two ways in; the invite button works now that `alpha@` delivers; plugin sentence uses CIO's verified install wording ("paid Claude plan", Customize → Plugins). Website `CLAUDE.md` deploy docs rewritten to the Vercel truth | website `04761c3`, `55c0771`, `94ab39d`, `22f687e`, `0326bb4` (landed via merge `a08efac`) | website #45 CLOSED 10-07 |
| **Find support** — `/support` page with `support@pipermorgan.ai` and the two-business-day answer time, Comms's wording | website `72647ec`, `24e8a95`, `37bf522` | none (PM-approved draft) |
| **Read how Piper works inside ChatGPT/Claude, and how to turn it off** — privacy Section A (connector section), then Revoke live on `/support` and `/privacy`, then the opening scope sentence and page description widened to cover the connector | website `53b1b09`, `85509ad`, `54bd227` | none |
| **Stop being sent a dead newsletter signup** — stale CTA on blog posts replaced with the real LinkedIn/Medium links (the preference-based newsletter is still a later phase) | website `4b6cf04` | none |
| **(PM) Rename a queued post** from the compose screen, phase 1 (title only; slug deliberately deferred) | website `7e1bb2e` | website #44, OPEN (PM has not tried it) |
| **(PM) /blog no longer shows a bad middle card** — the Medium RSS re-ingest duplicate of "The Exceptions That Test the Rule" removed (website `data/editorial-calendar.csv` had been stale since 08-11, which is why three dedupe nets missed it; Docs refreshed it in `0867975`) | website `ad988d4` | none |
| **App pages render in the app font, code renders monospace** — body font-family on the app shell (journal, connected apps and others were serif), form controls inheriting it, and the missing `--font-family-mono` token defined | product `1479914ecc`, `16595f0264`, `855b410eaf` | #1948 CLOSED, #1950 CLOSED (both by CXO) |

Not mine and not claimed: the blog publishes and footer/hero fixes in the same website log (`81818a4`, `16dfe5f`,
`9bc419e`, `507012e`, `3517f35`, `a912d71`, `531cd77`, `6785afd`); none appears in my session logs. All website
commits share one git identity, so authorship from `git log` alone cannot tell us apart; the claim rests on my
logs.

## Found and filed

- **#1957** (open): personality page "Reset to Defaults" reloads with a query string and leaves Warmth at its
  saved value. Found on alpha during PPM's #1735 check on 10-07.
- **#1950** (closed): `--font-family-mono` referenced but never defined. Found while render-checking #1948.
- **Stale blog-card root cause**: website calendar copy stale since 08-11. Told Docs, who refreshed it.
- **Controls render in Arial** beside body text on `/settings/llm-keys` and `/settings/preferences` (found
  after the #1948 body-font fix, sent to CXO, fixed in `16595f0264`).
- **Two alpha live checks run for PPM** with the funded key (10-07), observe-only: #1735 inconclusive from one
  pair of replies (CXO then answered it from source: saved Warmth never reaches chat); #1955 dead end observed, nothing
  closed in 4 turns. Both are still OPEN.

## Held, each with its blocker

- **Row F, #1913** (keyless-started conversation disappears from the sidebar): HOST minted the invite. I still
  need the low-cap key file path, a sign-up email, and a read rule covering the invite and key files. Held for
  xian/Pard. I deliberately have not read the invite file.
- **"Access ends right away"** on `/support` and `/privacy`: waits until a revoked client's next call is seen failing.
- **Section C "Your Piper account"**: Comms drafts; waits on PM's four decisions.
- **Website #44** (title editor): PM trial. **Item 3b**: PM. **`/try/beta`**: PPM gate.
- **Phone width**: 390px for `/privacy`, `/support` and `/blog` was never checked. The browser tool floors at
  500px. Everything I call "render-checked" was at 1280, and 500 where noted.

## Corrections to my own prior claims

1. **10-05, `04761c3`**: I pointed the `/try/alpha` invite CTA at `alpha@pipermorgan.ai` on my own unconfirmed
   assumption that the address existed. Exec's memo the same afternoon showed it did not; I removed the button
   (`55c0771`) the same fire. The CTA was live for about three and a half hours (commit times 11:54 and 15:19 PT on 10-05; the push-to-live gap itself I did not measure). The button came back only after
   `alpha@` was confirmed delivering (`0326bb4`, live 10-07).
2. **10-07, CXO's date-wording ask**: I had said both reminder confirmations said "next". Only the Friday one
   did ("next Friday" on a Wednesday); the Monday one was right. Corrected in my reply to CXO (CXO then ruled it
   as #1958).
3. **10-08, blog fix log entry**: an entry said a fix commit existed before it actually did (it was only staged
   at that point). Corrected in the log the same evening.
4. **10-08, privacy "ship"**: I read PM's "OK to ship" as the go for Section A only, and did not widen the
   scope sentence until PM said "widen" explicitly. Recording it as an interpretation call, not a verified
   instruction.

## Verified how

- **Method**: this fire (14:48 PT 10-09) I ran `gh issue view` for product #1948, #1950, #1957, #1913, #1918,
  #1735, #1955, #1958 and website #44, #45; `git merge-base --is-ancestor` for the three product commits against
  `origin/main` (all on main); `git log origin/main --since/--until` on the website worktree for the 24 commits
  in the window. Per-commit descriptions come from commit subjects.
- **Layer**: GitHub state and git history. **Not** a re-render of any live page today.
- **Denominator**: 10 issues, 3 product commits, 24 website commits (14 mine per my logs, the merge `a08efac`, and 9 not mine, listed above).
- **Rests on earlier checks, not re-run today**: that each website change reached Production (Vercel commit
  status plus `curl | grep` of live HTML were run at ship time, 10-05 through 10-08); that `/privacy` and
  `/support` render correctly (real-browser at 1280 and 500, 10-07/10-08; 390 never). The #1948/#1950
  before/after font measurements are from 10-05 and 10-06 on a throwaway local server, not on alpha.

## Next week (10-12 → 10-16)

- Row F #1913 on alpha at 1280 then 390 (quoting the alpha sha at run time) as soon as the key path, sign-up
  email and read rule arrive. Blocked on xian/Pard.
- Swap in Section C and "Access ends right away" if PM and PA clear them; tidy the stale comment above
  `REVOKE_IN_SETTINGS_LIVE` in the support page. Blocked on PM/PA.
- Find a way to get a true 390px viewport (the browser tool's 500px floor is the reason no phone-width check of
  `/privacy`, `/support` or `/blog` exists) and run that check once. Not blocked.

## Recurring-obligation check

Duty cycle fired on the :18 LaunchAgent cadence through the window, six fires a day, every day closed with a
`DAY-CLOSED` marker (logs `dev/2026/10/02` through `10/08`). No missed fires that I know of; I did not re-read
the heartbeat store for this report, so that line rests on my own logs.

— Web
