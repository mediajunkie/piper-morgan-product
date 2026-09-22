# Alpha Tester Invitation Email Template

**Version**: 3.0
**For**: Piper Morgan 0.8.13.0 Alpha Release (hosted)
**Purpose**: Internal template for PM to send to invited alpha testers
**Last Updated**: September 21, 2026

**v3.0 rewrite (2026-09-21, Lead — closes #1830)**: v2.x of this template described the
retired local-install flow (clone, Docker, Python, guided setup calls) and told
prospects a hosted version was "planned for later in 2026" — while the hosted alpha at
`alpha.pipermorgan.ai` has been the actual tester surface since July. This version
matches reality: **invite code → account → paste your LLM key → chat.** HOST drafts the
live invite email against the current roster; this template is the canonical baseline
they adapt — if the two drift, fix THIS file and re-derive.

---

## Subject Lines (A/B test these)

- "Your Piper Morgan alpha invite"
- "Piper Morgan alpha access — your invite code inside"
- "[Name], your Piper Morgan alpha account awaits"

---

## Email Template

```
Hey [Name],

You mentioned interest in testing Piper Morgan — excited to have you as an early alpha
tester!

Piper Morgan runs as a hosted app now, so there's nothing to install. Getting started
takes about ten minutes:

**GETTING STARTED**

1. Go to https://alpha.pipermorgan.ai/setup
2. Create your account — you'll need this invite code (single-use, just for you):

   [INVITE_CODE]

3. Log in, then open Settings → LLM Keys and paste an API key of your own:
   - an Anthropic key (https://console.anthropic.com/), and/or
   - an OpenAI key (https://platform.openai.com/api-keys)
4. Say hello.

**THE ONE REAL REQUIREMENT**

Piper runs on YOUR LLM key and bills YOUR account — it never spends anyone else's.
That's a design principle, not a limitation: your data and your costs stay yours.
Budget roughly $5–20 in API usage over the alpha period, and keep an eye on your
provider's usage dashboard (that's also a great way to verify the promise!).

Optional, for the integration features: a GitHub personal access token, a Notion API
key, or a Slack workspace — all connectable later under Settings → Integrations.
None are needed for core chat, lists, files, or standups.

**CRITICAL DISCLAIMERS**

This is ALPHA software (version 0.8.13.0). That means:
- It will have bugs and rough edges
- The alpha instance's data may be lost at any time — use test data only
- Security is not fully audited (your API key is stored encrypted; content at rest
  is not yet encrypted)
- You're responsible for your own API charges
- Not for mission-critical work or sensitive information

The full terms are in the attached Alpha Agreement — please read it before diving in.

**WHAT TO EXPECT**

Week 1: try it on real-ish PM work (test data!), tell me what confused you
Week 2-3: you test, I fix what you find
Week 4+: quick weekly check-ins if you're up for them

One thing we care about more than anything: **if Piper ever tells you something that
turns out not to be true — about your data, your tools, or what it just did — that's
our top-priority bug class.** Polite lies count double. Please report those first.

**STILL INTERESTED?**

Reply with:
1. Which LLM provider you'll use (Anthropic / OpenAI / both)
2. Your biggest PM pain point you hope Piper helps with
3. Anything that blocked or confused you in the first ten minutes

Best,
Christian

P.S. We're keeping the alpha cohort small so I can provide proper support — your
invite code is single-use and yours alone.
```

---

## Follow-up After First Login

```
[Name],

Great — saw you're in! A few pointers for the first real session:

**WORTH TRYING FIRST**
- "let's do my standup" — the guided interview builds a standup from your words
- Upload a PDF or DOCX and ask for a summary
- "Add a todo: [something real-ish]" then "what tasks do I have?"
- Connect GitHub under Settings → Integrations if you want issue features

**THE DOCS** (attached / linked)
- ALPHA_QUICKSTART.md — the 2-minute version of everything above
- ALPHA_TESTING_GUIDE.md — test walks for this release
- ALPHA_KNOWN_ISSUES.md — don't waste time on what we already know
- ALPHA_AGREEMENT_v2.md — the terms you acknowledged

Looking forward to your feedback — you're helping shape the future of AI-assisted PM
work.

Best,
Christian
```

---

## Template Variables

**Customize these for each tester:**

- `[Name]` — tester's first name
- `[INVITE_CODE]` — mint via the Lead-owned mechanism (`scripts/mint_prod_invite.sh`
  against the alpha DB — **Fly-hosted since 2026-09-22**, access grant-gated; see the
  cutover runbook + `docs/internal/operations/` runbooks). Single-use; HOST records
  who received which code (trust-zone split: Lead mints, HOST records identity,
  PM sends).

---

## Sending Checklist

Before sending:

- [ ] Mint a fresh invite code (never reuse; never send the same code to two people)
- [ ] Personalize the name
- [ ] Verify all technical claims are current for version 0.8.13.0
- [ ] Attach/link current documentation (from docs/)
- [ ] HOST records the invitee ↔ code pairing in the roster (PII stays out of the repo)

---

## Notes

**Email Tone**: friendly but honest about alpha status. Set realistic expectations
upfront.

**Documentation References**: always reference official docs by filename
(`ALPHA_TESTING_GUIDE.md`, `ALPHA_AGREEMENT_v2.md`), and versions by number
(0.8.13.0, not "latest").

**Support Commitment**: only promise what you can deliver. Small cohort is what makes
close support possible.

---

## See Also

- `../../ALPHA_QUICKSTART.md` — what the tester's first ten minutes look like
- `../../ALPHA_TESTING_GUIDE.md` — what testers receive for depth
- `../../ALPHA_AGREEMENT_v2.md` — legal terms testers acknowledge
- `../../VERSION_NUMBERING.md` — version scheme documentation

---

_Template Version: 3.0_
_For Software Version: 0.8.13.0_
_Last Updated: September 21, 2026_
