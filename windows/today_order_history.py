import tkinter as tk
from tkinter import ttk
import mysql.connector

class TodayOrderHistoryWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Today's Order History")
        self.window.geometry("1400x700")  # Increased width to accommodate all columns

        self.setup_ui()
        self.fetch_orders()

    def setup_ui(self):
        # Create container frame
        container = tk.Frame(self.window, bg='white', padx=20, pady=20)
        container.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        title_label = tk.Label(
            container,
            text="Today's Order History",
            font=('Helvetica', 24, 'bold'),
            bg='white',
            fg='#333333'
        )
        title_label.pack(pady=(0, 20))

        # Create frame for treeview and scrollbars
        tree_frame = tk.Frame(container)
        tree_frame.pack(fill='both', expand=True)

        # Create scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar.pack(side='bottom', fill='x')

        # Orders table
        self.orders_tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Configure scrollbars
        y_scrollbar.config(command=self.orders_tree.yview)
        x_scrollbar.config(command=self.orders_tree.xview)

        # Define and configure columns
        columns = (
            'OrderID', 'CustomerNo', 'total_items', 'Discount', 'Amount',
            'Amount_with_Gst', 'Payment_Mode', 'Received_Amount', 'Pending_Amount',
            'Status', 'OrderDate'
        )
        self.orders_tree['columns'] = columns

        # Configure index column
        self.orders_tree.column('#0', width=50, minwidth=50, stretch=False)
        self.orders_tree.heading('#0', text='S.No')

        # Configure columns with their properties
        column_configs = {
            'OrderID': {'width': 80, 'text': 'Order ID'},
            'CustomerNo': {'width': 100, 'text': 'Customer No'},
            'total_items': {'width': 80, 'text': 'Total Items'},
            'Discount': {'width': 80, 'text': 'Discount'},
            'Amount': {'width': 100, 'text': 'Amount'},
            'Amount_with_Gst': {'width': 120, 'text': 'Amount with GST'},
            'Payment_Mode': {'width': 100, 'text': 'Payment Mode'},
            'Received_Amount': {'width': 120, 'text': 'Received Amount'},
            'Pending_Amount': {'width': 120, 'text': 'Pending Amount'},
            'Status': {'width': 100, 'text': 'Status'},
            'OrderDate': {'width': 150, 'text': 'Order Date'}
        }

        # Apply configurations to each column
        for col, config in column_configs.items():
            self.orders_tree.column(col, width=config['width'], minwidth=config['width'], anchor='center')
            self.orders_tree.heading(col, text=config['text'])

        self.orders_tree.pack(fill='both', expand=True)

        # Style configuration
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)

        # Configure row tags for alternating colors
        self.orders_tree.tag_configure('oddrow', background='#f9f9f9')
        self.orders_tree.tag_configure('evenrow', background='white')

        # Total revenue label
        self.total_revenue_label = tk.Label(
            container,
            text="Today's Total Revenue: Rs. 0.00",
            font=('Helvetica', 16, 'bold'),
            bg='white',
            fg='#333333'
        )
        self.total_revenue_label.pack(pady=(20, 0))

    def fetch_orders(self):
        try:
            # Connect to MySQL database
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Anubhav25",
                database="Drycleaning"
            )

            cursor = db.cursor()

            # Fetch orders for today with specific columns in the correct order
            query = """
            SELECT OrderId, CustomerNo, Total_Items, Discount, Amount, 
                Amount_with_gst, Payment_Mode, Received_Amount, 
                Pending_Amount, Status, OrderDate 
            FROM Orders 
            WHERE DATE(OrderDate) = CURRENT_DATE()
            ORDER BY OrderID DESC;
            """
            cursor.execute(query)
            orders = cursor.fetchall()

            # Clear existing data in the tree
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)

            # Populate the tree with orders
            for i, order in enumerate(orders):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.orders_tree.insert('', 'end', text=f"{i+1}", values=order, tags=(tag,))

            # Calculate and display total revenue
            cursor.execute("SELECT SUM(amount_with_gst) FROM Orders WHERE DATE(OrderDate) = CURRENT_DATE()")
            total_revenue = cursor.fetchone()[0]
            if total_revenue is None:
                total_revenue = 0
            self.total_revenue_label.config(text=f"Today's Total Revenue: Rs. {total_revenue:.2f}")

            db.close()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            self.total_revenue_label.config(text="Today's Total Revenue: Rs. 0.00 (Error loading data)")
