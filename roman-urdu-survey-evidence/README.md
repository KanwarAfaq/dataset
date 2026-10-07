# Roman Urdu Survey Evidence Deposit

This directory archives the machine-readable evidence matrix and structural validator used for the submitted manuscript **“Roman Urdu and Roman Urdu–English NLP: a structured survey of resources, methods, evaluation, and large language model safety.”**

## Files

- `S3_evidence_matrix.csv` — one row per cited record (67 rows), with source type, peer-review status, task, linguistic scope, provenance, verification status, and integrity fields.
- `S4_validate_evidence.py` — standard-library submission validator for citation/BibTeX/S3 correspondence, required graphics, controlled fields, drafting residue, count labels, and SHA-256 source hashes.
- `LIVE_REFERENCE_STATUS_2026-10-07.csv` — live metadata/publication-status audit used in the final technical round.
- `SHA256SUMS.txt` — hashes for the deposited evidence/audit files.

## Validation

The submission package is required to pass `python3 S4_validate_evidence.py`. Validator v2.0 prints a UTC timestamp, source-file SHA-256 hashes, record/citation counts, and an explicit PASS/FAIL result for every structural check. The final submission transcript is included with the manuscript package as `S4_validation_final.txt`.

## Scope and limitation

This is a structured qualitative review rather than a formal systematic review. Original database exports, deduplication records, and row-level screening decisions were not preserved, so the original retrieval and screening flow cannot be reproduced exactly. The verification log covers selected high-impact claims; the structural validator does not itself establish statement-to-source validity.

## Version

Final technical audit date: **2026-10-07**.

This GitHub directory is public and versioned by Git commits. The manuscript cites a commit-pinned directory URL so the archived S3/S4 version cannot silently move with the default branch. No DOI is claimed unless a separate persistent DOI is minted.
