#!/usr/bin/env python3
"""Copy the customer-facing skills from the internal skills repo into the plugin folder.

The internal skills repo stays the single source of truth for skill content. This script
copies the skills listed in SKILLS into skills/ and applies the small set
of patches the directory build needs (see PATCHES). Run it whenever the source repo
changes, review the diff, bump "version" in every manifest (tools/check_manifests.py lists them),
and commit.

Usage:
    python3 tools/sync_skills.py /path/to/skills-checkout
"""

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / "skills"

# First release: skills that need no host-specific features.
# Not included yet:
#   lift-test-creation        — needs a plugin edition
#   attribution-weekly-report — depends on a host artifact tool and scheduled tasks
#   media-buyer-read, media-buyer-input-capture — only for AI Media Buyer customers
SKILLS = [
    "attribution-data-query",
    "attribution-intent-clarification",
    "attribution-model-comparison",
    "attribution-anomaly-diagnosis",
    "attribution-custom-dimension",
    "attribution-edge-routing",
    "lift-test-readout",
    "mbo-read-scenario",
    "mbo-create-scenario",
]

# (file relative to the skill folder, old text, new text). Every patch must match
# exactly once; the script stops if one doesn't, so an upstream edit can't slip
# through silently.
SKILL_READ_OLD = "read via `skills_read` if not loaded"
SKILL_READ_NEW = "load the `attribution-data-query` skill from this plugin if it isn't loaded"

PATCHES = [
    # In a plugin every skill is local, so cross-skill reads point at the bundled
    # skill instead of the server-side skills_read tool.
    ("attribution-data-query/references/sales-platform-scope.md", SKILL_READ_OLD, SKILL_READ_NEW),
    ("attribution-data-query/references/attribution-model.md", SKILL_READ_OLD, SKILL_READ_NEW),
    ("attribution-intent-clarification/SKILL.md", SKILL_READ_OLD, SKILL_READ_NEW),
    ("attribution-model-comparison/SKILL.md", SKILL_READ_OLD, SKILL_READ_NEW),
    ("attribution-anomaly-diagnosis/SKILL.md", SKILL_READ_OLD, SKILL_READ_NEW),
    # Routes to skills that are not in this release.
    (
        "attribution-data-query/SKILL.md",
        "If the ask is a **recurring business review** (\"weekly overview\", \"monthly review\"), "
        "route to `attribution-weekly-report` — it owns the board spec for each cadence |",
        "For a **recurring business review** (\"weekly overview\", \"monthly review\"), build the "
        "same live view with the prior period alongside for comparison |",
    ),
    (
        "attribution-data-query/SKILL.md",
        "| \"Send me a weekly/daily report\" | `attribution-weekly-report` |",
        "| \"Send me a weekly/daily report\" | Build the live view, then explain that scheduled "
        "delivery isn't available in this plugin yet; the user can set it up in the WorkMagic app |",
    ),
    (
        "lift-test-readout/SKILL.md",
        "| “Create a lift test for me” / “set up a Meta test” | `lift-test-creation` |",
        "| “Create a lift test for me” / “set up a Meta test” | Not covered by this plugin yet — "
        "point the user to Lift Tests in the WorkMagic app, or their CSM |",
    ),
    (
        "lift-test-readout/SKILL.md",
        "| `lift-test-creation` | Upstream: how the test being read was set up. Route here when the "
        "user follows up with “rerun this with adjusted parameters.” |",
        "| Lift Tests in the WorkMagic app | Upstream: how the test being read was set up. Point the "
        "user there when they follow up with “rerun this with adjusted parameters.” |",
    ),
]

# Files the directory scanner rejects outright.
JUNK = {".DS_Store", "Thumbs.db", "desktop.ini"}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = pathlib.Path(sys.argv[1]).resolve() / "skills"
    if not src.is_dir():
        print(f"no skills/ folder under {src.parent}")
        return 1

    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    for name in SKILLS:
        shutil.copytree(
            src / name,
            DEST / name,
            ignore=lambda _d, names: [n for n in names if n in JUNK or n == "__MACOSX"],
        )

    failed = []
    for rel, old, new in PATCHES:
        path = DEST / rel
        text = path.read_text(encoding="utf-8")
        count = text.count(old)
        if count != 1:
            failed.append(f"{rel}: expected 1 match, found {count}: {old[:70]}…")
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")

    if failed:
        print("Patches that no longer match upstream — update PATCHES:")
        print("\n".join(f"  - {f}" for f in failed))
        return 1

    # Nothing in the shipped skills may still point at a server-side skill loader or
    # at a skill this release doesn't include.
    banned = ["skills_read", "skills-read", "skills-list", "attribution-weekly-report",
              "lift-test-creation", "conversation-log", "user_original",
              # Internal-only hosts must never ship in a public skill (points customers at
              # help.workmagic.io instead; also keeps the directory's credential scan clean).
              "larksuite"]
    leftovers = []
    for f in DEST.rglob("*"):
        if f.is_file():
            body = f.read_text(encoding="utf-8", errors="ignore")
            leftovers += [f"{f.relative_to(DEST)}: {b}" for b in banned if b in body]
    if leftovers:
        print("References that must be removed before release:")
        print("\n".join(f"  - {x}" for x in leftovers))
        return 1

    print(f"Synced {len(SKILLS)} skills into {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
