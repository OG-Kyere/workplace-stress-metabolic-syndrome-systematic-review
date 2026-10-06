# OEM final submission assembly checklist

Preferred target: **Occupational and Environmental Medicine (BMJ)**

This checklist defines how the final submission package should be assembled after PRISMA counts are frozen.

## 1. Scientific master

Use the frozen scientific content from:

- `manuscript/main.tex`
- `manuscript/tables_main.tex`
- `manuscript/evidence_map_figure.tex`
- `manuscript/references_verified.bib`
- `manuscript/supplementary_material.tex`

Authoritative snapshot:

`freeze/non-prisma-2026-10-06-v2`

Do not alter substantive results, study classifications, or effect estimates unless a source-supported correction is documented.

## 2. OEM front matter

Use:

- `manuscript/oem_submission_wrapper.md`
- `manuscript/oem_author_front_matter.md`
- `manuscript/oem_key_messages.md`

Replace the current generic/Occupational Medicine-specific front matter with the OEM version only in the final OEM submission copy.

## 3. Abstract

Use the OEM-style headings:

- Objectives
- Methods
- Results
- Conclusions

Keep within the journal's abstract limit.

## 4. Key messages

Insert immediately after the abstract:

### What is already known on this topic
Use the text in `manuscript/oem_key_messages.md`.

### What this study adds
Use the text in `manuscript/oem_key_messages.md`.

### How this study might affect research, practice or policy
Use the text in `manuscript/oem_key_messages.md`.

## 5. PRISMA completion

Before assembly:

- populate `data/screening_log.csv`;
- run `python scripts/generate_prisma_counts.py`;
- verify duplicate links;
- verify companion-report links;
- freeze included report/study counts;
- populate the PRISMA flow diagram;
- remove provisional PRISMA caveats from the manuscript.

The PRISMA flow will become the fifth main display item.

## 6. Tables and figures

Final expected main display items:

1. Table 1 — Characteristics of included studies
2. Table 2 — Principal findings
3. Table 3 — Methodological appraisal summary
4. Figure 1 — Evidence map
5. Figure 2 — PRISMA 2020 flow diagram

This remains within OEM's five-item limit.

## 7. Supplementary material

Upload separately:

- Supplementary Methods S1 — complete search strategy
- Supplementary Table S1 — full study characteristics and extraction
- Supplementary Tables S2–S5 — item-level JBI appraisal
- Supplementary Note S1 — overlapping cohorts and companion reports

## 8. Author-facing files

Use:

- `manuscript/cover_letter_oem.md`
- `manuscript/oem_author_front_matter.md`

Still to resolve:
- corresponding-author email;
- final author list;
- contribution wording if additional authors qualify.

## 9. Data availability

For OEM's single-anonymised review model, the final submission copy may restore the public repository URL:

https://github.com/OG-Kyere/workplace-stress-metabolic-syndrome-systematic-review

## 10. Final checks before upload

Run:

```powershell
python scripts/check_freeze_drift.py
```

Then confirm:
- no unexplained drift from the frozen evidence files;
- no unfinished extraction markers;
- all citations resolve;
- all 34 study references remain present;
- word count remains within limit;
- display count remains at five;
- final PRISMA counts reconcile;
- title page and submission metadata use the same author list;
- cover letter uses the same title and article type;
- all required declarations are present.

## 11. Files not to upload

Do not upload internal workflow files such as:
- audit notes;
- freeze manifests;
- screening-development notes;
- old thesis figures;
- internal CSV audit files;
- provisional PRISMA templates once the final figure is available.

## Final state

Once PRISMA and author metadata are resolved, the project can be assembled into an OEM submission package without changing the frozen scientific evidence base.
