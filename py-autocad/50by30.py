import ezdxf

# === Parameters ===
plot_width = 50
plot_height = 30
wall_thickness = 0.5

# Room dimensions (can be adjusted)
rooms = {
    "Bedroom1": {"x": 0, "y": 0, "w": 12, "h": 12},
    "Bedroom2": {"x": 12, "y": 0, "w": 12, "h": 12},
    "Living":   {"x": 0, "y": 12, "w": 24, "h": 18},
}

doors = [
    {"x": 12, "y": 6, "w": 3, "orientation": "vertical"},   # door between Bedroom1 & Bedroom2
    {"x": 6, "y": 12, "w": 3, "orientation": "horizontal"}, # door into Living room
]

windows = [
    {"x": 6, "y": 30, "w": 4, "orientation": "horizontal"}, # window on top wall
]

# === DXF Creation ===
doc = ezdxf.new(dxfversion="R2010")
msp = doc.modelspace()

# Draw plot boundary
msp.add_lwpolyline([(0,0), (plot_width,0), (plot_width,plot_height), (0,plot_height)], close=True)

# Draw rooms
for name, r in rooms.items():
    x, y, w, h = r["x"], r["y"], r["w"], r["h"]
    msp.add_lwpolyline([(x,y),(x+w,y),(x+w,y+h),(x,y+h)], close=True)

# Draw doors
for d in doors:
    if d["orientation"] == "vertical":
        msp.add_line((d["x"], d["y"]-d["w"]/2), (d["x"], d["y"]+d["w"]/2))
    else:
        msp.add_line((d["x"]-d["w"]/2, d["y"]), (d["x"]+d["w"]/2, d["y"]))

# Draw windows
for w in windows:
    if w["orientation"] == "horizontal":
        msp.add_line((w["x"]-w["w"]/2, w["y"]), (w["x"]+w["w"]/2, w["y"]))
    else:
        msp.add_line((w["x"], w["y"]-w["w"]/2), (w["x"], w["y"]+w["w"]/2))

doc.saveas("parametric_house.dxf")
print("Draft saved as parametric_house.dxf")
