import pandas as pd
import json
import requests
from kedro.io import MemoryDataSet

from io import StringIO

def convert_api_to_json(
    api_dataset: requests.models.Response,
    name_dataset: MemoryDataSet
) -> dict:
    data = json.loads(api_dataset.content.decode('utf-8'))
    # showing how name_dataset_could be used:
    # data["country_name"] = name_dataset
    # this is not necessary in this case
    # but having the example of how it _could_ be used is instructive.
    return data