"""
На вход подается уже готовый список чатов в формате:
chat_id | dialogue
"""


import os
import sys
import logging
from openai import RateLimitError, APIConnectionError
import pandas as pd

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Получение пути текущего файла и корня проекта
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

# Импорт необходимых модулей
from utils.utils import chunks
from app.dependencies import validator, data_processor, parameters


data_df = pd.read_csv(os.path.join(project_root, "data", "tested_chats_for_new_prompt.csv"), sep="\t")
data_dicts = data_df.to_dict(orient="records")


for num, d in enumerate(data_dicts):
    print(num, "/", len(data_dicts))
    try:    
        is_valid = validator(d["dialogue"])
        logging.info(f"Результат валидации для диалога: {is_valid}")
    except RateLimitError:
        logging.error(f"Результат валидации для диалога Rate-limit error")
        is_valid = "Rate-limit error"
    d["gpt_val"] = is_valid

results_df = pd.DataFrame(data_dicts)
print(results_df)
results_df.to_excel(os.path.join("data", "results", "new_prompts_test_chats_validated.xlsx"), index=False)