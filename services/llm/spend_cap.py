"""A dollar cap on live model calls for one script run (#2383, ADR-084 D2).

A served request never sets a cap: ``current_cap()`` is ``None`` there and the two
hooks below return at once. A seat's paid run binds one through
``scripts/dev_key_binding.developer_keys_bound(max_usd=...)``, and from then on the
provider legs in ``services/llm/clients.py`` ask before every call and report after it:

- ``reserve(model, input_chars, max_tokens)`` works out the most the call could cost
  and refuses (``SpendCapReached``) when the run's total plus that figure would pass
  the cap. Nothing is sent for a refused call.
- ``settle(reservation, usage)`` replaces the estimate with the cost from the
  provider's own token counts.

A refusal ends the run: every later call is refused too, the provider legs let the
refusal pass without trying another provider, and the binder exits non-zero.

A call that raises keeps its upper estimate on the total: a timed-out request may
still have been billed, and the cap is a bound, so the doubt counts against the run.

A model with no price row is refused. Add the row with its source; do not guess one.
The batch half of the same rule is ``scripts/router_batch.py submit --cap-usd``.
"""

from __future__ import annotations

import contextlib
import math
import threading
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Dict, Iterator, Mapping, Optional, Tuple

# USD per million tokens, (input, output), standard (not batch) rates.
# Source: Anthropic's published model table as cached in the claude-api reference
# on 2026-11-03. OpenAI and Gemini rows are absent on purpose: nobody has recorded a
# sourced price for them, so a capped run on those models is refused.
_USD_PER_MTOK: Dict[str, Tuple[float, float]] = {
    "claude-opus-4-8": (5.00, 25.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
}
# Anthropic bills a cache write at 1.25 times the input rate and a cache read at 0.1.
_CACHE_WRITE_FACTOR = 1.25
_CACHE_READ_FACTOR = 0.10
# Characters per token for the upper estimate. Lower than prompts measure, so the
# estimate overstates the input side. Same figure as router_batch.py's ceiling.
_CEILING_CHARS_PER_TOKEN = 3


class SpendCapReached(Exception):
    """The next call was not sent: it could take the run past its cap."""


class SpendCapUncounted(Exception):
    """A spend the cap cannot count was reached under a cap, so it was not sent."""


def price_for(model: str) -> Tuple[float, float]:
    """(input, output) USD per million tokens, or ``SpendCapReached`` if unrecorded."""
    for name, price in _USD_PER_MTOK.items():
        if model == name or model.startswith(name + "-"):
            return price
    raise SpendCapReached(
        f"REFUSED: no price recorded for model {model!r}, so its cost can't be bounded. "
        "Nothing was sent. Add its row to services/llm/spend_cap.py with the source."
    )


def upper_usd(model: str, input_chars: int, max_tokens: int) -> float:
    """The most one call could cost: every input token as a cache write, full output."""
    usd_in, usd_out = price_for(model)
    tokens_in = math.ceil(max(input_chars, 0) / _CEILING_CHARS_PER_TOKEN)
    return (tokens_in * usd_in * _CACHE_WRITE_FACTOR + max(max_tokens, 0) * usd_out) / 1_000_000


def usage_usd(model: str, usage: Mapping[str, int]) -> float:
    """What one call cost, from the provider's own counts."""
    usd_in, usd_out = price_for(model)
    return (
        (usage.get("input_tokens") or 0) * usd_in
        + (usage.get("cache_creation_input_tokens") or 0) * usd_in * _CACHE_WRITE_FACTOR
        + (usage.get("cache_read_input_tokens") or 0) * usd_in * _CACHE_READ_FACTOR
        + (usage.get("output_tokens") or 0) * usd_out
    ) / 1_000_000


@dataclass
class Reservation:
    model: str
    upper: float
    settled: bool = False


class SpendCap:
    """The running total for one run. Shared by every task the run starts."""

    def __init__(self, max_usd: float):
        if not isinstance(max_usd, (int, float)) or isinstance(max_usd, bool) or max_usd <= 0:
            raise ValueError("max_usd must be a number above zero")
        self.max_usd = float(max_usd)
        self.measured_usd = 0.0  # from provider token counts
        self.estimated_usd = 0.0  # calls with no usage, at their upper estimate
        self.reserved_usd = 0.0  # calls in flight
        self.calls = 0
        self.unmeasured_calls = 0
        self.refused = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self._lock = threading.Lock()

    @property
    def counted_usd(self) -> float:
        return self.measured_usd + self.estimated_usd

    def reserve(self, model: str, input_chars: int, max_tokens: int) -> Reservation:
        try:
            upper = upper_usd(model, input_chars, max_tokens)
        except SpendCapReached:
            with self._lock:
                self.refused += 1
            raise
        with self._lock:
            committed = self.counted_usd + self.reserved_usd
            if self.refused:
                # A refused call ends the run (Arch 2026-11-16): its rows are not
                # counted, so nothing more is sent on its behalf.
                self.refused += 1
                raise SpendCapReached(
                    "REFUSED: an earlier call in this run was refused at the cap, so the "
                    "run is over. Nothing was sent."
                )
            if committed + upper > self.max_usd:
                self.refused += 1
                raise SpendCapReached(
                    f"REFUSED: this call could cost up to ${upper:.4f}; ${committed:.4f} is "
                    f"already counted against the ${self.max_usd:.2f} cap. Nothing was sent."
                )
            self.reserved_usd += upper
            self.calls += 1
        return Reservation(model=model, upper=upper)

    def settle(self, reservation: Reservation, usage: Optional[Mapping[str, int]]) -> None:
        """Swap the estimate for the measured cost. No usage keeps the estimate."""
        with self._lock:
            if reservation.settled:
                return
            reservation.settled = True
            self.reserved_usd = max(0.0, self.reserved_usd - reservation.upper)
            if usage:
                self.measured_usd += usage_usd(reservation.model, usage)
                self.input_tokens += (
                    (usage.get("input_tokens") or 0)
                    + (usage.get("cache_creation_input_tokens") or 0)
                    + (usage.get("cache_read_input_tokens") or 0)
                )
                self.output_tokens += usage.get("output_tokens") or 0
            else:
                self.estimated_usd += reservation.upper
                self.unmeasured_calls += 1

    def cost_line(self) -> str:
        """The line a run prints at its end. Same shape as router_batch.py's."""
        line = (
            f"COST: ${self.measured_usd:.4f} from the provider's token counts "
            f"({self.calls - self.unmeasured_calls} calls, {self.input_tokens} input and "
            f"{self.output_tokens} output tokens), against the ${self.max_usd:.2f} cap."
        )
        if self.unmeasured_calls:
            line += (
                f" {self.unmeasured_calls} more calls returned no token counts and are "
                f"counted at their upper estimate, ${self.estimated_usd:.4f}."
            )
        if self.refused:
            line += f" {self.refused} calls were refused and not sent."
        return line


_cap: ContextVar[Optional[SpendCap]] = ContextVar("llm_spend_cap", default=None)


def current_cap() -> Optional[SpendCap]:
    return _cap.get()


@contextlib.contextmanager
def spend_cap(max_usd: float) -> Iterator[SpendCap]:
    """Bind a cap for this block. Tasks started inside it share the same total."""
    cap = SpendCap(max_usd)
    token = _cap.set(cap)
    try:
        yield cap
    finally:
        _cap.reset(token)


def reserve_call(model: str, input_chars: int, max_tokens: int) -> Optional[Reservation]:
    """Called by a provider leg before it sends. ``None`` when no cap is bound."""
    cap = _cap.get()
    if cap is None:
        return None
    return cap.reserve(model, input_chars, max_tokens)


def settle_call(reservation: Optional[Reservation], usage: Optional[Mapping[str, int]]) -> None:
    """Called by a provider leg after the call, measured or not."""
    if reservation is None:
        return
    cap = _cap.get()
    if cap is not None:
        cap.settle(reservation, usage)


def refuse_uncounted(what: str) -> None:
    """For a spend site that reports no cost (embeddings): refuse it under a cap."""
    cap = _cap.get()
    if cap is not None:
        with cap._lock:
            cap.refused += 1
        raise SpendCapUncounted(
            f"REFUSED: {what} has no cost count, so a capped run can't include it. "
            "Nothing was sent."
        )
