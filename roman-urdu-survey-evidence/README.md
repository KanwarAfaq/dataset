# Roman Urdu Survey Evidence Deposit

This directory archives the machine-readable evidence matrix and structural validator used for the submitted manuscript **“Roman Urdu and Roman Urdu–English NLP: a structured survey of resources, methods, evaluation, and large language model safety.”**

## Files

- `S3_evidence_matrix.csv` — one row per cited record (67 rows), with source type, peer-review status, task, linguistic scope, provenance, verification status, and integrity fields.
- `S4_validate_evidence.py` — standard-library validator for citation/BibTeX/S3/file correspondence.
- `LIVE_REFERENCE_STATUS_2026-10-07.csv` — live metadata/publication-status audit used in the final technical round.
- `SHA256SUMS.txt` — hashes for the deposited files.

## Validation

The submitted package was required to pass `python3 S4_validate_evidence.py` with 67 BibTeX records, 67 unique citation keys, 67 S3 rows, no missing/extra/duplicate keys, and `VALIDATION: PASS`.

## Scope and limitation

This is a structured qualitative review rather than a formal systematic review. Original database exports, deduplication records, and row-level screening decisions were not preserved, so the original retrieval and screening flow cannot be reproduced exactly. The verification log covers selected high-impact claims; the structural validator does not itself establish statement-to-source validity.

## Version

Final technical audit date: **2026-10-07**.

This GitHub deposit is public and versioned by Git commits. It does **not** by itself provide a persistent DOI; a DOI can be minted separately through Zenodo/GitHub integration if desired.
