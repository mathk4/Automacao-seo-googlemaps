#tarefas:
# principais:
# - fazer funções relacionadas ao banco de dados

# secundarias:
# - verificar se a mepresa existe no google maps antes de cadastrar


import requests
import pandas as pd
import database as db
from procurar_posicao_cliente import buscar_todas_palavras

def cadastrar_comercio():
    print("=============CADASTRAR COMERCIO==============")
    nome_fantasia = input("Nome fantasia do comercio: ")
    responsavel = input("Nome do responsavel: ")
    pais = input("País: ")

    while True:
        cep = input("CEP do comercio (apenas números): ")
        url = "https://viacep.com.br/ws/" + cep + "/json/"

        resposta = requests.get(url)

        if resposta.status_code == 200:
            resposta_dict = resposta.json()

            if resposta_dict.get("erro") is None:
                break
            else:
                print("CEP inválido. Tente novamente.")
        else:
            print("Formato de CEP inválido (deve ter 8 números). Tente novamente.")

    estado = resposta_dict['uf']
    cidade = resposta_dict['localidade']
    bairro = resposta_dict['bairro']
    logradouro = resposta_dict['logradouro']
    
    while True:
        numero = input("Número do comercio: ")
        if numero.isdigit():
            break
        else:
            print("Número inválido. Tente novamente.")

    print("Tem certeza que deseja cadastrar?")
    resposta = input("Digite 's' para sim ou 'n' para não: ")
    
    if resposta.lower() == 'n':
        print("Cadastro cancelado.")
        return

    cep = cep[0:5] + '-' + cep[5:8]
    db.DB_inserir_comercio(nome_fantasia, responsavel, cep, pais, estado, cidade, bairro, logradouro, numero) 

def ver_comercios():
    print("=============COMERCIOS CADASTRADOS==============")

    lista_comercios = db.DB_ler_comercios()

    for comercio in lista_comercios:
        print(comercio)

def realizar_busca_posicao():
    print("=============BUSCA DE POSIÇÃO==============")

    while True:
        nome_comercio = input("Nome do comercio cadastrado: ")
        comercio_existe = db.DB_comercio_existe(nome_comercio)
        
        if comercio_existe == False:
            resposta = input("Comercio não encontrado. Deseja tentar novamente? (s/n)")
            if resposta.lower() == 'n':
                return
        else:
            break
    
    while True:
        resposta = input(""" 
                        1. Inserir nova lista de palavras-chave
                        2. Utilizar a ultima lista de palavras-chave cadastrada dessa empresa
                        
                        Escolha uma opção: """)
        
        if resposta == '1':
            palavras_chave =  input("Digite a lista de palavras-chave separadas por vírgula: ")
            palavras_chave = palavras_chave.split(',')
            break

        elif resposta == '2':
            
            palavras_chave = db.DB_buscar_ultimas_palavras_chave(nome_comercio)
            break

        else:
            print("Opção inválida, tente novamente.")
    
    resultado = buscar_todas_palavras(palavras_chave, nome_comercio)

    print("Resultados da busca:")
    print(resultado)

    resposta = input("deseja salvar esses resultados? (s/n): ")
    if resposta.lower() == 's':
        
        id_comercio = db.DB_obter_id_comercio(nome_comercio)

        db.DB_inserir_resultados_busca(id_comercio, resultado)
    else:
        print("Resultados não foram salvos.")
        
    return

def resultados_em_excel():
    print("=============RESULTADOS EM EXCEL==============")
    
    while True:
        nome_comercio = input("Nome do comercio cadastrado: ")
        comercio_existe = db.DB_comercio_existe(nome_comercio)
        
        if comercio_existe == False:
            resposta = input("Comercio não encontrado. Deseja tentar novamente? (s/n)")
            if resposta.lower() == 'n':
                return
        else:
            break
        
    data = input("De que data até que data deseja os resultados ? (formato dd/mm/aaaa - dd/mm/aaaa)")

    # Fazendo ainda...

    print("Excel gerado com sucesso!")

while True:
    print("=============MENU==============")
    print("1. Cadastrar comercio")
    print("2. Ver comercios cadastrados")
    print("3. Resalizar busca de posiçao")
    print("4. Resultados em excel")
    print("5. Sair")

    opcao = input("Escolha uma opçao: ")

    match opcao:
        case "1":
            cadastrar_comercio()
        case "2":
            ver_comercios()
        case "3":
            realizar_busca_posicao()
        case "4":
           # TODO: gerar resultados em excel com filtros
            pass
        case "5":
            print("Saindo...")
            break
        case _:
            print("Opção inválida. Tente novamente.")