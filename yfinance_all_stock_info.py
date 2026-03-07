
import os
import time
import pandas as pd
import yfinance as yf

INITIAL_RATE_LIMIT_WAIT_SECONDS = 30
RATE_LIMIT_BACKOFF_FACTOR = 2
MAX_RATE_LIMIT_WAIT_SECONDS = 15 * 60


def format_duration(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f'{hours}h {minutes}m {seconds}s'
    if minutes:
        return f'{minutes}m {seconds}s'
    return f'{seconds}s'


def is_rate_limited_error(exception):
    message = str(exception).lower()
    rate_limit_indicators = (
        'too many requests',
        'rate limited',
        'rate limit',
        '429',
    )
    return any(indicator in message for indicator in rate_limit_indicators)


def get_ticker_info_with_retry(symbol):
    wait_seconds = INITIAL_RATE_LIMIT_WAIT_SECONDS
    retry_count = 0

    while True:
        ticker = yf.Ticker(symbol)

        try:
            ticker_info = ticker.info
            if retry_count:
                print(f'Retry succeeded for {symbol} after {retry_count} pause(s). Resuming downloads.')
            return ticker_info
        except Exception as exception:
            if not is_rate_limited_error(exception):
                raise

            if retry_count == 0:
                print(
                    f'Rate limited while downloading {symbol}. '
                    f'Pausing for {format_duration(wait_seconds)} before retrying.'
                )
            else:
                next_wait_seconds = min(
                    wait_seconds * RATE_LIMIT_BACKOFF_FACTOR,
                    MAX_RATE_LIMIT_WAIT_SECONDS,
                )

                if next_wait_seconds > wait_seconds:
                    print(
                        f'Rate limited again for {symbol}. '
                        f'Increasing pause from {format_duration(wait_seconds)} '
                        f'to {format_duration(next_wait_seconds)}.'
                    )
                    wait_seconds = next_wait_seconds
                else:
                    print(
                        f'Rate limited again for {symbol}. '
                        f'Waiting {format_duration(wait_seconds)} before retrying.'
                    )

            print(f'Retrying {symbol} after the pause.')
            time.sleep(wait_seconds)
            retry_count += 1
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]

# pkl_file = pkl_files[0]

start_time = time.time()
# ----------------------------------------------------------------------
ls = []

i = 0

for pkl_file in pkl_files:

    symbol = pkl_file.split('-')[0]
    # ----------------------------------------------------------------------
    elapsed_time = time.time() - start_time

    time_per_item = elapsed_time / (i+1)
    
    estimated_total_time = time_per_item * len(pkl_files)

    estimated_time_remaining = estimated_total_time - elapsed_time
    # ----------------------------------------------------------------------
    print(f'Downloading {symbol.ljust(10)} [{i+1}/{len(pkl_files)}] - Elapsed time: {elapsed_time / 60:.2f} minutes. Estimated total time: {estimated_total_time / 60 :.2f} minutes. Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes.')
    
    # print(f'yf.Ticker {symbol}')
    
    try:
        ticker_info = get_ticker_info_with_retry(symbol)

        # ticker_info['symbol'] = symbol
        
        # ls.append(ticker.info)
        ls.append(ticker_info)
    except Exception as e:
        # print(f'Error: {e}')
        # ls.append({ 'error': str(e) })
        print(f'Error getting info for {symbol}. Exception: {e}')

    i += 1

    # if i >= 10:
    #     break

df = pd.DataFrame(ls)

df.to_pickle('all_stocks_info.pkl')
# ----------------------------------------------------------------------
#
# Examples.

# load dataframe from pickle file 'all_stocks_info.pkl'

# df = pd.read_pickle('all_stocks_info.pkl')


# print(df.iloc[0].to_string())
# This doesn't print all the properties.



# for column in df.columns:
#     print(f'{column}: {df[column].iloc[0]}')
#
# This does.



# for column in sorted(df.columns):
#     print(f'{column}: {df[column].iloc[0]}')
#
# This does also, but sorted.





# print(df.iloc[0][sorted(df.columns)].to_string())

# print(df[df['symbol'] == 'AAPL'].iloc[0].to_string())

# print(df[df['symbol'] == 'AAPL'].iloc[0][sorted(df.columns)].to_string())

# print(sorted(df.columns))

# len(df.columns)

# df[df['symbol'] == 'AAPL'].iloc[0].to_csv('c:/temp/info.csv', index=True)

# df.to_csv('c:/temp/all_stocks_info.csv', index=True)


# df['symbol'].iloc[0]

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)

# 10

# df['longBusinessSummary']

# rows where 'longBusinessSummary' contains 'Apple'

# df[df['longBusinessSummary'].str.contains('Apple', na=False)]

# print(df.iloc[19].to_string())

     
# ----------------------------------------------------------------------
