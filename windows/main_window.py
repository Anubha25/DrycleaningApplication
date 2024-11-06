# main_window.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from windows.create_order import CreateOrderWindow
from windows.view_order import viewOrderWindow
from windows.update_tables import UpdateOrdersWindow
from windows.Invoice import InvoiceOrder

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dry Cleaning Desktop Application")
        self.root.geometry("1000x800")  # Increased window size for better layout
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1000x800+{x}+{y}")
        
        self.setup_background()
        self.setup_ui()

    def setup_background(self):
        try:
            # Load and process background image
            image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "main.png")
            original_image = Image.open(image_path)
            
            # Resize image to fit window
            resized_image = original_image.resize((1000, 800), Image.Resampling.LANCZOS)
            
            # Create transparent version (40% opacity)
            transparent_image = Image.new('RGBA', resized_image.size, (255, 255, 255, 0))
            transparent_image = Image.blend(transparent_image, resized_image.convert('RGBA'), 0.8)
            
            self.bg_image = ImageTk.PhotoImage(transparent_image)
            
            # Create and place background label
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Create white background as fallback
            self.root.configure(bg='white')

    def setup_ui(self):
        # Create main container frame
        container = tk.Frame(self.root, bg='white', padx=20, pady=20)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Application Title
        title_frame = tk.Frame(container, bg='white')
        title_frame.pack(pady=(0, 40))
        
        title_label = tk.Label(
            title_frame,
            text="Dry Cleaning Application",
            font=('Helvetica', 32, 'bold'),
            bg='white',
            fg='#333333'  # Dark gray text
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="Management System",
            font=('Helvetica', 16),
            bg='white',
            fg='#666666'  # Medium gray text
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Buttons Frame
        buttons_frame = tk.Frame(container, bg='white')
        buttons_frame.pack(pady=20)
        
        # Button style configuration
        button_style = {
            'font': ('Helvetica', 14),
            'width': 25,
            'height': 2,
            'border': 0,
            'cursor': 'hand2',
            'borderwidth': 0,
            'relief': 'flat',
        }
        
        # Hover effects
        def on_enter(e):
            e.widget['background'] = e.widget.hover_color
        
        def on_leave(e):
            e.widget['background'] = e.widget.default_color
        
        # Create Order Button
        create_btn = tk.Button(
            buttons_frame,
            text="Create Order",
            command=self.open_create_order,
            bg='#ADD8E6',  # Light Blue
            **button_style
        )
        create_btn.default_color = '#ADD8E6'
        create_btn.hover_color = '#9CC8D6'
        create_btn.pack(pady=10)
        create_btn.bind("<Enter>", on_enter)
        create_btn.bind("<Leave>", on_leave)
        
        # Fetch Order Button
        fetch_btn = tk.Button(
            buttons_frame,
            text="View Orders ",
            command=self.open_view_order,
            bg='#FFFFE0',  # Light Yellow
            **button_style
        )
        fetch_btn.default_color = '#FFFFE0'
        fetch_btn.hover_color = '#EFEED0'
        fetch_btn.pack(pady=10)
        fetch_btn.bind("<Enter>", on_enter)
        fetch_btn.bind("<Leave>", on_leave)
        
        # Update Tables Button
        update_btn = tk.Button(
            buttons_frame,
            text="Update Orders",
            command=self.open_update_tables,
            bg='#FFB6C1',  # Light Pink
            **button_style
        )
        update_btn.default_color = '#FFB6C1'
        update_btn.hover_color = '#EFA6B1'
        update_btn.pack(pady=10)
        update_btn.bind("<Enter>", on_enter)
        update_btn.bind("<Leave>", on_leave)

        #invoice button
        invoice_btn = tk.Button(
            buttons_frame,
            text="Invoice Order",
            command=self.open_Invoice_Order,
            bg='#FFB6d3',  
            **button_style
        )
        invoice_btn.default_color = '#FFB6C1'
        invoice_btn.hover_color = '#EFA6B1'
        invoice_btn.pack(pady=10)
        invoice_btn.bind("<Enter>", on_enter)
        invoice_btn.bind("<Leave>", on_leave)

    def open_create_order(self):
        CreateOrderWindow(self.root)

    def open_view_order(self):
        viewOrderWindow(self.root)

    def open_update_tables(self):
        UpdateOrdersWindow(self.root)
    def open_Invoice_Order(self):
        InvoiceOrder(self.root)

    def run(self):
        self.root.mainloop()
