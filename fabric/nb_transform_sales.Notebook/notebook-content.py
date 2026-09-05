# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "9b505288-58e3-427b-b126-764fb8b1ef61",
# META       "default_lakehouse_name": "lh_retail",
# META       "default_lakehouse_workspace_id": "ba86760a-83d3-4269-b41e-5e1122086c5c",
# META       "known_lakehouses": [
# META         {
# META           "id": "9b505288-58e3-427b-b126-764fb8b1ef61"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql import types as T

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

bronze_path = "Files/bronze/sales"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sales_schema = T.StructType([
    T.StructField("order_id", T.StringType(), True),
    T.StructField("order_date", T.DateType(), True),
    T.StructField("customer_id", T.StringType(), True),
    T.StructField("product_id", T.StringType(), True),
    T.StructField("product_name", T.StringType(), True),
    T.StructField("category", T.StringType(), True),
    T.StructField("quantity", T.IntegerType(), True),
    T.StructField("unit_price", T.DoubleType(), True),
    T.StructField("discount_pct", T.DoubleType(), True),
    T.StructField("region", T.StringType(), True),
])

bronze_df = (
    spark.read
    .option("header", True)
    .schema(sales_schema)
    .csv(bronze_path)
)

display(bronze_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_df = (
    bronze_df
    .filter(F.col("order_id").isNotNull())
    .filter(F.col("quantity") > 0)
    .filter(F.col("unit_price") >= 0)
    .filter(
        (F.col("discount_pct") >= 0) &
        (F.col("discount_pct") <= 1)
    )
    .withColumn(
        "gross_amount",
        F.round(F.col("quantity") * F.col("unit_price"), 2)
    )
    .withColumn(
        "discount_amount",
        F.round(F.col("gross_amount") * F.col("discount_pct"), 2)
    )
    .withColumn(
        "net_revenue",
        F.round(F.col("gross_amount") - F.col("discount_amount"), 2)
    )
    .withColumn(
    "estimated_cost",
    F.round(F.col("gross_amount") * F.lit(0.65), 2)
    )
    .withColumn(
        "profit_amount",
        F.round(F.col("net_revenue") - F.col("estimated_cost"), 2)
    )
    .withColumn(
        "profit_margin",
        F.when(
            F.col("net_revenue") != 0,
            F.round(F.col("profit_amount") / F.col("net_revenue"), 4)
        ).otherwise(F.lit(None))
    )
)

display(silver_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("silver_sales")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

gold_df = (
    silver_df
    .groupBy("order_date", "region")
    .agg(
        F.countDistinct("order_id").alias("total_orders"),
        F.sum("quantity").alias("units_sold"),
        F.round(F.sum("net_revenue"), 2).alias("revenue"),
        F.round(
            F.sum("net_revenue") / F.countDistinct("order_id"),
            2
        ).alias("average_order_value")
    )
)

display(gold_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("gold_daily_sales")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

assert silver_df.count() > 0, "Silver table is empty"

assert (
    silver_df
    .filter(F.col("net_revenue") < 0)
    .count()
    == 0
), "Negative net revenue detected"

assert gold_df.count() > 0, "Gold table is empty"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
