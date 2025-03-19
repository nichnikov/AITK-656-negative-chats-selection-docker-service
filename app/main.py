import os
import sys
import logging
from openai import RateLimitError
import pandas as pd

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Получение пути текущего файла и корня проекта
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

# Импорт необходимых модулей
from utils.utils import chunks
from app.dependencies import validator, data_processor

def dialogue_validate(chat_dict: list[dict]):
    """
    Проверяет диалог, формируя строку из авторов и фраз, 
    а также валидируя его с помощью внешнего валидатора.

    :param chat_dict: Список словарей, содержащих информацию о диалоге.
    :return: Кортеж из строки диалога и результата валидации.
    """
    
    dialogue = "\n\t".join([str(d["Autor"]) + ": " + str(d["Phrase"]) for d in chat_dict])
    logging.debug(f"Сформированный диалог: {dialogue}")
    try:    
        is_valid = validator(dialogue)
        logging.info(f"Результат валидации для диалога: {is_valid}")
    except RateLimitError:
        logging.error(f"Результат валидации для диалога: {is_valid}")
        is_valid = "Rate-limit error"

    return dialogue, is_valid

def pipline(save_step: int):
    """
    Основной процесс обработки данных, который разбивает чаты на чанки и 
    валидирует их, сохраняя результаты в Excel.

    :param save_step: Количество чатов в одном чанкe для обработки.
    """
    
    logging.info("Запуск обработки данных...")
    
    # Инициализация процессора данных
    data_processor.pipline()
    
    keys = data_processor.dict_of_chats.keys()
    keys_chanks = chunks(list(keys), save_step)

    for num, keys_chank in enumerate(keys_chanks):

        chank_results = []

        for i in keys_chank:
            dialogue, val = dialogue_validate(data_processor.dict_of_chats[i])
            chank_results.append({"chat_id": i, 
                                  "dialogue": dialogue,
                                  "gpt_val": val})

        out_fn = "ai_validate" + str(num) + ".xlsx"
        chank_results_df = pd.DataFrame(chank_results)

        # Сохранение результатов в Excel файл
        output_path = os.path.join("data", "results", out_fn)
        chank_results_df.to_excel(output_path, index=False)
        logging.info(f"Результаты сохранены в файл: {output_path}")

    logging.info("Обработка данных завершена.")

if __name__ == "__main__":
    pipline(10)