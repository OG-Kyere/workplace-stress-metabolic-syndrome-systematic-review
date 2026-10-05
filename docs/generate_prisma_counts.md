# Generate PRISMA counts

After the complete search export has been entered into `data/screening_log.csv`, run from the repository root:

```powershell
python scripts/generate_prisma_counts.py
```

The script writes:

`data/prisma_generated_counts.csv`

It exits with a non-zero status if:
- canonical records lack title/abstract decisions;
- retrieved full texts lack final decisions;
- excluded full texts lack reasons;
- included reports lack final study IDs.

This safeguard prevents incomplete screening data from being treated as final PRISMA numbers.
