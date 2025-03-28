import os
import re
from glob import glob
from os import walk
import pandas as pd

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))

data_pth =os.path.join(project_root, "data", "chats_2025week11.feather")
data_df = pd.read_feather(data_pth)

print(data_df)

pth =os.path.join(project_root, "data", "results")
print(pth)

file_names = []
wlk = walk(pth)

print(wlk)
for (dirpath, dirnames, filenames) in walk(pth):
    file_names.extend(filenames)
    break

file_names_2 = []
for fn in file_names:
    val = re.findall(r".feather", fn)
    if val:
        file_names_2.append(fn)


dfs = []        
for fn in file_names_2:
    f_path = os.path.join(pth, fn)
    df = pd.read_feather(f_path)
    dfs.append(df)

tested_df = pd.concat(dfs, axis=0)
print(tested_df)

not_tested_df = data_df[~data_df["chat_id"].isin(tested_df["chat_id"])]
print(not_tested_df)

# [242913 rows x 15 columns]

# tested_df.to_feather(os.path.join(pth_out, "tested_results.feather"))
pth_out =os.path.join(project_root, "data")
not_tested_df.to_feather(os.path.join(pth_out, "not_tested.feather"))
print(not_tested_df.info())