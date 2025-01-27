import tkinter as tk
from tkinter import ttk

# Define the Item class
class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

# Define the items
items = [
    Item("Apple", 0.5, 1),
    Item("Banana", 0.3, 0.5),
    Item("Orange", 0.4, 0.7),
    Item("Grapes", 0.2, 1.2),
    Item("Milk", 1.0, 1.5),
    Item("Bread", 0.8, 1.0),
    Item("Cheese", 0.7, 1.3),
    Item("Chicken", 1.2, 2.0),
    Item("Eggs", 0.3, 0.6),
    Item("Tomato", 0.2, 0.4),
    Item("Potato", 0.4, 0.6),
    Item("Carrot", 0.3, 0.5),
    Item("Spinach", 0.2, 0.3),
    Item("Onion", 0.3, 0.5),
    Item("Cucumber", 0.4, 0.5),
    Item("Watermelon", 1.5, 2.0),
    Item("Pineapple", 0.8, 1.2),
    Item("Strawberry", 0.2, 0.4),
]

weight_limit = 3.0  # Weight limit for carrying capacity

# Initialize the GUI
root = tk.Tk()
root.title("Supermarket Shopping Optimization")

# Left Frame: Table of Items
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(left_frame, text="Item").grid(row=0, column=0)
tk.Label(left_frame, text="Weight (kg)").grid(row=0, column=1)
tk.Label(left_frame, text="Value").grid(row=0, column=2)

for i, item in enumerate(items):
    tk.Label(left_frame, text=item.name).grid(row=i+1, column=0)
    tk.Label(left_frame, text=item.weight).grid(row=i+1, column=1)
    tk.Label(left_frame, text=item.value).grid(row=i+1, column=2)

# Right Frame: Selection and Optimization
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(right_frame, text="Available Items:").grid(row=0, column=0)

# Dropdown for item selection
selected_item = tk.StringVar()
item_dropdown = ttk.Combobox(right_frame, textvariable=selected_item, state="readonly")
item_dropdown['values'] = [item.name for item in items]
item_dropdown.grid(row=1, column=0)

# Add Button
selected_items = []
def add_item():
    item_name = selected_item.get()
    for item in items:
        if item.name == item_name:
            selected_items.append(item)
            update_selected_items()
            break

add_button = tk.Button(right_frame, text="Add", command=add_item)
add_button.grid(row=2, column=0)

# Selected Items List
tk.Label(right_frame, text="Selected Items:").grid(row=3, column=0)
selected_items_list = tk.Text(right_frame, height=10, width=20)
selected_items_list.grid(row=4, column=0)

# Total Weight and Capacity
total_weight_label = tk.Label(right_frame, text="Total Weight: 0.0 kg")
total_weight_label.grid(row=5, column=0)

remaining_capacity_label = tk.Label(right_frame, text=f"Remaining Weight Capacity: {weight_limit} kg")
remaining_capacity_label.grid(row=6, column=0)

def update_selected_items():
    selected_items_list.delete(1.0, tk.END)
    total_weight = sum(item.weight for item in selected_items)
    remaining_capacity = weight_limit - total_weight

    for item in selected_items:
        selected_items_list.insert(tk.END, f"{item.name}\n")

    total_weight_label.config(text=f"Total Weight: {total_weight:.1f} kg")
    remaining_capacity_label.config(text=f"Remaining Weight Capacity: {remaining_capacity:.10f} kg")

# Remove Button
def remove_item():
    if selected_items:
        selected_items.pop()
        update_selected_items()

remove_button = tk.Button(right_frame, text="Remove", command=remove_item)
remove_button.grid(row=7, column=0)

# Optimization Functionality
def optimize():
    global selected_items
    selected_items = knapsack(items, weight_limit)
    update_selected_items()

optimize_button = tk.Button(right_frame, text="Optimize", command=optimize)
optimize_button.grid(row=8, column=0)

# Knapsack Optimization Algorithm
def knapsack(items, max_weight):
    n = len(items)
    dp = [[0] * (int(max_weight * 10) + 1) for _ in range(n+1)]
    
    for i in range(1, n+1):
        for w in range(int(max_weight * 10) + 1):
            if items[i-1].weight * 10 <= w:
                dp[i][w] = max(dp[i-1][w],
                               dp[i-1][int(w - items[i-1].weight * 10)] + items[i-1].value)
            else:
                dp[i][w] = dp[i-1][w]

    # Traceback to find selected items
    w = int(max_weight * 10)
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(items[i-1])
            w -= int(items[i-1].weight * 10)

    return selected

root.mainloop()
