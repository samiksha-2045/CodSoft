
import tkinter as tk
from tkinter import messagebox
import secrets
import string

# ---------------- COLORS ----------------

NAVY = "#14213D"
BLUE = "#243B64"
WHITE = "#FFFFFF"
BG = "#F3F5FA"
BLACK = "#172033"
GRAY = "#718096"
GREEN = "#168A70"

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg=BG)

# ---------------- HEADER ----------------

header = tk.Frame(root, bg=NAVY, height=110)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="PASSWORD GENERATOR",
    font=("Arial", 22, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(23, 5))

tk.Label(
    header,
    text="Create strong and secure passwords",
    font=("Arial", 10),
    bg=NAVY,
    fg="#C5D2E8"
).pack()

# ---------------- MAIN CONTAINER ----------------

main = tk.Frame(root, bg=WHITE)
main.pack(fill="both", expand=True, padx=25, pady=20)

# ---------------- PASSWORD LENGTH ----------------

tk.Label(
    main,
    text="Password Length",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", padx=22, pady=(20, 5))

length_var = tk.IntVar(value=12)

length_display = tk.Label(
    main,
    text="12",
    font=("Arial", 16, "bold"),
    bg=WHITE,
    fg=BLUE
)
length_display.pack(anchor="w", padx=22)

def update_length(value):
    length_display.config(text=str(int(float(value))))

length_slider = tk.Scale(
    main,
    from_=4,
    to=32,
    orient="horizontal",
    variable=length_var,
    command=update_length,
    bg=WHITE,
    fg=NAVY,
    troughcolor="#DCE6FA",
    highlightthickness=0,
    activebackground=BLUE,
    font=("Arial", 9)
)
length_slider.pack(fill="x", padx=18)

# ---------------- PASSWORD OPTIONS ----------------

tk.Label(
    main,
    text="Password Complexity",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", padx=22, pady=(18, 8))

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

options = [
    ("Uppercase Letters (A-Z)", upper_var),
    ("Lowercase Letters (a-z)", lower_var),
    ("Numbers (0-9)", number_var),
    ("Special Characters (@#$%)", symbol_var)
]

for text, variable in options:
    tk.Checkbutton(
        main,
        text=text,
        variable=variable,
        font=("Arial", 10),
        bg=WHITE,
        fg=BLACK,
        activebackground=WHITE,
        selectcolor="#DCE6FA",
        cursor="hand2"
    ).pack(anchor="w", padx=25, pady=3)

# ---------------- PASSWORD GENERATION ----------------

def generate_password():

    length = length_var.get()

    characters = ""

    if upper_var.get():
        characters += string.ascii_uppercase

    if lower_var.get():
        characters += string.ascii_lowercase

    if number_var.get():
        characters += string.digits

    if symbol_var.get():
        characters += "!@#$%^&*()-_=+"

    if not characters:
        messagebox.showwarning(
            "Select Options",
            "Please select at least one character type!"
        )
        return

    if length < 4:
        messagebox.showwarning(
            "Invalid Length",
            "Password length must be at least 4."
        )
        return

    # Ensure each selected character type is included
    groups = []

    if upper_var.get():
        groups.append(string.ascii_uppercase)

    if lower_var.get():
        groups.append(string.ascii_lowercase)

    if number_var.get():
        groups.append(string.digits)

    if symbol_var.get():
        groups.append("!@#$%^&*()-_=+")

    if length < len(groups):
        messagebox.showwarning(
            "Length Too Short",
            "Increase password length to match selected options."
        )
        return

    password_chars = [
        secrets.choice(group) for group in groups
    ]

    remaining = length - len(password_chars)

    password_chars.extend(
        secrets.choice(characters) for _ in range(remaining)
    )

    secrets.SystemRandom().shuffle(password_chars)

    password = "".join(password_chars)

    password_entry.config(state="normal")
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    password_entry.config(state="readonly")

    status_label.config(
        text="Password generated successfully!",
        fg=GREEN
    )


# ---------------- PASSWORD DISPLAY ----------------

tk.Label(
    main,
    text="Your Generated Password",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", padx=22, pady=(20, 8))

password_entry = tk.Entry(
    main,
    font=("Arial", 13, "bold"),
    justify="center",
    bg=BG,
    fg=NAVY,
    relief="flat",
    state="readonly"
)
password_entry.pack(fill="x", padx=22, ipady=12)

# ---------------- COPY FUNCTION ----------------

def copy_password():

    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Please generate a password first!"
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    status_label.config(
        text="Password copied to clipboard!",
        fg=GREEN
    )


# ---------------- CLEAR FUNCTION ----------------

def clear_password():

    password_entry.config(state="normal")
    password_entry.delete(0, tk.END)
    password_entry.config(state="readonly")

    status_label.config(
        text="",
        fg=GRAY
    )

# ---------------- BUTTONS ----------------

tk.Button(
    main,
    text="GENERATE PASSWORD",
    command=generate_password,
    font=("Arial", 11, "bold"),
    bg=NAVY,
    fg=WHITE,
    activebackground=BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2"
).pack(fill="x", padx=22, pady=(20, 8), ipady=12)

button_frame = tk.Frame(main, bg=WHITE)
button_frame.pack(fill="x", padx=22)

tk.Button(
    button_frame,
    text="COPY PASSWORD",
    command=copy_password,
    font=("Arial", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=NAVY,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2"
).pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=9)

tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_password,
    font=("Arial", 10, "bold"),
    bg="#E5EAF3",
    fg=NAVY,
    activebackground="#D0D9E9",
    relief="flat",
    cursor="hand2"
).pack(side="left", fill="x", expand=True, padx=(5, 0), ipady=9)


status_label = tk.Label(
    main,
    text="",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=GREEN
)
status_label.pack(pady=12)


tk.Label(
    root,
    text="TASK 3 | PYTHON PASSWORD GENERATOR",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=GRAY
).pack(pady=(0, 10))



root.mainloop()
