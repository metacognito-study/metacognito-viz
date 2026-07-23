# Labeler Opportunity Research

## Evidence Block

Based on the live microtask data (`microtask_byrow.json`):
- Total items: 213 (All chemistry)
- Sorter tasks: 129
- Sequencer tasks: 36
- Matcher tasks: 16
- Labeler tasks: 32

Repository state:
- ~65 SVG figures currently exist across `_diagrams/`.
- No economics content is active in the live sheet.

---

## Category A: Tool Conversion Proposals (Chemistry)

These rows currently use text-based sorting/sequencing but fundamentally test visual concepts that are better served by a diagram labeler.

1. **Row 1037: Identify Equilibrium from a Table**
   - **Current Tool:** Sorter ("At equilibrium" vs "Not at equilibrium")
   - **Why Labeler:** Seeing a concentration-time table and pointing to the row where values stabilize tests the skill more directly than matching text descriptions.
   - **Figure:** A data table showing Time vs. [Reactant] and [Product] with 4-5 rows.
   - **Hotspots:** Initial state (t=0 row), Reaching equilibrium (values changing row), At equilibrium (first row where values stabilize), Equilibrium maintained (subsequent flat rows).
   - **Distractors:** Reversal point, Equivalence point, Maximum rate.
   - **Misconception:** Students often confuse "concentrations equal" with "concentrations constant".

2. **Row 1588: Integrated Rate Law Graphs**
   - **Current Tool:** Sorter (Zero order, First order, Second order)
   - **Why Labeler:** Students need to visually identify the linear plot for each order rather than reading text descriptions like "linear ln[A] vs t".
   - **Figure:** Three side-by-side graphs: [A] vs t, ln[A] vs t, and 1/[A] vs t (showing straight lines).
   - **Hotspots:** Zero Order (on [A] vs t), First Order (on ln[A] vs t), Second Order (on 1/[A] vs t).
   - **Distractors:** Equilibrium, Catalyst added, Third Order, Inverse Order.
   - **Misconception:** Forgetting which axis transformation yields a straight line for which order.

3. **Row 1623: Exo vs Endo Potential Energy Diagrams**
   - **Current Tool:** Sorter (Exothermic vs Endothermic)
   - **Why Labeler:** Reading "Products lower on E diagram" is less effective than clicking the actual regions on a potential energy diagram.
   - **Figure:** Two potential energy profiles, one exothermic (products lower), one endothermic (products higher).
   - **Hotspots:** Exothermic profile, Endothermic profile, Activation Energy (Ea), Enthalpy change (ΔH).
   - **Distractors:** Kinetic energy, Temperature, Intermediate, Catalyst.
   - **Misconception:** Reversing the definitions of exo/endo on a graph and misidentifying activation energy vs enthalpy.

4. **Row 876: Heating Curves (Phases vs Temperature Change)**
   - **Current Tool:** Sorter (Temperature changing vs Phase change)
   - **Why Labeler:** Clicking on the sloped and flat regions of a heating curve is the standard way this is tested.
   - **Figure:** A standard heating curve (Temp vs Heat added) from solid to gas.
   - **Hotspots:** Solid heating (first slope), Melting (first plateau), Liquid heating (second slope), Boiling (second plateau).
   - **Distractors:** Sublimation, Deposition, Activation energy, Supercooling.
   - **Misconception:** Thinking temperature increases during a phase change.

5. **Row 995: Concentration-Time Curves (Equilibrium)**
   - **Current Tool:** Sorter (At equilibrium vs Not at equilibrium)
   - **Why Labeler:** Identifying the exact point on a graph where curves go flat is a direct visual skill.
   - **Figure:** Concentration vs Time graph showing reactants decreasing and products increasing until they flatten out.
   - **Hotspots:** Kinetic region (curves changing), Equilibrium established (point of flattening), Reactant line, Product line.
   - **Distractors:** Equivalence point, Reaction stops, Q > K, Rate = 0.
   - **Misconception:** Thinking equilibrium means the reactant and product lines must cross or be equal.

6. **Row 1403: Standard Cell Potential (E°cell)**
   - **Current Tool:** Sorter (E° > 0 occurs vs E° < 0 no rxn)
   - **Why Labeler:** Labeling a standard reduction potential table (like a miniature one) to show which combination is spontaneous.
   - **Figure:** A miniature table with two half-reactions and their E° values.
   - **Hotspots:** Cathode half-reaction (higher E°), Anode half-reaction (lower E°), Spontaneous cell E° calculation formula.
   - **Distractors:** Non-spontaneous, Electrolytic, Equilibrium.
   - **Misconception:** Misidentifying which species is reduced/oxidized based on E° values.

7. **Row 1444: Galvanic vs Electrolytic Cells**
   - **Current Tool:** Sorter (Galvanic vs Electrolytic)
   - **Why Labeler:** Pointing to the key differences (battery vs voltmeter) on a diagram is more effective.
   - **Figure:** Two cell diagrams side-by-side, one galvanic (with voltmeter/load), one electrolytic (with power source).
   - **Hotspots:** Galvanic Cell (ΔG < 0), Electrolytic Cell (ΔG > 0), Power Source (driving non-spontaneous rxn), Voltmeter.
   - **Distractors:** Salt bridge, Anode, Cathode, Equivalence point.
   - **Misconception:** Failing to distinguish between cells that generate voltage vs those that require it.

8. **Row 9: Scientific Method Steps**
   - **Current Tool:** Sequencer (Make observation, form hypothesis, etc.)
   - **Why Labeler:** A flowchart diagram is a great way to visualize this cyclic process.
   - **Figure:** A flowchart of the scientific method with blank boxes.
   - **Hotspots:** Observation, Hypothesis, Experiment, Data Analysis, Conclusion.
   - **Distractors:** Publication, Theory, Law, Variable.
   - **Misconception:** Thinking the scientific method is a strictly linear process.

9. **Row 105: Ionic vs Covalent Compounds (Particulate)**
   - **Current Tool:** Sorter (Ionic vs Covalent)
   - **Why Labeler:** Particle diagrams showing a lattice vs distinct molecules are classic AP Chem visuals.
   - **Figure:** Two particle diagrams: a 3D alternating charge lattice (ionic) and discrete groups of nonmetal atoms (covalent).
   - **Hotspots:** Ionic lattice (continuous network), Covalent molecules (discrete units), Cation, Anion.
   - **Distractors:** Metallic sea of electrons, Network covalent, Alloy.
   - **Misconception:** Confusing continuous ionic lattices with discrete covalent molecules.

10. **Row 912: Acids and Bases**
    - **Current Tool:** Sorter (Acid vs Base)
    - **Why Labeler:** Can use a particulate diagram showing proton transfer.
    - **Figure:** A reaction diagram showing HA + B -> A- + HB+.
    - **Hotspots:** Acid (proton donor), Base (proton acceptor), Conjugate Base, Conjugate Acid.
    - **Distractors:** Spectator ion, Catalyst, Precipitate, Hydronium.
    - **Misconception:** Confusing the roles of Bronsted-Lowry acids and bases.

---

## Category B: Diagram Gaps (No Labeler Yet)

### Chemistry

11. **Row TBD: Born-Haber Cycle**
    - **Figure:** A step-by-step energy diagram for forming an ionic solid (e.g., NaCl) from its elements.
    - **Hotspots:** Sublimation of metal, Ionization energy of metal, Bond dissociation of nonmetal, Electron affinity of nonmetal, Lattice energy.
    - **Distractors:** Hydration energy, Activation energy, Enthalpy of solution, Equilibrium.
    - **Misconception:** Confusing the signs and definitions of the individual steps (e.g., lattice energy vs enthalpy of formation).

12. **Row TBD: Mass Spectrometry**
    - **Figure:** A bar graph showing relative abundance vs m/z for an element with isotopes (e.g., Cl or Mg).
    - **Hotspots:** Most abundant isotope, Least abundant isotope, Average atomic mass estimate, m/z axis (mass).
    - **Distractors:** Atomic number axis, Number of protons, Ionization energy, Binding energy.
    - **Misconception:** Confusing individual isotope masses with the weighted average atomic mass.

13. **Row TBD: Photoelectron Spectroscopy (PES)**
    - **Figure:** A PES spectrum (Relative number of electrons vs Binding Energy) for an element like Oxygen or Magnesium.
    - **Hotspots:** 1s peak (highest binding E), Valence shell peaks (lowest binding E), Core electrons, Axis indicating Binding Energy.
    - **Distractors:** Kinetic energy, Number of protons, Ionization energy, Wavelength.
    - **Misconception:** Reading the binding energy axis backwards (highest energy is usually on the left, closest to nucleus).

14. **Row TBD: VSEPR Geometries**
    - **Figure:** 3D representations of common molecular geometries (Linear, Bent, Trigonal Planar, Tetrahedral).
    - **Hotspots:** Linear (180°), Bent (<120° or <109.5°), Trigonal Planar (120°), Tetrahedral (109.5°).
    - **Distractors:** Trigonal Bipyramidal, Octahedral, Square Planar, T-shaped.
    - **Misconception:** Forgetting the impact of lone pairs on bond angles (e.g., Bent vs Linear).

15. **Row TBD: Paper Chromatography**
    - **Figure:** A piece of chromatography paper dipped in solvent, with distinct spots separated vertically.
    - **Hotspots:** Solvent front, Origin line, Most polar spot (if polar stationary phase), Least polar spot.
    - **Distractors:** Mobile phase, Stationary phase, Equivalence point, Catalyst.
    - **Misconception:** Misinterpreting Rf values and how intermolecular forces determine separation.

16. **Row TBD: Hybridization**
    - **Figure:** A central atom showing sp, sp2, and sp3 hybridized orbitals in distinct molecules (e.g., ethyne, ethene, ethane).
    - **Hotspots:** sp hybridization (linear), sp2 hybridization (trigonal planar), sp3 hybridization (tetrahedral), unhybridized p-orbital (pi bond).
    - **Distractors:** sp3d, sp3d2, sigma bond, lone pair.
    - **Misconception:** Failing to associate steric number with hybridization state.

17. **Row TBD: Intermolecular Forces (Particulate)**
    - **Figure:** Diagram showing molecules interacting (e.g., water molecules H-bonding, nonpolar molecules with LDFs).
    - **Hotspots:** Hydrogen bond (dashed line between molecules), Covalent bond (solid line within molecule), Dipole-dipole interaction, London dispersion forces.
    - **Distractors:** Ionic bond, Metallic bond, Network covalent, Ion-dipole.
    - **Misconception:** Confusing intramolecular bonds with intermolecular forces.

18. **Row TBD: Atomic Emission Spectra**
    - **Figure:** Energy level diagram of a hydrogen atom showing electron transitions.
    - **Hotspots:** Absorption (arrow pointing up), Emission (arrow pointing down), Highest energy photon (longest arrow), Lowest energy photon (shortest arrow).
    - **Distractors:** Ionization, Ground state, Excited state, Wavelength.
    - **Misconception:** Associating longer transitions with longer wavelengths (instead of higher energy/shorter wavelength).

19. **Row TBD: Vapor Pressure Curves**
    - **Figure:** Graph of Vapor Pressure vs Temperature for various liquids.
    - **Hotspots:** Normal boiling point (at 1 atm), Most volatile liquid (steepest curve/lowest BP), Strongest IMFs (highest BP).
    - **Distractors:** Melting point, Critical point, Triple point, Sublimation.
    - **Misconception:** Failing to relate vapor pressure to intermolecular force strength.

20. **Row TBD: Reaction Mechanisms**
    - **Figure:** A multi-step reaction profile (Energy vs Reaction Coordinate) with two humps.
    - **Hotspots:** Rate-determining step (highest peak), Intermediate (valley), Reactants, Products.
    - **Distractors:** Catalyst, Transition state, Activation energy, Enthalpy.
    - **Misconception:** Identifying the overall highest point as the slow step, rather than the step with the largest activation energy.

### Economics

21. **Row TBD: Production Possibilities Curve (PPC)**
    - **Figure:** A bowed-out PPC curve showing points inside, on, and outside the curve.
    - **Hotspots:** Efficient point (on curve), Inefficient point (inside curve), Unattainable point (outside curve), Increasing opportunity cost (bowed shape).
    - **Distractors:** Constant opportunity cost, Economic growth, Recession, Inflation.
    - **Misconception:** Thinking points inside the curve are efficient or unattainable.

22. **Row TBD: Supply and Demand Market Equilibrium**
    - **Figure:** Standard intersecting upward S and downward D curves.
    - **Hotspots:** Equilibrium Price (Pe), Equilibrium Quantity (Qe), Supply curve, Demand curve.
    - **Distractors:** Price ceiling, Price floor, Shortage, Surplus.
    - **Misconception:** Confusing shifts in the curve with movements along the curve.

23. **Row TBD: Market Surplus and Shortage**
    - **Figure:** S & D graph showing horizontal lines above (surplus) and below (shortage) equilibrium.
    - **Hotspots:** Price Floor (above Pe), Price Ceiling (below Pe), Area of Surplus, Area of Shortage.
    - **Distractors:** Consumer surplus, Producer surplus, Equilibrium, Deadweight loss.
    - **Misconception:** Thinking price ceilings go above equilibrium (they are effective *below*).

24. **Row TBD: Elastic vs Inelastic Demand Curves**
    - **Figure:** Two demand curves side-by-side, one steep (inelastic) and one flat (elastic).
    - **Hotspots:** Inelastic demand (steep), Elastic demand (flat), Perfectly elastic (horizontal), Perfectly inelastic (vertical).
    - **Distractors:** Unit elastic, Supply, Revenue, Cost.
    - **Misconception:** Confusing the slope of the curve with elasticity.

25. **Row TBD: Perfect Competition Firm (Short Run)**
    - **Figure:** Side-by-side Market graph and Firm graph (MR=D=AR=P line, MC curve, ATC curve).
    - **Hotspots:** Profit-maximizing quantity (MC=MR), Break-even point (MC=ATC), Shutdown point (MC=AVC), Economic profit area.
    - **Distractors:** Loss area, Monopoly, Oligopoly, Allocative efficiency.
    - **Misconception:** Maximizing profit where revenue is highest rather than where MR = MC.

26. **Row TBD: Monopoly Market Structure**
    - **Figure:** Downward sloping Demand, steeper MR, U-shaped ATC, swoosh MC.
    - **Hotspots:** Profit-maximizing Q (MR=MC), Profit-maximizing P (up to Demand), Deadweight loss area, Economic profit area.
    - **Distractors:** Allocative efficiency, Productive efficiency, Perfect competition, Shutdown point.
    - **Misconception:** Setting price where MR=MC rather than going up to the demand curve.

27. **Row TBD: Aggregate Demand / Aggregate Supply (AD/AS)**
    - **Figure:** Macroeconomic model with AD, SRAS, and LRAS curves.
    - **Hotspots:** Full employment output (LRAS), Recessionary gap (equilibrium left of LRAS), Inflationary gap (equilibrium right of LRAS), Price Level axis.
    - **Distractors:** Real GDP, Micro supply/demand, Interest rate, Money supply.
    - **Misconception:** Confusing the macro AD/AS axes (Price Level, Real GDP) with micro axes (Price, Quantity).

28. **Row TBD: Money Market Graph**
    - **Figure:** Vertical Money Supply (MS) curve and downward sloping Money Demand (MD) curve.
    - **Hotspots:** Nominal Interest Rate axis, Quantity of Money axis, Equilibrium interest rate, Shift in MS (expansionary policy).
    - **Distractors:** Real interest rate, Investment, Aggregate demand, Price level.
    - **Misconception:** Confusing the Money Market (nominal rates, Fed policy) with Loanable Funds (real rates, savings/borrowing).

29. **Row TBD: The Business Cycle**
    - **Figure:** A wavy line oscillating around a straight long-term growth trend line.
    - **Hotspots:** Peak, Trough, Expansion/Recovery, Contraction/Recession.
    - **Distractors:** Inflation, Unemployment, Stagflation, Deficit.
    - **Misconception:** Thinking the trend line represents actual GDP rather than potential GDP.

30. **Row TBD: Phillips Curve (Short Run and Long Run)**
    - **Figure:** Downward sloping SRPC and vertical LRPC.
    - **Hotspots:** Natural Rate of Unemployment (LRPC), High inflation / low unemployment point, Stagflation shift (SRPC shifts right), Expected inflation rate.
    - **Distractors:** Deflation, Economic growth, Aggregate demand, Aggregate supply.
    - **Misconception:** Failing to relate shifts in SRPC to shifts in SRAS.

---

## Category C: Table Tasks ("Predict the Direction of Change")

These grid-based labelers require determining increases/decreases/no change for multiple variables under a specific scenario, effectively testing holistic understanding.

31. **Row TBD: Le Chatelier's Principle (Multiple Scenarios)**
    - **Figure:** A table with scenarios as rows (e.g., Increase Temp, Decrease Vol, Add Reactant) and columns for [Reactant], [Product], and K.
    - **Hotspots:** Every cell is a hotspot to predict how that variable changes (Increases/Decreases/No Change).
    - **Distractors:** Shifts left, Shifts right, Equilibrium.
    - **Misconception:** Thinking that adding a solid shifts equilibrium or that K changes with pressure/concentration.

32. **Row TBD: Buffer Solution Additions**
    - **Figure:** A table showing a buffer system. Rows: Add strong acid, Add strong base, Dilute with water. Columns: pH, [HA], [A-].
    - **Hotspots:** Cells predict changes in pH (slight decrease/slight increase/no change) and species concentrations.
    - **Distractors:** Drastic change, Neutralizes, Shifts left.
    - **Misconception:** Assuming pH doesn't change at all when acid/base is added to a buffer.

33. **Row TBD: Macroeconomic Fiscal Policy Effects**
    - **Figure:** A table for scenarios: Increase Govt Spending, Decrease Taxes. Columns: Aggregate Demand, Price Level, Real GDP, Unemployment.
    - **Hotspots:** Predict Increases/Decreases/No Change for each macroeconomic indicator.
    - **Distractors:** Shifts left, Shifts right, Inelastic.
    - **Misconception:** Confusing the direction of unemployment relative to Real GDP changes.

34. **Row TBD: Market Determinants (Shifts in S & D)**
    - **Figure:** Table with scenarios (e.g., Input price rises, Tech improves, Consumer income falls). Columns: Supply curve, Demand curve, Equilibrium Price, Eq. Quantity.
    - **Hotspots:** Predict Shifts (Left/Right/None) and resulting Price/Quantity changes.
    - **Distractors:** Moves along curve, Elastic, Inelastic.
    - **Misconception:** Shifting both curves when a scenario only explicitly affects one determinant.
