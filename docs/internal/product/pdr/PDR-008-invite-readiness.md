# PDR-008: Invite Readiness — What Must Be True Before Any Invitation

**Status**: ✅ **Accepted 2026-11-07.** xian approved P1, P2 and P3 as drafted, by 08:03 (Exec relay 08:04, recorded in decisions.log). Draft v1 was PPM's, 06:35. Sections 1 to 3 restate earlier rulings. Section 4's three proposals are now rules, and HOST owns P2's same-hour hold.
**Author**: PPM
**Stakeholders**: xian (decides), Exec (relays), Arch (tenancy reads), CXO (what a tester sees), HOST (sends invitations), Lead (builds)
**Source rulings**: xian 11-04 19:31 (no invitations of any kind until the tenancy P0s land); xian 11-05 10:47 (#2283 P0, #2282 yes, both before the first invite); the 11-06 goals (goal 1: lift the hold, then the cohort note and the next invitations on his word). All are in `docs/internal/architecture/decisions/decisions.log`.

---

## The question

The hold has lived in rulings, labels and carry-forward notes since 11-04. Each new finding raised the same question again: does this one hold invitations too? This PDR writes down what the hold protects, which conditions are on it, how a new one gets on, and how it lifts.

## 1. What the hold protects

An invitation is a promise to a stranger that their work stays theirs (promise T1, "your work is yours"). The hold covers only failures that would break that promise, or that would stop the invitation from reaching the person:

- **Tenancy.** Another user, or the server itself, can read or act on a tester's data or credentials.
- **Overreach.** A connection grants Piper more than the tester agreed to, or keeps a grant after they disconnect.
- **The front door.** The invitation never arrives, or it sends the tester to a host that breaks sign-in or connections.

Rough edges in first use (a wrong answer, a loop or an unclear page) aren't hold conditions. They belong to the onboarding sprint (11-13 to 11-26). xian ruled this distinction for #2157 and #2158 (P1, not hold conditions, 11-04 19:31).

## 2. The conditions, as of 2026-11-07 06:34

The status comes from `gh issue view` on each issue, read at 06:34.

| Issue | Class | Bar | State |
|---|---|---|---|
| #1551 per-user isolation | Tenancy | Guard green, Arch's validation, all 50 sites ruled | **Met** 11-04 20:49 (Lead; Arch 19:45 and 20:21). The epic stays open for the Slack and Notion families behind the offer gate. |
| #2283 OAuth callback tenancy | Tenancy | Served | **Closed** 11-05 |
| #2178 Disconnect revokes GitHub's grant | Overreach | Served | **Closed** 11-05 |
| #2261 GitHub connect scope | Overreach | ADR-081 D3 via #2174's staging check, or `public_repo` with CXO's two conditions (11-04 18:50) | **Open.** Waits on xian's #2174 runs. |
| #2282 one canonical host | Front door | Its four acceptance rows | **Open.** The MCP lane (a to c) is done. The browser row waits on xian's word for Web's sign-in check. |
| #2292 SPF, DKIM, DMARC | Front door | Records live, DMARC at `p=none` first (CIO 11-05 22:08), and one test mail lands in an inbox | **Open**, P1. Waits on xian's records. |

## 3. Lifting the hold (restates goal 1)

1. When every row in section 2 is met, PPM sends Exec one lift-readiness memo. Each row in it carries `Verified how:`, the layer that was checked, and the host it ran on.
2. xian says go. Silence isn't a go.
3. The cohort note goes first, then the next invitations, each on xian's word. HOST sends them.

## 4. Rules added by this PDR (xian yes, 2026-11-07)

- **P1. How a new condition gets on the list.** Any seat can propose one, and PPM checks it against section 1's three classes. Only xian admits it, through Exec. A finding that fits none of the three classes goes to the sprint or the plan, not the hold. *Why:* it ends the case-by-case re-asking, and it keeps the decision with xian.
- **P2. A new tenancy P0 after the lift re-holds unsent invitations.** Invitations already sent stand. HOST holds the unsent ones the hour the P0 is labelled, and xian rules within his next session whether the hold stays. *Why:* in this case the safe default is to pause. A tester invited during a known cross-tenant leak is the harm the hold exists to prevent.
- **P3. "Any invitation" means any.** That covers a new tester, a waiting-list confirmation that grants access, and a re-invite. The cohort note to people already in the beta isn't an invitation, but section 3 still sequences it after the lift. *Why:* Exec's relay of the 19:31 ruling reads "no invitations of any kind", and this makes that checkable.

## Not decided here

- Dates. Dates are xian's alone, and this PDR proposes none.
- Which onboarding work ships before the next invitation. That is the sprint's question, ratified at the 11-13 review.
