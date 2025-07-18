
import sys
import os
import time
import pandas as pd
import ta
import ta.momentum
import ta.trend
import datetime

# ----------------------------------------------------------------------
pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]
# ----------------------------------------------------------------------
if len(sys.argv) > 1:
    date = sys.argv[1]
else:
    date = datetime.datetime.today().strftime('%Y-%m-%d')
# ----------------------------------------------------------------------
start_time = time.time()
# ----------------------------------------------------------------------
ls = []

# pkl_file = pkl_files[0]

# pkl_file = 'HOOD-1d.pkl'

for pkl_file in pkl_files:
    
    file_path = os.path.join('pkl', pkl_file)

    df = pd.read_pickle(file_path)

    df = df.tail(10)

    # df['Close'].shift(1)

    df['Close_1'] = df['Close'].shift(1)

    df['change_pct'] = (df['Close'] - df['Close_1']) / df['Close_1'] * 100

    df['change_pct'] = df['change_pct'].round(2)

    symbol = pkl_file.replace('-1d.pkl', '')

    change_pct = df.iloc[-1]['change_pct']

    ls.append({'symbol': symbol, 'change_pct': change_pct})

    print(f'{symbol:10} {change_pct:10}')
# ----------------------------------------------------------------------

tmp = pd.DataFrame(ls)

tmp.sort_values(by='change_pct', ascending=False)

# ----------------------------------------------------------------------

df_info = pd.read_pickle('all_stocks_info.pkl')

df_info['marketCap_billions'] = df_info['marketCap'] / 1_000_000_000

df_info['marketCap_billions'] = df_info['marketCap_billions'].round(2)

df_type = df_info[['symbol', 'quoteType', 'sector', 'industry', 'marketCap_billions']]

tbl = pd.merge(left=tmp, right=df_type, on='symbol')

# tbl.sort_values(by='change_pct', ascending=False)

tbl.sort_values(by='change_pct', ascending=False).query('marketCap_billions > 200')

result = tbl.sort_values(by='change_pct', ascending=False).query('marketCap_billions > 1')

print(result.head(50))

print(result.tail(50))

# tbl.query('marketCap_billions > 0.1').sort

# elapsed_time = time.time() - start_time

# print(f'Processed files: {len(pkl_files)}')

# print(f'Items found: {len(ls)}')

# print(f'Elapsed time: {elapsed_time:.2f} seconds.')
# # ----------------------------------------------------------------------
# analysis.utils.write_list_to_file(ls, output_dir='out', file=f'golden_cross_50_200_{date}.txt')
# # ----------------------------------------------------------------------
# for item in ls:
#     item = item.replace('-1d.pkl', '')
#     item = f'${item}'
#     print(item)