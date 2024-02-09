import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.database import Database  # Import the Database class

class AddBookWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Add Book")

        # Entry for title
        self.title_var = tk.StringVar()
        self.title_label = ttk.Label(parent, text="Title:")
        self.title_entry = ttk.Entry(parent, textvariable=self.title_var)

        # Entry for author
        self.author_var = tk.StringVar()
        self.author_label = ttk.Label(parent, text="Author:")
        self.author_entry = ttk.Entry(parent, textvariable=self.author_var)

        # Drop-down box for location
        self.location_var = tk.StringVar()
        self.location_label = ttk.Label(parent, text="Location:")
        self.location_combobox = ttk.Combobox(parent, textvariable=self.location_var)

        # Entry for ISBN
        self.isbn_var = tk.StringVar()
        self.isbn_label = ttk.Label(parent, text="ISBN:")
        self.isbn_entry = ttk.Entry(parent, textvariable=self.isbn_var)

        # Entry for copies
        self.copies_var = tk.IntVar()
        self.copies_label = ttk.Label(parent, text="Copies:")
        self.copies_entry = ttk.Entry(parent, textvariable=self.copies_var, validate="key", validatecommand=(parent.register(self.validate_copies), "%P"))

        # Listbox for subjects
        self.subjects_listbox = tk.Listbox(parent, selectmode=tk.MULTIPLE, height=5)
        self.subjects_label = ttk.Label(parent, text="Subjects:")

        # Populate the subjects listbox
        self.populate_subjects_listbox()

        # Checkbox for loaned
        self.loaned_var = tk.StringVar(value="N")  # Default is "N"
        self.loaned_checkbox = ttk.Checkbutton(parent, text="Loaned", variable=self.loaned_var, onvalue="Y", offvalue="N")

        # Text box for notes
        self.notes_var = tk.StringVar()
        self.notes_label = ttk.Label(parent, text="Notes:")
        self.notes_text = tk.Text(parent, height=5, width=40, wrap="word", font=("Arial", 10), relief="solid", borderwidth=1)

        # Buttons
        self.confirm_button = ttk.Button(parent, text="Confirm", command=self.create_book_record)
        self.cancel_button = ttk.Button(parent, text="Cancel", command=self.cancel)

        # Grid layout
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.author_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.location_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.location_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.isbn_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.isbn_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.copies_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.copies_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.subjects_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.subjects_listbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.loaned_checkbox.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.notes_label.grid(row=7, column=0, padx=5, pady=5, sticky="ne")
        self.notes_text.grid(row=7, column=1, padx=5, pady=5, sticky="nw")
        self.confirm_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.cancel_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Populate the location combobox with library names
        self.populate_location_combobox()

    def create_book_record(self):
        # Get other details for creating the book record
        title = self.title_var.get()
        author = self.author_var.get()
        location_id = self.get_location_id()
        isbn = self.isbn_var.get()
        copies = self.copies_var.get()
        loaned = self.loaned_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Check if required fields are not empty
        if not title or not author or location_id is None or copies is None:
            messagebox.showwarning("Error", "Please fill in all required fields.")
            return

        # Call the function to add the book to the database
        db = Database()
        book_id = db.add_book(title, author, location_id, isbn, copies, loaned, notes)
        db.close_connection()

        messagebox.showinfo("Success", "Book added successfully.")

        # Get the selected subjects from the listbox
        self.selected_subjects = []
        self.selected_subjects = self.subjects_listbox.curselection()

        # After creating the book record, add subjects if any are selected
        if self.selected_subjects:
            self.add_selected_subjects(book_id)

        self.parent.destroy()

    def add_selected_subjects(self, book_id):
        # Add the selected subjects to the database
        db = Database()
        for subject in self.selected_subjects:
            subject_id = db.get_subject_id(self.subjects_listbox.get(subject))
            db.add_book_subject(book_id, subject_id)
        db.close_connection()

    def cancel(self):
        self.parent.destroy()

    def populate_location_combobox(self):
        # Populate the location combobox with library names
        db = Database()
        libraries = db.get_library_names()
        db.close_connection()

        self.location_combobox["values"] = [library[0] for library in libraries]

        try:
            self.location_combobox.current(0)  # Set the default selection
        except Exception:
            messagebox.showwarning("Error", "No libraries found. Please add a library first.")
            self.parent.destroy()

    def populate_subjects_listbox(self):
        # Populate the subjects listbox with subject names
        db = Database()
        subjects = db.get_subject_names()
        db.close_connection()

        for subject in subjects:
            self.subjects_listbox.insert(tk.END, subject)

    def get_location_id(self):
        # Get the selected location ID from the combobox
        selected_library = self.location_combobox.get()

        db = Database()
        location_id = db.get_library_id(selected_library)
        db.close_connection()

        return location_id

    def validate_copies(self, new_value):
        # Validate the entry for copies to allow only non-negative integer values
        try:
            value = int(new_value)
            return value >= 0
        except ValueError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = AddBookWindow(root)
    root.mainloop()
