#!/usr/bin/env python3
"""
Generate PRISMA 2020 counts from data/screening_log.csv.

This script intentionally refuses to infer missing decisions.
It reports incomplete fields so PRISMA numbers are not frozen prematurely.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

INPUT = Path("data/screening_log.csv")
OUTPUT = Path("data/prisma_generated_counts.csv")

YES = {"yes", "y", "true", "1"}
INCLUDE = {"include", "included"}
EXCLUDE = {"exclude", "excluded"}

def norm(value: str) -> str:
    return (value or "").strip().lower()

def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    if not INPUT.exists():
        raise SystemExit(
            "Missing data/screening_log.csv. Copy the template, populate every retrieved record, "
            "and rerun this script."
        )

    rows = load_rows(INPUT)
    if not rows:
        raise SystemExit("screening_log.csv contains no records.")

    duplicates = [r for r in rows if norm(r.get("duplicate_of"))]
    canonical = [r for r in rows if not norm(r.get("duplicate_of"))]

    ta_missing = [r for r in canonical if norm(r.get("title_abstract_decision")) not in INCLUDE | EXCLUDE]
    screened = [r for r in canonical if norm(r.get("title_abstract_decision")) in INCLUDE | EXCLUDE]
    ta_excluded = [r for r in canonical if norm(r.get("title_abstract_decision")) in EXCLUDE]
    ta_included = [r for r in canonical if norm(r.get("title_abstract_decision")) in INCLUDE]

    sought = [r for r in ta_included if norm(r.get("full_text_sought")) in YES]
    not_retrieved = [
        r for r in sought
        if norm(r.get("full_text_retrieved")) not in YES
    ]
    retrieved = [
        r for r in sought
        if norm(r.get("full_text_retrieved")) in YES
    ]

    ft_missing = [
        r for r in retrieved
        if norm(r.get("full_text_decision")) not in INCLUDE | EXCLUDE
    ]
    ft_excluded = [
        r for r in retrieved
        if norm(r.get("full_text_decision")) in EXCLUDE
    ]
    ft_included = [
        r for r in retrieved
        if norm(r.get("full_text_decision")) in INCLUDE
    ]

    reasons = Counter(
        (r.get("full_text_exclusion_reason") or "Reason not recorded").strip()
        for r in ft_excluded
    )

    included_reports = len(ft_included)
    study_ids = {
        (r.get("final_study_id") or "").strip()
        for r in ft_included
        if (r.get("final_study_id") or "").strip()
    }
    included_studies = len(study_ids)

    source_counts = Counter((r.get("source") or "Unspecified source").strip() for r in rows)

    incomplete = []
    if ta_missing:
        incomplete.append(f"{len(ta_missing)} canonical records lack title/abstract decisions")
    if ft_missing:
        incomplete.append(f"{len(ft_missing)} retrieved full texts lack final eligibility decisions")
    missing_reason = [r for r in ft_excluded if not norm(r.get("full_text_exclusion_reason"))]
    if missing_reason:
        incomplete.append(f"{len(missing_reason)} excluded full texts lack an exclusion reason")
    missing_study_id = [r for r in ft_included if not norm(r.get("final_study_id"))]
    if missing_study_id:
        incomplete.append(f"{len(missing_study_id)} included reports lack final_study_id")

    out_rows = [
        ("records_total_all_sources", len(rows)),
        ("duplicates_removed", len(duplicates)),
        ("records_screened", len(screened)),
        ("records_excluded_title_abstract", len(ta_excluded)),
        ("reports_sought_for_retrieval", len(sought)),
        ("reports_not_retrieved", len(not_retrieved)),
        ("reports_assessed_full_text", len(retrieved)),
        ("reports_excluded_full_text", len(ft_excluded)),
        ("reports_included", included_reports),
        ("unique_studies_included", included_studies),
    ]

    for source, count in sorted(source_counts.items()):
        out_rows.append((f"source::{source}", count))
    for reason, count in sorted(reasons.items()):
        out_rows.append((f"full_text_exclusion::{reason}", count))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "count"])
        writer.writerows(out_rows)

    print(f"Wrote {OUTPUT}")
    for metric, count in out_rows:
        print(f"{metric}: {count}")

    if incomplete:
        print("\nPRISMA NOT READY TO FREEZE:")
        for item in incomplete:
            print(f"- {item}")
        raise SystemExit(2)

    print("\nAll required screening decisions are populated.")
    print("Counts may be frozen only after duplicate and companion-report links are manually reviewed.")

if __name__ == "__main__":
    main()
