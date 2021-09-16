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
            else:
                to_clean[key] = series
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
    left_series = to_clean.apply(
        lambda x: config['left_join_character'].join(x[key].split(' ')[: config['split_point']]),
        axis=1
    )
    right_series = to_clean.apply(
        lambda x: config['right_join_character'].join(x[key].split(' ')[config['split_point'] :]),
        axis=1
    )
    to_clean[config['left_field_name']] = left_series
    to_clean[config['right_field_name']] = right_series
    to_clean.drop(key, axis=1, inplace=True)

