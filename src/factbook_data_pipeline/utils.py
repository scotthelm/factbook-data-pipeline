import pandas as pd
import os.path

def load_geo_codes():
    if os.path.isfile('conf/local/factbook_codes_normalized.csv'):
        df = pd.read_csv('conf/local/factbook_codes_normalized.csv')
    else:
        df = pd.DataFrame()
    return df
