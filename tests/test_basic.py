from pathlib import Path


def test_expected_fabric_artifacts_exist():
    root = Path("fabric")

    assert (root / "lh_retail.Lakehouse").exists()
    assert (root / "nb_transform_sales.Notebook").exists()
    assert (root / "pl_daily_sales.DataPipeline").exists()
