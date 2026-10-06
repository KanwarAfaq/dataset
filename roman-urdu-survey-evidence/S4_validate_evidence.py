#!/usr/bin/env python3
"""Structural validation for the final Roman Urdu survey package.

This script checks file/citation/evidence-matrix correspondence and drafting residue.
It does not establish statement-to-source validity.
"""
from __future__ import annotations
import csv, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "main.tex"
S1 = ROOT / "S1.tex"
S2 = ROOT / "S2.tex"
BIB = ROOT / "roman_urdu_survey.bib"
S3 = ROOT / "S3_evidence_matrix.csv"
FIGURES = [
    ROOT / "material" / "review_methodology_process_flowchart.png",
    ROOT / "material" / "evidence_taxonomy.png",
]
REQUIRED_FILES = [MAIN, S1, S2, BIB, S3, ROOT / "wlpeerj.cls", *FIGURES]
TEXT_FILES = [MAIN, S1, S2, BIB, S3]


def bib_keys(text: str):
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)


def citation_keys(text: str):
    out=[]
    for group in re.findall(r"\\cite\w*\s*(?:\[[^\]]*\]\s*)?\{([^}]*)\}", text):
        out.extend(k.strip() for k in group.split(",") if k.strip())
    return out


def main():
    missing_files=[str(p.relative_to(ROOT)) for p in REQUIRED_FILES if not p.exists()]
    bib=bib_keys(BIB.read_text(encoding="utf-8")) if BIB.exists() else []
    bib_dupes=sorted(k for k,c in Counter(bib).items() if c>1)
    cited=[]
    for p in (MAIN,S1,S2):
        if p.exists(): cited.extend(citation_keys(p.read_text(encoding="utf-8")))
    cited=sorted(set(cited))
    bibset=set(bib)
    rows=[]
    if S3.exists():
        with S3.open(newline="",encoding="utf-8-sig") as f:
            reader=csv.DictReader(f); fields=reader.fieldnames or []; rows=list(reader)
    else:
        fields=[]
    s3=[r.get("citation_key","").strip() for r in rows]
    s3_dupes=sorted(k for k,c in Counter(s3).items() if k and c>1)
    s3set=set(s3)
    mandatory=("citation_key","title","year","publication_type","peer_review_status","task","script_language_scope","verification_status","inclusion_rationale","doi_or_url")
    missing_fields=sorted(set(mandatory)-set(fields))
    empty_mandatory=[]
    for i,row in enumerate(rows,start=2):
        for col in mandatory:
            if col in row and not row[col].strip(): empty_mandatory.append(f"row {i}:{col}")
    integrity_cols=[c for c in fields if c.startswith("integrity_")]
    invalid_integrity=[]
    for i,row in enumerate(rows,start=2):
        for col in integrity_cols:
            if row.get(col,"").strip() not in {"Y","N","P","NR","NA"}:
                invalid_integrity.append(f"row {i}:{col}={row.get(col,'')!r}")
    residue_patterns=(
        r"\bTO"+r"DO\b", r"\bFIX"+r"ME\b", r"\bT"+r"BD\b", r"\[citation "+r"needed\]",
        r"\[IN"+r"SERT", r"\bPLACE"+r"HOLDER\b", r"UP"+r"DATE TO:", r"\bFI"+r"ND:",
        r"VERIFY "+r"BEFORE SUBMISSION", r"CONSULT "+r"S2", r"CONSULT "+r"MAIN",
        r"SEE "+r"SOURCE", r"SEE "+r"PRIMARY", r"DEFAULT "+r"METADATA",
        r"NOT INDEPENDENTLY "+r"TABULATED"
    )
    residue=[]
    for p in TEXT_FILES:
        if not p.exists(): continue
        txt=p.read_text(encoding="utf-8")
        for pat in residue_patterns:
            if re.search(pat,txt,re.I): residue.append((p.name,pat))
    main_text=MAIN.read_text(encoding="utf-8") if MAIN.exists() else ""
    supplement_mentions=[x for x in ("S1","S2","S3","S4") if not re.search(rf"Supplementary File~?{x}|\b{x}\b",main_text)]
    checks={
        "missing required files":missing_files,
        "duplicate BibTeX keys":bib_dupes,
        "citations missing from BibTeX":sorted(set(cited)-bibset),
        "BibTeX records not cited in manuscript/supplements":sorted(bibset-set(cited)),
        "BibTeX records missing from S3":sorted(bibset-s3set),
        "S3 keys absent from BibTeX":sorted(s3set-bibset),
        "duplicate S3 citation keys":s3_dupes,
        "missing mandatory S3 columns":missing_fields,
        "empty mandatory S3 fields":empty_mandatory,
        "invalid integrity controlled values":invalid_integrity,
        "supplements not mentioned in main.tex":supplement_mentions,
        "drafting residue":residue,
    }
    print(f"BibTeX records: {len(bib)}")
    print(f"Unique citation keys across main/S1/S2: {len(cited)}")
    print(f"S3 evidence rows: {len(rows)}")
    failed=False
    for name,value in checks.items():
        print(f"{name}: {value if value else 'none'}")
        failed |= bool(value)
    if len(bib)!=len(rows):
        print(f"count mismatch: bibliography={len(bib)}, S3={len(rows)}"); failed=True
    if failed:
        print("VALIDATION: FAIL"); return 1
    print("VALIDATION: PASS")
    print("Scope: structural correspondence only; statement-to-source validity requires source review.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
