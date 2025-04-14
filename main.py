import tkinter as tk
from tkinter import ttk, messagebox
from quiz import QuizApp
from admin import open_admin_window
import db

def open_quiz_window():
    messagebox.showinfo("Quiz", "Quiz interface would start here.")

PASSWORD = "password1"

def check_password():
    entered = password_entry.get()
    if entered == PASSWORD:
        root.withdraw()  # hide it, don't destroy it
        open_admin_window(parent_root=root)
    else:
        messagebox.showerror("Access Denied", "Incorrect password")

def start_quiz():
    root.withdraw()
    QuizApp(tk.Toplevel())

# Setup database
db.create_tables()

# GUI Setup
root = tk.Tk()
root.title("Quiz Bowl Login")

ttk.Label(root, text="Welcome to Quiz Bowl!", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Admin login
ttk.Label(root, text="Admin Login:").grid(row=1, column=0, sticky="e")
password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(root, text="Login as Admin", command=check_password).grid(row=2, column=0, columnspan=2, pady=5)

# Quiz button
ttk.Label(root, text="OR").grid(row=3, column=0, columnspan=2)
ttk.Button(root, text="Take a Quiz", command=start_quiz).grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
