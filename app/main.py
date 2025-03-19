import os
import sys
import pandas as pd

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from app.dependencies import validator, data_processor

def pipline():
    data_processor()
    results = []
    for i in data_processor.dict_of_chats:
            dialogue = "\n\t".join([str(d["Autor"]) + ": " + str(d["Phrase"]) for d in data_processor.dict_of_chats[i]])
            val = validator(dialogue)
            results.append({"chat_id": i, 
                            "dialogue": dialogue,
                            "gpt_val": val})
    return pd.DataFrame(results)