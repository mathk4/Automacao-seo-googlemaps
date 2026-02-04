from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import random

#___________________ Caso o valor de algum elemento mude, altere por aqui __________________

classe_nome_empresa = 'hfpxzc'  
css_container_resultados = 'div[role="feed"]'
classe_fim_da_lista = 'HlvSq'
xpath_botao_pesquisar = '/html/body/div[1]/div[2]/div[9]/div[3]/div[1]/div[1]/div/div[1]/div[1]/button/span'

#___________________________________________________________________________________________




#_________________________________________ Funções _________________________________________

def pesquisar_palavra_chave(navegador, palavra_chave):
    palavra_chave_formatada = palavra_chave.strip()
    palavra_chave_formatada = palavra_chave_formatada.lower()
    palavra_chave_formatada = palavra_chave_formatada.replace(' ', '+')
    navegador.get(f'https://www.google.com/maps/search/{palavra_chave_formatada}/')
    while len(navegador.find_elements(By.XPATH, xpath_botao_pesquisar)) < 1: # -> lista for vazia -> o botão de pesquisar não carregou ainda
        time.sleep(1.5)
    botao = navegador.find_element(By.XPATH, xpath_botao_pesquisar)
    botao.click() # por algum motivo, o rankin da palavra muda se o botão de pesquisar for clicado (normalmente é por onde eu fazia as pesquisas manuais, entao optei por fazer isso)

def carregar_todos_resultados(navegador):
    
    while len(navegador.find_elements(By.CSS_SELECTOR, css_container_resultados)) < 1: # -> lista for vazia -> o container de resultados não carregou ainda
        time.sleep(1.5)

    container_resultado =  navegador.find_element(By.CSS_SELECTOR, css_container_resultados)
    antiga_quantidade_elementos_no_container = 0
    tentativas = 0

    while True:
        
        navegador.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', container_resultado) # scroll no container de resultados
        time.sleep(random.uniform(2, 3.5))

        Quantidade_elementos_no_conteiner = len(container_resultado.find_elements(By.CLASS_NAME, classe_nome_empresa))

        if Quantidade_elementos_no_conteiner == antiga_quantidade_elementos_no_container:
            if tentativas >= 3 and len(navegador.find_elements(By.CLASS_NAME, classe_fim_da_lista)) > 0:
                    tentativas = 0
                    break
            tentativas = tentativas + 1  
        if tentativas == 10:
            break
        
        antiga_quantidade_elementos_no_container = Quantidade_elementos_no_conteiner


def buscar_posicao_cliente(navegador, nome_empresa):

    lista_empresas = navegador.find_elements(By.CLASS_NAME, classe_nome_empresa)
    
    for i, empresa in enumerate(lista_empresas, start=1):
        if empresa.get_attribute("aria-label") == nome_empresa:
            return i, len(lista_empresas) # (empresa na posição i, Quantidade de empresas analisadas)

    # Empresa não encontrada na lista de resultados
    return None, len(lista_empresas)

#___________________________________________________________________________________________




#_________________________________________ Script __________________________________________

def buscar_todas_palavras(palavra_chave, nome_empresa):

    chrome_options = Options() 
    chrome_options.add_argument("--window-size=1920,1080") # A parte de apertar o botao de buscar as vezes nao funciona se a janela estiver pequena
    chrome_options.add_argument("--log-level=3") # Silencia logs que não sejam erros críticos
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Limpa avisos desnecessários do console

    #abrindo o navegador
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=chrome_options)

    #realizando a pesquisa de todas as palavras-chave
    resultado = []
    try: 
        for palavra in tqdm(palavra_chave, desc="Pesquisando palavras-chave"):
            pesquisar_palavra_chave(navegador, palavra)

            carregar_todos_resultados(navegador)

            posicao_cliente, total_empresas = buscar_posicao_cliente(navegador,nome_empresa)
            resultado.append((palavra.strip(), posicao_cliente, total_empresas))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        navegador.quit()
    
    return resultado
#___________________________________________________________________________________________
