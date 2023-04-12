import json

FILE = "history_data/1/clear_all.json"
projects_dict: dict

with open(FILE) as file:
    projects_dict = json.load(file)

cluster_de_palavras_chaves = {}

for project in projects_dict:
    for palavra_chave in project['palavras_chaves']:

        if cluster_de_palavras_chaves.get(palavra_chave):
            cluster_de_palavras_chaves[palavra_chave] += project['titulo'] + project['resumo']
        else:
            cluster_de_palavras_chaves[palavra_chave] = project['titulo'] + project['resumo']


with open(f'history_data/1/cluster_palavras_chaves.json', 'w', encoding='utf-8') as fp:
    json.dump(cluster_de_palavras_chaves, fp, indent=4, ensure_ascii=False)
