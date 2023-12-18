from pathlib import Path
from llama_index import download_loader
import os
import sys
import json
import random

def find_files_with_extension(directory, extension):
    file_paths = []  # ファイルのパスを保存するリスト
    # ディレクトリ内を再帰的に探索
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_paths.append(os.path.join(root, file))

    return file_paths

if __name__ == "__main__":
    results_path = "shaji_contents.json"
    DocxReader = download_loader("DocxReader")

    loader = DocxReader()
    directory_path = './papers_docx'  
    extension = '.docx'
    paths = find_files_with_extension(directory_path, extension)
    random.shuffle(paths)
    shajis = []
    for path in paths:
        documents = loader.load_data(file=Path(path))
        
        texts = documents[0].text.split("\n\n")
        texts = [item for item in texts if item.strip()]
        target = "謝辞"
        target_indexs = [index for index, value in enumerate(texts) if target == ''.join(value.split())]

        # 謝辞がない時はconinueする
        if target_indexs == []:
            continue

        # 複数できた場合は最後の要素と判定する
        target_index = target_indexs[-1]

        shaji_content = ""
        stop_words = ["参考文献","付録","出典","引用","参考URL"]
        for text in texts[target_index :]:
            if any(word in text for word in stop_words):
                break
            else:
                text = ''.join(text.split())
                shaji_content += text + "\n"
        shaji_content = shaji_content[:-2]

        shaji_content_json = {"content" : shaji_content, "metadata" : documents[0].metadata}
        shajis.append(shaji_content_json)
    
    with open(results_path, 'x') as json_file:
        json.dump(shajis, json_file,ensure_ascii=False,indent=4)