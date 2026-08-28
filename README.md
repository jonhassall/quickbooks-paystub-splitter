# QuickBooks Paystub Splitter (v1.0.0)

This utility splits standard QuickBooks paystub PDF files into individual files per employee.

## 🚀 Downloads & Releases

Pre-compiled standalone Windows executables (`Paystub Splitter.exe`) are built automatically via GitHub Actions:

- **[Latest Release & Downloads](https://github.com/jonhassall/quickbooks-paystub-splitter/releases)**

No installation or Python runtime is required—simply download and run `Paystub Splitter.exe`.

---

## 🌿 Branching Strategy

- **`main`**: Default production branch. Contains stable, tagged release code.
- **`dev`**: Primary development branch. Active development, new features, and bug fixes occur here or in topic branches off `dev`.

---

## 🛠️ Local Development & Building

To build the executable locally from source code, you will need Python 3.10+ and `pip`.

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
