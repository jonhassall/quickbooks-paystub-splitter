# QuickBooks Paystub Splitter (v1.0.0)

QuickBooks Paystub Splitter is a simple Windows application designed for QuickBooks users and payroll managers. When QuickBooks generates a payroll batch, it exports all employee paystubs into a single multi-page PDF document. 

This tool automatically processes that master PDF file, extracts each employee's name and pay date, and splits the document into separate PDF files for each individual employee (named in the format `Pay_Stub_MM-DD-YYYY_Employee_Name.pdf`). This makes it easy to email or print individual paystubs without needing PDF editing software.

## Downloads & Releases

You do not need Python or technical experience to use this app. Pre-compiled Windows executables (`Paystub Splitter.exe`) are available for download:

- **[Download Latest Release](https://github.com/jonhassall/quickbooks-paystub-splitter/releases)**

Simply download `Paystub Splitter.exe` and double-click to run it on any Windows computer.

---

## Local Development & Building

To build the executable locally from source code, Python 3.10+ and `pip` are required.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jonhassall/quickbooks-paystub-splitter.git
   cd quickbooks-paystub-splitter
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   pip install pyinstaller
   ```

4. **Build the standalone executable:**
   ```powershell
   pyinstaller --clean "Paystub Splitter.spec"
   ```
   The generated executable will be placed in `dist/Paystub Splitter.exe`.

---

## Branching Strategy

- **`main`**: Default production branch. Contains stable, tagged release code.
- **`dev`**: Primary development branch. Active development, new features, and bug fixes occur here or in topic branches off `dev`.
