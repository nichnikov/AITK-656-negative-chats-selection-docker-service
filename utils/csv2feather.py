import os
import pandas as pd


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))



# Предварительная подготовка
in_pth = os.path.join(project_root, "data", "2025w12_data")
df = pd.read_csv(os.path.join(in_pth, "chats_2025week12.csv"))
print(df)
print(df.info())

work_columns = ["id", "chat_id", "created", "text", "discriminator", "operator_id", "user_id", "evaluation", 
 "c_ts_ms", "u_ts_ms", "search_vector", "template_id", "algorithm", "etalon_text", "score"]

df[work_columns].to_feather(os.path.join(in_pth, "chats_2025week12.feather"))


'''
out_pth = ""
data_xlsx_df = pd.read_excel(os.path.join(out_pth, "ai_validated_chats.xlsx"))
print(data_xlsx_df)

data_xlsx_df.to_feather(os.path.join(out_pth, "ai_validated_105.feather"))
'''