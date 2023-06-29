CREATE EXTERNAL TABLE IF NOT EXISTS ${TARGET_DATABASE}.regiao (
        Region_Code			string
        ,Region_Name        string
    )
COMMENT 'Tabela de Região'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
location '${HDFS_DIR}'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS ${TARGET_DATABASE}.tbl_regiao(
        Region_Code			string
        ,Region_Name        string
)
PARTITIONED BY (DT_FOTO STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
TBLPROPERTIES ('orc.compress'='SNAPPY');

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE ${TARGET_DATABASE}.tbl_regiao
PARTITION(DT_FOTO)
SELECT
        Region_Code			
        ,Region_Name                                    
        ,${PARTICAO} as DT_FOTO
FROM ${TARGET_DATABASE}.regiao;