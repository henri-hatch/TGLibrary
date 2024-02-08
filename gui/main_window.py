# main_window.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.database import Database

from gui.add_library import AddLibraryWindow
from gui.add_subject import AddSubjectWindow
from gui.add_book import AddBookWindow

from gui.edit_book import EditBookWindow

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
        self.populate_libraries_tab()
        self.populate_subjects_tab()

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
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.filter)
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


############################################################################################################
# Populate Tabs
############################################################################################################


    def populate_books_tab(self):
        self.headers = ["ID", "Title", "Author", "Subject", "Location", "ISBN", "Copies", "Loaned?"]

        # Table to display books
        self.booktree = ttk.Treeview(self.book_tab, columns=self.headers, show="headings", height=10)

        # Insert headers over the columns
        for col, header in enumerate(self.headers):
            self.booktree.heading(col, text=header)
            if header == "ID":
                self.booktree.column(col, width=30)
            if header == "Copies" or header == "Loaned?":
                self.booktree.column(col, width=50)

        self.booktree.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.book_tab, orient="vertical", command=self.booktree.yview)
        scrollbar.grid(row=2, column=7, sticky="ns")
        self.booktree.configure(yscrollcommand=scrollbar.set)

        # Call database for all books
        db = Database()
        books_data = db.get_all_books_data()
        db.close_connection()

        # Insert data into the table
        for book in books_data:
            self.booktree.insert("", "end", values=book)

    def populate_subjects_tab(self):
        self.headers = ["ID", "Subject Name"]

        # Table to display books
        self.subjecttree = ttk.Treeview(self.subject_tab, columns=self.headers, show="headings", height=10)

        # Insert headers over the columns
        for col, header in enumerate(self.headers):
            self.subjecttree.heading(col, text=header)
            if header == "ID":
                self.subjecttree.column(col, width=30)

        self.subjecttree.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.subject_tab, orient="vertical", command=self.subjecttree.yview)
        scrollbar.grid(row=2, column=7, sticky="ns")
        self.subjecttree.configure(yscrollcommand=scrollbar.set)

        # Call database for all subjects
        db = Database()
        subjects_data = db.get_subjects()
        db.close_connection()

        # Insert data into the table
        for subject in subjects_data:
            self.subjecttree.insert("", "end", values=subject)

    def populate_libraries_tab(self):
        self.headers = ["ID", "Library Name"]

        # Table to display books
        self.librarytree = ttk.Treeview(self.library_tab, columns=self.headers, show="headings", height=10)

        # Insert headers over the columns
        for col, header in enumerate(self.headers):
            self.librarytree.heading(col, text=header)
            if header == "ID":
                self.librarytree.column(col, width=30)

        self.librarytree.grid(row=2, column=1, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.library_tab, orient="vertical", command=self.librarytree.yview)
        scrollbar.grid(row=2, column=7, sticky="ns")
        self.librarytree.configure(yscrollcommand=scrollbar.set)

        # Call database for all libraries
        db = Database()
        libraries_data = db.get_libraries()
        db.close_connection()

        # Insert data into the table
        for library in libraries_data:
            self.librarytree.insert("", "end", values=library)


############################################################################################################
# Filter and Search
############################################################################################################


    def filter(self):
        # Get the filter option and search query
        filter_option = self.filter_var.get()
        search_query = self.search_var.get()

        # Check which tab is currently selected
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 0:
            self.filter_books_by(filter_option, search_query)
        elif selected_tab == 1:
            self.filter_subjects_by(search_query)
        elif selected_tab == 2:
            self.filter_libraries_by(search_query)

    def filter_books_by(self, filter_option, search_query):
        # Check if the search query is empty
        if not search_query:
            messagebox.showwarning("Error", "Please enter a search query.")
            return

        # Call database for filtered books
        db = Database()
        if filter_option == "Title":
            books_data = db.get_books_by_title(search_query)
        elif filter_option == "Author":
            books_data = db.get_books_by_author(search_query)
        elif filter_option == "Subject":
            books_data = db.get_books_by_subject(search_query)
        elif filter_option == "Location":
            books_data = db.get_books_by_location(search_query)
        elif filter_option == "ISBN":
            books_data = db.get_books_by_isbn(search_query)
        else:
            messagebox.showwarning("Error", "Invalid filter option.")
        db.close_connection()

        # Clear the table
        self.booktree.delete(*self.booktree.get_children())

        # Insert data into the table
        for book in books_data:
            self.booktree.insert("", "end", values=book)

    def filter_subjects_by(self, search_query):
        # Check if the search query is empty
        if not search_query:
            messagebox.showwarning("Error", "Please enter a search query.")
            return

        # Call database for filtered subjects
        db = Database()
        subjects_data = db.get_subjects_by_name(search_query)
        db.close_connection()

        # Clear the table
        self.subjecttree.delete(*self.subjecttree.get_children())

        # Insert data into the table
        for subject in subjects_data:
            self.subjecttree.insert("", "end", values=subject)

    def filter_libraries_by(self, search_query):
        # Check if the search query is empty
        if not search_query:
            messagebox.showwarning("Error", "Please enter a search query.")
            return

        # Call database for filtered libraries
        db = Database()
        libraries_data = db.get_libraries_by_name(search_query)
        db.close_connection()

        # Clear the table
        self.librarytree.delete(*self.librarytree.get_children())

        # Insert data into the table
        for library in libraries_data:
            self.librarytree.insert("", "end", values=library)

    def clear_filter(self):
        self.populate_books_tab()
        self.populate_libraries_tab()
        self.populate_subjects_tab()


############################################################################################################
# Add and Edit Windows
############################################################################################################


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
        # Open window for editing either book, library, or subject

        # Check which tab is currently selected
        selected_tab = self.notebook.index(self.notebook.select())

        # Check what is selected in the table based on the selected tab
        if selected_tab == 0:
            selected_item = self.booktree.selection()[0]

            # Get the data from the selected row
            book_data = self.booktree.item(selected_item, "values")
            print(book_data)

        elif selected_tab == 1:
            selected_item = self.subjecttree.selection()[0]

            # Get the data from the selected row
            subject_data = self.subjecttree.item(selected_item, "values")
            print(subject_data)

        elif selected_tab == 2:
            selected_item = self.librarytree.selection()[0]

            # Get the data from the selected row
            library_data = self.librarytree.item(selected_item, "values")
            print(library_data)

        
        # Open window for editing either book, library, or subject with the data from the selected row
        if selected_tab == 0:
            book_window = tk.Toplevel(self.root)
            EditBookWindow(book_window, book_data)
        # elif selected_tab == 1:
        #     subject_window = tk.Toplevel(self.root)
        #     EditSubjectWindow(subject_window, subject_data)
        # elif selected_tab == 2:
        #     library_window = tk.Toplevel(self.root)
        #     EditLibraryWindow(library_window, library_data)
        

############################################################################################################
# Search Bar and Filter Options
############################################################################################################


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
