# Freeze drift check

The non-PRISMA manuscript was frozen on 6 October 2026.

A dedicated branch preserves that snapshot:

`freeze/non-prisma-2026-10-06`

To check whether locked files have drifted on `main`, run:

```powershell
python scripts/check_freeze_drift.py
```

The checker compares each frozen file against its Git blob SHA recorded at freeze time.

## Expected behaviour

- Exit code **0**: all frozen files still match.
- Exit code **2**: at least one frozen file changed or is missing.

Changes after freeze are acceptable only for:
- PRISMA completion;
- final author metadata;
- source-supported factual corrections;
- pure production/LaTeX fixes.

If a substantive file changes, document why before submission.
