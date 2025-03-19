import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')

class GPT_Validator:
    client = OpenAI(
    api_key=API_KEY, # ваш ключ в VseGPT после регистрации
    base_url=API_HOST,)

    def gpt_validation(self, init_prompt: str, dialogue: str):
        prompt = init_prompt.format(str(dialogue))

        messages = []
        messages.append({"role": "user", "content": prompt})

        response_big = self.client.chat.completions.create(
            model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр openai/gpt-4o-mini
            messages=messages,
            temperature=0.7,
            n=1,
            max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
            extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
        )

        #print("Response BIG:",response_big)
        return response_big.choices[0].message.content

    def __call__(self, p:str, d: str):
        return self.gpt_validation(p, d)

