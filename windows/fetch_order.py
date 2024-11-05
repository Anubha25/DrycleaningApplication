import tkinter as tk
from tkinter import ttk

class FetchOrderWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Fetch Order Details")
        self.window.geometry("600x400")
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Fetch Order Details", font=('Helvetica', 14, 'bold')).grid(row=0, column=0)
        # Add search and display elements
