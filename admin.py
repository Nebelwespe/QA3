import tkinter as tk
from tkinter import ttk
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

    # --- Scrollable frame for results ---
    frame = ttk.Frame(admin)
    frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    canvas = tk.Canvas(frame, width=600, height=300)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # --- Load Questions Function ---
    def load_questions():
        # Clear old widgets in scroll_frame
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        selected_label = course_var.get()
        if not selected_label:
            return

        # Convert back to table name
        table_name = [k for k, v in db.courses.items() if v == selected_label][0]
        questions = db.preload_questions(table_name)

        for idx, q in enumerate(questions, start=1):
            question_text = f"{idx}. {q[1]}"
            options = f"A. {q[2]} | B. {q[3]} | C. {q[4]} | D. {q[5]}"
            correct = f"Answer: {q[6]}"
            ttk.Label(scroll_frame, text=question_text, wraplength=580).grid(row=idx*3, column=0, sticky="w", pady=(10, 0))
            ttk.Label(scroll_frame, text=options, wraplength=580).grid(row=idx*3+1, column=0, sticky="w")
            ttk.Label(scroll_frame, text=correct, foreground="green").grid(row=idx*3+2, column=0, sticky="w")

    # --- Load Button ---
    ttk.Button(admin, text="Load Questions", command=load_questions).grid(row=1, column=2, padx=10)

    admin.mainloop()
