# main.py

from gui.main_window import MainWindow
import tkinter as tk
import os, sys
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS "BookSubjects" (
    "book_id"    INTEGER,
    "subject_id"    INTEGER,
    FOREIGN KEY("subject_id") REFERENCES "Subjects"("subject_id"),
    FOREIGN KEY("book_id") REFERENCES "Books"("book_id")
);
CREATE TABLE IF NOT EXISTS "Books" (
    "book_id"    INTEGER,
    "library_id"    INTEGER,
    "title"    TEXT NOT NULL,
    "author"    TEXT,
    "isbn"    TEXT,
    "copies"    INTEGER NOT NULL,
    "loaned"    TEXT NOT NULL,
    "notes"    TEXT,
    PRIMARY KEY("book_id" AUTOINCREMENT),
    FOREIGN KEY("library_id") REFERENCES "Libraries"("library_id")
);
CREATE TABLE IF NOT EXISTS "Subjects" (
    "subject_id"    INTEGER,
    "subject_name"    TEXT NOT NULL,
    "subject_notes"    TEXT,
    PRIMARY KEY("subject_id")
);
CREATE TABLE IF NOT EXISTS "Libraries" (
    "library_id"    INTEGER,
    "name"    TEXT NOT NULL,
    "notes"    TEXT,
    PRIMARY KEY("library_id")
);
"""

def get_script_directory():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        return os.path.dirname(sys.executable)
    else:
        # Get the absolute path of the script
        script_path = os.path.abspath(__file__)
        # Return the directory containing the script
        return os.path.dirname(script_path)

def check_files():
    # Get the script directory
    script_directory = get_script_directory()

    # Combine the script directory with the relative paths to your files
    library_directory = os.path.join(script_directory, "library")
    config_file_path = os.path.join(library_directory, "config.ini")

    print("Config file path: {}".format(config_file_path))
    print("Library directory: {}".format(library_directory))

    # Check if the library directory exists
    if not os.path.exists(library_directory):
        print("Library directory not found. Creating a new one.")
        os.mkdir(library_directory)

    # Check if the config file exists
    if not os.path.exists(config_file_path):
        print("Config file not found. Creating a new one.")
        # Create config file with a default database file path
        with open(config_file_path, "w+") as config_file:
            config_file.write("PATH_TO_DB_FILE = " + os.path.join(library_directory, "tgl.db"))
    else:
        print("Config file found. Importing...")

    # Read the database file path from the config file
    with open(config_file_path, "r") as config_file:
        lines = config_file.readlines()

    # Check if the config file is empty and set a default path
    if not lines:
        lines.append("PATH_TO_DB_FILE = " + os.path.join(library_directory, "tgl.db"))
        with open(config_file_path, "w+") as config_file:
            config_file.write(lines[0])

    # Extract the path to the database file from the config
    path = lines[0].split("=")[1].strip()
    print("Import successful. Database file path: {}".format(path))

    # Check if the database file exists - if not, create it from schema
    if not os.path.exists(path):
        print("Database file not found. Creating a new one.")
        # Create the database file using the schema
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.executescript(SCHEMA)

        print("Database file created.")
    else:
        print("Database file found. Importing...")

    print("Import successful.")

if __name__ == "__main__":
    check_files()

    root = tk.Tk()
    app = MainWindow(root)
    root.resizable(False, False)
    root.mainloop()
