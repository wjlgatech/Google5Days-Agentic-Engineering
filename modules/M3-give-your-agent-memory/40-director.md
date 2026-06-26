# M3 for the 🎯 40-year-old AI Director — Give Your Agent Memory

*Goal: treat context + memory as a governed data asset — the place where personalization value
and privacy/security risk both concentrate.*

## Plain explanation

Memory is what turns a generic model into *your* assistant — and it's also where you accumulate
personal data, with all the governance that implies. Two systems to fund and govern: **session**
(transient) and **memory** (durable, per-user, curated). And a strategic distinction: **RAG** =
expert on your *facts/knowledge* (shared, auditable); **memory** = expert on the *user* (private,
isolated). Different data, different controls, different value.

## Concrete example

The exercise keeps **provenance** on every memory and **prunes** stale data — the seeds of a
governance posture (know where each fact came from; forget what you shouldn't keep). Scale that:
PII redaction before persistence, per-user isolation/ACLs, retention/TTL policy, and validation
against **memory poisoning**. The same `memory/` pattern is how this hub stores its *team* memory
(decisions + lessons) — auditable organizational knowledge.

## Hands-on exercise

```bash
cd exercise && python3 context_manager.py --selftest
```
Director's lens:
1. **Data map:** for one agent, list what lands in session vs. long-term memory vs. RAG; mark
   each with a sensitivity class and a retention policy.
2. **Set the controls:** require PII redaction-before-persist, per-user isolation, and
   provenance on every memory as a platform standard.
3. **Decide RAG vs. memory** for personalization features — and who owns each store.

## Real-world use case

Standing up personalization safely: a governed memory service (isolation, provenance, retention),
a RAG knowledge base (versioned, access-controlled), and a policy for what may be remembered.
This module + the hub's [`memory/`](../../memory/) + [`schemas/`](../../schemas/) are a copyable
miniature of that governed-memory operating model.

## Failure mode

**Ungoverned memory.** Cross-user leakage (missing isolation), unbounded retention of PII, no
provenance (can't audit or delete), and **memory poisoning** (an attacker writes false durable
"facts"). Plus the cost/quality tax of **context rot** when teams never compact. The director
failure is treating memory as a feature instead of governed data.

## Measurable output

A one-page **memory-governance standard**: the data map (session/memory/RAG × sensitivity), the
required controls (isolation, PII redaction, provenance, TTL), and the owner. **Done when** no
production memory feature ships without isolation + provenance + a retention policy, enforced in
review.

## Next step

- Operationalize evaluation of context use → **M4 (Agent Quality)**: measure RAG/context handling
  in the trajectory (did it ground its answer, or hallucinate?).
- Plan the production data plane → **M5**: stateful deploy, externalized state, observability.
