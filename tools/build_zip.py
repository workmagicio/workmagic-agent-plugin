#!/usr/bin/env python3
"""Build upload ZIPs for platforms that take an archive instead of a repo.

    python3 tools/build_zip.py chatgpt   # → dist/workmagic-chatgpt.zip (OpenAI plugin portal)
    python3 tools/build_zip.py claude    # → dist/workmagic-claude.zip  (Customize > Plugins > Upload, for testing)

Each archive holds only what that platform reads, at the archive root, so no
platform sees another platform's manifest.
"""

import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

COMMON = ["README.md", "LICENSE", "skills", "assets"]
TARGETS = {
    "chatgpt": ["plugin.json", "mcp.json"],
    "claude": [".claude-plugin/plugin.json", ".mcp.json"],
}
JUNK = {".DS_Store", "Thumbs.db", "desktop.ini"}


def files(rel):
    path = ROOT / rel
    if path.is_file():
        yield path
    elif path.is_dir():
        for f in sorted(path.rglob("*")):
            if f.is_file() and f.name not in JUNK and "__MACOSX" not in f.parts:
                yield f


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in TARGETS:
        print(__doc__)
        return 2
    target = sys.argv[1]
    DIST.mkdir(exist_ok=True)
    out = DIST / f"workmagic-{target}.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in TARGETS[target] + COMMON:
            for f in files(rel):
                z.write(f, f.relative_to(ROOT).as_posix())
                count += 1
    print(f"{out.relative_to(ROOT)}: {count} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
