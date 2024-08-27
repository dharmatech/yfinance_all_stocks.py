
import os
import pandas as pd
# ----------------------------------------------------------------------
def write_list_to_file(ls, output_dir='out', file='out.txt'):
    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, file)

    with open(output_file_path, 'w') as f:
        for item in ls:
            f.write("%s\n" % item)

    print(f'List of symbols saved to {output_file_path}')
# ----------------------------------------------------------------------
def scan(pkl_files, date, proc, pred):
    ls = []

    for pkl_file in pkl_files:
        
        file_path = os.path.join('pkl', pkl_file)

        df = pd.read_pickle(file_path)
        
        proc(df)
                
        if pred(df, date):
            ls.append(pkl_file)
            print(pkl_file)

    return ls
# ----------------------------------------------------------------------