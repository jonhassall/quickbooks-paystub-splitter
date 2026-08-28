import fitz  # PyMuPDF
import re
import os
import sys
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dotenv import load_dotenv
from PIL import Image, ImageTk

__version__ = "1.0.0"

# Helper to find resources bundled with PyInstaller or local directory
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load environment variables
load_dotenv(get_resource_path('.env'))
APP_TITLE = os.getenv('APP_NAME', 'Paystub Splitter')
LOGO_FILENAME = os.getenv('LOGO_PATH', '').strip()

def sanitize_filename(name, default=""):
    if not name:
        return default
    # Replace newlines and tabs with spaces
    name = re.sub(r'[\r\n\t]+', ' ', name)
    # Remove characters forbidden in Windows filenames: \ / : * ? " < > |
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    # Strip leading/trailing dots, spaces, underscores
    name = name.strip('._ ')
    return name if name else default

class PaystubSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} v{__version__}")
        self.root.geometry("640x480")
        self.root.resizable(False, False)
        
        self.root.rowconfigure(7, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('vista' if 'vista' in style.theme_names() else 'default')
        style.configure('.', font=("Segoe UI", 11))
        style.configure('TButton', font=("Segoe UI", 11))
        style.configure('Header.TLabel', font=("Segoe UI", 16, "bold"))
        style.configure('Desc.TLabel', font=("Segoe UI", 10), foreground="#444444")
        style.configure('Status.TLabel', font=("Segoe UI", 10, "italic"))
        style.configure('ActionButton.TButton', font=("Segoe UI", 12, "bold"))
        style.configure('Credit.TLabel', font=("Segoe UI", 9), foreground="#0066cc")
        
        # Form Variables
        self.input_pdf = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready to process.")
        
        # Set Window Icon if logo exists
        self.logo_image = None
        if LOGO_FILENAME:
            logo_path = get_resource_path(LOGO_FILENAME)
            if os.path.isfile(logo_path):
                try:
                    pil_img = Image.open(logo_path)
                    # Keep reference for tkinter icon & header
                    icon_img = pil_img.resize((32, 32), Image.Resampling.LANCZOS)
                    self.tk_icon = ImageTk.PhotoImage(icon_img)
                    self.root.iconphoto(False, self.tk_icon)
                    
                    header_img = pil_img.resize((56, 56), Image.Resampling.LANCZOS)
                    self.logo_image = ImageTk.PhotoImage(header_img)
                except Exception as e:
                    print(f"Failed to load logo: {e}")

        self._build_gui()

    def _build_gui(self):
        # Header Section with Optional Logo
        header_frame = ttk.Frame(self.root)
        header_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=(15, 5), sticky="w")
        
        if self.logo_image:
            logo_label = ttk.Label(header_frame, image=self.logo_image)
            logo_label.pack(side="left", padx=(0, 12))
        
        header_text = ttk.Label(header_frame, text=APP_TITLE, style='Header.TLabel')
        header_text.pack(side="left", fill="y")
        
        # Description Section
        desc_text = "This utility splits standard QuickBooks paystub PDF files into individual files per employee."
        desc_label = ttk.Label(self.root, text=desc_text, style='Desc.TLabel', wraplength=590, justify="left")
        desc_label.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 15), sticky="w")
        
        # Input File Section
        ttk.Label(self.root, text="Input PDF File:").grid(row=2, column=0, padx=20, pady=8, sticky="e")
        ttk.Entry(self.root, textvariable=self.input_pdf, width=40, font=("Segoe UI", 11)).grid(row=2, column=1, padx=8, pady=8, sticky="ew")
        ttk.Button(self.root, text="Browse...", command=self.browse_input).grid(row=2, column=2, padx=20, pady=8)
        
        # Output Directory Section
        ttk.Label(self.root, text="Output Folder:").grid(row=3, column=0, padx=20, pady=8, sticky="e")
        ttk.Entry(self.root, textvariable=self.output_dir, width=40, font=("Segoe UI", 11)).grid(row=3, column=1, padx=8, pady=8, sticky="ew")
        ttk.Button(self.root, text="Browse...", command=self.browse_output).grid(row=3, column=2, padx=20, pady=8)
        
        # Progress Bar & Status
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, padx=20, pady=15, sticky="ew")
        
        status_label = ttk.Label(self.root, textvariable=self.status_text, style='Status.TLabel')
        status_label.grid(row=5, column=0, columnspan=3, padx=20, pady=0)
        
        # Action Button
        self.start_btn = ttk.Button(self.root, text="Start Splitting", style='ActionButton.TButton', command=self.start_processing_thread)
        self.start_btn.grid(row=6, column=0, columnspan=3, pady=(15, 5))

        # Bottom Right Credit Link (flushed to the absolute bottom-right corner)
        credit_label = ttk.Label(self.root, text="By Jon Hassall", style='Credit.TLabel', cursor="hand2")
        credit_label.grid(row=7, column=0, columnspan=3, padx=10, pady=8, sticky="se")
        credit_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/jonhassall"))

    def browse_input(self):
        file_path = filedialog.askopenfilename(
            title="Select Payroll Master PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.input_pdf.set(file_path)
            # Default output folder to same directory as source PDF if not set
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(file_path))

    def browse_output(self):
        folder_path = filedialog.askdirectory(title="Select Destination Directory")
        if folder_path:
            self.output_dir.set(folder_path)

    def start_processing_thread(self):
        # Validate inputs
        if not self.input_pdf.get() or not os.path.exists(self.input_pdf.get()):
            messagebox.showwarning("Missing Input", "Please select a valid input PDF file.")
            return
            
        if not self.output_dir.get() or not os.path.exists(self.output_dir.get()):
            messagebox.showwarning("Missing Destination", "Please select a valid output folder.")
            return
            
        # Disable button during execution
        self.start_btn.config(state="disabled")
        
        # Run worker thread so the GUI remains responsive
        threading.Thread(target=self.process_pdf, daemon=True).start()

    def process_pdf(self):
        pdf_path = self.input_pdf.get()
        out_dir = self.output_dir.get()
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            self.progress["maximum"] = total_pages
            self.progress["value"] = 0
            
            success_count = 0
            fallback_count = 0
            
            for i in range(total_pages):
                page = doc[i]
                text = page.get_text("text")
                
                # Extract Pay Date
                date_match = re.search(r'Pay Date:\s*(\d{2}/\d{2}/\d{4})', text, re.IGNORECASE)
                if not date_match:
                    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
                clean_date = date_match.group(1).strip().replace('/', '-') if date_match else None

                # Extract Employee Name
                clean_name = None
                
                # Strategy 1: Look for "Employee" line followed by name up to comma
                emp_match = re.search(r'Employee\s*\n\s*([^,\n\r]+?)\s*,', text, re.IGNORECASE)
                if emp_match and emp_match.group(1).strip():
                    cand = emp_match.group(1).strip()
                    if cand.lower() not in ('pay period', 'pay date', 'check number', 'ssn'):
                        clean_name = cand

                # Strategy 2: Look for "Employee:" line followed by name
                if not clean_name:
                    emp_match2 = re.search(r'Employee:?\s*\n?\s*([A-Za-z\s\'-]+?)(?:,|\n|\r|$)', text, re.IGNORECASE)
                    if emp_match2 and emp_match2.group(1).strip():
                        cand = emp_match2.group(1).strip()
                        if cand.lower() not in ('pay period', 'pay date', 'check number', 'ssn'):
                            clean_name = cand
                
                # Strategy 3: Check number block followed by lines up to comma
                if not clean_name:
                    name_match = re.search(r'Check number:\s*[\w\d]+\s*\n([^,]+),', text, re.IGNORECASE)
                    if name_match:
                        raw_block = name_match.group(1)
                        lines = [l.strip() for l in raw_block.splitlines() if l.strip()]
                        lines = [l for l in lines if not re.match(r'^(pay period|pay date|check|employee|ssn)', l, re.IGNORECASE)]
                        if lines:
                            clean_name = lines[-1]
                
                # Strategy 4: Name pattern before comma
                if not clean_name:
                    comma_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*,', text)
                    if comma_match:
                        clean_name = comma_match.group(1).strip()

                if clean_name and clean_date:
                    safe_name = sanitize_filename(clean_name)
                    safe_date = sanitize_filename(clean_date)
                    base_filename = f"Pay_Stub_{safe_date}_{safe_name}.pdf"
                    success_count += 1
                else:
                    base_filename = f"ManualReview_Page_{i + 1}.pdf"
                    fallback_count += 1
                
                # Ensure base_filename is sanitized against any remaining bad path chars
                base_filename = sanitize_filename(base_filename, default=f"ManualReview_Page_{i + 1}.pdf")
                if not base_filename.lower().endswith(".pdf"):
                    base_filename += ".pdf"

                # Prevent overwriting if duplicate names/dates exist in the same batch
                output_path = os.path.join(out_dir, base_filename)
                counter = 1
                while os.path.exists(output_path):
                    name_part, ext = os.path.splitext(base_filename)
                    output_path = os.path.join(out_dir, f"{name_part}_({counter}){ext}")
                    counter += 1
                
                # Save individual page
                out_pdf = fitz.open()
                out_pdf.insert_pdf(doc, from_page=i, to_page=i)
                out_pdf.save(output_path)
                out_pdf.close()
                
                # Update progress
                self.progress["value"] = i + 1
                self.status_text.set(f"Processing page {i + 1} of {total_pages}...")
                self.root.update_idletasks()
            
            doc.close()
            self.status_text.set("Completed successfully!")
            messagebox.showinfo(
                "Process Complete", 
                f"Successfully split {total_pages} pages into '{out_dir}'.\n\n"
                f"• Clean extraction: {success_count}\n"
                f"• Flagged for review: {fallback_count}"
            )
            
        except Exception as e:
            self.status_text.set("An error occurred.")
            messagebox.showerror("Error", f"Failed to process PDF:\n{str(e)}")
            
        finally:
            self.start_btn.config(state="normal")
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = PaystubSplitterApp(root)
    root.mainloop()