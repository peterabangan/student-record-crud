# UI for Student Record CRUD App using Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

db = Database()

root = tk.Tk()
root.title("Student Record System")
root.geometry("1800x800")

#form frame
form_frame = tk.LabelFrame(root, text="Student Details")
form_frame.pack(fill='x', padx=10, pady=5)

#input variables
first_name_var = tk.StringVar()
last_name_var = tk.StringVar()
age_var = tk.StringVar()
grade_var = tk.StringVar()
section_var = tk.StringVar()
gender_var = tk.StringVar()

#input fields
#name
tk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(form_frame, textvariable=first_name_var).grid(row=0, column=1)

tk.Label(form_frame, text="Last Name:").grid(row=0, column=2, padx=10, pady=5)
tk.Entry(form_frame, textvariable=last_name_var).grid(row=0, column=3)

#age
tk.Label(form_frame, text="Age:").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(form_frame, textvariable=age_var).grid(row=1, column=1)

#grade
tk.Label(form_frame, text="Grade:").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(form_frame, textvariable=grade_var).grid(row=2, column=1)

#section
tk.Label(form_frame, text="Section:").grid(row=1, column=2, padx=10, pady=5)
tk.Entry(form_frame, textvariable=section_var).grid(row=1, column=3)

#gender
tk.Label(form_frame, text="Gender:").grid(row=2, column=2, padx=10, pady=5)
ttk.Combobox(form_frame, textvariable=gender_var, values=["Male", "Female"], state="readonly").grid(row=2, column=3, padx=5, pady=5)

#table frame
table_frame = tk.LabelFrame(root, text="Records")
table_frame.pack(fill='both', padx=10, pady=5, expand=True)

#treeview
tree = ttk.Treeview(table_frame, columns=("ID", "First Name", "Last Name", "Age", "Grade", "Section", "Gender"), show="headings")
for col in ("ID", "First Name", "Last Name", "Age", "Grade", "Section", "Gender"):
    tree.heading(col, text=col)
tree.pack(fill='both', expand=True)

#functions
def load_students():
    for row in tree.get_children():
        tree.delete(row)
    for record in db.get_all_students():
        tree.insert("", "end", values=record)

def add_student():
    if not first_name_var.get() or not last_name_var.get() or not age_var.get() or not grade_var.get() or not section_var.get() or not gender_var.get():
        messagebox.showerror("Error", "All fields are required.")
        return
    if not age_var.get().isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return
    db.add_student(first_name_var.get(), last_name_var.get(), age_var.get(), grade_var.get(), section_var.get(), gender_var.get())
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
    db.update_student(student_id, first_name_var.get(), last_name_var.get(), age_var.get(), grade_var.get(), section_var.get(), gender_var.get())
    load_students()

def select_student(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected)["values"]
        first_name_var.set(values[1])
        last_name_var.set(values[2])
        age_var.set(values[3])
        grade_var.set(values[4])
        section_var.set(values[5])
        gender_var.set(values[6])

def clear_fields():
    first_name_var.set("")
    last_name_var.set("")
    age_var.set("")
    grade_var.set("")
    section_var.set("")
    gender_var.set("")
    search_var.set("")

def search_students(*args):
    query = search_var.get().strip().lower()
    for row in tree.get_children():
        tree.delete(row)
    for record in db.get_all_students():
        if query in str(record[1]).lower() or query in str(record[2]).lower():
            tree.insert("", "end", values=record)       

def sort_by_firstname():
    for row in tree.get_children():
        tree.delete(row)
    for record in db.get_all_students_sorted():
        tree.insert("", "end", values=record)      

def sort_by_id():
    for row in tree.get_children():
        tree.delete(row)
    for record in db.get_all_students_by_id(): 
        tree.insert("", "end", values=record)     
    
#search frame
search_frame = tk.LabelFrame(root, text="Search")
search_frame.pack(fill='x', padx=10, pady=5)    

search_var = tk.StringVar()
search_var.trace("w", search_students) 
tk.Entry(search_frame, textvariable=search_var).pack(side='left', padx=5, pady=5, fill='x', expand=True)
tk.Button(search_frame, text="Sort by ID", command=sort_by_id).pack(side='left', padx=5, pady=5)
tk.Button(search_frame, text="Sort by First Name", command=sort_by_firstname).pack(side='left', padx=5, pady=5)

#button frame
button_frame = tk.LabelFrame(root, text="Actions")
button_frame.pack(fill='x', padx=10, pady=5)

#buttons

tk.Button(button_frame, text="Add", command=add_student).pack(side='left', padx=5, pady=5)
tk.Button(button_frame, text="Update", command=update_student).pack(side='left', padx=5, pady=5)
tk.Button(button_frame, text="Delete", command=delete_student).pack(side='left', padx=5, pady=5)
tk.Button(button_frame, text="Clear", command=clear_fields).pack(side='left', padx=5, pady=5)

# Bind click on treeview to auto-fill input fields
tree.bind("<ButtonRelease-1>", select_student)

load_students()
root.mainloop()