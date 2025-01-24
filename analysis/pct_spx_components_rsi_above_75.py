
import os
import pandas as pd
import ta

def pct_spx_rsi_above(val):

    df = pd.read_csv('spx-constituents.csv')

    symbols = df['Symbol'].to_list()

    # --------------------------------------------------

    df_all = pd.DataFrame()

    for symbol in symbols:
        
        path = os.path.join('pkl', f'{symbol}-1d.pkl')

        if not os.path.exists(path):
            continue
        
        df = pd.read_pickle(path)

        df['symbol'] = symbol
        
        df['rsi'] = ta.momentum.rsi(close=df['Close'], window=14)
                
        df = df[['symbol', 'rsi']]

        df_all = pd.concat([df_all, df])
        
    # --------------------------------------------------

    df_pivot = df_all.pivot(columns='symbol', values='rsi')


    df_pivot['count'] = df_pivot.count(axis=1)


    df_pivot['greater_than_75'] = (df_pivot.drop(columns='count') > 75).sum(axis=1)

    df_pivot['pct_greater_than_75'] = df_pivot['greater_than_75'] / df_pivot['count'] * 100

    df = df_pivot[['pct_greater_than_75']].reset_index().rename_axis(None, axis=1)

    return df



