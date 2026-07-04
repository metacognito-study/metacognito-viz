# UNDERLAY CORPUS — CLOSING DOCUMENT
Lane ELENA2_67 (ELENA-6/7 merged surveyor+producer → ELENA-67B continuation). Closed 2026-07-04.
Sheets: chem `1jZ…` / econ `1Fn…`, tab `My Checklist`. Wiring: orchestrator #108, registry-driven (CDN publish). This lane made zero Sheet writes, app edits, deploys, or commits.

## Totals
**112 registry entries · 112 hand-authored SVGs** (+ `_validate_batch1.py` structural gate, `_gen_batch1.py` batch-1 generator, `registry.json`). ~190 total row-placements counting `serves` reuse.

| batch | assets | scope |
|---|---|---|
| 1 | 21 | owner's non-negotiable classes: galvanic/filtration/M-B/mass-spec label tasks, particulate completion, partial Lewis, equilibrium/PE/M-B axes pads, econ circular-flow + shift + P-Q/PPC families |
| 2 | 25 | PES pair, Lewis skeletons e2–e5, u_335, distillation, particle 5-panel, titration/heating/P-t/[A]-t axes, econ 5-sector + S&D-unmarked + Laffer/step/2×2/sort/table/world-price families |
| 3 | 13 | shown-state curves: heating/cooling, KNO₃ solubility, 1-/2-/3-step PE, SA-SB/WA-SB/WB-SA/overlay titrations, A⇌B/NH₃/HI approach |
| 4 | 26 | IMF particulate 8-set, Morse pair, Beer-Lambert 6-set, Ksp 4-set, electrochem particulate 6-set |
| 5 | 16 | Ksp log-axis pair (ruling), kinetics 5-set (given-label variants + M-B/Ea), acid/gas particulates, half-equivalence-marked titrations, econ chain/number-line/trade-flow skeletons |
| 6 | 11 | equilibrium variants (approach/Δ-ratio/P-t/stress/snapshots/data tables ×2), titration 4-panel particulate trio |

## Leak discipline (every asset has a recorded `answer_leak_check` in registry.json)
Pads: the missing part IS the exercise (blank boxes/axes; no answer geometry). Shown-states: full given geometry drawn, but every feature the task asks the student to locate/name/label is deliberately absent. Deliberate contrasts: u_1691 (migration arrows = the given) vs u_1699 (no arrows = the question).

## Exclusions
- **Row 1640 — REGISTRY-EXCLUDED** (coordinator-ruled leak review): its cell-described figure is a Zn/Cu cell WITH anode/cathode labels + e⁻-flow arrow — the verbatim answer key to u_1624's label task on identical chemistry two rows away. Row remains serviceable as prose.

## Flagged judgment calls & self-chosen values (all noted per-entry in registry.json)
- u_1468: Qsp/Ksp regions carry math labels only; the cell's English verdicts (supersaturated/precipitates) withheld as the task's second half.
- u_652: calibration scale self-chosen for a clean A=0.45 → 4.5×10⁻⁴ M read (cell figure generic).
- u_1126 / u_1133 plateaus and u_1169 table values: self-chosen but stoichiometry-exact (1:3:2 and 1:2); starts verbatim.
- u_1467: log-axis ruling applied on a 2-decade window (8 decades would hide the factor-2 drop) — coordinator-approved interpretation.
- u_86: Athletic-Country schedule left blank — the full A–F data is NOT in the Sheet (X86 reveals only B/C); nothing fabricated.
- u_1189: one ionized pair drawn "for visibility" with an honesty caption against the <1% given.

## Residuals — spec'd but not yet built (survey is CLOSED; no unspec'd rows remain)
Per-row figure descriptions for all of these live verbatim in the persisted `[Open` enumeration and are clustered in `../VISUAL_PLACEMENT_MAP.md` §E; a successor can build them mechanically in house style:
1. **Equilibrium numeric shown-state variants:** 1134 (N₂O₄⇌2NO₂ P-t), 1135 (SO₂/O₂/SO₃ P-t), 1137 (ΔP-ratio read), 1138 (PCl₅ P-t), 1155 J+L (simultaneous-jump / product-drop stress graphs), 1156 (NH₃-removed stress).
2. **A5 ≤635 shown-state remainder, CHAPTER-ASCENDING (coordinator ruling):** 80 · 115 · 125 · 140 · 158 · 159 · 203 · 204 · 248 · 250 · 272 · 273 · 277 · 343 · 355 · 368 · 377 · 384 · 397 · 402 · 491 · 510 · 512–517 · 621 · 622 · 645. (658 built in batch 4.)
3. **Wiring-time follow-ups:** K–N-column spot-checks of mapped rows (map §Method); u_1405-family 1407–1415 example-col hooks unverified (serves trimmed accordingly).
4. **Out of this lane's scope by design:** viz-link interactives (`_pending_push/metacognito-viz/`, publish pending) and video-link clips (Krug/Nasser lane, owner-gated).

## QA regime (applied to every batch)
`_validate_batch1.py`: XML well-formed · all coordinates in-viewBox · only allowed theme tokens, each with literal fallback · every text haloed · registry↔files consistent. Render gate: rsvg-convert @480px on var()-resolved copies, visual inspection of every distinct geometry (parameter variants honestly noted), **all rasters deleted after inspection**. Defects caught by the render gate across the program: 2 in batch 1 (label collisions), 1 in batch 4 (u_794 induced-dipole orientation) — all fixed and re-verified.
