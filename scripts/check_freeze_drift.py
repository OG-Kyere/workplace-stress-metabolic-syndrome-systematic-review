#!/usr/bin/env python3
"""
Check whether frozen non-PRISMA files have drifted from the 6 Oct 2026 freeze.

Run from the repository root:
    python scripts/check_freeze_drift.py

Requires Git to be installed and the files to be present in the working tree.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
import sys

FROZEN = {
    "manuscript/main.tex": "6ccd2479b34e1e8c1dea710e5853430cc2257e8c",
    "manuscript/tables_main.tex": "2a31d25530c69ef7589a775ef667f7deccfc3978",
    "manuscript/supplementary_material.tex": "df0a84cca1a67cb0f286164a4bb9771441246c10",
    "manuscript/references_verified.bib": "12d16f21e1794fbaa8aa7201705a8f5132a157cd",
    "data/master_study_characteristics_findings.csv": "18398b3913c1dce0e93743adf7c27ac369ab83e3",
    "data/effect_estimate_verification_status.csv": "3a0ae0c5e430d1a7cdae6d10a207127e72ff2d5a",
    "manuscript/evidence_map_figure.tex": "b4efa80e34a79133b48ed0ecdc5714113f9ad4c0",
    "manuscript/title_page.md": "b0cd53b365d89af3b76dccd322ef2f51d6af46cc",
    "manuscript/cover_letter_occupational_medicine.md": "16fbc7f5d8aa8df1c1f9beae0b1bde567e0dce38",
}

def git_blob_hash(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def main() -> int:
    changed = []
    missing = []

    print("Non-PRISMA freeze drift check")
    print("=" * 34)

    for filename, frozen_sha in FROZEN.items():
        path = Path(filename)
        if not path.exists():
            missing.append(filename)
            print(f"MISSING  {filename}")
            continue

        current_sha = git_blob_hash(path)
        if current_sha == frozen_sha:
            print(f"OK       {filename}")
        else:
            changed.append((filename, frozen_sha, current_sha))
            print(f"CHANGED  {filename}")
            print(f"         frozen:  {frozen_sha}")
            print(f"         current: {current_sha}")

    print()

    if not changed and not missing:
        print("PASS: all frozen files match the 6 Oct 2026 freeze.")
        return 0

    print("FREEZE DRIFT DETECTED.")
    if changed:
        print("\nChanged files:")
        for filename, _, _ in changed:
            print(f"- {filename}")
    if missing:
        print("\nMissing files:")
        for filename in missing:
            print(f"- {filename}")

    print(
        "\nA difference is acceptable only if it is explained by PRISMA completion, "
        "final author metadata, a source-supported correction, or a pure production fix."
    )
    return 2

if __name__ == "__main__":
    sys.exit(main())
