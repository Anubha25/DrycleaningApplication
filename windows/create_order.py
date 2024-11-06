# windows/create_order.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime
import sys
import os

class CreateOrderWindow:
    """
    A window class for creating new orders with customer details, items, and payment information.
    Handles both UI interactions and database operations.
    """
    
    def __init__(self, parent):
        """Initialize the order creation window and data structures."""
        self.window = tk.Toplevel(parent)
        self.window.title("Create New Order")
        self.window.geometry("900x600")
        
        # Initialize empty tuples for storing data
        self.item_entries = ()     # Stores widget references
        self.order_data = ()       # Stores item details (name, quantity, price)
        self.customer_data = ()    # Stores customer information
        
        # Database configuration
        self.db_config = {
            "host": "127.0.0.1",
            "user": "root", 
            "password": "Anubhav25",
            "database": "Drycleaning",
            "port": 3306    }
        
        # Initialize total amounts
        self.total_amount = 0.0
        self.gst_amount = 0.0
        self.amount_with_gst = 0.0
        
        self.setup_ui()

    def setup_ui(self):
        """Set up the main user interface components."""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_headers(main_frame)
        self.setup_item_entries(main_frame)
        self.setup_discount_section(main_frame)
        self.setup_customer_section(main_frame)
        self.setup_payment_section(main_frame)
        self.setup_save_button(main_frame)

    def setup_headers(self, main_frame):
        """Set up the header section with column titles."""
        ttk.Label(main_frame, text="Create New Order", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        headers = ["Item", "Quantity", "Price Per Unit"]
        for i, header in enumerate(headers):
            ttk.Label(main_frame, text=header, 
                     font=('Helvetica', 10, 'bold')).grid(row=1, column=i, padx=5)

    def setup_item_entries(self, main_frame):
        """Create entry fields for items, quantity, and price."""
        entries = []
        for row in range(5):
            item_entry = ttk.Entry(main_frame)
            quantity_entry = ttk.Entry(main_frame)
            price_entry = ttk.Entry(main_frame)
            
            item_entry.grid(row=row+2, column=0, padx=5, pady=5)
            quantity_entry.grid(row=row+2, column=1, padx=5, pady=5)
            price_entry.grid(row=row+2, column=2, padx=5, pady=5)
            
            entries.append((item_entry, quantity_entry, price_entry))
        
        self.item_entries = tuple(entries)

    def setup_discount_section(self, main_frame):
        """Set up the discount and total calculation section."""
        ttk.Label(main_frame, text="Discount (%):").grid(row=7, column=0, pady=10)
        self.discount_entry = ttk.Entry(main_frame)
        self.discount_entry.grid(row=7, column=1, pady=10)
        
        calculate_btn = ttk.Button(main_frame, text="Calculate", command=self.calculate_total)
        calculate_btn.grid(row=7, column=2, pady=10)
        
        self.total_label = ttk.Label(main_frame, text="Total: 0")
        self.total_label.grid(row=7, column=3, pady=10)
        
        self.gst_label = ttk.Label(main_frame, text="Amount with GST: 0")
        self.gst_label.grid(row=7, column=4, pady=10)

    def setup_customer_section(self, main_frame):
        """Set up customer information input section."""
        customer_frame = ttk.Frame(main_frame)
        customer_frame.grid(row=8, column=0, columnspan=4, pady=10)
        
        # Customer information inputs
        self.customer_no = ttk.Entry(customer_frame)
        self.customer_no.grid(row=0, column=0, padx=5)
        ttk.Label(customer_frame, text="Customer No").grid(row=1, column=0, padx=5)
        
        self.fetch_customer_btn = ttk.Button(customer_frame, text="Fetch", command=self.fetch_customer_data)
        self.fetch_customer_btn.grid(row=0, column=1, padx=5)
        
        self.customer_name = ttk.Entry(customer_frame)
        self.customer_name.grid(row=0, column=2, padx=5)
        ttk.Label(customer_frame, text="Customer Name").grid(row=1, column=2, padx=5)
        
        self.customer_type = ttk.Combobox(customer_frame, values=["Customer", "Vendor"])
        self.customer_type.grid(row=0, column=3, padx=5)
        ttk.Label(customer_frame, text="Type").grid(row=1, column=3, padx=5)
        
        # Address section
        ttk.Label(main_frame, text="Address:").grid(row=9, column=0, pady=5)
        self.address_entry = ttk.Entry(main_frame, width=50)
        self.address_entry.grid(row=9, column=1, columnspan=3, pady=5)

    def setup_payment_section(self, main_frame):
        """Set up payment information section."""
        payment_frame = ttk.Frame(main_frame)
        payment_frame.grid(row=10, column=0, columnspan=4, pady=10)
        
        # Payment Mode
        self.payment_mode_var = tk.StringVar()
        self.payment_mode_dropdown = ttk.Combobox(payment_frame, textvariable=self.payment_mode_var, 
                                                 values=["Cash","Card","UPI","Others"])
        self.payment_mode_dropdown.grid(row=0, column=0, padx=5)
        ttk.Label(payment_frame, text="Payment Mode").grid(row=1, column=0, padx=5)
        
        # Advance Payment
        self.advance_btn = ttk.Button(payment_frame, text="Advance", 
                                    command=self.set_advance_payment)
        self.advance_btn.grid(row=0, column=1, padx=5)
        self.advance_var = tk.StringVar(value="0")
        self.advance_label = ttk.Label(payment_frame, textvariable=self.advance_var)
        self.advance_label.grid(row=1, column=1, padx=5)
        
        # Pending Amount Display
        ttk.Label(payment_frame, text="Pending Amount:").grid(row=0, column=2, padx=5)
        self.pending_var = tk.StringVar(value="0")
        self.pending_label = ttk.Label(payment_frame, textvariable=self.pending_var)
        self.pending_label.grid(row=1, column=2, padx=5)

    def setup_save_button(self, main_frame):
        """Set up the save button."""
        save_btn = ttk.Button(main_frame, text="Save", command=self.save_order)
        save_btn.grid(row=11, column=0, columnspan=4, pady=20)

    def fetch_customer_data(self):
        """Fetch customer data from the database based on the Customer No."""
        customer_no = self.customer_no.get().strip()
        if not customer_no:
            messagebox.showerror("Error", "Please enter a Customer No.")
            return

        try:
            # Connect to the database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Execute the SELECT query
            cursor.execute("SELECT Name, Type, Address FROM Customers WHERE CustomerNo = %s", (customer_no,))
            result = cursor.fetchone()

            if result:
                self.customer_name.delete(0, tk.END)
                self.customer_name.insert(0, result[0])
                self.customer_type.set(result[1])
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, result[2])
            else:
                messagebox.showerror("Error", "No customer found with the given Customer No.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

    def set_payment_mode(self):
        """Handle payment mode input via dialog."""
        mode = simpledialog.askstring("Payment Mode", "Enter Payment Mode:")
        if mode:
            self.payment_mode_var.set(mode)

    def set_advance_payment(self):
        """Handle advance payment input and calculate pending amount."""
        if not hasattr(self, 'amount_with_gst') or self.amount_with_gst == 0:
            messagebox.showerror("Error", "Please calculate total first")
            return
            
        advance = simpledialog.askfloat("Advance Payment", "Enter Advance Amount:",
                                      minvalue=0.0)
        if advance is not None:
            if advance > self.amount_with_gst:
                messagebox.showerror("Error", "Advance cannot be greater than total amount with GST")
                return
                
            self.advance_var.set(f"{advance:.2f}")
            # Calculate pending amount based on amount with GST
            pending = self.amount_with_gst - advance
            self.pending_var.set(f"{pending:.2f}")

    def calculate_total(self):
        """Calculate total amount, GST, and prepare order data."""
        total = 0
        items_data = []
        
        for item_entry, quantity_entry, price_entry in self.item_entries:
            try:
                item = item_entry.get().strip()
                quantity = int(quantity_entry.get()) if quantity_entry.get().strip() else 0
                price = float(price_entry.get()) if price_entry.get().strip() else 0
                
                subtotal = quantity * price
                total += subtotal
                
                if item and quantity and price:
                    items_data.append((item, quantity, price))
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for quantity and price")
                return
        
        try:
            discount = float(self.discount_entry.get()) if self.discount_entry.get().strip() else 0
            discounted_price = total - (total * discount / 100)
            self.gst_amount = discounted_price * 0.18  # 18% GST
            self.amount_with_gst = discounted_price + self.gst_amount
            
            self.total_amount = discounted_price
            self.total_label.config(text=f"Total: {discounted_price:.2f}")
            self.gst_label.config(text=f"Amount with GST: {self.amount_with_gst:.2f}")
            self.pending_var.set(f"{self.amount_with_gst:.2f}")
            
            # Store items data as tuple
            self.order_data = tuple(items_data)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid discount percentage")

    def save_order(self):
        """Save order details to database with transaction handling."""
        # Validate required fields
        if not self.validate_order():
            return
            
        # Prepare customer data
        self.customer_data = (
            self.customer_no.get().strip(),
            self.customer_name.get().strip(),
            self.customer_type.get(),
            self.address_entry.get().strip()
        )
        
        # Calculate totals
        total_items = sum(int(qty_entry.get()) for _, qty_entry, _ in self.item_entries 
                         if qty_entry.get().strip())
        
        try:
            # Connect to database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            try:
                # Start transaction
                cursor.execute("START TRANSACTION")
                
                # Insert or update customer
                cursor.execute("""
                    INSERT INTO Customers (CustomerNo, Name, Type, Address)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    Name = VALUES(Name),
                    Type = VALUES(Type),
                    Address = VALUES(Address)
                """, self.customer_data)
                
                # Insert order
                order_data = (
                    self.customer_no.get(),
                    total_items,
                    float(self.discount_entry.get() if self.discount_entry.get().strip() else 0),
                    self.total_amount,
                    self.amount_with_gst,
                    self.payment_mode_var.get(),
                    float(self.advance_var.get()),
                    float(self.pending_var.get())
                )
                
                cursor.execute("""
                    INSERT INTO Orders (CustomerNo, Total_Items, Discount, Amount, 
                                      Amount_with_GST, Payment_Mode, Received_Amount, 
                                      Pending_Amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, order_data)
                
                # Get the last inserted order ID
                order_id = cursor.lastrowid
                
                # Insert items
                for item, quantity, price in self.order_data:
                    cursor.execute("""
                        INSERT INTO Items (OrderId, Item_Name, Quantity, Price)
                        VALUES (%s, %s, %s, %s)
                    """, (order_id, item, quantity, price))
                
                # Commit transaction
                conn.commit()
                messagebox.showinfo("Success", "Order saved successfully!")
                self.window.destroy()  # Close window after successful save
                
            except mysql.connector.Error as err:
                conn.rollback()
                messagebox.showerror("Database Error", f"Error: {err}")
                
            finally:
                cursor.close()
                conn.close()
                
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {err}")

    def validate_order(self):
        """Validate all required fields before saving."""
        if not self.customer_no.get().strip():
            messagebox.showerror("Error", "Customer No is required")
            return False
            
        if not self.customer_name.get().strip():
            messagebox.showerror("Error", "Customer Name is required")
            return False
            
        if not self.customer_type.get():
            messagebox.showerror("Error", "Customer Type is required")
            return False
            
        if not self.payment_mode_var.get():
            messagebox.showerror("Error", "Payment Mode is required")
            return False
            
        if not self.order_data:
            messagebox.showerror("Error", "At least one item is required")
            return False
            
        return True
