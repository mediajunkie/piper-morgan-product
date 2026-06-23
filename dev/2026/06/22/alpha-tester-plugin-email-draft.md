# Alpha tester email — plugin wave draft

**From**: xian (Christian Crumlish)
**To**: [alpha tester list]
**Subject**: Next piece: the Piper Morgan plugin for Claude Desktop

---

Hey,

Follow-up to the skills I sent last week — this is the next piece, and it's meaningfully different.

The skills were prompting patterns: useful, but Piper didn't know anything about you. What you're getting now is the plugin — the hosted version of Piper that has a profile, remembers you across sessions, and can connect to your tools over time.

**What it is:**

The Piper Morgan plugin connects Claude Desktop to a hosted backend running at alpha.pipermorgan.ai. Once installed, Piper shows up as a set of tools in Claude. You authenticate once, and then Piper can remember your context, your company, your work patterns.

**Installing it:**

1. Download `piper-morgan-v0.1.4.mcpb` (attached)
2. Double-click it — Claude Desktop installs it automatically
3. In any Claude conversation, run: `connect [shared password]`
   - Password: `[SHARED_PASSWORD]`
4. That's it. Six tools will be active.

**What to try:**

- `meet-piper` — let Piper learn who you are and what you work on. Run this first.
- `ask_piper` — give it a real PM question. Does it feel like it knows the context you gave it in meet-piper?
- `consult-piper` — a specific challenge you're working through. Does it feel calibrated?
- Come back tomorrow and run `ask_piper` again — does it remember?

**What I'm looking for:**

- Does the install work, or does something break?
- Does `meet-piper` feel like it's actually capturing something useful about you?
- Does `ask_piper` feel different from just asking Claude directly? Is that difference worth it?
- Anything weird or broken — reply and tell me.

**Honest alpha caveat:**

This is connected to a live server I'm running. It works, but it's not hardened. Don't put anything genuinely sensitive in your profile yet. And if something feels off, assume it's a bug and let me know — that's what this is for.

The skills you already have still work independently. The plugin adds the memory and personalization layer on top.

Thanks for being early,
xian

---

*P.S. The model here: you bring your own Claude subscription (and the AI does the work inside Claude), Piper contributes the PM expertise and the memory. BYOC — bring your own Claude. It keeps your data in your control and the costs low.*

---

**[Attachment]: piper-morgan-v0.1.4.mcpb (~41MB)**

---

*Draft for PM review — not yet sent*
*Waiting on: Droplet deploy of 0.8.9 + PM clean-machine test of v0.1.4*
