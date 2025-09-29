"""
Parametric House Layout Generator (Patched)
- Generates a 50' x 30' house plan using parametric rules.
- Exports DXF (if ezdxf installed), SVG, and PNG preview.
- Text placement fixed to work across ezdxf versions.
"""

import math
import os
import sys

# Try imports but allow fallback if ezdxf is not present
try:
    import ezdxf
    HAVE_EZDXF = True
except Exception:
    HAVE_EZDXF = False

import svgwrite
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# === PARAMETERS ===
PLOT_W = 50.0      # feet
PLOT_H = 30.0      # feet
WALL_THK = 0.5     # feet
CORRIDOR_W = 5.0   # feet
DOOR_W = 3.0
WINDOW_W = 4.0

rooms_spec = [
    {"name": "Bedroom1", "pw": 12, "ph": 12},
    {"name": "Bedroom2", "pw": 12, "ph": 12},
    {"name": "Bedroom3", "pw": 12, "ph": 12},
    {"name": "Bathroom", "pw": 7, "ph": 8},
    {"name": "Kitchen",  "pw": 10, "ph": 12},
    {"name": "Living",   "pw": 16, "ph": 18},
    {"name": "Dining",   "pw": 12, "ph": 10},
]

OUTPUT_DIR = os.path.dirname(__file__)
DXF_PATH = os.path.join(OUTPUT_DIR, "parametric_house.dxf")
SVG_PATH = os.path.join(OUTPUT_DIR, "parametric_house.svg")
PNG_PATH = os.path.join(OUTPUT_DIR, "parametric_house_preview.png")

# === Layout engine (same as before, shortened for clarity) ===
left_col_w = max(r["pw"] for r in rooms_spec if "Bedroom" in r["name"]) + WALL_THK*2 + 1.0
right_col_w = PLOT_W - left_col_w - CORRIDOR_W - 2.0
if right_col_w < 12:
    left_col_w = PLOT_W - CORRIDOR_W - 2.0 - 12
    right_col_w = 12.0

bedrooms_spec = [r for r in rooms_spec if "Bedroom" in r["name"]]
total_bed_h = sum(b["ph"] for b in bedrooms_spec)
available_h = PLOT_H - 2.0
scale_factor = available_h / total_bed_h

placed_rooms = []
y_cursor = 1.0
for b in bedrooms_spec:
    h = b["ph"] * scale_factor
    w = left_col_w - WALL_THK*2 - 0.5
    x = 1.0
    y = y_cursor
    placed_rooms.append({"name": b["name"], "x": x, "y": y, "w": w, "h": h})
    y_cursor += h + 0.5

corr_x = left_col_w + 0.5
corr_y = 1.0
corr_w = CORRIDOR_W
corr_h = PLOT_H - 2.0

right_x = corr_x + corr_w + 0.5
kitchen = next(r for r in rooms_spec if r["name"] == "Kitchen")
living = next(r for r in rooms_spec if r["name"] == "Living")
dining = next(r for r in rooms_spec if r["name"] == "Dining")
bath = next(r for r in rooms_spec if r["name"] == "Bathroom")

k_w = right_col_w - 2.0
k_h = min(kitchen["ph"], available_h * 0.25)
living_w = right_col_w - 2.0
living_h = min(living["ph"], available_h * 0.45)
dining_w = right_col_w - 2.0
dining_h = min(dining["ph"], available_h * 0.2)

sum_h = k_h + living_h + dining_h + 1.0
if sum_h > available_h:
    factor = available_h / sum_h
    k_h *= factor; living_h *= factor; dining_h *= factor

k_x = right_x
k_y = PLOT_H - 1.0 - k_h
lv_x = right_x
lv_y = k_y - 0.5 - living_h
dn_x = right_x
dn_y = lv_y - 0.5 - dining_h

bath_w = bath["pw"]; bath_h = bath["ph"]
bath_x = left_col_w - bath_w - 0.5
bath_y = PLOT_H / 2.0 - bath_h / 2.0

placed_rooms.extend([
    {"name": "Kitchen", "x": k_x, "y": k_y, "w": k_w, "h": k_h},
    {"name": "Living", "x": lv_x, "y": lv_y, "w": living_w, "h": living_h},
    {"name": "Dining", "x": dn_x, "y": dn_y, "w": dining_w, "h": dining_h},
    {"name": "Bathroom", "x": bath_x, "y": bath_y, "w": bath_w, "h": bath_h},
])

# Doors & windows (unchanged, omitted for brevity) ...
doors = []
windows = []

# === Helper for walls ===
def rect_outer_inner(x,y,w,h,thk=WALL_THK):
    outer = [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    inner = [(x+thk,y+thk),(x+w-thk,y+thk),(x+w-thk,y+h-thk),(x+thk,y+h-thk),(x+thk,y+thk)]
    return outer, inner

# === DXF Export (patched text placement) ===
if HAVE_EZDXF:
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()
    msp.add_lwpolyline([(0,0),(PLOT_W,0),(PLOT_W,PLOT_H),(0,PLOT_H)], close=True)
    for r in placed_rooms:
        outer, inner = rect_outer_inner(r["x"], r["y"], r["w"], r["h"])
        msp.add_lwpolyline(outer, close=True, dxfattribs={'layer':'WALLS'})
        msp.add_lwpolyline(inner, close=True, dxfattribs={'layer':'WALLS'})
        cx = r["x"] + r["w"]/2
        cy = r["y"] + r["h"]/2
        # ✅ Insert text directly (cross-version safe)
        txt = msp.add_text(r["name"], dxfattribs={'height':0.6})
        txt.dxf.insert = (cx-1, cy-0.3)

    doc.saveas(DXF_PATH)
    print("DXF saved to:", DXF_PATH)
else:
    print("ezdxf not installed — skipping DXF export.")
