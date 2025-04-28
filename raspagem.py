import numpy as np
import pandas as pd

# webdriver é o arquivo do navegador para simular
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# service para config path do executavel do chrome driver
from selenium.webdriver.chrome.service import Service

# class que permite executar ações avançadas (o mover do mouse, clique/array)
from selenium.webdriver.common.action_chains import ActionChains

# selenium action chains serve tanto par web scraping quanto teste automatizado
# nem todo site aceita, e o processo é demorado

# class q espera de forma explicita até q uma condition seja true (ex: elemento aparecer)
from selenium.webdriver.support.ui import WebDriverWait

# condicoes esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# para tratamento de exceção
from selenium.common.exceptions import TimeoutException

import pandas as pd

# uso funções de tempo
import time

# caminho ChromeDrver
chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# config webdriver (simulador do navegador)
service = Service(chrome_driver_path) # control navegador pelo selenium
options = webdriver.ChromeOptions() # config opções do navegador
# exemplo: Não aparecer na tela a interface acontecendo
# options.add_argument("--headless")
options.add_argument('--disable-gpu') # evitar erros graficos
options.add_argument('--window_size=1920,1080') # define tamanho de tela fixo

# inicialização do webdriver
driver = webdriver.Chrome(service=service, options=options) # o segundo 'service' e 'options' são as variaveis declaradas previamente

url_base = 'https://www.vivareal.com.br/venda/?transacao=venda&pagina=1'
driver.get(url_base)
time.sleep(5) 

casas = {"metragem":[], 'quartos':[], 'banheiros':[], 'vagas':[], 'valor':[], 'nomeRua':[]}
pagina = 1


i = 0

while i <= 100:
    print(f'\nEscaneando Página {pagina}')

    try:
        # espera condição ser satisfeita
            # espera o driver até pegar os dados SE não pegar em 10 segundos ele passa para o próximo
        WebDriverWait(driver,10).until(

            # verif se todos elementos 'productCard' estão acessíveis
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="rp-property-cd"]'))

        )
        print('Elementos encontrados com sucesso!')
    except TimeoutException:
        print('Tempo de espera excedido!')

    
    lista_casas = driver.find_elements(By.CSS_SELECTOR, '[data-cy="rp-property-cd"]')

    for casa in lista_casas:
        try:
            nomeRua = casa.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-street-txt"]').text.strip()
            valor = casa.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text.strip()

            metragem = casa.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text.strip() if casa.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]') else np.nan
            quartos = casa.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text.strip() if casa.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]') else np.nan
            banheiros = casa.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]').text.strip() if casa.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]') else np.nan
            vagas = casa.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]').text.strip() if casa.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]') else np.nan

            
            print(f"{nomeRua} - {valor}")

            casas['metragem'].append(metragem)
            casas['quartos'].append(quartos)
            casas['banheiros'].append(banheiros)
            casas['vagas'].append(vagas)
            casas['valor'].append(valor)
            casas['nomeRua'].append(nomeRua)

            i += 1

        except Exception:
            print('Erro ao coletar dados: ', Exception)
            i += 1
    
    # encontrar acesso/botão da proxima pagina
    try:
        btn_proximo = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="next-page"]'))
            ) 
        if btn_proximo:
            # simulação de clicar e scrollar para achar btn prox page
                # execute_script da controle ao Selenium
            driver.execute_script('arguments[0].scrollIntoView();', btn_proximo)

            # clicar no elemento
            driver.execute_script('arguments[0].click();', btn_proximo)
            pagina += 1
            print(f'Indo para a página {pagina}')
            time.sleep(5)
        else:
            print('Você chegou na última página')
            break

    except Exception as e:
        print('Não foi possível avançar para a próxima página', e)
        break

driver.quit()


# dataframe
df = pd.DataFrame(casas)

# salvar dados em excel
df.to_excel('casas.xlsx', index=False)

print(f'Arquivo "casas" salvo com sucesso! ({len(df)}) produtos capturados!')