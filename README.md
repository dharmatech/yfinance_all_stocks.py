
### Use thetadata to download all actively traded symbols

    python -m get_symbols_thetadata

You'll need a thetadata 'stock standard' account to run the above.

However, this repository comes with a `symbols.txt` file to get you started.

### Download 1D candles from yfinance for all symbosl in `symbols.txt`

    python -m yfinance_all_stocks

### Run a scan

    python -m analysis.golden_cross_50_200 2024-08-27

![image](https://github.com/user-attachments/assets/a3684f6b-1215-4a16-aede-7447e83b791b)

### Dependencies

https://github.com/dharmatech/yfinance_download.py
