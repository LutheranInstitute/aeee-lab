# GitHub runner communication

Verify current official documentation when generating a production workflow:
https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands
https://docs.github.com/en/actions/tutorials/authenticate-with-github_token

## Environment files

| File | Purpose |
|---|---|
| GITHUB_ENV | Environment variables for later steps in the job; not the writing step |
| GITHUB_OUTPUT | Step outputs; give the step an id to reference them |
| GITHUB_PATH | Paths for later steps |
| GITHUB_STEP_SUMMARY | Per-step Markdown collected into the job summary |

Write UTF-8 and use shell-appropriate syntax. Use a collision-safe delimiter for multiline values, or a file for arbitrary data. Do not override reserved runner variables.

```bash
printf '%s\n' 'AE_LABEL=prepared' >> "$GITHUB_ENV"
printf '%s\n' 'result=prepared' >> "$GITHUB_OUTPUT"
printf '%s\n' "$RUNNER_TEMP/ae-bin" >> "$GITHUB_PATH"
printf '%s\n' '## Prepared' >> "$GITHUB_STEP_SUMMARY"
```

## Supported log commands

Use `::debug::`, `::notice::`, `::warning::`, `::error::`, `::group::`, `::endgroup::`, `::add-mask::`, `::stop-commands::`, and `::echo::` where appropriate. These are not collectively obsolete. Avoid obsolete `set-output` and `set-env` commands.

An error annotation alone does not fail a step; return a failing exit status. Register masks before disclosure; masking does not grant safe secret transport. Do not enable command echo around secrets. Use a unique stop-command token, then resume explicitly, when displaying untrusted text.

Keep GITHUB_TOKEN permissions minimal. Check event-specific access and runner trust. Do not run untrusted fork code in a privileged context.
