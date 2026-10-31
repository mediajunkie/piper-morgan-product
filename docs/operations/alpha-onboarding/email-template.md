# Beta Tester Invitation Email Template

**Version**: 3.0
**For**: Piper Morgan 0.9.0.0 Private Beta Release (hosted)
**Purpose**: Internal template for PM to send to invited beta testers
**Last Updated**: October 31, 2026

**v3.0 rewrite (2026-09-21, Lead — closes #1830)**: v2.x of this template described the
retired local-install flow (clone, Docker, Python, guided setup calls) and told
prospects a hosted version was "planned for later in 2026" — while the hosted alpha at
`alpha.pipermorgan.ai` has been the actual tester surface since July. This version
matches reality: **invite code → account → paste your LLM key → chat.** HOST drafts the
live invite email against the current roster; this template is the canonical baseline
they adapt — if the two drift, fix THIS file and re-derive.

---

## Subject Lines (A/B test these)

- "Your Piper Morgan beta invite"
- "Piper Morgan beta access — your invite code inside"
- "[Name], your Piper Morgan beta account awaits"

---

## Email Template

```
Hey [Name],

You mentioned interest in testing Piper Morgan, and I'm glad to have you in the private beta.

Piper runs as a hosted app, so there's nothing to install.

**Getting in.** Go to https://beta.pipermorgan.ai and choose "Create your account". The first step asks for your invite code:

[INVITE_CODE]

It works once, for one account, so please don't share it. The next step asks for your Anthropic API key, so have one ready.

**What you can connect.** Piper works with GitHub and Google Calendar. With Calendar connected, you can ask about today's meetings or this week's, and your standup includes them. Piper only reads your calendar. They can't change it.

When Google asks, make sure the box next to "See and download any calendar you can access using your Google Calendar" is ticked, or Piper can't read your calendar.

**Who sees it.** Piper sends your messages, and anything they add from the tools you connect (such as calendar or GitHub items you ask about), to Anthropic under your own key. From there, Anthropic's own terms and privacy policy apply. Our admin tools don't display your conversations, and our server logs don't keep the text of what you send. The app has no analytics or ad tracking.

**Your key.** Piper runs on your own Anthropic key. We store it on our server in encrypted form and use it only to make your own requests. We hold the key that unlocks it, so in principle we could read it. Please use a key with a spending limit you're comfortable with. We don't read it on purpose. You can remove your key in Settings at any time, and that deletes it from our live database. Our encrypted backups can keep it for up to about five days. To cut off access completely, also revoke the key in Anthropic's console, so it stops working for Piper too.

**What you're agreeing to.** The plain-language terms are at https://pipermorgan.ai/terms/ and our privacy page is at https://pipermorgan.ai/privacy/. Please read them before you start.

**Known issues in this beta**

- **Piper sometimes misreads what you ask.** They may answer a different question or give a general reply. Rephrasing usually works.
- **An answer about your own data can be wrong.** Now and then Piper states something about your projects, issues or to-dos that isn't right, such as a wrong count. If an answer looks off, check the source and tell us.
- **Piper can state a detail about one of your records, such as a milestone or when something last changed, that they did not look up.** Check anything that matters in GitHub before you rely on it.
- **Asking for a milestone's issues in two steps ("show issues from one milestone", then the name) can list the wrong issues.** Ask in one step instead, with the milestone's name in the same sentence, such as "show my open issues in the Launch milestone". This is a known issue and isn't fixed yet.
- **No undo for deleted to-dos.** Deleting a to-do is permanent for now, and "delete all my to-dos" deletes one at a time.
- **Searching your documents from chat doesn't work yet.** You can upload a file and ask Piper about it by name, or paste the text into the chat.
- **If Piper asks which repository to create an issue in and you answer, they may add your answer to the draft instead of filing it.** Name the repository in your first request, such as "Create a GitHub issue in owner/name: 'your title'".
- **Piper can't change your default repository from chat yet.** Open Settings → Integrations → GitHub to set it.
- **When you ask what Piper can do, the answer may promise more than is there today.** For example, Piper may say they will notice things on their own. They don't start conversations or send anything unprompted.

**Feedback and help.** When you find something new, send feedback from the left-hand menu once you're in the app, or email support@pipermorgan.ai. Either way the message will be read by the team, including by me (xian), the human who owns this particular loop.

Thank you for trying it.

xian
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
- [ ] Verify all technical claims are current for version 0.9.0.0
- [ ] Attach/link current documentation (from docs/)
- [ ] HOST records the invitee ↔ code pairing in the roster (PII stays out of the repo)

---

## Notes

**Email Tone**: friendly and plain about beta status. Set realistic expectations
upfront.

**Documentation References**: always reference official docs by filename
(`ALPHA_TESTING_GUIDE.md`), and versions by number
(0.9.0.0, not "latest").

**Support Commitment**: only promise what you can deliver. Small cohort is what makes
close support possible.

---

## See Also

- `../../ALPHA_QUICKSTART.md` — what the tester's first ten minutes look like
- `../../ALPHA_TESTING_GUIDE.md` — what testers receive for depth
- `../../VERSION_NUMBERING.md` — version scheme documentation

---

_Template Version: 3.0_
_For Software Version: 0.9.0.0_
_Last Updated: October 31, 2026_
