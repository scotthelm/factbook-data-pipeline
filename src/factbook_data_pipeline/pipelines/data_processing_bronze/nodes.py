from pandas.core.frame import DataFrame
from factbook_data_pipeline.utils import load_geo_codes
import pandas as pd

def combine(*argv) -> pd.DataFrame:
    combined_dataset = pd.DataFrame()
    for df in argv:
        combined_dataset = combined_dataset.append(df, ignore_index=True)

    return combined_dataset

def intermediate_dataset_names():
    ds_names = []
    for _index, row in load_geo_codes().iterrows():
        ds_names.append(
            f'{row["code"]}_intermediate_csv_dataset'
        )
    return ds_names

def create_column_analysis(unfiltered_bronze_dataset: pd.DataFrame) -> pd.DataFrame:
    column_df = pd.DataFrame()
    column_df['count'] = unfiltered_bronze_dataset.count(0)
    column_df['percentage_of_max'] = column_df.apply(
        lambda x : x / column_df['count'].max()
    )
    column_df['should_remove'] = column_df.apply(lambda x: x['percentage_of_max'] < 0.75, axis=1)
    column_df['index_length'] = column_df.index.str.len()
    column_df['index_name'] = list(column_df.index)
    column_df['sql_shortened_name'] = column_df.apply(lambda x: shorten_name(x['index_name']), axis=1)
    return column_df

def filter_bronze_dataset_columns(
    unfiltered_bronze_dataset: pd.DataFrame,
    bronze_column_analysis_dataset: pd.DataFrame
) -> pd.DataFrame:
    unfiltered = unfiltered_bronze_dataset
    analysis = bronze_column_analysis_dataset
    # columns_to_filter = list(analysis.loc[analysis['should_remove'] == True]['index_name'])
    columns_to_filter = list(analysis.loc[analysis['should_remove'] == True]['sql_shortened_name'])
    rename = dict((x, y) for (x, y) in zip(analysis['index_name'], analysis['sql_shortened_name']))
    unfiltered.rename(columns=rename, inplace=True)
    unfiltered.drop(columns_to_filter, inplace=True, axis=1)
    return unfiltered

def strings_to_truncate():
    return [
        'economy_gini_index_coefficient_distribution_of_family_income_',
        'economy_reserves_of_foreign_exchange_and_gold_',
        'transportation_national_air_transport_system_',
        'military_and_security_military_expenditures_',
        'economy_real_gdp_purchasing_power_parity_',
        'economy_inflation_rate_consumer_prices_',
        'military_and_security_',
        'transnational_issues_',
        'waste_and_recycling_',
        'people_and_society_',
        'or_consumption_by_',   
        '_representation_',
        'transportation_',
        'communications_',
        'index_scores_',
        'environment_',
        '_inhabitants',
        'government_',
        'geography_',
        'economy_',
        'energy_',
    ]

def shorten_name(name: str) -> str:
    for prefix in strings_to_truncate():
        name = name.replace(prefix, '')
    return name
