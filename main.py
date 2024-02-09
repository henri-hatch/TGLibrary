# main.py

from gui.main_window import MainWindow
import tkinter as tk
import os
import sqlite3

def check_files():
    # Check if the config file exists
    config_file_path = "config.ini"
    if not os.path.exists(config_file_path):
        print("Config file not found. Creating a new one.")
        # Create config file with a default database file path
        with open(config_file_path, "w") as config_file:
            config_file.write("PATH_TO_DB_FILE = tgl.db")
    else:
        print("Config file found. Importing...")

    # Read the database file path from the config file
    with open(config_file_path, "r") as config_file:
        lines = config_file.readlines()

    # Check if the config file is empty and set a default path
    if not lines:
        lines.append("PATH_TO_DB_FILE = tgl.db")
        with open(config_file_path, "w") as config_file:
            config_file.write(lines[0])

    # Extract the path to the database file from the config
    path = lines[0].split("=")[1].strip()
    print("Import successful. Database file path: {}".format(path))

    # Check if the database file exists - if not, create it from schema
    if not os.path.exists(path):
        print("Database file not found. Creating a new one.")
        # Read schema from the file
        with open("assets/schema.txt", "r") as schema_file:
            schema = schema_file.read()

        # Create the database file using the schema
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.executescript(schema)

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
