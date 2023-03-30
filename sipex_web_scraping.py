import json
import traceback
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


class SipexWebScraping:

    MODALIDADE_X_PATH = '//*[@id="div2"]/table[1]/tbody/tr[1]/td[2]'

    DATA_TO_SEARCH = {
        'titulo': '//*[@id="div2"]/table[1]/tbody/tr[2]/td[2]',
        'departamento_setor': '//*[@id="div2"]/table[1]/tbody/tr[8]/td[2]',
        'resumo': '//*[@id="div2"]/table[1]/tbody/tr[7]/td[2]',
        'palavras_chaves': '//*[@id="div2"]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td'
    }

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.furb.br/pqex/index.do")
        sleep(15)

    def find_text(self, xpath: str) -> str | None:
        try:
            return self.driver.find_element(By.XPATH, xpath).text
        except:
            return None

    def get_data(self, ano: int, numeros_de_procura: int) -> list:
        result = []

        for num in range(numeros_de_procura):
            try:
                url = f"https://www.furb.br/pqex/projeto/buscaProjeto.view?nrAnoProjeto={ano}&nrProjeto={num}"
                self.driver.get(url)

                modalidade = self.find_text(self.MODALIDADE_X_PATH)

                if 'Projeto de Extensão - Projeto' not in modalidade:
                    continue

                data = {}
                for key, xpath in self.DATA_TO_SEARCH.items():
                    text = self.find_text(xpath)
                    if text:
                        data[key] = text

                if not data:
                    continue

                data.update({
                    'ano': ano,
                    'projeto_numero': num
                })

                result.append(data)
                print(f"Carregou ano={ano} num={num}")

            except:
                traceback.print_exc()

        return result

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    sipex = SipexWebScraping()

    for ano in range(2022, 2023):
        result = sipex.get_data(ano=ano, numeros_de_procura=300)

        with open(f'data/{ano}.json', 'w') as fp:
            json.dump(result, fp)
