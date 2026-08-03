import requests
import pandas as pd
import database as db
from procurar_posicao_cliente import buscar_todas_palavras
import re
from procurar_potenciais_clientes import busca_potenciais_clientes

def potenciais_clientes():
    print("=============POTENCIAIS CLIENTES==============")
    termos_pesquisa = input("Digite palavras chaves que possam ser usadas para encontrar potenciais clientes (separadas por vírgula) (cada termo gera um conjunto de resultados com quantidade especificada nos proximos passos): Ex: Fisioterapia, Pilates Clínico, etc:  ")
    termos_pesquisa = [termo.strip() for termo in termos_pesquisa.split(",")]

    cidades = input("Digite as cidades que deseja buscar potenciais clientes (separadas por vírgula): Ex: São Paulo, Rio de Janeiro, etc:  ")
    cidades = [cidade.strip() for cidade in cidades.split(",")]
    
    while True:
        qnt_cliente_por_cidade = input("digite a quantidade de clientes que deseja buscar por cidade separe por virgula na ordem das cidaddes escritas anteriormente: Ex: 10, 20, etc:  ")
        qnt_cliente_por_cidade = [int(qtd.strip()) for qtd in qnt_cliente_por_cidade.split(",")]
        if len(qnt_cliente_por_cidade) == len(cidades):
            break
        else:
            resposta = input("Número de quantidades não corresponde ao número de cidades. Deseja tentar novamente ou desistir? (1 para tentar novamente | 2 para desistir)")
            if resposta == '2':
                return

    pais = input("Digite o país que deseja buscar potenciais clientes: Ex: BR, USA, etc:  ")
    pais = pais.strip()

    print("Iniciando busca, aguarde...")

    resultado = busca_potenciais_clientes(termos_pesquisa, cidades, pais, qnt_cliente_por_cidade)

    if resultado.empty:
        print("Nenhum potencial cliente encontrado.")
        return
    else:
        resultado.to_excel("potenciais_clientes.xlsx", index=False)

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
        data_inicioBR = f"{dia_inicio}/{mes_inicio}/{ano_inicio}"
        data_fim = f"{ano_fim}-{mes_fim}-{dia_fim}"
        data_fimBR = f"{dia_fim}/{mes_fim}/{ano_fim}"

        print(f"Você escolheu o período de {data_inicioBR} até {data_fimBR}. Está correto ?")
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

    data_inicioBR = data_inicioBR.replace("/", "-")
    data_fimBR = data_fimBR.replace("/", "-")
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome_comercio)
    tabela_excel.to_excel(f'resultados_{nome_limpo}_{data_inicioBR}_a_{data_fimBR}.xlsx')

    print("Excel gerado com sucesso!")





while True:
    print("=============MENU==============")
    print("1. Cadastrar comercio")
    print("2. Ver comercios cadastrados")
    print("3. Resalizar busca de posiçao")
    print("4. Resultados em excel")
    print("5. Buscar potenciais clientes")
    print("6. Sair")

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
            potenciais_clientes()
        case "6":
            print("Saindo...")
            break
        case _:
            print("Opção inválida. Tente novamente.")