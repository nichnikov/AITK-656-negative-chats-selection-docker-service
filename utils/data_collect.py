import os
import re
from glob import glob
from os import walk
import pandas as pd

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))

data_pth =os.path.join(project_root, "data", "2025w13_data", "chats_2025week13.feather")
data_df = pd.read_feather(data_pth)

print(data_df)

pth =os.path.join(project_root, "data",  "results", "2025w13_test_new_prompt")
print("2025w13_results PATH:", pth)

file_names = []
wlk = walk(pth)

print(wlk)
for (dirpath, dirnames, filenames) in walk(pth):
    file_names.extend(filenames)
    break

print(file_names)

file_names_2 = []
for fn in file_names:
    val = re.findall(r".feather", fn)
    if val:
        file_names_2.append(fn)

print(file_names_2)

dfs = []        
for fn in file_names_2:
    f_path = os.path.join(pth, fn)
    df = pd.read_feather(f_path)
    dfs.append(df)

tested_df = pd.concat(dfs, axis=0)
print("tested_df:\n", tested_df)

not_tested_df = data_df[~data_df["chat_id"].isin(tested_df["chat_id"])]
print("not_tested_df:\n", not_tested_df)

# [242913 rows x 15 columns]


pth_out =os.path.join(project_root, "data", "results", "2025w13_test_new_prompt")
tested_df.to_feather(os.path.join(pth_out, "tested_results_250413_test.feather"))
tested_df.to_csv(os.path.join(pth_out, "all_tested_w13_250413_test.csv"), sep="\t", index=False)
print(tested_df.info())

not_tested_df.to_feather(os.path.join(pth_out, "not_tested_250414_1.feather"))
print(not_tested_df.info())
