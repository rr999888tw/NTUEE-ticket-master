# NTUEE-ticket-master

1. `git clone https://github.com/rr999888tw/NTUEE-ticket-master`
2. `cd NTUEE-ticket-master && pip3 install -r requirements.txt` (or pip)
3. open `eric_wu/recreation_checker.py`
  - update `USERNAME` and `PASSWORD`.
  - randomly choose `TIME_BLOCK` to one of the following (default to `7:00 AM - 8:00 AM`)
    ```python
    # TIME_BLOCK = "7:00 AM - 8:00 AM"`
    # TIME_BLOCK = "8:00 AM - 9:00 AM"
    # TIME_BLOCK = "9:00 AM - 10:00 AM"
    # TIME_BLOCK = "10:00 AM - 11:00 AM"
    ```
4. show author the output of your `git diff` (through messenger) and get confirmation from Jackson, Kuan-Yu, or Eric Wu
5. Make sure you have `python3 --version`. Otherwise, you need to replace `python3` with `python` in `spawn-multi-windows.sh`.
6. Run the script a few minutes before 7:00 am PT.
  - `cd NTUEE-ticket-master && run ./spawn-multi-windows.sh`