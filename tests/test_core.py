import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch
from weaver_nexus import (EvidenceLedger, FrozenPolicy, Proposal, Rule,
                          WeaverReferenceGate, canonical, digest)
from weaver_nexus.adapters import Candidate, select_advisory


def gate():
    return WeaverReferenceGate(FrozenPolicy([
        Rule("operator", "put", "memo"),
        Rule("operator", "read", "memo"),
        Rule("auditor", "read", "memo"),
    ]), initial={"memo": "original"})


class BoundaryTests(unittest.TestCase):
    def test_authorized_write_changes_state(self):
        g = gate()
        out = g.submit(trusted_principal="operator", proposal=Proposal("quillan", "put", "memo", "updated"))
        self.assertEqual(out.verdict, "ALLOW")
        self.assertEqual(g.snapshot()["memo"], "updated")
        self.assertTrue(g.ledger.verify(expected_head=out.receipt_hash, expected_length=1))

    def test_read_only_principal_cannot_write_even_with_permission_claim(self):
        g = gate()
        before = g.snapshot()
        result = g.submit(trusted_principal="auditor", proposal=Proposal("angela", "put", "memo", "BAD", ("operator", "put", "approved")))
        self.assertEqual(result.verdict, "DENY")
        self.assertEqual(g.snapshot(), before)

    def test_unknown_action_fails_closed(self):
        g = gate()
        out = g.submit(trusted_principal="operator", proposal=Proposal("quillan", "delete", "memo"))
        self.assertEqual((out.verdict, out.reason), ("DENY", "unknown_action"))
        self.assertEqual(g.snapshot(), {"memo": "original"})

    def test_policy_edit_proposal_denied(self):
        g = gate()
        old_policy = g.policy_digest
        out = g.submit(trusted_principal="operator", proposal=Proposal("angela", "policy.edit", "memo", "ALLOW ALL"))
        self.assertEqual(out.verdict, "DENY")
        self.assertEqual(g.policy_digest, old_policy)

    def test_identity_is_host_supplied_not_proposer_supplied(self):
        g = gate()
        out = g.submit(trusted_principal="guest", proposal=Proposal("operator", "put", "memo", "spoof"))
        self.assertEqual(out.verdict, "DENY")

    def test_missing_value_denied_and_logged(self):
        g = gate()
        out = g.submit(trusted_principal="operator", proposal=Proposal("quillan", "put", "memo"))
        self.assertEqual((out.verdict, out.reason), ("DENY", "missing_value"))
        self.assertEqual(g.ledger.length, 1)

    def test_empty_principal_denied(self):
        g = gate()
        out = g.submit(trusted_principal="", proposal=Proposal("quillan", "put", "memo", "x"))
        self.assertEqual(out.reason, "invalid_host_identity")

    def test_authorized_read_does_not_mutate(self):
        g = gate()
        out = g.submit(trusted_principal="auditor", proposal=Proposal("angela", "read", "memo", "ignored"))
        self.assertEqual((out.verdict, out.value), ("ALLOW", "original"))
        self.assertEqual(g.snapshot(), {"memo": "original"})

    def test_council_priority_never_grants_permission(self):
        g = gate()
        selected = select_advisory((
            Candidate(Proposal("angela", "read", "memo"), "reflection", 1),
            Candidate(Proposal("quillan", "put", "memo", "BAD", ("self-approved",)), "council", 999)))
        self.assertEqual(selected.source, "quillan")
        result = g.submit(trusted_principal="auditor", proposal=selected)
        self.assertEqual(result.verdict, "DENY")
        self.assertEqual(g.snapshot()["memo"], "original")

    def test_no_candidate_returns_none(self):
        self.assertIsNone(select_advisory(()))

    def test_policy_rules_are_not_inferred_from_request(self):
        g = gate()
        out = g.submit(trusted_principal="auditor", proposal=Proposal("quillan", "put", "memo", "x", ("read",)))
        self.assertEqual(out.verdict, "DENY")

    def test_same_input_same_receipt(self):
        a, b = gate(), gate()
        p = Proposal("quillan", "put", "memo", "same", advisory_notes=("angela: review",))
        self.assertEqual(a.submit(trusted_principal="operator", proposal=p).receipt_hash,
                         b.submit(trusted_principal="operator", proposal=p).receipt_hash)

    def test_full_record_tamper_detected(self):
        g = gate()
        g.submit(trusted_principal="operator", proposal=Proposal("quillan", "put", "memo", "x"))
        g.ledger._records[0]["payload"]["verdict"] = "DENY"
        self.assertFalse(g.ledger.verify())

    def test_truncation_requires_external_head(self):
        g = gate()
        g.submit(trusted_principal="operator", proposal=Proposal("quillan", "put", "memo", "x"))
        original_head = g.ledger.head
        g.submit(trusted_principal="auditor", proposal=Proposal("angela", "read", "memo"))
        pinned_head = g.ledger.head
        g.ledger._records.pop()
        self.assertTrue(g.ledger.verify())  # An intentional LIMITATION, not proof of completeness.
        self.assertEqual(g.ledger.head, original_head)
        self.assertFalse(g.ledger.verify(expected_head=pinned_head, expected_length=2))

    def test_invalid_transport_input_refused(self):
        g = gate()
        with self.assertRaises(TypeError):
            g.submit(trusted_principal="operator", proposal={"action": "put"})

    def test_nonfinite_float_not_canonical(self):
        with self.assertRaises(ValueError):
            canonical({"x": float("nan")})

    def test_rule_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            FrozenPolicy([Rule("operator", "delete", "memo")])

    def test_tampered_receipt_hash_detected(self):
        led = EvidenceLedger()
        led.append({"x": 1})
        led._records[0]["hash"] = "f" * 64
        self.assertFalse(led.verify())

    def test_positive_control_reject_all_mutant_would_fail(self):
        g = gate()
        self.assertEqual(g.submit(trusted_principal="operator", proposal=Proposal("quillan", "put", "memo", "OK")).verdict, "ALLOW")

    def test_proposal_validation_rejects_invalid_source(self):
        with self.assertRaises(ValueError):
            Proposal("", "read", "memo")

    def test_receipt_failure_cannot_mutate_local_store(self):
        g = gate()
        with patch.object(g.ledger, "append", side_effect=RuntimeError("receipt unavailable")):
            with self.assertRaises(RuntimeError):
                g.submit(trusted_principal="operator", proposal=Proposal("quillan", "put", "memo", "BAD"))
        self.assertEqual(g.snapshot(), {"memo": "original"})

    def test_normal_policy_field_assignment_is_blocked(self):
        p = FrozenPolicy([Rule("operator", "read", "memo")])
        with self.assertRaises(FrozenInstanceError):
            p.digest = "attacker"  # type: ignore[misc]

    def test_canonical_key_order_independent(self):
        self.assertEqual(digest({"z": 2, "a": 1}), digest({"a": 1, "z": 2}))


if __name__ == "__main__":
    unittest.main()
