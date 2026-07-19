import sys,os; sys.path.insert(0,os.path.dirname(__file__)); from viz_lib import *

def catmull_rom(pts, n_per_seg=20):
    if len(pts) < 2:
        return pts
    p = [(2*pts[0][0] - pts[1][0], 2*pts[0][1] - pts[1][1])] + pts + [(2*pts[-1][0] - pts[-2][0], 2*pts[-1][1] - pts[-2][1])]
    res = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i-1], p[i], p[i+1], p[i+2]
        for t_i in range(n_per_seg if i < len(p)-3 else n_per_seg + 1):
            t = t_i / float(n_per_seg)
            t2 = t * t
            t3 = t2 * t
            x = 0.5 * ((2*p1[0]) + (-p0[0] + p2[0])*t + (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0])*t2 + (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0])*t3)
            y = 0.5 * ((2*p1[1]) + (-p0[1] + p2[1])*t + (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1])*t2 + (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1])*t3)
            res.append((x, y))
    return res

def draw_curve(pts, color, w=2.5, dash=None, smooth=True):
    curve_pts = catmull_rom(pts) if smooth else pts
    s = ""
    for i in range(len(curve_pts) - 1):
        x1, y1 = curve_pts[i]
        x2, y2 = curve_pts[i+1]
        s += lnQP(x1, y1, x2, y2, color, w, dash)
    return s

count = 0

# 1) u_chem_mass_spectrum (Cl isotopes)
def draw_bar_plain(x, h):
    return (
        lnQP(x-4, 0, x-4, h, "#1d4ed8", 2) +
        lnQP(x-4, h, x+4, h, "#1d4ed8", 2) +
        lnQP(x+4, h, x+4, 0, "#1d4ed8", 2)
    )

def draw_bar_fill(x, h):
    poly_pts = [(x-4, 0), (x-4, h), (x+4, h), (x+4, 0)]
    return polyQP(poly_pts, "#1d4ed8", 0.35)

bars_plain = draw_bar_plain(32, 75) + draw_bar_plain(62, 25)
bars_fill = draw_bar_fill(32, 75) + draw_bar_fill(62, 25)

lbl_ms = (
    txtQP(32, 84, "m/z 35", 12, "#1d4ed8", "middle", True) +
    txtQP(32, 78, "(75%)", 11, "#333", "middle") +
    txtQP(62, 34, "m/z 37", 12, "#1d4ed8", "middle", True) +
    txtQP(62, 28, "(25%)", 11, "#333", "middle")
)

body_ms_plain = axes("m/z (mass-to-charge ratio)", "Relative abundance (%)") + bars_plain
body_ms_labeled = axes("m/z (mass-to-charge ratio)", "Relative abundance (%)") + bars_fill + bars_plain + lbl_ms

save("u_chem_mass_spectrum__plain.svg", body_ms_plain)
count += 1
save("u_chem_mass_spectrum__labeled.svg", body_ms_labeled)
count += 1


# 2) u_chem_arrhenius
line_arr = lnQP(8, 86, 92, 20, "#b91c1c", 2.5)
dots_arr = dotQP(24, 73) + dotQP(50, 53) + dotQP(76, 33)

lbl_arr = (
    txtQP(60, 70, "slope = -Ea/R", 13, "#b91c1c", "middle", True) +
    ln(sx(58), sy(66), sx(50), sy(53), "#999", 1) +
    txtQP(20, 90, "y-intercept = ln A", 11, "#333", "start", True) +
    ln(sx(10), sy(88), sx(8), sy(86), "#999", 1)
)

body_arr_plain = axes("1/T  (K^-1)", "ln k") + line_arr + dots_arr
body_arr_labeled = body_arr_plain + lbl_arr

save("u_chem_arrhenius__plain.svg", body_arr_plain)
count += 1
save("u_chem_arrhenius__labeled.svg", body_arr_labeled)
count += 1


# 3) u_chem_solubility_curve
pts_kno3 = [(4,12),(25,26),(50,50),(75,76),(96,92)]
pts_nacl = [(4,34),(50,37),(96,40)]
pts_caoh2 = [(4,30),(50,24),(96,17)]

c_kno3 = draw_curve(pts_kno3, "#1d4ed8", 2.5)
c_nacl = draw_curve(pts_nacl, "#0f766e", 2.5)
c_caoh2 = draw_curve(pts_caoh2, "#b91c1c", 2.5)

lbl_sol = (
    txtQP(78, 93, "KNO3", 12, "#1d4ed8", "middle", True) +
    ln(sx(83), sy(92), sx(92), sy(89), "#999", 1) +
    txtQP(78, 48, "NaCl", 12, "#0f766e", "middle", True) +
    ln(sx(78), sy(45), sx(85), sy(39), "#999", 1) +
    txtQP(82, 9, "Ca(OH)2", 12, "#b91c1c", "middle", True) +
    ln(sx(82), sy(12), sx(88), sy(18), "#999", 1)
)

body_sol_plain = axes("Temperature (°C)", "Solubility (g / 100 g H2O)") + c_kno3 + c_nacl + c_caoh2
body_sol_labeled = body_sol_plain + lbl_sol

save("u_chem_solubility_curve__plain.svg", body_sol_plain)
count += 1
save("u_chem_solubility_curve__labeled.svg", body_sol_labeled)
count += 1


# 4) u_chem_galvanic_cell
beakers = (
    lnQP(8,55,8,10,"#333",2) + lnQP(8,10,30,10,"#333",2) + lnQP(30,10,30,55,"#333",2) +
    lnQP(70,55,70,10,"#333",2) + lnQP(70,10,92,10,"#333",2) + lnQP(92,10,92,55,"#333",2)
)
solutions = (
    polyQP([(8,10),(8,40),(30,40),(30,10)], "#93c5fd", 0.35) +
    polyQP([(70,10),(70,40),(92,40),(92,10)], "#fca5a5", 0.35)
)
electrodes = (
    lnQP(19,58,19,20,"#555",5) +
    lnQP(81,58,81,20,"#b45309",5)
)
wire_voltmeter = (
    lnQP(19,58,19,70,"#333",1.5) + lnQP(19,70,44,70,"#333",1.5) +
    polyQP([(44,64),(56,64),(56,76),(44,76)], "#ffffff", 1.0) +
    lnQP(44,64,56,64,"#333",1.5) + lnQP(56,64,56,76,"#333",1.5) +
    lnQP(56,76,44,76,"#333",1.5) + lnQP(44,76,44,64,"#333",1.5) +
    txtQP(50,70,"V",13,"#000","middle",True) +
    lnQP(56,70,81,70,"#333",1.5) + lnQP(81,70,81,58,"#333",1.5) +
    lnQP(30,72,33,70,"#000",1.5) + lnQP(30,68,33,70,"#000",1.5) +
    lnQP(66,72,69,70,"#000",1.5) + lnQP(66,68,69,70,"#000",1.5)
)
salt_bridge = (
    lnQP(24,42,24,48,"#7c3aed",3) +
    lnQP(24,48,76,48,"#7c3aed",3) +
    lnQP(76,48,76,42,"#7c3aed",3)
)

body_gal_plain = beakers + solutions + electrodes + wire_voltmeter + salt_bridge

lbl_gal = (
    txtQP(20, 78, "Zn anode (-)", 11, "#555", "middle", True) +
    ln(sx(20), sy(76), sx(19), sy(58), "#999", 1) +
    txtQP(80, 78, "Cu cathode (+)", 11, "#b45309", "middle", True) +
    ln(sx(80), sy(76), sx(81), sy(58), "#999", 1) +
    txtQP(50, 84, "e- flow  ->", 11, "#000", "middle") +
    txtQP(50, 35, "salt bridge", 10, "#7c3aed", "middle") +
    ln(sx(50), sy(38), sx(50), sy(48), "#999", 1) +
    txtQP(13.5, 25, "ZnSO4", 10, "#1e40af", "middle") +
    txtQP(86.5, 25, "CuSO4", 10, "#991b1b", "middle")
)

body_gal_labeled = body_gal_plain + lbl_gal

save("u_chem_galvanic_cell__plain.svg", body_gal_plain)
count += 1
save("u_chem_galvanic_cell__labeled.svg", body_gal_labeled)
count += 1

print(f"Successfully generated {count} SVG files.")
