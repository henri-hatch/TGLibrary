import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.database import Database  # Import your Database class

class AddLibraryWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Add Library")

        # Entry for library name
        self.library_name_var = tk.StringVar()
        self.library_name_label = ttk.Label(parent, text="Library Name:")
        self.library_name_entry = ttk.Entry(parent, textvariable=self.library_name_var)

        # Text box for library notes
        self.library_notes_var = tk.StringVar()
        self.library_notes_label = ttk.Label(parent, text="Notes:")
        self.library_notes_text = tk.Text(parent, height=5, width=40, wrap="word", font=("Arial", 10), relief="solid", borderwidth=1)

        # Buttons
        self.confirm_button = ttk.Button(parent, text="Confirm", command=self.confirm)
        self.cancel_button = ttk.Button(parent, text="Cancel", command=self.cancel)

        # Grid layout
        self.library_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.library_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.library_notes_label.grid(row=1, column=0, padx=5, pady=5, sticky="ne")
        self.library_notes_text.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
        self.confirm_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.cancel_button.grid(row=3, column=0, columnspan=2, pady=10)

    def confirm(self):
        # Get the entered library name
        library_name = self.library_name_var.get()

        # Check if the library name is not empty
        if not library_name:
            messagebox.showwarning("Error", "Please enter a library name.")
            return

        # Call the function to add the library to the database
        db = Database()
        db.add_library(library_name)
        db.close_connection()

        messagebox.showinfo("Success", "Library added successfully.")
        self.parent.destroy()

    def cancel(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AddLibraryWindow(root)
    root.mainloop()
