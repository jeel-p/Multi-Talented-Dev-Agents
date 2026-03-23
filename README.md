# Multi-Talented Dev Agents

> Multi-talented AI agent prompts for engineering, product, and design work, with clear personalities, practical workflows, and concrete deliverables in every Markdown file.

[License: MIT](https://opensource.org/licenses/MIT)

---

## What this is

This repository contains **25 agents** in two categories:

- `**engineering/`** — Development, infrastructure, security, data, and related technical roles  
- `**design/`** — UX, UI, brand, research, and visual craft

Each agent is a standalone `.md` file with YAML frontmatter (`name`, `description`, `color`, …) and structured sections (identity, mission, deliverables, workflows).

---

## Quick start

### Option 1: Claude Code

Copy agent files into your Claude Code agents directory (paths vary by OS):

```bash
cp engineering/*.md design/*.md ~/.claude/agents/
```

Or use the installer (see below).

### Option 2: Use as reference

Open any file under `engineering/` or `design/`, copy the prompt, or adapt the structure for your own agents.

### Option 3: Other tools (Cursor, Aider, Windsurf, Gemini CLI, OpenCode, …)

Generate tool-specific outputs from this repo’s agent Markdown, then install:

```bash
./scripts/convert.sh
./scripts/install.sh
```

See [Multi-tool integrations](#multi-tool-integrations) for details.

### Option 4: Install your own SKILL.md packs (one command)

If you maintain **skills** (each skill is a folder with `SKILL.md`), copy them into **Cursor, Claude Code, Codex, OpenCode, Antigravity, OpenClaw**, and `.agents` in one step—no `convert.sh` needed.

**Simplest:** from the repo root, put skills under `skills/`, `demo/`, or `.agents/skills/` (see [universal-skill-install/README.md](universal-skill-install/README.md)), then run:

```bash
python universal-skill-install/install_skills.py
```

That installs to **all** configured tools in your user (global) folders. Preview first with `--dry-run`.

**Windows (PowerShell):** `.\universal-skill-install\install-skills.ps1`

**Custom folder:** `python universal-skill-install/install_skills.py --source path/to/your-skills`

More flags and paths: [universal-skill-install/README.md](universal-skill-install/README.md).

---

## Agent roster

### Engineering


| Agent                             | File                                                                                     |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| Frontend Developer                | [frontend-developer.md](engineering/frontend-developer.md)                               |
| Backend Architect                 | [backend-architect.md](engineering/backend-architect.md)                                 |
| Mobile App Builder                | [mobile-app-builder.md](engineering/mobile-app-builder.md)                               |
| AI Engineer                       | [ai-engineer.md](engineering/ai-engineer.md)                                             |
| DevOps Automator                  | [devops-automator.md](engineering/devops-automator.md)                                   |
| Senior Developer                  | [senior-developer.md](engineering/senior-developer.md)                                   |
| Security Engineer                 | [security-engineer.md](engineering/security-engineer.md)                                 |
| Autonomous Optimization Architect | [autonomous-optimization-architect.md](engineering/autonomous-optimization-architect.md) |
| Incident Response Commander       | [incident-response-commander.md](engineering/incident-response-commander.md)             |
| Technical Writer                  | [technical-writer.md](engineering/technical-writer.md)                                   |
| Threat Detection Engineer         | [threat-detection-engineer.md](engineering/threat-detection-engineer.md)                 |
| Code Reviewer                     | [code-reviewer.md](engineering/code-reviewer.md)                                         |
| Database Optimizer                | [database-optimizer.md](engineering/database-optimizer.md)                               |
| Git Workflow Master               | [git-workflow-master.md](engineering/git-workflow-master.md)                             |
| Software Architect                | [software-architect.md](engineering/software-architect.md)                               |
| AI Data Remediation Engineer      | [ai-data-remediation-engineer.md](engineering/ai-data-remediation-engineer.md)           |
| Data Engineer                     | [data-engineer.md](engineering/data-engineer.md)                                         |


### Design


| Agent                        | File                                                                      |
| ---------------------------- | ------------------------------------------------------------------------- |
| UI Designer                  | [ui-designer.md](design/ui-designer.md)                                   |
| UX Researcher                | [ux-researcher.md](design/ux-researcher.md)                               |
| UX Architect                 | [ux-architect.md](design/ux-architect.md)                                 |
| Brand Guardian               | [brand-guardian.md](design/brand-guardian.md)                             |
| Visual Storyteller           | [visual-storyteller.md](design/visual-storyteller.md)                     |
| Whimsy Injector              | [whimsy-injector.md](design/whimsy-injector.md)                           |
| Image Prompt Engineer        | [image-prompt-engineer.md](design/image-prompt-engineer.md)               |
| Inclusive Visuals Specialist | [inclusive-visuals-specialist.md](design/inclusive-visuals-specialist.md) |


---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or improve agents.

---

## Agent design philosophy

1. **Clear voice** — Not generic templates; each agent has a distinct tone.
2. **Concrete deliverables** — Code, checklists, frameworks—not vague advice.
3. **Success metrics** — What “good” looks like for that role.
4. **Repeatable workflows** — Steps you can follow in a real session.

---

## Multi-tool integrations

The same agents can be converted for Claude Code, GitHub Copilot, Antigravity, Gemini CLI, OpenCode, Cursor, Aider, Windsurf, OpenClaw, and Qwen Code. Generated files live under `integrations/`.

### Supported tools

- **[Claude Code](https://claude.ai/code)** — native `.md` agents → `~/.claude/agents/`
- **[GitHub Copilot](https://github.com/copilot)** — native `.md` → `~/.github/agents/` and `~/.copilot/agents/`
- **[Antigravity](https://github.com/google-gemini/antigravity)** — `SKILL.md` per agent → `~/.gemini/antigravity/skills/`
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — extension + skills → `~/.gemini/extensions/agency-agents/`
- **[OpenCode](https://opencode.ai)** — `.md` in `.opencode/agent/`
- **[Cursor](https://cursor.sh)** — **Skills** (folders with `SKILL.md`): project `.agents/skills/`, `.cursor/skills/`; user `~/.cursor/skills/`. **Compatibility:** Cursor also loads skills from `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`. **From this repo’s converter:** `.mdc` rules → `.cursor/rules/` (separate from skills; see `convert.sh` / `integrations/cursor/`).
- **[Aider](https://aider.chat)** — single `CONVENTIONS.md`
- **[Windsurf](https://codeium.com/windsurf)** — `.windsurfrules`
- **[OpenClaw](https://github.com/openclaw/openclaw)** — `SOUL.md` workspaces per agent
- **[Qwen Code](https://github.com/QwenLM/qwen-code)** — SubAgent `.md` files

### Quick install

**Note:** This repo keeps **source agents** under `engineering/` and `design/` only. Converted outputs under `integrations/antigravity/`, `integrations/gemini-cli/`, `integrations/cursor/rules/`, `integrations/opencode/agents/`, `integrations/openclaw/`*, `integrations/qwen/agents/`, plus `integrations/aider/CONVENTIONS.md` and `integrations/windsurf/.windsurfrules`, are **created by** `./scripts/convert.sh` and are not versioned here—you must run the script before those installers will work.

**Step 1 — Generate integration files**

```bash
./scripts/convert.sh
# Optional: ./scripts/convert.sh --parallel
```

**Step 2 — Install**

```bash
./scripts/install.sh
# Or: ./scripts/install.sh --tool cursor
# Non-interactive: ./scripts/install.sh --no-interactive --tool all
```

More detail: [integrations/README.md](integrations/README.md).

### Universal skill install (SKILL.md packs)

This repo includes **[universal-skill-install/](universal-skill-install/)** for distributing **skills** (not the `engineering/` / `design/` agents unless you turn them into skill folders). It reads [universal-skill-install/targets.json](universal-skill-install/targets.json) and copies each skill folder into the right place per tool.


| Step                                                             | Command                                                         |
| ---------------------------------------------------------------- | --------------------------------------------------------------- |
| Install (auto-finds `./skills`, `./demo`, or `./.agents/skills`) | `python universal-skill-install/install_skills.py`              |
| See what would happen                                            | add `--dry-run`                                                 |
| Only some tools                                                  | add `-t cursor,claude`                                          |
| Install into the current project tree                            | add `--scope project`                                           |
| List tool ids                                                    | `python universal-skill-install/install_skills.py --list-tools` |
| Your pack lives somewhere else                                   | `--source /path/to/pack`                                        |


Edit `targets.json` if a tool changes where it expects skills. Full reference: [universal-skill-install/README.md](universal-skill-install/README.md).

### Tool-specific READMEs

- [claude-code](integrations/claude-code/README.md) · [github-copilot](integrations/github-copilot/README.md) · [antigravity](integrations/antigravity/README.md) · [gemini-cli](integrations/gemini-cli/README.md) · [opencode](integrations/opencode/README.md) · [cursor](integrations/cursor/README.md) · [aider](integrations/aider/README.md) · [windsurf](integrations/windsurf/README.md) · [openclaw](integrations/openclaw/README.md)

### Regenerating after edits

```bash
./scripts/convert.sh
./scripts/convert.sh --tool cursor   # one tool only
```

---

## License

MIT — use freely for commercial or personal projects. Attribution is appreciated but not required.

---

