VALID_REGIONS = {"North", "South", "East", "West"}


def test_valid_region_values():
    sample_regions = ["North", "South", "East", "West"]

    assert all(region in VALID_REGIONS for region in sample_regions)


def test_quantity_must_be_positive():
    valid_quantities = [1, 2, 5, 10]

    assert all(quantity > 0 for quantity in valid_quantities)


def test_discount_range():
    discounts = [0.0, 0.10, 0.25, 1.0]

    assert all(0 <= discount <= 1 for discount in discounts)

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


def test_expected_silver_schema():
    actual_columns = EXPECTED_SILVER_COLUMNS.copy()

    assert actual_columns == EXPECTED_SILVER_COLUMNS
