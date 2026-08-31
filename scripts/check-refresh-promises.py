#!/usr/bin/env python3
"""check-refresh-promises.py — did the refresh a document PROMISES actually happen?

THE FAILURE THIS CATCHES
------------------------
A document states its own currency mechanism in prose: "refreshed as part of the
weekly workstream review." Nothing connects the two acts but that sentence. Writing
the review and editing the document are separate acts on separate surfaces, so the
promise can hold for months and then quietly stop holding, and the document keeps
ASSERTING it is current while going stale. Vigilance wearing a mechanism's costume.

Real instance (2026-08-04): ROLE-PORTFOLIO-CXO.md promised "sections 2 and 4 touched
every review." last_updated was 2026-06-19. Four workstream reviews shipped after it
(051 07-10, 052 07-19, 053 07-29, 054 07-31) and touched none of it — 6.5 weeks. It
was found by reading the section that made the promise, which is not a mechanism either.

WHY IT IS NOT THE SAME AS check-derived-drift.sh
------------------------------------------------
That script asks "does this artifact still match its GENERATOR." These documents have
no generator — they are hand-authored. The question here is "did the EVENT that was
promised to update this document actually touch it." Same family (m-46: promotion is a
re-verification event), different hop: not copy-vs-source, but promise-vs-event.

⚠️ AND THE STALENESS RULE IT REPLACES WOULD HAVE MISDIAGNOSED IT. The portfolio's own
signal said a lagging last_updated means "investigate the review cadence." The cadence
was healthy — four reviews, on time. The broken thing was the LINK, not the rhythm, so
the diagnostic pointed at the one part that was working. This checks the link.

CONTRACT: reads only, never writes, exit 0 = every promise held, exit 1 = one lapsed.
A document opts in by declaring in its YAML frontmatter:

    last_updated: 2026-08-04
    refresh_trigger_glob: "mailboxes/cxo/sent/workstream-*-cxo-*.md"

The trigger's date comes from an ISO date in its FILENAME (not mtime — mtime is
destroyed by checkout, rebase, and worktree provisioning, so it would report noise).

DIFF MODE (--diff [REF], added 2026-08-22 — HOST's three-for-three lapse data)
------------------------------------------------------------------------------
The audit mode above catches lapses AFTER the fact; HOST's portfolio lapsed three
consecutive times the same way (content edited, frontmatter bump forgotten), each
caught at the next audit and none prevented. A manual habit with a 0% success rate
across three tries is not a habit. And auto-bump is the wrong fix — it would turn
last_updated from a CLAIM ("this content was refreshed") into an artifact of touching
the file, and the audit mode would then verify something meaningless.

So --diff moves the CATCH to edit time while keeping the CLAIM deliberate: for every
changed promise-carrying document in `git diff [REF]` (default HEAD: staged + unstaged),
if content lines changed but the last_updated line did not, warn — in the same session,
at the moment the claim goes stale, instead of at whoever's next audit. The inverse
(last_updated bumped with no content change) is noted too: a content-free bump is the
opposite failure, the one auto-bump would have institutionalized.

Denominator honesty (m-44): a run that finds no changed promise-carrying documents says
so — "nothing to check" is not a pass over the population. Exit 1 only on
content-changed-without-bump. Wireable as an advisory hook; advisory-not-control per the
standing Amber hooks doctrine.
"""

import glob
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISO = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")

# ── DISCOVERY ───────────────────────────────────────────────────────────────────
# ⚠️ THIS WAS A HARDCODED LIST UNTIL 2026-08-04, AND THAT WAS THE DEFECT.
#
# The docstring advertised opt-in via a frontmatter key; enrollment actually required
# membership in a list only the author edited. HOST followed the documented instruction,
# added refresh_trigger_glob to their portfolio, re-ran, and got "checked: 1 document.
# NOT checked: 0.  ✓ Every CHECKED promise held." — their opted-in document invisible,
# exit 0.
#
# ⭐ And the coverage line — the honest-reporting feature, the whole point — reported
# NOT checked: 0 while a document that had opted in went unchecked, because ITS
# DENOMINATOR WAS THE WATCH LIST. A coverage report whose denominator is its own
# registration can never report the thing it exists to report. That is the denominator
# lesson (m-43's companion) occurring inside the coverage report built to honor it.
#
# So discovery now scans, and the denominator is the population of PROMISES, not of
# registrations: a document that declares a refresh discipline in prose but no checkable
# trigger is REPORTED AS UNVERIFIABLE rather than being silently outside the count.
# "Declared but unwatched" is now impossible to reach silently.
SCAN_GLOBS = [
    "docs/briefing/*.md",
]

# Documents outside the scanned directories. This is a supplement to discovery now,
# never the gate.
EXTRA = []

# Frontmatter keys that constitute a PROSE refresh promise — a document carrying one of
# these is claiming to stay current, and belongs in the denominator whether or not it
# has made that claim checkable.
PROMISE_KEYS = ("refresh_discipline", "refresh_trigger_glob", "staleness_note")

# ⚠️ ADDED 2026-08-04, SECOND NON-AUTHOR RUN — this script created a perverse incentive.
#
# Web read the UNVERIFIABLE list, checked their own portfolio, found its claim ("the START
# act is the refresh mechanism") was FALSE, and did the right thing: refreshed the content,
# then rewrote the claim to say what is actually true — "I notice drift by re-reading and
# decide by hand." Vigilance, declared honestly.
#
# And this script would have gone on listing them next to six roles making claims that are
# still false, because it could not tell an honest declaration from an unexamined one. The
# only way off the list was to register a glob — and Web explained precisely why theirs
# would be a BAD one: session logs fire 6x/day, so "any trigger after last_updated →
# LAPSED" would report constant lapse, conflating "no new session yet" with "content is
# stale." A false signal, not a correct one.
#
# ⭐ So the incentive ran: make a false claim checkable with a mismatched proxy, or stay on
# a list that reads as delinquency. BOTH WORSE THAN THE TRUTH. A report that cannot
# distinguish an honest limit from an unexamined claim punishes the person who examined it.
#
# `refresh_verifiability: by-hand` is the declaration. It is NOT an exemption and it does
# not make the document pass — it moves it to a bucket that says "this promise is kept by a
# person, by hand, and the author has said so." Some promises are genuinely unmechanizable,
# and inventing an artifact whose only purpose is to be checked defeats the point (Web's
# words, and they are right).
VERIFIABILITY_KEY = "refresh_verifiability"


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


_LAST_UPDATED_LINE = re.compile(r"^[+-]last_updated:")


def _today():
    """Local date as ISO. Used only to recognize the same-day-amendment case."""
    import datetime

    return datetime.date.today().isoformat()


def diff_mode(ref):
    """Edit-time check: changed promise-carrying docs must move content and
    last_updated together. Reads git only; never writes; exit 1 only on
    content-changed-without-bump."""
    out = subprocess.run(
        ["git", "diff", "--name-only", ref], capture_output=True, text=True, cwd=ROOT
    )
    if out.returncode != 0:
        print(f"✗ git diff --name-only {ref} failed — this check DID NOT RUN; not a pass")
        print(out.stderr.strip())
        return 1
    changed_md = [l.strip() for l in out.stdout.splitlines() if l.strip().endswith(".md")]

    print(f"── refresh-promise DIFF check (vs {ref}) ────────────────────────────────────")
    fail = 0
    examined = 0
    for rel in changed_md:
        path = ROOT / rel
        if not path.exists():
            continue  # deleted in this diff; a deletion is not a stale claim
        if not any(k in frontmatter(path) for k in PROMISE_KEYS):
            continue
        examined += 1
        d = subprocess.run(
            ["git", "diff", ref, "--", rel], capture_output=True, text=True, cwd=ROOT
        ).stdout
        changes = [
            l
            for l in d.splitlines()
            if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))
        ]
        bumped = any(_LAST_UPDATED_LINE.match(l) for l in changes)
        content = any(not _LAST_UPDATED_LINE.match(l) for l in changes)
        # ⚠️ SAME-DAY AMENDMENT (fixed 2026-08-28, found by using the tool on a
        # real second edit): last_updated may already carry TODAY's date from an
        # earlier commit, in which case a further edit the same day is correctly
        # current and must not bump again. Flagging it would be a false positive —
        # and a checker that cries wolf on legitimate work trains people to skip
        # it, which is exactly the failure this tool exists to prevent.
        # The claim is "this content was refreshed on DATE"; if DATE is today,
        # the claim is TRUE regardless of whether the line moved in this diff.
        already_current_today = frontmatter(path).get("last_updated", "") == _today()
        if content and not bumped and not already_current_today:
            fail = 1
            print(f"  ✗ {rel} — CONTENT CHANGED, last_updated NOT bumped in the same change.")
            print(f"    This is the claim going stale at the moment it goes stale. Bump it now,")
            print(f"    deliberately — or state why this change isn't a refresh.")
        elif bumped and not content:
            print(f"  ⚠️  {rel} — last_updated bumped with NO content change. A content-free bump")
            print(f"    is the opposite failure (the one auto-bump would institutionalize). Fine")
            print(f"    only if deliberate.")
        elif bumped and content:
            print(f"  ✓ {rel} — content and last_updated moved together.")
    print()
    if examined == 0:
        print("no changed promise-carrying documents in this diff — NOTHING TO CHECK.")
        print("(That is an empty denominator, not a pass over the population.)")
    else:
        print(f"examined: {examined} changed promise-carrying document(s).")
    return fail


def main():
    fail = 0
    checked = 0
    unverifiable = []
    by_hand = []
    skipped = []

    candidates = []
    for g in SCAN_GLOBS:
        candidates.extend(sorted(glob.glob(str(ROOT / g))))
    candidates.extend(str(ROOT / e) for e in EXTRA)
    seen = set()

    print("── refresh-promise check ────────────────────────────────────────────────────")
    for c in candidates:
        path = Path(c)
        rel = str(path.relative_to(ROOT))
        if rel in seen or not path.exists():
            continue
        seen.add(rel)

        fm = frontmatter(path)
        if not any(k in fm for k in PROMISE_KEYS):
            continue  # makes no refresh promise; not in the denominator

        pattern = fm.get("refresh_trigger_glob")
        updated = fm.get("last_updated", "")
        declared = fm.get(VERIFIABILITY_KEY, "").strip().lower()

        if not pattern:
            if declared == "by-hand":
                by_hand.append(
                    f"{rel} — kept by hand, declared (last_updated {updated or 'absent'})"
                )
            else:
                unverifiable.append(
                    f"{rel} — declares a refresh promise in prose, no refresh_trigger_glob and no "
                    f"{VERIFIABILITY_KEY} declaration; nothing can check it and nobody has said so "
                    f"(last_updated {updated or 'absent'})"
                )
            continue
        if not ISO.match(updated):
            skipped.append(f"{rel} — last_updated is not an ISO date: {updated!r}")
            continue

        triggers = sorted(
            (m.group(0), p)
            for p in glob.glob(str(ROOT / pattern))
            for m in [ISO.search(Path(p).name)]
            if m
        )
        checked += 1
        print()
        print(f"▸ {rel}")
        if not triggers:
            print(
                f"  ⚠️  no trigger files match {pattern} — the promise names an event that leaves no trace"
            )
            fail = 1
            continue
        newest, newest_path = triggers[-1]
        later = [d for d, _ in triggers if d > updated]
        if later:
            fail = 1
            print(
                f"  ✗ LAPSED — last_updated {updated}, but {len(later)} trigger(s) shipped after it"
            )
            print(f"    newest: {Path(newest_path).name} ({newest})")
            print(
                f"    the promised refresh did not happen the last {len(later)} time(s) it was due"
            )
        else:
            print(f"  ✓ current — last_updated {updated} ≥ newest trigger {newest}")

    print()
    print("── coverage ─────────────────────────────────────────────────────────────────")
    total = checked + len(unverifiable) + len(by_hand) + len(skipped)
    print(f"documents making a refresh promise: {total}")
    print(f"  verifiable and checked: {checked}")
    print(f"  kept by hand, DECLARED: {len(by_hand)}")
    for b in by_hand:
        print(f"    · {b}")
    print(f"  UNVERIFIABLE and undeclared: {len(unverifiable)}")
    for u in unverifiable:
        print(f"    ✗ {u}")
    if skipped:
        print(f"  malformed: {len(skipped)}")
        for s_ in skipped:
            print(f"    ✗ {s_}")
    if by_hand:
        print()
        print("  · 'kept by hand' is NOT a failure and NOT an exemption. It records that a person")
        print("    keeps this promise and has said so. Declaring it honestly is strictly better")
        print("    than registering a trigger whose cadence doesn't match the claim, which would")
        print("    produce a confident wrong signal instead of an honest silence.")
    if unverifiable:
        print()
        print("  ⚠️  The undeclared ones are the finding. Each claims to stay current and nothing")
        print("      can contradict it — including the author. A recent last_updated tells you the")
        print("      author is diligent and tells you nothing about the promise.")
    print()
    if fail:
        print("✗ Exit 1: at least one VERIFIABLE promise has lapsed.")
    else:
        print(f"✓ Exit 0 means: none of the {checked} VERIFIABLE promise(s) has lapsed.")
    print(f"  It does NOT mean the other {total - checked} are current. The exit code's")
    print("  denominator is the checked set, and it can only ever be. Read the coverage")
    print("  block above before treating a green as a statement about the cohort.")
    return fail


def trigger_sent_mode(sent_path):
    """CXO's 2026-08-28 relocation, HOST's 4th-lapse report: --diff only catches a
    lapse if someone remembers to EDIT the promise-carrying doc; all four real lapses
    happened upstream of any edit, in the gap between the trigger event (filing a
    workstream review) and remembering the doc exists at all. Nothing connects those
    two acts but memory. This mode closes that specific gap: given a path that was
    JUST SENT via mail-send.sh, check whether it matches any promise-carrying doc's
    own refresh_trigger_glob, and if so, report right then whether that doc is
    current — so the act of sending the trigger is what tells you your portfolio
    just went stale, not a later habit of remembering to check.

    PURE ADVISORY, by design and by necessity: this runs inside mail-send.sh, which
    is on every role's critical path for every mail send. It must never fail the
    send and must never slow down or alter a send that matches nothing (the
    overwhelming majority). Silent on no-match; prints only when a trigger-carrying
    doc actually matches the sent path. Reuses the exact same lapse logic as main()
    (last_updated vs. newest trigger file) scoped to the one path that just moved,
    not the whole SCAN_GLOBS population — a full re-scan on every mail send would be
    both slower than necessary and would print noise for docs the send had nothing
    to do with.
    """
    m = ISO.search(Path(sent_path).name)
    if not m:
        return 0  # no ISO date in the filename — can't be a trigger by this scheme
    sent_date = m.group(0)

    candidates = []
    for g in SCAN_GLOBS:
        candidates.extend(sorted(glob.glob(str(ROOT / g))))
    candidates.extend(str(ROOT / e) for e in EXTRA)

    matched_any = False
    for c in candidates:
        path = Path(c)
        if not path.exists():
            continue
        fm = frontmatter(path)
        pattern = fm.get("refresh_trigger_glob")
        if not pattern:
            continue
        # Does the sent path fall inside this doc's declared trigger glob?
        matches = {str(Path(p)) for p in glob.glob(str(ROOT / pattern))}
        if (
            str((ROOT / sent_path).resolve()) not in {str(Path(p).resolve()) for p in matches}
            and str(ROOT / sent_path) not in matches
        ):
            continue
        matched_any = True
        rel = str(path.relative_to(ROOT))
        updated = fm.get("last_updated", "")
        if not ISO.match(updated):
            print(
                f"mail-send: refresh-trigger check — {rel} has a malformed last_updated ({updated!r}); cannot evaluate"
            )
            continue
        if sent_date > updated:
            print(
                f"mail-send: ⚠️  {rel}'s promise just LAPSED — this send ({sent_date}) postdates its last_updated ({updated})"
            )
            print(
                f"mail-send:   the trigger you just sent is exactly what {rel} declared it refreshes on — bump it now, while it's in front of you"
            )
        else:
            print(
                f"mail-send: {rel} still current relative to this send ({sent_date} ≤ last_updated {updated})"
            )
    return 0  # advisory only — never a failure signal, matching the mail-send.sh contract this hooks into


# ── STATE-FILES MODE (CXO's design, docs/internal/design/tracked-state-staleness-design-2026-08-29.md)
# The class this covers is DIFFERENT from the promise-vs-event class above: a carry-forward's claim
# is CADENCE-shaped ("rewritten at every STOP"), checkable only against time and the agent's own
# rhythm, not against a trigger artifact. CXO measured all 11 real carry-forwards before designing
# this: 7 of 11 declared no date at all; CXO's own header was actively wrong at the moment of
# measuring. Same script per CXO's own weak lean (§5 of the design doc) — frontmatter reading,
# denominator reporting, and honest-declaration handling are already here; a cadence predicate is a
# different CHECK on the same substrate, not a different substrate.
STATE_FILE_GLOBS = [
    "dev/active/*-carry-forward.md",
    "dev/active/*-standing-items.md",
]

CURRENCY_KEYS = ("currency_claim", "max_age_days")


def _parse_iso_date(s):
    import datetime

    m = ISO.match(s or "")
    if not m:
        return None
    y, mo, d = (int(g) for g in m.groups())
    try:
        return datetime.date(y, mo, d)
    except ValueError:
        return None


def state_files_mode(role=None):
    """Cadence-predicate check for tracked-state files (carry-forwards, standing-items).
    role=None audits every role's tracked-state files (cohort-wide sweep, denominator-reported
    like main()); a role slug scopes to just that role's own files — the shape duty-cycle-tick's
    Step 3 calls at START, right where it already reads the carry-forward, per the design doc's
    §3(b). Reads only, never writes. Exit 1 only if a DECLARED claim is actually stale — same
    contract as main(): a green here means the declared/checked set held, not that every tracked-
    state file in the cohort is current (the undeclared bucket is the finding, not a pass)."""
    import datetime

    candidates = []
    for g in STATE_FILE_GLOBS:
        candidates.extend(sorted(glob.glob(str(ROOT / g))))

    if role:
        candidates = [c for c in candidates if Path(c).name.startswith(f"{role}-")]

    checked = 0
    stale = 0
    declared_none = []
    undeclared = []
    malformed = []
    today = datetime.date.today()

    print(f"── tracked-state staleness check{f' ({role})' if role else ''} ──────────────────────")
    for c in candidates:
        path = Path(c)
        if not path.exists():
            continue
        rel = str(path.relative_to(ROOT))
        fm = frontmatter(path)

        if not any(k in fm for k in CURRENCY_KEYS) and "last_updated" not in fm:
            undeclared.append(f"{rel} — no currency_claim/max_age_days/last_updated at all")
            continue

        claim = fm.get("currency_claim", "").strip().lower()
        updated_raw = fm.get("last_updated", "")

        if claim == "none":
            declared_none.append(
                f"{rel} — currency_claim: none, declared honest (like refresh_verifiability: by-hand)"
            )
            continue

        if not claim or "max_age_days" not in fm:
            undeclared.append(
                f"{rel} — has last_updated but no currency_claim/max_age_days pair (not yet migrated)"
            )
            continue

        updated = _parse_iso_date(updated_raw)
        try:
            max_age = int(fm.get("max_age_days", ""))
        except ValueError:
            max_age = None

        if updated is None or max_age is None:
            malformed.append(
                f"{rel} — currency_claim {claim!r} declared but last_updated={updated_raw!r} / max_age_days={fm.get('max_age_days')!r} unparseable"
            )
            continue

        checked += 1
        age_days = (today - updated).days
        print()
        print(f"▸ {rel}  (claim: {claim}, max {max_age}d)")
        if age_days > max_age:
            stale += 1
            print(
                f"  ✗ STALE — last_updated {updated_raw}, {age_days}d old, claim allows {max_age}d."
            )
            print(f"    Its header is not evidence; the frontmatter is what's being checked.")
        else:
            print(
                f"  ✓ current — last_updated {updated_raw}, {age_days}d old, within its own {max_age}d claim."
            )

    print()
    print("── coverage ─────────────────────────────────────────────────────────────────")
    total = checked + len(declared_none) + len(undeclared) + len(malformed)
    print(f"tracked-state files examined: {total}")
    print(f"  verifiable and checked: {checked}")
    print(f"  declared currency_claim: none (honest, not a failure): {len(declared_none)}")
    for d in declared_none:
        print(f"    · {d}")
    print(
        f"  UNDECLARED (no checkable claim at all — the finding, per CXO's measurement): {len(undeclared)}"
    )
    for u in undeclared:
        print(f"    ✗ {u}")
    if malformed:
        print(f"  malformed: {len(malformed)}")
        for m_ in malformed:
            print(f"    ✗ {m_}")
    print()
    if stale:
        print(f"✗ Exit 1: {stale} of {checked} VERIFIABLE tracked-state claim(s) are stale.")
    else:
        print(f"✓ Exit 0 means: none of the {checked} VERIFIABLE claim(s) are stale.")
    print(f"  It does NOT mean the other {total - checked} are current — {len(undeclared)} of them")
    print("  make no checkable claim at all. Read the coverage block before treating green as a")
    print("  statement about the whole tracked-state population.")
    return 1 if stale else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--diff":
        sys.exit(diff_mode(sys.argv[2] if len(sys.argv) > 2 else "HEAD"))
    if len(sys.argv) > 2 and sys.argv[1] == "--trigger-sent":
        sys.exit(trigger_sent_mode(sys.argv[2]))
    if sys.argv[1:2] == ["--state-files"]:
        sys.exit(state_files_mode(sys.argv[2] if len(sys.argv) > 2 else None))
    sys.exit(main())
