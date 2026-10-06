# OEM LaTeX shell notes

`manuscript/oem_main_shell.tex` is an OEM-specific submission shell.

It is intentionally **not** the scientific master.

## Why it exists

The repository now separates:

- frozen scientific content: `manuscript/main.tex`
- OEM-specific submission framing: `manuscript/oem_main_shell.tex`

This avoids editing the frozen evidence synthesis simply to satisfy journal front-matter requirements.

## Final assembly

After PRISMA counts are frozen:

1. copy the scientific body from `main.tex`, beginning at `\section{Introduction}`;
2. stop before the current declarations/bibliography block;
3. paste that body into the OEM shell at the marked location;
4. insert the final PRISMA flow figure and final study-selection counts;
5. remove all provisional PRISMA caveats;
6. confirm the final author list and corresponding-author email;
7. compile and visually inspect;
8. run the freeze-drift checker before upload.

Do not edit locked effect sizes, study designs or interpretations during assembly unless a source-supported correction is documented.
