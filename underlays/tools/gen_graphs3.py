import sys,os; sys.path.insert(0,os.path.dirname(__file__)); from viz_lib import *
from viz_lib import _demandQP, _supplyQP

saved_files = []

# ==============================================================================
# 1) u_econ_monopsony — a monopsony LABOUR market. axes("Quantity of Labour","Wage")
# ==============================================================================
g1_curves = axes("Quantity of Labour", "Wage") + _supplyQP(0) + lnQP(0, 0, 50, 100, "#7c3aed", 2.2) + _demandQP(100)

g1_dots = (
    ln(sx(33.3), PY0, sx(33.3), sy(66.7), "#999", 1, "4 4") +
    ln(QX0, sy(33.3), sx(33.3), sy(33.3), "#999", 1, "4 4") +
    dotQP(33.3, 66.7) +
    dotQP(33.3, 33.3)
)

g1_labels = (
    clabel('D', 100, "MRP", "#1d4ed8") +
    clabel('S', 0, "S = ACL", "#b91c1c") +
    txtQP(38, 88, "MCL", 11, "#7c3aed") +
    txt(sx(33.3), 296, "Lm", 11) +
    txt(52, sy(33.3) + 4, "Wm", 11, "#333", "end")
)

g1_labeled = g1_curves + g1_dots + g1_labels
g1_plain = g1_curves

saved_files.append(save("u_econ_monopsony__labeled.svg", g1_labeled))
saved_files.append(save("u_econ_monopsony__plain.svg", g1_plain))

# ==============================================================================
# 2) u_econ_natural_monopoly — declining ATC over the whole range (economies of scale). axes("Q","$")
# ==============================================================================
atc_pts = [(12, 82), (30, 58), (50, 45), (70, 38), (90, 34)]
atc_poly = f'<polyline points="{" ".join(f"{sx(q)},{sy(p)}" for q,p in atc_pts)}" stroke="#0f766e" stroke-width="2.2" fill="none"/>'

mc_pts = [(12, 55), (50, 30), (90, 24)]
mc_poly = f'<polyline points="{" ".join(f"{sx(q)},{sy(p)}" for q,p in mc_pts)}" stroke="#b91c1c" stroke-width="2.2" fill="none"/>'

mr_line = lnQP(0, 100, 50, 0, "#60a5fa", 2)
demand_line = _demandQP(100)

g2_curves = axes("Q", "$") + atc_poly + mc_poly + demand_line + mr_line

g2_dots = (
    ln(QX0, sy(72), sx(28), sy(72), "#999", 1, "4 4") +
    ln(sx(28), PY0, sx(28), sy(72), "#999", 1, "4 4") +
    ln(QX0, sy(28), sx(72), sy(28), "#999", 1, "4 4") +
    dotQP(28, 72) +
    dotQP(28, 44) +
    dotQP(72, 28)
)

g2_labels = (
    clabel('D', 100, "D", "#1d4ed8") +
    txtQP(40, 14, "MR", 11, "#60a5fa") +
    txtQP(88, 20, "MC", 11, "#b91c1c") +
    txtQP(88, 30, "ATC", 11, "#0f766e") +
    txt(52, sy(72) + 4, "Pm", 11, "#333", "end") +
    txt(sx(28), 296, "Qm", 11) +
    txt(52, sy(28) + 4, "P=MC", 11, "#333", "end")
)

g2_labeled = g2_curves + g2_dots + g2_labels
g2_plain = g2_curves

saved_files.append(save("u_econ_natural_monopoly__labeled.svg", g2_labeled))
saved_files.append(save("u_econ_natural_monopoly__plain.svg", g2_plain))

# ==============================================================================
# 3) u_econ_reserve_market — the federal funds market. axes("Quantity of Reserves","Federal funds rate")
# ==============================================================================
ms_line = lnQP(50, 0, 50, 92, "#b91c1c", 2.5)
md_line = _demandQP(100)

g3_curves = axes("Quantity of Reserves", "Federal funds rate") + md_line + ms_line

g3_dots = (
    ln(QX0, sy(50), sx(50), sy(50), "#999", 1, "4 4") +
    dotQP(50, 50)
)

g3_labels = (
    txtQP(50, 96, "MS", 11, "#b91c1c") +
    clabel('D', 100, "MD", "#1d4ed8") +
    txt(52, sy(50) + 4, "r*", 11, "#333", "end") +
    txt(sx(50), 296, "Q*", 11)
)

g3_labeled = g3_curves + g3_dots + g3_labels
g3_plain = g3_curves

saved_files.append(save("u_econ_reserve_market__labeled.svg", g3_labeled))
saved_files.append(save("u_econ_reserve_market__plain.svg", g3_plain))

# ==============================================================================
# 4) u_econ_ppc_growth_shift — PPC shifting OUTWARD (economic growth). axes("Good X","Good Y")
# ==============================================================================
ppc1_pts = [(5, 88), (30, 80), (55, 66), (75, 45), (90, 12)]
ppc1_poly = f'<polyline points="{" ".join(f"{sx(q)},{sy(p)}" for q,p in ppc1_pts)}" stroke="#0f766e" stroke-width="2.2" fill="none"/>'

ppc2_pts = [(8, 98), (38, 92), (66, 80), (86, 58), (98, 20)]
ppc2_poly = f'<polyline points="{" ".join(f"{sx(q)},{sy(p)}" for q,p in ppc2_pts)}" stroke="#0f766e" stroke-width="2.2" stroke-dasharray="7 5" fill="none"/>'

g4_curves = axes("Good X", "Good Y") + ppc1_poly + ppc2_poly

g4_arrow = arrow(sx(55), sy(66), sx(66), sy(80), "#0f766e")

g4_labels = (
    txtQP(20, 72, "PPC1", 11, "#0f766e") +
    txtQP(50, 90, "PPC2", 11, "#0f766e") +
    txtQP(70, 68, "Growth", 10, "#0f766e") +
    g4_arrow
)

g4_labeled = g4_curves + g4_labels
g4_plain = g4_curves

saved_files.append(save("u_econ_ppc_growth_shift__labeled.svg", g4_labeled))
saved_files.append(save("u_econ_ppc_growth_shift__plain.svg", g4_plain))

print(f"Saved {len(saved_files)} files.")
