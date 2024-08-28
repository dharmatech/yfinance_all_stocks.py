
import os
import time
import pandas as pd

def single_dataframe():

    pkl_files = [file for file in os.listdir('pkl') if file.endswith('.pkl')]

    start_time = time.time()

    i = 0

    dataframes = []

    for pkl_file in pkl_files:

        elapsed_time = time.time() - start_time    

        time_per_iteration = elapsed_time / (i + 1)

        estimated_time_remaining = time_per_iteration * (len(pkl_files) - i)

        if i % 100 == 0:
            print(f'{i}/{len(pkl_files)} Elapsed time: {elapsed_time:.2f} seconds. Estimated time remaining: {estimated_time_remaining:.2f} seconds.')
        
        file_path = os.path.join('pkl', pkl_file)

        df = pd.read_pickle(file_path)

        symbol = pkl_file.replace('-1d.pkl', '')

        df['symbol'] = symbol

        dataframes.append(df)

        i += 1

    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f'Elapsed time: {elapsed_time:.2f} seconds.')

    # ----------------------------------------------------------------------

    combined_df = pd.concat(dataframes)

    return combined_df