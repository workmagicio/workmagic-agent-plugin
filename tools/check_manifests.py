#!/usr/bin/env python3
"""Check that every platform manifest in this repo agrees with the others.

The plugin ships one set of skills and one MCP server, described by a manifest per
platform. This script fails if their name, version or MCP URL drift apart, or if a
skill is missing its frontmatter.

Usage:
    python3 tools/check_manifests.py
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = "workmagic"
MCP_URL = "https://mcp.workmagic.io/mcp"

MANIFESTS = {
    ".claude-plugin/plugin.json": "Claude",
    ".claude-plugin/marketplace.json": "Claude marketplace",
    ".codex-plugin/plugin.json": "Codex",
    ".cursor-plugin/plugin.json": "Cursor",
    "plugin.json": "Agent Plugins (ChatGPT, Copilot, …)",
    "gemini-extension.json": "Gemini CLI",
}
MCP_FILES = [".mcp.json", "mcp.json"]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    errors, warnings, versions = [], [], {}

    for rel, label in MANIFESTS.items():
        try:
            data = load(rel)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{rel}: can't parse ({e})")
            continue
        if rel.endswith("marketplace.json"):
            entry = next((p for p in data.get("plugins", []) if p.get("name") == NAME), None)
            if not entry:
                errors.append(f"{rel}: no plugin entry named {NAME}")
                continue
            versions[label] = entry.get("version")
        else:
            if data.get("name") != NAME:
                errors.append(f"{rel}: name is {data.get('name')!r}, expected {NAME!r}")
            versions[label] = data.get("version")

    if len(set(versions.values())) > 1:
        errors.append("versions differ: " + ", ".join(f"{k}={v}" for k, v in versions.items()))

    urls = []
    for rel in MCP_FILES:
        urls += [s.get("url") for s in load(rel)["mcpServers"].values()]
    urls += [s.get("httpUrl") for s in load("gemini-extension.json")["mcpServers"].values()]
    if set(urls) != {MCP_URL}:
        errors.append(f"MCP URLs differ from {MCP_URL}: {urls}")

    logo = load("plugin.json")["extensions"]["com.openai"]["interface"].get("logo")
    if logo and not (ROOT / logo).exists():
        warnings.append(f"plugin.json points at {logo}, which doesn't exist yet (needed for ChatGPT)")

    for skill in sorted((ROOT / "skills").iterdir()):
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        front = m.group(1) if m else ""
        name = re.search(r"^name:\s*(.+)$", front, re.M)
        desc = re.search(r"^description:\s*(.+)$", front, re.M)
        if not (name and name.group(1).strip() == skill.name and desc):
            errors.append(f"skills/{skill.name}/SKILL.md: needs name: {skill.name} and a description")

    for w in warnings:
        print("warning:", w)
    if errors:
        print("\n".join(f"error: {e}" for e in errors))
        return 1
    print(f"OK — {len(MANIFESTS)} manifests agree on {NAME} {next(iter(versions.values()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
