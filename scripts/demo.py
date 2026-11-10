from weaver_nexus import FrozenPolicy, Proposal, Rule, WeaverReferenceGate
from weaver_nexus.adapters import Candidate, select_advisory

# Do not use this program to authorize real-world actions.
gate = WeaverReferenceGate(FrozenPolicy([
    Rule("operator", "put", "memo"),
    Rule("auditor", "read", "memo"),
]), initial={"memo": "original"})
proposal = select_advisory((
    Candidate(Proposal("angela", "read", "memo"), "continuity review", 1),
    Candidate(Proposal("quillan", "put", "memo", "new", ("approved",)), "council", 3),
))
assert proposal is not None
result = gate.submit(trusted_principal="auditor", proposal=proposal)
print({"verdict": result.verdict, "reason": result.reason,
       "state": gate.snapshot(), "ledger_valid": gate.ledger.verify(),
       "ledger_head": gate.ledger.head})
