import pandas as pd
import requests

from io import StringIO

def convert_api_to_csv_dataset(
    api_dataset: requests.models.Response
) -> pd.DataFrame:
    str_response = api_dataset.content.decode('utf-8')
    df = pd.read_csv(StringIO(str_response))
    return df