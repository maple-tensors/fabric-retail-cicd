from src.retail_logic import calculate_metrics


def test_standard_sale():
    result = calculate_metrics(
        quantity=2,
        unit_price=25.00,
        discount_pct=0.10,
    )

    assert result["gross_amount"] == 50.00
    assert result["discount_amount"] == 5.00
    assert result["net_revenue"] == 45.00
    assert result["estimated_cost"] == 32.50
    assert result["profit_amount"] == 12.50
    assert result["profit_margin"] == 0.2778


def test_zero_discount():
    result = calculate_metrics(
        quantity=3,
        unit_price=30.00,
        discount_pct=0.00,
    )

    assert result["gross_amount"] == 90.00
    assert result["discount_amount"] == 0.00
    assert result["net_revenue"] == 90.00


def test_full_discount_returns_no_margin():
    result = calculate_metrics(
        quantity=1,
        unit_price=100.00,
        discount_pct=1.00,
    )

    assert result["net_revenue"] == 0.00
    assert result["profit_margin"] is None
