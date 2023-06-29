CREATE EXTERNAL TABLE IF NOT EXISTS ${TARGET_DATABASE}.endereco (
        Address_Number			string
        ,City                   string
        ,Country                string
        ,Customer_Address_1     string
        ,Customer_Address_2     string
        ,Customer_Address_3     string
        ,Customer_Address_4     string
        ,State                  string
        ,Zip_Code               string
    )
COMMENT 'Tabela de Endereço'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE
location '${HDFS_DIR}'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS ${TARGET_DATABASE}.tbl_endereco(
        Address_Number			string
        ,City                   string
        ,Country                string
        ,Customer_Address_1     string
        ,Customer_Address_2     string
        ,Customer_Address_3     string
        ,Customer_Address_4     string
        ,State                  string
        ,Zip_Code               string
)
PARTITIONED BY (DT_FOTO STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
TBLPROPERTIES ('orc.compress'='SNAPPY');

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE ${TARGET_DATABASE}.tbl_endereco
PARTITION(DT_FOTO)
SELECT
        Address_Number			
        ,City
        ,Country
        ,Customer_Address_1
        ,Customer_Address_2
        ,Customer_Address_3
        ,Customer_Address_4
        ,State
        ,Zip_Code                                 
        ,${PARTICAO} as DT_FOTO
FROM ${TARGET_DATABASE}.endereco;