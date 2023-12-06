# main.py

from gui.main_window import MainWindow
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.resizable(False, False)
    root.mainloop()
