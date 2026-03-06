# skill-creator (platform-agnostic fork)

Create new skills, improve existing skills, and measure skill performance.

## What this is

A fork of [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) (`plugins/skill-creator/`) that produces **platform-agnostic skills** — usable by any agent that reads SKILL.md files, not just Claude Code.

The tool itself still runs on Claude Code (that's fine — it's the authoring environment). Only the **generated output** (SKILL.md files, descriptions, reference content) has been neutralized to remove platform-specific assumptions.

## Installation

### Prerequisites

- Python 3.8+
- [`claude` CLI](https://docs.anthropic.com/en/docs/claude-code) — required by `run_eval.py` and `run_loop.py`
- [`git-filter-repo`](https://github.com/newren/git-filter-repo) — only needed for syncing upstream changes

### Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic pyyaml
```

| Package | Required by | Purpose |
|---------|------------|---------|
| `anthropic` | `improve_description.py`, `run_loop.py` | API calls for description optimization |
| `pyyaml` | `quick_validate.py`, `package_skill.py` | SKILL.md frontmatter parsing |

All other scripts use Python standard library only.

## What changed

Two files modified, everything else untouched:

- **`skills/skill-creator/SKILL.md`** — 18 text replacements + 1 new "Platform-Agnostic Output" section. All output-shaping and contextual references neutralized: "Claude" → "the agent" / "AI" / "an LLM", "MCPs" → "tools", "Claude's available_skills list" → "the agent's skill list", "Claude.ai-specific instructions" → "Limited-environment instructions". Only the `claude` CLI binary name and the Platform-Agnostic Output instructional section retain the word "Claude".

- **`skills/skill-creator/scripts/improve_description.py`** — Prompt template and docstrings neutralized. Fork note moved to module level to reduce merge-conflict surface with upstream.

Files **not** modified (confirmed no output-shaping Claude references): `run_eval.py`, `run_loop.py`, `aggregate_benchmark.py`, `generate_report.py`, `package_skill.py`, `quick_validate.py`, `utils.py`, `grader.md`, `comparator.md`, `analyzer.md`, `schemas.md`, `viewer.html`, `generate_review.py`, `eval_review.html`.

## Upstream source

```
Repository: https://github.com/anthropics/claude-plugins-official
Subtree:    plugins/skill-creator/
License:    Apache 2.0
```

## Syncing upstream changes

To pull in upstream updates:

```bash
# Fresh extraction of upstream subtree
git clone https://github.com/anthropics/claude-plugins-official.git /tmp/upstream-fresh
cd /tmp/upstream-fresh && git filter-repo --subdirectory-filter plugins/skill-creator/

# Merge into this repo
cd /path/to/skill-creator
git remote add upstream-update /tmp/upstream-fresh
git fetch upstream-update && git merge upstream-update/main
git remote remove upstream-update
rm -rf /tmp/upstream-fresh
```

Resolve any conflicts in `SKILL.md` or `improve_description.py` by keeping the platform-agnostic wording.

## License

Apache 2.0 — see [LICENSE](LICENSE).
