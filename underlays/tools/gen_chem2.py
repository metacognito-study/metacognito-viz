import sys,os; sys.path.insert(0,os.path.dirname(__file__)); from viz_lib import *

def draw_polyline(pts, color, w=2.5, dash=None):
    s = ""
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        s += lnQP(x1, y1, x2, y2, color, w, dash)
    return s

count = 0

# 1) u_chem_phase_diagram
sublimation = lnQP(6, 9, 30, 30, "#333", 2)
fusion = lnQP(30, 30, 40, 92, "#333", 2)
vap_pts = [(30,30), (45,48), (60,66), (75,80)]
vaporization = draw_polyline(vap_pts, "#333", 2)

body_pd_plain = axes("Temperature", "Pressure") + sublimation + fusion + vaporization

lbl_pd = (
    dotQP(30, 30) +
    dotQP(75, 80) +
    txtQP(15, 55, "Solid", 13, "#333", "middle", True) +
    txtQP(45, 72, "Liquid", 13, "#333", "middle", True) +
    txtQP(70, 25, "Gas", 13, "#333", "middle", True) +
    txtQP(22, 14, "Triple point", 11, "#333", "middle", True) +
    ln(sx(22), sy(16), sx(30), sy(30), "#666", 1) +
    txtQP(85, 88, "Critical point", 11, "#333", "middle", True) +
    ln(sx(82), sy(86), sx(75), sy(80), "#666", 1)
)

body_pd_labeled = body_pd_plain + lbl_pd

save("u_chem_phase_diagram__plain.svg", body_pd_plain)
count += 1
save("u_chem_phase_diagram__labeled.svg", body_pd_labeled)
count += 1


# 2) u_chem_concentration_time
pts_reactant = [(3,88), (15,60), (30,40), (50,24), (75,14), (95,10)]
pts_product = [(3,8), (15,36), (30,56), (50,72), (75,82), (95,86)]

c_reactant = draw_polyline(pts_reactant, "#b91c1c", 2.5)
c_product = draw_polyline(pts_product, "#1d4ed8", 2.5)

body_ct_plain = axes("Time", "Concentration") + c_reactant + c_product

lbl_ct = (
    txtQP(78, 22, "[reactant]", 12, "#b91c1c", "start", True) +
    txtQP(78, 74, "[product]", 12, "#1d4ed8", "start", True)
)

body_ct_labeled = body_ct_plain + lbl_ct

save("u_chem_concentration_time__plain.svg", body_ct_plain)
count += 1
save("u_chem_concentration_time__labeled.svg", body_ct_labeled)
count += 1


# 3) u_chem_kinetics_first_order
line_fo = lnQP(5, 90, 92, 15, "#1d4ed8", 2.5)

body_fo_plain = axes("Time", "ln[A]") + line_fo

lbl_fo = (
    txtQP(65, 78, "ln[A] vs t is linear -> first order", 12, "#1d4ed8", "middle", True) +
    txtQP(65, 68, "slope = -k", 12, "#333", "middle", True) +
    ln(sx(65), sy(64), sx(65), sy(40), "#666", 1)
)

body_fo_labeled = body_fo_plain + lbl_fo

save("u_chem_kinetics_first_order__plain.svg", body_fo_plain)
count += 1
save("u_chem_kinetics_first_order__labeled.svg", body_fo_labeled)
count += 1


# 4) u_chem_kinetics_second_order
line_so = lnQP(5, 12, 92, 90, "#1d4ed8", 2.5)

body_so_plain = axes("Time", "1/[A]") + line_so

lbl_so = (
    txtQP(35, 78, "1/[A] vs t is linear -> second order", 12, "#1d4ed8", "middle", True) +
    txtQP(35, 68, "slope = +k", 12, "#333", "middle", True) +
    ln(sx(35), sy(64), sx(35), sy(41), "#666", 1)
)

body_so_labeled = body_so_plain + lbl_so

save("u_chem_kinetics_second_order__plain.svg", body_so_plain)
count += 1
save("u_chem_kinetics_second_order__labeled.svg", body_so_labeled)
count += 1


# 5) u_chem_ice_table
title_ice = "ICE Table:  A + B <=> 2C"
heads_ice = ["", "[A]", "[B]", "[C]"]
rows_ice = [
    ["I", "0.80", "0.80", "0"],
    ["C", "-x", "-x", "+2x"],
    ["E", "0.80-x", "0.80-x", "2x"]
]

body_ice_plain = table(title_ice, heads_ice, rows_ice, blanks=[(2,1),(2,2),(2,3)])
body_ice_labeled = table(title_ice, heads_ice, rows_ice)

save("u_chem_ice_table__plain.svg", body_ice_plain)
count += 1
save("u_chem_ice_table__labeled.svg", body_ice_labeled)
count += 1

print(f"Successfully generated {count} SVG files.")
