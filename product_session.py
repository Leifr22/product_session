import pandas as pd

def add_session_id(df, session_timeout=3):
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by=['customer_id', 'timestamp'], ignore_index=True)

    prev_customer = df['customer_id'].shift(1)
    prev_timestamp = df['timestamp'].shift(1)

    new_customer = df['customer_id'] != prev_customer
    time_diff_exceeds = (df['timestamp'] - prev_timestamp) > pd.Timedelta(minutes=session_timeout)

    df['new_session'] = new_customer | time_diff_exceeds
    df['session_id'] = df['new_session'].cumsum().astype(int)

    df.drop(columns=['new_session'], inplace=True)

    return df
