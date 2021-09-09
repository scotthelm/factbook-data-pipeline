import pandas as pd
import json
import requests

from io import StringIO

def convert_api_to_csv_dataset(
    api_dataset: requests.models.Response
) -> pd.DataFrame:
    str_response = api_dataset.content.decode('utf-8')
    df = pd.read_csv(StringIO(str_response))
    return df.loc[df['Category'] == 'Countries']

def normalize_factbook_codes(
    codes_dataset: pd.DataFrame
) -> pd.DataFrame:
    codes_dataset.rename(
        columns={
            'Code': 'code',
            'Region': 'region',
            'Name': 'name',
            'Category': 'category',
        },
        inplace=True
    )
    normalized_region = codes_dataset['region'].map(
        lambda x: x.lower().replace(' ', '-').replace('&', 'n').replace('and', 'n')
    )
    codes_dataset['normalized_region'] = normalized_region
    codes_dataset['github_url'] = codes_dataset.apply(
        lambda x:
            '/'.join(
                [
                    'https:/',
                    'raw.githubusercontent.com',
                    'factbook',
                    'factbook.json',
                    'master',
                    x['normalized_region'],
                    f'{x["code"]}.json'
                ]
            ),
            axis=1)
        
    return codes_dataset

def convert_api_to_json(
    api_dataset: requests.models.Response
) -> dict:
    return json.loads(api_dataset.content.decode('utf-8'))