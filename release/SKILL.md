---
name: release
description: Release iOS, Android, Node (package.json), or mygo (mygo.json) projects by incrementing versions and build numbers, committing, tagging, and pushing to Git. Use for project releases, not just standalone version edits or store/package publishing.
---

# Release

Update versions, create a Git commit and tag, and push to the remote. Invoking this skill authorizes this workflow; it does not authorize npm publishing, app store uploads, deployments, or creating a GitHub Release.

## First step: require a clean working tree

Before discovering release targets, reading versions, offering choices, or contacting remotes, locate the Git root and read applicable repository instructions, then run `git status --porcelain=v1 --untracked-files=all --ignore-submodules=none` from that root. Apply this check on every invocation, including retries. If the check fails or the directory is not a Git repository, report the problem and stop.

Any staged, unstaged, untracked (non-ignored), conflicted, or dirty submodule entry blocks the release. List the affected paths, tell the user that uncommitted changes must be handled before rerunning the skill, and end the invocation immediately. Do not offer version choices, automatically commit or stash changes, discard files, or proceed with any release step. This also applies to uncommitted version edits left by an interrupted release; preserve them and report the incomplete state. Ignored files do not block the check.

## Required release choice

After the clean-working-tree check passes, identify the release target and read its current version and build number without modifying files. Resolve missing, unsupported, or conflicting values using the platform rules below before calculating choices. For every new release, ask: **Which version bump should this release use?** Display all four options as `<Choice> v<current-version>-<current-build> -> v<next-version>-<next-build>`, calculating each next version using the shared and platform-specific rules below. For a current version of `0.1.0` and build number `41`, show:

- `Major v0.1.0-41 -> v1.0.0-42`
- `Minor v0.1.0-41 -> v0.2.0-42`
- `Patch v0.1.0-41 -> v0.1.1-42`
- `Build v0.1.0-41 -> v0.1.0-42`

Use the actual project version and numeric build values, not these example values or literal N / (N+1) placeholders. The next build number is always the current build number plus one. Explain that all choices increment the build number once, including Build. For a legacy two-component Node version, label Build as requiring a format decision and follow the Node-specific rule below if selected; do not imply it is ready to release unchanged.

Ask once even if the invocation already includes a bump type. Use an available interactive question tool with all four options and their full version/build previews; do not merely print the options when a suitable tool is available. Prefer `request_user_input_async` when available, passing the four labels in its `options` array. Otherwise use another interactive question tool only if it is permitted in the current mode and supports all four options. Fall back to a text question only when no available, permitted tool can present all four choices; briefly explain that limitation.

Wait for the user's explicit selection before modifying versions or proceeding with the release. A preselected option, an unanswered asynchronous question, or elapsed time is not a selection. Read-only inspection may continue while waiting after the clean-working-tree check passes. When resuming the same release after a failed push, do not ask again or increment again.

## Discovery and preflight

- Read project instructions and inspect the Git root, branch, working tree, staging area, remotes, and upstream. Exclude dependencies, caches, and generated directories.
- Identify the actual release target: an app-owned `.xcodeproj` for iOS, an Android application module and its Gradle version source, `package.json` for Node, or `mygo.json` for mygo. When mobile projects coexist with a tooling package.json, do not treat the tooling package as a release target. Ask which target to release if multiple independent targets exist and context is insufficient.
- Preserve user changes. If new unrelated changes appear after the initial clean-working-tree check, report them and stop. Do not run `git add .`, automatically stash, reset, or overwrite user changes.
- Release from a named branch. Use its configured upstream remote and branch. Without an upstream, choose the same-named branch only when there is exactly one remote and the destination is clear; otherwise ask. Inspect the remote branch and tags. Resolve synchronization before proceeding if the branch is behind or diverged; do not automatically force-push, reset, or rebase user commits. Explain that existing ahead commits will also be pushed, and ask if their scope is unclear.

## Shared version rules

| Choice | Version change | Build number |
| --- | --- | --- |
| major | Increment major and reset remaining components; 2.0 → 3.0, 2.3.4 → 3.0.0 | +1 |
| minor | Increment minor and reset patch if present; 2.0 → 2.1, 2.3.4 → 2.4.0 | +1 |
| patch | Increment patch, treating a missing patch as 0; 2.0 → 2.0.1 | +1 |
| build | Keep the version unchanged | +1 |

Preserve the original two- or three-component format, except when patch adds a third component or Node requires normalization as described below. Automatically handle only versions with two or three nonnegative integer components without leading zeros, and nonnegative integer build numbers. For prereleases, dynamic expressions, noninteger build numbers, or conflicting values, locate the source configuration or ask; do not guess. Increment the build number exactly once, without resetting it for major or minor bumps.

### Optional version calculator

Use [scripts/next_version.py](scripts/next_version.py) when Python is available. It only calculates values and does not modify the project or Git. It requires Python 3.6 or newer and uses only the standard library, with no additional packages or platform-specific APIs.

On macOS or Linux:

```sh
python3 "<skill-dir>/scripts/next_version.py" minor --version 2.0 --build 41
```

On Windows, with the Python launcher installed (PowerShell or Command Prompt):

```powershell
py -3 "<skill-dir>/scripts/next_version.py" minor --version 2.0 --build 41
```

If the launcher is unavailable but Python 3 is on PATH, use `python` instead. Invoke the interpreter explicitly; do not rely on the shebang or `.py` file association on Windows. Both commands produce:

```json
{"version": "2.1", "buildVersion": 42, "tag": "v2.1-42", "commit": "release: v2.1-42"}
```

`<skill-dir>` is the directory containing this SKILL.md. Add `--node` for Node projects. Pass `--build 0` when the JSON buildVersion field is absent.

If Python is unavailable, continue without the helper. Calculate values directly using the shared rules and platform-specific constraints in this skill, then independently verify the version components, build increment, tag, and commit message before editing. Reject the same unsupported inputs as the helper. Python is optional for this workflow; do not install a runtime solely to run the calculator.

## Platform version sources

| Platform | Version | Build number |
| --- | --- | --- |
| iOS | MARKETING_VERSION / CFBundleShortVersionString | CURRENT_PROJECT_VERSION / CFBundleVersion |
| Android | versionName | versionCode |
| Node | Top-level version in package.json | Top-level integer buildVersion |
| mygo | Top-level version in mygo.json | Top-level integer buildVersion |

- **iOS**: Inspect the actual definitions in the project, xcconfig, and Info.plist. Preserve variable references and edit their source values. Synchronize configurations and extensions that must match within the same app. Exclude dependencies and generated content such as Pods, Carthage, and DerivedData. Establish the release scope when targets or configurations disagree; inspect `xcodebuild -showBuildSettings` when needed. Write build numbers in the string or build-setting format required by the platform; do not add JSON fields.
- **Android**: Trace versionName/versionCode through the app module's build.gradle / build.gradle.kts, gradle.properties, version catalogs, or custom scripts. Preserve references and Gradle syntax; do not replace derived expressions. Synchronize the selected release variants. For derived versionCode values such as flavor or ABI offsets, verify that incrementing the base by one produces correct effective values within platform limits. Ask if a unique version source cannot be established.
- **Node / mygo**: Treat a missing buildVersion as 0 and write the number 1 for the first release. An existing value must be a nonnegative integer, not a boolean or string, and remain a JSON number after incrementing. Preserve other fields and formatting. Do not confuse it with or overwrite a custom builder_version field. Ask for an initial version if version is missing.
- **Node specifics**: package.json requires a three-component version. For major/minor/patch, append .0 to a legacy two-component version before calculating. Since build must preserve the original version, stop on a legacy two-component version and ask whether format normalization is allowed. Do not silently change it. For package-lock.json / npm-shrinkwrap.json, synchronize the root package version and packages[""] version when present. Do not modify dependency versions or add buildVersion to lockfiles. Update other lockfiles only where they actually record this package's version. Avoid dependency upgrades, lifecycle scripts, or automatic commits and tags from npm version.

## Edit and validate

Show the target, old and new versions, old and new build numbers, intended tag, and push destination, then perform the selected bump without another routine confirmation.

Inspect the complete diff, parse JSON or platform configuration, confirm consistent effective values for the selected target, and verify that the build number increased by exactly one. Run relevant checks required by the project. An ordinary version change does not require a full build. Fix failed checks or report the blocker; do not continue the release while checks fail.

## Commit, tag, and push

Let `V` be the version written to the project and `B` the incremented build number. Use exactly:

- Commit message: `release: v<V>-<B>`
- Tag: `v<V>-<B>`

For example, `release: v2.1-42` and `v2.1-42`. A Node commit example is `release: v2.1.0-42`.

1. Before editing, verify that the intended tag does not exist locally or remotely. Stop on a conflict; do not overwrite or delete tags or increment again to bypass it.
2. Stage only reviewed release files or precise hunks, inspect the staged diff, and create a commit with the exact message above. Do not use another commit skill to rewrite the message.
3. Create an annotated tag on that release commit, using the same release message as its annotation. Verify that the tag points to the commit and that the commit contains the intended versions.
4. Prefer an atomic push of the current branch to the explicit destination branch and this single tag: `git push --atomic <remote> HEAD:refs/heads/<branch> refs/tags/<tag>:refs/tags/<tag>`. Quote arguments appropriately when executing. Do not use `--tags`, `--force`, or `--mirror`.
5. Only if the server explicitly does not support atomic pushes, inspect remote state and then push the branch followed by the single tag. Do not interpret other rejections or network errors as lack of atomic support or blindly switch strategies.
6. Verify remote refs: the branch commit and the tag's peeled commit must both equal the release commit. Report the version change, build number, commit, tag, remote/branch, and push result.

## Interruptions and retries

Preserve completed work on failure and report which steps finished and which remain. Before retrying, inspect version files, HEAD, the commit message, the local tag, and remote refs. Do not repeat completed version edits, commits, or tags, and do not increment the build number again. Stop and explain conflicts involving non-fast-forward updates, an unexpected tag target, or unexpected commit contents; do not force-push. If the branch push succeeded but the tag push failed, retry only the missing tag push. Do not report a successful release when only the local commit or tag exists.
