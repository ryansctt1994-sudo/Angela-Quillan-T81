"""Advisory-only multi-system candidate selection. No execution or approval API."""
from dataclasses import dataclass
from .core import Proposal


@dataclass(frozen=True)
class Candidate:
    proposal: Proposal
    rationale: str
    priority: int = 0  # Untrusted preference, NEVER authorization.


def select_advisory(candidates: tuple[Candidate, ...]) -> Proposal | None:
    """Deterministic candidate ordering; selected output still requires Weaver gate."""
    if not candidates:
        return None
    if any(not isinstance(item, Candidate) or not isinstance(item.proposal, Proposal)
           or not isinstance(item.priority, int) for item in candidates):
        raise ValueError("invalid advisory candidate")
    best = sorted(candidates, key=lambda c: (-c.priority, c.proposal.source,
                    c.proposal.action, c.proposal.resource, c.proposal.value or ""))[0]
    return best.proposal
