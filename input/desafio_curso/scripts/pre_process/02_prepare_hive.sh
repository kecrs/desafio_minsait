#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG="${BASEDIR}/../../config/config.sh"
source "${CONFIG}"

#CRIANDO A BASE DE DADOS
beeline -u jdbc:hive2://localhost:10000 -f ../hql/create_database.hql

#CRIANDO AS TABELAS
for t in "${TABLES[@]}"
do
    echo $t

    HDFS_DIR="${DIR_HDFS}$t"
    
    beeline -u jdbc:hive2://localhost:10000 \
    --hivevar TARGET_DATABASE="${TARGET_DATABASE}"\
    --hivevar HDFS_DIR="${HDFS_DIR}"\
    --hivevar PARTICAO="${PARTICAO}"\
    -f ../hql/create_table_$t.hql 
done