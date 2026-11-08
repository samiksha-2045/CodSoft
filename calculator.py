
import tkinter as tk

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Smart Calculator")
root.geometry("380x570")
root.resizable(False, False)
root.configure(bg="#E9EDF5")

NAVY = "#14213D"
BLUE = "#243B64"
WHITE = "#FFFFFF"
BLACK = "#111827"
LIGHT = "#E8EEFA"
GRAY = "#718096"
RED = "#D9534F"

expression = ""

# ---------------- DISPLAY ----------------

header = tk.Frame(root, bg=NAVY, height=85)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="SMART CALCULATOR",
    font=("Arial", 20, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=24)

display_frame = tk.Frame(root, bg=WHITE)
display_frame.pack(fill="x", padx=18, pady=18)

display = tk.Entry(
    display_frame,
    font=("Arial", 27, "bold"),
    justify="right",
    bg=WHITE,
    fg=NAVY,
    relief="flat",
    bd=0
)
display.pack(fill="x", padx=15, pady=18, ipady=12)

display.insert(0, "0")

# ---------------- FUNCTIONS ----------------

def press(value):
    current = display.get()

    if current == "Error":
        current = ""

    if current == "0" and value not in ["."]:
        current = ""

    display.delete(0, tk.END)
    display.insert(0, current + str(value))


def clear():
    display.delete(0, tk.END)
    display.insert(0, "0")


def backspace():
    current = display.get()

    if current == "Error":
        clear()
        return

    current = current[:-1]

    display.delete(0, tk.END)
    display.insert(0, current if current else "0")


def calculate():
    expression = display.get()

    try:
        if not expression or expression == "Error":
            return

        # Only allow calculator characters
        allowed = "0123456789+-*/.() "

        if any(char not in allowed for char in expression):
            raise ValueError

        result = eval(expression, {"__builtins__": {}}, {})

        if isinstance(result, float):
            result = round(result, 10)

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except ZeroDivisionError:
        display.delete(0, tk.END)
        display.insert(0, "Error")

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


# ---------------- BUTTON DESIGN ----------------

button_frame = tk.Frame(root, bg="#E9EDF5")
button_frame.pack(padx=15, pady=5, fill="both", expand=True)

buttons = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]


def button_click(value):
    if value == "C":
        clear()

    elif value == "⌫":
        backspace()

    elif value == "=":
        calculate()

    else:
        if value == "×":
            press("*")
        elif value == "÷":
            press("/")
        else:
            press(value)


for row_index, row in enumerate(buttons):

    for col_index, value in enumerate(row):

        if value == "=":
            color = NAVY
            text_color = WHITE

        elif value in ["+", "-", "×", "÷", "C", "⌫", "(", ")"]:
            color = BLUE
            text_color = WHITE

        else:
            color = WHITE
            text_color = BLACK

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 17, "bold"),
            bg=color,
            fg=text_color,
            activebackground=NAVY,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            command=lambda v=value: button_click(v)
        )

        button.grid(
            row=row_index,
            column=col_index,
            padx=5,
            pady=5,
            sticky="nsew"
        )

for i in range(5):
    button_frame.rowconfigure(i, weight=1)

for i in range(4):
    button_frame.columnconfigure(i, weight=1)

# ---------------- KEYBOARD SUPPORT ----------------

def keyboard_input(event):
    char = event.char

    if char in "0123456789.+-*/()":
        press(char)

    elif event.keysym == "Return":
        calculate()

    elif event.keysym == "BackSpace":
        backspace()

    elif event.keysym == "Escape":
        clear()


root.bind("<Key>", keyboard_input)

# ---------------- FOOTER ----------------

tk.Label(
    root,
    text="TASK 2  |  PYTHON CALCULATOR",
    font=("Arial", 9, "bold"),
    bg="#E9EDF5",
    fg=GRAY
).pack(pady=10)

root.mainloop()
