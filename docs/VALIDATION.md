# Evidence and validation scope

**Date:** 2026-11-10 · **Subject:** local Python reference harness (NOT the upstream projects) · **Evidence ceiling:** local author-run tests only · **Independent reproductions:** 0 · **Witness:** W0 · **Operational authority:** O0.

## Local commands

```bash
export PYTHONPATH=src
python -m unittest discover -s tests -v
python scripts/demo.py
```

Author-run initial local check: **23 tests passed (0 failures)** with source import via `PYTHONPATH=src`, then an independent demo invocation in the same local environment. The GitHub Actions workflow is included as a **candidate gate**. At the time of drafting, it has **not** been observed running on a published GitHub commit. Do not report CI pass until actual CI logs exist.

## Positive / negative controls

| Case | Outcome expected | Caveat |
| --- | --- | --- |
| Operator exact-match `put` | ALLOW, toy state updates | Valid positive control; no real identity authentication |
| Auditor `read` | ALLOW, toy state unchanged | Local method semantics only |
| Auditor `put` + claimed approval | DENY, toy state unchanged | Claimed permission ignored |
| Unsupported `delete` and `policy.edit` | DENY | No real policy path exists in this harness |
| Candidate council vote for prohibited write | DENY | Selection must not authorize |
| Receipt append exception | No state commit | In-memory only; no crash/recovery proof |
| Tampered record or hash | Chain verifier reports false | Hash does not prevent rewriting whole history |
| Removed tail without external anchor | Chain verifier reports true | **Expected negative result**: local omission resistance fails |
| Removed tail against retained external head | Verification false | Requires real external custody, absent here |
| Same input and initial state | Matching local receipt hashes | Not a cross-platform determinism claim |

## Tests that remain unexecuted

Actual ANGELA runtime import, Quillan inference/council metrics, T81 ISA/VM/CanonFS execution, Weaver cryptographic authority adapter, invalid principal impersonation under host identity, external-mediator bypass, crash atomicity, external witness, independent reproduction, and matched-compute performance baselines.

**A passing local suite does not override the listed untested gates.** Evidence from the three upstream repositories is not inherited. An always-deny mutant would be rejected by the positive-control assertion, but this is not a comprehensive mutation campaign.

## Release criterion

To advance: pin code/config/test revisions, independently inspect source inventory, run negative cases and valid controls on a fresh checkout, archive stdout/stderr/exit codes and raw state evidence, compute a file manifest, obtain an external retained head, and repeat under a second evaluator. Assign evidence and witness grades separately. A release label is not approval to execute high-stakes actions.
