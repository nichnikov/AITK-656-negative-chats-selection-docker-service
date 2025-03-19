import os
import sys
import json
from pydantic_core import from_json

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from core.data_definition import Settings, Parameters
from services.validator import GPT_Validator
from services.data_processor import ChatDataProcessor


with open(os.path.join("data", "parameters.json"), "r") as pf:
    prmt_json = json.load(pf)


settings = Settings()
parameters = Parameters(**prmt_json)

data_processor = ChatDataProcessor(os.path.join("data", parameters.data_file_name))
validator = GPT_Validator(settings, parameters)


if __name__ == "__main__":
    print(parameters.prompt)
    data_processor.pipline()
    k = 1
    for i in data_processor.dict_of_chats:
        dialogue = "\n\t".join([str(d["Autor"]) + ": " + str(d["Phrase"]) for d in data_processor.dict_of_chats[i]])
        val = validator(dialogue)
        print(dialogue)
        print(val)
        if k > 10:
            break
        k += 1