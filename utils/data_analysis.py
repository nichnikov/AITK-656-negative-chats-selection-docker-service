import os
import pandas as pd


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
not_tested_files = ["chats_2025week11_not_tested_2.feather", 
                    "chats_2025week11_not_tested.feather", 
                    "chats_2025week11.feather", "tested_results_250331.feather"]

for fn in not_tested_files:
    data_pth =os.path.join(project_root, "data", "2025w11_data", fn)
    df = pd.read_feather(data_pth)
    print(len(df["chat_id"].unique()))


res_data_pth = os.path.join(project_root, "data", "2025w11_data", "tested_results_250331.feather")
tested_results_df = pd.read_feather(res_data_pth)
not_res_data_pth = os.path.join(project_root, "data", "2025w11_data", "chats_2025week11_not_tested_2.feather")
not_tested_df = pd.read_feather(not_res_data_pth)
print(tested_results_df.drop_duplicates())
print(len(list(not_tested_df["chat_id"].unique())))
print(len(list(tested_results_df.drop_duplicates()["chat_id"])))


all_data_path = res_data_pth = os.path.join(project_root, "data", "2025w11_data", "chats_2025week11.feather")
all_data_df = pd.read_feather(all_data_path)
print(len(list(all_data_df["chat_id"].unique())))

chats_ids = list(not_tested_df["chat_id"].unique()) + list(tested_results_df["chat_id"].unique())
print(all_data_df[~all_data_df["chat_id"].isin(chats_ids)])



'''
data_pth =os.path.join(project_root, "data", "2025w11_data", "chats_2025week11.feather")
data_df = pd.read_feather(data_pth)


results_pth =os.path.join(project_root, "data")
results_df = pd.read_feather(os.path.join(results_pth, "tested_results_250331.feather"))

print(len(data_df["chat_id"].unique()))
print(len(results_df["chat_id"].unique()))
'''
