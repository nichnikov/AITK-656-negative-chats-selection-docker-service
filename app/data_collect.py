import os
import re
from glob import glob
from os import walk
import pandas as pd

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))


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

df_all = pd.concat(dfs, axis=0)
print(df_all)

pth_out =os.path.join(project_root, "data")
df_all.to_feather(os.path.join(pth_out, "tested_results.feather"))