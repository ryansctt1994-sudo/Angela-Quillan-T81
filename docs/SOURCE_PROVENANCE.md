# Source provenance and code-reuse boundaries

**Observed 2026-11-10.** Exact upstream GitHub branch-head commits at the review snapshot:

| Repo | Observed `main` commit | Selection evidence | Licensing observation |
| --- | --- | --- | --- |
| [Weaver OS](https://github.com/ryansctt1994-sudo/Weaver_Os) | `55bdfb9fce42065a0c97b3249e9887454b58a23b` (review snapshot; adoption still needs validation) | [README](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/55bdfb9fce42065a0c97b3249e9887454b58a23b/README.md), [portfolio status](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/55bdfb9fce42065a0c97b3249e9887454b58a23b/PORTFOLIO_STATUS.md) | MIT in README; independently review before copying |
| [ANGELA](https://github.com/t81dev/ANGELA/tree/956d201277b5c207a10fbcc4797e36d69037c875) | `956d201277b5c207a10fbcc4797e36d69037c875` | [README](https://github.com/t81dev/ANGELA/blob/956d201277b5c207a10fbcc4797e36d69037c875/README.md), `docs/ARCHITECTURE.md`, `docs/STATUS.md` | Root `LICENSE`: MIT, copyright t81dev 2026 |
| [Quillan-Ronin](https://github.com/leeex1/Quillan-Ronin/tree/c9895fdc8b2ee11b70c80e4fc9ba05f12a1e6ba5) | `c9895fdc8b2ee11b70c80e4fc9ba05f12a1e6ba5` | [README](https://github.com/leeex1/Quillan-Ronin/blob/c9895fdc8b2ee11b70c80e4fc9ba05f12a1e6ba5/README.md), `01 - Core Architecture/specs.md` | README claims MIT/modified MIT, root LICENSE starts Apache-2.0; **inconsistent in reviewed materials**; do not transplant until clarified |
| [T81 Foundation](https://github.com/t81dev/t81-foundation/tree/e5c30560aa77c31184a14b03ed152a6deef5c1a3) | `e5c30560aa77c31184a14b03ed152a6deef5c1a3` | [README](https://github.com/t81dev/t81-foundation/blob/e5c30560aa77c31184a14b03ed152a6deef5c1a3/README.md), `docs/governance/DETERMINISM_SURFACE_REGISTRY.md` | Root `LICENSE`: Apache 2.0 |

**The Weaver OS reference revision is pinned for comparison, but executable-contract adoption requires separate verification.** This lab uses independent code and avoids implying it imports Weaver's existing gate: the actual Weaver `policy/policy_gate.py` and `policy/signed_verifier_adapter.py` remain documented TODO stubs (C-STUB-001 in Weaver's README at review time).

### Provenance assertions

- No ANGELA, Quillan-Ronin, T81 Foundation, or Weaver OS implementation code is vendored in this project.
- Architectural patterns are compared and independently re-expressed as a small reference experiment; sources retain their names, owners, and separate claims.
- These source SHA values identify what was inspected. They are not cryptographic proofs of license provenance, quality, or downstream compatibility.
- A component import requires a new source manifest with file hashes, licenses, import path, test matrix, and external custody before use.

**No endorsement, collaboration, approval, or transfer of rights by the upstream maintainers is implied.**
