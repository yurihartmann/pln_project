import json

FILE = "history_data/1/clear_all.json"
projects_dict: dict

with open(FILE) as file:
    projects_dict = json.load(file)

for cluster_name in ['palavras_chaves', 'depta/instituto']:

    cluster = {}

    for project in projects_dict:
        for palavra_chave in project[cluster_name]:

            if cluster.get(palavra_chave):
                cluster[palavra_chave] += project['titulo'] + project['resumo']
            else:
                cluster[palavra_chave] = project['titulo'] + project['resumo']

    with open(f'history_data/1/cluster_{cluster_name.replace("/", "_")}.json', 'w', encoding='utf-8') as fp:
        json.dump(cluster, fp, indent=4, ensure_ascii=False)
