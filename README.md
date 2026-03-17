# mint

Create new skills or protocols, improve existing ones, and measure performance.

## What this is

A fork of [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) (`plugins/skill-creator/`) that produces **platform-agnostic skills and protocols** usable by any agent that reads `SKILL.md` files, not just Claude Code.

The tool itself still runs on Claude Code (that's fine — it's the authoring environment). Only the **generated output** (SKILL.md files, descriptions, reference content) has been neutralized to remove platform-specific assumptions.

## Installation

### Prerequisites

- Python 3.8+
- [`claude` CLI](https://docs.anthropic.com/en/docs/claude-code) — required by `run_eval.py` and `run_loop.py`

> **Note:** Only tested on Debian. Other Linux distributions, macOS, and Windows are untested.

### Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic pyyaml
```

| Package | Required by | Purpose |
|---------|------------|---------|
| `anthropic` | `improve_description.py`, `run_loop.py` | API calls for description optimization |
| `pyyaml` | `quick_validate.py`, `package_skill.py` | SKILL.md frontmatter parsing and validation |

All other scripts use Python standard library only.

## What changed

Key fork-specific changes:

- **`skills/mint/SKILL.md`** — renamed to `mint`, broadened to cover protocols as well as skills, and kept platform-agnostic in its generated output guidance.
- **`skills/mint/scripts/quick_validate.py`** — now accepts both skills and protocols. Skills require `name` and `description`; protocols additionally require `requires`, `accepts`, `produces`, `may_produce`, and `trigger`.
- **`skills/mint/scripts/improve_description.py`** — prompt template neutralized. Fork note remains at module level to reduce merge-conflict surface with upstream.

The upstream source subtree remains `plugins/skill-creator/`; only the fork identity and validator contract changed locally.

## Upstream source

```
Repository: https://github.com/anthropics/claude-plugins-official
Subtree:    plugins/skill-creator/
License:    Apache 2.0
```

## Syncing upstream changes

Requires [`git-filter-repo`](https://github.com/newren/git-filter-repo). To pull in upstream updates:

```bash
UPSTREAM_DIR="$(mktemp -d)"

# Fresh extraction of upstream subtree
git clone https://github.com/anthropics/claude-plugins-official.git "$UPSTREAM_DIR"
git -C "$UPSTREAM_DIR" filter-repo --subdirectory-filter plugins/skill-creator/

# Merge into this repo (run from your mint checkout)
git remote add upstream-update "$UPSTREAM_DIR"
git fetch upstream-update && git merge upstream-update/main
git remote remove upstream-update
rm -rf "$UPSTREAM_DIR"
```

Resolve conflicts in `SKILL.md`, `quick_validate.py`, or `improve_description.py` by keeping the fork's `mint` naming, protocol support, and platform-agnostic wording.

## License

Apache 2.0 — see [LICENSE](LICENSE).
