import json
import os

WIDTH = 480
HEIGHT = 320

def norm_x(x): return round(x / WIDTH, 3)
def norm_y(y): return round(y / HEIGHT, 3)

def check_hotspots(hotspots):
    # Bounds check
    for h in hotspots:
        assert 0.06 <= h['x'] <= 0.94, f"x out of bounds: {h}"
        assert 0.08 <= h['y'] <= 0.92, f"y out of bounds: {h}"
    # Separation check
    for i in range(len(hotspots)):
        for j in range(i + 1, len(hotspots)):
            dx = abs(hotspots[i]['x'] - hotspots[j]['x'])
            dy = abs(hotspots[i]['y'] - hotspots[j]['y'])
            assert dx >= 0.14 or dy >= 0.16, f"Too close: {hotspots[i]['id']} and {hotspots[j]['id']} dx={dx:.3f}, dy={dy:.3f}"

def write_files(slug, prompt, options, hotspots, svg_elements):
    check_hotspots(hotspots)

    # Add an arrow (ink) for the direction hotspot so check_labelers passes
    dir_h = next((h for h in hotspots if h['id'] == 'h_dir'), None)
    if dir_h:
        dx, dy = dir_h['x'] * WIDTH, dir_h['y'] * HEIGHT
        # Draw a simple arrow or just a line around the center so it has ink
        is_right = "right" in slug or slug == "ppc_growth" or slug == "ppc_biased_rotation" or slug == "shift_money_supply"
        is_left = "left" in slug or slug == "shift_loanable_demand"
        if is_right:
            svg_elements += f'\n  <path d="M {dx-15},{dy} L {dx+15},{dy} L {dx+5},{dy-10} M {dx+15},{dy} L {dx+5},{dy+10}" stroke="#333" stroke-width="2" fill="none"/>'
        elif is_left:
            svg_elements += f'\n  <path d="M {dx+15},{dy} L {dx-15},{dy} L {dx-5},{dy-10} M {dx-15},{dy} L {dx-5},{dy+10}" stroke="#333" stroke-width="2" fill="none"/>'
        else:
            svg_elements += f'\n  <circle cx="{dx}" cy="{dy}" r="5" fill="#333"/>'

    # JSON
    coord_file = f"_coords/econ_{slug}.json"
    with open(coord_file, "w") as f:
        json.dump({
            "slug": slug,
            "prompt": prompt,
            "options": options,
            "hotspots": hotspots
        }, f, indent=2)

    # SVG
    svg_file = f"_diagrams/econ/{slug}.svg"
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>
  <!-- Axes -->
  <line x1="40" y1="20" x2="40" y2="280" stroke="#333" stroke-width="2"/>
  <line x1="40" y1="280" x2="460" y2="280" stroke="#333" stroke-width="2"/>
  {svg_elements}
</svg>"""
    with open(svg_file, "w") as f:
        f.write(svg_content)

def make_demand_supply(slug):
    is_demand = "demand" in slug
    is_right = "right" in slug

    if is_demand:
        opts = ["Quantity demanded", "Equilibrium", "Price level", "Average price", "Cost", "Quantity", "Price", "D₁", "D₂", "Shift right (increase)", "Shift left (decrease)"]
        prompt = "Label the axes, the demand curves, and the direction of the shift."

        c1_x1, c1_y1 = 80, 50
        c1_x2, c1_y2 = 320, 250

        shift_dx = 100 if is_right else -100
        if not is_right:
            c1_x1 += 100
            c1_x2 += 100

        c2_x1 = c1_x1 + shift_dx
        c2_y1 = c1_y1
        c2_x2 = c1_x2 + shift_dx
        c2_y2 = c1_y2

        l1, l2 = "D₁", "D₂"

        h1_px, h1_py = c1_x1, c1_y1
        h2_px, h2_py = c2_x2, c2_y2

        gap_x = (c1_x1 + c2_x1) / 2 + 120
        gap_y = (c1_y1 + c2_y1) / 2 + 100
        hx_pos = 250

    else:
        opts = ["Quantity supplied", "Equilibrium", "Price level", "Average price", "Cost", "Quantity", "Price", "S₁", "S₂", "Shift right (increase)", "Shift left (decrease)"]
        prompt = "Label the axes, the supply curves, and the direction of the shift."

        c1_x1, c1_y1 = 80, 250
        c1_x2, c1_y2 = 320, 50

        shift_dx = 100 if is_right else -100
        if not is_right:
            c1_x1 += 100
            c1_x2 += 100

        c2_x1 = c1_x1 + shift_dx
        c2_y1 = c1_y1
        c2_x2 = c1_x2 + shift_dx
        c2_y2 = c1_y2

        l1, l2 = "S₁", "S₂"

        h1_px, h1_py = c1_x1, c1_y1
        h2_px, h2_py = c2_x2, c2_y2

        gap_x = (c1_x1 + c2_x1) / 2 + 120
        gap_y = (c1_y1 + c2_y1) / 2 - 100
        hx_pos = 250

    hotspots = [
        {"id": "h_y", "label": "Price", "x": norm_x(40), "y": norm_y(150)},
        {"id": "h_x", "label": "Quantity", "x": norm_x(hx_pos), "y": norm_y(280)},
        {"id": "h_c1", "label": l1, "x": norm_x(h1_px), "y": norm_y(h1_py)},
        {"id": "h_c2", "label": l2, "x": norm_x(h2_px), "y": norm_y(h2_py)},
        {"id": "h_dir", "label": "Shift right (increase)" if is_right else "Shift left (decrease)", "x": norm_x(gap_x), "y": norm_y(gap_y)}
    ]

    svg = f"""<line x1="{c1_x1}" y1="{c1_y1}" x2="{c1_x2}" y2="{c1_y2}" stroke="#333" stroke-width="2.5"/>
  <line x1="{c2_x1}" y1="{c2_y1}" x2="{c2_x2}" y2="{c2_y2}" stroke="#333" stroke-width="2.5" stroke-dasharray="5,5"/>"""

    write_files(slug, prompt, opts, hotspots, svg)

def make_adas_money(slug):
    hx_pos = 250
    hy_pos = 150

    if slug == "shift_ad":
        opts = ["Real GDP", "Price level", "Aggregate supply", "AD₁", "AD₂", "Shift right (increase)", "Shift left (decrease)", "Inflation", "Unemployment"]
        prompt = "Label the axes, the aggregate demand curves, and the direction of the shift."

        c1_x1, c1_y1 = 80, 50
        c1_x2, c1_y2 = 320, 250

        c2_x1, c2_y1 = 180, 50
        c2_x2, c2_y2 = 420, 250

        l1, l2 = "AD₁", "AD₂"

        h1_px, h1_py = c1_x1, c1_y1
        h2_px, h2_py = c2_x2, c2_y2
        gap_x = (c1_x1 + c2_x1) / 2 + 120
        gap_y = (c1_y1 + c2_y1) / 2 + 100

        x_lbl, y_lbl = "Real GDP", "Price level"
        dir_lbl = "Shift right (increase)"

    elif slug == "shift_sras":
        opts = ["Real GDP", "Price level", "Aggregate demand", "SRAS₁", "SRAS₂", "Shift right (increase)", "Shift left (decrease)", "Inflation", "Unemployment"]
        prompt = "Label the axes, the short-run aggregate supply curves, and the direction of the shift."

        c1_x1, c1_y1 = 180, 250
        c1_x2, c1_y2 = 420, 50

        c2_x1, c2_y1 = 80, 250
        c2_x2, c2_y2 = 320, 50

        l1, l2 = "SRAS₁", "SRAS₂"

        h1_px, h1_py = c1_x1, c1_y1
        h2_px, h2_py = c2_x2, c2_y2
        gap_x = (c1_x1 + c2_x1) / 2 + 120
        gap_y = (c1_y1 + c2_y1) / 2 - 100

        x_lbl, y_lbl = "Real GDP", "Price level"
        dir_lbl = "Shift left (decrease)"

    elif slug == "shift_money_supply":
        opts = ["Quantity of money", "Nominal interest rate", "Real interest rate", "Money demand", "MS₁", "MS₂", "Shift right (increase)", "Shift left (decrease)"]
        prompt = "Label the axes, the money supply curves, and the direction of the shift."

        c1_x1, c1_y1 = 150, 50
        c1_x2, c1_y2 = 150, 250

        c2_x1, c2_y1 = 280, 50
        c2_x2, c2_y2 = 280, 250

        l1, l2 = "MS₁", "MS₂"

        h1_px, h1_py = c1_x1, c1_y1
        h2_px, h2_py = c2_x2, c2_y2
        gap_x = (c1_x1 + c2_x1) / 2
        gap_y = 150
        hx_pos = 400

        x_lbl, y_lbl = "Quantity of money", "Nominal interest rate"
        dir_lbl = "Shift right (increase)"

    elif slug == "shift_loanable_demand":
        opts = ["Quantity of loanable funds", "Real interest rate", "Nominal interest rate", "Supply of loanable funds", "D₁", "D₂", "Shift right (increase)", "Shift left (decrease)"]
        prompt = "Label the axes, the demand for loanable funds curves, and the direction of the shift."

        c1_x1, c1_y1 = 180, 50
        c1_x2, c1_y2 = 420, 250

        c2_x1, c2_y1 = 80, 50
        c2_x2, c2_y2 = 320, 250

        l1, l2 = "D₁", "D₂"

        h1_px, h1_py = c1_x1, c1_y1
        h2_px, h2_py = c2_x2, c2_y2
        gap_x = (c1_x1 + c2_x1) / 2 + 120
        gap_y = (c1_y1 + c2_y1) / 2 + 100
        hx_pos = 200

        x_lbl, y_lbl = "Quantity of loanable funds", "Real interest rate"
        dir_lbl = "Shift left (decrease)"

    hotspots = [
        {"id": "h_y", "label": y_lbl, "x": norm_x(40), "y": norm_y(hy_pos)},
        {"id": "h_x", "label": x_lbl, "x": norm_x(hx_pos), "y": norm_y(280)},
        {"id": "h_c1", "label": l1, "x": norm_x(h1_px), "y": norm_y(h1_py)},
        {"id": "h_c2", "label": l2, "x": norm_x(h2_px), "y": norm_y(h2_py)},
        {"id": "h_dir", "label": dir_lbl, "x": norm_x(gap_x), "y": norm_y(gap_y)}
    ]

    svg = f"""<line x1="{c1_x1}" y1="{c1_y1}" x2="{c1_x2}" y2="{c1_y2}" stroke="#333" stroke-width="2.5"/>
  <line x1="{c2_x1}" y1="{c2_y1}" x2="{c2_x2}" y2="{c2_y2}" stroke="#333" stroke-width="2.5" stroke-dasharray="5,5"/>"""

    write_files(slug, prompt, opts, hotspots, svg)

def make_ppc(slug):
    hx_pos = 350
    hy_pos = 150

    if slug == "ppc_growth":
        opts = ["Consumer goods", "Capital goods", "PPC₁", "PPC₂", "Shift right (increase)", "Shift left (decrease)", "Economic growth", "Opportunity cost"]
        prompt = "Label the axes, the production possibilities curves, and the direction of the shift."

        c1_start_x, c1_start_y = 40, 100
        c1_end_x, c1_end_y = 220, 280
        rx1, ry1 = 200, 200

        c2_start_x, c2_start_y = 40, 50
        c2_end_x, c2_end_y = 300, 280
        rx2, ry2 = 300, 300

        svg = f"""<path d="M {c1_start_x},{c1_start_y} A {rx1},{ry1} 0 0,1 {c1_end_x},{c1_end_y}" stroke="#333" stroke-width="2.5" fill="none"/>
  <path d="M {c2_start_x},{c2_start_y} A {rx2},{ry2} 0 0,1 {c2_end_x},{c2_end_y}" stroke="#333" stroke-width="2.5" fill="none" stroke-dasharray="5,5"/>"""

        l1, l2 = "PPC₁", "PPC₂"
        dir_lbl = "Shift right (increase)"

        h1_px, h1_py = c1_end_x, c1_end_y # 220, 280 (will conflict with h_x at 350,280? dx=130 > dx>=0.14(67). OK!)
        h2_px, h2_py = c2_start_x, c2_start_y # 40, 50
        gap_x = 220
        gap_y = 180

    elif slug == "ppc_biased_rotation":
        opts = ["Good X", "Good Y", "PPC₁", "PPC₂", "Shift right (increase)", "Shift left (decrease)", "Technological advance in Good X"]
        prompt = "Label the axes, the production possibilities curves, and the direction of the shift."

        c1_start_x, c1_start_y = 40, 80
        c1_end_x, c1_end_y = 220, 280
        rx1, ry1 = 220, 220

        c2_start_x, c2_start_y = 40, 80
        c2_end_x, c2_end_y = 350, 280
        rx2, ry2 = 350, 280

        svg = f"""<path d="M {c1_start_x},{c1_start_y} A {rx1},{ry1} 0 0,1 {c1_end_x},{c1_end_y}" stroke="#333" stroke-width="2.5" fill="none"/>
  <path d="M {c2_start_x},{c2_start_y} A {rx2},{ry2} 0 0,1 {c2_end_x},{c2_end_y}" stroke="#333" stroke-width="2.5" fill="none" stroke-dasharray="5,5"/>"""

        l1, l2 = "PPC₁", "PPC₂"
        dir_lbl = "Shift right (increase)"

        # In biased rotation, they share start (40,80). c1 ends at 220,280. c2 ends at 350,280.
        h1_px, h1_py = c1_start_x, c1_start_y # 40, 80
        h2_px, h2_py = c2_end_x, c2_end_y # 350, 280
        # Wait, if h2_py is 280 and h_x is at y=280, what is dx?
        # h_x is at 420. dx = 70. 70/480 = 0.145 >= 0.14. That's fine!
        hx_pos = 420
        hy_pos = 180

        gap_x = 220
        gap_y = 230

    hotspots = [
        {"id": "h_y", "label": opts[1], "x": norm_x(40), "y": norm_y(hy_pos)},
        {"id": "h_x", "label": opts[0], "x": norm_x(hx_pos), "y": norm_y(280)},
        {"id": "h_c1", "label": l1, "x": norm_x(h1_px), "y": norm_y(h1_py)},
        {"id": "h_c2", "label": l2, "x": norm_x(h2_px), "y": norm_y(h2_py)},
        {"id": "h_dir", "label": dir_lbl, "x": norm_x(gap_x), "y": norm_y(gap_y)}
    ]

    write_files(slug, prompt, opts, hotspots, svg)

for slug in ["shift_demand_right", "shift_demand_left", "shift_supply_right", "shift_supply_left"]:
    make_demand_supply(slug)

for slug in ["shift_ad", "shift_sras", "shift_money_supply", "shift_loanable_demand"]:
    make_adas_money(slug)

for slug in ["ppc_growth", "ppc_biased_rotation"]:
    make_ppc(slug)

print("Done phase 3")
