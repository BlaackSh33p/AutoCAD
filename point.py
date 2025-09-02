import pandas as pd
from pyautocad import Autocad, APoint

# Initialize AutoCAD connection
acad = Autocad(create_if_not_exists=True)
acad.prompt("Python-AutoCAD Electrical Layout Started\n")

# Load netlist
netlist = pd.read_csv('netlist.csv')

# Dictionary to store AutoCAD points for each component
component_points = {}

# Function to insert symbols
def insert_symbol(name, comp_type, x, y):
    point = APoint(x, y)
    component_points[name] = point
    
    # Example: Draw a simple circle for symbol
    if comp_type.lower() == 'light':
        acad.model.AddCircle(point, 2)  # radius = 2
    elif comp_type.lower() == 'switch':
        acad.model.AddRectangle(point, 2, 2)  # square switch
    
    # Label the component
    acad.model.AddText(name, APoint(x, y + 3), 1)  # text height = 1

# Step 1: Insert all components
for idx, row in netlist.iterrows():
    insert_symbol(row['Component'], row['Type'], row['X'], row['Y'])

# Step 2: Draw connections
for idx, row in netlist.iterrows():
    comp = row['Component']
    target = row['Connection']
    if target in component_points:
        start = component_points[comp]
        end = component_points[target]
        acad.model.AddLine(start, end)

# Step 3: Basic Validation
errors = []
for idx, row in netlist.iterrows():
    if row['Connection'] not in component_points:
        errors.append(f"Component {row['Component']} connected to missing {row['Connection']}")

if errors:
    print("Validation Errors Found:")
    for e in errors:
        print(e)
else:
    print("Layout validation passed. All connections are valid.")

