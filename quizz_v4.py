import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json
import random
import os
import sys
import webbrowser
import pyperclip

def get_resource_path(relative_path):
    """Get the absolute path to the resource."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_questions(filename):
    """Load questions from a specified JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def open_service_and_copy_question(service_name):
    """Open a browser window to the service's URL and copy the question to the clipboard."""
    current_question_text = question_label.get("1.0", tk.END).strip()
    current_options_text = "\n".join([button.cget("text") for button in option_buttons if button.cget("text") != ""])
    full_text = f"{current_question_text}\n{current_options_text}"
    pyperclip.copy(full_text)  # Copy the question and options to the clipboard
    
    messagebox.showinfo("Copied to Clipboard", "The question and options have been copied to your clipboard. Please paste them into the selected service.")
    
    # Open a new browser window/tab to the service's URL
    if service_name == "ChatGPT":
        webbrowser.open_new_tab("https://chat.openai.com/chat")
    elif service_name == "Gemini":
        webbrowser.open_new_tab("https://gemini.google.com/app")  

def start_practice_quiz():
    start_quiz("practice")

def start_timed_quiz():
    start_quiz("timed")

def start_quiz(mode):
    global quiz_mode, current_question, user_score, questions_data
    quiz_mode = mode
    if mode == "timed":
        start_timer(60 * 60)
    random.shuffle(questions_data)
    questions_data = questions_data[:50] if mode == "timed" else questions_data
    current_question = 0
    user_score = 0
    update_score_label()
    display_next_question()

def start_timer(seconds):
    def countdown():
        nonlocal seconds
        mins, secs = divmod(seconds, 60)
        time_label.config(text=f"Time Left: {mins:02d}:{secs:02d}")
        seconds -= 1
        if seconds >= 0:
            root.after(1000, countdown)
        else:
            messagebox.showinfo("Time's up", "Time is up! Your session is over.")
            root.destroy()
    countdown()

def display_next_question():
    global current_question, user_score, questions_data
    if current_question < len(questions_data):
        question_info = questions_data[current_question]
        question_label.configure(state="normal")
        question_label.delete("1.0", tk.END)
        question_label.insert(tk.END, question_info['question'])
        question_label.configure(state="disabled")
        for i, option_text in enumerate('ABCD'):
            option_buttons[i].config(text=f"{option_text}: {question_info['options'][option_text]}", state="normal")
    else:
        messagebox.showinfo("Quiz Completed", f"Your score is {user_score}/{len(questions_data)}")
        root.destroy()

def check_answer(option):
    global current_question, user_score, questions_data
    question_info = questions_data[current_question]
    correct_answer = question_info['answer']
    explanation = question_info.get('explanation', 'No explanation provided.')
    feedback = "Correct!" if option == correct_answer else f"Incorrect! The correct answer was {correct_answer}: {question_info['options'][correct_answer]}. {explanation}"
    user_score += 1 if option == correct_answer else 0
    messagebox.showinfo("Feedback", feedback)
    current_question += 1
    update_score_label()
    display_next_question()

def update_score_label():
    score_label.config(text=f"Score: {user_score} correct, {current_question - user_score} incorrect")

def select_question_set(set_name):
    global questions_data
    question_sets = {'CDL': 'questions_answers.json', 'ACE': 'questions_answers_ACE.json'}
    filename = get_resource_path(question_sets[set_name])
    questions_data = list(load_questions(filename).values())
    show_quiz_modes()

def show_question_set_selection():
    for widget in root.winfo_children():
        widget.destroy()
    
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(side="top", fill="x", pady=10)
    
    tk.Button(top_frame, text="Home", command=show_question_set_selection, font=("Verdana", 12), bg="#f44336", fg="white").pack(side="left", padx=(10,0))
    tk.Button(top_frame, text="Info", command=show_info, font=("Verdana", 12), bg="#2196f3", fg="white").pack(side="left", padx=(10,0))
    
    tk.Label(root, text="Select Question Set", font=("Verdana", 18, "bold"), bg="#f0f0f0").pack(pady=(20, 10))
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=20, fill="x", padx=100)
    button_style = {'font': ('Verdana', 12), 'bg': '#4caf50', 'fg': 'white', 'padx': 20, 'pady': 10, 'width': 20}
    tk.Button(frame, text="CDL Questions", command=lambda: select_question_set('CDL'), **button_style).pack(pady=10)
    tk.Button(frame, text="ACE Questions", command=lambda: select_question_set('ACE'), **button_style).pack(pady=10)

def show_info():
    messagebox.showinfo("About", "This application was created by psilly-billy. You can find the source code at https://github.com/psilly-billy")

def show_quiz_modes():
    for widget in root.winfo_children():
        widget.destroy()
    setup_quiz_ui()

def setup_quiz_ui():
    global question_label, option_buttons, score_label, time_label
    tk.Button(root, text="Practice Mode", command=start_practice_quiz, font=("Verdana", 12), bg="#4caf50", fg="white").pack(pady=(10, 5))
    tk.Button(root, text="Timed Mode", command=start_timed_quiz, font=("Verdana", 12), bg="#2196f3", fg="white").pack(pady=5)
    question_frame = tk.Frame(root, bg="#f0f0f0")
    question_frame.pack(pady=10, padx=20)
    question_scrollbar = tk.Scrollbar(question_frame, orient="vertical")
    question_label = tk.Text(question_frame, wrap="word", font=("Verdana", 12), bg="#f0f0f0", borderwidth=0, highlightthickness=0, height=10, padx=10, pady=10, yscrollcommand=question_scrollbar.set)
    question_label.pack(side="left", fill="both", expand=True)
    question_scrollbar.pack(side="right", fill="y")
    question_scrollbar.config(command=question_label.yview)
    option_buttons = []
    for option_text in 'ABCD':
        button = tk.Button(root, text="", command=lambda option=option_text: check_answer(option), font=("Verdana", 12), bg="#ffffff", fg="#000000", width=20)
        button.pack(fill='x', padx=20, pady=5)
        option_buttons.append(button)
    score_label = tk.Label(root, text="Score: 0 correct, 0 incorrect", font=("Verdana", 12), bg="#f0f0f0")
    score_label.pack(pady=5)
    time_label = tk.Label(root, text="", font=("Verdana", 12), bg="#f0f0f0")
    time_label.pack()
    # Adding "Check with ChatGPT" and "Check with Gemini" buttons with updated command functions
    tk.Button(root, text="Check with ChatGPT", command=lambda: open_service_and_copy_question("ChatGPT"), font=("Verdana", 10), bg="#2196f3", fg="white").pack(fill='x', padx=20, pady=2)
    tk.Button(root, text="Check with Gemini", command=lambda: open_service_and_copy_question("Gemini"), font=("Verdana", 10), bg="#4caf50", fg="white").pack(fill='x', padx=20, pady=2)
    # Adding a "Home" button
    tk.Button(root, text="Home", command=show_question_set_selection, font=("Verdana", 12), bg="#f44336", fg="white").pack(pady=10)
    # Adding an "Info" button
    tk.Button(root, text="Info", command=show_info, font=("Verdana", 12), bg="#2196f3", fg="white").pack(pady=10)

root = tk.Tk()
root.title("Quiz Application")
root.configure(bg="#f0f0f0")
root.geometry("1200x800")

show_question_set_selection()

root.mainloop()
