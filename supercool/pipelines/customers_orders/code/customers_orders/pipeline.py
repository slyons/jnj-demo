from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from customers_orders.config.ConfigStore import *
from customers_orders.udfs.UDFs import *
from prophecy.utils import *
from customers_orders.graph import *

def pipeline(spark: SparkSession) -> None:
    df_orders = orders(spark)
    df_orders = collectMetrics(
        spark, 
        df_orders, 
        "graph", 
        "rPAIuwDmq8wRor7DyKZax$$8A1ILhO7hFjsMomKihDL1", 
        "rrE9EIn6fZIP3JjAzuiNX$$Gm330ZAC-57_gZ-jCVb8c"
    )
    df_customers = customers(spark)
    df_customers = collectMetrics(
        spark, 
        df_customers, 
        "graph", 
        "uNtJnICwfKv_ooKP9IjsN$$NRqYPzWKCGeHPEySd-7Sq", 
        "OnTMNqxbigMCD3M14OhWr$$J7SQ7cPUHbF5Ek7eOKz2w"
    )
    df_By_CustomerId = By_CustomerId(spark, df_orders, df_customers)
    df_By_CustomerId = collectMetrics(
        spark, 
        df_By_CustomerId, 
        "graph", 
        "93DFXOMtuH2f5Xq4_Cdqi$$rh2cfpyFIjbj53qu0U5IZ", 
        "l5_p0m9fgJ32uNjyozV2h$$jA94aU8AnriJNBCAcOjEM"
    )
    df_Account_Length_Subgraph = Account_Length_Subgraph(spark, df_By_CustomerId)
    df_SumAmounts = SumAmounts(spark, df_Account_Length_Subgraph)
    df_SumAmounts = collectMetrics(
        spark, 
        df_SumAmounts, 
        "graph", 
        "CJrTkjxKezt0GaymeWYQ4$$rOqyJaqbqDFgtklKNC1v9", 
        "njxDmpL-AZxfQkJfbmjf6$$ioHwtNMH0FzuI2PDne7IR"
    )
    df_SchemaTransform_4 = SchemaTransform_4(spark, df_SumAmounts)
    df_SchemaTransform_4 = collectMetrics(
        spark, 
        df_SchemaTransform_4, 
        "graph", 
        "Aqup0HfHHhVSBmBLMzHEH$$plNH6Cq80t5xwXlSlGKSd", 
        "vCeOkxxCet_4pb3qv1dBz$$NeBomQDBsObqXUlcef-HR"
    )
    Customers_Orders(spark, df_SchemaTransform_4)
    df_SchemaTransform_2 = SchemaTransform_2(spark, df_By_CustomerId)
    df_SchemaTransform_2 = collectMetrics(
        spark, 
        df_SchemaTransform_2, 
        "graph", 
        "TVTWx852GgqwxetK6PEip$$LtgWJdPBWqgQXu-M4HF0Y", 
        "IT7so1xe75UXoiui4aSQM$$IPD3PiwG_H18MDwehkhTS"
    )
    Script_1(spark, df_SumAmounts)
    df_SchemaTransform_3 = SchemaTransform_3(spark, df_SchemaTransform_2)
    df_SchemaTransform_3 = collectMetrics(
        spark, 
        df_SchemaTransform_3, 
        "graph", 
        "XaVC9pgck1nG0bzdgukNj$$_bJUizP20RHabJp92FcQZ", 
        "PDr-fQqeL9djHXKkwgVKg$$m0_eicAQEnrxMOYfhiEKt"
    )
    df_SchemaTransform_3.cache().count()
    df_SchemaTransform_3.unpersist()

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    MetricsCollector.initializeMetrics(spark)
    spark.conf.set("prophecy.collect.basic.stats", "true")
    spark.conf.set("spark.sql.legacy.allowUntypedScalaUDF", "true")
    spark.conf.set("spark.sql.optimizer.excludedRules", "org.apache.spark.sql.catalyst.optimizer.ColumnPruning")
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/customers_orders")
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/customers_orders")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
