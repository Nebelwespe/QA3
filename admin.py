import tkinter as tk
from tkinter import ttk, messagebox
import db

def open_admin_window():
    admin = tk.Toplevel()
    admin.title("Admin Panel")

    # --- Header ---
    ttk.Label(admin, text="Admin Panel: View Questions", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

    # --- Course dropdown ---
    ttk.Label(admin, text="Select Course:").grid(row=1, column=0, padx=5, sticky="e")
    course_var = tk.StringVar()
    course_dropdown = ttk.Combobox(admin, textvariable=course_var, state="readonly", width=30)
    course_dropdown['values'] = list(db.courses.values())
    course_dropdown.grid(row=1, column=1, padx=5, pady=5)

    # --- Scrollable frame for questions ---
    frame = ttk.Frame(admin)
    frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    canvas = tk.Canvas(frame, width=650, height=300)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # --- Load Questions Function (must be above button) ---
    def load_questions(course_label):
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        if not course_label:
            return

        table_name = [k for k, v in db.courses.items() if v == course_label][0]
        questions = db.get_all_questions(table_name)

        for idx, q in enumerate(questions, start=1):
            question_text = f"{idx}. {q[1]}"
            options = f"A. {q[2]} | B. {q[3]} | C. {q[4]} | D. {q[5]}"
            correct = f"Answer: {q[6]}"
            ttk.Label(scroll_frame, text=question_text, wraplength=600).grid(row=idx*3, column=0, sticky="w", pady=(10, 0))
            ttk.Label(scroll_frame, text=options, wraplength=600).grid(row=idx*3+1, column=0, sticky="w")
            ttk.Label(scroll_frame, text=correct, foreground="green").grid(row=idx*3+2, column=0, sticky="w")

    # --- Load Button (now safe to reference load_questions) ---
    ttk.Button(admin, text="Load Questions", command=lambda: load_questions(course_var.get())).grid(row=1, column=2, padx=10)

    # --- Add Button ---
    ttk.Button(admin, text="Add Question", command=open_add_question_window).grid(row=2, column=0, columnspan=3, pady=5)

    # --- Add Question Window ---
    def open_add_question_window():
        add_win = tk.Toplevel()
        add_win.title("Add New Question")

        ttk.Label(add_win, text="Add New Question", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Course
        ttk.Label(add_win, text="Course:").grid(row=1, column=0, sticky="e")
        course_var_add = tk.StringVar()
        course_combo = ttk.Combobox(add_win, textvariable=course_var_add, state="readonly")
        course_combo['values'] = list(db.courses.values())
        course_combo.grid(row=1, column=1, pady=5)

        # Question
        ttk.Label(add_win, text="Question:").grid(row=2, column=0, sticky="e")
        question_entry = ttk.Entry(add_win, width=60)
        question_entry.grid(row=2, column=1, pady=5)

        # Options
        options = []
        for i in range(4):
            ttk.Label(add_win, text=f"Option {i+1}:").grid(row=3+i, column=0, sticky="e")
            entry = ttk.Entry(add_win, width=50)
            entry.grid(row=3+i, column=1, pady=2)
            options.append(entry)

        # Correct
        ttk.Label(add_win, text="Correct Answer:").grid(row=7, column=0, sticky="e")
        correct_entry = ttk.Entry(add_win, width=50)
        correct_entry.grid(row=7, column=1, pady=5)

        def submit_question():
            table = [k for k, v in db.courses.items() if v == course_var_add.get()]
            if not table:
                messagebox.showerror("Error", "Please select a course.")
                return

            table = table[0]
            q = question_entry.get()
            opts = [opt.get() for opt in options]
            correct = correct_entry.get()

            if not all([q] + opts + [correct]):
                messagebox.showerror("Error", "All fields are required.")
                return

            db.insert_question(table, q, opts, correct)
            messagebox.showinfo("Success", "Question added.")
            add_win.destroy()

        ttk.Button(add_win, text="Submit", command=submit_question).grid(row=8, column=0, columnspan=2, pady=10)

    admin.mainloop()
