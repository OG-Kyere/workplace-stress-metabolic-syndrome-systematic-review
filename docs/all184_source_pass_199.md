# All184 source-capture pass

All184 available originals were processed together, with source and packet hashes checked and no parsing failures. This is a first-pass source capture, not completed clinical extraction or independent verification.

Actual formats:162XML,10HTML,12PDF. Thirty-seven `.source` files contain XML; they had been incorrectly routed to manual capture by filename suffix. The full343-original format audit finds267XML,36HTML,40PDF; its62XML `.source` files explain the earlier inflated PDF/other category.

The pass captured5,521 clinical-keyword candidate table rows across165 reports, alongside original methods/results passages, captions, headers, footnotes, row/column spans and exact source hashes. Candidates include baseline descriptions and rows whose exposure/model/endpoint cannot yet be interpreted. They are not5,521 verified effects and are not added to the normalized result count. PDF pages may include references or columns requiring visual separation. Graphics-only tables and absent candidate matches remain explicit.

Three PDF originals were visually inspected at their clinical tables and contributed33 specified results:Viester12,Geaney9,Rusali12. Two of those papers had no automatically captured table rows. Of the184 reports,3 now have those specified PDF findings,164 have machine table candidates only, and17 have no machine candidate rows and need narrative/figure/manual work. These statuses do not certify full extraction for any report.

Overall specified-result coverage is162reports. Of388 provisional reports,181available originals still lack specified rows in these ledgers and45original-source gaps remain deferred. Reports with some rows still require full endpoint/model/denominator and companion verification. Independent reviews completed:zero. Eligibility decisions, screening counts and PRISMA freeze have not been changed.

The local ZIP contains184 report packets, the whole-set index, candidate table rows, source-format audit, three visually checked PDF-result rows, source images for those checks, the capture/validation scripts and a hash manifest. Original article files remain in the research workspace; the packet source paths/hashes identify them. Primary passages are source captures rather than independently reviewed findings. Read this status alongside the manuscript; do not treat the archive as a finished research freeze.
