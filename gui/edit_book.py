import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.database import Database

class EditBookWindow:
    def __init__(self, parent, data):
        self.parent = parent
        self.parent.title("Edit Book")

        # Initialize DB
        db = Database()

        # Get the book data
        self.id = data[0]
        self.title = data[1]
        self.author = data[2]
        self.subjects = data[3]
        self.location = data[4]
        self.isbn = data[5]
        self.copies = data[6]
        self.loaned = data[7]
        self.notes = db.get_book_notes(self.id)

        # Close DB connection
        db.close_connection()

        # Entry for book title
        self.title_var = tk.StringVar()
        self.title_label = ttk.Label(parent, text="Title:")
        self.title_entry = ttk.Entry(parent, textvariable=self.title_var)

        # Entry for book author
        self.author_var = tk.StringVar()
        self.author_label = ttk.Label(parent, text="Author:")
        self.author_entry = ttk.Entry(parent, textvariable=self.author_var)

        # Combobox for book location
        self.location_var = tk.StringVar()
        self.location_label = ttk.Label(parent, text="Location:")
        self.location_combobox = ttk.Combobox(parent, textvariable=self.location_var)

        # Populate the location combobox with library names
        self.populate_location_combobox()
        
        # Entry for book ISBN
        self.isbn_var = tk.StringVar()
        self.isbn_label = ttk.Label(parent, text="ISBN:")
        self.isbn_entry = ttk.Entry(parent, textvariable=self.isbn_var)

        # Entry for book copies
        self.copies_var = tk.IntVar()
        self.copies_label = ttk.Label(parent, text="Copies:")
        self.copies_entry = ttk.Entry(parent, textvariable=self.copies_var, validate="key", validatecommand=(parent.register(self.validate_copies), "%P"))

        # Listbox for book subjects
        self.subjects_listbox = tk.Listbox(parent, selectmode=tk.MULTIPLE, height=5)
        self.subjects_label = ttk.Label(parent, text="Subjects:")

        # Populate the subjects listbox
        self.populate_subjects_listbox()

        # Checkbox for loaned
        self.loaned_var = tk.StringVar(value=self.loaned)
        self.loaned_checkbox = ttk.Checkbutton(parent, text="Loaned", variable=self.loaned_var, onvalue="Y", offvalue="N")

        # Text box for notes
        self.notes_var = tk.StringVar()
        self.notes_label = ttk.Label(parent, text="Notes:")
        self.notes_text = tk.Text(parent, height=5, width=40, wrap="word", font=("Arial", 10), relief="solid", borderwidth=1)
        
        # Populate the notes text box
        self.populate_notes_text()

        # Buttons
        self.confirm_button = ttk.Button(parent, text="Save", command=self.update_book_record)
        self.delete_button = ttk.Button(parent, text="Delete", command=self.delete_book_record)
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
        self.notes_text.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.confirm_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.delete_button.grid(row=9, column=0, columnspan=2, pady=10)
        self.cancel_button.grid(row=10, column=0, columnspan=2, pady=10)

        # Populate the entry fields
        self.populate_entry_fields()

    def populate_entry_fields(self):
        self.title_var.set(self.title)
        self.author_var.set(self.author)
        self.isbn_var.set(self.isbn)
        self.copies_var.set(self.copies)

        # Parse subjects into a list
        subjects = self.subjects.split(", ")

        # Convert tuple to a list
        subjects_list = list(self.subjects_listbox.get(0, tk.END))

        # Select the subjects in the listbox
        for subject in subjects:
            try:
                index = subjects_list.index(subject)
                self.subjects_listbox.selection_set(index)
            except ValueError:
                # Handle the case where the subject is not found in the list
                pass

    def populate_subjects_listbox(self):
        # Get the subjects from the database
        db = Database()
        subjects = db.get_subject_names()
        db.close_connection()

        # Populate the subjects listbox
        for subject in subjects:
            self.subjects_listbox.insert(tk.END, subject)

    def populate_location_combobox(self):
        # Get the libraries from the database
        db = Database()
        libraries = db.get_library_names()
        db.close_connection()

        # Populate the location combobox with library names without brackets
        self.location_combobox["values"] = [library[0] for library in libraries]


        # Select the location for the book
        self.location_combobox.set(self.location)

    def populate_notes_text(self):
        self.notes_text.insert(tk.END, self.notes)

    def validate_copies(self, new_value):
        # Validate the entry for copies to allow only non-negative integer values
        try:
            value = int(new_value)
            return value >= 0
        except ValueError:
            return False
        
    def get_location_id(self):
        # Get the location name from the combobox
        location_name = self.location_var.get()

        # Get the location ID from the database
        db = Database()
        location_id = db.get_library_id(location_name)
        db.close_connection()

        return location_id
    
    def update_book_record(self):
        # Get other details for updating the book record
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

        # Call the function to update the book in the database
        db = Database()
        db.update_book(self.id, title, author, location_id, isbn, copies, loaned, notes)
        db.close_connection()

        # Update the subjects for the book
        selected_subjects = []
        selected_subjects = self.subjects_listbox.curselection()

        self.update_book_subjects(selected_subjects)


        messagebox.showinfo("Success", "Book updated successfully.")
        self.parent.destroy()

    def update_book_subjects(self, selected_subjects):
        db = Database()
        db.delete_book_subjects(self.id)

        for subject in selected_subjects:
            subject_id = db.get_subject_id(self.subjects_listbox.get(subject))
            db.add_book_subject(self.id, subject_id)

        db.close_connection()

    def delete_book_record(self):
        # Confirm the deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this book?")

        if confirm:
            # Initialize DB
            db = Database()

            # Delete the book
            db.delete_book(self.id)

            # Delete the book subjects
            db.delete_book_subjects(self.id)

            # Close DB connection
            db.close_connection()

            messagebox.showinfo("Success", "Book deleted successfully.")
            self.parent.destroy()

    def cancel(self):
        self.parent.destroy()
