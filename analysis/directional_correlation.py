
import os
import time
import datetime
import pandas as pd

import argparse

# ----------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--symbol', type=str)

args = parser.parse_args()

symbol = args.symbol
# ----------------------------------------------------------------------
# symbol = 'TSLA'

pkl_file = f'{symbol}-1d.pkl'

file_path = os.path.join('pkl', pkl_file)

df = pd.read_pickle(file_path)

df['color'] = 'equal'

df.loc[df['Close'] > df['Open'], 'color'] = 'green'
df.loc[df['Close'] < df['Open'], 'color'] = 'red'

# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
start_time = time.time()
# ----------------------------------------------------------------------
ls = []

# pkl_file = pkl_files[0]

# pkl_file = 'FER-1d.pkl'

# pkl_file = 'FERG-1d.pkl'

for pkl_file in pkl_files:
        
    file_path = os.path.join('pkl', pkl_file)

    df_other = pd.read_pickle(file_path)

    df_other['color'] = 'equal'

    df_other.loc[df_other['Close'] > df_other['Open'], 'color'] = 'green'
    df_other.loc[df_other['Close'] < df_other['Open'], 'color'] = 'red'
    
    df_other = df_other[df_other['color'] != 'equal']
    
    tmp = pd.merge(df['color'], df_other['color'], left_index=True, right_index=True)
    
    tmp['equal'] = tmp['color_x'] == tmp['color_y']
    
    equal_percent = tmp['equal'].sum() / len(tmp) * 100

    tmp_len = len(tmp)

    entry = {
        'pkl_file': pkl_file,
        'equal_percent': equal_percent,
        'tmp_len': tmp_len
    }
        
    ls.append(entry)
        
    print(f'{pkl_file.ljust(20)} : {equal_percent:10.2f}% : len: {tmp_len:10d}')
# ----------------------------------------------------------------------
df_info = pd.read_pickle('all_stocks_info.pkl')

df_info['marketCap_billions'] = df_info['marketCap'] / 1_000_000_000

df_info['marketCap_billions'] = df_info['marketCap_billions'].round(2)

df_type = df_info[['symbol', 'quoteType', 'sector', 'industry', 'marketCap_billions']]

tbl = pd.DataFrame(ls)

tbl['equal_percent'] = tbl['equal_percent'].round(2)

tbl['symbol'] = tbl['pkl_file'].str.split('-').str[0]

tbl = pd.merge(tbl, df_type, left_on='symbol', right_on='symbol')

result = tbl.query('tmp_len > 250').query('quoteType == "EQUITY"').sort_values('equal_percent', ascending=False)

print(result.query('marketCap_billions > 0.1').head(50))

print(result.query('marketCap_billions > 0.1').tail(50))

# ----------------------------------------------------------------------
date = datetime.datetime.today().strftime('%Y-%m-%d')

filename = f'out/directional_correlation_{symbol}_{date}.txt'

os.makedirs(os.path.dirname(filename), exist_ok=True)

with open(filename, 'w') as f:

    f.write(result.query('marketCap_billions > 0.1').head(50).to_string(index=False))
    f.write('\n')
    f.write('\n')
    f.write(result.query('marketCap_billions > 0.1').tail(50).to_string(index=False))
