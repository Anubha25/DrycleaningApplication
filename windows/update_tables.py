import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class UpdateTablesWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Update Tables")
        self.window.geometry("800x600")
        
        # Center the window
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.window.geometry(f"800x600+{x}+{y}")
        
        self.setup_background()
        self.setup_ui()

    def setup_background(self):
        try:
            # Load and process background image
            image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "tables.png")
            original_image = Image.open(image_path)
            
            # Resize image to fit window
            resized_image = original_image.resize((800, 600), Image.Resampling.LANCZOS)
            
            # Create transparent version (40% opacity)
            transparent_image = Image.new('RGBA', resized_image.size, (255, 255, 255, 0))
            transparent_image = Image.blend(transparent_image, resized_image.convert('RGBA'), 0.4)
            
            self.bg_image = ImageTk.PhotoImage(transparent_image)
            
            # Create and place background label
            self.bg_label = tk.Label(self.window, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Create white background as fallback
            self.window.configure(bg='white')

    def setup_ui(self):
        # Create main container frame with semi-transparent white background
        container = tk.Frame(self.window, bg='white')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_frame = tk.Frame(container, bg='white')
        title_frame.pack(pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Update Tables",
            font=('Helvetica', 24, 'bold'),
            bg='white',
            fg='#333333'
        )
        title_label.pack()
        
        # Add your table update elements here
        # For example:
        content_frame = tk.Frame(container, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Example table selection dropdown
        ttk.Label(
            content_frame,
            text="Select Table:",
            font=('Helvetica', 12)
        ).pack(pady=(0, 5))
        
        table_combo = ttk.Combobox(
            content_frame,
            values=["Customers", "Orders", "Services"],
            width=30
        )
        table_combo.pack(pady=(0, 20))