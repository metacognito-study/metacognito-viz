import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from viz_lib import *
from viz_lib import _demandQP, _supplyQP

saved_files = []

# ==============================================================================
# DIAGRAM 1 — u_econ_externality_negative (overproduction, e.g. pollution)
# ==============================================================================
# Base curves: D = MSB = MPB (a=100), MPC (b=0), MSC (b=-20, dashed red)
d1_curves = axes("Q", "P") + _demandQP(100) + _supplyQP(0) + _supplyQP(-20, "7 5")

# DWL triangle polygon shading (overproduction)
d1_dwl = polyQP([(40, 60), (50, 50), (50, 70)], "#6b7280", 0.25)

# Dots and guide lines for market eq (50,50) & social opt (40,60)
d1_dots = dotQP(50, 50) + dotQP(40, 60) + guideQP(50, 50) + guideQP(40, 60)

# Labels
d1_labels = (
    txtQP(62, 90, "MSC", 12, "#b91c1c") +
    clabel('S', 0, "MPC", "#b91c1c") +
    clabel('D', 100, "D=MSB", "#1d4ed8") +
    txt(sx(40), 296, "Qopt", 11) +
    txt(sx(50), 308, "Qmkt", 11) +
    ln(sx(75), sy(12), sx(48), sy(58), "#999", 1) +
    txtQP(75, 12, "DWL", 11, "#555")
)

d1_labeled_svg = axes("Q", "P") + d1_dwl + _demandQP(100) + _supplyQP(0) + _supplyQP(-20, "7 5") + d1_dots + d1_labels
d1_plain_svg = d1_curves

saved_files.append(save("u_econ_externality_negative__labeled.svg", d1_labeled_svg))
saved_files.append(save("u_econ_externality_negative__plain.svg", d1_plain_svg))

# ==============================================================================
# DIAGRAM 2 — u_econ_externality_positive (underproduction, e.g. education)
# ==============================================================================
# Base curves: S = MPC = MSC (b=0), MPB (a=100), MSB (a=120, dashed blue)
d2_curves = axes("Q", "P") + _supplyQP(0) + _demandQP(100) + _demandQP(120, "7 5")

# DWL triangle polygon shading (underproduction)
d2_dwl = polyQP([(50, 50), (60, 60), (50, 70)], "#6b7280", 0.25)

# Dots and guide lines for market eq (50,50) & social opt (60,60)
d2_dots = dotQP(50, 50) + dotQP(60, 60) + guideQP(50, 50) + guideQP(60, 60)

# Labels
d2_labels = (
    txtQP(33, 92, "MSB", 12, "#1d4ed8") +
    clabel('D', 100, "MPB", "#1d4ed8") +
    clabel('S', 0, "S", "#b91c1c") +
    txt(sx(50), 296, "Qmkt", 11) +
    txt(sx(60), 308, "Qopt", 11) +
    ln(sx(75), sy(12), sx(54), sy(60), "#999", 1) +
    txtQP(75, 12, "DWL", 11, "#555")
)

d2_labeled_svg = axes("Q", "P") + d2_dwl + _supplyQP(0) + _demandQP(100) + _demandQP(120, "7 5") + d2_dots + d2_labels
d2_plain_svg = d2_curves

saved_files.append(save("u_econ_externality_positive__labeled.svg", d2_labeled_svg))
saved_files.append(save("u_econ_externality_positive__plain.svg", d2_plain_svg))

print(f"Saved {len(saved_files)} files.")
