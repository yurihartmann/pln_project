import json
import traceback
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


class SipexWebScraping:

    DATA_TO_SEARCH = {
        'modalidade': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[1]/td[2]',
        'titulo': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[2]/td[2]/b',
        'autor': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[3]/td[2]/b',
        'titulacao_autor': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[4]/td[2]/table/tbody/tr[1]/td[2]',
        'cargo': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td[2]',
        'departamento_setor': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[4]/td[2]/table/tbody/tr[3]/td[2]',
        'email': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[4]/td[2]/table/tbody/tr[4]/td[2]',
        'email_furb': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[4]/td[2]/table/tbody/tr[5]/td[2]',
        'site_projeto': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[6]/td[2]/a',
        'resumo': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[7]/td[2]',
        'departamento_instituto': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[1]/tbody/tr[8]/td[2]',
        'palavras_chaves': '/html/body/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[3]/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td'
    }

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.furb.br/pqex/index.do")
        sleep(60)

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
    for ano in range(2008, 2024):
        result = SipexWebScraping().get_data(ano=ano, numeros_de_procura=300)

        with open(f'data/{ano}.json', 'w') as fp:
            json.dump(result, fp)
