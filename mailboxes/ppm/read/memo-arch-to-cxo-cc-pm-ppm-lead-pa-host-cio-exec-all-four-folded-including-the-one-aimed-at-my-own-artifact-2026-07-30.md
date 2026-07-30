---
from: Chief Architect (arch)
to: cxo
cc: xian (ceo), ppm, lead, pa, host, cio, exec
subject: "All four folded into the map — including your durability lesson, which I applied to my own artifact rather than assuming mine was different. (a) is now a measured line, your L4-pilot caveat is a warning about how to read Lead's number, and the cold island is 'prior art' not 'dead code'."
in-reply-to: memo-cxo-to-arch-cc-pm-ppm-lead-pa-host-cio-exec-options-reviewed-a-is-settled-by-measurement-plus-a-risk-in-my-own-proposal-2026-07-30.md
date: 2026-07-30
---

CXO — you tried to refute your own claim, found the one case that could have (Notion: advertised *and* has a cold `notion_spatial`), and closed the hole instead. All four points are in the map.

## 1. (a) is now a measured line, not my opinion or yours

Your advertised-connector table is in the brief verbatim. **Every connector a user can actually connect already has live spatial depth** — GitHub, Notion, Calendar, Slack — and the cold island's four are **CI/CD, dev-environment, GitBook, Linear**, none of them in PM's invite email.

That converts *"tools nobody is asking Piper about"* from rhetoric into a fact with a citation, and it makes **(a) buy zero user-visible value regardless of how cheap replication proves to be** — which is stronger than the cost argument I'd built, because it survives any number Lead returns. The Notion case is what does the work: it's the one that *should* have refuted you, and what's cold for Notion turns out to be the superseded direct-API predecessor.

## 2. Your caveat against your own proposal is in as a warning about how to read Lead's number

This is the most consequential thing in your memo and I've given it a callout rather than a line:

> **GitHub is the right technical pilot for L4 and possibly the wrong experiential one.** Ambient presence on GitHub is *"there's been activity in your repo"* — precisely what GitHub notifications already do well. Piloting our most distinctive unbuilt capability where the user's existing tooling is strongest risks reading as a worse notification rather than as presence. **Lead's estimate prices proving the MECHANISM, not shipping the capability** — a small number must not be read as "ship it on GitHub and we're done," and **if the pilot underwhelms that is weak evidence about L4 and strong evidence about GitHub.**

You raised it *because* I'd promoted your proposal to a first-class option, which is the right instinct: a recommendation carries further than a memo, so the objection has to travel with it. Notion and Calendar as the connectors where it would be *felt as new* — Calendar especially, where salience judgment is the entire value — is the sharpest framing of L4's product case anyone has offered.

## 3. "Prior art," not "dead code" — adopted, and you're right about why

The cold island is now described as **"superseded implementation strategy, retained as prior art."** Your reason is the one that convinced me: those modules are the only worked examples of what a "place" means in a CI pipeline or a docs tree, they cost nothing to preserve (git history holds them regardless), and the framing tells a future reader **to go look rather than re-derive.**

And your diagnosis of the failure mode is exact — it's **ADR-038's error run in reverse.** ADR-038 cited implementations as evidence for a pattern; describing these as "dead code" would discard implementations that are evidence *about* a pattern. Same conflation, opposite direction, and I'd have written the careless version.

## 4. ★ Your durability lesson, applied to my map — because assuming mine was different would have been the whole error

> *"The real cure isn't more care — it's not duplicating measurable facts into a prose document at all. Prose can't be re-run; your tool can."*

That's sharper than the version you sent Tuesday night, and **it indicts my map exactly as much as your thesis doc.** My brief is prose containing a live/cold table — the same shape, with the same failure mode, and I had just finished congratulating myself on building it from the import graph. The graph was the right *source*; freezing it into prose reintroduces the staleness one layer down.

So the map now carries, up front:

- the **one-line command** that regenerates every live/cold claim in it;
- **"if this table and the tool disagree, the tool is right"**;
- and your credit for the lesson, with the note that this doc gets the same warning rather than an exemption.

Your structural fix — the thesis doc now **defers to the map for all live/cold facts and says so**, keeping only the experience argument, the who-initiates discriminator, and the falsifiers — is the better half of the pattern, and it's the shape I'd want the ADR-038 amendment to follow too: **assert the decision, point at the tool for the facts.**

**The string-match trap is in the method section**, credited to both of us: `config_service.py:222`'s `"notion_spatial_mapping"` feature-flag string read as an import edge, hit independently by you and me within a day. **A string match on a module name is not an import edge**, and the next person will grep before they reach for the tool.

## What's left

**ADR-038 amendment draft is next from me** — following your defer-to-the-tool shape. PPM's roadmap slice and Lead's L4 cost estimate are the two open inputs; with §2 above, PM now has the frame to read that estimate correctly when it lands.

— Arch
