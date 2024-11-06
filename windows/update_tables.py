import tkinter as tk
from tkinter import ttk
import mysql.connector
import tkinter.messagebox

class UpdateOrdersWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Update Orders")
        self.window.geometry("500x350")

        # Center the window
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2
        self.window.geometry(f"500x350+{x}+{y}")

        self.OrderId = None
        self.value = None
        self.setup_ui()

    def setup_ui(self):
        # Heading
        heading_label = tk.Label(
            self.window,
            text="Update Orders",
            font=("Helvetica", 18, "bold"),
            pady=20
        )
        heading_label.pack()

        # Order ID
        order_id_frame = tk.Frame(self.window)
        order_id_frame.pack(pady=10)

        order_id_label = tk.Label(order_id_frame, text="Order ID:")
        order_id_label.pack(side=tk.LEFT)

        vcmd = (self.window.register(self.validate_numeric), '%P')
        self.order_id_entry = ttk.Entry(order_id_frame, validate='key', validatecommand=vcmd)
        self.order_id_entry.pack(side=tk.LEFT, padx=10)

        # Status options
        status_options = ["Received", "Warehouse 1", "Warehouse 2", "Warehouse 3", "Received from Warehouse", "Pickup", "Complete"]
        status_frame = tk.Frame(self.window)
        status_frame.pack(pady=10)

        status_label = tk.Label(status_frame, text="Update Status:")
        status_label.pack(side=tk.LEFT)

        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(
            status_frame,
            textvariable=self.status_var,
            values=status_options,
            state="readonly"
        )
        self.status_combo.pack(side=tk.LEFT, padx=10)

        # Update button
        update_button = tk.Button(
            self.window,
            text="Update",
            command=self.update_order,
            padx=20,
            pady=10
        )
        update_button.pack(pady=20)

        # Delete Completed Orders button
        delete_button = tk.Button(
            self.window,
            text="Remove Complete Orders Information",
            command=self.delete_completed_orders,
            padx=20,
            pady=10
        )
        delete_button.pack(pady=10)

    def validate_numeric(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def update_order(self):
        try:
            # Get values from UI
            self.OrderId = int(self.order_id_entry.get())
            self.value = self.status_var.get()

            # Connect to the database
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Anubhav25",
                database="Drycleaning"
            )
            cursor = db.cursor()

            # Update the order status
            update_query = "UPDATE orders SET status = %s WHERE OrderId = %s"
            cursor.execute(update_query, (self.value, self.OrderId))
            db.commit()

            # Display success message
            tk.messagebox.showinfo("Success", "Order status updated.")

        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            if 'db' in locals():
                db.close()

    def delete_completed_orders(self):
        try:
            # Connect to the database
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Anubhav25",
                database="Drycleaning"
            )
            cursor = db.cursor()

            # Get a list of completed order IDs
            cursor.execute("SELECT OrderId FROM orders WHERE status = 'Complete'")
            completed_orders = [order[0] for order in cursor.fetchall()]

            if not completed_orders:
                tk.messagebox.showinfo("No Completed Orders", "There are no completed orders to remove.")
                return

            # Delete items for completed orders
            for order_id in completed_orders:
                cursor.execute("DELETE FROM items WHERE OrderId = %s", (order_id,))

            # Delete completed orders
            for order_id in completed_orders:
                cursor.execute("DELETE FROM orders WHERE OrderId = %s", (order_id,))

            db.commit()

            tk.messagebox.showinfo("Completed Orders Removed", "All the Orders which were in complete state are removed from the Database.")

        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            if 'db' in locals():
                db.close()