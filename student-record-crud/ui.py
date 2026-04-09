# UI for Student Record CRUD App using Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

db = Database()

root = tk.Tk()
root.title("Student Record System")
root.geometry("820x400")

#input variables
name_var = tk.StringVar()
age_var = tk.StringVar()
grade_var = tk.StringVar()

#input fields
#name
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1)

#age
tk.Label(root, text="Age:").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=age_var).grid(row=1, column=1)

#grade
tk.Label(root, text="Grade:").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=grade_var).grid(row=2, column=1)

#treeview
tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Grade"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Grade", text="Grade")
tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

#functions
def load_students():
    for row in tree.get_children():
        tree.delete(row)
    for record in db.get_all_students():
        tree.insert("", "end", values=record)

def add_student():
    if not name_var.get() or not age_var.get() or not grade_var.get():
        messagebox.showerror("Error", "All fields are required.")
        return
    if not age_var.get().isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return
    db.add_student(name_var.get(), age_var.get(), grade_var.get())
    load_students()

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student first.")
        return
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
    if confirm:
        student_id = tree.item(selected)["values"][0]
        db.delete_student(student_id)
        load_students()

def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student first.")
        return
    student_id = tree.item(selected)["values"][0]
    db.update_student(student_id, name_var.get(), age_var.get(), grade_var.get())
    load_students()

def select_student(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected)["values"]
        name_var.set(values[1])
        age_var.set(values[2])
        grade_var.set(values[3])

def clear_fields():
    name_var.set("")
    age_var.set("")
    grade_var.set("")

def search_students(*args):
    query = search_var.get().strip().lower()
    for row in tree.get_children():
        tree.delete(row)
    for record in db.get_all_students():
        if query in str(record[1]).lower():
            tree.insert("", "end", values=record)       

search_var = tk.StringVar()
search_var.trace("w", search_students) 
tk.Entry(root, textvariable=search_var).grid(row=0, column=3, columnspan=2, padx=10, pady=5)
tk.Label(root, text="Search:").grid(row=0, column=2, padx=10, pady=5)

#buttons

tk.Button(root, text="Add", command=add_student).grid(row=3, column=0, pady=5)
tk.Button(root, text="Update", command=update_student).grid(row=3, column=1)
tk.Button(root, text="Delete", command=delete_student).grid(row=3, column=2)
tk.Button(root, text="Clear", command=clear_fields).grid(row=3, column=3)

# Bind click on treeview to auto-fill input fields
tree.bind("<ButtonRelease-1>", select_student)

load_students()
root.mainloop()