import tkinter as tk
from tkinter import messagebox
import random
import csv
import time

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        
        self.flashcards = self.load_flashcards("flashcards.csv")
        self.current_index = 0
        self.showing_question = True
        self.show_only_unknown = False
        self.quiz_mode = False
        self.time_left = 60
        self.correct_answers = 0
        self.total_questions = len(self.flashcards)
        
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        
        self.question_text = self.canvas.create_text(400, 300, text="", font=("Arial", 24, "italic"))
        
        self.flip_button = tk.Button(root, text="Flip", command=self.flip_flashcard, width=10, height=2)
        self.flip_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.prev_button = tk.Button(root, text="Previous", command=self.show_previous_flashcard, width=10, height=2)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.next_button = tk.Button(root, text="Next", command=self.show_next_flashcard, width=10, height=2)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.shuffle_button = tk.Button(root, text="Shuffle", command=self.shuffle_flashcards, width=10, height=2)
        self.shuffle_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.known_button = tk.Button(root, text="Known", command=self.mark_known, width=10, height=2)
        self.known_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.unknown_button = tk.Button(root, text="Unknown", command=self.mark_unknown, width=10, height=2)
        self.unknown_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.filter_button = tk.Button(root, text="Filter Unknown", command=self.toggle_filter, width=15, height=2)
        self.filter_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.quiz_button = tk.Button(root, text="Quiz Mode", command=self.toggle_quiz_mode, width=15, height=2)
        self.quiz_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.timer_label = tk.Label(root, text=f"Time left: {self.time_left}s", font=("Arial", 16))
        self.timer_label.pack(side=tk.TOP, pady=10)
        
        self.answer_entry = tk.Entry(root, font=("Arial", 24))
        self.answer_entry.pack(side=tk.BOTTOM, pady=10)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        self.show_flashcard()
        
        self.root.bind("<space>", self.flip_flashcard)
    
    def load_flashcards(self, filename):
        flashcards = []
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["question"] == "Boiling point of water":
                        row["answer"] = "100"
                    row["known"] = False
                    flashcards.append(row)
            print(f"Loaded flashcards: {flashcards}")  # Debug print
            return flashcards
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {filename} not found.")
            self.root.quit()
        except csv.Error:
            messagebox.showerror("Error", f"File {filename} is not a valid CSV file.")
            self.root.quit()
    
    def show_flashcard(self):
        print(f"Current index: {self.current_index}, Showing question: {self.showing_question}")  # Debug print
        if self.flashcards:
            flashcard = self.flashcards[self.current_index]
            print(f"Showing flashcard: {flashcard}")  # Debug print
            text = flashcard["question"] if self.showing_question else flashcard["answer"]
            self.canvas.itemconfig(self.question_text, text=text)
            if self.quiz_mode and self.showing_question:
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.pack(side=tk.BOTTOM, pady=10)
            else:
                self.answer_entry.pack_forget()
        else:
            self.canvas.itemconfig(self.question_text, text="No flashcards available.")
    
    def flip_flashcard(self, event=None):
        if not self.quiz_mode:
            print("Flipping flashcard")  # Debug print
            self.showing_question = not self.showing_question
            self.show_flashcard()
    
    def check_answer(self, event=None):
        if self.flashcards:
            flashcard = self.flashcards[self.current_index]
            user_answer = self.answer_entry.get().strip().lower()
            correct_answer = flashcard["answer"].strip().lower()
            if user_answer == correct_answer:
                messagebox.showinfo("Correct!", "Your answer is correct!")
                self.correct_answers += 1
            else:
                messagebox.showinfo("Incorrect", f"The correct answer was: {flashcard['answer']}")
            self.showing_question = False
            self.show_flashcard()
            if self.quiz_mode:
                self.show_next_flashcard()
                if self.current_index == 0:
                    self.end_quiz_mode()
    
    def toggle_quiz_mode(self):
        self.quiz_mode = not self.quiz_mode
        self.showing_question = True
        self.correct_answers = 0
        if self.quiz_mode:
            self.time_left = 60
            self.update_timer()
        else:
            self.timer_label.config(text="")
        self.show_flashcard()
    
    def end_quiz_mode(self):
        self.quiz_mode = False
        self.timer_label.config(text="")
        percentage_correct = (self.correct_answers / self.total_questions) * 100
        messagebox.showinfo("Quiz Completed", f"You answered {percentage_correct:.2f}% of questions correctly.")
        self.show_flashcard()
    
    def update_timer(self):
        if self.quiz_mode:
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=f"Time left: {self.time_left}s")
                self.root.after(1000, self.update_timer)
            else:
                messagebox.showinfo("Time's up!", "You ran out of time!")
                self.end_quiz_mode()
    
    def show_next_flashcard(self):
        print("Showing next flashcard")  # Debug print
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            self.showing_question = True
            self.show_flashcard()
            if self.quiz_mode:
                self.answer_entry.delete(0, tk.END)
    
    def show_previous_flashcard(self):
        print("Showing previous flashcard")  # Debug print
        if self.flashcards:
            self.current_index = (self.current_index - 1) % len(self.flashcards)
            self.showing_question = True
            self.show_flashcard()
            if self.quiz_mode:
                self.answer_entry.delete(0, tk.END)
    
    def shuffle_flashcards(self):
        print("Shuffling flashcards")  # Debug print
        random.shuffle(self.flashcards)
        self.current_index = 0
        self.showing_question = True
        self.show_flashcard()
        if self.quiz_mode:
            self.answer_entry.delete(0, tk.END)
    
    def mark_known(self):
        print("Marking flashcard as known")  # Debug print
        if self.flashcards:
            self.flashcards[self.current_index]["known"] = True
            self.flip_flashcard()  # Flip the flashcard
            self.show_next_flashcard()
            if self.quiz_mode:
                self.answer_entry.delete(0, tk.END)
    
    def mark_unknown(self):
        print("Marking flashcard as unknown")  # Debug print
        if self.flashcards:
            self.flashcards[self.current_index]["known"] = False
            self.flip_flashcard()  # Flip the flashcard
            self.show_next_flashcard()
            if self.quiz_mode:
                self.answer_entry.delete(0, tk.END)
    
    def toggle_filter(self):
        print("Toggling filter for unknown flashcards")  # Debug print
        self.show_only_unknown = not self.show_only_unknown
        if self.show_only_unknown:
            self.flashcards = [card for card in self.flashcards if not card["known"]]
        else:
            self.flashcards = self.load_flashcards("flashcards.csv")
        self.current_index = 0
        self.show_flashcard()
        if self.quiz_mode:
            self.answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
