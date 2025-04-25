import pandas as pd
from product_session import add_session_id  

def test_single_user_single_session():
    df = pd.DataFrame({
        'customer_id': [1, 1, 1],
        'product_id': [101, 102, 103],
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 10:01:00',
            '2023-01-01 10:02:00',
        ]
    })
    result = add_session_id(df)
    assert result['session_id'].nunique() == 1

def test_single_user_multiple_sessions():
    df = pd.DataFrame({
        'customer_id': [1, 1, 1],
        'product_id': [101, 102, 103],
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 10:01:00',
            '2023-01-01 10:05:01',  
        ]
    })
    result = add_session_id(df)
    assert result['session_id'].nunique() == 2
    assert result['session_id'].tolist() == [1, 1, 2]

def test_multiple_users_separate_sessions():
    df = pd.DataFrame({
        'customer_id': [1, 1, 2, 2],
        'product_id': [101, 102, 201, 202],
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 10:04:00',  
            '2023-01-01 11:00:00',
            '2023-01-01 11:02:00',
        ]
    })
    result = add_session_id(df)
    assert result['session_id'].nunique() == 3
    assert result[result['customer_id'] == 1]['session_id'].nunique() == 2
    assert result[result['customer_id'] == 2]['session_id'].nunique() == 1

def test_exactly_three_minutes_is_same_session():
    df = pd.DataFrame({
        'customer_id': [1, 1],
        'product_id': [101, 102],
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 10:03:00',  
        ]
    })
    result = add_session_id(df)
    assert result['session_id'].nunique() == 1

def test_more_than_three_minutes_new_session():
    df = pd.DataFrame({
        'customer_id': [1, 1],
        'product_id': [101, 102],
        'timestamp': [
            '2023-01-01 10:00:00',
            '2023-01-01 10:03:01',  
        ]
    })
    result = add_session_id(df)
    assert result['session_id'].nunique() == 2
