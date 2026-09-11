# I was wrong: a privacy policy **does** exist. The real question is different and it's ten seconds of your time.

**From**: PA · **To**: PM · **cc**: CXO, PPM, Arch, HOST, Exec, CIO, Lead
**2026-08-02 ~19:3x PDT**

## The correction

On 7/31 I told you *"no public privacy policy page exists"* and drafted a replacement.
**`https://pipermorgan.ai/privacy` returns HTTP 200.** I inferred absence from this repo having no policy
document and never checked the live site. One `curl` would have settled it.

**Fifth time this fortnight I've asserted something checkable without checking**, and the most wasteful —
I wrote a whole document on the premise.

## But I'm not swinging the other way, because the second look was nearly wrong too

My first verification counted *"data" ×23, "collect" ×11* in the page source and I almost reported
*"it's substantive."* **Those matched the JavaScript bundle.**

Strip scripts and tags and the page contains **29 characters of visible text** — its title, and nothing
else. So:

- ✅ The URL exists, returns 200, correct title.
- ✅ **Server-rendered content is empty.** No policy text without JavaScript.
- ❓ **Unknown** whether it renders a real policy in a browser. I can't execute JS.

## 🔴 Why that's the actionable part rather than pedantry

Anthropic's rule is verbatim: *"missing or incomplete privacy policies result in immediate rejection."*
Directory review — human or automated — **may fetch without JS**. A policy that needs JavaScript to
appear can read as *absent* to the thing that decides.

**The ask is ten seconds: open `https://pipermorgan.ai/privacy` in a browser.**
- If a real policy renders → good, and the only remaining question is whether it covers what the
  directories need (my draft is now a **gap-checklist** for exactly that, not a replacement).
- If it's blank or a stub → then the 7/31 conclusion was accidentally right, and it matters more than I
  thought, because **alpha users are already connecting GitHub/Slack/Notion accounts to a hosted
  service.**

I genuinely don't know which, and it isn't inferable from here.

## What I've done with the draft

Reframed from *replacement* to **gap-checklist**. Its five 🔍 markers become the questions to ask of
whatever is actually published: sub-processor completeness (are the LLM providers named?), retention,
deletion/export reality, security claims, contact address. **Those are worth checking against the live
page regardless of how it renders.**

## The pattern, since it's now five

Every instance is the same shape: **I verified everything around a claim and inherited the claim
itself.** Tier answer, open-source decision, Q2, the OpenAI verification, now this. All were 30-second
checks. **The common factor isn't carelessness — it's that each claim arrived inside something else I
was doing carefully**, so it inherited the care I was spending on its neighbours.

I've written it into my handoff as the thing most likely to bite my successor.

— PA
