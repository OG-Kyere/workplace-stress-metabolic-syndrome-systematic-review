# Non-PRISMA freeze manifest

Freeze date: 6 October 2026.

Authoritative freeze branch: `freeze/non-prisma-2026-10-06-v2`.

Earlier snapshot retained for audit history: `freeze/non-prisma-2026-10-06`.

This manifest records the current Git blob identities for the manuscript components that are considered **frozen except for PRISMA insertion, final author metadata, or source-supported corrections**.

## Frozen core files

| File | Git blob SHA |
|---|---|
| `manuscript/main.tex` | `6ccd2479b34e1e8c1dea710e5853430cc2257e8c` |
| `manuscript/tables_main.tex` | `2a31d25530c69ef7589a775ef667f7deccfc3978` |
| `manuscript/supplementary_material.tex` | `df0a84cca1a67cb0f286164a4bb9771441246c10` |
| `manuscript/references_verified.bib` | `12d16f21e1794fbaa8aa7201705a8f5132a157cd` |
| `data/master_study_characteristics_findings.csv` | `18398b3913c1dce0e93743adf7c27ac369ab83e3` |
| `data/effect_estimate_verification_status.csv` | `3a0ae0c5e430d1a7cdae6d10a207127e72ff2d5a` |
| `manuscript/evidence_map_figure.tex` | `b4efa80e34a79133b48ed0ecdc5714113f9ad4c0` |
| `manuscript/title_page.md` | `b0cd53b365d89af3b76dccd322ef2f51d6af46cc` |
| `manuscript/cover_letter_occupational_medicine.md` | `16fbc7f5d8aa8df1c1f9beae0b1bde567e0dce38` |

## Freeze scope

The following are frozen:
- title and article type;
- abstract and teaser;
- eligibility framework;
- study-design classification;
- 34-study active evidence pool;
- Table 1 study characteristics;
- Table 2 principal findings;
- Table 3 appraisal summary;
- evidence-map figure;
- bibliography mapping;
- supplementary extraction table;
- supplementary JBI tables;
- funding/conflict/ethics/data-availability/AI text;
- cover-letter core narrative.

## Permitted changes after freeze

Changes to frozen files should be limited to:

1. **PRISMA completion**
   - final search counts;
   - final included report/study count;
   - PRISMA flow figure;
   - removal of provisional PRISMA caveats.

2. **Final author metadata**
   - corresponding-author email;
   - final author list;
   - author contributions;
   - title-page metadata.

3. **Source-supported correction**
   - only when a source-level audit identifies a factual, bibliographic, methodological, or numerical error.

4. **Pure production fixes**
   - LaTeX compile repair;
   - line wrapping;
   - pagination;
   - accessibility text;
   - journal formatting that does not alter substantive meaning.

## Not frozen

The following remain intentionally open:
- record-level screening library;
- PRISMA identification/screening/retrieval/exclusion counts;
- PRISMA flow diagram;
- corresponding-author email;
- final authorship.

## Drift check

Before submission, refetch the frozen files and compare their blob SHAs with this manifest. Any difference should be explainable by one of the permitted changes above.

This provides an auditable boundary between the completed evidence/manuscript work and the remaining PRISMA/metadata tasks.
