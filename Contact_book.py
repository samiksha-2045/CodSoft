
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

# ---------------- COLORS ----------------

NAVY = "#14213D"
BLUE = "#243B64"
WHITE = "#FFFFFF"
BG = "#F3F5FA"
BLACK = "#172033"
GRAY = "#010812"
GREEN = "#168A70"
RED = "#D9534F"

FILE_NAME = "contacts.json"
contacts = []
selected_contact = None

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Contact Book Manager")
root.geometry("1150x720")
root.minsize(950, 650)
root.configure(bg=BG)

# ---------------- LOAD CONTACTS ----------------

def load_contacts():
    global contacts

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                contacts = json.load(file)

        except (json.JSONDecodeError, OSError):
            contacts = []
            messagebox.showwarning(
                "File Warning",
                "Could not read contacts.json. Starting with an empty contact list."
            )


def save_contacts():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4)
        return True

    except OSError:
        messagebox.showerror(
            "Save Error",
            "Unable to save contacts. Check folder permissions."
        )
        return False


# ---------------- HEADER ----------------

header = tk.Frame(root, bg=NAVY, height=105)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="CONTACT BOOK",
    font=("Arial", 25, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w", padx=30, pady=(18, 3))

tk.Label(
    header,
    text="Manage your contacts in one place",
    font=("Arial", 11),
    bg=NAVY,
    fg="#C5D2E8"
).pack(anchor="w", padx=33)

# ---------------- MAIN CONTAINER ----------------

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=25, pady=20)

# ---------------- TOP STATISTICS ----------------

stats = tk.Frame(main, bg=WHITE)
stats.pack(fill="x", pady=(0, 18))

tk.Label(
    stats,
    text="TOTAL CONTACTS",
    font=("Arial", 11, "bold"),
    bg=WHITE,
    fg=GRAY
).pack(side="left", padx=20, pady=15)

count_label = tk.Label(
    stats,
    text="0",
    font=("Arial", 20, "bold"),
    bg=WHITE,
    fg=NAVY
)
count_label.pack(side="left", padx=10)

# ---------------- CONTENT ----------------

content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True)

# LEFT PANEL - CONTACT FORM

left = tk.Frame(
    content,
    bg=WHITE,
    width=340,
    highlightbackground="#E0E5EF",
    highlightthickness=1
)
left.pack(side="left", fill="y", padx=(0, 15))
left.pack_propagate(False)

tk.Label(
    left,
    text="Contact Details",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", padx=22, pady=(20, 5))

tk.Label(
    left,
    text="Add or update contact information",
    font=("Arial", 9),
    bg=WHITE,
    fg=GRAY
).pack(anchor="w", padx=22, pady=(0, 15))


def create_label(text):
    tk.Label(
        left,
        text=text,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(anchor="w", padx=22, pady=(9, 5))


def create_entry():
    entry = tk.Entry(
        left,
        font=("Arial", 11),
        bg=BG,
        fg=BLACK,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#DCE2ED",
        highlightcolor=BLUE
    )
    entry.pack(fill="x", padx=22, ipady=9)
    return entry


create_label("Full Name")
name_entry = create_entry()

create_label("Phone Number")
phone_entry = create_entry()

create_label("Email Address")
email_entry = create_entry()

create_label("Address")
address_entry = tk.Text(
    left,
    height=3,
    font=("Arial", 10),
    bg=BG,
    fg=BLACK,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#DCE2ED",
    wrap="word"
)
address_entry.pack(fill="x", padx=22)

# ---------------- FORM FUNCTIONS ----------------

def clear_fields():
    global selected_contact

    selected_contact = None

    for entry in [name_entry, phone_entry, email_entry]:
        entry.delete(0, tk.END)

    address_entry.delete("1.0", tk.END)

    if contact_table.selection():
        contact_table.selection_remove(contact_table.selection())


def get_contact_details():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get("1.0", tk.END).strip()

    if not name or not phone or not email or not address:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all contact details."
        )
        return None

    if not re.fullmatch(r"[0-9+\-\s()]{7,20}", phone):
        messagebox.showwarning(
            "Invalid Phone",
            "Please enter a valid phone number."
        )
        return None

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address."
        )
        return None

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }


# ---------------- ADD CONTACT ----------------

def add_contact():
    details = get_contact_details()

    if details is None:
        return

    contacts.append(details)

    if save_contacts():
        clear_fields()
        refresh_contacts()
        messagebox.showinfo(
            "Success",
            "Contact added successfully!"
        )
    else:
        contacts.pop()


# ---------------- VIEW CONTACTS ----------------

def refresh_contacts():
    contact_table.delete(*contact_table.get_children())

    search_text = search_entry.get().strip().lower()

    for index, contact in enumerate(contacts):

        if (
            search_text not in contact["name"].lower()
            and search_text not in contact["phone"].lower()
        ):
            continue

        contact_table.insert(
            "",
            "end",
            iid=str(index),
            values=(
                contact["name"],
                contact["phone"],
                contact["email"]
            )
        )

    count_label.config(text=str(len(contacts)))


# ---------------- SELECT CONTACT ----------------

def select_contact(event):
    global selected_contact

    selected = contact_table.selection()

    if not selected:
        return

    selected_contact = int(selected[0])
    contact = contacts[selected_contact]

    clear_selection = False

    name_entry.delete(0, tk.END)
    name_entry.insert(0, contact["name"])

    phone_entry.delete(0, tk.END)
    phone_entry.insert(0, contact["phone"])

    email_entry.delete(0, tk.END)
    email_entry.insert(0, contact["email"])

    address_entry.delete("1.0", tk.END)
    address_entry.insert("1.0", contact["address"])


# ---------------- UPDATE CONTACT ----------------

def update_contact():
    if selected_contact is None:
        messagebox.showwarning(
            "Select Contact",
            "Please select a contact from the list first."
        )
        return

    details = get_contact_details()

    if details is None:
        return

    old_contact = contacts[selected_contact].copy()
    contacts[selected_contact] = details

    if save_contacts():
        clear_fields()
        refresh_contacts()
        messagebox.showinfo(
            "Updated",
            "Contact updated successfully!"
        )
    else:
        contacts[selected_contact] = old_contact


# ---------------- DELETE CONTACT ----------------

def delete_contact():
    if selected_contact is None:
        messagebox.showwarning(
            "Select Contact",
            "Please select a contact to delete."
        )
        return

    if messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this contact?"
    ):
        index = selected_contact
        removed_contact = contacts.pop(index)

        if save_contacts():
            clear_fields()
            refresh_contacts()
            messagebox.showinfo(
                "Deleted",
                "Contact deleted successfully!"
            )
        else:
            contacts.insert(index, removed_contact)
            refresh_contacts()


# ---------------- BUTTON DESIGN ----------------

def make_button(parent, text, command, color):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        pady=9
    )


make_button(
    left, "+ Add Contact", add_contact, NAVY
).pack(fill="x", padx=22, pady=(18, 5))

make_button(
    left, "Update Contact", update_contact, BLUE
).pack(fill="x", padx=22, pady=5)

make_button(
    left, "Delete Contact", delete_contact, RED
).pack(fill="x", padx=22, pady=5)

tk.Button(
    left,
    text="Clear Fields",
    command=clear_fields,
    font=("Arial", 10, "bold"),
    bg="#E5EAF3",
    fg=NAVY,
    activebackground="#D0D9E9",
    relief="flat",
    cursor="hand2",
    pady=9
).pack(fill="x", padx=22, pady=5)

# ---------------- RIGHT PANEL ----------------

right = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground="#E0E5EF",
    highlightthickness=1
)
right.pack(side="left", fill="both", expand=True)

tk.Label(
    right,
    text="Saved Contacts",
    font=("Arial", 17, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", padx=20, pady=(20, 4))

tk.Label(
    right,
    text="Search by contact name or phone number",
    font=("Arial", 9),
    bg=WHITE,
    fg=GRAY
).pack(anchor="w", padx=20, pady=(0, 12))

# ---------------- SEARCH ----------------

search_frame = tk.Frame(right, bg=WHITE)
search_frame.pack(fill="x", padx=20, pady=5)

search_entry = tk.Entry(
    search_frame,
    font=("Arial", 11),
    bg=BG,
    fg=BLACK,
    relief="flat"
)
search_entry.pack(fill="x", ipady=10)

search_entry.bind(
    "<KeyRelease>",
    lambda event: refresh_contacts()
)

# ---------------- CONTACT TABLE ----------------

table_frame = tk.Frame(right, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=20, pady=15)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=BLACK,
    fieldbackground=WHITE,
    rowheight=38,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Arial", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#DCE6FA")],
    foreground=[("selected", NAVY)]
)

columns = ("Name", "Phone", "Email")

contact_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

contact_table.heading("Name", text="NAME")
contact_table.heading("Phone", text="PHONE NUMBER")
contact_table.heading("Email", text="EMAIL")

contact_table.column("Name", width=130, anchor="w")
contact_table.column("Phone", width=125, anchor="center")
contact_table.column("Email", width=180, anchor="w")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=contact_table.yview
)

contact_table.configure(yscrollcommand=scrollbar.set)

contact_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

contact_table.bind(
    "<<TreeviewSelect>>",
    select_contact
)

# ---------------- FOOTER ----------------

footer = tk.Frame(root, bg=NAVY, height=35)
footer.pack(fill="x", side="bottom")

tk.Label(
    footer,
    text="CONTACT BOOK | PYTHON INTERNSHIP TASK 4",
    font=("Arial", 9),
    bg=NAVY,
    fg=WHITE
).pack(pady=9)

# ---------------- START APPLICATION ----------------

load_contacts()
refresh_contacts()

root.mainloop()
