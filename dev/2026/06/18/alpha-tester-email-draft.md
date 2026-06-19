# Alpha tester email — draft v3

**From**: xian (Christian Crumlish)
**To**: [alpha tester list]
**Subject**: Piper Morgan skills — try these in Claude

---

Hey,

Quick note — I've been building something I think you'll find useful and wanted to give you a first look before it's more broadly available.

**Piper Morgan skills** are a set of slash commands for Claude that make product management work faster. They're calibrated for how I actually work — direct, no fluff, action-oriented. I'm sharing them now because I want real feedback, not a polished launch.

**What's included:**

- `/piper-sprint-plan` — given your current issues or backlog, help you decide what to tackle and in what order
- `/piper-stakeholder-update` — turn rough notes into a clear stakeholder update, calibrated for your audience (exec, team, investors)
- `/piper-draft-issue` — structure a rough idea into a properly scoped GitHub issue (or any tracker)
- `/piper-draft-spec` — turn a rough idea into a complete, reviewable feature spec
- `/piper-synthesize-feedback` — take raw user feedback and extract prioritized themes with recommendations

**To install:**

```bash
curl -sSL https://raw.githubusercontent.com/mediajunkie/piper-morgan-product/main/scripts/install-skills.sh | bash
```

That installs the skills into `~/.claude/skills/`. They'll show up as slash commands in Claude Desktop (Chat, Cowork, and Code).

**What I'm looking for:**
- Do they actually save you time?
- Do they feel right, or do they feel generic?
- Which ones do you reach for and which ones sit unused?
- What's missing?

You don't need to be systematic — just use them when they naturally fit and let me know what you notice. Honest takes only, please.

If you hit any weirdness, just reply to this email.

Thanks for being part of this,
xian

---

*Piper Morgan is a PM-specific AI assistant I've been building. The skills are the first distributable piece — the full assistant (profile-aware, connected to your tools) is coming. More soon.*
