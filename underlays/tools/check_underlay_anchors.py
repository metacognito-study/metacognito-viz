#!/usr/bin/env python3
"""Detect underlay ROW-DRIFT before it silently breaks the app.

WHY: registry bindings are keyed by SHEET ROW NUMBER. When LO rows are inserted or
split (e.g. the one-outcome-granularity campaigns), every binding below the insert
point silently points at the WRONG learning objective - a draw-scaffold ends up on a
"calculate" LO or a section header, and the student gets a diagram that doesn't match
the task. This is invisible: nothing errors, the asset still renders.

FIX: each entry carries a `stem_anchor` = the LO stem text captured when the binding
was verified. This tool re-reads the LIVE stems and flags any entry whose anchor no
longer matches the stem at its row. Row drift becomes a RED GATE instead of silent rot.

Usage:
  python3 check_underlay_anchors.py registry.json stems.json [--strict]
    stems.json = {"econ": {"74": "label real and money flows...", ...}, "chem": {...}}
    exit 0 = no drift; exit 1 = drift found (or unanchored entries under --strict)

Producing stems.json: any session with Sheets access dumps column C for the bound
rows. Re-run this after ANY campaign that inserts/splits/deletes LO rows.
"""
import json, re, sys

def norm(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip().lower().rstrip('.')

def main():
    if len(sys.argv) < 3:
        print(__doc__); return 2
    reg = json.load(open(sys.argv[1])); stems = json.load(open(sys.argv[2]))
    strict = '--strict' in sys.argv
    drift, unanchored, ok = [], [], 0
    for e in reg.get("entries", []):
        sh, row, asset = e.get("sheet"), e.get("row"), e.get("asset")
        anchor = e.get("stem_anchor")
        live = (stems.get(sh) or {}).get(str(row))
        if not anchor:
            unanchored.append((sh, row, asset)); continue
        if live is None:
            continue                      # stem not in this export - can't judge
        if norm(anchor) == norm(live): ok += 1
        else: drift.append((sh, row, asset, anchor, live))
    print(f"anchored-OK={ok}  DRIFT={len(drift)}  unanchored={len(unanchored)}")
    for sh, row, asset, a, l in drift:
        print(f"\n  DRIFT {sh} row {row}  {asset}")
        print(f"    anchored to : {a[:88]}")
        print(f"    live stem is: {l[:88]}")
    if unanchored and strict:
        print(f"\n  UNANCHORED (strict): {len(unanchored)} entries lack stem_anchor")
        for sh, row, asset in unanchored[:20]: print(f"    {sh} {row} {asset}")
    if drift: return 1
    if unanchored and strict: return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
