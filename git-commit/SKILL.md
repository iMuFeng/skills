---
name: git-commit
description: Create clean, reviewable git commits for code changes. Use when the user asks to commit changes, especially when a large or mixed working tree should be split into multiple logical commits.
---

# Git Commit

Use this skill when the user asks to commit changes in a git repository.

## Goal

Create clean, reviewable commits that each represent one coherent, independently understandable change. For large or mixed change sets, prefer several logically ordered commits over one catch-all commit.

## Behavior

1. Inspect the current repository state before committing:

   * Run `git status`.
   * Review changed files.
   * Review diffs with `git diff` and, when relevant, `git diff --staged`.

2. Plan the commit split before staging:

   * For anything beyond a small, single-purpose change, identify the intended commits and map files or hunks to each one.
   * Split by intent and independently revertible unit: feature, fix, refactor, test, build, chore, or documentation change.
   * Keep an implementation with its directly related tests and necessary documentation when they form one atomic change.
   * Separate opportunistic refactors, formatting, generated noise, dependency maintenance, and unrelated fixes from the primary change.
   * If one file contains changes for multiple purposes, stage only the relevant hunks when practical.
   * Do not split mechanically by file count. A focused commit may touch many files, while one file may require several commits.
   * Treat one large commit as an exception. Use it only when the changes are genuinely inseparable and splitting would create misleading or broken intermediate commits.

3. Stage and commit one logical group at a time:

   * Prefer explicit paths or patch staging for large or mixed working trees; do not start with `git add -A` or `git add .` unless every change belongs to the same commit.
   * Before each commit, inspect `git diff --staged --stat` and `git diff --staged` to verify that the staged set has exactly one purpose.
   * Commit that group, then inspect `git status` and repeat for the next group.
   * Order commits so foundational refactors or build changes come before the features that depend on them, while keeping each commit valid when practical.

4. Protect the repository:

   * Do not commit secrets, credentials, tokens, private keys, generated noise, or unrelated local files.
   * Do not modify files only to make a commit unless the user explicitly asked for edits.
   * Do not push commits without the user's confirmation (see step 7).
   * If there are no changes to commit, report that clearly and do not create an empty commit unless explicitly requested.

5. Validate when appropriate:

   * Run relevant tests, linters, or formatters when they are obvious and reasonably scoped.
   * If validation fails, explain the failure and avoid committing broken changes unless the user explicitly instructs otherwise.

6. Omit the `Co-Authored-By` trailer from commit messages.

7. Offer to push when commits are ready:

   * After all commits are created, summarize them with `git log --oneline @{u}..HEAD` (or the new commits if there is no upstream).
   * Ask: **Push these commits to `origin`?** Offer two choices: `Push to origin/<branch>` and `Keep local`.
   * Prefer the current environment's available interactive question or selection tool, using its actual interface and respecting its execution-mode limits. Do not assume any product-specific tool name or API exists. Use numbered text options only when no suitable interactive tool is available or permitted, and briefly explain the limitation. Do not merely print options when a suitable interactive tool is available.
   * Wait for the user's explicit selection. A preselected option, an unanswered asynchronous question, or elapsed time is not a selection. Ask even if the request already mentions pushing.
   * If the user selects push, run `git push` (use `git push -u origin <branch>` when the branch has no upstream) and report the result. Do not use `--force`, `--tags`, or `--mirror`.
   * If the user selects `Keep local`, leave the commits local and do not push.

## Atomic Commit Check

Before creating each commit, verify that:

* The commit has one clear purpose that can be summarized in one subject line.
* Every staged file or hunk supports that purpose.
* Reverting the commit would undo only that purpose.
* Required tests, schema changes, lockfile updates, or generated artifacts are included with the change that requires them.
* Unrelated work remains unstaged for a later commit.

## Commit Message Rules

Use [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) for every commit.

Commit messages must follow this structure:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Allowed common types include:

* `feat`: a new feature
* `fix`: a bug fix
* `docs`: documentation-only changes
* `style`: formatting or style changes that do not affect behavior
* `refactor`: code changes that neither fix a bug nor add a feature
* `perf`: performance improvements
* `test`: adding or updating tests
* `build`: build system or dependency changes
* `ci`: CI configuration changes
* `chore`: maintenance tasks
* `revert`: reverting a previous commit

## Message Quality

* Use an imperative, concise description.
* Keep the subject line focused and specific.
* Prefer a scope when it improves clarity.
* Add a body when the reason for the change is not obvious from the subject.
* Add footers for breaking changes or issue references when relevant.

## Examples

```text
feat(auth): add session refresh handling
```

```text
fix(api): handle empty response payloads
```

```text
docs(readme): clarify local setup steps
```

```text
refactor(ui): split dashboard widgets by responsibility
```

For breaking changes, use `!` or a `BREAKING CHANGE` footer:

```text
feat(api)!: remove legacy user endpoint

BREAKING CHANGE: The `/v1/users/legacy` endpoint has been removed.
```
