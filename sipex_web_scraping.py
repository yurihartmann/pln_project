import json
import traceback
from time import sleep
from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.common.by import By


class SipexWebScraping:

    MODALIDADE_X_PATH = '//*[@id="div2"]/table[1]/tbody/tr[1]/td[2]'

    def __init__(self):
        self.config = dotenv_values(".env")
        print(self.config)
        self.driver = webdriver.Chrome()
        self.login()

    def login(self):
        self.driver.get("https://www.furb.br/pqex/index.do")
        user = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/form/div[1]/input")
        user.send_keys(self.config.get("USER"))
        password = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/form/div[2]/input")
        password.send_keys(self.config.get("PASSWORD"))
        submit_button = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div/form/div[3]/button")
        submit_button.click()
        sleep(5)

    def find_text(self, xpath: str) -> str | None:
        try:
            return self.driver.find_element(By.XPATH, xpath).text
        except:
            return None

    def get_data_in_geral_data(self):
        SEARCH_LIST_IN_GERAL_DATA: dict = {
            'Resumo:': 'resumo',
            'Título:': 'titulo',
            'Depto/Instituto:': 'depta/instituto',
        }
        data = {}

        tbody = self.driver.find_element(By.XPATH, '//*[@id="div2"]/table/tbody')

        for tr in tbody.find_elements(By.TAG_NAME, "tr"):

            tds = tr.find_elements(By.TAG_NAME, "td")

            if tds[0].text in SEARCH_LIST_IN_GERAL_DATA.keys():
                data[SEARCH_LIST_IN_GERAL_DATA.get(tds[0].text)] = tds[1].text

        return data

    def get_palavra_chaves(self):
        try:
            th = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Palavras-Chave')]")[1]
            tbody = th.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
            tr = tbody.find_elements(By.TAG_NAME, "tr")[1]

            palavras_chaves = tr.find_element(By.TAG_NAME, "td").text.split(";")
            palavras_chaves = list(map(lambda x: x.strip(), palavras_chaves))

            return {
                "palavras_chaves": palavras_chaves[:-1]
            }
        except:
            return {}

    def get_areas(self):
        return {}

    def get_data(self, ano: int, numeros_de_procura: int) -> list:
        result = []

        for num in range(numeros_de_procura):
            try:
                url = f"https://www.furb.br/pqex/projeto/buscaProjeto.view?nrAnoProjeto={ano}&nrProjeto={num}"
                self.driver.get(url)

                modalidade = self.find_text(self.MODALIDADE_X_PATH)

                if not modalidade or 'Projeto de Extensão - Projeto' not in modalidade:
                    continue

                data = {}
                data.update(self.get_data_in_geral_data())
                data.update(self.get_palavra_chaves())
                # data.update(self.get_areas())

                if not data:
                    continue

                data.update({
                    'ano': ano,
                    'projeto_numero': num
                })
                print(data)

                result.append(data)
                print(f"Carregou ano={ano} num={num}")

            except:
                traceback.print_exc()

        return result

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    START_ANO = 2008
    FINAL_ANO = 2022
    N_DE_PROCURA = 500

    sipex = SipexWebScraping()

    for ano in range(START_ANO, FINAL_ANO+1):
        result = sipex.get_data(ano=ano, numeros_de_procura=N_DE_PROCURA)

        with open(f'data/{ano}.json', 'w', encoding='utf-8') as fp:
            json.dump(result, fp, indent=4, ensure_ascii=False)
