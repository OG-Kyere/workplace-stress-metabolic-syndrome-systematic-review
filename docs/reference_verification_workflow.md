# Reference Verification Workflow

This folder uses a two-stage bibliography process.

1. `data/citation_key_map.csv` assigns one stable citation key to every study in the active pool.
2. `data/reference_verification_status.csv` records whether the full bibliographic metadata has been independently verified.

A DOI or PMID in the candidate table is **not** treated as sufficient evidence for a complete citation. Author list, journal title, year, volume/issue, pages/article number, and DOI must be checked before the corresponding BibTeX record is frozen.

## Current verified examples

- Alavi et al. 2015 — Int J Occup Environ Med 6(1):34–40; PMID 25588224.
- Garbarino & Magnavita 2015 — PLOS ONE 10(12):e0144318.
- Kuwahara et al. 2016 — Endocrine 53(3):710–721; PMID 26951053.
- Browne et al. 2017 — J Occup Environ Med 59(11):1029–1033; DOI 10.1097/JOM.0000000000001104.
- Appiah et al. 2020 — Pan Afr Med J 36:136; PMID 32849991.
- Eftekhari et al. 2021 — J Diabetes Metab Disord 20(1):321–327; PMID 34178840.
- Zhang et al. 2024 — BMC Public Health 24:802.
- So et al. 2025 — Occup Med (Lond) 75(8):502–509; PMID 40796105.
- Bogale et al. 2025 — Scientific Reports 15:39266.

## Rule

The final `references.bib` must be generated only from records whose bibliographic metadata has been verified. Placeholder or guessed metadata must never be silently promoted to the final reference list.
