
### Use thetadata to download all actively traded symbols

    python -m get_symbols_thetadata

You'll need a thetadata 'stock standard' account to run the above.

However, this repository comes with a `symbols.txt` file to get you started.

### Download 1D candles from yfinance for all symbosl in `symbols.txt`

    python -m yfinance_all_stocks

### Dependencies

https://github.com/dharmatech/yfinance_download.py
