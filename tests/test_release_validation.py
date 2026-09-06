from scripts.validate_test_release import (
    validate_invalid_rows,
    validate_pipeline_status,
    validate_silver_schema,
    validate_tables_exist,
    validate_test_revenue,
)


def test_valid_release_result():
    result = {
        "pipeline_status": "Succeeded",
        "tables": [
            "silver_sales",
            "gold_daily_sales",
        ],
        "silver_columns": [
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
        ],
        "total_revenue": 465.0,
        "invalid_row_count": 0,
    }

    validate_pipeline_status(result)
    validate_tables_exist(result)
    validate_silver_schema(result)
    validate_test_revenue(result)
    validate_invalid_rows(result)
