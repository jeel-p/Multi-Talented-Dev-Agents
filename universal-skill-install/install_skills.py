#!/usr/bin/env python3
"""
Copy or symlink skill folders (each containing SKILL.md) into tool-specific
global or project directories. Cross-platform (Windows + Unix).

Usage:
  python install_skills.py
  python install_skills.py --source ./my-skills --tools all --scope global
  python install_skills.py -s ./my-skills -t cursor,claude --scope project
  python install_skills.py --list-tools
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def home() -> Path:
    return Path(os.path.expanduser("~")).resolve()


def codex_home() -> Path:
    raw = os.environ.get("CODEX_HOME", "").strip()
    if raw:
        return Path(os.path.expandvars(raw)).expanduser().resolve()
    return home() / ".codex"


def expand_template(tpl: str) -> Path:
    tpl = tpl.replace("{HOME}", str(home()))
    tpl = tpl.replace("{CODEX_HOME}", str(codex_home()))
    return Path(os.path.expandvars(tpl)).expanduser().resolve()


def load_targets(config_path: Path) -> dict:
    with config_path.open(encoding="utf-8") as f:
        data = json.load(f)
    if "tools" not in data:
        raise SystemExit(f"Invalid config: missing 'tools' in {config_path}")
    return data


def discover_skills(source: Path, *, shallow: bool = False) -> list[Path]:
    if not source.is_dir():
        raise SystemExit(f"Source is not a directory: {source}")

    # Case 1: source itself is a single skill folder.
    if (source / "SKILL.md").is_file():
        return [source]

    # Case 2: direct children are skill folders.
    direct: list[Path] = []
    for child in sorted(source.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            direct.append(child)
    if direct:
        return direct

    if shallow:
        return []

    # Case 3: nested layout (common in larger repos). Discover recursively.
    nested = sorted({p.parent.resolve() for p in source.glob("**/SKILL.md") if p.is_file()})
    return nested


def resolve_auto_source(*, script_dir: Path, cwd: Path) -> Path | None:
    """Pick a skill folder without --source: common paths under cwd, then repo root."""
    bases: list[Path] = []
    for b in (cwd.resolve(), script_dir.parent.resolve()):
        if b not in bases:
            bases.append(b)
    rels = ("skills", "demo", ".agents/skills", ".")
    for base in bases:
        for rel in rels:
            cand = (base / rel).resolve()
            if cand.is_dir() and discover_skills(cand, shallow=True):
                return cand
    return None


def resolve_tools(requested: str, data: dict) -> list[str]:
    requested = requested.strip().lower()
    aliases = data.get("tool_aliases") or {}
    if requested == "all":
        return list(aliases.get("all", list((data.get("tools") or {}).keys())))
    ids = [t.strip().lower() for t in requested.split(",") if t.strip()]
    known = set((data.get("tools") or {}).keys())
    bad = [t for t in ids if t not in known]
    if bad:
        raise SystemExit(f"Unknown tool(s): {', '.join(bad)}. Use --list-tools.")
    return ids


def install_one_skill(
    skill_dir: Path,
    dest_root: Path,
    *,
    use_symlink: bool,
    force: bool,
    dry_run: bool,
) -> None:
    name = skill_dir.name
    target = dest_root / name
    replacing = target.exists() or target.is_symlink()
    if replacing:
        if not force:
            print(f"  skip (exists): {target}")
            return
        if dry_run:
            print(f"  would replace: {target}")
        elif target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    if dry_run and not replacing:
        print(f"  would install: {skill_dir.name} -> {target}")
        return
    if dry_run:
        return
    dest_root.mkdir(parents=True, exist_ok=True)
    if use_symlink:
        try:
            try:
                rel = os.path.relpath(skill_dir, dest_root)
            except ValueError:
                rel = None
            if rel and not (rel.startswith("..\\") or rel.startswith("../")):
                target.symlink_to(rel, target_is_directory=True)
            else:
                target.symlink_to(skill_dir.resolve(), target_is_directory=True)
        except OSError:
            shutil.copytree(skill_dir, target, dirs_exist_ok=False)
    else:
        shutil.copytree(skill_dir, target, dirs_exist_ok=False)


def run(
    *,
    source: Path,
    config_path: Path,
    tools: list[str],
    scope: str,
    use_symlink: bool,
    force: bool,
    dry_run: bool,
    project_root: Path,
) -> None:
    data = load_targets(config_path)
    tool_map = data["tools"]
    skills = discover_skills(source, shallow=False)
    if not skills:
        raise SystemExit(
            "\n".join(
                [
                    f"No SKILL.md files found under {source}",
                    "",
                    "Expected one of these layouts:",
                    f"  1) {source / 'SKILL.md'}",
                    f"  2) {source / '<skill-name>' / 'SKILL.md'}",
                    f"  3) nested folders anywhere under {source} containing SKILL.md (use --source for deep trees)",
                    "",
                    "Tip: run --dry-run first once SKILL.md files are present.",
                ]
            )
        )

    print(f"Found {len(skills)} skill(s) in {source}")
    for tool_id in tools:
        entry = tool_map.get(tool_id)
        if not entry:
            print(f"Skipping unknown tool id: {tool_id}")
            continue
        label = entry.get("label", tool_id)
        keys = "global" if scope == "global" else "project"
        rel_list = entry.get(keys) or []
        if not rel_list:
            print(f"[{label}] no {keys} paths configured; skip")
            continue
        for tpl in rel_list:
            dest_root = expand_template(tpl) if scope == "global" else (project_root / tpl).resolve()
            print(f"\n[{label}] -> {dest_root}")
            for s in skills:
                install_one_skill(s, dest_root, use_symlink=use_symlink, force=force, dry_run=dry_run)

    if dry_run:
        print("\nDry run only; no files were written.")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    here = Path(__file__).resolve().parent
    default_config = here / "targets.json"

    p = argparse.ArgumentParser(description="Install SKILL.md bundles into multiple AI tool directories.")
    p.add_argument(
        "-s",
        "--source",
        type=Path,
        help="Skill pack directory (omit to auto-detect: ./skills, ./demo, ./.agents/skills, or . under cwd and repo root).",
    )
    p.add_argument(
        "-t",
        "--tools",
        default="all",
        help="Comma-separated tool ids, or 'all'. Example: cursor,claude,opencode",
    )
    p.add_argument(
        "--scope",
        choices=("global", "project"),
        default="global",
        help="global = user home paths; project = paths under --project-root",
    )
    p.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Root for project scope (default: current directory).",
    )
    p.add_argument("--config", type=Path, default=default_config, help="Path to targets.json")
    p.add_argument("--dry-run", action="store_true", help="Print actions without writing")
    p.add_argument("--force", action="store_true", help="Overwrite existing skill folders")
    p.add_argument(
        "--link",
        action="store_true",
        help="Try symlink per skill (falls back to copy if OS denies symlink)",
    )
    p.add_argument("--list-tools", action="store_true", help="List configured tools and exit")

    args = p.parse_args(argv)

    if args.list_tools:
        data = load_targets(args.config)
        print("Configured tools:\n")
        for tid, meta in sorted((data.get("tools") or {}).items()):
            label = meta.get("label", tid)
            print(f"  {tid:14}  {label}")
        print("\nUse: --tools all  or  --tools cursor,claude,...")
        return 0

    cwd = Path.cwd()
    if args.source:
        source = args.source.resolve()
    else:
        picked = resolve_auto_source(script_dir=here, cwd=cwd)
        if not picked:
            raise SystemExit(
                "\n".join(
                    [
                        "No skill folder found (and --source not set).",
                        "",
                        "Put skills in one of these (each skill is a folder containing SKILL.md):",
                        f"  {cwd / 'skills'}",
                        f"  {cwd / 'demo'}",
                        f"  {cwd / '.agents' / 'skills'}",
                        f"  {cwd}  (if this folder is one skill or contains skill subfolders)",
                        "",
                        f"Also checked next to this script: {here.parent / 'skills'}, demo, …",
                        "",
                        "Or pass an explicit path:",
                        "  python install_skills.py --source path/to/your-skills",
                    ]
                )
            )
        source = picked
        print(f"Using skill source (auto): {source}\n")

    data = load_targets(args.config)
    tools = resolve_tools(args.tools, data)
    run(
        source=source,
        config_path=args.config.resolve(),
        tools=tools,
        scope=args.scope,
        use_symlink=args.link,
        force=args.force,
        dry_run=args.dry_run,
        project_root=args.project_root.resolve(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
