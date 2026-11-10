# Threat model — experiment, not a hardened access-control product

## Asset and boundary

Toy asset: the dictionary key `memo`. Binding policy is supplied by a trusted host and names effective principal, action (`read` or `put`), and resource. A proposed action is treated as untrusted content, even if it comes from a named AI architecture, a reflective council, or a confidence/vote score.

**Trusted computing base in this example:** the Python interpreter, `WeaverReferenceGate`, frozen policy constructor, the caller providing `trusted_principal`, `EvidenceLedger`, and the host process. None is isolated from another within the interpreter. No claim is made that this boundary holds against an adversary who can execute arbitrary Python or mutate process memory.

## Attacker capabilities in the local tests

- Control `Proposal.source`, `action`, `resource`, `value`, claimed permissions, and advisory notes.
- Rank council candidates and make self-approval claims in proposed content.
- Request unsupported actions such as `delete` or `policy.edit`.
- Corrupt or truncate an in-memory ledger in a test fixture.
- Deny service by creating unsupported inputs (not comprehensively tested).

## Bounded expected invariants

1. A proposed permission string has no effect on the trusted access-control decision.
2. The action registry, not the proposer's name for a permission, determines what is understood as `read` versus `put`.
3. No unsupported action mutates the toy state through the mediator.
4. On a failed receipt append, no toy-state change is committed.
5. Every admitted `submit` attempt yields an allow/deny receipt if receipt construction succeeds.
6. Mutating a record without recomputing hash breaks local chain verification.
7. A truncated ledger is only detectable **if a previously retained external head or length is provided**.
8. Candidate priority and advisory self-review do not constitute host authorization.

## NOT established — operationally blocking

- Authenticating the host principal. A malicious caller can currently supply `trusted_principal="operator"`.
- Preventing direct database/filesystem/process writes that never call `submit`.
- Preventing Python introspection or monkeypatching of the reference gate and policy.
- Cryptographic signatures, trusted key custody, replay protection or external witness independence.
- Durable atomicity: crash during receipt/state commit, multiple processes, rollbacks and storage recovery.
- Concurrency correctness against all interleavings or distributed revocation races.
- A canonical JSON profile with language-independent normalization, float semantics and replay envelopes.
- Host resource isolation, hardware veto, immutable deployment configuration or CI integrity.
- End-to-end performance, actual ANGELA/Quillan/T81 execution, or production suitability.

## P0 hostile review gate — WEAVER-GOV-NEG-001 (future)

At a pinned revision, an **independently reviewed** inventory must enumerate all mechanisms that can change effective policy or bypass the mediator: API, admin interface, filesystem/database, migrations, deployment credentials, service identity, process memory, and configuration. Attacks must attempt every path with real effective identities. Store effective policy **before and after** each attempt, raw exit status and artifacts, plus independent resource-state inspection. Report separate `passed`, `failed`, and `untested` totals. Any unauthorized effective-policy mutation counts as **FAILED**, even if the script itself exits zero. Unreachable or unsupported host controls count **UNTESTED**, never PASS.

The current experiment explicitly does **not** meet this gate; therefore production and authority remain denied.
