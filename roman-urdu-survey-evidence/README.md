# Roman Urdu Survey Evidence Deposit

This directory archives the machine-readable evidence matrix and structural validator used for the manuscript **“Roman Urdu and Roman Urdu–English NLP: a structured survey of resources, methods, evaluation, and large language model safety.”**

## Files

- `S3_evidence_matrix.csv` — one row per cited record (67 rows), with source type, peer-review status, task, linguistic scope, provenance, verification status, and integrity fields.
- `S4_validate_evidence.py` — standard-library submission validator for citation/BibTeX/S3 correspondence, required graphics, controlled fields, drafting residue, count labels, SHA-256 source hashes, and generated source-type counts.
- `S3_SOURCE_TYPE_COUNTS.txt` — count artifact generated directly from the controlled S3 fields, including the documented aggregation rule used for descriptive source-type reporting.
- `LIVE_REFERENCE_STATUS_2026-10-07.csv` — live metadata/publication-status audit used in the final technical round.
- `ELIGIBILITY_CUTOFF_AUDIT_2026-10-07.csv` — audit of the 2026 records retained in the 67-record source set against the 15 July 2026 eligibility cutoff.
- `POST_CUTOFF_CONTEXT_CHECK_2026-10-07.csv` — documents the post-cutoff CMU/EMNLP romanization paper raised by a reviewer and records that it is not cited or included in the current source set.
- `REVIEWER_MINOR_REVISION_WEB_CHECK_2026-10-07.csv` — issue-by-issue resolution of the final metadata/cutoff comments using official web records.
- `SHA256SUMS.txt` — hashes for the deposited evidence/audit files.
- `evidence_bundle.zip` — convenience bundle of the deposited evidence/audit files.

## Validation

The submission package is required to pass `python3 S4_validate_evidence.py`. Validator v2.0 prints a UTC timestamp, source-file SHA-256 hashes, record/citation counts, controlled S3 publication-type and peer-review-status counts, normalized source-type counts, and an explicit PASS/FAIL result for every structural check. The final submission transcript is included with the manuscript package as `S4_validation_final.txt`.

## Metadata decisions verified against official records

- ROMEVA is retained as arXiv:2606.22478 (v1 submitted 21 June 2026); ACL Anthology ID `2025.americasnlp-1.2` is an unrelated Choctaw dialogue-system paper.
- Token Cost Inequality uses the official GEM 2026 ACL Anthology record, DOI `10.18653/v1/2026.gem-main.54`.
- RomanUrdu-NLP-Sentiment-Corpus uses the official Hugging Face dataset DOI `10.57967/hf/7931`.
- The post-cutoff paper *One Form to Transfer Them All* (arXiv:2608.25904; submitted 26 August 2026) is not part of the current 67-record evidence set.

## Scope and limitation

This is a structured qualitative review rather than a formal systematic review. Original database exports, deduplication records, and row-level screening decisions were not preserved, so the original retrieval and screening flow cannot be reproduced exactly. The verification log covers selected high-impact claims; the structural validator does not itself establish statement-to-source validity.

## Version

Final technical audit date: **2026-10-07**.

This GitHub directory is public and versioned by Git commits. The manuscript cites a commit-pinned directory URL so the archived S3/S4 version cannot silently move with the default branch. No DOI is claimed unless a separate persistent DOI is minted.