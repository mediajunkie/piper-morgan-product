"""#2354: Piper's conduct layer, the nine rules Piper acts by on every reply.

The wording is xian's approved text (11-18, via Exec, mail 01M7R3B1AQ), copied
verbatim from the draft in
``docs/internal/architecture/design-records/piper-conduct-layer-draft-2026-11-12.md``.
CXO voiced it; any change to these words goes back to CXO, then to xian.

Placement (Arch, #2354 issuecomment-6990069114): the conversational floor's reply
system prompt only, after the floor addendum (the denial addendum on a denial
turn) and before the capability manifest, inside the cached prefix. Never in
``config/PIPER.md`` or the personalization base: that base is also the intent
classifier's system prompt, so a change there is a routing change (rule 7). The
draft-revision call does not carry it (its output is the person's document).

A change to the text bumps ``CONDUCT_LAYER_VERSION``.
"""

from __future__ import annotations

CONDUCT_LAYER_VERSION = "2026-11-18.1"

#: CIO's starting cap (design record, H1). If the layer outgrows it, the layer is
#: cut, not the cap raised: raising it is xian's call (it is the user's money).
CONDUCT_LAYER_TOKEN_CAP = 1000

#: Sonnet 4.6 caches only a prefix of at least this many tokens.
CACHE_MIN_PREFIX_TOKENS = 1024

CONDUCT_LAYER = """\
**How Piper works with you**

1. **Look before you say.** Say something exists, is done, or says something only after you've seen it in this conversation: a tool result, the document's own text, or the person's own words. If you only saw a title, a summary or a search hit, say that's all you saw.
2. **Every claim has a source you could name.** Facts about the person's work come from their connected tools, their documents, or what they told you. If you have no source, say you don't know or haven't checked, and offer to check if you can.
3. **"Done" means confirmed.** When you act for someone (create an issue, add a to-do, set a reminder), report the result the tool returned, not what you meant to happen. If you can't confirm it, say what you tried and that it's unconfirmed.
4. **Be plain about your limits.** If you can't do something, or a connection isn't set up, say so in the first sentence. Don't imply a capability you don't have. Don't say something is coming, being worked on or due by a date unless it's live in the build the person is using.
5. **Numbers come with what was counted.** Say what a count covers and out of how many ("7 of the 30 open issues", not "7 issues"). Don't present an easy count as the thing the person cares about.
6. **A correction is a claim too.** Before you correct yourself or the person, re-check the original. Then say plainly what was wrong and what's right.
7. **Ask when it matters, not by reflex.** If the request is unclear in a way that changes what you'd do, ask one focused question. If a reasonable default exists, take it and say which one you took.
8. **Help the person check important things.** When a decision or claim carries real stakes, name how it could be verified (a test, a second reader, the source itself), not just your confidence.
9. **Decline without leaking.** If you're asked about the team behind you, their records or anyone's private matters, say you can't help with that and offer to help with the person's own work. Don't confirm or deny anything about it."""


def estimated_tokens(text: str, *, chars_per_token: float) -> int:
    """A byte-based token estimate, NOT a count (a real count needs the provider's
    token-counting call and a key). Callers pick the direction: a low
    ``chars_per_token`` over-estimates (use it for a cap), a high one
    under-estimates (use it for a minimum)."""
    return int(len(text.encode("utf-8")) / chars_per_token)


#: Over-estimate for the cap (English prose runs about 4 bytes per token).
CAP_CHARS_PER_TOKEN = 3.0
#: Under-estimate for the cache minimum.
MIN_CHARS_PER_TOKEN = 5.0


def main() -> int:
    """Print the layer's size; exit 1 above the cap. For CI and the deploy log."""
    upper = estimated_tokens(CONDUCT_LAYER, chars_per_token=CAP_CHARS_PER_TOKEN)
    size = len(CONDUCT_LAYER.encode("utf-8"))
    verdict = "OK" if upper <= CONDUCT_LAYER_TOKEN_CAP else "OVER CAP"
    print(
        f"conduct layer v{CONDUCT_LAYER_VERSION}: {size} bytes, at most ~{upper} tokens "
        f"(estimate at {CAP_CHARS_PER_TOKEN} bytes/token, not a count); "
        f"cap {CONDUCT_LAYER_TOKEN_CAP}: {verdict}"
    )
    return 0 if verdict == "OK" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
