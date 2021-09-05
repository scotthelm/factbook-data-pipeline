import pandas as pd

def convert_json_to_dataframe(json_data: dict) -> pd.DataFrame:
    return pd.json_normalize(json_data)