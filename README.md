# Monitoramento de Posição no Google Maps

Este projeto é uma aplicação **Python** que permite **monitorar a posição de um comércio nos resultados de busca do Google Maps**, com base em termos de buscas específicos.

Ele foi pensado para ajudar a WA Digital Premium (empresa de Marketing) a acompanhar o desempenho de SEO de empresas no Google Maps ao longo do tempo, armazenando históricos e exportando relatórios em Excel.

---

## Funcionalidades

* Cadastro de comércios em banco de dados PostgreSQL
* Busca automática da posição do comércio no Google Maps (via Selenium)
* Armazenamento do histórico de buscas e rankings
* Reutilização da última lista de termos de buscas pesquisados
* Exportação dos resultados para **Excel**, organizados por data
* Validação de endereço automaticamente via **API ViaCEP**

---

## Tecnologias Utilizadas

* **Python 3.13.1**
* **Selenium** (automação do navegador)
* **PostgreSQL** (armazenamento dos dados)
* **Pandas** (manipulação e exportação de dados)
* **Requests** (consumo da API ViaCEP)
* **webdriver‑manager**
* **tqdm** (barra de progresso)
* **Git/Github** (Versionamento de código)

---

## Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

* Python 3.13.1
* Google Chrome (o webdriver_manager cuidará do driver automaticamente)
* Instância do PostgreSQL ativa

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/mathk4/Automacao-seo-googlemaps.git
cd Automacao-seo-googlemaps
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 3. Configuração do Banco de Dados

* Crie um banco de dados no PostgreSQL
* Execute os comandos contidos no arquivo Tabelas.sql para criar a estrutura de tabelas necessária.

### 4. Variáveis de Ambiente

* Renomeie o arquivo .env.example para .env
* Preencha as credenciais de acesso ao seu banco de dados:

```env
DB_HOST=localhost
DB_NAME=nome_do_banco
DB_USER=usuario
DB_PASS=senha
DB_PORT=5432
```

---

## Como Usar

Execute o projeto com:

```bash
python main.py
```

Você verá um menu interativo no terminal:

```text
1. Cadastrar comercio           # Registra uma nova empresa no banco (solicita CEP e valida dados)
2. Ver comercios cadastrados    # Lista todas as empresas salvas
3. Realizar busca de posição    # Inicia uma automação no Selenium para verificar o ranking no Google Maps (Deve-se ter o comercio cadastrado antes)
4. Resultados em excel          # Exporta um relatório de um período selecionado por você para um arquivo .xlsx
5. Sair                         # Encerra a aplicação
```

Escreva o número da opção que quer acessar e aperte enter

### Busca de posição

* Informe o nome do comércio cadastrado
* Insira novos termos de pesquisa (Exemplo: Massagem em Joinville, Massoterapia em Joinville, ...) **ou** reutilize a última lista
* O sistema abrirá o Google Maps em modo invisível e analisará os resultados

---

## Estrutura do Projeto 

```text
├── criacao_das_tabelas_no_postgree/
    ├── Tabelas.sql # Schema do banco de dados
├── main.py # Menu principal e fluxo da aplicação
├── procurar_posicao_cliente.py # Lógica de busca no Google Maps (Selenium)
├── database.py # Funções de acesso ao banco de dados
├── requirements.txt # Dependências do projeto
├── .env.example # Exemplo de variáveis de ambiente
```

---

## ⚠️ Observações Importantes

* Seletores CSS: O Google Maps altera suas classes de CSS frequentemente. Caso o script pare de encontrar elementos, verifique as variáveis no topo de procurar_posicao_cliente.py
* Modo Headless: Por padrão, o navegador roda em segundo plano. Para visualizar o trabalho em tempo real, altere a linha chrome_options.add_argument("--headless=new") no arquivo de busca, apagando ou tornando a linha como comentario.

---

## 🤝 Contribuições e Feedbacks

Este projeto foi desenvolvido a partir de um **problema real enfrentado pela empresa de marketing mencionada antes**, sendo também uma oportunidade de aplicar, na prática, conhecimentos adquiridos durante meus estudos em Engenharia da Computação.

Como estou em constante aprendizado, feedbacks e sugestões são muito bem-vindos.  
Sinta-se à vontade para abrir uma *Issue*, enviar um *Pull Request* ou entrar em contato.

Toda contribuição é uma oportunidade de evolução técnica e melhoria contínua do projeto.

---

## Autor

**Matheus Rodrigues**
Estudante de Engenharia da Computação

---