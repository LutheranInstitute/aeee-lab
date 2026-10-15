# RFC-æQR-0001 — Recursive Addressability of Agentic Environments

**Status:** Locked design doctrine · v1.0 (specification, not deployed protocol)  
**Project:** #OpenSourceWare (#OSW) → #InternetOfAgents (#IoA)  
**Principal:** HUMAN://principal

> **æQR makes the nested environment discoverable and portable.**  
> It gives intelligent work an address — a way to recover its context, a path to reuse, and a route to publication. Every widget carries its own æQR. Every loft can become a tower. Every tower can become a city.

## Doctrine

1. **Every widget has an æQR.** It identifies a stable, version-resolvable capability or work product, not a credential.
2. **Every loft can become a tower.** A contained environment may be independently addressed, forked, configured and published.
3. **Every tower can become a city.** A portable environment may become a discoverable index of subordinate environments and capabilities.
4. **Recursion preserves lineage, not authority.** Parent and child may share nonsecret context and provenance; no child inherits the parent's permission, identity or tokens.
5. **The human remains principal.** Every consequential effect requires its own valid authorization at the execution boundary.
6. **Witness closes the loop.** Results and lineage are recorded as evidence, with claims distinguished from independently verified execution.

## Address resolution contract (proposed)

An æQR encodes a **durable HTTPS resolver URL**. The resolver returns or points to a versioned manifest with:

- `id`, `version`, `kind` (`widget | loft | tower | city`)
- `canonical_url`, `parent_id` (optional), `children` (optional)
- `manifest_url`, `capabilities`, `required_permissions`
- `context_pointer` (nonsecret, access controlled as necessary)
- `issuer`, `provenance`, `witness_pointer`
- `fork_source`, `publication_status`

A QR payload MUST NOT contain access tokens, private user context, credentials, or implied authorization. Resolution is discovery; execution is a separate human-governed operation.

## Composition

```text
🫵 HUMAN://principal
    ↓ intent
🧩 WIDGET + æQR
    ↓ composition / fork
🚪 LOFT + æQR
    ↓ promote / publish
🏢 TOWER + æQR
    ↓ federate / index
🌐 CITY + æQR
    ↓ discover / interoperate
🛸 #InternetOfAgents
    ↓ verify
🧾 WITNESS → 🫵
```

**Invariant:** Context may propagate; authority does not.

**Thesis:** #OSW yields #IoA **when** open, portable work is made addressable, interoperable, permissioned, and verifiable. Open licensing or a QR code alone is insufficient.

## Implementation gates

- [ ] Implement and host HTTPS resolver.
- [ ] Define and validate the manifest JSON Schema and versioning rules.
- [ ] Generate an actual scannable QR from the resolver URL and decode-test it.
- [ ] Implement parent-child traversal, cycle prevention and fork lineage.
- [ ] Separate discovery from identity verification and per-effect authorization.
- [ ] Verify capability invocation and Witness receipts with real connected providers.
- [ ] Test portability across clients and publish the specification.

The existing `aeqr://widget/mcp/codex-micro` is **symbolic**, not a registered resolver or usable QR payload. This document fixes the design contract without claiming those implementation gates have passed.
