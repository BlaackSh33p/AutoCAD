import tkinter as tk
from tkinter import ttk, messagebox
import math

# Preset lamp lumen values (for convenience)
lamp_lumens = {
    "Fluorescent 2ft (~1600 lm)": 1600,
    "Fluorescent 4ft (~3350 lm)": 3350
}

# Estimate UF from Room Index (K)
def estimate_UF(K):
    if K < 1: return 0.5
    elif K < 2: return 0.6
    elif K < 3: return 0.7
    elif K < 5: return 0.75
    else: return 0.8

def calculate_lamps():
    try:
        # Inputs
        length = float(length_entry.get())
        width = float(width_entry.get())
        height = float(height_entry.get())
        lux_required = float(lux_entry.get())
        lamp_type = lamp_type_var.get()

        # Decide lumen value
        custom_lumen = custom_lumen_entry.get()
        if custom_lumen.strip():
            F = float(custom_lumen)   # use manual lumen input
            lamp_name = f"Custom Lamp ({F} lm)"
        else:
            if lamp_type not in lamp_lumens:
                messagebox.showerror("Error", "Please select a lamp type or enter custom lumen.")
                return
            F = lamp_lumens[lamp_type]
            lamp_name = lamp_type

        workplane = 0.8
        Hm = height - workplane

        # Room Index
        K = (length * width) / (Hm * (length + width))
        UF = estimate_UF(K)
        MF = 0.8

        # Room area
        A = length * width

        # Lumen method
        N = (lux_required * A) / (F * UF * MF)
        lamps_needed = int(N) + (0 if N.is_integer() else 1)

        # Spacing recommendation
        SHR = 1.25
        max_spacing = SHR * Hm

        # Layout suggestion
        rows = max(1, round(length / max_spacing))
        cols = max(1, round(width / max_spacing))
        layout_lamps = rows * cols

        if layout_lamps < lamps_needed:
            if (length / (rows + 1)) > (width / (cols + 1)):
                rows += 1
            else:
                cols += 1
            layout_lamps = rows * cols

        spacing_length = length / rows
        spacing_width = width / cols

        # Result
        result_label.config(
            text=(
                f"👉 You need ~{lamps_needed} {lamp_name} lamps.\n\n"
                f"📐 Room Index (K): {K:.2f}\n"
                f"⚡ Estimated UF: {UF:.2f}\n"
                f"🔆 Max lamp spacing: {max_spacing:.2f} m\n\n"
                f"🗺️ Suggested Layout: {rows} rows × {cols} columns = {layout_lamps} lamps\n"
                f"   ➤ Spacing along length: {spacing_length:.2f} m\n"
                f"   ➤ Spacing along width: {spacing_width:.2f} m"
            )
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Illumination Design Assistant")
root.geometry("550x600")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
style.configure("TCombobox", font=("Segoe UI", 11))

# Title
ttk.Label(root, text="💡 Illumination Design Assistant", 
          font=("Segoe UI", 14, "bold"), foreground="#004080").pack(pady=10)

frame = ttk.Frame(root, padding=15)
frame.pack()

# Inputs
ttk.Label(frame, text="Room length (m):").grid(row=0, column=0, sticky="w", pady=5)
length_entry = ttk.Entry(frame, width=15); length_entry.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Room width (m):").grid(row=1, column=0, sticky="w", pady=5)
width_entry = ttk.Entry(frame, width=15); width_entry.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Room height (m):").grid(row=2, column=0, sticky="w", pady=5)
height_entry = ttk.Entry(frame, width=15); height_entry.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Required Lux (lx):").grid(row=3, column=0, sticky="w", pady=5)
lux_entry = ttk.Entry(frame, width=15); lux_entry.grid(row=3, column=1, pady=5)

# Lamp type (dropdown)
ttk.Label(frame, text="Lamp Type (preset):").grid(row=4, column=0, sticky="w", pady=5)
lamp_type_var = tk.StringVar()
lamp_dropdown = ttk.Combobox(frame, textvariable=lamp_type_var, state="readonly", width=28)
lamp_dropdown["values"] = list(lamp_lumens.keys())
lamp_dropdown.grid(row=4, column=1, pady=5)

# Custom lumen input
ttk.Label(frame, text="Custom Lumen (lm):").grid(row=5, column=0, sticky="w", pady=5)
custom_lumen_entry = ttk.Entry(frame, width=15)
custom_lumen_entry.grid(row=5, column=1, pady=5)
ttk.Label(frame, text="(Optional: overrides preset)").grid(row=6, column=1, sticky="w")

# Calculate button
ttk.Button(root, text="Calculate", command=calculate_lamps).pack(pady=15)

# Result label
result_label = ttk.Label(root, text="Enter details and click Calculate.", 
                         font=("Segoe UI", 12, "italic"), foreground="#006600", 
                         wraplength=500, justify="left")
result_label.pack(pady=10)

root.mainloop()

