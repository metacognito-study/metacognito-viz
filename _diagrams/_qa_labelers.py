#!/usr/bin/env python3
"""Mechanical QA gate for agy-built labeler diagrams. Run AFTER the agy batches finish.
Checks per row: files exist, XML valid, viewBox exact, coords integrity (ids/labels/order match authored,
bounds, pairwise separation), answer-leak grep. Renders every SVG to PNG for the human visual gate."""
import json, os, re, subprocess, sys
import xml.dom.minidom as MD

EP = "/Users/work/Documents/Claude/Projects/Economics Project"
OUT = EP + "/_align/_pending_push/metacognito-viz/_diagrams"
PNG = "/tmp/labeler_qa_png"
auth = {t["row"]: t for t in json.load(open("/tmp/labelers.json"))}
os.makedirs(PNG, exist_ok=True)

def leak_ok(label, svgtext):
    """Answer must not appear. Bracketed stimulus is allowed: strip '(...)' and test the head phrase."""
    head = re.sub(r"\s*\(.*\)$", "", label).strip()
    return head.lower() not in svgtext.lower()

report, hard_fail = [], 0
for row, t in sorted(auth.items()):
    svg = f"{OUT}/{t['svgKey']}.svg"; cj = f"/tmp/labeler_coords/{row}.json"
    probs = []
    if not os.path.exists(svg): report.append((row, ["SVG MISSING"])); hard_fail += 1; continue
    if not os.path.exists(cj):  probs.append("COORDS MISSING")
    try:
        doc = MD.parse(svg)
        vb = doc.documentElement.getAttribute("viewBox").split()
        if [round(float(v)) for v in vb] != [0, 0, 480, 320]: probs.append(f"viewBox={vb}")
        svgtext = " ".join(n.firstChild.nodeValue for n in doc.getElementsByTagName("text") if n.firstChild)
    except Exception as e:
        report.append((row, [f"XML FAIL {e}"])); hard_fail += 1; continue
    if os.path.exists(cj):
        try:
            c = json.load(open(cj))["hotspots"]; a = t["hotspots"]
            if [h["id"] for h in c] != [h["id"] for h in a]: probs.append("ID MISMATCH")
            if [h["label"] for h in c] != [h["label"] for h in a]: probs.append("LABEL MISMATCH")
            for h in c:
                if not (0.05 <= h["x"] <= 0.95 and 0.07 <= h["y"] <= 0.93): probs.append(f"OOB {h['id']}")
            for i in range(len(c)):
                for j in range(i+1, len(c)):
                    if abs(c[i]["x"]-c[j]["x"]) < 0.13 and abs(c[i]["y"]-c[j]["y"]) < 0.15:
                        probs.append(f"TOO CLOSE {c[i]['id']}/{c[j]['id']}")
        except Exception as e: probs.append(f"COORDS BAD {e}")
    for h in t["hotspots"]:
        if not leak_ok(h["label"], svgtext): probs.append(f"LEAK '{h['label'][:24]}'")
    subprocess.run(["qlmanage","-t","-s","520","-o",PNG,svg], capture_output=True)
    if probs: hard_fail += 1
    report.append((row, probs or ["OK"]))

print(f"{'ROW':>6}  RESULT")
for row, probs in report: print(f"{row:>6}  {'; '.join(probs)}")
print(f"\nTOTAL {len(report)} | clean {len(report)-hard_fail} | flagged {hard_fail}")
pngs = [f for f in os.listdir(PNG) if f.endswith(".png")]
print(f"PNGs rendered for visual gate: {len(pngs)} -> {PNG}")
sys.exit(1 if hard_fail else 0)
