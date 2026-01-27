-- Tabela para armazenar dados do comércio
CREATE TABLE comercios (
	id_comercio INT GENERATED ALWAYS AS IDENTITY,
	nome_fantasia VARCHAR NOT NULL,
	responsavel VARCHAR NOT NULL,
	cep CHAR(9) NOT NULL,
	pais VARCHAR NOT NULL,
	estado CHAR(2) NOT NULL,
	cidade VARCHAR NOT NULL,
	bairro VARCHAR NOT NULL,
	logradouro VARCHAR NOT NULL,
	numero INT NOT NULL,
	PRIMARY KEY (id_comercio)
);

-- Tabela para armazenar as sessões de pesquisa
CREATE TABLE sessoes (
    id_sessao INT GENERATED ALWAYS AS IDENTITY,
    id_comercio INT NOT NULL,
    data_pesquisa DATE DEFAULT CURRENT_DATE, 
    PRIMARY KEY (id_sessao),
    CONSTRAINT fk_comercio FOREIGN KEY(id_comercio) REFERENCES comercios(id_comercio)
);

-- Tabela para armazenar os resultados das palavras
CREATE TABLE rank_palavras (
	id_ranking INT GENERATED ALWAYS AS IDENTITY,
	id_sessao INT NOT NULL,
	termo_pesquisado VARCHAR NOT NULL,
	posicao INT,
	total_resultados INT,
	PRIMARY KEY (id_ranking),
	CONSTRAINT fk_sessao FOREIGN KEY(id_sessao) REFERENCES sessoes(id_sessao)
);