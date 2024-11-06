import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class viewOrderWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("View Order Details")
        self.window.geometry("1220x600")
        self.phoneNumber = None
        self.orderId = None
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Part 1: Phone Number Search
        phone_frame = ttk.LabelFrame(main_frame, text="Search Order by Phone Number", padding="10")
        phone_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(phone_frame, text="Enter Phone Number to fetch Orders:").grid(row=0, column=0, padx=5)
        self.phone_entry = ttk.Entry(phone_frame)
        self.phone_entry.grid(row=0, column=1, padx=5)
        ttk.Button(phone_frame, text="Fetch", command=self.fetch_orders).grid(row=0, column=2, padx=5)

        # Orders Table
        orders_frame = ttk.Frame(main_frame)
        orders_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Create Treeview with scrollbar for orders
        self.orders_tree = ttk.Treeview(orders_frame, columns=(
            "OrderId", "CustomerNo", "Total_Items", "Discount", "Amount",
            "Amount_with_GST", "Payment_Mode", "Received_Amount",
            "Pending_Amount", "Status", "OrderDate"
        ), show="headings")

        # Set column headings
        for col in self.orders_tree["columns"]:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=105)

        # Add scrollbars
        orders_yscroll = ttk.Scrollbar(orders_frame, orient="vertical", command=self.orders_tree.yview)
        orders_xscroll = ttk.Scrollbar(orders_frame, orient="horizontal", command=self.orders_tree.xview)
        self.orders_tree.configure(yscrollcommand=orders_yscroll.set, xscrollcommand=orders_xscroll.set)

        # Grid the Treeview and scrollbars
        self.orders_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        orders_yscroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        orders_xscroll.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Part 2: Order ID Search
        order_frame = ttk.LabelFrame(main_frame, text="Search by Order ID", padding="10")
        order_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(order_frame, text="Enter OrderId to fetch Order details:").grid(row=0, column=0, padx=5)
        self.order_entry = ttk.Entry(order_frame)
        self.order_entry.grid(row=0, column=1, padx=5)
        ttk.Button(order_frame, text="Fetch", command=self.fetch_items).grid(row=0, column=2, padx=5)

        # Items Table
        items_frame = ttk.Frame(main_frame)
        items_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Create Treeview with scrollbar for items
        self.items_tree = ttk.Treeview(items_frame, columns=(
             "Item", "Price Per Unit", "Quantity"
        ), show="headings")

        # Set column headings
        for col in self.items_tree["columns"]:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)

        # Add scrollbars
        items_yscroll = ttk.Scrollbar(items_frame, orient="vertical", command=self.items_tree.yview)
        items_xscroll = ttk.Scrollbar(items_frame, orient="horizontal", command=self.items_tree.xview)
        self.items_tree.configure(yscrollcommand=items_yscroll.set, xscrollcommand=items_xscroll.set)

        # Grid the Treeview and scrollbars
        self.items_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        items_yscroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        items_xscroll.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        orders_frame.columnconfigure(0, weight=1)
        items_frame.columnconfigure(0, weight=1)

    def fetch_orders(self):
        self.phoneNumber = self.phone_entry.get()
        if not self.phoneNumber:
            messagebox.showerror("Error", "Please enter a phone number")
            return

        try:
            # Clear existing items
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)

            # Database connection
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Anubhav25",
                database="Drycleaning"
            )
            cursor = conn.cursor()

            # Execute query
            query = "SELECT * FROM orders WHERE CustomerNo = %s"
            cursor.execute(query, (self.phoneNumber,))
            
            # Fetch and display results
            for row in cursor.fetchall():
                self.orders_tree.insert("", "end", values=row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def fetch_items(self):
        try:
            self.orderId = int(self.order_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric Order ID")
            return

        try:
            # Clear existing items
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)

            # Database connection
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Anubhav25",
                database="Drycleaning"
            )
            cursor = conn.cursor()

            # Execute query
            query = "SELECT Item_Name,Price,Quantity FROM items WHERE OrderId = %s"
            cursor.execute(query, (self.orderId,))
            
            # Fetch and display results
            for row in cursor.fetchall():
                self.items_tree.insert("", "end", values=row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")