# Compatibility and disagreement matrix

**Scope:** repository sources observed at pinned `main` revisions on 2026-11-10; architectural comparison, not a validated integrated system. Source SHA and URLs: [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md).

| Question | Weaver OS (flagship) | ANGELA | Quillan-Ronin | T81 Foundation | Integration rule |
| --- | --- | --- | --- | --- | --- |
| Who proposes? | Bounded cognition / untrusted requestor | Reflexive reasoning and planning (documented) | Council/agent candidate selection (documented) | VM inputs / encoded programs (implemented within scoped profiles) | Proposers only return typed data |
| Who authorizes? | Separate trusted verification/policy plane is the target | Some source language describes self-ratifying sovereignty | Some source language describes a sovereign executor with native tools | Axion policy-before-effect is a design/implementation surface | **Weaver wins:** no self-authorization, ever |
| What is policy? | An externally governed rule set and authority model | Symbolic ethical/constitutional prompts and consistency metrics | Council safety/reflection and proposed tool guards | Explicit scoped Axion policy / interpreter rules | Only trusted host/config policy is binding; semantic judgments advisory |
| What counts as a receipt? | Schemas, signatures, replay, witness and promotion rules | Continuity/memory ledger concepts; self-reported metrics | Benchmarks, rationale, agent traces, model claims | Reproducible program artifacts, trace and formalized deterministic surface registry | Binding digest + execution evidence + independent witness are different fields |
| What happens on uncertainty? | Fail closed / maintain O0 | Can produce a reflective summary | Can produce disputed alternatives | Bounded deterministic profiles; no claims outside the profile | Deny unsupported action; log negative result |
| Where does state live? | Chronicle, canonical contracts, ledger and anchors under bounded validation | Context/memory continuity structures | Memory and council state concepts | Content-addressed CanonFS and typed VM states | Start with toy in-memory state; no persistence claim |
| Evidence status | Local bounded validation, portfolio E2 ceiling / W0 / O0 | Documentation and implementation artifacts, no end-to-end validation reproduced here | Large codebase; no claimed AGI or benchmark superiority independently checked here | Narrow cross-profile equivalence and determinism research with explicit limits in current README | **Never inherit evidence:** validate each adapter on exact source commit |

## Contradictions intentionally NOT reconciled

1. **Self-ratification versus non-sovereignty.** ANGELA's self-ratifying constitutional language and Quillan's sovereign-execution language cannot be admitted as policy authority under Weaver. Their outputs may be proposed context only.
2. **Heuristic safety versus enforceable access control.** Ethical scores, council votes, confidence, or intent text are not effective authorization. The trusted host must determine actual identity/action/resource.
3. **Bit-exact profile versus general determinism.** T81's bounded deterministic execution on declared profiles does not establish deterministic AI model generation or full multi-repository integration.
4. **Hash chain versus omission-resistance.** A locally consistent chain cannot detect a coherent truncation or rewrite by an actor who controls both ledger and its purported head. External anchoring is required.
5. **Static local tests versus hostile boundary enforcement.** All local tests may pass while a co-resident adversary bypasses the Python gate entirely. Hostile review must attempt actual bypass at every reachable execution/write path.
6. **Licenses.** Source-license headers and repository descriptions are not always concordant. Code transplants are deferred until reviewed and notice-preserving.

## Selection criteria for future upstream imports

Accept a component only if: (a) it solves a bounded problem not better solved by a simpler baseline; (b) its version and license are pinned; (c) it has a formally specified interface with a kill switch/fail-closed default; (d) hostile cases and counterexamples are run; (e) the component cannot authorize itself; (f) upstream claims remain attributed and scoped; and (g) adoption passes matched-compute or matched-workload comparison where performance is the motivation.

### Rejected shortcuts

- No bulk source tree copying or git submodule that silently broadens the trusted computing base.
- No mandatory ANGELA reflection as a substitute for policy enforcement.
- No Quillan council vote turned into a permit or a private execution credential.
- No T81 hardware/VM performance claims transferred to a Python integration wrapper.
- No Weaver authority or E-level upgrade simply because an integration repository exists.
