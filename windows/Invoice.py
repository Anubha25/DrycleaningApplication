import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class InvoiceOrder:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Invoice Order")
        self.window.geometry("400x200")
        self.OrderId = None
        self.result1 = None
        self.result2 = None
        self.setup_ui()

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

        # Generate Invoice button
        invoice_button = ttk.Button(main_frame, text="Generate Invoice", command=self.generate_invoice)
        invoice_button.grid(row=1, column=0, columnspan=2, pady=20)

    def validate_numeric(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def generate_invoice(self):
        try:
            # Validate input
            if not self.order_id_entry.get():
                messagebox.showerror("Error", "Please enter an Order ID")
                return

            self.OrderId = int(self.order_id_entry.get())
            
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
                    return

                cursor.execute("SELECT * FROM items WHERE OrderId = %s", (self.OrderId,))
                self.result2 = cursor.fetchall()

                self.create_pdf()
                messagebox.showinfo("Success", f"Invoice_{self.OrderId}.pdf has been generated successfully!")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Database error: {err}")

            finally:
                if 'db' in locals():
                    db.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_pdf(self):
        doc = SimpleDocTemplate(
            f"Invoice_{self.OrderId}.pdf",
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        elements = []

        # Add heading
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            alignment=1,  # Center alignment
            spaceAfter=30
        )
        elements.append(Paragraph("Dry Cleaning Total Bill", title_style))

        # Customer and Order Information
        customer_data = [
            ["Customer Number:", str(self.result1[1])]
        ]
        customer_table = Table(customer_data, colWidths=[1.5*inch, 2*inch])
        customer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(customer_table)

        # Order details
        order_data = [
            ["Order ID:", str(self.result1[0]), "Total Items:", str(self.result1[2]), "Order Date:", str(self.result1[10])]
        ]
        order_table = Table(order_data, colWidths=[1*inch, 1*inch, 1.2*inch, 0.8*inch, 0.8*inch, 1.5*inch])
        order_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(order_table)
        elements.append(Spacer(1, 20))

        # Items details
        items_data = [['Item', 'Quantity', 'Price Per Unit']]
        for item in self.result2:
            items_data.append([str(item[2]), str(item[3]), str(item[4])])

        items_table = Table(items_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ]))
        elements.append(items_table)
        
        elements.append(Spacer(1, 20))

        # Summary information
        summary_data = [
            ["Discount:", str(self.result1[3]),"Amount with GST:", str(self.result1[5]), 
             "Payment Mode:", str(self.result1[6])]
        ]
        summary_table = Table(summary_data, colWidths=[1*inch, 1*inch, 1.3*inch, 1*inch, 1.2*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(summary_table)

        # Final details
        final_data = [
            ["Advance:", str(self.result1[7]), "Pending:", str(self.result1[8]), 
             "Order Status:", str(self.result1[9])]
        ]
        final_table = Table(final_data, colWidths=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.5*inch])
        final_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(final_table)

        # Build the PDF
        doc.build(elements, onFirstPage=self.add_page_border, onLaterPages=self.add_page_border)

    def add_page_border(self, canvas, doc):
        # Add border around the page
        canvas.saveState()
        canvas.setLineWidth(1)
        canvas.rect(10, 10, 590, 780)
        canvas.restoreState()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceOrder(root)
    root.mainloop()
