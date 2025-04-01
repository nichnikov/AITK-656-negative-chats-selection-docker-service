import os
import pandas as pd

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
data_pth =os.path.join(project_root, "data", "results")


data_xlsx_df = pd.read_excel(os.path.join(data_pth, "ai_validated_chats.xlsx"))
print(data_xlsx_df)

data_xlsx_df.to_feather(os.path.join(data_pth, "ai_validated_105.feather"))
