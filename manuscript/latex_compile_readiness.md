# LaTeX compile-readiness audit

Audit date: 5 October 2026.

## Static checks passed

- All `\\begin{...}` / `\\end{...}` environment counts reconcile across the integrated manuscript, main tables, and evidence-map figure.
- The manuscript inputs only the expected component files:
  - `tables_main.tex`
  - `evidence_map_figure.tex`
- Bibliography has no raw unescaped ampersands remaining.
- Suspicious malformed TeX accent groups in the bibliography were removed.
- All citation keys used in the manuscript resolve to bibliography entries.
- All 34 active studies map to bibliography records.

## Build status

A true PDF compilation could not be executed in the current runtime because the repository could not be cloned into the local container owing to unavailable DNS/network access. Therefore this audit is a static compile-readiness check, not a claim of successful PDF compilation.

## Recommended final local/Overleaf build sequence

1. Put `main.tex`, `tables_main.tex`, `evidence_map_figure.tex`, and `references_verified.bib` in the same Overleaf project directory.
2. Set `main.tex` as the main document.
3. Compile with pdfLaTeX/BibTeX (Overleaf handles the sequence automatically).
4. Inspect for overfull tables, line wrapping, and bibliography formatting.
5. Do not insert the PRISMA flow template into the review copy until the counts are frozen.
