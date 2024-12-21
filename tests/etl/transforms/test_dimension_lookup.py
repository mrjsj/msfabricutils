

#from msfabricutils.etl.transforms.transforms import get_dimension_surrogate_key, get_dimension_historical_surrogate_key


# @pytest.fixture
# def config():
#     return get_default_config()

# @pytest.fixture
# def mock_dimension_table(tmp_path, config):
#     # Create a sample dimension table with both current and historical records
#     df = pl.DataFrame({
#         "customer_bk": ["C1", "C1", "C2"],
#         "customer_sk": [1, 1, 2],
#         "valid_from": [
#             datetime(2023, 1, 1),
#             datetime(2023, 6, 1),
#             datetime(2023, 1, 1)
#         ],
#         "valid_to": [
#             datetime(2023, 6, 1),
#             None,
#             None
#         ]
#     })
    
#     # Save as Delta table
#     delta_path = tmp_path / "dimension_table"
#     df.write_delta(delta_path)
#     return str(delta_path)

# def test_get_dimension_surrogate_key_business_key(mock_dimension_table, config):
#     # Test data with business key
#     fact_df = pl.DataFrame({
#         "customer_bk": ["C1", "C2", "C3"],
#         "amount": [100, 200, 300]
#     })
    
#     result = get_dimension_surrogate_key(
#         fact_df,
#         mock_dimension_table,
#         config,
#         keep_key_columns=True
#     )
    
#     assert "customer_sk" in result.columns
#     assert "customer_bk" in result.columns
#     assert result.filter(pl.col("customer_bk") == "C1")["customer_sk"][0] == 1
#     assert result.filter(pl.col("customer_bk") == "C2")["customer_sk"][0] == 2
#     # C3 should get default surrogate key (usually -1)
#     assert result.filter(pl.col("customer_bk") == "C3")["customer_sk"][0] == config.surrogate_key_column.default_value

# def test_get_dimension_surrogate_key_historical(mock_dimension_table, config):
#     # Test data with business key and date for historical lookup
#     fact_df = pl.DataFrame({
#         "customer_bk": ["C1", "C1"],
#         "date_bk": [date(2023, 3, 1), date(2023, 7, 1)],
#         "amount": [100, 200]
#     })
    
#     result = get_dimension_surrogate_key(
#         fact_df,
#         mock_dimension_table,
#         config,
#         keep_key_columns=True,
#         create_historical_surrogate_key=True
#     )
    
#     # Verify current surrogate keys
#     assert result.filter(pl.col("customer_bk") == "C1")["customer_sk"].to_list() == [1, 1]
    
#     # Verify historical surrogate keys (if implemented)
#     if "customer_hsk" in result.columns:
#         historical_sks = result.filter(pl.col("customer_bk") == "C1")["customer_hsk"].to_list()
#         assert len(historical_sks) == 2
#         assert historical_sks[0] != historical_sks[1]  # Different periods should have different historical keys 

# def test_get_dimension_historical_surrogate_key():
#     # Arrange
#     config = get_default_config()
    
#     # Create sample fact data
#     fact_df = pl.DataFrame({
#         "customer_id_bk": ["C1", "C2", "C3"],
#         "order_date_bk": ["2024-01-01", "2024-01-02", "2024-01-03"]
#     })

#     # Create sample dimension data with historical records
#     dimension_df = pl.DataFrame({
#         "customer_id_bk": ["C1", "C1", "C2"],
#         "customer_sk": [1, 2, 3],
#         "valid_from": ["2023-12-01", "2024-01-02", "2023-12-01"],
#         "valid_to": ["2024-01-02", None, None]
#     })

#     # Act
#     result_df = get_dimension_historical_surrogate_key(
#         df=fact_df,
#         dimension_df=dimension_df,
#         key_columns=["customer_id_bk"],
#         config=config
#     )

#     # Assert
#     expected_df = pl.DataFrame({
#         "customer_id_bk": ["C1", "C2", "C3"],
#         "order_date_bk": ["2024-01-01", "2024-01-02", "2024-01-03"],
#         "customer_hsk": [1, 3, -1]  # -1 is the default value for non-matching records
#     })

#     assert result_df.collect() if isinstance(result_df, pl.LazyFrame) else result_df == expected_df


# def test_get_dimension_historical_surrogate_key_with_empty_dataframe():
#     # Arrange
#     config = get_default_config()
    
#     fact_df = pl.DataFrame({
#         "customer_id_bk": [],
#         "order_date_bk": []
#     })

#     dimension_df = pl.DataFrame({
#         "customer_id_bk": ["C1"],
#         "customer_sk": [1],
#         "valid_from": ["2023-12-01"],
#         "valid_to": [None]
#     })

#     # Act
#     result_df = get_dimension_historical_surrogate_key(
#         df=fact_df,
#         dimension_df=dimension_df,
#         key_columns=["customer_id_bk"],
#         config=config
#     )

#     # Assert
#     expected_df = pl.DataFrame({
#         "customer_id_bk": [],
#         "order_date_bk": [],
#         "customer_hsk": []
#     })

#     assert result_df.collect() if isinstance(result_df, pl.LazyFrame) else result_df == expected_df


# def test_get_dimension_historical_surrogate_key_invalid_key():
#     # Arrange
#     config = get_default_config()
    
#     fact_df = pl.DataFrame({
#         "customer_id_bk": ["C1"]
#     })

#     dimension_df = pl.DataFrame({
#         "customer_id_bk": ["C1"],
#         "customer_sk": [1],
#         "valid_from": ["2023-12-01"],
#         "valid_to": [None]
#     })

#     # Act & Assert
#     with pytest.raises(Exception):  # Replace with specific exception if known
#         get_dimension_historical_surrogate_key(
#             df=fact_df,
#             dimension_df=dimension_df,
#             key_columns=["invalid_column"],
#             config=config
#         )