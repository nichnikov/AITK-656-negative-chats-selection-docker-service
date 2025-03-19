
import os
import re
import time
import pandas as pd
from openai import OpenAI
from itertools import groupby
from operator import itemgetter
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPT_Validator:
    client = OpenAI(
    api_key="sk-or-vv-17bd53f8f505e0a1d24a3bf0a8bb702e13edbc78c89ac9aa41f6bda7ec72270c", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",)


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


if __name__ == "__main__":

    prompt =  """Ты талантливый и ответственный аналитик в большой компании. Цель твоей работы – читать диалоги между Пользователями и Оператором и анализировать их на негативные факторы. Ниже диалог между Пользователем и Оператором. Прочитай его и ответь на вопросы:

                1. Высказывал ли Пользователь в чате возмущение ответом оператора?
                2. Проявлял ли Пользователь любые негативные эмоции, связанные с качеством ответа, длительностью ожидания и так далее?

                Ответь односложно – да/нет.

                Диалог между Пользователем и Оператором:
                {}
                """

    validator = GPT_Validator()

    fale_names = ["chats_2025week10.feather"]
    for fale_name in fale_names:

        # data_df = pd.read_csv(os.path.join("data", fale_name), sep="\t")
        data_df = pd.read_feather(os.path.join("data", fale_name))
        # print(list(data_df.columns.values))
        for cl in data_df.columns:
            clear_cn = re.sub(r"\s+", "", cl)
            data_df.rename(columns={cl: clear_cn}, inplace=True)
        
        patterns = re.compile(r"\n|\¶|(?P<url>https?://[^\s]+)|<a href=|</a>|/#/document/\d\d/\d+/|\"\s*\">|\s+")

        for col in ["chat_id", "text"]:
            data_df[col] = data_df[col].apply(lambda x: patterns.sub(" ", str(x)))
        
        data_df["discriminator"] = data_df["discriminator"].apply(lambda x: re.sub(r"\s+", "", str(x))) 
        data_df["Autor"] = "Нет"
        
        user_messages = ["UserMessage", "UserNewsPositiveReactionMessage", "UserMobileMessage", "UserFileMessage"]
        operator_messages = ["AutoGoodbyeMessage", "AutoHello2Message",  "AutoHelloMessage", "AutoHelloNewsMessage", "AutoHelloOfflineMessage",
                             "AutoRateMessage", "HotlineNotificationMessage", "MLRoboChatMessage", "NewsAutoMessage", "OperatorMessage"]

        print(data_df["discriminator"].unique())
        data_df["Autor"][data_df["discriminator"].isin(user_messages)] = "Пользователь"
        data_df["Autor"][data_df["discriminator"].isin(operator_messages)] = "Оператор"
        
        data_dics = data_df[["chat_id", "Autor", "text"]].to_dict(orient="records")

        # группировка текстов по чатам:
        data_dics.sort(key=itemgetter('chat_id'))
        dict_of_chats = {int(k): [{"Autor": d["Autor"], "Phrase": d["text"]} for d in list(g)] for k, g in groupby(data_dics, itemgetter("chat_id"))}

        dict_results = []
        k = 1

        t_in = datetime.datetime.now()
        for i in dict_of_chats:
            t_start = datetime.datetime.now()
            try:
                dialogue = "\n\t".join([str(d["Autor"]) + ": " + str(d["Phrase"]) for d in dict_of_chats[i]])

                # print(dialogue)

                if k > 1000000:
                    break
                
                k += 1

                val = validator(prompt, dialogue)
                t_end = datetime.datetime.now()
                # print(fale_name, k, "/", len(dict_of_chats), "\n", "val:", val, "\n\n", "time:", t_end - t_start, "\n\n")
                # logger.info(str(fale_name) + str(k) + "/" + str(len(dict_of_chats)) + "\n" + "val: " + str(val) + "\n\n" + "time: " + str(t_end - t_start) + "\n\n")
                logger.info(" ".join([str(fale_name), str(k), "/", str(len(dict_of_chats)), "\n", "val: ", str(val), "\n\n", "time: ", str(t_end - t_start), "\n\n"]))
                dict_results.append({"chat_id": i, "dialogue": dialogue, "val": val})
            
            except Exception as e:
                pass
            
            out_fn = "ai_analysis2_" + fale_name
            results_df = pd.DataFrame(dict_results)
            results_df.to_feather(os.path.join("results", out_fn))
            # results_df.to_csv(os.path.join("results", out_fn), sep="\t", index=False)
            # time.sleep(1)
        time_interval = datetime.datetime.now() - t_in
        print("working time:", time_interval)
        print("working time for 1 item:", time_interval/30)