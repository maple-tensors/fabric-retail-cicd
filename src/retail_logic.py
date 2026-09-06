def calculate_metrics(quantity, unit_price, discount_pct, cost_rate=0.65):
    gross_amount = round(quantity * unit_price, 2)
    discount_amount = round(gross_amount * discount_pct, 2)
    net_revenue = round(gross_amount - discount_amount, 2)
    estimated_cost = round(gross_amount * cost_rate, 2)
    profit_amount = round(net_revenue - estimated_cost, 2)

    profit_margin = None
    if net_revenue != 0:
        profit_margin = round(profit_amount / net_revenue, 4)

    return {
        "gross_amount": gross_amount,
        "discount_amount": discount_amount,
        "net_revenue": net_revenue,
        "estimated_cost": estimated_cost,
        "profit_amount": profit_amount,
        "profit_margin": profit_margin,
    }
