import json
import sys
from pathlib import Path


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


EXPECTED_TEST_REVENUE = 465.00


def load_validation_result(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Validation result file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_pipeline_status(result: dict) -> None:
    assert result["pipeline_status"] == "Succeeded", (
        f"Pipeline failed: {result['pipeline_status']}"
    )


def validate_tables_exist(result: dict) -> None:
    tables = set(result["tables"])

    assert "silver_sales" in tables, "silver_sales table is missing"
    assert "gold_daily_sales" in tables, "gold_daily_sales table is missing"


def validate_silver_schema(result: dict) -> None:
    actual_columns = set(result["silver_columns"])

    missing_columns = EXPECTED_SILVER_COLUMNS - actual_columns

    assert not missing_columns, (
        f"Missing Silver columns: {sorted(missing_columns)}"
    )


def validate_test_revenue(result: dict) -> None:
    actual_revenue = float(result["total_revenue"])

    assert actual_revenue == EXPECTED_TEST_REVENUE, (
        f"Expected revenue {EXPECTED_TEST_REVENUE}, "
        f"but got {actual_revenue}"
    )


def validate_invalid_rows(result: dict) -> None:
    invalid_rows = int(result["invalid_row_count"])

    assert invalid_rows == 0, (
        f"Expected 0 invalid rows, but found {invalid_rows}"
    )


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/validate_test_release.py "
            "<validation_result.json>"
        )
        sys.exit(2)

    result = load_validation_result(sys.argv[1])

    validate_pipeline_status(result)
    validate_tables_exist(result)
    validate_silver_schema(result)
    validate_test_revenue(result)
    validate_invalid_rows(result)

    print("Test release validation passed.")


if __name__ == "__main__":
    main()
