
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

  

A aplicação existente em /input/desafio_curso/app/Projeto Vendas.pbix é um exemplo básico de utilização de ferramente de BI para criar dashboard para visualização dos dados que foram tratados no projeto.