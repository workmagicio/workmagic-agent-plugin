#!/usr/bin/env python3
"""构建各平台的插件产物，配置文件位于产物根目录。

ZIP（本地测试 / 门户上传）：

    python3 tools/build_zip.py chatgpt   # → dist/workmagic-chatgpt.zip (OpenAI plugin portal)
    python3 tools/build_zip.py claude    # → dist/workmagic-claude.zip  (Customize > Plugins > Upload, for testing)
    python3 tools/build_zip.py codex     # → dist/workmagic-codex.zip (解压后添加本地 marketplace)

目录（给 Claude plugin directory 提交用，自包含、全合规文件类型）：

    python3 tools/build_zip.py claude --dir   # → plugins/claude/ (提交时 plugin path 填 plugins/claude)

Each archive/dir holds only what that platform reads, at its root, so no
platform sees another platform's manifest, and dev-only files (tools/, .codex/)
stay out of what the directory scans.
"""

import pathlib
import shutil
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PLUGINS = ROOT / "plugins"

COMMON = ["README.md", "LICENSE", "skills", "assets"]
TARGETS = {
    "chatgpt": ["plugin.json", "mcp.json"],
    "claude": [".claude-plugin/plugin.json", ".mcp.json"],
    "codex": [
        ".agents/plugins/marketplace.json",
        ".codex-plugin/plugin.json",
        ".mcp.json",
    ],
}
JUNK = {".DS_Store", "Thumbs.db", "desktop.ini"}


def files(rel):
    path = ROOT / rel
    if not path.exists():
        raise FileNotFoundError(f"缺少打包源文件或目录: {rel}")
    if path.is_file():
        yield path
    elif path.is_dir():
        for f in sorted(path.rglob("*")):
            if f.is_file() and f.name not in JUNK and "__MACOSX" not in f.parts:
                yield f


def build_zip(target, sources):
    DIST.mkdir(exist_ok=True)
    out = DIST / f"workmagic-{target}.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sources:
            z.write(f, f.relative_to(ROOT).as_posix())
            count += 1
    print(f"{out.relative_to(ROOT)}: {count} files")
    return 0


# Directory-submission file-type allowlist. Intersection of the portal
# reviewer's rule (PNG/JPEG/GIF/WebP/ICO) and the published checklist
# (text/SVG/PNG/JPEG/GIF/WebP) — the two disagree on SVG vs ICO, so we ship
# only what BOTH accept: text-family + PNG/JPEG/GIF/WebP + fonts. No SVG, ICO,
# or scripts. Files without an extension (LICENSE) are text and allowed.
ALLOWED_EXT = {
    ".md", ".txt", ".json", ".yaml", ".yml",
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".woff", ".woff2", ".ttf", ".otf",
}


def build_dir(target, sources):
    out = PLUGINS / target
    if out.exists():
        shutil.rmtree(out)
    count = 0
    skipped = []
    for f in sources:
        if f.suffix and f.suffix.lower() not in ALLOWED_EXT:
            skipped.append(f.relative_to(ROOT).as_posix())
            continue
        dest = out / f.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        count += 1
    print(f"{out.relative_to(ROOT)}/: {count} files")
    if skipped:
        print(f"  skipped {len(skipped)} non-allowed: {', '.join(skipped)}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    as_dir = "--dir" in args
    args = [a for a in args if a != "--dir"]
    if len(args) != 1 or args[0] not in TARGETS:
        print(__doc__)
        return 2
    target = args[0]
    # 先收集并检查源文件，避免缺少配置时生成不完整的产物。
    sources = [f for rel in TARGETS[target] + COMMON for f in files(rel)]
    return build_dir(target, sources) if as_dir else build_zip(target, sources)


if __name__ == "__main__":
    sys.exit(main())
