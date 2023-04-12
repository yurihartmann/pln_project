import json
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
print(stopwords.words('portuguese'))


def int_to_roman(input):
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []

    for i in range(len(ints)):
       count = int(input / ints[i])
       result.append(nums[i] * count)
       input -= ints[i] * count
    return ''.join(result).lower()


stopwords_custom = stopwords.words('portuguese')
stopwords_custom += ['-', '/', ',', '.', '(', ')', ';', 'º', '`', "``", "''", "'", ":", "¿"]
stopwords_custom += [int_to_roman(i) for i in range(1, 100)]


def clear_number(text: str) -> str:
    return ''.join(
        char for char in text if not char.isdigit()
    )


FILE = "history_data/1/all.json"
projects_dict: dict

with open(FILE) as file:
    projects_dict = json.load(file)

for project in projects_dict:
    titulo = clear_number(project['titulo']).lower()
    titulo_tokens = nltk.word_tokenize(titulo)
    titulo_tokens_clear = [word for word in titulo_tokens if not word in stopwords_custom]
    project['titulo'] = titulo_tokens_clear

    resumo = clear_number(project['resumo']).lower()
    resumo_tokens = nltk.word_tokenize(resumo)
    resumo_tokens_clear = [word for word in resumo_tokens if not word in stopwords_custom]
    project['resumo'] = resumo_tokens_clear

    instituto = clear_number(project['depta/instituto']).lower()
    instituto_tokens = nltk.word_tokenize(instituto)
    instituto_tokens_clear = [word for word in instituto_tokens if not word in stopwords_custom]
    project['depta/instituto'] = instituto_tokens_clear

    palavras_chaves_tokens_clear = [word.lower() for word in project['palavras_chaves'] if not word in stopwords_custom]
    project['palavras_chaves'] = palavras_chaves_tokens_clear

    print(project)


with open(f'history_data/1/clear_all.json', 'w', encoding='utf-8') as fp:
    json.dump(projects_dict, fp, indent=4, ensure_ascii=False)
