# Alpha Tester Pre-Qualification Email Template

**Version**: 2.7
**For**: Piper Morgan 0.8.11.0 Alpha Release
**Purpose**: Internal template for PM to send to potential alpha testers
**Last Updated**: July 17, 2026

---

## Subject Lines (A/B test these)

- "Ready to test Piper Morgan? Check requirements first"
- "Piper Morgan alpha access - Prerequisites inside"
- "[Name], before we set up Piper Morgan..."

---

## Email Template

```
Hey [Name],

You mentioned interest in testing Piper Morgan - excited to have you as an early alpha tester!

Before we schedule setup, let's make sure you have everything needed. The good news: we've built a visual setup wizard that makes initial configuration much easier.

**PREREQUISITES CHECKLIST**

Technical Requirements:
□ Comfortable using command line/terminal (for initial clone and install)
□ Python 3.11 or 3.12 installed on your machine
□ Docker installed and running
□ Git installed and working
□ About 1GB free disk space
□ 30-45 minutes available for guided setup (includes Docker installation if needed)

Accounts & API Keys You'll Need:
□ GitHub account
□ At least one LLM API key:
  - OpenAI (GPT-4 preferred) -OR-
  - Anthropic (Claude) -OR-
  - Google Gemini
  (You can configure multiple providers)
□ Budget $5-20 for API testing costs
□ Notion account (optional but recommended)

**WHAT MAKES THIS EASY (0.8.11)**

Our GUI setup wizard (`python main.py` → opens in browser) will:
- Check your system automatically (Docker, Python, ports, database)
- Show results visually with clear status indicators
- Guide you through API key configuration in a web form (much easier than CLI)
- Guide you through account creation with real-time validation
- Validate your API keys before storing them
- Set up the database and services for you
- Take about 10-15 minutes total (or 30-45 minutes if Docker installation is needed)

Once set up, your API keys and provider choice are genuinely yours: keys are stored per-user and encrypted at rest, and every chat request uses YOUR chosen provider — one tester's setup can't affect another's. The personality questionnaire (`python main.py preferences`) shapes how Piper talks to you: tone, confidence, level of detail. And when something goes wrong — an invalid or out-of-quota API key, a data source Piper can't reach — Piper tells you honestly what happened instead of guessing or claiming there's nothing there.

After setup, you can optionally configure your preferences (`python main.py preferences`) to personalize how Piper works for you.

**CRITICAL DISCLAIMERS**

This is ALPHA software (version 0.8.11.0). That means:
- It will have bugs and rough edges
- It might crash or lose data
- Security is not fully audited (API key secrets are encrypted; content/PII at rest not yet encrypted)
- You're responsible for your API charges
- Not for mission-critical work
- Not for employer machines (without permission)

**WHAT TO EXPECT**

Week 1: Guided setup call (30 mins) + initial testing
Week 2-3: You test, I fix bugs you find
Week 4+: Quick weekly check-ins

Setup, login, and core features are stable in 0.8.11.0. **Focus your testing on**: the personality questionnaire (re-answer it once after updating — earlier answers were lost to a bug — then check whether Piper's tone reflects your choices), provider selection (set your own key and provider in Settings → LLM Keys and confirm chat uses it), greetings with a question attached (the question should get answered), "connect my GitHub"-style requests (should get real guidance, not a decline), and status/agenda answers (claims about your todos should be honest — "I couldn't check" is fine; a false "nothing found" is a bug). The goal is finding PM workflows that delight you, despite the rough edges.

**STILL INTERESTED?**

Reply with:
1. Which LLM provider you'll use (OpenAI/Anthropic)
2. Your biggest PM pain point you hope Piper helps with
3. Best time for a 30-min setup call (recommended for first-time setup)

If this feels like too much technical setup, totally understand! We're planning a hosted version for later in 2026.

Best,
Christian

P.S. We're keeping the alpha cohort small so I can provide proper support.
```

---

## Follow-up After Confirmation

```
[Name],

Perfect! You're confirmed for Piper Morgan alpha access.

**NEXT STEPS:**

1. Review the attached Alpha Testing Guide (streamlined setup instructions)
2. Read and acknowledge the Alpha Agreement (legal stuff)
3. Gather your API keys
4. Our setup call is [DATE/TIME] (calendar invite coming)

**WHAT TO PREPARE:**
- Your LLM API key ready to paste
- A test PM task/project (nothing sensitive)
- Questions about what Piper can/can't do
- Patience for alpha software quirks

**SETUP PREVIEW:**
We'll run `python main.py` together, which opens the GUI setup wizard in your browser. It handles:
- System verification (Docker, Python, database) with visual indicators
- API key configuration via web form (much easier than CLI)
- Account creation with real-time validation
- Service initialization

The visual interface makes setup straightforward. Optionally, you can run `python main.py preferences` to personalize your experience.

Looking forward to your feedback! You're helping shape the future of AI-assisted PM work.

Best,
Christian

Attachments:
- ALPHA_TESTING_GUIDE.md (comprehensive setup guide)
- ALPHA_AGREEMENT.md (legal terms)
- ALPHA_QUICKSTART.md (minimal 2-minute guide)
- ALPHA_KNOWN_ISSUES.md (current bugs and limitations)
```

---

## Template Variables

**Customize these for each tester:**

- `[Name]` - Tester's first name
- `[2/3/4]` - Tester number (keep cohort small)
- `[DATE/TIME]` - Scheduled setup call
- `[domain]` - Your actual email domain
- `christian@[domain]` - Your actual contact email

---

## Sending Checklist

Before sending:

- [ ] Personalize name and tester number
- [ ] Verify all technical claims are current for version 0.8.11.0
- [ ] Attach current documentation (from docs/)
- [ ] Schedule setup call before sending confirmation
- [ ] Update internal tracking (who's in alpha cohort)
- [ ] Mention the personality questionnaire, per-user provider choice, and the honesty fixes as key new features

---

## Notes

**Email Tone**: Friendly but honest about alpha status. Set realistic expectations upfront.

**Documentation References**: Always reference official docs by filename:
- `ALPHA_TESTING_GUIDE.md` (not "the guide")
- `ALPHA_AGREEMENT_v2.md` (not "the legal doc")
- Version 0.8.11.0 (not "alpha" or "latest")

**Support Commitment**: Only promise what you can deliver. Small cohort (2-5) is manageable for close support.

**Technical Prerequisites**: Don't sugarcoat - command line comfort is required. Better to filter out now than frustrate later.

---

## See Also

- `../../ALPHA_TESTING_GUIDE.md` - Reference for what testers will receive
- `../../ALPHA_AGREEMENT_v2.md` - Legal terms testers will see
- `../../VERSION_NUMBERING.md` - Version scheme documentation
- `../../ALPHA_QUICKSTART.md` - Quick reference guide for testers

---

_Template Version: 2.7_
_For Software Version: 0.8.11.0_
_Last Updated: July 17, 2026_
