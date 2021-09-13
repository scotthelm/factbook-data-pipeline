import re
import pandas as pd
import sys

thismodule = sys.modules[__name__]

# take in dataset, key, config
def clean(to_clean: pd.DataFrame, key: str, config: dict):
    for config_key in config:
        if config_key == 'regex_replacement':
            series = to_clean.apply(
                lambda x: regex_replacement(x[key], config),
                axis=1
            )
            if config.get('rename_to'):
                to_clean[config['rename_to']] = series 
                to_clean.drop(key, inplace=True, axis=1)
        elif config_key == 'tokenize_and_split_fields':
            tokenize_and_split_fields(to_clean, key, config['tokenize_and_split_fields'])

def regex_replacement(value: str, config: dict) -> str:
    regexes = config['regex_replacement']
    if not isinstance(value, str):
        return None
    else:
        for r in regexes:
            value = re.sub(r, '', value)
        return value

def tokenize_and_split_fields(to_clean: pd.DataFrame, key: str, config: dict):
    to_clean