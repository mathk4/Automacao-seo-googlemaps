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

            # caso o cep tenha 8 números, mas esteja errado, a API renorta erro igual a true
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
        
        try:
            numero = int(input("Número do comercio: "))
        except ValueError:
            print("Número inválido. Tente novamente.")
            continue
        break

    cep = cep[0:5] + '-' + cep[5:8]
    
    print("Tem certeza que deseja cadastrar?")
    print(f"""
        Nome Fantasia: {nome_fantasia}
          Responsavel: {responsavel}
                  CEP: {cep}
                 País: {pais}
               Estado: {estado}
               Cidade: {cidade}
               Bairro: {bairro}
           Logradouro: {logradouro}
               Número: {numero}
        """)
    while True:
        resposta = input("Digite 's' para sim ou 'n' para não: ")
        
        if resposta.lower() == 'n':
            print("Cadastro cancelado.")
            return
        if resposta.lower() != 's':
            print("Resposta inválida. Tente novamente.")
            continue
        break

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
            if not palavras_chave:
                return

            break

        else:
            print("Opção inválida, tente novamente.")
    
    resultado = buscar_todas_palavras(palavras_chave, nome_comercio)
    if not resultado:
        print("Nenhum resultado obtido.")
        return

    print("Resultados da busca:")
    print(resultado)

    resposta = input("deseja salvar esses resultados? (s/n): ")
    if resposta.lower() == 's':
        
        id_comercio = db.DB_obter_id_comercio(nome_comercio)
        if id_comercio is None:
            print("Erro ao obter ID do comercio. Resultados não foram salvos.")
            return

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
        
    while True:
        try:
            print("De que data até que data deseja os resultados ?")
            dia_inicio = int(input("Dia inicio (DD): "))
            mes_inicio = int(input("Mes inicio (MM): "))
            ano_inicio = int(input("Ano inicio (AAAA): "))
            dia_fim = int(input("Dia fim (DD): "))
            mes_fim = int(input("Mes fim (MM): "))
            ano_fim = int(input("Ano fim (AAAA): "))
        except ValueError:
            print("Data invalida, escreva numeros inteiros.")
            continue

        data_inicio = f"{ano_inicio}-{mes_inicio}-{dia_inicio}"
        data_fim = f"{ano_fim}-{mes_fim}-{dia_fim}"

        print(f"Você escolheu o período de {data_inicio} até {data_fim}. Está correto ?")
        resposta = input("Digite 's' para sim ou 'n' para não: ")
        if resposta.lower() == 's':
            break
    
    df = db.DB_procurar_rank_empresa_por_data(nome_comercio, data_inicio, data_fim)

    if df.empty:
        print("Nenhum dado encontrado para esse período.")
        return

    # Datas viram colunas e os termos viram linhas
    # swaplevel organiza os cabeçalhos para que a data fique acima de 'posicao' e 'total'
    tabela_excel = df.pivot_table(index='termo_pesquisado', columns='data_pesquisa', values=['posicao', 'total_resultados'], aggfunc='max')
    tabela_excel = tabela_excel.swaplevel(0,1, axis=1).sort_index(axis=1)

    tabela_excel.columns.names = [None, None] # Remove "data_pesquisa" do topo
    tabela_excel.index.name = None            # Remove "termo_pesquisado" de cima da coluna A

    tabela_excel.to_excel(f'resultados_{nome_comercio}_{data_inicio}_a_{data_fim}.xlsx')

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
            resultados_em_excel()
        case "5":
            print("Saindo...")
            break
        case _:
            print("Opção inválida. Tente novamente.")