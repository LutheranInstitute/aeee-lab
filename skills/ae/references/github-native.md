# GitHub Actions native lifecycle

Read current official contracts when implementing:
https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
https://docs.github.com/en/rest/actions/workflows

## Select and prepare

Verify the account and repository. Inspect available workflows, current state, default branch, requested ref, declared inputs, effects, and runner requirements. Inspect the workflow at the execution ref; do not infer safety from its name. Resolve the intended source revision.

Manual dispatch requires workflow_dispatch and a workflow present on the default branch. Check repository access and the exact transport's permissions. Do not merge a prepared workflow merely to make it dispatchable unless authorized.

Discover actual connector capabilities. A GET-only fetch tool cannot dispatch. Prefer a supported mutation connector; otherwise use an authenticated supported CLI/API when available. If no execution transport exists, leave a concrete reviewed plan and identify dispatch as pending. Do not invent callable tools or collect credentials in chat.

## Dispatch and observe

Validate inputs and ref. Pass input JSON through structured arguments or stdin; never embed untrusted expressions into shell code. For an authenticated GitHub CLI, the documented pattern is:

```bash
gh workflow run "$AE_WORKFLOW" --repo "$AE_REPO" --ref "$AE_REF" --json < "$AE_INPUTS_FILE"
```

These variables are task-local placeholders; set them only from checked facts and a reviewed JSON file. Do not place secrets in that file.

Inspect the actual dispatch response. When it does not provide a run ID, correlate workflow, event, ref/revision, inputs or a supported unique marker, and dispatch time. Do not choose an unrelated latest run. If correlation remains ambiguous, report it rather than redispatching.

Track queued, running, waiting, and terminal states. Inspect relevant jobs, logs, summaries, and artifacts. Interpret the run conclusion separately from provider-effect verification. Rerun or cancellation is a separate mutation: check scope and prior effects before acting. Retry only the appropriate work and preserve attempt history.

## Control surfaces

A public index may expose documentation, public run status, and links to GitHub's Actions UI. Authenticated dispatch, private logs, and repo writes require a real supported connector or backend. Do not label a static button connected, simulate successful runs, or embed credentials in HTML. Do not overwrite an existing /ae/ index without inspecting its role and obtaining scope for that change.
