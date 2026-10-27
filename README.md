# Agent Skills

A collection of focused agent skills for software development workflows.

## Skills

| Skill | Description |
| --- | --- |
| [`git-commit`](git-commit) | Creates clean, reviewable commits with Conventional Commit messages. |
| [`naming-review`](naming-review) | Reviews filenames and source-code identifiers for clarity, precision, consistency, and ambiguity. |
| [`release`](release) | Releases iOS, Android, Node, and mygo projects by bumping versions and build numbers, committing, tagging, and pushing to Git. |

The `release` skill first checks for uncommitted changes, including staged, unstaged, and untracked files and dirty submodules. If any exist, it reports them and stops before offering release choices. Once the working tree is clean, it reads the current version and build number and presents an interactive selector when a suitable tool is available, falling back to a text question otherwise. It waits for your explicit selection. For example, with version `0.1.0` and build number `41`:

- `Major v0.1.0-41 -> v1.0.0-42`
- `Minor v0.1.0-41 -> v0.2.0-42`
- `Patch v0.1.0-41 -> v0.1.1-42`
- `Build v0.1.0-41 -> v0.1.0-42`

Every choice increments the build number once (`buildVersion` in Node/mygo JSON files), including Build. The skill uses `release: v<version>-<build>` for the commit and `v<version>-<build>` for the tag. Store uploads, package publishing, deployments, and GitHub Release creation are outside its scope.

Its optional version calculator uses Python 3.6+ with no extra packages. Run it with `python3` on macOS/Linux or `py -3` on Windows (`python` also works when Python 3 is on PATH). Without Python, the agent follows the same calculation and validation rules directly. See the [release instructions](release/SKILL.md) for commands and platform details.

## Install

Install it from GitHub with the [`skills`](https://github.com/vercel-labs/skills) CLI:

```sh
# GitHub shorthand (owner/repo)
npx skills add iMuFeng/skills

# Full GitHub URL
npx skills add https://github.com/iMuFeng/skills
```

The installer will prompt you to choose the agents and installation scope.

To install it globally for Codex without prompts:

```sh
npx skills add iMuFeng/skills -g -a codex -y
```
