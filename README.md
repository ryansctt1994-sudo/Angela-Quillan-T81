# WEAVER NEXUS — Interoperability Lab

**A bounded, clean-room interoperability experiment. Weaver OS remains the flagship and the canonical authority/evidence spine.**

This repository is **not** a merger of ANGELA, Quillan-Ronin, T81 Foundation, or Weaver OS. It contains a small original Python reference harness and a comparative specification. It does not copy upstream implementation code or transfer upstream assurance claims, names, or project governance. The existing [Weaver OS](https://github.com/ryansctt1994-sudo/Weaver_Os) remains the portfolio anchor.

> **Disposition:** `RESEARCH_PROTOTYPE` · `LOCAL_TESTS_ONLY` · `INDEPENDENT_REPRODUCTION=0` · `WITNESS=W0` · `AUTHORITY=O0` · `PRODUCTION=PROHIBITED`. These labels apply to this repository, not to the upstream projects.

## Single research question

**Can independently produced reasoning proposals be usefully composed without transferring any power to authorize actions, edit governing policy, or certify evidence?**

The answer is not presumed. The current harness only checks a deliberately small in-process example. An implementation in one Python process does **not** prove that a hostile component cannot bypass the gate in a real deployment.

## Conceptual contributions, with authority kept separate

| Source | Candidate concept | Placement here | Authority consequence |
| --- | --- | --- | --- |
| [Weaver OS](https://github.com/ryansctt1994-sudo/Weaver_Os) | Proposal/authority separation, fail-closed validation, receipt discipline | **Flagship contract**; small reference gate, not imported Weaver code | Only a separately trusted host-provided principal plus frozen exact-match policy can allow the toy action |
| [ANGELA](https://github.com/t81dev/ANGELA) | Self-review, ethics/context reflection, continuity annotations | **Untrusted advisory notes** | Cannot ratify its own authority or modify the policy |
| [Quillan-Ronin](https://github.com/leeex1/Quillan-Ronin) | Specialist council proposals and candidate ranking | **Untrusted candidate selector** | Council preference and permission claims are ignored by authorization |
| [T81 Foundation](https://github.com/t81dev/t81-foundation) | Deterministic typed operations, scoped replay, content-hash evidence | **Local bounded JSON/sha256 digest experiment** | No inherited VM/hardware/CanonFS verification or cross-platform bit-exact claim |

The actual upstream implementations are **not connected**. ANGELA, Quillan, and T81 are **inspirations with pinned references**, not functioning plugins in this PR. A future adapter must satisfy its own interface contract and evidence gates.

## Reference path

```text
ANGELA-style review (untrusted)       Quillan-style candidates (untrusted)
                \                              /
                 ---> advisory-only proposal <--
                               |
                               v
       trusted host identity (not derived from proposal)
                               |
                               v
              WEAVER-style policy decision
                 |                   |
             DENY|                   |ALLOW (toy read/put)
                 +--------+----------+
                          |
                local hash-chain receipt
                          |
                in-memory resource state
```

The harness supports two toy actions (`read`, `put`) on an in-memory dictionary. It deliberately supports **no filesystem, network, shell, deployment, policy-write, or external side effects**. Authorization is exact-match on `principal + action + resource`, derived from **trusted policy** and never from the proposed permission set.

**Critical limitation:** `trusted_principal` is passed to the Python method by its caller. A real host must authenticate and bind it to an effective identity; the harness does not. A malicious module with interpreter-level access could tamper with internal state, monkeypatch the kernel, or call the gate with a forged principal. The security boundary remains **unproven**.

## Reproduce locally

```bash
export PYTHONPATH=src
python -m unittest discover -s tests -v
python scripts/demo.py
```

No AI model, hardware, GPU, secret, or network service is needed. The reference run is expected to deny an auditor's proposed write and leave the stored value unchanged.

## What the tests establish (and do not)

The initial author-run suite contains **23 local unit tests** covering valid read/write, unsupported action denial, permission-claim spoofing, host-supplied identity separation within the test harness, requested policy edit rejection, failed-receipt no-commit behavior, stable local hashes, and hash-chain tampering. One test intentionally demonstrates that a **truncated ledger verifies locally without an externally retained head**. A positive authorized action provides a basic control against an always-deny implementation.

This is a **bounded local result**, not an independent reproduction, a security proof, a hardware validation, an end-to-end ANGELA/Quillan/T81 integration, or a demonstration that policy remains safe from a malicious process. See [validation scope](docs/VALIDATION.md) and [threat model](docs/THREAT_MODEL.md).

## Next acceptance gate

Before attempting a real integration, implement an **out-of-process trusted mediator**, external principal authentication, immutable operator-controlled policy provisioning, complete inventory of write paths, durable atomic commit, and externally anchored receipts. Then test all bypass paths against the same pinned revision with passing/failing/untested counts, plus independent replay. No upstream module may declare its own PASS.

## Review documents

- [Compatibility matrix, conflicts, and exclusions](docs/COMPATIBILITY_MATRIX.md)
- [Source revisions, license cautions, and attribution](docs/SOURCE_PROVENANCE.md)
- [Threat model and explicitly unproven boundaries](docs/THREAT_MODEL.md)
- [Validation commands and evidence claims](docs/VALIDATION.md)
- [Proposed future adapter contracts](docs/ADAPTER_CONTRACTS.md)

## Licensing

The original reference code in this repository follows the repository's MIT license. **No upstream code has been copied.** Consult the actual license and notices of each upstream component before any future reuse; the Quillan repository currently contains inconsistent license labeling between its README and LICENSE file, so no license compatibility for imported Quillan code is asserted. This work is independent and does not imply endorsement by upstream maintainers.
