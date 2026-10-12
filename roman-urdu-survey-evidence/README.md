# Roman Urdu Survey Evidence Deposit

This directory contains the remaining machine-readable evidence artifacts and the structural validator used for the manuscript **“Roman Urdu and Roman Urdu–English NLP: a structured survey of resources, methods, and evaluation practices.”**

## Remaining files

- `S3_evidence_matrix.csv` — one row per cited record (67 rows), with source type, peer-review status, task, linguistic scope, provenance, verification status, and integrity fields.
- `S4_validate_evidence.py` — standard-library validator for citation/BibTeX/S3 correspondence, required graphics, controlled fields, drafting residue, count labels, SHA-256 source hashes, and package completeness. It is retained here as the validation script used with the full manuscript package.
- `S3_SOURCE_TYPE_COUNTS.txt` — count artifact generated from the controlled S3 fields, including the documented aggregation rule used for descriptive source-type reporting.
- `SHA256SUMS.txt` — SHA-256 checksums for the evidence files retained in this directory.
- `README.md` — this description of the retained deposit.

The live metadata audits, cutoff-review tables, reviewer web-check table, and ZIP convenience bundle previously associated with this deposit are no longer present in the directory and are not listed as part of the current deposit.

## Validation

From this directory, verify the retained evidence-file checksums with:

```bash
sha256sum -c SHA256SUMS.txt
```

`S4_validate_evidence.py` was written for the complete manuscript submission package. It expects companion files such as `main.tex`, `S1.tex`, `S2.tex`, `roman_urdu_survey.bib`, `wlpeerj.cls`, and any graphics referenced by the manuscript; those files are not included in the current directory listing. Run the validator from the complete package when those companion files are available.

## Evidence summary

The retained S3 matrix contains 67 cited records. The accompanying count artifact reports the controlled publication-type and peer-review-status counts, plus normalized source-type counts. These counts describe only the identified source set; they are not field-wide publication rates or temporal trends.

## Scope and limitation

This is a structured qualitative review rather than a formal systematic review. Original database exports, deduplication records, row-level screening decisions, and the previously deposited audit tables are not preserved in the current directory. The retained matrix should therefore be interpreted as the final evidence table available in this repository, not as a complete reconstruction of the original search and screening process.

## Version

This directory is public and versioned by Git commits. Use a commit-pinned directory URL when citing the deposit so the referenced S3 matrix and validation artifacts cannot silently move with the default branch. The current directory contains only the files listed above.
