import sys,os; sys.path.insert(0,os.path.dirname(__file__)); from viz_lib import *
from viz_lib import _demandQP, _supplyQP

saved_files = []

# ==============================================================================
# 1) u_econ_min_wage_labor
# ==============================================================================
g1_curves = axes("Quantity of Labour", "Wage") + _demandQP(100) + _supplyQP(0) + lnQP(0, 70, 100, 70, "#0f766e", 2, "6 4")

g1_dots = (
    ln(sx(30), sy(70), sx(30), PY0, "#999", 1, "4 4") +
    ln(sx(70), sy(70), sx(70), PY0, "#999", 1, "4 4") +
    dotQP(30, 70) +
    dotQP(70, 70)
)

g1_labels = (
    clabel('D', 100, "D (labour demand)", "#1d4ed8") +
    clabel('S', 0, "S (labour supply)", "#b91c1c") +
    txtQP(85, 74, "Min wage", 11, "#0f766e") +
    txt(sx(30), 296, "Qd", 11) +
    txt(sx(70), 296, "Qs", 11) +
    txtQP(50, 84, "Unemployment", 11)
)

g1_labeled = g1_curves + g1_dots + g1_labels
g1_plain = g1_curves

saved_files.append(save("u_econ_min_wage_labor__labeled.svg", g1_labeled))
saved_files.append(save("u_econ_min_wage_labor__plain.svg", g1_plain))

# ==============================================================================
# 2) u_econ_lorenz_curve
# ==============================================================================
lorenz_pts = [(0,0), (20,5), (40,15), (60,32), (80,58), (100,100)]
lorenz_poly = f'<polyline points="{" ".join(f"{sx(q)},{sy(p)}" for q,p in lorenz_pts)}" stroke="#1d4ed8" stroke-width="2.5" fill="none"/>'
diagonal = lnQP(0, 0, 100, 100, "#333", 1.5)

g2_curves = axes("% households (cumulative)", "% income (cumulative)") + diagonal + lorenz_poly
g2_shading = polyQP([(0,0), (20,5), (40,15), (60,32), (80,58), (100,100), (0,0)], "#6b7280", 0.12)

g2_labels = (
    txtQP(50, 72, "Line of equality", 11, "#333") +
    txtQP(72, 22, "Lorenz curve", 11, "#1d4ed8")
)

g2_labeled = axes("% households (cumulative)", "% income (cumulative)") + g2_shading + diagonal + lorenz_poly + g2_labels
g2_plain = g2_curves

saved_files.append(save("u_econ_lorenz_curve__labeled.svg", g2_labeled))
saved_files.append(save("u_econ_lorenz_curve__plain.svg", g2_plain))

# ==============================================================================
# 3) u_econ_business_cycle
# ==============================================================================
trend_line = lnQP(5, 32, 95, 80, "#0f766e", 2, "6 4")
cycle_pts = [(5,32), (18,50), (30,40), (45,66), (58,52), (72,82), (88,70), (95,84)]
cycle_poly = f'<polyline points="{" ".join(f"{sx(q)},{sy(p)}" for q,p in cycle_pts)}" stroke="#1d4ed8" stroke-width="2.5" fill="none"/>'

g3_curves = axes("Time", "Real GDP") + trend_line + cycle_poly
g3_dots = dotQP(18, 50) + dotQP(30, 40)

g3_labels = (
    txtQP(18, 56, "Peak", 11, "#333") +
    txtQP(30, 33, "Trough", 11, "#333") +
    txtQP(78, 88, "Trend (potential)", 10, "#0f766e") +
    txtQP(36, 62, "Expansion", 10, "#1d4ed8") +   # on the 30->45 RISING segment (was on a falling one)
    txtQP(52, 42, "Recession", 10, "#1d4ed8")
)

g3_labeled = g3_curves + g3_dots + g3_labels
g3_plain = g3_curves

saved_files.append(save("u_econ_business_cycle__labeled.svg", g3_labeled))
saved_files.append(save("u_econ_business_cycle__plain.svg", g3_plain))

# ==============================================================================
# 4) u_econ_forex_shift
# ==============================================================================
g4_curves = axes("Quantity of $", "Exchange rate") + _demandQP(100) + _supplyQP(0) + _demandQP(120, "7 5")

g4_dots = guideQP(50, 50) + guideQP(60, 60) + dotQP(50, 50) + dotQP(60, 60)
g4_arrow = arrow(sx(32), sy(72), sx(46), sy(72), "#0f766e")

g4_labels = (
    clabel('D', 100, "D$1", "#1d4ed8") +
    clabel('D', 120, "D$2", "#1d4ed8") +
    clabel('S', 0, "S$", "#b91c1c") +
    txt(52, sy(50) + 4, "e1", 11, "#333", "end") +
    txt(52, sy(60) + 4, "e2", 11, "#333", "end") +
    txt(sx(50), 296, "Q1", 11) +
    txt(sx(60), 296, "Q2", 11) +
    g4_arrow
)

g4_labeled = g4_curves + g4_dots + g4_labels
g4_plain = g4_curves

saved_files.append(save("u_econ_forex_shift__labeled.svg", g4_labeled))
saved_files.append(save("u_econ_forex_shift__plain.svg", g4_plain))

print(f"Saved {len(saved_files)} files.")
