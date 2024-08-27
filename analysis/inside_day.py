
import os
import time
import pandas as pd
import pprint
# ----------------------------------------------------------------------
def is_inside_day(df, date):

    if date not in df.index:
        return False
	
    a = df.loc[:date].iloc[-2]
    b = df.loc[date]

    return b['High'] < a['High'] and b['Low'] > a['Low']
# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
start_time = time.time()

ls = []

for pkl_file in pkl_files:
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)
       
    if is_inside_day(df, '2024-08-22'):
        ls.append(pkl_file)

elapsed_time = time.time() - start_time

pprint.pprint(ls)

pprint.pprint(f'Processed files: {len(pkl_files)}')

pprint.pprint(f'Items found: {len(ls)}')

print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# ----------------------------------------------------------------------