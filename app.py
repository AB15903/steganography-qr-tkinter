# app.py

import tkinter as tk
from src.gui import StegoApp  # Ensure gui.py defines StegoApp class



def main():
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

