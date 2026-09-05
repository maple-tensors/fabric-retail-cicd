from pathlib import Path


def test_profit_margin_logic_exists():
    notebook_dir = Path("fabric/nb_transform_sales.Notebook")

    text = ""

    for file in notebook_dir.rglob("*"):
        if file.is_file():
            try:
                text += file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass

    assert "profit_margin" in text
    assert "profit_amount" in text
    assert "estimated_cost" in text
