import tkinter as tk
from tkinter import ttk, messagebox
from asset_module import Asset
import logic
import datetime

logic.init_db()


root = tk.Tk()
root.title("NEXUS CORP - IT Asset Management")
root.geometry("750x550")
root.resizable(False, False)
FONT = ("Segoe UI", 10)

# ---------------- Helper Functions ----------------
def clear_fields():
    name_entry.delete(0, tk.END)
    brand_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, "YYYY-MM-DD")

def add_asset_ui():
    try:
        date_val = date_entry.get()
        if len(name_entry.get()) == 0 or len(brand_entry.get()) == 0:
            messagebox.showerror("Error", "Name and Brand cannot be empty")
            return
        if len(date_val) != 10 or date_val[4] != '-' or date_val[7] != '-':
            messagebox.showerror("Error", "Date format must be YYYY-MM-DD")
            return

        asset = Asset(
            asset_id=None,
            name=name_entry.get(),
            asset_type=type_combo.get(),
            brand=brand_entry.get(),
            status=status_combo.get(),
            purchase_date=date_entry.get()
        )
        logic.add_asset(asset)
        messagebox.showinfo("Success", "Asset Added Successfully")
        clear_fields()
        refresh_assets_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_asset_ui():
    selected = assets_table.focus()
    if not selected:
        messagebox.showerror("Error", "Select an asset to delete")
        return
    data = assets_table.item(selected)['values']
    logic.delete_asset(data[0])
    messagebox.showinfo("Deleted", f"Asset ID {data[0]} deleted")
    refresh_assets_table()

def search_asset_ui():
    asset_id = search_entry.get()
    if not asset_id.isdigit():
        messagebox.showerror("Error", "Enter a valid Asset ID")
        return
    data = logic.search_asset(int(asset_id))
    if data:
        assets_table.selection_set(assets_table.get_children()[0])
        clear_fields()
        name_entry.insert(0, data[1])
        type_combo.set(data[2])
        brand_entry.insert(0, data[3])
        status_combo.set(data[4])
        date_entry.insert(0, data[5])
    else:
        messagebox.showinfo("Not Found", "Asset not found")

def refresh_assets_table():
    for row in assets_table.get_children():
        assets_table.delete(row)
    for row in logic.fetch_all_assets():
        assets_table.insert("", tk.END, values=row)

def open_dashboard():
    win = tk.Toplevel(root)
    win.title("Dashboard")
    win.geometry("320x250")
    total, working, repair, disposed = logic.dashboard_counts()

    tk.Label(win, text="Dashboard", font=("Segoe UI", 14, "bold")).pack(pady=10)
    tk.Label(win, text=f"Total Assets: {total}", font=FONT).pack()
    tk.Label(win, text=f"Working: {working}", font=FONT).pack()
    tk.Label(win, text=f"In Repair: {repair}", font=FONT).pack()
    tk.Label(win, text=f"Disposed: {disposed}", font=FONT).pack()

    # Progress bars
    if total > 0:
        tk.Label(win, text="Working %").pack(pady=2)
        pb = ttk.Progressbar(win, length=200, maximum=100, value=(working/total)*100)
        pb.pack()
        tk.Label(win, text="In Repair %").pack(pady=2)
        pb2 = ttk.Progressbar(win, length=200, maximum=100, value=(repair/total)*100)
        pb2.pack()
        tk.Label(win, text="Disposed %").pack(pady=2)
        pb3 = ttk.Progressbar(win, length=200, maximum=100, value=(disposed/total)*100)
        pb3.pack()

# ---------------- Front Page ----------------
front_frame = tk.Frame(root)
front_frame.pack(fill="both", expand=True)

tk.Label(front_frame, text="NEXUS CORP", font=("Segoe UI", 20, "bold")).pack(pady=20)
tk.Label(front_frame, text="IT ASSET MANAGEMENT SYSTEM", font=("Segoe UI", 14)).pack(pady=10)

tk.Button(front_frame, text="Open Asset Management", width=25, command=lambda: front_frame.pack_forget() or asset_frame.pack(fill="both", expand=True)).pack(pady=10)
tk.Button(front_frame, text="View Dashboard", width=25, command=open_dashboard).pack(pady=10)

# ---------------- Asset Management Page ----------------
asset_frame = tk.Frame(root)

frame = tk.Frame(asset_frame)
frame.pack(pady=10)

# Labels
labels = ["Name", "Type", "Brand", "Status", "Purchase Date"]
for i, txt in enumerate(labels):
    tk.Label(frame, text=txt, font=FONT).grid(row=i, column=0, sticky="w", pady=4)

name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1)

type_combo = ttk.Combobox(frame, values=["Computer", "Laptop", "Printer", "Router", "Other"])
type_combo.grid(row=1, column=1)
type_combo.current(0)

brand_entry = tk.Entry(frame)
brand_entry.grid(row=2, column=1)

status_combo = ttk.Combobox(frame, values=["Working", "In Repair", "Disposed"])
status_combo.grid(row=3, column=1)
status_combo.current(0)

date_entry = tk.Entry(frame)
date_entry.insert(0, "YYYY-MM-DD")
date_entry.grid(row=4, column=1)

tk.Button(frame, text="Add Asset", width=15, command=add_asset_ui).grid(row=5, column=0, pady=10)
tk.Button(frame, text="Delete Selected", width=15, command=delete_asset_ui).grid(row=5, column=1, pady=10)

# Search section
search_frame = tk.Frame(asset_frame)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Search Asset by ID:", font=FONT).grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Search", command=search_asset_ui).grid(row=0, column=2, padx=5)

# Assets Table
assets_table = ttk.Treeview(asset_frame, columns=("ID", "Name", "Type", "Brand", "Status", "Date"), show="headings")
for col in ("ID", "Name", "Type", "Brand", "Status", "Date"):
    assets_table.heading(col, text=col)
    assets_table.column(col, width=110)
assets_table.pack(pady=10, fill="x")
refresh_assets_table()

# Navigation Buttons
nav_frame = tk.Frame(asset_frame)
nav_frame.pack(pady=10)
tk.Button(nav_frame, text="Back to Home", width=20, command=lambda: asset_frame.pack_forget() or front_frame.pack(fill="both", expand=True)).grid(row=0, column=0, padx=5)
tk.Button(nav_frame, text="Dashboard", width=20, command=open_dashboard).grid(row=0, column=1, padx=5)

root.mainloop()
