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

# 1) u_chem_maxwell_boltzmann
pts_t1 = [(2,2),(10,30),(18,55),(26,48),(40,30),(60,15),(85,4)]
pts_t2 = [(2,1),(12,20),(24,36),(36,38),(50,30),(70,17),(92,6)]
c_t1 = draw_curve(pts_t1, "#1d4ed8", 2.5)
c_t2 = draw_curve(pts_t2, "#b91c1c", 2.5)
ea_line = lnQP(55, 0, 55, 60, "#0f766e", 2, "6 4")

# Shaded tail under T2 right of Ea (x >= 55)
t2_dense = catmull_rom(pts_t2)
t2_right_of_ea = [(x, y) for x, y in t2_dense if x >= 55]
shade_pts = [(55, 0)] + t2_right_of_ea + [(t2_right_of_ea[-1][0], 0)]
shade = polyQP(shade_pts, "#0f766e", 0.15)

lbl_mb = (
    txtQP(18, 62, "T1 (lower temp)", 12, "#1d4ed8", "middle", True) +
    txtQP(52, 35, "T2 (higher temp)", 12, "#b91c1c", "start", True) +
    txtQP(55, 64, "Ea", 13, "#0f766e", "middle", True) +
    txtQP(76, 30, "Molecules with E ≥ Ea", 11, "#0f766e", "middle") +
    ln(sx(76), sy(27), sx(68), sy(12), "#999", 1)
)

body_mb_plain = axes("Kinetic energy", "Fraction of molecules") + c_t1 + c_t2 + ea_line
body_mb_labeled = body_mb_plain + shade + lbl_mb

save("u_chem_maxwell_boltzmann__plain.svg", body_mb_plain)
count += 1
save("u_chem_maxwell_boltzmann__labeled.svg", body_mb_labeled)
count += 1


# 2) u_chem_titration_strong
pts_tit = [(2,2),(20,3),(40,5),(48,7),(50,25),(50,50),(50,75),(52,88),(70,93),(95,96)]
c_tit = draw_curve(pts_tit, "#1d4ed8", 2.5, smooth=False)

eq_dot = dotQP(50, 50)
lbl_tit = (
    eq_dot +
    # Half-equivalence tick & label
    lnQP(25, 1, 25, 6, "#555", 1.5) +
    txtQP(25, 14, "Half-equivalence", 11, "#555", "middle") +
    # Equivalence point label & leader
    txtQP(18, 62, "Equivalence point (pH 7)", 11, "#333", "start", True) +
    ln(sx(27), sy(54), sx(48), sy(50), "#999", 1)
)

body_tit_plain = axes("Volume of base added (mL)", "pH") + c_tit
body_tit_labeled = body_tit_plain + lbl_tit

save("u_chem_titration_strong__plain.svg", body_tit_plain)
count += 1
save("u_chem_titration_strong__labeled.svg", body_tit_labeled)
count += 1


# 3) u_chem_heating_curve
pts_heat = [(3,8),(15,28),(35,28),(48,55),(80,55),(92,80)]
c_heat = draw_curve(pts_heat, "#1d4ed8", 2.5, smooth=False)

lbl_heat = (
    txtQP(8, 22, "Solid", 12, "#1d4ed8", "middle", True) +
    txtQP(25, 34, "Melting", 12, "#0f766e", "middle", True) +
    txtQP(36, 46, "Liquid", 12, "#1d4ed8", "end", True) +
    txtQP(64, 61, "Boiling", 12, "#0f766e", "middle", True) +
    txtQP(84, 75, "Gas", 12, "#1d4ed8", "end", True)
)

body_heat_plain = axes("Heat added", "Temperature") + c_heat
body_heat_labeled = body_heat_plain + lbl_heat

save("u_chem_heating_curve__plain.svg", body_heat_plain)
count += 1
save("u_chem_heating_curve__labeled.svg", body_heat_labeled)
count += 1


# 4) u_chem_energy_profile
pts_uncat = [(5,40),(20,50),(35,72),(45,80),(55,72),(70,35),(92,20)]
pts_cat = [(5,40),(30,58),(45,62),(60,52),(92,20)]

c_uncat = draw_curve(pts_uncat, "#1d4ed8", 2.5)
c_cat = draw_curve(pts_cat, "#0f766e", 2, dash="5 4")

# Reference lines & markers for labeled version
ref_reactants = lnQP(2, 40, 45, 40, "#aaa", 1, "3 3")
ref_products = lnQP(55, 20, 95, 20, "#aaa", 1, "3 3")

# Ea arrow (from y=40 to y=80 at x=45)
ea_arrow = (
    lnQP(45, 40, 45, 80, "#b91c1c", 1.5, "4 3") +
    lnQP(43, 76, 45, 80, "#b91c1c", 1.5) + lnQP(47, 76, 45, 80, "#b91c1c", 1.5) +
    lnQP(43, 44, 45, 40, "#b91c1c", 1.5) + lnQP(47, 44, 45, 40, "#b91c1c", 1.5)
)

# dH arrow (from y=40 to y=20 at x=82)
dh_arrow = (
    lnQP(82, 20, 82, 40, "#0f766e", 1.5, "4 3") +
    lnQP(80, 36, 82, 40, "#0f766e", 1.5) + lnQP(84, 36, 82, 40, "#0f766e", 1.5) +
    lnQP(80, 24, 82, 20, "#0f766e", 1.5) + lnQP(84, 24, 82, 20, "#0f766e", 1.5)
)

lbl_ep = (
    c_cat + ref_reactants + ref_products + ea_arrow + dh_arrow +
    txtQP(13, 33, "Reactants", 11, "#1d4ed8", "middle", True) +
    txtQP(82, 13, "Products", 12, "#1d4ed8", "middle", True) +
    txtQP(45, 85, "Ea", 12, "#b91c1c", "middle", True) +
    txtQP(45, 71, "Catalysed", 11, "#0f766e", "middle") +
    txtQP(86, 30, "dH", 12, "#0f766e", "start", True)
)

body_ep_plain = axes("Reaction progress", "Energy") + c_uncat
body_ep_labeled = body_ep_plain + lbl_ep

save("u_chem_energy_profile__plain.svg", body_ep_plain)
count += 1
save("u_chem_energy_profile__labeled.svg", body_ep_labeled)
count += 1


# 5) u_chem_pes
def draw_bar_plain(x, h):
    return (
        lnQP(x-4, 0, x-4, h, "#1d4ed8", 2) +
        lnQP(x-4, h, x+4, h, "#1d4ed8", 2) +
        lnQP(x+4, h, x+4, 0, "#1d4ed8", 2)
    )

def draw_bar_labeled(x, h, label):
    poly_pts = [(x-4, 0), (x-4, h), (x+4, h), (x+4, 0)]
    return (
        polyQP(poly_pts, "#1d4ed8", 0.5) +
        draw_bar_plain(x, h) +
        txtQP(x, h + 6, label, 12, "#1d4ed8", "middle", True)
    )

bars_plain = draw_bar_plain(85, 40) + draw_bar_plain(45, 40) + draw_bar_plain(20, 80)
bars_labeled = draw_bar_labeled(85, 40, "1s") + draw_bar_labeled(45, 40, "2s") + draw_bar_labeled(20, 80, "2p")

body_pes_plain = axes("Binding energy (increasing ->)", "Relative # of electrons") + bars_plain
body_pes_labeled = axes("Binding energy (increasing ->)", "Relative # of electrons") + bars_labeled

save("u_chem_pes__plain.svg", body_pes_plain)
count += 1
save("u_chem_pes__labeled.svg", body_pes_labeled)
count += 1

print(f"Successfully generated {count} SVG files.")
