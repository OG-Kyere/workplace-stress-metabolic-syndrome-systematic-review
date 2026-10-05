# Workplace Determinants of Metabolic Syndrome in Working Adults

Updated systematic review examining occupational stress, diet and workplace nutrition, physical activity and sedentary behaviour, and workplace lifestyle interventions in relation to metabolic syndrome (MetS) among working adults.

## Current review status

This repository contains both:

1. the **archived undergraduate thesis source**, preserved for transparency; and
2. the **updated journal manuscript workflow**, which uses a revised workplace-focused eligibility framework and a fresh literature search extending through 2026.

The current journal manuscript is being prepared for submission to **Occupational Medicine**.

### Current evidence base

- **Search period:** 2015–2026
- **Primary bibliographic source:** PubMed/MEDLINE
- **Supplementary identification:** targeted searches, reference chasing, citation chasing, publisher records, related-article searching, and review-reference mining
- **Active evidence pool:** 34 primary studies
- **Study designs:** randomized controlled trials, prospective/cohort studies, analytical cross-sectional studies, and quasi-/nonrandomized workplace interventions
- **Critical appraisal:** design-specific Joanna Briggs Institute tools
- **Synthesis:** narrative, organized by occupational stress, diet/nutrition, physical activity/sedentary behaviour, and multicomponent workplace interventions

The **34-study pool is not yet the final PRISMA included-study count** because the complete record-level search export and deduplication library are not available in the repository. PRISMA counts are intentionally not reconstructed from memory.

## Historical undergraduate review

The archived thesis reported:
- 1,214 records identified;
- 27 included studies;
- searches using PubMed/MEDLINE, Scopus, and ScienceDirect;
- a 2015–2025 review window.

Those historical numbers belong to the undergraduate review only and **must not be reused as the PRISMA flow for the updated 2026 manuscript**.

The original thesis files are retained under `thesis_source/`.

## Working manuscript title

**Workplace Determinants of Metabolic Syndrome in Working Adults: Systematic Review**

## Repository structure

```text
.
├── README.md
├── LICENSE
├── data/                 # extraction, appraisal, screening and audit files
├── docs/                 # methods, eligibility, search and PRISMA documentation
├── manuscript/           # main manuscript, tables, supplement and submission files
├── scripts/              # reproducibility utilities
└── thesis_source/        # archived undergraduate thesis source and original figures
```

## Main manuscript files

- `manuscript/main.tex` — blinded journal manuscript
- `manuscript/tables_main.tex` — main Tables 1–3
- `manuscript/evidence_map_figure.tex` — evidence-map figure
- `manuscript/references_verified.bib` — bibliography aligned to the active 34-study pool
- `manuscript/supplementary_material.tex` — search strategy, full extraction table, item-level JBI appraisal
- `manuscript/title_page.md` — separate identifying title-page content
- `manuscript/cover_letter_occupational_medicine.md` — target-journal cover letter
- `manuscript/submission_upload_manifest.md` — upload map for the submission system

## PRISMA reproducibility

A record-level screening template is provided at:

`data/screening_log_template.csv`

When the complete search export is available:

1. copy the template to `data/screening_log.csv`;
2. enter every identified record, including duplicates;
3. complete screening and full-text decisions;
4. run:

```powershell
python scripts/generate_prisma_counts.py
```

The script generates `data/prisma_generated_counts.csv` and refuses to freeze incomplete screening data.

## Methodological safeguards

The updated review deliberately:
- separates historical thesis counts from the current review;
- avoids inferring missing PRISMA numbers;
- links overlapping cohorts and companion reports;
- prefers adjusted estimates where available;
- prefers between-group effects for intervention studies;
- uses design-specific JBI appraisal without arbitrary summed quality scores;
- avoids causal language for cross-sectional evidence;
- retains full study-level extraction and appraisal details in supplementary material.

## Authorship

The archived undergraduate thesis involved multiple student contributors.

**Final authorship of the journal manuscript is not yet frozen.**  
The current submission files should therefore be treated as provisional until authorship eligibility and contribution statements are finalized.

## Data and reproducibility

The repository contains:
- the active-study master table;
- design classification;
- study-level effect extraction;
- JBI appraisal files;
- bibliographic identity corrections;
- bibliography-to-study audit;
- PRISMA completion protocol;
- submission-readiness and anonymization checks.

## Archived-source note

The historical thesis source references an `abbreviations.tex` file that was not present in the archived package. The archive is preserved as supplied rather than silently reconstructing the missing file.

## License

Unless otherwise noted, research materials in this repository are shared under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

## Contact

For questions about the repository, please open an issue.
