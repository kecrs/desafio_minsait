CREATE EXTERNAL TABLE IF NOT EXISTS ${TARGET_DATABASE}.divisao (
        Division                string
        ,Division_Name          string
    )
COMMENT 'Tabela de Divisão'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
location '${HDFS_DIR}'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS ${TARGET_DATABASE}.tbl_divisao(
        Division                string
        ,Division_Name          string
)
PARTITIONED BY (DT_FOTO STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
TBLPROPERTIES ('orc.compress'='SNAPPY');

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE ${TARGET_DATABASE}.tbl_divisao
PARTITION(DT_FOTO)
SELECT
        Division                
        ,Division_Name                                  
        ,${PARTICAO} as DT_FOTO
FROM ${TARGET_DATABASE}.divisao;