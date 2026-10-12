# Roman Urdu Survey Evidence Deposit

This directory archives the machine-readable evidence matrix, the structural validation script, and the final audit artifacts used for the manuscript **“Roman Urdu and Roman Urdu–English NLP: a structured survey of resources, methods, and evaluation practices.”** The deposit is intended to make the cited evidence set reproducible and inspectable without depending on a moving default branch.

## Files

- `S3_evidence_matrix.csv` — one row per cited record (67 rows), with source type, peer-review status, task, linguistic scope, provenance, verification status, and integrity fields.
- `S4_validate_evidence.py` — standard-library submission validator for citation/BibTeX/S3 correspondence, required graphics, controlled fields, drafting residue, count labels, SHA-256 source hashes, and package completeness.
- `S3_SOURCE_TYPE_COUNTS.txt` — count artifact generated directly from the controlled S3 fields, including the documented aggregation rule used for descriptive source-type reporting.
- `LIVE_REFERENCE_STATUS_2026-10-07.csv` — live metadata/publication-status audit used in the final technical round.
- `ELIGIBILITY_CUTOFF_AUDIT_2026-10-07.csv` — audit of the 2026 records retained in the 67-record source set against the 15 July 2026 eligibility cutoff.
- `POST_CUTOFF_CONTEXT_CHECK_2026-10-07.csv` — documents the post-cutoff CMU/EMNLP romanization paper raised by a reviewer and records that it is not cited or included in the current source set.
- `REVIEWER_MINOR_REVISION_WEB_CHECK_2026-10-07.csv` — issue-by-issue resolution of the final metadata/cutoff comments using official web records.
- `SHA256SUMS.txt` — hashes for the deposited evidence/audit files.
- `evidence_bundle.zip` — convenience bundle of the deposited evidence/audit files.

## Quick validation

The submission package is required to pass:

```bash
python3 S4_validate_evidence.py
```

To verify the archived file integrity hash bundle, also run:

```bash
sha256sum -c SHA256SUMS.txt
```

The validator prints a UTC timestamp, source-file SHA-256 hashes, record/citation counts, controlled S3 publication-type summaries, normalized source-type counts, and any structural mismatches or drafting residue.

## Metadata decisions verified against official records

- ROMEVA is retained as arXiv:2606.22478 (v1 submitted 21 June 2026); ACL Anthology ID `2025.americasnlp-1.2` is an unrelated Choctaw dialogue-system paper.
- Token Cost Inequality uses the official GEM 2026 ACL Anthology record, DOI `10.18653/v1/2026.gem-main.54`.
- RomanUrdu-NLP-Sentiment-Corpus uses the official Hugging Face dataset DOI `10.57967/hf/7931`.
- The post-cutoff paper *One Form to Transfer Them All* (arXiv:2608.25904; submitted 26 August 2026) is not part of the current 67-record evidence set.

## Scope and limitation

This is a structured qualitative review rather than a formal systematic review. Original database exports, deduplication records, and row-level screening decisions were not preserved, so the original evidence curation trail cannot be fully reconstructed from this deposit alone. The retained matrix and audit records are therefore best interpreted as the final, auditable source set used in the manuscript, not as a comprehensive publication database.

## Version

Final technical audit date: **2026-10-07**.

This GitHub directory is public and versioned by Git commits. The manuscript cites a commit-pinned directory URL so the archived S3/S4 version cannot silently move with the default branch. No DOI is assigned to this deposit; the authoritative source is the commit-pinned GitHub directory itself.
