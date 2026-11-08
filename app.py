
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ---------------- COLORS ----------------
BG = "#F3F5FA"
NAVY = "#14213D"
BLUE = "#243B64"
WHITE = "#FFFFFF"
BLACK = "#172033"
LIGHT_BLUE = "#E8EEFA"
GREEN = "#16A085"
RED = "#E74C3C"
ORANGE = "#F39C12"
GRAY = "#01060F"

tasks = []
selected_task = None

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("TaskFlow | To-Do List")
root.geometry("1100x720")
root.minsize(950, 650)
root.configure(bg=BG)

# ---------------- FUNCTIONS ----------------
def update_statistics():
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed

    total_label.config(text=str(total))
    completed_label.config(text=str(completed))
    pending_label.config(text=str(pending))

    progress = int((completed / total) * 100) if total else 0
    progress_label.config(text=f"{progress}% completed")


def refresh_tasks():
    task_table.delete(*task_table.get_children())

    search = search_entry.get().lower()
    filter_value = filter_box.get()

    for index, task in enumerate(tasks):
        if search not in task["title"].lower():
            continue

        if filter_value == "Pending" and task["completed"]:
            continue
        if filter_value == "Completed" and not task["completed"]:
            continue

        status = "Completed" if task["completed"] else "Pending"

        task_table.insert(
            "",
            "end",
            iid=str(index),
            values=(
                task["title"],
                task["category"],
                task["priority"],
                status,
                task["date"]
            )
        )

    update_statistics()


def clear_fields():
    global selected_task
    selected_task = None
    title_entry.delete(0, tk.END)
    category_box.set("Study")
    priority_box.set("Medium")
    task_table.selection_remove(task_table.selection())


def add_task():
    title = title_entry.get().strip()

    if not title:
        messagebox.showwarning("Missing Task", "Please enter a task!")
        return

    tasks.append({
        "title": title,
        "category": category_box.get(),
        "priority": priority_box.get(),
        "completed": False,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    clear_fields()
    refresh_tasks()
    messagebox.showinfo("Success", "Task added successfully!")


def select_task(event):
    global selected_task

    selected = task_table.selection()

    if not selected:
        return

    selected_task = int(selected[0])
    task = tasks[selected_task]

    title_entry.delete(0, tk.END)
    title_entry.insert(0, task["title"])
    category_box.set(task["category"])
    priority_box.set(task["priority"])


def update_task():
    if selected_task is None:
        messagebox.showwarning("Select Task", "Please select a task first!")
        return

    title = title_entry.get().strip()

    if not title:
        messagebox.showwarning("Missing Task", "Task name cannot be empty!")
        return

    tasks[selected_task]["title"] = title
    tasks[selected_task]["category"] = category_box.get()
    tasks[selected_task]["priority"] = priority_box.get()

    clear_fields()
    refresh_tasks()
    messagebox.showinfo("Updated", "Task updated successfully!")


def delete_task():
    selected = task_table.selection()

    if not selected:
        messagebox.showwarning("Select Task", "Please select a task!")
        return

    index = int(selected[0])

    if messagebox.askyesno("Confirm", "Delete this task?"):
        tasks.pop(index)
        clear_fields()
        refresh_tasks()


def complete_task():
    selected = task_table.selection()

    if not selected:
        messagebox.showwarning("Select Task", "Please select a task!")
        return

    index = int(selected[0])
    tasks[index]["completed"] = not tasks[index]["completed"]

    clear_fields()
    refresh_tasks()


def reset_search():
    search_entry.delete(0, tk.END)
    filter_box.set("All")
    refresh_tasks()


# ---------------- HEADER ----------------
header = tk.Frame(root, bg=NAVY, height=110)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="TASKFLOW",
    font=("Arial", 25, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w", padx=35, pady=(17, 0))

tk.Label(
    header,
    text="Organize your day. Achieve your goals.",
    font=("Arial", 11),
    bg=NAVY,
    fg="#C5D2E8"
).pack(anchor="w", padx=37)

date_label = tk.Label(
    header,
    text=datetime.now().strftime("%A, %d %B %Y"),
    font=("Arial", 11, "bold"),
    bg=NAVY,
    fg=WHITE
)
date_label.place(relx=0.98, rely=0.5, anchor="e")

# ---------------- MAIN CONTAINER ----------------
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=30, pady=20)

# ---------------- STATISTICS ----------------
stats = tk.Frame(main, bg=BG)
stats.pack(fill="x", pady=(0, 20))

def create_stat(parent, title, color):
    card = tk.Frame(parent, bg=WHITE, highlightbackground="#E0E5EF",
                    highlightthickness=1)
    card.pack(side="left", fill="both", expand=True, padx=7)

    tk.Label(
        card, text=title, font=("Arial", 11, "bold"),
        bg=WHITE, fg=GRAY
    ).pack(anchor="w", padx=18, pady=(13, 5))

    number = tk.Label(
        card, text="0", font=("Arial", 25, "bold"),
        bg=WHITE, fg=color
    )
    number.pack(anchor="w", padx=18, pady=(0, 12))

    return number


total_label = create_stat(stats, "TOTAL TASKS", NAVY)
pending_label = create_stat(stats, "PENDING", ORANGE)
completed_label = create_stat(stats, "COMPLETED", GREEN)
progress_label = create_stat(stats, "PROGRESS", BLUE)

# ---------------- CONTENT ----------------
content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True)

# LEFT: TASK FORM
left = tk.Frame(content, bg=WHITE, width=290,
                highlightbackground="#E0E5EF", highlightthickness=1)
left.pack(side="left", fill="y", padx=(0, 15))
left.pack_propagate(False)

tk.Label(
    left, text="Manage Tasks",
    font=("Arial", 17, "bold"), bg=WHITE, fg=NAVY
).pack(anchor="w", padx=20, pady=(22, 5))

tk.Label(
    left, text="Create or update your tasks",
    font=("Arial", 9), bg=WHITE, fg=GRAY
).pack(anchor="w", padx=20, pady=(0, 20))


def field_label(text):
    tk.Label(
        left, text=text, font=("Arial", 10, "bold"),
        bg=WHITE, fg=BLACK
    ).pack(anchor="w", padx=20, pady=(10, 5))


field_label("Task Name")

title_entry = tk.Entry(
    left, font=("Arial", 11), bg="#F7F8FC",
    fg=BLACK, relief="flat", highlightthickness=1,
    highlightbackground="#DCE2ED", highlightcolor=BLUE
)
title_entry.pack(fill="x", padx=20, ipady=10)

field_label("Category")

category_box = ttk.Combobox(
    left, values=["Study", "Personal", "Work", "Other"],
    state="readonly", font=("Arial", 10)
)
category_box.pack(fill="x", padx=20, ipady=5)
category_box.set("Study")

field_label("Priority")

priority_box = ttk.Combobox(
    left, values=["High", "Medium", "Low"],
    state="readonly", font=("Arial", 10)
)
priority_box.pack(fill="x", padx=20, ipady=5)
priority_box.set("Medium")


def make_button(parent, text, command, color):
    return tk.Button(
        parent, text=text, command=command,
        font=("Arial", 10, "bold"),
        bg=color, fg=WHITE, activebackground=BLUE,
        activeforeground=WHITE, relief="flat",
        cursor="hand2", pady=10, bd=0
    )


make_button(left, "+  Add Task", add_task, NAVY).pack(
    fill="x", padx=20, pady=(25, 7)
)

make_button(left, "Update Task", update_task, BLUE).pack(
    fill="x", padx=20, pady=5
)

make_button(left, "Mark Complete / Undo", complete_task, GREEN).pack(
    fill="x", padx=20, pady=5
)

make_button(left, "Delete Task", delete_task, RED).pack(
    fill="x", padx=20, pady=5
)

# RIGHT: TASK LIST
right = tk.Frame(content, bg=WHITE,
                 highlightbackground="#E0E5EF", highlightthickness=1)
right.pack(side="left", fill="both", expand=True)

tk.Label(
    right, text="My Tasks",
    font=("Arial", 17, "bold"), bg=WHITE, fg=NAVY
).pack(anchor="w", padx=20, pady=(20, 3))

tk.Label(
    right, text="Select a task to edit or manage it.",
    font=("Arial", 9), bg=WHITE, fg=GRAY
).pack(anchor="w", padx=20, pady=(0, 15))

# SEARCH BAR
search_frame = tk.Frame(right, bg=WHITE)
search_frame.pack(fill="x", padx=20, pady=5)

search_entry = tk.Entry(
    search_frame, font=("Arial", 10),
    bg="#F3F5FA", relief="flat"
)
search_entry.pack(side="left", fill="x", expand=True, ipady=9)

search_entry.insert(0, "")

search_entry.bind("<KeyRelease>", lambda e: refresh_tasks())

filter_box = ttk.Combobox(
    search_frame,
    values=["All", "Pending", "Completed"],
    state="readonly", width=12
)
filter_box.pack(side="left", padx=(8, 0))
filter_box.set("All")
filter_box.bind("<<ComboboxSelected>>", lambda e: refresh_tasks())

# TABLE
table_frame = tk.Frame(right, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=20, pady=15)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=BLACK,
    fieldbackground=WHITE,
    rowheight=35,
    font=("Arial", 9)
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Arial", 9, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#DCE6FA")],
    foreground=[("selected", NAVY)]
)

columns = ("Task", "Category", "Priority", "Status", "Date")

task_table = ttk.Treeview(
    table_frame, columns=columns,
    show="headings", selectmode="browse"
)

for col in columns:
    task_table.heading(col, text=col)
    task_table.column(col, width=100, anchor="center")

task_table.column("Task", width=160, anchor="w")
task_table.pack(fill="both", expand=True)

task_table.bind("<<TreeviewSelect>>", select_task)

# FOOTER
footer = tk.Frame(root, bg=NAVY, height=35)
footer.pack(fill="x", side="bottom")

tk.Label(
    footer,
    text="TASKFLOW  |  Stay Organized • Stay Productive",
    font=("Arial", 9),
    bg=NAVY, fg=WHITE
).pack(pady=9)

# ---------------- START APPLICATION ----------------
refresh_tasks()
root.mainloop()
