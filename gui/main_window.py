# main_window.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.database import Database

from gui.add_library import AddLibraryWindow
from gui.add_subject import AddSubjectWindow
from gui.add_book import AddBookWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Teaghlach Gramhar Library")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, columnspan=6, rowspan=4, padx=5, pady=5, sticky="nsew")

        # Create tabs for books, subjects, and libraries
        self.book_tab = ttk.Frame(self.notebook)
        self.subject_tab = ttk.Frame(self.notebook)
        self.library_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.book_tab, text="Books")
        self.notebook.add(self.subject_tab, text="Subjects")
        self.notebook.add(self.library_tab, text="Libraries")

        # Call functions to populate each tab
        self.populate_books_tab()
        self.populate_subjects_tab()
        self.populate_libraries_tab()

        # Search bar and filter options
        self.search_var = tk.StringVar()

        self.filter_var = tk.StringVar()
        self.filter_var.set("Title")  # Default filter option

        # Create an entry with a placeholder
        self.search_entry = tk.Entry(self.root, width=30, textvariable=self.search_var, fg="grey")
        self.search_entry.insert(0, "Search...")  # Insert the placeholder text
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)

        self.filter_dropdown = ttk.Combobox(self.root, values=["Title", "Author", "Subject", "Location", "ISBN"],
                                            textvariable=self.filter_var)
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.filter_books)
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_filter)

        # Button to open a new window to add a new book, library, or subject
        self.add_button = ttk.Button(self.root, text="Add", command=self.open_add_window)

        # Button to open a new window to edit a book, library, or subject
        self.edit_button = ttk.Button(self.root, text="Edit", command=self.open_edit_window)

        # Grid layout
        self.search_entry.grid(row=0, column=0, columnspan=2, pady=20, padx=(120, 0))
        self.filter_dropdown.grid(row=0, column=2, padx=5, pady=5)
        self.submit_button.grid(row=0, column=3, padx=5, pady=5)
        self.clear_button.grid(row=0, column=4, padx=5, pady=5)
        self.add_button.grid(row=5, column=0, columnspan=4, pady=20, padx=(0, 120))
        self.edit_button.grid(row=5, column=4, pady=20, padx=5)

    def populate_books_tab(self):
        self.headers = ["Title", "Author", "Subject", "Location", "ISBN", "Copies", "Loaned?"]

        # Table to display books
        self.tree = ttk.Treeview(self.book_tab, columns=self.headers, show="headings", height=10)

        # Insert headers over the columns
        for col, header in enumerate(self.headers):
            self.tree.heading(col, text=header)
            if header == "Copies" or header == "Loaned?":
                self.tree.column(col, width=50)

        self.tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.book_tab, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=7, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Call database for all books
        db = Database()
        books_data = db.get_all_books_data()
        db.close_connection()

        # Insert data into the table
        for book in books_data:
            self.tree.insert("", "end", values=book)

    def populate_subjects_tab(self):
        self.headers = ["Subject Name"]

        # Table to display books
        self.tree = ttk.Treeview(self.subject_tab, columns=self.headers, show="headings", height=10)

        # Insert headers over the columns
        for col, header in enumerate(self.headers):
            self.tree.heading(col, text=header)

        self.tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.subject_tab, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=7, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Call database for all subjects
        db = Database()
        subjects_data = db.get_subjects()
        db.close_connection()

        # Insert data into the table
        for subject in subjects_data:
            self.tree.insert("", "end", values=subject)

    def populate_libraries_tab(self):
        self.headers = ["Library Name"]

        # Table to display books
        self.tree = ttk.Treeview(self.library_tab, columns=self.headers, show="headings", height=10)

        # Insert headers over the columns
        for col, header in enumerate(self.headers):
            self.tree.heading(col, text=header)

        self.tree.grid(row=2, column=1, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.library_tab, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=7, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Call database for all libraries
        db = Database()
        libraries_data = db.get_libraries()
        db.close_connection()

        # Insert data into the table
        for library in libraries_data:
            self.tree.insert("", "end", values=library)

    def filter_books(self):
        # Get the filter option and search query
        filter_option = self.filter_var.get()
        search_query = self.search_var.get()

        # Check which tab is currently selected
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 0:
            self.filter_books_by(filter_option, search_query)
        elif selected_tab == 1:
            self.filter_subjects_by(filter_option, search_query)
        elif selected_tab == 2:
            self.filter_libraries_by(filter_option, search_query)

    def filter_books_by(self, filter_option, search_query):
        # Check if the search query is empty
        if not search_query:
            messagebox.showwarning("Error", "Please enter a search query.")
            return

        # Call database for filtered books
        db = Database()
        books_data = db.get_filtered_books_data(filter_option, search_query)
        db.close_connection()

        # Clear the table
        self.tree.delete(*self.tree.get_children())

        # Insert data into the table
        for book in books_data:
            self.tree.insert("", "end", values=book)

    def clear_filter(self):
        self.populate_all_table()

    def open_add_window(self):
        # Open window for adding either book, library, or subject

        # Check which tab is currently selected
        selected_tab = self.notebook.index(self.notebook.select())

        if selected_tab == 0:
            # Open window for adding a book
            book_window = tk.Toplevel(self.root)
            AddBookWindow(book_window)
        elif selected_tab == 1:
            # Open window for adding a subject
            subject_window = tk.Toplevel(self.root)
            AddSubjectWindow(subject_window)
        elif selected_tab == 2:
            # Open window for adding a library
            library_window = tk.Toplevel(self.root)
            AddLibraryWindow(library_window)

    def open_edit_window(self):
        # Get value for highlighted row
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return

        # Get the values of the selected row
        selected_values = self.tree.item(selected_item)["values"]

        # Open window for editing a book
        messagebox.showinfo("Edit Book", "Open Book Window")

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="light slate gray")  # Change text color to black

    def restore_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search...")
            self.search_entry.config(fg="grey")  # Change text color to grey

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.resizable(False, False)
    root.mainloop()
