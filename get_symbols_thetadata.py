
import requests
import io
import pandas as pd

# ----------------------------------------------------------------------
def thetadata_active_stocks():
    url = 'http://127.0.0.1:25510/v2/bulk_snapshot/stock/quote'

    headers = {"Accept": "application/json"}
    
    params = { "root": 0, "use_csv": "true" }
    
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return None

    df = pd.read_csv(io.BytesIO(response.content), keep_default_na=False)

    return df['root'].to_list()
# ----------------------------------------------------------------------
roots_stock = thetadata_active_stocks()

roots_stock.sort()
# ----------------------------------------------------------------------
with open('symbols.txt', 'w') as f:
    for symbol in roots_stock:
        f.write(symbol + '\n')

