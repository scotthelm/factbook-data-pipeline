import re
import pandas as pd
import sys
import json
import functools

thismodule = sys.modules[__name__]

# take in dataset, key, config
def clean(to_clean: pd.DataFrame, key: str, config: dict):
    """
    Takes in a DataFrame, column_name(key), and cleaning configuration
    and modifies the DataFrame in place

    Args:
        to_clean (DataFrame): the DataFrame to celan
        key (str): the column to clean
        config: the configuration for how to clean the column
    """
    for config_key in config:
        if config_key != 'rename_to':
            # rename_to requires a series and is handled by regex_replace
            getattr(thismodule, config_key)(to_clean, key, config)

def regex_replacement(to_clean: pd.DataFrame, key: str, config: dict):
    """
    Takes in a DataFrame, a column name (key) and a cleaning config
    and modifies the DataFrame in place. The config contains the regex
    to use for regex substitution

    If rename_to is part of the config, it will be applied here.

    Args:
        to_clean (DataFrame): the DataFrame to celan
        key (str): the column to clean
        config: the configuration for how to clean the column
    """
    series = to_clean.apply(
        lambda x: regex_replacement_value(x[key], config),
        axis=1
    )
    if config.get('rename_to'):
        to_clean[config['rename_to']] = series 
        to_clean.drop(key, inplace=True, axis=1)
    else:
        to_clean[key] = series

def regex_replacement_value(value: str, config: dict) -> str:
    """
    Takes in a string and a config. For each regex in the config,
    replace the regex in the string

    Args:
        value (str): the string to replace
        config (dict): the regexes to use to replace
    Returns:
        the fully replaced string
    """
    regexes = config['regex_replacement']
    if not isinstance(value, str):
        return None
    else:
        for r in regexes:
            value = re.sub(r, '', value)
        return value

def tokenize_and_split_fields(to_clean: pd.DataFrame, key: str, config: dict):
    """
    Takes in a DataFrame, column (key), and config. It tokenizes and splits
    the column in a series according to the config and creates separate fields
    for left and right.

    It adds the left and right series to the DataFrame in place according to
    the names in the configs.

    Args:
        to_clean (DataFrame): the DataFrame to celan
        key (str): the column to clean
        config: the configuration for how to clean the column
    """
    token_config = config['tokenize_and_split_fields']
    sp = token_config['split_point']
    ljc = token_config['left_join_character']
    rjc = token_config['right_join_character']
    left_series = to_clean.apply(
        lambda x: ljc.join(x[key].strip().split(' ')[: sp]) if type(x[key]) == str else x[key],
        axis=1
    )
    right_series = to_clean.apply(
        lambda x: rjc.join(re.sub('m m$', 'm', x[key]).strip().split(' ')[sp :]) if type(x[key]) == str else x[key],
        axis=1
    )
    to_clean[token_config['left_field_name']] = left_series
    to_clean[token_config['right_field_name']] = right_series
    to_clean.drop(key, axis=1, inplace=True)

def create_dictionary(to_clean: pd.DataFrame, key: str, config: dict):
    """
    Takes in a DataFrame, column (key), and config. It splits the items
    according to the config and creates a dictionary if it can.

    It adds the series to the DataFrame in place according to the names
    in the configs.

    Args:
        to_clean (DataFrame): the DataFrame to celan
        key (str): the column to clean
        config: the configuration for how to clean the column
    """

    dict_config = config['create_dictionary']
    series = to_clean.apply(
        lambda x: separate_into_dict(x[key], dict_config),
        axis=1
    )
    to_clean[key] = series

def drop_column(to_clean: pd.DataFrame, key: str, config: dict):
    """
    Takes in a DataFrame, column (key), and config. It drops the column
    in place. (there is really no need for the config. It lets us adhere
    to the contract)

    Args:
        to_clean (DataFrame): the DataFrame to celan
        key (str): the column to clean
        config: the configuration for how to clean the column
    """

    to_clean.drop(key, axis=1, inplace=True)

def separate_into_dict(value: str, config: dict) -> dict:
    """
    Takes in a string and returns a dict, filled out if it can

    Args:
        value (str): string to turn into a dict
        config (dict): contains the separator character
    Returns:
        a dict
    """
    if value == None:
        return {}
    values = value.split(config['item_separator'])
    items = [i.strip().split(" ") for i in values]
    items = [[" ".join(x[:-1]), "".join(x[-1:])] for x in items]
    items = [item for sublist in items for item in sublist]
    if second_values_numeric(items):
        it = iter(items)
        return dict(zip(it, it))
    else:
        return {}

def second_values_numeric(value: list) -> bool:
    """ 
    Takes in a list and return whether every second value is
    numeric

    Args:
        value (list): the list to comprehend
    Returns:
        a bool indicating whether or not every second value
        is numeric
    """
    numeric_values = [
        bool(re.search('[0-9]', value[i])) for i in range(1, len(value), 2)
    ]
    return functools.reduce(lambda a, b: a & b, numeric_values)