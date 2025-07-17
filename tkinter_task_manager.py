import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import uuid
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Task Manager App")
        self.tasks = []

        # UI Elements
        self.desc_label = tk.Label(root, text="Task Description:")
        self.desc_entry = tk.Entry(root, width=40)

        self.priority_label = tk.Label(root, text="Priority:")
        self.priority_combo = ttk.Combobox(root, values=["1 (High)", "2 (Medium)", "3 (Low)"], width=15)
        self.priority_combo.current(0)

        self.add_btn = tk.Button(root, text="Add Task", command=self.add_task)
        self.remove_btn = tk.Button(root, text="Remove Task", command=self.remove_task)
        self.recommend_btn = tk.Button(root, text="Recommend Task", command=self.recommend_task)

        self.task_listbox = tk.Listbox(root, width=80, height=10)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.task_listbox.yview)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Layout
        self.desc_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        self.priority_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.priority_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.add_btn.grid(row=2, column=0, padx=5, pady=10)
        self.remove_btn.grid(row=2, column=1, padx=5, pady=10)
        self.recommend_btn.grid(row=2, column=2, padx=5, pady=10)

        self.task_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        self.scrollbar.grid(row=3, column=3, sticky='ns')

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

    def add_task(self):
        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")
            return

        priority = int(self.priority_combo.get()[0])
        task_id = str(uuid.uuid4())[:8]
        self.tasks.append({'id': task_id, 'description': desc, 'priority': priority})
        self.update_listbox()
        self.desc_entry.delete(0, tk.END)

    def remove_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a task to remove.")
            return

        task_text = self.task_listbox.get(selection[0])
        task_id = task_text.split('|')[0].split(':')[1].strip()
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.update_listbox()

    def recommend_task(self):
        if len(self.tasks) < 2:
            messagebox.showinfo("Insufficient Data", "Add at least 2 tasks to get recommendations.")
            return

        input_desc = simpledialog.askstring("Recommend", "Enter task description to find similar:")
        if not input_desc:
            return

        descriptions = [task['description'] for task in self.tasks]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(descriptions + [input_desc])
        similarity = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()

        index = similarity.argmax()
        recommended = self.tasks[index]
        messagebox.showinfo("Recommended Task",
                            f"ID: {recommended['id']}\nPriority: {recommended['priority']}\nDescription: {recommended['description']}")

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        sorted_tasks = sorted(self.tasks, key=lambda x: x['priority'])
        for task in sorted_tasks:
            self.task_listbox.insert(
                tk.END,
                f"ID: {task['id']} | Priority: {task['priority']} | {task['description']}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
