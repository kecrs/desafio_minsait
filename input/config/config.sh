#!/bin/bash

DATE="$(date --date="-0 day" "+%Y%m%d")"

TABLES=("CLIENTES" "DIVISAO" "ENDERECO" "REGIAO" "VENDAS")

#HIVE
TARGET_DATABASE="desafio_curso"
DIR_HDFS="/datalake/raw/"
PARTICAO="$(date --date="-0 day" "+%Y%m%d")"