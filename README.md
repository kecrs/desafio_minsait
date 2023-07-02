
# DESAFIO BIG DATA/MODELAGEM

  

## 📌 ESCOPO DO DESAFIO

Neste desafio serão feitas as ingestões dos dados que estão na pasta /raw onde vamos ter alguns arquivos .csv de um banco relacional de vendas.

  

- VENDAS.CSV

- CLIENTES.CSV

- ENDERECO.CSV

- REGIAO.CSV

- DIVISAO.CSV

  

Seu trabalho como engenheiro de dados/arquiteto de BI é prover dados em uma pasta desafio_curso/gold em .csv para ser consumido por um relatório em PowerBI que deverá ser construído dentro da pasta 'app' (já tem o template).

  

## 📑 ETAPAS

1. Etapa 1 - Enviar os arquivos para o HDFS

	- nesta etapa lembre de criar um shell script para fazer o trabalho repetitivo (não é obrigatório)

  

1. Etapa 2 - Criar o banco DEASFIO_CURSO e dentro tabelas no Hive usando o HQL e executando um script shell dentro do hive server na pasta scripts/pre_process.

  

	- DESAFIO_CURSO (nome do banco)

		- TBL_VENDAS

		- TBL_CLIENTES

		- TBL_ENDERECO

		- TBL_REGIAO

		- TBL_DIVISAO

  

1. Etapa 3 - Processar os dados no Spark Efetuando suas devidas transformações criando os arquivos com a modelagem de BI.

	OBS. o desenvolvimento pode ser feito no jupyter porem no final o codigo deve estar no arquivo desafio_curso/scripts/process/process.py

  

1. Etapa 4 - Gravar as informações em tabelas dimensionais em formato cvs delimitado por ';'.

  

	- FT_VENDAS

	- DIM_CLIENTES

	- DIM_TEMPO

	- DIM_LOCALIDADE

  

1. Etapa 5 - Exportar os dados para a pasta desafio_curso/gold

  

1. Etapa 6 - Criar e editar o PowerBI com os dados que você trabalhou.

	- No PowerBI criar gráficos de vendas.

1. Etapa 7 - Criar uma documentação com os testes e etapas do projeto.

  

## REGRAS

Campos strings vazios deverão ser preenchidos com 'Não informado'.

Campos decimais ou inteiros nulos ou vazios, deversão ser preenchidos por 0.

Atentem-se a modelagem de dados da tabela FATO e Dimensão.

Na tabela FATO, pelo menos a métrica <b>valor de venda</b> é um requisito obrigatório.

Nas dimensões deverá conter valores únicos, não deverá conter valores repetidos.

para a dimensão tempo considerar o campo da TBL_VENDAS <b>Invoice Date</b>

  
  

## ✅ RESOLUÇÃO

### PROCEDIMENTOS REALIZADOS

Para o desenvolvimento deste desafio foram recebidos 05 arquivos no formato .csv, conforme citado acima, como insumos de entrada para o projeto.

Portanto, essas foram as etapas realizadas:

* Upload dos arquivos para o HDFS do ambiente;

	* Para realização dessa etapa foi implementado o script /input/desafio_curso/scripts/pre_process/01_copy_to_hdfs.sh

* Criação da base de dados e das tabelas dentro do hive para armazenar os dados

	* Para realização dessa etapa foi implementado o script /input/desafio_curso/scripts/pre_process/02_prepare_hive.sh

* Análise dos dados

	* Foi visto que:

		* Cliente.csv

			* Existiam clientes duplicados (customer key: 10021911);

			* Existiam colunas que não eram interessantes para a utilização em uma aplicação de BI, exemplo: "business_unit", "customer_type", "phone" e "regional_sales_mgr";

			* Existiam colunas com os campos em branco ou nulo e que precisariam ser tratadas, conforme solicitação no desafio;

			* Existiam colunas numéricas que estavam sendo identificadas como string.

		* Endereco.csv

			* Existiam colunas que não eram interessantes para utilização em uma aplicação de BI, exemplo: "customer_address_1", "customer_address_2", "customer_address_3", "customer_address_4" e "zip_code";

			* Existiam colunas com os campos em branco ou nulo e que precisariam ser tratadas, conforme solicitação no desafio;

			* Existiam colunas numéricas que estavam sendo identificadas como string.

		* Divisao.csv

			* Os dados são simples e houve apenas a identificação de converter coluna que continha apenas valores numéricos e era do tipo string para o tipo Inteiro.

		* Regiao.csv

			* Os dados são simples e houve apenas a identificação de converter coluna que continha apenas valores numéricos e era do tipo string para o tipo Inteiro.

		* Vendas.csv

			* Existiam colunas com os campos em branco ou nulo e que precisariam ser tratadas, conforme solicitação no desafio;

			* Existiam colunas numéricas que estavam sendo identificadas como string;

			* Existiam colunas de data que estavam sendo identificadas como string;

			* Existiam colunas que não eram interessantes para utilização em uma aplicação de BI, exemplo: 'item_class', 'item_number', 'item', 'line_number' e 'list_price';

* Criação de script, utilizando o jupyter-spark, para que realize todos os tratamentos e processamentos necessários que foram identificados na análise dos dados e demais etapas (/input/desafio_curso/scripts/process/process.py);

* Criação dos arquivos csv para serem utilizados na aplicação em Power BI;

* Criação da aplicação Projeto.pbix  

### ESTRUTURA DE ARQUIVOS

Foi utilizada a seguite estrutura de arquivos para a resolução do projeto

  

Criação da Pasta input/desafio_curso, com a seguinte hierarquia:

  

* app => Pasta que armazena a aplicação em Power BI da resolução do desafio

* config => Pasta que armazena o arquivo de configuração que é utilizado pelos scripts do projeto

* gold => Pasta que armazena os arquivos de dados, depois de tratados, para serem utilizados pela aplicação Power BI

* raw => Pasta que armazena os dados originais do projeto

* run => Pasta que armazena shell script para executar o script do spark

* scripts => Pasta que armazena os scripts utilizado no projeto

	* hql => Pasta que armazena os scripts .hql para criar as tabelas que armazena os dados do projeto

	* pre_process => Pasta que armazena os scripts que devem se executados antes de realizar o processamento do projeto

	* process => Pasta que armazena o script de processamento dos dados

  

### SEQUÊNCIA DE EXECUÇÃO DOS SCRIPTS

  

1. O projeto utiliza uma estrutura de ferramentas para BIG DATA que estão dockerizadas e para isso foi realizado um fork no repositório: https://github.com/caiuafranca/bigdata_docker/tree/ambiente-curso e realizado um clone da branch ambiente-curso;

  

1. Após startar o ambiente dockerizado, executar a seguinte sequência de scripts:

	* Em input/desafio_curso/scripts/pre_process, executar 01_copy_to_hdfs.sh

	* Em input/desafio_curso/scripts/pre_process, executar 02_prepare_hive.sh

  

1. Entrar no docker jupyter-spark e executar o script input/desafio_curso/run/process.sh

  

### APLICAÇÃO DE BI

  

A aplicação existente em /input/desafio_curso/app/Projeto.pbix é um exemplo básico de utilização de ferramente de BI para criar dashboard para visualização dos dados que foram tratados no projeto.