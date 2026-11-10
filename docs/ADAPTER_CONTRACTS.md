# Proposed integration contracts (NOT implemented)

This document defines future seams. None of these interfaces connects to an upstream runtime today.

## Advisory interface: ANGELA-like reviewer

Input: `task_digest`, read-only context/candidate, bounded time/resource budget. Output: typed `review_notes` with independently checkable references; no `allow`, `grant`, `policy_delta`, or executable tool invocation. Reflexive consistency is useful as an *advisory signal* and cannot sign or enact a policy decision.

## Deliberation interface: Quillan-like council

Input: task and allowed output schema. Output: one or more typed proposed actions, rationale, candidate ranking, source/version stamp. No credential, direct host tool, dynamic Python, assumed consensus, or implicit delegation. Compare its verified success rate and cost against a single-proposer baseline on frozen tasks. `select_advisory` currently sorts synthetic candidates only.

## Execution interface: T81-like deterministic adapter

Input: a frozen, policy-approved operation plus typed data/object hashes and a declared deterministic surface. Output: bounded execution result, measured outcome, exact object identifiers, interpreter/profile version, and raw trace. Outside profile -> `UNTESTED/REFUSE`, not a success claim. No VM, CanonFS, ternary hardware or TISC opcode is imported here.

## Weaver authority/evidence adapter — mandatory before real effects

Input: authenticated effective host identity, immutable operator-approved policy version, normalized action/resource, external witness context. Output: allow/deny (default deny), policy digest, immutable request digest, expiry/nonce and receipt. The proposing AI must not hold signing keys, mutate effective policy, or bypass the gate. The physical effect must occur only after final verification, with revocation and commit ordering specified. The existing flagship Weaver OS code is the source to evaluate; do not claim this demo replaces it.

## Acceptance gates

1. A committed, reviewed source SHA for each adapter and file-level license/notices inventory.
2. Complete authenticated access-path and policy-write-path inventory with adversarial cases, not only API calls.
3. Frozen schema and canonicalization vectors across at least two implementations.
4. Positive controls, failure injection, mutation checks and actual post-state observation.
5. Persistent atomic operation + receipt and independent external checkpoint.
6. Fresh-checkout reproduction under a non-origin witness and a results ledger that includes failed/untested outcomes.

Each adapter must remain disable-able independently. If any higher-trust dependency is unavailable or fails verification, no real-world effect is permitted.
