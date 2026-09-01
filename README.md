# Agent Skills

A collection of focused agent skills for software development workflows.

## Skills

| Skill | Description |
| --- | --- |
| [`git-commit`](git-commit) | Creates clean, reviewable commits with Conventional Commit messages. |
| [`review-code-naming`](review-code-naming) | Reviews filenames and source-code identifiers for clarity, precision, consistency, and ambiguity. |

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
