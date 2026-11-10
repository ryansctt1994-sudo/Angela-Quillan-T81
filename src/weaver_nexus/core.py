"""Bounded, in-process interoperability experiment; NOT a security sandbox."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from threading import RLock
from typing import Any, Iterable

GENESIS = "0" * 64
SUPPORTED_ACTIONS = frozenset({"read", "put"})


def canonical(value: Any) -> bytes:
    """Local deterministic JSON subset; not a cross-language canonical JSON standard."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Rule:
    principal: str
    action: str
    resource: str


@dataclass(frozen=True)
class Proposal:
    source: str
    action: str
    resource: str
    value: str | None = None
    claimed_permissions: tuple[str, ...] = ()
    advisory_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not all(isinstance(x, str) and 0 < len(x) <= 256 for x in
                   (self.source, self.action, self.resource)):
            raise ValueError("invalid proposal identity, action, or resource")
        if self.value is not None and not isinstance(self.value, str):
            raise ValueError("value must be a string or None")
        if not isinstance(self.claimed_permissions, tuple) or not all(
                isinstance(x, str) for x in self.claimed_permissions):
            raise ValueError("claimed_permissions must be a tuple of strings")
        if not isinstance(self.advisory_notes, tuple) or not all(
                isinstance(x, str) for x in self.advisory_notes):
            raise ValueError("advisory_notes must be a tuple of strings")


@dataclass(frozen=True, init=False)
class FrozenPolicy:
    """Trusted configuration: proposals cannot write or replace policy rules."""
    def __init__(self, rules: Iterable[Rule]):
        rules = tuple(rules)
        if any(not isinstance(r, Rule) or r.action not in SUPPORTED_ACTIONS or
               not r.principal or not r.resource for r in rules):
            raise ValueError("unsupported policy rule")
        immutable_rules = frozenset(rules)
        object.__setattr__(self, "_rules", immutable_rules)
        object.__setattr__(self, "digest", digest([asdict(r) for r in sorted(
            immutable_rules, key=lambda r: (r.principal, r.action, r.resource))]))

    def allows(self, principal: str, action: str, resource: str) -> bool:
        return action in SUPPORTED_ACTIONS and Rule(principal, action, resource) in self._rules


class EvidenceLedger:
    """In-memory hash chain; only externally retained heads detect coherent rewrite/truncation."""
    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = []

    def append(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = {"index": len(self._records), "previous_hash": self.head, "payload": payload}
        record = {**data, "hash": digest(data)}
        self._records.append(record)
        return json.loads(canonical(record))

    @property
    def head(self) -> str:
        return self._records[-1]["hash"] if self._records else GENESIS

    @property
    def length(self) -> int:
        return len(self._records)

    def records(self) -> list[dict[str, Any]]:
        return json.loads(canonical(self._records))

    def verify(self, *, expected_head: str | None = None,
               expected_length: int | None = None) -> bool:
        previous = GENESIS
        for index, record in enumerate(self._records):
            if not isinstance(record, dict) or set(record) != {
                    "index", "previous_hash", "payload", "hash"}:
                return False
            body = {k: record[k] for k in ("index", "previous_hash", "payload")}
            try:
                if record["index"] != index or record["previous_hash"] != previous or \
                        record["hash"] != digest(body):
                    return False
            except (ValueError, TypeError, OverflowError):
                return False
            previous = record["hash"]
        return (expected_head is None or previous == expected_head) and (
            expected_length is None or len(self._records) == expected_length)


@dataclass(frozen=True)
class Outcome:
    verdict: str
    reason: str
    value: str | None
    receipt_hash: str


class WeaverReferenceGate:
    """Toy resource mediator. Caller must supply authenticated identity from a trusted host.

    This module does NOT authenticate principals, isolate processes, block direct
    filesystem access, or enforce policy outside this instance. Never deploy as
    a production authorization system.
    """

    def __init__(self, policy: FrozenPolicy, *, initial: dict[str, str] | None = None):
        self._policy = policy
        self._state = dict(initial or {})
        self._lock = RLock()
        self.ledger = EvidenceLedger()

    def snapshot(self) -> dict[str, str]:
        with self._lock:
            return dict(self._state)

    @property
    def policy_digest(self) -> str:
        return self._policy.digest

    def submit(self, *, trusted_principal: str, proposal: Proposal) -> Outcome:
        if not isinstance(proposal, Proposal):
            raise TypeError("only Proposal accepted; host must validate transport input")
        with self._lock:
            before = digest(self._state)
            next_state = dict(self._state)
            verdict, reason, value = "DENY", "policy_denied", None
            if not isinstance(trusted_principal, str) or not trusted_principal:
                reason = "invalid_host_identity"
            elif proposal.action not in SUPPORTED_ACTIONS:
                reason = "unknown_action"
            elif not self._policy.allows(trusted_principal, proposal.action, proposal.resource):
                reason = "policy_denied"
            elif proposal.action == "put" and proposal.value is None:
                reason = "missing_value"
            elif proposal.action == "read":
                verdict, reason, value = "ALLOW", "authorized_read", next_state.get(proposal.resource)
            elif proposal.action == "put":
                next_state[proposal.resource] = proposal.value  # type: ignore[assignment]
                verdict, reason, value = "ALLOW", "authorized_put", proposal.value
            after = digest(next_state)
            # No local state change unless a receipt can be constructed and appended.
            # Still not a durable two-phase transaction or a cross-process security gate.
            record = self.ledger.append({
                "policy_digest": self._policy.digest,
                "trusted_principal": trusted_principal,
                "proposal": asdict(proposal),
                "verdict": verdict,
                "reason": reason,
                "state_before": before,
                "state_after": after,
            })
            self._state = next_state
            return Outcome(verdict, reason, value, record["hash"])
