import json
from openai import OpenAI
import os
import random

client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"]
)

if __name__ == "__main__":

    user_text = ""

    result_path = "shaji_contents.json"
    with open(result_path , 'r') as json_file:
        loaded_arrays = json.load(json_file)
    
    shajis = [item["content"] for item in loaded_arrays]
    print(shajis)
    random.shuffle(shajis)

    system_text = f"""あなたは、卒業論文における謝辞を作成することが非常に得意です。ユーザーの学校の卒業論文の謝辞を次に3個示します。形式や言い回しなどは例示する謝辞に可能な限り近づけて、ユーザーが指定する内容を含むような謝辞を考え出力してください。
{{
・{shajis[0]}

・{shajis[1]}

・{shajis[2]}
}}"""

    print("system_text : ", system_text)

    #model = "gpt-3.5-turbo-1106"
    model = "gpt-4-1106-preview"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text}
        ],
        temperature = 0.3
    )


    result = completion.choices[0].message.content
    print("result : ",result)