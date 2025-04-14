import tkinter as tk
from tkinter import ttk, messagebox
import db
import random

class QuizApp:
    def __init__(self, root, parent_root=None):
        self.root = root
        self.root.title("Quiz Time!")
        self.parent_root = parent_root

        self.reset_quiz()
        self.setup_course_selection()

    def reset_quiz(self):
        self.current_question = 0
        self.score = 0
        self.selected_course = None
        self.questions = []
        self.total_questions = 0
        self.answered_questions = set()

    def setup_course_selection(self):
        self.reset_quiz()
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Choose a Course", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(self.root, textvariable=self.course_var, state="readonly", width=30)
        self.course_dropdown['values'] = list(db.courses.values())
        self.course_dropdown.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(self.root, text="Start Quiz", command=self.start_quiz).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Exit", command=self.exit_quiz).grid(row=3, column=0, columnspan=2, pady=5)

    def start_quiz(self):
        label = self.course_var.get()
        if not label:
            messagebox.showerror("Error", "Please select a course.")
            return

        table_name = [k for k, v in db.courses.items() if v == label][0]
        all_questions = db.get_all_questions(table_name)

        if not all_questions:
            messagebox.showinfo("No Questions", "There are no questions for this course yet.")
            return

        self.questions = all_questions.copy()
        random.shuffle(self.questions)
        self.total_questions = len(self.questions)
        self.current_question = 0
        self.score = 0
        self.display_question()

    def display_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        question = self.questions[self.current_question]

        ttk.Label(self.root, text=f"Question {self.current_question + 1} of {self.total_questions}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.root, text=question[1], wraplength=500).grid(row=1, column=0, columnspan=2, pady=5)

        self.answer_var = tk.StringVar()
        self.feedback_label = ttk.Label(self.root, text="")
        self.feedback_label.grid(row=6, column=0, columnspan=2, pady=5)

        for i, opt in enumerate(question[2:6]):
            ttk.Radiobutton(self.root, text=opt, variable=self.answer_var, value=opt).grid(row=2+i, column=0, columnspan=2, sticky="w", padx=20, pady=2)

        ttk.Button(self.root, text="Submit Answer", command=self.check_answer).grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(self.root, text="Exit", command=self.exit_quiz).grid(row=8, column=0, columnspan=2, pady=5)

    def check_answer(self):
        if not self.answer_var.get():
            messagebox.showerror("Error", "Please select an answer.")
            return

        correct = self.questions[self.current_question][6]
        if self.answer_var.get() == correct:
            self.score += 1
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text=f"Incorrect! Correct answer: {correct}", foreground="red")

        self.root.after(1500, self.next_question)

    def next_question(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Quiz Completed!", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.root, text=f"Your score: {self.score} out of {self.total_questions}").grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Take Another Quiz", command=self.setup_course_selection).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(self.root, text="Exit", command=self.exit_quiz).grid(row=3, column=0, columnspan=2, pady=5)

    def exit_quiz(self):
        self.root.destroy()
