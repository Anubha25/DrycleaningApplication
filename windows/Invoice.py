import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pywhatkit as pwk
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile

class InvoiceOrder:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Invoice Order")
        self.window.geometry("600x300")
        self.OrderId = None
        self.Phone = None
        self.result1 = None
        self.result2 = None
        self.setup_ui()
        
        # Initialize fonts - adjust paths based on your system
        try:
            self.title_font = ImageFont.truetype("arial.ttf", 36)
            self.header_font = ImageFont.truetype("arial.ttf", 16)
            self.normal_font = ImageFont.truetype("arial.ttf", 14)
        except:
            # Fallback to default font if arial.ttf is not found
            self.title_font = ImageFont.load_default()
            self.header_font = ImageFont.load_default()
            self.normal_font = ImageFont.load_default()

    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Order ID label and entry with validation
        order_id_label = ttk.Label(main_frame, text="Order ID:")
        order_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        vcmd = (self.window.register(self.validate_numeric), '%P')
        self.order_id_entry = ttk.Entry(main_frame, validate='key', validatecommand=vcmd)
        self.order_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # WhatsApp number label and entry
        whatsapp_label = ttk.Label(main_frame, text="WhatsApp No:")
        whatsapp_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.whatsapp_entry = ttk.Entry(main_frame)
        self.whatsapp_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Caution label with red text
        caution_frame = ttk.Frame(main_frame)
        caution_frame.grid(row=2, column=0, columnspan=2, pady=(10, 5))
        
        caution_label = ttk.Label(
            caution_frame, 
            text="⚠️ Login WhatsApp Web In Default Browser",
            foreground='red',
            font=('Helvetica', 10, 'bold')
        )
        caution_label.pack()

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Generate and Send button
        whatsapp_button = ttk.Button(
            button_frame, 
            text="Generate & Send to WhatsApp", 
            command=self.generate_and_send
        )
        whatsapp_button.grid(row=0, column=1, padx=5)

    def validate_numeric(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def validate_and_get_inputs(self):
        if not self.order_id_entry.get():
            messagebox.showerror("Error", "Please enter an Order ID")
            return False

        self.OrderId = int(self.order_id_entry.get())
        self.Phone = self.whatsapp_entry.get().strip()
        return True

    def create_invoice_image(self):
        """Create invoice as an image directly"""
        # Create a new image with white background
        img_width = 1000
        img_height = 1400
        image = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(image)

        # Add border
        draw.rectangle([(20, 20), (img_width-20, img_height-20)], outline='black', width=2)

        # Initialize y_position for dynamic content placement
        y_position = 50

        # Add title
        title = "Dry Cleaning Total Bill"
        title_bbox = draw.textbbox((0, 0), title, font=self.title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((img_width - title_width) // 2, y_position), title, fill='black', font=self.title_font)
        y_position += 80

        # Customer Information
        draw.text((50, y_position), f"Customer Number: {self.result1[1]}", fill='black', font=self.header_font)
        y_position += 40

        # Order Details
        draw.text((50, y_position), f"Order ID: {self.result1[0]}", fill='black', font=self.normal_font)
        draw.text((300, y_position), f"Total Items: {self.result1[2]}", fill='black', font=self.normal_font)
        draw.text((550, y_position), f"Order Date: {self.result1[10]}", fill='black', font=self.normal_font)
        y_position += 50

        # Draw table headers
        headers = ['Item', 'Quantity', 'Price Per Unit']
        col_widths = [400, 200, 200]
        x_position = 50
        
        # Draw table header background
        header_height = 30
        draw.rectangle([(50, y_position), (850, y_position + header_height)], fill='grey')
        
        # Draw header text
        for header, width in zip(headers, col_widths):
            draw.text((x_position + 10, y_position + 5), header, fill='white', font=self.header_font)
            x_position += width
        y_position += header_height

        # Draw items
        for item in self.result2:
            x_position = 50
            item_data = [str(item[2]), str(item[3]), str(item[4])]
            
            # Draw row background (alternating colors)
            row_height = 30
            draw.rectangle([(50, y_position), (850, y_position + row_height)], fill='white', outline='grey')
            
            # Draw item data
            for data, width in zip(item_data, col_widths):
                draw.text((x_position + 10, y_position + 5), data, fill='black', font=self.normal_font)
                x_position += width
            y_position += row_height

        y_position += 30

        # Summary Information
        draw.text((50, y_position), f"Discount: {self.result1[3]}", fill='black', font=self.normal_font)
        draw.text((300, y_position), f"Amount with GST: {self.result1[5]}", fill='black', font=self.normal_font)
        draw.text((550, y_position), f"Payment Mode: {self.result1[6]}", fill='black', font=self.normal_font)
        y_position += 40

        # Final Details
        draw.text((50, y_position), f"Advance: {self.result1[7]}", fill='black', font=self.normal_font)
        draw.text((300, y_position), f"Pending: {self.result1[8]}", fill='black', font=self.normal_font)
        draw.text((550, y_position), f"Order Status: {self.result1[9]}", fill='black', font=self.normal_font)

        # Save image to temporary file
        temp_image_path = os.path.join(tempfile.gettempdir(), f"Invoice_{self.OrderId}.png")
        image.save(temp_image_path, 'PNG')
        return temp_image_path

    def generate_and_send(self):
        if not self.validate_and_get_inputs():
            return

        if not self.Phone:
            messagebox.showerror("Error", "Please enter a WhatsApp number")
            return

        try:
            # Clean the phone number
            self.Phone = self.Phone.replace(" ", "").replace("-", "")
            if not self.Phone.startswith("+"):
                self.Phone = "+91" + self.Phone

            # Database connection
            try:
                db = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="Anubhav25",
                    database="Drycleaning"
                )
                cursor = db.cursor()

                # Execute queries
                cursor.execute("SELECT * FROM orders WHERE OrderId = %s", (self.OrderId,))
                self.result1 = cursor.fetchone()

                if not self.result1:
                    messagebox.showerror("Error", f"No order found with ID: {self.OrderId}")
                    return False

                cursor.execute("SELECT * FROM items WHERE OrderId = %s", (self.OrderId,))
                self.result2 = cursor.fetchall()

                # Generate image
                image_path = self.create_invoice_image()

                # Send via WhatsApp
                pwk.sendwhats_image(
                    receiver=self.Phone,
                    img_path=image_path,
                    caption=f"Invoice for Order #{self.OrderId}\nThank you for your business!",
                    wait_time=15,
                    tab_close=True
                )
                
                messagebox.showinfo(
                    "Success", 
                    "Invoice has been generated and sent successfully via WhatsApp!"
                )

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Database error: {err}")

            finally:
                if 'db' in locals():
                    db.close()
                # Clean up temporary file
                if 'image_path' in locals() and os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                    except:
                        pass

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while processing your request:\n{str(e)}"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceOrder(root)
    root.mainloop()