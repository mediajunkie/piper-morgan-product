# PDR-009: The Public-Beta Gate — What Must Be True Before Beta Opens to the Public

**Status**: 📝 **Draft v0.1, 2026-11-12 17:06, PPM** (v0 17:03; v0.1 folds in CXO's experience rows E1 to E8, sent 17:00 before CXO had seen v0). CXO judges the experience rows (G4, G5 and section 3a) and Arch reads the technical ones (G1, G2, G6, G7). It goes to Exec for one yes or no from xian that covers both the gate and the PUB disposition in section 5.
**Author**: PPM
**Stakeholders**: xian (decides), Exec (relays), CXO (experience rows), Arch (technical rows), HOST (admission and support), Lead (builds), PA (MCP rows)
**Source**: xian, 11-12 (via Exec, verbatim): "While the old PUB sprint label is likely superseded given the reorg of the Production milestone, it remains for us to define a gate for the public beta." Earlier rulings this has to stay inside are listed in section 2.

---

## 1. What changes at public beta

Private beta (today) admits people xian invites. Each one has a relationship with him, and PDR-008's hold sets what must be true before any of them is invited.

Public beta admits people nobody on the team knows. The waiting list runs through public beta and admits by wave (xian, 11-02, #2164), so admission is still paced, but no one vouches for the person. Four things change:

- **Strangers.** Some will probe, overuse or abuse the service. Nobody can ask them what they meant.
- **No hand-holding.** A tester can't message xian when sign-up or connecting breaks. The product has to carry them to a first useful answer alone.
- **Public words.** Terms, the site and what Piper says about itself become promises to the public.
- **Volume.** Support, limits and cost scale with the number of people, not with xian's attention.

The gate covers those four changes. Everything else in Production finishes during the public beta, or at 1.0 when the Production milestone closes (`release-model.md` §2, unchanged).

## 2. Rulings this draft stays inside

- **ESSENCE v1.1, commitment 6, and PDR-005 Amendment 1 (xian, 10-23 18:03):** the MCP and plugin surface "ships during the beta, and its completion gates public beta." This draft keeps that clause and proposes what "completion" means (G6). Changing the clause itself would be an ESSENCE amendment, which is xian's.
- **xian, 10-16 (#2063):** legal review of the Terms comes "before any outside user beyond the design partners".
- **xian, 11-02 (#2164):** the waiting list is the one way in. It runs through the public beta and ends at production.
- **PDR-008:** the invite hold, and P2 (a new tenancy P0 re-holds unsent invitations).
- **xian, 11-12:** the PUB sprint value is "likely superseded", which is not yet a go to clear it. Section 5 proposes the clear.

## 3. The gate

Each row names what must be true, how it is checked served, and who judges. "Served" means checked on the public host (`beta.pipermorgan.ai`) at a named commit, not on main or in tests.

| Row | What must be true | Checked served how | Judge | Issues today |
|---|---|---|---|---|
| **G1. The hold stays met** | PDR-008 §2 is all met and the hold has lifted. No open P0 in the three hold classes (tenancy, overreach, front door). | PDR-008's lift memo rows, re-read at gate time with `gh issue view`; a label search for open P0-critical returns none in the three classes. | Arch (tenancy), PPM (the list) | #2261 via #2342 and #2343; #2282; #1551's remaining families |
| **G2. Strangers can't hurt others or the service** | Per-account rate and abuse limits, with a line the user can read when one is hit. CSRF protection and sign-in lockout. Hosted MCP access has a stated policy for strangers (#2242's allowlist, opened or kept). Sign-in by email works for every account. | One account driven past each limit on the public host sees the line; a cross-site form post is refused; repeated wrong passwords lock; an unlisted or new account meets the stated MCP policy. | Arch | #2165, #1378, #2242, #2267 |
| **G3. Public words are true and reviewed** | Terms published, every commitment mapped to a mechanism, and legal review done. Account deletion purges for real. Export of what Piper holds. One support queue with a named owner and a response window the Terms state. | Terms page live on the public host, its commitment-to-mechanism table checked row by row; one test account deleted and the purge read in the database; one export opened; a test message reaches the support queue and is answered inside the window. | xian (Terms and legal), Arch (deletion and export mechanisms), HOST (support) | #2062, #2063, #2158, #2159, #2160 |
| **G4. A stranger gets in and to a first useful answer alone** | Waiting-list sign-up with batch admission. A person arriving from the plugin or MCP endpoint has a path to an account. Sign-up screens don't repeat. A new account reaches one useful answer about its own work with no help from the team. | CXO watches (or has PA or Web run) a fresh account from the public site through admission, sign-in, one connector and a first answer, with no team help, on both the web and MCP arrival paths. | CXO, on section 3a's E1, E5 and E7 | #2164, #2175, #2256; onboarding sprint 2's served rows |
| **G5. Piper doesn't make false claims a stranger can't catch** | No open Class-3 (false answer) shape on the paths G4 walks. Any other known false-answer shape is either fixed or listed in plain words on a public known-issues line. | CXO's G4 walk includes the honesty probes for those paths; the known-issues line is read on the public site against the open H-section issues. | CXO, on section 3a's E2, E3, E4 and E6, with Arch on cause | #2042 (diagnosis), #2184, #2183, #2185, #2186, #2209; H section as it stands then |
| **G6. MCP-path completion (ESSENCE commitment 6)** | Proposed meaning of "completion": increments 2 to 7 (#1701 to #1706) each served on the hosted endpoint and passed against CXO's ratified plugin-surface rubric (#2168). Increment 8 (#1707) is a placeholder its own issue says not to build until the plugin-surface trust gradient exists; it is not part of completion. | PA runs each increment's rubric on the hosted MCP endpoint at a named MCP version; CXO rules each pass. | CXO (rubric), Arch (endpoint) | #1462 epic, #2168, #1701 to #1706, #1441 (#1706 depends on it) |
| **G7. Operable at volume** | Someone is alerted when the hosted service is down or failing, and the evidence lines needed to diagnose it are kept. A paused-admission switch exists (HOST can stop a wave in the same hour, as PDR-008 P2 does for invitations). | A forced health failure on staging reaches the named person; the evidence logger's lines are read on the host; HOST pauses and resumes one test wave. | HOST, Arch | #2348, #2350; a pause-switch issue to file if none exists |

### 3a. The experience rows (CXO, 11-12 17:00)

CXO's test: a stranger arrives with no invitation conversation, no one on our side to ask, and no knowledge of what we have ruled. The experience part of the gate is met when that person gets from sign-in to a first useful, true reply, and can recover from each failure by reading what Piper says. G4 and G5 are met when these eight rows are.

| # | What must be true | Issues that bear on it |
|---|---|---|
| E1 | First contact says what Piper is, and setup tells the truth: the sign-in screen, the key step (a Claude subscription is not API access), and a wizard whose "connected" is real. | #2275, #2274, #2268, #2206 |
| E2 | Honesty floor: a failed or missing source never reads as an empty result, in every reply that reads a source. | #1995, #1963, #2217, #2216, #2209 |
| E3 | Capability truth: "what can you do" promises nothing the beta refuses. | #2236, #2245, #2093 |
| E4 | The core loop works as described: todos and projects, the first thing most testers try, answer right and don't repeat or invent. | #2219, #2295, #2297, #2328, #2330, #2010 |
| E5 | Connections are truthful end to end: connect, disconnect and reconnect each say what will happen and then do it; what the beta doesn't offer isn't offered. | #2286, #2287, #2187, #2053, #2342's served rows, #2239 |
| E6 | Recovery: every failure names the way on, and none is a blank or a raw error. | the #2232 fault-run set; #1911, #2239 |
| E7 | A person can reach us from inside Piper, and "how do I get help" leads to a person. | #2246, #2276 |
| E8 | The chat is usable at phone width (a minimum bar, not a redesign). | #2278 |

**Checked served:** a fixed script of turns run by Web (browser) or PA (connector) on the named hosted build. Replies are quoted verbatim, with the layer and the denominator per row ("7 of 7 scripted turns"). A unit pin or a template read doesn't count. A row that needs an account state we can't produce is marked not served, never assumed. CXO judges, and a row passes only when every quoted reply meets the bar.

**PPM's note on overlap:** E7 and G3's support queue (#2160) are the two ends of one path, and E5 carries #2342's served rows, which G1 also needs. Each issue is checked once and counts for both rows.

### Lifting the gate

The same shape as PDR-008 §3:

1. When every row is met, PPM sends Exec one gate-readiness memo. Each row carries `Verified how:`, the layer checked, the host and the commit.
2. xian says go. Silence isn't a go. The date is his alone.
3. HOST opens the first public wave.

### How a row gets on or off

Like PDR-008 P1: any seat proposes, PPM checks it against section 1's four changes, and only xian admits or removes a row, through Exec. A finding that fits none of the four goes to the plan, not the gate.

## 4. What is deliberately not a gate row

- **Connectors complete (C section).** v18.7(kk) let the beta start without them, and they close at 1.0.
- **Multi-LLM providers (#1612).** Its title says "before public beta", but xian's "no optional complexity" ruling (08-27) froze multi-provider investment. **Choice for xian:** keep it off the gate (PPM's lean), or admit it as a G-row.
- **Local running (#2351).** It serves a private-beta tester now and is placed in Production (Dist). It isn't needed for the hosted public beta.
- **Experience polish, trust and learning, documents** (E, T, Doc), except the issues section 3a names. These finish during the public beta.
- **CXO's not-gate list (11-12):** Radar as the actionable default landing page (#2277), proactive presence (#1174), the "what makes you different" repetition (#2116), subject-less advice (#1962), the calendar edge cases (#2204, #2130, #2155), the invites-page refresh (#2099), and the self-knowledge Tier 1 corpus beyond the generated capability list (#2349). They stay open in Production; none stops a stranger getting a true first reply.

## 5. The PUB sprint value: a proposal

37 open issues carry Sprint `PUB - Public Beta` (board snapshot 11-12, 15:35 on `dev/snapshots/project-board-2026-11-12.tsv`). Read from each issue's title, labels and last update, and from its plan row; bodies were not re-read for this draft.

**Proposal:** the gate replaces the Sprint value. The gate rows in section 3 are the list, and PPM clears Sprint `PUB` per item (`clearProjectV2ItemFieldValue`, never the field's option list) once xian says yes. No new PUB values are set in the meantime. CXO sorts the experience ones by end of Friday 11-13 (their 17:00 offer), and v1 carries CXO's sort where it differs from this one.

| Disposition | Issues | Count |
|---|---|---|
| **Under the gate** (named in a G-row) | #1378, #1441, #1462, #1551, #1701, #1702, #1703, #1704, #1705, #1706, #2042, #2164, #2165, #2168, #2175, #2183, #2184, #2185, #2186, #2209, #2239 (E5, E6), #2242, #2342 | 23 |
| **Covered by Production, not the gate** (back to their plan section) | #1379 (Q, titled post-beta), #1537, #1538, #1539, #1540 (E, the onboarding sprint's FTUX rows), #1553 (H), #1591 (E), #1612 (see §4), #1624 (Doc), #1658 (Doc), #1673 (T), #1707 (T, placeholder), #2195 (V), #2237 (C) | 14 |
| **Close** | None proposed. No issue of the 37 reads as done or superseded from its title and plan row. A close needs a body read and evidence, which this draft didn't do. | 0 |

Plan rows in the PUB section that don't carry Sprint PUB, and would follow the same proposal: #2261, #2266, #2267, #2281, #2282, #2343 (G1 or G2), and #2256 (G4).

## Not decided here

- **Dates.** xian's alone. This PDR proposes none.
- **The wave size and pacing.** HOST's comparison under #2164.
- **ESSENCE's clause itself.** G6 proposes a meaning for "completion". Removing or changing the clause is an ESSENCE amendment.
