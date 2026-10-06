# PRISMA 2020 checklist crosswalk

Current manuscript: **Workplace Determinants of Metabolic Syndrome in Working Adults: Systematic Review**

Target workflow: OEM/BMJ submission after PRISMA record-level counts are frozen.

This crosswalk maps PRISMA 2020 reporting items to the current manuscript and supplementary files. Count-dependent items remain intentionally incomplete until the record-level screening library is available.

## Title and abstract

| PRISMA item | Reporting status | Current location |
|---|---|---|
| 1. Title identifies the report as a systematic review | Complete | Manuscript title |
| 2. Abstract follows systematic-review reporting structure | Complete, OEM wrapper prepared | `manuscript/oem_submission_wrapper.md`; scientific abstract in `manuscript/main.tex` |

## Introduction

| PRISMA item | Reporting status | Current location |
|---|---|---|
| 3. Rationale | Complete | Introduction, paragraphs 1–5 |
| 4. Objectives | Complete | Final paragraph of Introduction |

## Methods

| PRISMA item | Reporting status | Current location |
|---|---|---|
| 5. Eligibility criteria | Complete | Methods — Eligibility criteria |
| 6. Information sources | Complete in principle | Methods — Search strategy; Supplementary Methods S1 |
| 7. Search strategy | Complete | Supplementary Methods S1; `docs/fresh_search_protocol.md` |
| 8. Selection process | Complete in method description; counts pending | Methods — Study selection and data extraction |
| 9. Data collection process | Complete | Methods — Study selection and data extraction |
| 10a. Data items — outcomes | Complete | Eligibility criteria; master extraction table |
| 10b. Data items — other variables | Complete | Methods — Study selection and data extraction |
| 11. Study risk-of-bias / quality assessment | Complete | Methods — Critical appraisal; Supplementary Tables S2–S5 |
| 12. Effect measures | Complete in narrative framework | Methods — Study selection/data extraction and Data synthesis |
| 13a. Eligibility for each synthesis | Complete | Methods — Data synthesis |
| 13b. Data preparation | Complete in repository workflow | Master extraction/effect-estimate files |
| 13c. Tabulation/visual display methods | Complete | Tables 1–3; evidence-map figure |
| 13d. Synthesis methods | Complete | Methods — Data synthesis |
| 13e. Exploration of heterogeneity | Narrative only; complete for current design | Methods and Discussion |
| 13f. Sensitivity analyses | Not applicable | No quantitative meta-analysis performed |
| 14. Reporting-bias assessment | Not formally performed | Must be stated explicitly before final submission |
| 15. Certainty/confidence assessment | Not formally graded | JBI appraisal used to qualify confidence; no GRADE framework applied |

## Results

| PRISMA item | Reporting status | Current location |
|---|---|---|
| 16a. Study selection flow | **Pending** | Final PRISMA 2020 flow diagram |
| 16b. Studies that appeared eligible but were excluded, with reasons | **Pending record-level reconciliation** | `data/screening_log.csv` once available |
| 17. Study characteristics | Complete | Table 1; Supplementary Table S1 |
| 18. Risk-of-bias / quality results | Complete | Table 3; Supplementary Tables S2–S5 |
| 19. Results of individual studies | Complete for displayed principal findings | Table 2; Supplementary Table S1 |
| 20a. Summary of contributing studies for each synthesis | Complete | Results subsections |
| 20b. Statistical synthesis results | Not applicable | No meta-analysis |
| 20c. Investigation of heterogeneity | Narrative | Results and Discussion |
| 20d. Sensitivity analyses | Not applicable | No meta-analysis |
| 21. Reporting biases | Not formally assessed | Must be acknowledged in limitations |
| 22. Certainty of evidence | Narratively qualified, not formally graded | Discussion; Table 3 |

## Discussion

| PRISMA item | Reporting status | Current location |
|---|---|---|
| 23a. General interpretation | Complete | Discussion paragraphs 1–4 |
| 23b. Limitations of included evidence | Complete | Discussion |
| 23c. Limitations of review processes | Complete but PRISMA limitation remains open | Discussion |
| 23d. Implications for practice/policy/future research | Complete | Final Discussion paragraphs |

## Other information

| PRISMA item | Reporting status | Current location |
|---|---|---|
| 24a. Registration information | Not currently registered | Must be stated explicitly in final manuscript |
| 24b. Protocol access | No formal prospective protocol currently documented | Historical/fresh-search workflow documented in repo |
| 24c. Amendments to protocol | Not applicable in formal-registration sense | Scope/path-A decisions documented in repository |
| 25. Sources of support | Complete | Funding statement |
| 26. Competing interests | Complete | Conflict-of-interest statement |
| 27. Availability of data/code/materials | Complete in principle | Data Availability Statement and public repository |

## Items that still require an explicit statement before submission

The following PRISMA items are not missing because of oversight; they simply require transparent wording:

1. **Reporting-bias assessment:** no formal publication-bias analysis was performed because no pooled meta-analysis was undertaken and the evidence was highly heterogeneous.
2. **Certainty assessment:** no formal GRADE certainty framework was applied; design-specific JBI appraisal and study design were used to qualify confidence in the narrative synthesis.
3. **Registration:** the updated review was not prospectively registered.
4. **Protocol:** no prospectively registered protocol was available; the updated eligibility/search framework is transparently documented in the repository.

## Count-dependent items still blocked by missing raw search export

Do not mark the following complete until `data/screening_log.csv` is populated and reconciled:

- records identified by source;
- duplicates removed;
- records screened;
- title/abstract exclusions;
- reports sought;
- reports not retrieved;
- full texts assessed;
- full-text exclusions by reason;
- included reports;
- included unique studies;
- PRISMA flow diagram;
- excluded-near-miss study list.

## Final rule

The PRISMA checklist should be uploaded only after the record-level counts are frozen and all "Pending" entries above have been replaced by exact manuscript page/section references.
