import pandas as pd
from product_session import add_session_id

def test_single_session():
    data = {
        "customer_id": [1, 1, 1],
        "product_id": [100, 200, 300],
        "timestamp": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 10:02:00", "2023-01-01 10:03:59"])
    }
    df = pd.DataFrame(data)
    df = add_session_id(df)
    assert (df["session_id"] == 1).all()
def test_two_sessions():
    data = {
        "customer_id": [1, 1, 1],
        "product_id": [100, 200, 300],
        "timestamp": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 10:04:01", "2023-01-01 10:05:00"])
    }
    df = pd.DataFrame(data)
    df = add_session_id(df)
    assert df["session_id"].tolist() == [1, 2, 2]
def test_exact_3_minutes():
    data = {
        "customer_id": [1, 1],
        "timestamp": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 10:03:00"])
    }
    df = pd.DataFrame(data)
    df = add_session_id(df)
    assert df["session_id"].tolist() == [1, 1]
def test_single_row():
    data = {
        "customer_id": [1],
        "timestamp": pd.to_datetime(["2023-01-01 10:00:00"])
    }
    df = pd.DataFrame(data)
    df = add_session_id(df)
    assert df["session_id"].tolist() == [1]
def test_different_customers():
    data = {
        "customer_id": [1, 2],
        "timestamp": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 10:01:00"])
    }
    df = pd.DataFrame(data)
    df = add_session_id(df)
    assert df["session_id"].tolist() == [1, 2]
def test_unsorted_data():
    data = {
        "customer_id": [1, 1, 1],
        "timestamp": pd.to_datetime(["2023-01-01 10:05:00", "2023-01-01 10:00:00", "2023-01-01 10:10:00"])
    }
    df = pd.DataFrame(data)
    df = add_session_id(df)
    
    assert df["session_id"].tolist() == [1, 2, 3]  
def test_original_columns():
    data = {
        "customer_id": [1, 1],
        "product_id": [100, 200],
        "timestamp": pd.to_datetime(["2023-01-01 10:00:00", "2023-01-01 10:04:00"])
    }
    df_original = pd.DataFrame(data).copy()
    df = add_session_id(df_original)
    assert "product_id" in df.columns  