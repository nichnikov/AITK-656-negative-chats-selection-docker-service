import os
import re
import pandas as pd

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))


data_path = os.path.join(project_root, "data", "2025w11_data")
res_df = pd.read_feather(os.path.join(data_path, "tested_results_250331_4.feather"))


res_dicts = res_df.to_dict(orient="records")

for d in res_dicts:
    d["val"] = False
    neg_sign = re.findall("да", d["gpt_val"].lower())
    if neg_sign:
        d["val"] = True


out_path = os.path.join(project_root, "data", "2025w11_results")
res_df = pd.DataFrame(res_dicts)
print(res_df)

res_df.to_excel(os.path.join(out_path, "tested_results_week11.xlsx"), index=False)
res_neg_df = res_df[res_df["val"] == True]
print(res_neg_df)

res_neg_df.to_excel(os.path.join(out_path, "tested_results_week11_negative.xlsx"), index=False)