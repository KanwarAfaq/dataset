#!/usr/bin/env python3
"""Submission-grade structural validation for the Roman Urdu survey package.

Checks file/citation/evidence-matrix correspondence, required graphics, controlled
fields, evidence-matrix count labels, and drafting residue. The transcript prints
SHA-256 hashes so a validation result can be tied to exact source files.

This script does not establish statement-to-source validity; that requires source review.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VALIDATOR_VERSION = "2.0"
ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "main.tex"
S1 = ROOT / "S1.tex"
S2 = ROOT / "S2.tex"
BIB = ROOT / "roman_urdu_survey.bib"
S3 = ROOT / "S3_evidence_matrix.csv"
SELF = Path(__file__).resolve()
BASE_REQUIRED_FILES = [MAIN, S1, S2, BIB, S3, ROOT / "wlpeerj.cls"]
TEXT_FILES = [MAIN, S1, S2, BIB, S3, SELF]
HASH_FILES = [MAIN, BIB, S1, S2, S3, SELF]


def bib_keys(text: str) -> list[str]:
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)


def citation_keys(text: str) -> list[str]:
    out: list[str] = []
    for group in re.findall(r"\\cite\w*\s*(?:\[[^\]]*\]\s*)?\{([^}]*)\}", text):
        out.extend(k.strip() for k in group.split(",") if k.strip())
    return out


def graphics_paths(text: str) -> list[str]:
    return [x.strip() for x in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^}]+)\}", text, re.S)]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    main_text = MAIN.read_text(encoding="utf-8") if MAIN.exists() else ""

    graphics = graphics_paths(main_text)
    graphic_files = [ROOT / p for p in graphics]
    required_files = BASE_REQUIRED_FILES + graphic_files
    missing_files = [str(p.relative_to(ROOT)) for p in required_files if not p.exists()]

    bib = bib_keys(BIB.read_text(encoding="utf-8")) if BIB.exists() else []
    bib_dupes = sorted(k for k, c in Counter(bib).items() if c > 1)

    all_citations: list[str] = []
    for p in (MAIN, S1, S2):
        if p.exists():
            all_citations.extend(citation_keys(p.read_text(encoding="utf-8")))
    citation_occurrences = len(all_citations)
    cited = sorted(set(all_citations))
    bibset = set(bib)

    rows: list[dict[str, str]] = []
    if S3.exists():
        with S3.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            rows = list(reader)
    else:
        fields = []

    s3 = [r.get("citation_key", "").strip() for r in rows]
    s3_dupes = sorted(k for k, c in Counter(s3).items() if k and c > 1)
    s3set = set(s3)

    mandatory = (
        "citation_key", "title", "year", "publication_type", "peer_review_status",
        "task", "script_language_scope", "verification_status", "inclusion_rationale",
        "doi_or_url",
    )
    missing_fields = sorted(set(mandatory) - set(fields))
    empty_mandatory: list[str] = []
    for i, row in enumerate(rows, start=2):
        for col in mandatory:
            if col in row and not row[col].strip():
                empty_mandatory.append(f"row {i}:{col}")

    integrity_cols = [c for c in fields if c.startswith("integrity_")]
    invalid_integrity: list[str] = []
    for i, row in enumerate(rows, start=2):
        for col in integrity_cols:
            if row.get(col, "").strip() not in {"Y", "N", "P", "NR", "NA"}:
                invalid_integrity.append(f"row {i}:{col}={row.get(col, '')!r}")

    # Split strings keep the validator from matching its own regex definitions.
    residue_patterns = (
        r"\bTO" + r"DO\b",
        r"\bFIX" + r"ME\b",
        r"\bT" + r"BD\b",
        r"\[citation\s+" + r"needed\]",
        r"\[IN" + r"SERT",
        r"\bPLACE" + r"HOLDER\b",
        r"\bto\s+be\s+" + r"inserted\b",
        r"\bto\s+be\s+" + r"added\b",
        r"\brepository\s+" + r"link\b",
        r"\bactual\s+" + r"doi\b",
        r"\?" + r"\?" + r"\?",
        r"UP" + r"DATE TO:",
        r"\bFI" + r"ND:",
        r"VERIFY " + r"BEFORE SUBMISSION",
        r"CONSULT " + r"S2",
        r"CONSULT " + r"MAIN",
        r"SEE " + r"SOURCE",
        r"SEE " + r"PRIMARY",
        r"DEFAULT " + r"METADATA",
        r"NOT INDEPENDENTLY " + r"TABULATED",
    )
    residue: list[tuple[str, str]] = []
    for p in TEXT_FILES:
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        for pat in residue_patterns:
            if re.search(pat, txt, re.I):
                residue.append((p.name, pat))

    supplement_mentions = [
        x for x in ("S1", "S2", "S3", "S4")
        if not re.search(rf"Supplementary File~?{x}|\b{x}\b", main_text)
    ]

    matrix_n_values = [int(x) for x in re.findall(r"(?:final\s+)?(?:S3\s+)?evidence matrix\s*\(n=(\d+)\)", main_text, re.I)]
    matrix_count_mismatches = [f"main n={n}, S3 rows={len(rows)}" for n in matrix_n_values if n != len(rows)]

    repo_statement_issue = []
    if MAIN.exists() and "public versioned GitHub directory" in main_text:
        if not re.search(r"https://github\.com/[^}\s]+/tree/[0-9a-f]{40}/[^}\s]+", main_text, re.I):
            repo_statement_issue.append("Data Availability claims a versioned GitHub directory but does not use a commit-pinned 40-hex URL")

    count_mismatch = [] if len(bib) == len(rows) else [f"bibliography={len(bib)}, S3={len(rows)}"]

    checks = {
        "missing required files/graphics": missing_files,
        "duplicate BibTeX keys": bib_dupes,
        "citations missing from BibTeX": sorted(set(cited) - bibset),
        "BibTeX records not cited in manuscript/supplements": sorted(bibset - set(cited)),
        "BibTeX records missing from S3": sorted(bibset - s3set),
        "S3 keys absent from BibTeX": sorted(s3set - bibset),
        "duplicate S3 citation keys": s3_dupes,
        "missing mandatory S3 columns": missing_fields,
        "empty mandatory S3 fields": empty_mandatory,
        "invalid integrity controlled values": invalid_integrity,
        "supplements not mentioned in main.tex": supplement_mentions,
        "evidence-matrix n= count mismatches": matrix_count_mismatches,
        "bibliography/S3 total-count mismatch": count_mismatch,
        "versioned repository statement": repo_statement_issue,
        "drafting residue (including S4 itself)": residue,
    }

    print(f"S4 validator version: {VALIDATOR_VERSION}")
    print(f"Validation timestamp (UTC): {timestamp}")
    print("SHA-256 source hashes:")
    for p in HASH_FILES:
        if p.exists():
            print(f"  {sha256(p)}  {p.name}")
        else:
            print(f"  MISSING  {p.name}")

    print(f"BibTeX records: {len(bib)}")
    print(f"Citation occurrences across main/S1/S2: {citation_occurrences}")
    print(f"Unique citation keys across main/S1/S2: {len(cited)}")
    print(f"S3 evidence rows: {len(rows)}")
    print(f"Graphics referenced by main.tex: {len(graphics)}")

    publication_type_counts = Counter(r.get("publication_type", "").strip() for r in rows)
    peer_status_counts = Counter(r.get("peer_review_status", "").strip() for r in rows)
    print("S3 publication_type counts (controlled values):")
    for label, count in sorted(publication_type_counts.items()):
        print(f"  {label}: {count}")
    print("S3 peer_review_status counts (controlled values):")
    for label, count in sorted(peer_status_counts.items()):
        print(f"  {label}: {count}")

    normalized_source_counts = Counter()
    for r in rows:
        status = r.get("peer_review_status", "").strip().lower()
        if status.startswith("peer-reviewed journal"):
            normalized_source_counts["Peer-reviewed journal/review article"] += 1
        elif status == "peer-reviewed conference/workshop paper":
            normalized_source_counts["Peer-reviewed conference/workshop paper"] += 1
        elif status == "retracted proceedings paper":
            normalized_source_counts["Retracted proceedings paper"] += 1
        elif status == "preprint; not peer reviewed":
            normalized_source_counts["Preprint/technical report"] += 1
        elif "card" in status:
            normalized_source_counts["Dataset/model card"] += 1
        elif "repository" in status or "resource record" in status:
            normalized_source_counts["Repository/resource record"] += 1
        elif status == "scholarly book":
            normalized_source_counts["Scholarly book"] += 1
        else:
            normalized_source_counts[f"Other: {r.get('peer_review_status', '').strip()}"] += 1
    print("S3 normalized source-type counts (derived from peer_review_status):")
    for label, count in sorted(normalized_source_counts.items()):
        print(f"  {label}: {count}")
    print(f"  TOTAL: {sum(normalized_source_counts.values())}")

    failed = False
    print("Check results:")
    for name, value in checks.items():
        status = "FAIL" if value else "PASS"
        print(f"  [{status}] {name}: {value if value else 'none'}")
        failed |= bool(value)

    if failed:
        print("VALIDATION: FAIL")
        return 1
    print("VALIDATION: PASS")
    print("Scope: structural correspondence only; statement-to-source validity requires source review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
