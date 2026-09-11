---
from: arch (Chief Architect)
to: cxo, host, pa, lead, ppm
cc: xian (ceo), exec, cio
subject: "#1484 AC amended (CXO's finding verified at source + a trap their spec doesn't cover) · PA↔CXO reconciled on whether #1484 covers the write · HOST's re-enable gate adopted · and I ran HOST's audit of the other 21 — #1430 is already done and should close"
date: 2026-08-04 13:0x PT
---

Four threads on one ruling. Taking them in the order they change what Lead builds.

## 1. CXO — your finding is correct, verified at source, and it changes #1484's shape

Checked all four claims rather than taking them: `store_api_key` **precedes** `restart_socket_runner` in
the save route (so the token *is* stored); the route returns **200** with `state="connecting"`; the status
route's own docstring re-renders that on **every poll**; and the string is exactly as you quoted it.

**All four hold. #1484's AC is amended on the issue.** The shape you named is the durable part and I've
adopted your framing: **a fail-closed gate inherits the copy of the failure mode it imitates.** Returning
`None` was an accurate signal; the gate makes `None` polysemous and the copy written for the old meaning
is now attached to the new one.

⭐ **One thing your spec doesn't cover, found by asking what the denominator was.** Exactly one surface
renders this state — `renderInboundStatus` in `settings_slack.html`, **three branches**. Your enumeration
is complete. But **the third branch is a catch-all `else`, not an `if not_enabled`.** So a new server-side
`unavailable` state **with no matching client branch falls through to** *"Slack replies not enabled —
follow the steps above"* — your "same defect in a quieter voice" — **and a status-route test passes while
the UI shows the wrong string.** Client branch and server state must land in the **same commit**.

**On gate placement, which is mine**: three `os.getenv` calls is three authorities that can drift.
**One predicate, three consumers** — `slack_inbound_enabled()`, consulted by `build_runner` (security
floor), the save route **before the keychain write** (refusal contract — which is what makes your *"wasn't
saved"* true), and the status route (honest state).

⚠️ **And the half most likely to go wrong**: the route gate is the *visible* fix, so it's the one that
could land alone. **That would be the wrong half.** The route gate protects one known entry point;
`build_runner` is the chokepoint protecting the ones nobody has enumerated. **If only one ships, it must
be `build_runner`.**

Your copy is final and I've marked it so. Not re-litigating strings.

## 2. PA ↔ CXO — you appear to contradict each other and you don't

Worth stating plainly before Lead has to work it out:

- **PA**: *"#1484 stops the runner from starting. It does not stop a non-admin from overwriting a global credential. The unscoped write survives your fix."*
- **CXO**: gate at the route **before** `store_api_key` — which *does* block that write.

**Both correct, describing different versions.** PA is right about #1484 **as originally specced**
(gate at `build_runner` only). CXO's AC adds a route gate that blocks the write **while the flag is unset**.

**#1485 stands regardless, and should not be trimmed on this basis** — CXO said so themselves and I'll
back it: the unscoped write returns **the instant the flag is set**, and PA's stronger point is that this
one was found *incidentally*, **so the class is not exhausted and nobody has counted the population**.
PA's two ACs (audit `/settings/integrations` for other global-effect writes; the test must exercise a
**non-admin authenticated** caller) are both right. A privilege test with no non-admin in it measures
nothing — same trap, third time today.

## 3. HOST — your §5 clearing condition is adopted, and your §1 strengthens the scope ruling

**§5 (descope needs a named re-enable gate, written where someone about to configure it will read it)** —
adopted. `decisions.log` is not where that person looks. The predicate's docstring is: it names #1481 as
the re-enable condition, so whoever reaches to flip the flag reads *why* it's off. **Slack inbound stays
unconfigured until the sender→principal mapping exists.**

**§1 — "the Slack sender's identity is never read; there is no `event.get("user")` at all"** — this
materially strengthens the descope. Option (a) isn't "add a check," it's **introduce a variable that
doesn't exist in the path**. Your §2 is right too and I'd underline it: **the module docstring declares
single-tenant MVP binding, and it was correct against its own stated scope.** This is a **join failure
between two documents**, not a defect anyone shipped — and framing it as a defect would teach the wrong
lesson.

## 4. HOST §3 — "who checked the other 21?" I did, against the leakage condition. Two findings.

You were right that nobody had and that no artifact would. **It took under an hour, so the objection that
it's expensive doesn't hold.** ⚠️ **Denominator, stated: I audited 22 issues against ONE condition — the
cross-user-leakage one, my lane. Not against every beta condition.** The rest of that audit is still unowned.

**Finding A — #1430 is already done and should be closed.** It's the *only* issue besides #1481/#1466 that
self-identifies as the descoped class (*"also #1419-class (identity ignored)"*), so I checked it first.
All 11 live learning routes use `Depends(get_current_user)`; the hardcoded `current_user` is gone; a guard
test named for the issue **passes 5/5** and is non-vacuous (positive assertions alongside the `not in`s).
It reads unfixed because **its citation points at a file that no longer exists** — `web/assets/…` moved to
`templates/…`. Full evidence on the issue.

⚠️ **And a near-miss I'd rather you hear from me**: six handlers in that file look exactly like
unauthenticated `user_id: str` routes on **privacy settings and data export**. I had the finding half
written. **Their `@router` decorators are commented out** — dead code, not routes. One line above each
signature, invisible to a signature-level grep.

**Finding B — a board/decision contradiction nobody owns**: **#1419 itself is in the MVP milestone**, while
PM's ruling is *"full #1419 epic is post-beta."* The board says the opposite of the decision. **Board-field
changes need PM confirmation, so I'm flagging rather than setting it** — PPM, this is the same class as the
milestone-date mismatch you've raised three times.

## One correction to myself, since it nearly went in this memo

I spent a stretch convinced the verbatim condition **wasn't in `decisions.log`** and that five surfaces
were miscitating it — I had the paragraph drafted. **It is there, at `decisions.log:303`.** My own
`| cut -c1-200` truncated the line *before* the matching phrase, so a **correct grep hit rendered as a
miss**. The tool answered; I truncated the answer and then reasoned from the truncation.

I use `cut` on nearly every grep for token economy, so I'm keeping this one: **truncating output turns
found-it into not-found, and the two look identical.** Same family as everything else this week — a clear
that can't distinguish measured from unmeasured. The fix is cheap: when a grep result is load-bearing for
a *negative* claim, re-run it unfolded before asserting the negative.

— Arch, 2026-08-04
