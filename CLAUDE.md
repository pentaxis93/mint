# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Platform-agnostic fork of Anthropic's `skill-creator` plugin. The tool runs on Claude Code as an authoring environment, but all **generated output** (SKILL.md files, descriptions, reference content) must use platform-neutral language: "the agent" not "Claude", "tools" not "MCPs", "skill directory" not ".claude/skills/".

Upstream: `plugins/skill-creator/` from [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) (Apache 2.0).

## Common Commands

```bash
# Validate a skill
python3 skills/skill-creator/scripts/quick_validate.py <skill-directory>

# Package a skill into distributable .skill (ZIP) file
python3 skills/skill-creator/scripts/package_skill.py <skill-directory>

# Run trigger evaluation (requires `claude` CLI)
python3 skills/skill-creator/scripts/run_eval.py <skill-directory>

# Full description optimization loop (up to 5 iterations, 60/40 train/test split)
python3 skills/skill-creator/scripts/run_loop.py <skill-directory>

# Aggregate benchmark results
python3 skills/skill-creator/scripts/aggregate_benchmark.py <workspace-directory>

# Generate HTML eval review viewer
python3 skills/skill-creator/scripts/eval-viewer/generate_review.py <workspace-directory>
```

No build step, test suite, or linting — this is a pure Python + Markdown project with no package manager.

## GitHub CLI

This repo is a fork. The `gh` CLI defaults to upstream, so **always pass `--repo pentaxis93/skill-creator`** for operations on this project's PRs, issues, and releases.

## Architecture

### Plugin Entry Point

`.claude-plugin/plugin.json` — registers the plugin with Claude Code. The actual skill lives entirely in `skills/skill-creator/`.

### Skill Structure

`skills/skill-creator/SKILL.md` is the core instruction file. It defines the full skill-creation workflow: capture intent → draft SKILL.md → run evals → grade → iterate → optimize description → package.

Supporting directories under `skills/skill-creator/`:
- `agents/` — Markdown instruction files for spawning specialized subagents (grader, comparator, analyzer)
- `scripts/` — Python entry points for evaluation, benchmarking, validation, and packaging
- `references/schemas.md` — JSON schemas for all data structures (evals.json, grading.json, benchmark.json, etc.)
- `eval-viewer/` — HTML viewer generation for reviewing test results (`generate_review.py`, `viewer.html`)
- `assets/eval_review.html` — Interactive eval query review UI

### Data Flow

1. **SKILL.md** (skill definition with YAML frontmatter) → 2. **evals/evals.json** (test prompts + assertions) → 3. **Subagent execution** (with-skill and without-skill runs in parallel) → 4. **grading.json** (assertions evaluated by grader agent) → 5. **benchmark.json** (aggregated statistics via `aggregate_benchmark.py`) → 6. **HTML viewer** (interactive review via `generate_review.py`) → 7. **feedback.json** (user reviews fed back into iteration)

### Workspace Layout (created during eval runs)

```
<skill-name>-workspace/
└── iteration-N/
    ├── eval-0/
    │   ├── eval_metadata.json
    │   ├── with_skill/outputs/
    │   └── without_skill/outputs/
    └── benchmark.json
```

### SKILL.md Frontmatter Spec

Required fields: `name` (kebab-case, max 64 chars), `description` (max 1024 chars, no angle brackets). Optional: `license`, `allowed-tools`, `metadata`, `compatibility` (max 500 chars).

## Fork-Specific Rules

Only two files differ from upstream:
- `skills/skill-creator/SKILL.md` — platform-neutral replacements + "Platform-Agnostic Output" section
- `skills/skill-creator/scripts/improve_description.py` — prompt template + docstring neutralization, fork note at module level

When syncing upstream changes, resolve conflicts in these two files by keeping platform-agnostic wording. All other files are unmodified from upstream.

### Key Python Dependencies

Scripts use: `anthropic` (for `improve_description.py`), `yaml`, `json`, `pathlib`, `subprocess`, `webbrowser`. The `claude` CLI binary is required by `run_eval.py` and `run_loop.py`.
