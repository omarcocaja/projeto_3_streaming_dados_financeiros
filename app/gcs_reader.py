from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import pyspark.sql.functions as F

def build_spark_session(app_name="Projeto-3"):
    builder = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.driver.extraClassPath", "/opt/spark/jars/*")
        .config("spark.executor.extraClassPath", "/opt/spark/jars/*")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("google.cloud.auth.service.account.enable", "true")
    hadoop_conf.set("google.cloud.auth.service.account.json.keyfile", "/app/")
    hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")

    return spark

spark = build_spark_session()

BUCKET_NAME = 'bucket-portfolio-projeto-3'
BRONZE_PATH = f'gs://{BUCKET_NAME}/bronze/yfinance/'
SILVER_PATH = f'gs://{BUCKET_NAME}/silver/finance'
DATA_PATH = SILVER_PATH + '/financial_data'
CHECKPOINT_DIR = SILVER_PATH+'/checkpoints/financial_data_checkpoint'

from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema = StructType([
    StructField("ticker", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("time", StringType(), True),
    StructField("exchange", StringType(), True),
    StructField("change_percent", DoubleType(), True),
    StructField("change", DoubleType(), True)
])


(
    spark
    .read
    .format('parquet')
    .load(f'gs://{BUCKET_NAME}/silver/finance/financial_data/ticker=BNB-USD/part-00000-06301389-dce7-4206-b1b6-69a61de536ae.c000.snappy.parquet').show()
)