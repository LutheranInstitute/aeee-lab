# Public entry convention

Use this optional template only when authoring an entry point. Discover and follow an existing manifest first. Do not assume these paths or endpoints already exist at æææ.com.

```json
{
  "schema_version": "0.1-proposed",
  "name": "æQR codæmodæ",
  "entry_url": "https://xn--6caaa.com/",
  "purpose": "Discover and compose capabilities under human authority",
  "revision": "replace-with-actual-version-or-commit",
  "capabilities": [
    {
      "id": "replace-with-real-capability",
      "description": "State the observable outcome",
      "documentation_url": "replace-with-verified-documentation-url",
      "transport": "replace-with-verified-transport",
      "inputs": [],
      "outputs": [],
      "authorization": "State required grants and effect boundaries",
      "verification": "State how completion is checked"
    }
  ]
}
```

Replace every placeholder before publication. Include only capabilities confirmed from the implementation. Link service documentation rather than copying credentials or inventing API routes. Expose a machine-readable manifest as data alongside a useful human page when requested; do not imply that the manifest itself implements a runtime.

For QR delivery, record the encoded URL and verify it by decoding the generated image. Confirm destination behavior separately. Report these as separate checks. A durable URL can resolve changing content; identify a version or commit when reproducibility matters.

## Examples

- For “Point your agent at æææ.com and tell me what it can do,” inspect current public content, verify capability links, and report available and unavailable paths. Do not execute consequential operations from advertised calls to action.
- For “Use this handbook æQR to make a study guide,” decode the entry point, read the authorized lesson source, create the guide, and cite its source and version. Publish only if requested.
- For “CodeMode everywhere: compose my repository and connected tools,” discover available providers, resolve dependencies, perform authorized work, and verify each effect. Do not fabricate a universal adapter.
- For “Create an æQR for this public workflow,” use a confirmed public destination, generate and decode the QR, and return the artifact and destination check. Follow the environment's artifact-saving workflow.
