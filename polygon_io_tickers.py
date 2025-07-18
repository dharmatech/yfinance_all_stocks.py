
import os
import time
import pprint
import requests
import pandas as pd

api_key = os.getenv('POLYGON_IO_API_KEY')

url = 'https://api.polygon.io/v3/reference/tickers'

params = {
    'market' : 'stocks',
    'limit'  : 1000,
    'sort'   : 'ticker',
    'apiKey' : api_key
}

responses = []
tbl = []

response = requests.get(url, params=params)

data = response.json()

responses.append(data)

tbl = tbl + data['results']

time.sleep(20)

while True:

    if 'next_url' not in data:
        print('next_url is None')
        pprint.pprint(data, depth=1)
        break

    uri = data['next_url']

    print(f'next_uri: {uri}')

    uri = f'{uri}&apiKey={api_key}'

    response = requests.get(uri)

    response.raise_for_status()

    data = response.json()

    pprint.pprint(data, depth=1)

    responses.append(data)
    
    tbl = tbl + data['results']

    print(f'{len(responses)=} {len(tbl)=}')
    
    time.sleep(20)

# len(tbl)

df = pd.DataFrame(tbl)

df.to_pickle('polygon_io_tickers.pkl')

# write df to csv

df.to_csv('polygon_io_tickers.csv', index=False)



# read dataframe from pkl file

# df = pd.read_pickle('polygon_io_tickers.pkl')

# df = pd.read_pickle('polygon_io_tickers.pkl')

# df

with open('symbols-polygon-io.txt', 'w') as f:
    for ticker in df['ticker']:
        f.write(f'{ticker}\n')

# ----------------------------------------------------------------------

# data

# import pprint

# pprint.pprint(data, depth=1)

# data['results']

# pprint.pprint(data['results'], depth=2)

# pprint.pprint(data['results'], depth=2)

# type(data['results'])

# pprint.pprint(data['results'][:5], depth=2)



# pprint.pprint(data, depth=1)

# import pandas as pd

# # df = pd.DataFrame(data['results'])

# pd.DataFrame(data)

# pd.DataFrame(data['results'])