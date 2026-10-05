# PRISMA completion protocol

This file defines how the final PRISMA 2020 counts will be generated once the complete search export is available.

## 1. Import every record

All records returned by the final PubMed/MEDLINE search and supplementary searches must be entered into:

`data/screening_log.csv`

The template is stored as:

`data/screening_log_template.csv`

Each retrieved record should have one row.

## 2. Preserve source provenance

For every record retain:
- database/source;
- exact query or supplementary-search route;
- date searched;
- title;
- first author;
- publication year;
- DOI or PMID where available.

Do not discard duplicate rows before recording their source.

## 3. Deduplication

Duplicates should be identified primarily by:
1. DOI;
2. PMID;
3. normalized title + year when identifiers are absent.

For duplicate records:
- retain one canonical row;
- populate `duplicate_of` for additional instances.

The number of duplicate rows gives the PRISMA count for duplicates removed before screening.

## 4. Title/abstract screening

Use only:
- `Include`
- `Exclude`

For exclusions, use a controlled reason where possible:
- not employed/workplace population;
- no eligible exposure/intervention;
- no MetS or eligible component outcome;
- wrong publication type;
- outside date/language criteria;
- protocol only;
- duplicate.

## 5. Full-text screening

Record:
- whether full text was sought;
- whether it was retrieved;
- final Include/Exclude decision;
- one primary exclusion reason.

Recommended full-text exclusion categories:
- wrong population/context;
- wrong exposure/intervention;
- wrong outcome;
- wrong study design/publication type;
- protocol/no completed results;
- duplicate/companion report without unique eligible outcome;
- outside publication criteria.

## 6. Companion reports

Where multiple papers arise from the same cohort or intervention:
- retain each eligible report in the screening log;
- populate `companion_report_of`;
- use a shared `final_study_id` for the underlying study where appropriate.

This permits PRISMA to distinguish reports from studies.

## 7. Count derivation

Once the screening log is complete, calculate:

### Identification
- records identified from PubMed/MEDLINE;
- records identified from supplementary methods;
- duplicates removed.

### Screening
- records screened;
- records excluded at title/abstract stage.

### Retrieval
- reports sought;
- reports not retrieved.

### Eligibility
- reports assessed at full text;
- reports excluded by reason.

### Inclusion
- included reports;
- included unique studies.

## 8. Freeze rule

No PRISMA number should be inserted into the abstract, manuscript, or final figure until:
- every row has a screening decision;
- every full-text exclusion has a reason;
- duplicate relationships are frozen;
- companion-report relationships are frozen;
- included-study and included-report counts reconcile with the final bibliography.

## 9. Current status

The active evidence pool contains 34 primary studies, and all 34 currently have bibliography records. This remains a working inclusion pool until the complete record-level search library is reconciled.
