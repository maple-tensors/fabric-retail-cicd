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
import json

EXPECTED_SILVER_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "discount_pct",
    "region",
    "gross_amount",
    "discount_amount",
    "net_revenue",
    "estimated_cost",
    "profit_amount",
    "profit_margin",
}

silver_df = spark.table("silver_sales")
gold_df = spark.table("gold_daily_sales")

silver_columns = silver_df.columns

total_revenue = (
    gold_df
    .agg(F.round(F.sum("revenue"), 2).alias("total_revenue"))
    .collect()[0]["total_revenue"]
)

invalid_row_count = (
    silver_df
    .filter(
        F.col("order_id").isNull()
        | (F.col("quantity") <= 0)
        | (F.col("unit_price") < 0)
        | (F.col("discount_pct") < 0)
        | (F.col("discount_pct") > 1)
    )
    .count()
)

validation_result = {
    "pipeline_status": "Succeeded",
    "tables": [
        "silver_sales",
        "gold_daily_sales",
    ],
    "silver_columns": silver_columns,
    "total_revenue": float(total_revenue),
    "invalid_row_count": invalid_row_count,
}

print(json.dumps(validation_result, indent=2))

assert "silver_sales" in validation_result["tables"]
assert "gold_daily_sales" in validation_result["tables"]

missing_columns = EXPECTED_SILVER_COLUMNS - set(validation_result["silver_columns"])
assert not missing_columns, f"Missing Silver columns: {sorted(missing_columns)}"

assert validation_result["invalid_row_count"] == 0, (
    f"Invalid rows found: {validation_result['invalid_row_count']}"
)

assert round(validation_result["total_revenue"], 2) == 465.00, (
    f"Expected Test revenue 465.00, "
    f"got {validation_result['total_revenue']}"
)

print("Test release validation passed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
