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

# 1) u_chem_titration_weak — WEAK acid titrated with strong base
pts_tit = [(2,28),(12,40),(25,47),(38,54),(46,64),(49,72),(50,80),(52,86),(60,90),(90,93)]
c_tit = draw_curve(pts_tit, "#1d4ed8", 2.5)

lbl_tit = (
    dotQP(25, 47) +
    dotQP(50, 80) +
    # half-equivalence label
    ln(sx(25), sy(43), sx(25), sy(30), "#999", 1) +
    txtQP(25, 24, "half-equivalence: pH = pKa", 11, "#333", "middle", True) +
    # equivalence point label
    ln(sx(36), sy(88), sx(48), sy(81), "#999", 1) +
    txtQP(13, 91, "equivalence point (pH > 7)", 11, "#333", "start", True)
)

body_tit_plain = axes("Volume of base added (mL)", "pH") + c_tit
body_tit_labeled = body_tit_plain + lbl_tit

save("u_chem_titration_weak__plain.svg", body_tit_plain)
count += 1
save("u_chem_titration_weak__labeled.svg", body_tit_labeled)
count += 1


# 2) u_chem_beers_law — Beer-Lambert calibration
line_beer = lnQP(0, 0, 88, 84, "#1d4ed8", 2.5)
dots_beer = dotQP(20, 19) + dotQP(44, 42) + dotQP(66, 63)

lbl_beer = (
    dots_beer +
    txtQP(25, 68, "A = εlc", 14, "#1d4ed8", "middle", True) +
    ln(sx(48), sy(67), sx(54), sy(53.5), "#999", 1) +
    txtQP(48, 72, "slope = εl", 12, "#333", "middle", True)
)

body_beer_plain = axes("Concentration (M)", "Absorbance") + line_beer
body_beer_labeled = body_beer_plain + lbl_beer

save("u_chem_beers_law__plain.svg", body_beer_plain)
count += 1
save("u_chem_beers_law__labeled.svg", body_beer_labeled)
count += 1


# 3) u_chem_gas_boyle — Boyle's law P vs V
pts_boyle = [(10,90),(16,66),(24,46),(36,30),(52,21),(72,15),(92,12)]
c_boyle = draw_curve(pts_boyle, "#b91c1c", 2.5)

lbl_boyle = (
    txtQP(62, 72, "PV = constant (Boyle's law)", 13, "#b91c1c", "middle", True) +
    txtQP(62, 58, "P ∝ 1/V", 12, "#333", "middle", True)
)

body_boyle_plain = axes("Volume", "Pressure") + c_boyle
body_boyle_labeled = body_boyle_plain + lbl_boyle

save("u_chem_gas_boyle__plain.svg", body_boyle_plain)
count += 1
save("u_chem_gas_boyle__labeled.svg", body_boyle_labeled)
count += 1


# 4) u_chem_pe_internuclear — potential-energy vs internuclear distance
zero_line = lnQP(0, 55, 100, 55, "#999", 1, "4 4")
pts_pe = [(8,92),(14,68),(20,44),(28,30),(34,27),(44,37),(58,47),(75,52),(95,54)]
c_pe = draw_curve(pts_pe, "#0f766e", 2.5)

# Vertical dashed line for bond length (broken to leave space for text)
dash_bond = lnQP(34, 0, 34, 6, "#999", 1, "4 4") + lnQP(34, 15, 34, 27, "#999", 1, "4 4")

# Double arrow for bond energy at x=34 from y=27 to y=55
arrow_be = (
    lnQP(34, 27, 34, 55, "#b91c1c", 1.5) +
    lnQP(32, 51, 34, 55, "#b91c1c", 1.5) + lnQP(36, 51, 34, 55, "#b91c1c", 1.5) +
    lnQP(32, 31, 34, 27, "#b91c1c", 1.5) + lnQP(36, 31, 34, 27, "#b91c1c", 1.5)
)

lbl_pe = (
    dotQP(34, 27) +
    dash_bond +
    txtQP(34, 10, "bond length", 11, "#333", "middle", True) +
    arrow_be +
    ln(sx(50), sy(72), sx(35), sy(42), "#999", 1) +
    txtQP(58, 76, "bond energy (well depth)", 11, "#b91c1c", "middle", True)
)

body_pe_plain = axes("Internuclear distance", "Potential energy") + zero_line + c_pe
body_pe_labeled = body_pe_plain + lbl_pe

save("u_chem_pe_internuclear__plain.svg", body_pe_plain)
count += 1
save("u_chem_pe_internuclear__labeled.svg", body_pe_labeled)
count += 1

print(f"Successfully generated {count} SVG files.")
