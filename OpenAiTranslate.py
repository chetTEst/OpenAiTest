import json
import openai
from bs4 import BeautifulSoup
from os import path
import tiktoken


import os
api_key = os.environ['OPENAI_API_KEY']

with open(path.join('kursSCORM','course.json'), 'r') as f:
    data = json.load(f)

#Объект токенизации для подсчета токенов
encoding = tiktoken.get_encoding("p50k_base")


openai.api_key = api_key

# HTML-текст, который нужно перевести
html_text = data['sections']['module2']['blocks']['uxfKBSpMMc']['html']

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_text, 'html.parser')

# Итерируем по каждому элементу в HTML-тексте
def translate_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text}\n\nTranslate the above text to Russian:",
        temperature=0.5,
        max_tokens=150
    )

    return response.choices[0].text.strip()

def extract_and_translate(tag):
    if tag.name not in ["script", "style"]:
        if tag.string:
            translated_text = translate_text(tag.string)
            print(translated_text)
            tag.string.replace_with(translated_text)
        else:
            for child in tag.children:
                extract_and_translate(child)

for tag in soup.find_all(True):
    extract_and_translate(tag)
# Получаем переведенный HTML-текст
translated_html = str(soup)
print(soup.prettify())

data['sections']['module2']['blocks']['uxfKBSpMMc']['html'] = translated_html

with open(path.join('kursSCORM','course.json'), 'w') as f:
    json.dump(data, f)
