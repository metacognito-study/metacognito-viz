import json
import glob
import os
import sys
import xml.etree.ElementTree as ET
import math
from pathlib import Path

try:
    from svgpathtools import svg2paths
    HAS_SVGPATHTOOLS = True
except ImportError:
    HAS_SVGPATHTOOLS = False

def get_visible_texts(root):
    texts = []
    for elem in root.iter():
        if elem.tag.endswith('text') or elem.tag.endswith('tspan'):
            if elem.get('display') == 'none': continue
            if elem.get('visibility') == 'hidden': continue
            if elem.text:
                texts.append(elem.text.strip())
    return texts

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distance_to_line(px, py, x1, y1, x2, y2):
    l2 = (x1 - x2)**2 + (y1 - y2)**2
    if l2 == 0:
        return distance(px, py, x1, y1)
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2))
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    return distance(px, py, proj_x, proj_y)

def distance_to_rect(px, py, rx, ry, rw, rh):
    nx = max(rx, min(px, rx + rw))
    ny = max(ry, min(py, ry + rh))
    return distance(px, py, nx, ny)

def distance_to_circle(px, py, cx, cy, r):
    d = distance(px, py, cx, cy)
    if d <= r:
        return 0
    return d - r

def _path_polygon_distance(px, py, path_data):
    """Fallback when svgpathtools is unavailable: measure against the path's CONTROL POLYGON.
    A quadratic/cubic control polygon hugs its curve closely, so this is a good approximation --
    and vastly better than returning infinity, which silently marks every curve as blank ink."""
    import re as _re
    nums = [float(n) for n in _re.findall(r'-?\d+\.?\d*', path_data)]
    pts = [(nums[i], nums[i+1]) for i in range(0, len(nums) - 1, 2)]
    if not pts:
        return float('inf')
    best = float('inf')
    for a, b in zip(pts, pts[1:]):
        best = min(best, distance_to_line(px, py, a[0], a[1], b[0], b[1]))
    for a in pts:
        best = min(best, distance(px, py, a[0], a[1]))
    return best

def distance_to_path(px, py, path_data):
    if not HAS_SVGPATHTOOLS:
        return _path_polygon_distance(px, py, path_data)
    from svgpathtools import parse_path
    try:
        path = parse_path(path_data)
        if not path:
            return float('inf')

        # simple heuristic: sample points
        min_d = float('inf')
        # 100 samples per path should be enough for approx distance to 40px
        # We can also sample based on length, but 100 is typically enough for these simple diagrams
        for i in range(100):
            pt = path.point(i / 99.0)
            d = distance(px, py, pt.real, pt.imag)
            if d < min_d:
                min_d = d
        return min_d
    except Exception:
        # FALLBACK: svgpathtools missing/unparseable -> sample the raw numbers in d= as points.
        # Without this the ink test silently returns infinity and every curve reads as blank.
        try:
            import re as _re
            nums=[float(n) for n in _re.findall(r'-?\d+\.?\d*', d_attr)]
            best=float('inf')
            pts=[(nums[i],nums[i+1]) for i in range(0,len(nums)-1,2)]
            # measure along the control polygon, not just its vertices: a quadratic's control
            # polygon hugs the curve, so segment distance approximates curve distance well
            for a,b in zip(pts,pts[1:]):
                best=min(best, distance_to_line(px,py,a[0],a[1],b[0],b[1]))
            for a in pts:
                best=min(best, distance(px,py,a[0],a[1]))
            return best
        except Exception:
            return float('inf')

def parse_float(val, default=0.0):
    try:
        return float(val)
    except:
        return default

def check_nearest_ink(x_px, y_px, root):
    min_dist = float('inf')

    for elem in root.iter():
        tag = elem.tag.split('}')[-1]

        if elem.get('display') == 'none': continue
        if elem.get('visibility') == 'hidden': continue

        if tag == 'line':
            x1 = parse_float(elem.get('x1'))
            y1 = parse_float(elem.get('y1'))
            x2 = parse_float(elem.get('x2'))
            y2 = parse_float(elem.get('y2'))
            d = distance_to_line(x_px, y_px, x1, y1, x2, y2)
            min_dist = min(min_dist, d)

        elif tag == 'rect':
            rx = parse_float(elem.get('x'))
            ry = parse_float(elem.get('y'))
            rw = parse_float(elem.get('width'))
            rh = parse_float(elem.get('height'))

            fill = elem.get('fill', '').lower()
            # Ignore background rects
            if rw >= 480 and rh >= 320 and (fill == '#ffffff' or fill == 'white' or fill == 'none'):
                continue

            d = distance_to_rect(x_px, y_px, rx, ry, rw, rh)
            min_dist = min(min_dist, d)

        elif tag == 'circle':
            cx = parse_float(elem.get('cx'))
            cy = parse_float(elem.get('cy'))
            r = parse_float(elem.get('r'))
            d = distance_to_circle(x_px, y_px, cx, cy, r)
            min_dist = min(min_dist, d)

        elif tag == 'path':
            path_data = elem.get('d', '')
            if path_data:
                d = distance_to_path(x_px, y_px, path_data)
                min_dist = min(min_dist, d)

        elif tag == 'polyline' or tag == 'polygon':
            pts_str = elem.get('points', '')
            if pts_str:
                pts = pts_str.replace(',', ' ').split()
                try:
                    coords = [float(p) for p in pts if p.strip()]
                    if len(coords) >= 2:
                        for k in range(0, len(coords)-2, 2):
                            x1, y1 = coords[k], coords[k+1]
                            x2, y2 = coords[k+2], coords[k+3]
                            d = distance_to_line(x_px, y_px, x1, y1, x2, y2)
                            min_dist = min(min_dist, d)
                        if tag == 'polygon' and len(coords) >= 4:
                            x1, y1 = coords[-2], coords[-1]
                            x2, y2 = coords[0], coords[1]
                            d = distance_to_line(x_px, y_px, x1, y1, x2, y2)
                            min_dist = min(min_dist, d)
                except:
                    pass

        elif tag == 'text':
            tx = parse_float(elem.get('x'))
            ty = parse_float(elem.get('y'))
            d = distance(x_px, y_px, tx, ty)
            min_dist = min(min_dist, d)

    return min_dist <= 40.0

def main():
    # Find all _coords files
    coords_files = []
    for p in Path('.').rglob('*.json'):
        if '_coords_WIP' in str(p): continue   # stale pre-fix snapshot, not a live coords file
        if '_coords' in str(p) or 'coords' in p.parts:
            # check if it's a file and avoid node_modules etc
            if p.is_file() and 'node_modules' not in str(p):
                coords_files.append(str(p))

    if not coords_files:
        print("No coords files found.")
        sys.exit(0)

    any_fail = False

    for cfile in sorted(coords_files):
        basename = os.path.basename(cfile)
        row_num = basename.split('.')[0]

        # matching _diagrams/**/*.svg
        if row_num.startswith('econ_'):
            cand = os.path.join('_diagrams','econ', row_num[5:] + '.svg')
            svg_files = [cand] if os.path.exists(cand) else []
        elif row_num.startswith('chem_'):
            cand = os.path.join('_diagrams','chem_cmp', row_num[5:] + '.svg')
            svg_files = [cand] if os.path.exists(cand) else []
        elif row_num.startswith('table_'):
            cand = os.path.join('_diagrams','tables', row_num[6:] + '.svg')
            svg_files = [cand] if os.path.exists(cand) else []
        else:
            svg_files = glob.glob(f'_diagrams/**/row_{row_num}.svg', recursive=True) + glob.glob(f'_diagrams/**/{row_num}.svg', recursive=True)
        if not svg_files:
            # try finding ANY svg ending in that row_num
            svg_files = list(Path('_diagrams').rglob(f'*{row_num}.svg'))
            svg_files = [str(f) for f in svg_files]

        if not svg_files:
            print(f"FAIL {cfile}: No matching SVG found")
            any_fail = True
            continue

        svg_file = svg_files[0]

        try:
            tree = ET.parse(svg_file)
            root = tree.getroot()
            if root.get('viewBox') != '0 0 480 320':
                print(f"FAIL {cfile}: viewBox is not '0 0 480 320'")
                any_fail = True
                continue
        except Exception as e:
            print(f"FAIL {cfile}: SVG failed to parse: {e}")
            any_fail = True
            continue

        try:
            with open(cfile, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"FAIL {cfile}: JSON failed to parse: {e}")
            any_fail = True
            continue

        if 'hotspots' not in data:
            print(f"FAIL {cfile}: JSON has no 'hotspots'")
            any_fail = True
            continue

        fail_reason = None
        hotspots = data['hotspots']
        for i, h in enumerate(hotspots):
            if 'id' not in h or 'label' not in h or 'x' not in h or 'y' not in h:
                fail_reason = f"Hotspot {i} missing id/label/x/y"
                break
            if not isinstance(h['x'], (int, float)) or not isinstance(h['y'], (int, float)):
                fail_reason = f"Hotspot {i} x or y is not numeric"
                break

        if fail_reason:
            print(f"FAIL {cfile}: {fail_reason}")
            any_fail = True
            continue

        for i, h in enumerate(hotspots):
            x, y = h['x'], h['y']
            if not (0.06 <= x <= 0.94):
                fail_reason = f"Hotspot '{h['id']}' x {x} out of bounds"
                break
            if not (0.08 <= y <= 0.92):
                fail_reason = f"Hotspot '{h['id']}' y {y} out of bounds"
                break

        if fail_reason:
            print(f"FAIL {cfile}: {fail_reason}")
            any_fail = True
            continue

        for i in range(len(hotspots)):
            for j in range(i + 1, len(hotspots)):
                h1, h2 = hotspots[i], hotspots[j]
                dx = abs(h1['x'] - h2['x'])
                dy = abs(h1['y'] - h2['y'])
                if dx < 0.14 and dy < 0.16:
                    fail_reason = f"Hotspots '{h1['id']}' and '{h2['id']}' too close (dx={dx:.3f}, dy={dy:.3f})"
                    break
            if fail_reason:
                break

        if fail_reason:
            print(f"FAIL {cfile}: {fail_reason}")
            any_fail = True
            continue

        # 5. ANSWER LEAK
        visible_texts = get_visible_texts(root)
        for h in hotspots:
            label = h['label']
            idx = label.find('(')
            if idx != -1:
                head_phrase = label[:idx].strip()
            else:
                head_phrase = label.strip()

            for vt in visible_texts:
                if vt == head_phrase:
                    fail_reason = f"Answer leak: '{head_phrase}' found in SVG text"
                    break
            if fail_reason:
                break

        if fail_reason:
            print(f"FAIL {cfile}: {fail_reason}")
            any_fail = True
            continue

        # 6. NEAREST-INK
        for h in hotspots:
            x_px = h['x'] * 480
            y_px = h['y'] * 320
            if not check_nearest_ink(x_px, y_px, root):
                fail_reason = f"Hotspot '{h['id']}' is not near any ink"
                break

        if fail_reason:
            print(f"FAIL {cfile}: {fail_reason}")
            any_fail = True
            continue

        print(f"PASS {cfile}")

    if any_fail:
        sys.exit(1)

if __name__ == '__main__':
    main()
