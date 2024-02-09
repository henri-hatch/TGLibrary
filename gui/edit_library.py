import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.database import Database

class EditLibraryWindow:
    def __init__(self, parent, data):
        self.parent = parent
        self.parent.title("Edit Library")

        # Initialize DB
        db = Database()

        # Get the library data
        self.id = data[0]
        self.name = data[1]

        self.notes = db.get_library_notes(self.id)
        if self.notes == None:
            self.notes = ""

        # Close DB connection
        db.close_connection()

        # Entry for library name
        self.name_var = tk.StringVar()
        self.name_label = ttk.Label(parent, text="Library Name:")
        self.name_entry = ttk.Entry(parent, textvariable=self.name_var)

        # Text for library notes
        self.notes_text = tk.Text(parent, height=10, width=40)
        self.notes_label = ttk.Label(parent, text="Notes:")

        # Button to save changes
        self.save_button = ttk.Button(parent, text="Save", command=self.save)

        # Button to delete the library
        self.delete_button = ttk.Button(parent, text="Delete", command=self.delete)

        # Button to cancel
        self.cancel_button = ttk.Button(parent, text="Cancel", command=self.cancel)

        # Populate the entry fields with the data
        self.populate_fields()

        # Place the widgets on the window
        self.name_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, sticky="W", padx=10, pady=10)
        self.notes_label.grid(row=1, column=0, sticky="W", padx=10, pady=10)
        self.notes_text.grid(row=1, column=1, sticky="W", padx=10, pady=10)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.delete_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def populate_fields(self):
        self.name_var.set(self.name)
        self.notes_text.insert(tk.END, self.notes)

    def save(self):
        # Get the new data
        new_name = self.name_var.get()
        new_notes = self.notes_text.get("1.0", tk.END)

        # Initialize DB
        db = Database()

        # Update the library
        db.update_library(self.id, new_name, new_notes)

        # Close DB connection
        db.close_connection()

        # Show success message
        messagebox.showinfo("Success", "Library updated successfully")

        # Close the window
        self.parent.destroy()

    def delete(self):
        # Confirm the deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this library?")

        if confirm:
            # Initialize DB
            db = Database()

            # Delete the library
            db.delete_library(self.id)

            # Close DB connection
            db.close_connection()

            # Show success message
            messagebox.showinfo("Success", "Library deleted successfully")

            # Close the window
            self.parent.destroy()


    def cancel(self):
        self.parent.destroy()

            