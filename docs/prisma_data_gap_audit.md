# PRISMA data-gap audit

Audit date: 5 October 2026.

## Repository inspection result

The repository was inspected directly for:
- raw database exports;
- PubMed/MEDLINE export files;
- complete title/abstract screening logs;
- duplicate-resolution tables;
- full-text retrieval logs;
- record-level exclusion logs;
- prior finalized PRISMA count files.

No complete record-level search export or full screening library is currently present.

The repository does contain:
- `data/fresh_search_candidates.csv`;
- `data/verified_include_candidates.csv`;
- historical screening-decision files;
- active included-study tables;
- PRISMA working-count and checklist files;
- the original undergraduate thesis materials.

These are sufficient to support the 34-study active evidence pool, but **not** sufficient to reconstruct valid identification, deduplication, screening, retrieval, and exclusion counts for a new PRISMA 2020 flow diagram.

## Why the old thesis counts cannot be reused

The archived undergraduate review reported historical counts (including 1,214 records and 27 included studies), but the current manuscript:
- uses a revised workplace-focused eligibility framework;
- includes studies through 2026;
- was freshly searched and re-screened;
- contains 34 active primary studies;
- treats cohort overlap and companion reports differently.

Therefore, reusing the thesis counts would create a false PRISMA trail.

## Resolution

A complete final search export is still required.

Once available:
1. populate `data/screening_log.csv` using `data/screening_log_template.csv`;
2. retain all duplicate records and mark `duplicate_of`;
3. complete title/abstract and full-text decisions;
4. assign one primary full-text exclusion reason;
5. assign `final_study_id` to each included report;
6. run `scripts/generate_prisma_counts.py`;
7. manually verify companion-report and duplicate links;
8. insert the generated counts into the PRISMA figure and manuscript.

## Current conclusion

The PRISMA counts remain intentionally unresolved. This is a documented data-availability limitation, not a manuscript-writing omission.
