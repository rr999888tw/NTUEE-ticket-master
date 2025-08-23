# NTUEE-ticket-master

## Quick Start 

1. Clone the repository:
   ```sh
   git clone https://github.com/rr999888tw/NTUEE-ticket-master
   ```
2. Install dependencies:
   ```sh
   cd NTUEE-ticket-master
   pip3 install -r requirements.txt
   # Or use pip if python3 is not available
   ```
3. Open and edit credentials:
   - Edit `eric_wu/credentials.py` to set your `USERNAME` and `PASSWORD`.
   - In `eric_wu/recreation_checker.py`, set `TIME_BLOCK` to one of the following (default: `7:00 AM - 8:00 AM`):
     ```python
     TIME_BLOCK = "7:00 AM - 8:00 AM"
     TIME_BLOCK = "8:00 AM - 9:00 AM"
     TIME_BLOCK = "9:00 AM - 10:00 AM"
     TIME_BLOCK = "10:00 AM - 11:00 AM"
     ```
4. After making code changes, run:
   ```sh
   git diff > patch
   ```
   - Share the patch file with Jackson, Kuan-Yu, or Eric Wu for confirmation.
5. Ensure you have Python 3 installed:
   ```sh
   python3 --version
   ```
   - If not, update `spawn-multi-windows.sh` to use `python` instead of `python3`.
6. Run the script a few minutes before 7:00 am PT:
   ```sh
   cd NTUEE-ticket-master
   ./spawn-multi-windows.sh
   ```

---
**Note:**
- Use a code editor (VS Code, PyCharm, etc.) for editing and reviewing code.
- Always confirm changes with the project authors before deploying.