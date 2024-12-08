import polars as pl

from msfabricutils.etl import get_default_flow


def test_default_flow(tmp_path):
    source_table_path = str(tmp_path / "source_table")
    target_table_path = str(tmp_path / "target_table")

    source_df = pl.DataFrame(
        {
            "ID": [1, 2, 3, 1, 2],
            "FirstName": ["Alice", "Bob", "Charlie", "AliceS", "BobB"],
            "batch_id": [1, 1, 1, 2, 2],
        }
    )
    source_df.write_delta(source_table_path)

    flow = get_default_flow()
    flow = flow.add_source_delta_table(source_table_path, "my_source").add_sink_upsert_scd_type_1(
        target_table_path, primary_key_columns="ID"
    )

    flow.run()
