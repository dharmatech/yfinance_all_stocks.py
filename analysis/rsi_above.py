
import os
import time
import pandas as pd
import ta
import pprint

# ----------------------------------------------------------------------
def is_rsi_above(df, date, rsi=70):
    if date not in df.index:
        return False

    return df.loc[date]['rsi'] > rsi

# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
start_time = time.time()

ls = []

for pkl_file in pkl_files:
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)
       
    df['rsi'] = ta.momentum.rsi(close=df['Close'], window=14)

    if is_rsi_above(df, '2024-08-22'):
        ls.append(pkl_file)
        print(f'{pkl_file.ljust(20)} - {df.loc["2024-08-22"]["rsi"]}')

elapsed_time = time.time() - start_time

# pprint.pprint(ls)

pprint.pprint(f'Processed files: {len(pkl_files)}')

pprint.pprint(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------