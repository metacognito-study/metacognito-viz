import json

with open('_coords/1606.json', 'r') as f:
    data = json.load(f)

new_hotspots = [
    {
        "id": "b2_1",
        "label": "Activation energy Ea (height from reactants to peak)",
        "x": 170 / 480, # 0.354
        "y": 160 / 320  # 0.500
    },
    {
        "id": "b2_2",
        "label": "Transition state position on the curve",
        "x": 280 / 480, # 0.583
        "y": 60 / 320   # 0.188  -> We will draw a label/arrow at (280, 60) pointing to peak (240,112). Or dot at 240, 112. Wait, 'ts' is at x=0.5, y=0.12 (x=240, y=38.4). 
        # Let's check distances:
        # ts: (0.500, 0.120)
        # peak: (0.500, 0.350)
        # b2_2 needs to be away from 0.5, 0.12 and 0.5, 0.35.
        # How about x = 200/480 = 0.417? dx to 0.500 is 0.083 < 0.14. dy needs to be >= 0.16. 
        # ts y=0.12, peak y=0.35. If we put b2_2 at y=0.51? 0.51-0.35 = 0.16. But then it overlaps with b2_1 (0.500).
        # What if we put b2_2 at x=340/480 = 0.708? dx to 0.500 is 0.208 > 0.14! So x=340, y=112 (y=0.35).
    },
    {
        "id": "b2_3",
        "label": "Enthalpy change ΔH (products \u2013 reactants)",
        "x": 100 / 480, # 0.208
        "y": 228 / 320  # 0.713
    }
]

# Let's adjust b2_2 and b2_3 to satisfy dx >= 0.14 or dy >= 0.16.
# b2_3 vs reac (0.150, 0.619):
# b2_3 x=0.208, y=0.713. dy = 0.094 < 0.16. dx = 0.058 < 0.14. Fail.
# Let's move b2_3 x to be 0.150 + 0.142 = 0.292. (x = 140/480).
# Let's move b2_3 y to remain centered between 208 and 249.6 (y=228.8/320 = 0.715).
# So b2_3 -> x=140/480 (0.292), y=228.8/320 (0.715). dx with reac is 0.142 > 0.14.

# b2_2 vs peak (0.500, 0.350) and ts (0.500, 0.120):
# Let's put b2_2 at x=170/480 (0.354), y=60/320 (0.188). 
# Wait, b2_1 is at x=0.354, y=0.500. dy between b2_1 and b2_2 is 0.500 - 0.188 = 0.312 > 0.16.
# dx between b2_2 (0.354) and peak (0.500) is 0.146 > 0.14.
# dx between b2_2 (0.354) and ts (0.500) is 0.146 > 0.14.
# Perfect.

new_hotspots[0]['x'] = 170 / 480
new_hotspots[0]['y'] = 160 / 320

new_hotspots[1]['x'] = 330 / 480 # 0.688. 0.688 - 0.5 = 0.188 > 0.14
new_hotspots[1]['y'] = 112 / 320 # 0.350. (dx is sufficient)

new_hotspots[2]['x'] = 140 / 480 # 0.292. 0.292 - 0.150 = 0.142 > 0.14
new_hotspots[2]['y'] = 228.8 / 320 # 0.715.

# Verify against prod (0.850, 0.750):
# b2_2 (0.688, 0.350) to prod: dx = 0.162 > 0.14.
# b2_3 (0.292, 0.715) to prod: dx = 0.558 > 0.14.
# b2_1 (0.354, 0.500) to b2_3 (0.292, 0.715): dx = 0.062 < 0.14, dy = 0.215 > 0.16! OK.

for hotspot in new_hotspots:
    hotspot['x'] = round(hotspot['x'], 3)
    hotspot['y'] = round(hotspot['y'], 3)

data['hotspots'].extend(new_hotspots)

if 'options' not in data:
    data['options'] = [
        "Reactants",
        "Transition state (‡)",
        "Products",
        "Maximum energy point",
        "Intermediate",
        "Activated complex",
        "Equilibrium state"
    ]

# The prompt options must have all correct answers and distractors for the variant.
new_options = [
    "Activation energy Ea (height from reactants to peak)",
    "Height = energy released by the reaction",
    "Height tells you if reaction is exothermic or endothermic",
    "The taller the peak, the faster the reaction always goes",
    "Transition state position on the curve",
    "Transition state is where the curve starts to level off",
    "Transition state occurs at the endpoint of the curve",
    "Transition state is the same as the product energy level",
    "Enthalpy change ΔH (products \u2013 reactants)",
    "ΔH is the height from reactants to the peak",
    "ΔH is determined by how high the peak rises",
    "ΔH and Ea are the same value on a reaction coordinate curve"
]
for opt in new_options:
    if opt not in data['options']:
        data['options'].append(opt)

with open('_coords/1606.json', 'w') as f:
    json.dump(data, f, indent=1)
