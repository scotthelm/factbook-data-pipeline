import pandas as pd
import json
import requests

from io import StringIO

def convert_api_to_json(
    api_dataset: requests.models.Response
) -> dict:
    return json.loads(api_dataset.content.decode('utf-8'))