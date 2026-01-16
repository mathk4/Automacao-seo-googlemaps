from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

#___________________ Caso o valor de algum elemento mude, altere por aqui __________________

classe_nome_empresa = 'hfpxzc'  
css_container_resultados = 'div[role="feed"]'
classe_fim_da_lista = 'HlvSq'
xpath_botao_pesquisar = '/html/body/div[1]/div[2]/div[9]/div[3]/div[1]/div[1]/div/div[1]/div[1]/button/span'

#___________________________________________________________________________________________




#_________________________________________ Funções _________________________________________

def pesquisar_palavra_chave(palavra_chave):
    palavra_chave_formatada = palavra_chave.strip()
    palavra_chave_formatada = palavra_chave_formatada.lower()
    palavra_chave_formatada = palavra_chave_formatada.replace(' ', '+')
    navegador.get(f'https://www.google.com/maps/search/{palavra_chave_formatada}/')
    while len(navegador.find_elements(By.XPATH, xpath_botao_pesquisar)) < 1: # -> lista for vazia -> o botão de pesquisar não carregou ainda
        time.sleep(1.5)
    botao = navegador.find_element(By.XPATH, xpath_botao_pesquisar)
    botao.click() # por algum motivo, o rankin da palavra muda se o botão de pesquisar for clicado (normalmente é por onde eu fazia as pesquisas manuais, entao optei por fazer isso)

def carregar_todos_resultados():
    
    while len(navegador.find_elements(By.CSS_SELECTOR, css_container_resultados)) < 1: # -> lista for vazia -> o container de resultados não carregou ainda
        time.sleep(1.5)

    while len(navegador.find_elements(By.CLASS_NAME, classe_fim_da_lista)) < 1: # -> lista for vazia -> o elemento de "Você chegou ao final da lista." não carregou ainda
        navegador.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', navegador.find_element(By.CSS_SELECTOR, css_container_resultados)) # scroll no container de resultados
        time.sleep(2)


def buscar_posicao_cliente(nome_empresa):

    lista_empresas = navegador.find_elements(By.CLASS_NAME, classe_nome_empresa)
    
    for i, empresa in enumerate(lista_empresas, start=1):
        if empresa.get_attribute("aria-label") == nome_empresa:
            print(f'Encontrei a empresa na posição {i}')
            print(f"Quantidade de empresas analisadas: {len(lista_empresas)}")
            return i, len(lista_empresas)

    print("Empresa não encontrada na lista de resultados.")
    return None, len(lista_empresas)

#___________________________________________________________________________________________




#_________________________________________ Script __________________________________________

palavra_chave = '...'

nome_empresa = '...'

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
navegador.maximize_window() # A parte de apertar o botao de buscar as vezes nao funciona se a janela estiver pequena

pesquisar_palavra_chave(palavra_chave)

carregar_todos_resultados()

buscar_posicao_cliente(nome_empresa)

navegador.quit()
#___________________________________________________________________________________________
