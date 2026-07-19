import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from viz_lib import *
from viz_lib import _demandQP, _supplyQP

def main():
    saved_count = 0

    # PLAIN: axes + demand + supply + two horizontal price lines (solid Pw, dashed Pw+t)
    plain_body = (
        axes("Q", "P")
        + _demandQP(100)
        + _supplyQP(0)
        + lnQP(0, 30, 100, 30, "#0f766e", 2)
        + lnQP(0, 45, 100, 45, "#0f766e", 2, "6 4")
    )
    save("u_econ_tariff_trade__plain.svg", plain_body)
    saved_count += 1

    # LABELED: shading first, then curves/lines, guides, dots, and text labels
    dwl_prod = polyQP([(30, 30), (45, 45), (45, 30)], "#6b7280", 0.25)
    dwl_cons = polyQP([(55, 45), (70, 30), (55, 30)], "#6b7280", 0.25)

    guides = (
        lnQP(30, 30, 30, 0, "#999", 1, "4 4")
        + lnQP(45, 45, 45, 0, "#999", 1, "4 4")
        + lnQP(55, 45, 55, 0, "#999", 1, "4 4")
        + lnQP(70, 30, 70, 0, "#999", 1, "4 4")
    )

    dots = dotQP(30, 30) + dotQP(70, 30) + dotQP(45, 45) + dotQP(55, 45)

    labels = (
        clabel('D', 100, "D", "#1d4ed8")
        + clabel('S', 0, "S", "#b91c1c")
        + txtQP(84, 34, "World price", 11, "#0f766e")
        + txtQP(84, 49, "+tariff", 11, "#0f766e")
        + txt(52, sy(30) + 4, "Pw", 11, "#0f766e", "end")
        + txt(52, sy(45) + 4, "Pw+t", 11, "#0f766e", "end")
        + txt(sx(30), 296, "Qs1", 11)
        + txt(sx(45), 308, "Qs2", 11)
        + txt(sx(55), 296, "Qd2", 11)
        + txt(sx(70), 308, "Qd1", 11)
    )

    labeled_body = (
        axes("Q", "P")
        + dwl_prod
        + dwl_cons
        + _demandQP(100)
        + _supplyQP(0)
        + lnQP(0, 30, 100, 30, "#0f766e", 2)
        + lnQP(0, 45, 100, 45, "#0f766e", 2, "6 4")
        + guides
        + dots
        + labels
    )
    save("u_econ_tariff_trade__labeled.svg", labeled_body)
    saved_count += 1

    print(f"Saved {saved_count} files.")

if __name__ == "__main__":
    main()
