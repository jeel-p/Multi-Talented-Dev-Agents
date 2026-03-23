# Universal skill install

Install the same skill folders (each containing `SKILL.md`) into every supported tool’s skills directory in one run. Paths are driven by `targets.json` so you can add tools or fix locations when vendors change layouts.

## Requirements

- **Python 3.8+** on `PATH` as `python` or `python3`.

## Easiest way (no flags)

1. Put your skills where the script can find them (see **Auto-detect** below), usually a `skills/` folder next to your project or repo root.
2. Run:

```bash
python install_skills.py
```

Defaults: **all tools**, **global** (user home) install paths. Add `--dry-run` first if you want a preview only.

**From the parent repo** (this `agency-agents` project):

```bash
python universal-skill-install/install_skills.py
```

**Windows (PowerShell), from this folder:**

```powershell
.\install-skills.ps1
```

### Auto-detect (when you omit `--source`)

The script looks for the first folder that already contains skills, in this order:

1. Under your **current directory**: `skills/`, then `demo/`, then `.agents/skills/`, then `.` (only if that folder is one skill or has skill subfolders—not a deep repo-wide scan).
2. Then the same list under the **parent of this folder** (so you can `cd universal-skill-install` and still pick up `../demo` or `../skills`).

If nothing matches, you get a short message telling you to create `skills/` or pass `--source`.

## Layout

Your skill pack can be in any of these layouts:

```text
# A) source itself is one skill
my-skill/
  SKILL.md

# B) source contains multiple skill folders
my-skills/
  my-skill-one/
    SKILL.md
    scripts/          # optional
  another-skill/
    SKILL.md

# C) nested repo layout (only when you pass --source; full tree scan)
my-repo/
  skills/
    team/
      deploy-skill/
        SKILL.md
```

## More commands (when you need control)

```bash
# List tool ids
python install_skills.py --list-tools

# Explicit pack path
python install_skills.py --source /path/to/my-skills

# Install only into the current project (creates .cursor/skills, .claude/skills, …)
python install_skills.py --scope project

# Subset of tools
python install_skills.py -t cursor,claude,opencode

# Preview
python install_skills.py --dry-run
```

**Windows (PowerShell):**

```powershell
.\install-skills.ps1 -ListTools
.\install-skills.ps1 -Source D:\path\to\my-skills
```

**Unix:**

```bash
chmod +x install-skills.sh
./install-skills.sh
./install-skills.sh --source ./my-skills
```

### Options

| Flag | Meaning |
|------|--------|
| `--source` / `-s` | Skill pack folder (optional if auto-detect finds one) |
| `--tools` / `-t` | `all` (default) or comma-separated ids from `--list-tools` |
| `--scope` | `global` (default, home) or `project` (under `--project-root`) |
| `--project-root` | Base path for project scope (default: cwd) |
| `--config` | Alternate `targets.json` |
| `--dry-run` | Print planned actions only |
| `--force` | Replace existing skill folders |
| `--link` | Prefer symlinks (falls back to copy if the OS blocks links) |

## Configuring destinations

Edit `targets.json`:

- **`global`**: templates use `{HOME}` and `{CODEX_HOME}` (defaults to `~/.codex` if `CODEX_HOME` is unset).
- **`project`**: paths are relative to `--project-root`.

To add a new tool, copy an existing block under `tools` and set `global` / `project` arrays.

## Defaults (current tools)

| Id | Typical global path |
|----|---------------------|
| `cursor` | `~/.cursor/skills` |
| `claude` | `~/.claude/skills` |
| `codex` | `$CODEX_HOME/skills` or `~/.codex/skills` |
| `opencode` | `~/.config/opencode/skills` |
| `agents` | `~/.agents/skills` |
| `antigravity` | `~/.gemini/antigravity/skills` |
| `openclaw` | `~/.openclaw/skills` |

Vendor docs change; verify paths after major tool upgrades.

## License

Same as the parent repository (MIT unless stated otherwise).
