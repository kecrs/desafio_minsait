from pyspark.sql import SparkSession, dataframe, Row
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType
from pyspark.sql import HiveContext
from pyspark.sql.functions import *
from pyspark.sql import functions as f
from pyspark.sql.functions import col,trim,ltrim,rtrim,when,regexp_replace,concat_ws, lit, sha2

import os
import re 

spark = SparkSession.builder.master("local[*]")\
    .enableHiveSupport()\
    .getOrCreate()

#Iniciando o tratamento dos dados

#===========================================CLIENTE===========================================
#Criando DataFrame
df_clientes = spark.sql("select * from desafio_curso.tbl_clientes")
#Convertendo os tipos de dados
df_clientes = df_clientes.withColumn("address_number",col("address_number").cast(IntegerType()))\
        .withColumn("business_unit",col("business_unit").cast(IntegerType()))\
        .withColumn("customerkey",col("customerkey").cast(IntegerType()))\
        .withColumn("division",col("division").cast(IntegerType()))\
        .withColumn("region_code",col("region_code").cast(IntegerType()))
#Tratando as colunas vazias
df_clientes = df_clientes.withColumn('line_of_business', regexp_replace('line_of_business', '   ', 'Não Informado'))
#Criando view
df_clientes.createOrReplaceTempView('tb_clientes')

#===========================================DIVISAO===========================================
#Criando DataFrame
df_divisao = spark.sql("select * from desafio_curso.tbl_divisao")
#Convertendo os tipos de dados
df_divisao = df_divisao.withColumn("division",col("division").cast(IntegerType()))
#Criando view
df_divisao.createOrReplaceTempView('tb_divisao')

#===========================================ENDEREÇO===========================================
#Criando DataFrame
df_endereco = spark.sql("select * from desafio_curso.tbl_endereco")
#Convertendo os tipos de dados
df_endereco = df_endereco.withColumn("address_number",col("address_number").cast(IntegerType()))
#Tratando as colunas vazias
df_endereco = df_endereco.withColumn('city', regexp_replace('city', '                        ', 'Não Informado'))            .withColumn('customer_address_1', regexp_replace('customer_address_1', '                                       ', 'Não Informado'))            .withColumn('customer_address_2', regexp_replace('customer_address_2', '                                       ', 'Não Informado'))            .withColumn('customer_address_3', regexp_replace('customer_address_3', '                                       ', 'Não Informado'))            .withColumn('customer_address_4', regexp_replace('customer_address_4', '                                       ', 'Não Informado'))            .withColumn('zip_code', regexp_replace('zip_code', '            ', 'Não Informado'))
df_endereco = df_endereco.select([when(col(c)=="",None).otherwise(col(c)).alias(c) for c in df_endereco.columns])
df_endereco = df_endereco.na.fill("Não Informado")
#Criando view
df_endereco.createOrReplaceTempView('tb_endereco')

#===========================================REGIÃO===========================================
#Criando DataFrame
df_regiao = spark.sql("select * from desafio_curso.tbl_regiao")
#Convertendo os tipos de dados
df_regiao = df_regiao.withColumn("region_code",col("region_code").cast(IntegerType()))
#Criando view
df_regiao.createOrReplaceTempView('tb_regiao')

#===========================================VENDAS===========================================
#Criando DataFrame
df_vendas = spark.sql("select * from desafio_curso.tbl_vendas")
#Convertendo os tipos de dados
df_vendas = df_vendas.withColumn("customerkey",col("customerkey").cast(IntegerType()))\
        .withColumn("discount_amount",col("discount_amount").cast(DoubleType()))\
        .withColumn("invoice_number",col("invoice_number").cast(IntegerType()))\
        .withColumn("item_number",col("item_number").cast(IntegerType()))\
        .withColumn("line_number",col("item_number").cast(IntegerType()))\
        .withColumn("list_price",col("list_price").cast(DoubleType()))\
        .withColumn("order_number",col("order_number").cast(IntegerType()))\
        .withColumn("sales_amount",col("sales_amount").cast(DoubleType()))\
        .withColumn("sales_amount_based_on_list_price",col("sales_amount_based_on_list_price").cast(DoubleType()))\
        .withColumn("sales_cost_amount",col("sales_cost_amount").cast(DoubleType()))\
        .withColumn("sales_margin_amount",col("sales_margin_amount").cast(DoubleType()))\
        .withColumn("sales_price",col("sales_price").cast(DoubleType()))\
        .withColumn("sales_quantity",col("sales_quantity").cast(IntegerType()))\
        .withColumn("sales_rep",col("sales_rep").cast(IntegerType()))
#Convertendo string para timestamp
df_vendas = df_vendas.select('discount_amount',
                             'invoice_number',
                             'item_class',
                             'item_number',
                             'item',
                             'line_number',
                             'list_price',
                             'order_number',
                             'sales_amount',
                             'sales_amount_based_on_list_price',
                             'sales_cost_amount',
                             'sales_margin_amount',
                             'sales_price',
                             'sales_quantity',
                             'sales_rep',
                             'u_m', 
                             'customerkey',
                             'dt_foto',
                             from_unixtime(unix_timestamp('actual_delivery_date', 'dd/MM/yyy')).alias('actual_delivery_date'),
                             from_unixtime(unix_timestamp('invoice_date', 'dd/MM/yyy')).alias('invoice_date'),
                             from_unixtime(unix_timestamp('promised_delivery_date', 'dd/MM/yyy')).alias('promised_delivery_date'),
                             from_unixtime(unix_timestamp('datekey', 'dd/MM/yyy')).alias('datekey')
                            )
#Tratando as colunas vazias
df_vendas = df_vendas.na.fill(value=0)
df_vendas = df_vendas.select([when(col(c)=="",None).otherwise(col(c)).alias(c) for c in df_vendas.columns])
df_vendas = df_vendas.na.fill("Não Informado")
df_vendas = df_vendas.withColumn("datekey",to_timestamp(col("datekey")))
df_vendas = df_vendas.withColumn("promised_delivery_date",to_timestamp(col("promised_delivery_date")))
df_vendas = df_vendas.withColumn("invoice_date",to_timestamp(col("invoice_date")))
df_vendas = df_vendas.withColumn("actual_delivery_date",to_timestamp(col("actual_delivery_date")))
#Criando view
df_vendas.createOrReplaceTempView('tb_vendas')

#===========================================STAGE===========================================

#Criando tabelão com todos os dados
query='''
SELECT    c.customerkey
          ,c.customer
          ,c.customer_type
          ,c.business_family
          ,c.business_unit
          ,c.division
          ,d.division_name
          ,c.line_of_business
          ,c.phone
          ,c.region_code
          ,r.region_name
          ,c.regional_sales_mgr
          ,c.search_type
          ,v.datekey
          ,v.actual_delivery_date
          ,v.discount_amount
          ,v.invoice_date
          ,v.invoice_number
          ,v.item_class
          ,v.item_number
          ,v.item
          ,v.line_number
          ,v.list_price
          ,v.order_number
          ,v.promised_delivery_date
          ,v.sales_amount
          ,v.sales_amount_based_on_list_price
          ,v.sales_cost_amount
          ,v.sales_margin_amount
          ,v.sales_price
          ,v.sales_quantity
          ,v.sales_rep
          ,v.u_m
          ,e.address_number
          ,e.city
          ,e.country
          ,e.customer_address_1
          ,e.customer_address_2
          ,e.customer_address_3
          ,e.customer_address_4
          ,e.state
          ,e.zip_code
          ,e.dt_foto
FROM      tb_vendas v
          INNER JOIN tb_clientes c ON v.customerkey == c.customerkey
          INNER JOIN tb_regiao r ON c.region_code == r.region_code
          INNER JOIN tb_divisao d ON c.division == d.division
          LEFT JOIN tb_endereco e ON c.address_number == e.address_number
'''

#Criando DataFrame
df_stage = spark.sql(query)
#Adicionando as colunas do tempo
df_stage = (df_stage
            .withColumn('Ano', year(df_stage.invoice_date))
            .withColumn('Mes', month(df_stage.invoice_date))
            .withColumn('Dia', dayofmonth(df_stage.invoice_date))
            .withColumn('Trimestre', quarter(df_stage.invoice_date))
           )
#Tratando as colunas nulas após os JOINS
df_stage = df_stage.select([when(col(c)=="",None).otherwise(col(c)).alias(c) for c in df_stage.columns])
df_stage = df_stage.na.fill("Não Informado")

#Gerando keys para as DIMs
df_stage = df_stage.withColumn('key_cliente',sha2(col("customerkey").cast(StringType()),256))
df_stage = df_stage.withColumn('key_tempo',sha2(concat_ws('|', col('invoice_date'), col('Ano'),col('Mes'),col('Dia')),256))
df_stage = df_stage.withColumn('key_localidade',sha2(concat_ws('|', col('division'), col('region_code'),col('address_number')),256))

#Gerando VIEW
df_stage.createOrReplaceTempView('tb_stage')

#===========================================DIMENSÕES===========================================

#Criando DataFrame para a dimensão de tempo
dim_clientes = spark.sql('''
    SELECT DISTINCT key_cliente
        ,business_family
        ,customer 
        ,customer_type 
        ,line_of_business
        ,regional_sales_mgr
        ,search_type
    FROM tb_stage    
''')

#Criando DataFrame para a dimensão de tempo
dim_tempo = spark.sql('''
    SELECT DISTINCT key_tempo
        ,invoice_date
        ,Ano 
        ,Mes 
        ,Dia
        ,Trimestre
    FROM tb_stage    
''')

dim_tempo = dim_tempo.withColumn('invoice_date',to_date('invoice_date'))

#Criando DataFrame para a dimensão de localidade
dim_localidade = spark.sql('''
    SELECT DISTINCT key_localidade
        ,division_name
        ,region_name 
        ,country 
        ,state
        ,city
        ,zip_code
    FROM tb_stage    
''')

#===========================================FATO===========================================

#Criando o DataFrame da fato
ft_vendas = spark.sql('''
    SELECT DISTINCT key_cliente
        ,key_tempo
        ,key_localidade
        ,count(distinct invoice_number) qty_vendas
        ,sum(sales_quantity) quantity
        ,sum(sales_amount) amount
        ,sum(sales_cost_amount) cost
        ,sum(sales_amount - sales_cost_amount) total_amount
    FROM tb_stage    
    GROUP BY key_cliente
        ,key_tempo
        ,key_localidade
''')

#===========================================CSV===========================================

#Procedimento para gerar os arquivos CSVs
def criar_csv (df,name):
    
    df.coalesce(1).write\
        .format('csv')\
        .option('header',True)\
        .mode('overwrite')\
        .option('sep',';')\
        .save("/datalake/gold/"+name)
    
    copiar = "hdfs dfs -get /datalake/gold/"+name+"/*.csv /input/gold/"+name+".csv"
    
    os.system(copiar)

#Criando os arquivos csv    
criar_csv(dim_tempo,'dim_tempo')
criar_csv(dim_localidade,'dim_localidade')
criar_csv(dim_clientes,'dim_clientes')
criar_csv(ft_vendas,'ft_vendas')