import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.database import Database  # Import the Database class

class AddSubjectWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Add Subject")

        # Entry for subject name
        self.subject_name_var = tk.StringVar()
        self.subject_name_label = ttk.Label(parent, text="Subject Name:")
        self.subject_name_entry = ttk.Entry(parent, textvariable=self.subject_name_var)

        # Buttons
        self.confirm_button = ttk.Button(parent, text="Confirm", command=self.confirm)
        self.cancel_button = ttk.Button(parent, text="Cancel", command=self.cancel)

        # Grid layout
        self.subject_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.subject_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.confirm_button.grid(row=1, column=0, columnspan=2, pady=10)
        self.cancel_button.grid(row=2, column=0, columnspan=2, pady=10)

    def confirm(self):
        # Get the entered subject name
        subject_name = self.subject_name_var.get()

        # Check if the subject name is not empty
        if not subject_name:
            messagebox.showwarning("Error", "Please enter a subject name.")
            return

        # Call the function to add the subject to the database
        db = Database()
        db.add_subject(subject_name)
        db.close_connection()

        messagebox.showinfo("Success", "Subject added successfully.")
        self.parent.destroy()

    def cancel(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AddSubjectWindow(root)
    root.mainloop()
