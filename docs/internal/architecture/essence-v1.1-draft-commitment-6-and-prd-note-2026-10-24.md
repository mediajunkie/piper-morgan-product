# ESSENCE v1.1, draft for xian to ratify: commitment 6 rewritten, and the PRD/spec note

**Status**: DRAFT (Arch, 2026-10-24 17:32 PT). Not law until xian ratifies it. On ratification, Arch applies it to `ESSENCE.md` word for word, as v1.1, and logs it in the amendment log.
**Asked for by**: xian's Production-map rulings, 2026-10-24 17:28 (decisions.log): ruling 3 ("Rewrite ESSENCE commitment 6: yes. that was always a bit of an overreading") and ruling 4 (PRD/spec drafting goes after 1.0, noted in ESSENCE). Finding F25 and F11 in `docs/internal/planning/production-map-review-round2-2026-10-23.md`.

## Why commitment 6 changes

The current text says Piper reaches its user "through the chat surfaces the user already lives in … not a destination app". Four rulings since then contradict it:

- **xian, 2026-08-08:** "The fundamental idea of the modeled user experience is that it is not specific to any one surface… I have never said that we are abandoning any one of those services."
- **xian, 2026-08-10:** "These are COMPLEMENTARY things… the byoc model that we're adding now is another additional option… that's not something that we want to decide for them." (decisions.log 08-10 ~10:56)
- **The beta-gate standard R7:** the hosted web UI is required for beta; the MCP path is not.
- **PDR-005 and PDR-006, Amendment 1 (ratified 2026-10-23 18:03):** "The hosted web UI is the beta surface." The MCP endpoint and plugin are "one of Piper's complementary surfaces".

The "What it is NOT" section repeats the overreading ("Not a destination UI, the structurally doomed shape in the copilot category"), and the 08-29 snapshot calls web "explicit maintenance mode". Both change with it, or the document contradicts itself.

## The edits

### 1. Commitment 6, replaced

> 6. **It meets its user on whichever surface they're working in, as one Piper.** The hosted web app, the MCP endpoint and plugin inside the user's own chat, and chat platforms when they return are complementary surfaces over one backend. The user chooses where to meet Piper, and we don't decide that for them. The web app is a real surface, the beta surface, where conversations, the radar and settings live. The MCP and plugin surface ships during the beta, and its completion gates public beta. Each surface expresses the same Piper as that surface allows (initiation where the host affords it, per commitment 3). Connector rule, ratified: Piper's backend holds a grant only where it must act without the user present (standup generation, background reflection, document mirroring), or where Piper is itself the host (the web app reads with the user's own grant). Inside another host's chat, in-conversation reads of third-party services belong to that host's connectors.
>
> *(v1.1, xian 2026-10-24: "not a destination app" retired as an overreading; sources: xian 08-08 and 08-10, gate R7, PDR-005 and PDR-006 Amendment 1.)*

**The one substantive addition, for xian to see plainly:** the connector rule's "or where Piper is itself the host" clause. The old text written for the MCP path implied the backend never reads third-party services during a conversation. On the web app Piper is the host, and it already reads GitHub and Calendar with the user's own grant (the #2121 rule: read as the account, never a host token). The clause states what the product does and has to do. Strike it if you'd rather settle it in the GitHub identity ADR.

### 2. "What Piper Morgan is NOT": the destination line, replaced

Old: "Not a **destination UI** (the structurally doomed shape in the copilot category)."

New:

> Not a **walled garden**: no surface is required, and none is the only way in. The web app is a surface the user can choose, never one they're made to come to.

### 3. Commitment 2: the PRD/spec note

At the end of commitment 2, append:

> *(Scope, xian 2026-10-24: GitHub issues are the 1.0 artifact. Drafting PRDs and specs comes after 1.0, built on the document and GitHub capabilities once they're solid; #2139 is the nearest existing work. The commitment is unchanged; only its sequencing is recorded.)*

### 4. The 08-29 snapshot: the maintenance-mode clause marked

At "in **explicit maintenance mode** as of 2026-08-29 — bugs fixed, nothing new built", add in place:

> *superseded 10-23: the hosted web UI is the beta surface (PDR-005 Amendment 1); Sprint E builds on it.*

The snapshot stays dated and is otherwise untouched; this marks one stale claim, as v1.0.3 did for flip-1.

### 5. Amendment log entry, on ratification

> *v1.1, 2026-10-24 (xian's Production-map rulings 3 and 4; drafted by Arch): commitment 6 rewritten (surfaces complementary, web is the beta surface, the connector rule gains the Piper-as-host clause); the "destination UI" boundary line replaced by "walled garden"; commitment 2 records PRD/spec drafting as post-1.0; the 08-29 maintenance-mode clause marked superseded.*

## What this does not change

- Commitment 3's surface-bounded ritual. It already says the same thing per surface.
- The public-beta gate: MCP-path completion still gates it.
- The "no operator key" rule (PDR-005 Amendment 1 §2). It stays in the PDR, not here.

Verified how: read `ESSENCE.md` in full (196 lines), PDR-005 Amendment 1 (L21–48), PDR-006 Amendment 1 (L9–23), decisions.log 08-10 (L1646), 08-27 (L1713) and 10-24 17:28 (L2798), the rulings page and F11/F25 in the round-2 record. Layer: documents. Denominator: 4 edits, all in ESSENCE.md.
