import tkinter as tk
from tkinter import ttk, messagebox

# Lamp lumen values
lamp_lumens = {
    "Fluorescent 2ft (~1600 lm)": 1600,   # ~18W tube
    "Fluorescent 4ft (~3350 lm)": 3350    # ~36W tube
}

# Calculation function
def calculate_lamps():
    try:
        length = float(length_entry.get())
        width = float(width_entry.get())
        lux_required = float(lux_entry.get())
        lamp_type = lamp_type_var.get()

        if lamp_type not in lamp_lumens:
            messagebox.showerror("Error", "Please select a lamp type.")
            return

        F = lamp_lumens[lamp_type]
        UF, MF = 0.7, 0.8  # defaults
        A = length * width
        N = (lux_required * A) / (F * UF * MF)

        lamps_needed = int(N) + (0 if N.is_integer() else 1)
        result_label.config(
            text=f"👉 You need {lamps_needed} {lamp_type} lamps."
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Lighting Calculator - Fluorescent Lamps")
root.geometry("420x350")
root.resizable(False, False)

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
style.configure("TCombobox", font=("Segoe UI", 11))

# Title
title_label = ttk.Label(
    root, 
    text="💡 Lighting Calculator", 
    font=("Segoe UI", 14, "bold"), 
    foreground="#004080"
)
title_label.pack(pady=10)

# Frame for inputs
frame = ttk.Frame(root, padding=15)
frame.pack()

# Room length
ttk.Label(frame, text="Room length (m):").grid(row=0, column=0, sticky="w", pady=5)
length_entry = ttk.Entry(frame, width=15)
length_entry.grid(row=0, column=1, pady=5)

# Room width
ttk.Label(frame, text="Room width (m):").grid(row=1, column=0, sticky="w", pady=5)
width_entry = ttk.Entry(frame, width=15)
width_entry.grid(row=1, column=1, pady=5)

# Lux level
ttk.Label(frame, text="Required Lux (lx):").grid(row=2, column=0, sticky="w", pady=5)
lux_entry = ttk.Entry(frame, width=15)
lux_entry.grid(row=2, column=1, pady=5)

# Lamp type
ttk.Label(frame, text="Lamp Type:").grid(row=3, column=0, sticky="w", pady=5)
lamp_type_var = tk.StringVar()
lamp_dropdown = ttk.Combobox(
    frame, textvariable=lamp_type_var, state="readonly", width=25
)
lamp_dropdown["values"] = list(lamp_lumens.keys())
lamp_dropdown.grid(row=3, column=1, pady=5)

# Calculate button
calc_button = ttk.Button(root, text="Calculate", command=calculate_lamps)
calc_button.pack(pady=15)

# Result label
result_label = ttk.Label(
    root, 
    text="Enter details and click Calculate.", 
    font=("Segoe UI", 12, "italic"), 
    foreground="#006600", 
    wraplength=380
)
result_label.pack(pady=10)

# Run app
root.mainloop()

