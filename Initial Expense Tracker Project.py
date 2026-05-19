from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------

conn = sqlite3.connect("expense.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit

# ---------------- FUNCTIONS ----------------


def add_expense():
    title = title_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()

    if title == "" or amount == "" or category == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    date = datetime.now().strftime("%d-%m-%Y")

    cursor.execute("""
    INSERT INTO expenses(title, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    conn.commit()

    messagebox.showinfo("Success", "Expense Added Successfully!")

    title_entry.delete(0, END)
    amount_entry.delete(0, END)
    category_entry.delete(0, END)

    show_expenses()
    update_total()


def show_expenses():
    listbox.delete(0, END)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    for row in rows:
        text = f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]} | {row[4]}"
        listbox.insert(END, text)


def delete_expense():
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select an expense first!")
        return

    item = listbox.get(selected[0])

    expense_id = item.split("|")[0].strip()

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

    messagebox.showinfo("Deleted", "Expense Deleted!")

    show_expenses()
    update_total()


def update_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    total_label.config(text=f"Total Expense: ₹{total}")


# ---------------- GUI ----------------

root = Tk()
root.title("AI Expense Tracker")
root.geometry("800x600")
root.config(bg="#1e1e1e")

heading = Label(
    root,
    text="AI Expense Tracker",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)
heading.pack(pady=20)

# ---------- INPUT FRAME ----------

frame = Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

Label(frame, text="Title", bg="#1e1e1e",
      fg="white").grid(row=0, column=0, padx=10)
title_entry = Entry(frame, width=20)
title_entry.grid(row=0, column=1)

Label(frame, text="Amount", bg="#1e1e1e",
      fg="white").grid(row=0, column=2, padx=10)
amount_entry = Entry(frame, width=20)
amount_entry.grid(row=0, column=3)

Label(frame, text="Category", bg="#1e1e1e",
      fg="white").grid(row=0, column=4, padx=10)
category_entry = Entry(frame, width=20)
category_entry.grid(row=0, column=5)

# ---------- BUTTONS ----------

btn_frame = Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=20)

add_btn = Button(
    btn_frame,
    text="Add Expense",
    command=add_expense,
    bg="green",
    fg="white",
    width=15
)
add_btn.grid(row=0, column=0, padx=10)

delete_btn = Button(
    btn_frame,
    text="Delete Expense",
    command=delete_expense,
    bg="red",
    fg="white",
    width=15
)
delete_btn.grid(row=0, column=1, padx=10)

# ---------- LISTBOX ----------

listbox = Listbox(
    root,
    width=100,
    height=18,
    bg="#2d2d2d",
    fg="white",
    font=("Consolas", 11)
)
listbox.pack(pady=20)

# ---------- TOTAL ----------

total_label = Label(
    root,
    text="Total Expense: $0",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="cyan"
)
total_label.pack(pady=10)

# ---------- LOAD DATA ----------

show_expenses()
update_total()

root.mainloop()

conn.close()
