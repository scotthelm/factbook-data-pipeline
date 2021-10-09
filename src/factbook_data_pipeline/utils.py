import importlib
import os.path

import pandas as pd
from kedro.extras.datasets.pandas import SQLTableDataSet
from kedro.extras.datasets.pandas.sql_dataset import (
    _get_missing_module_error,
    _get_sql_alchemy_missing_error,
)
from sqlalchemy.exc import NoSuchModuleError


def load_geo_codes():
    if os.path.isfile('conf/local/factbook_codes_normalized.csv'):
        df = pd.read_csv('conf/local/factbook_codes_normalized.csv')
    else:
        df = pd.DataFrame()
    return df

class DTypedSqlTableDataSet(SQLTableDataSet):
    def _save(self, data: pd.DataFrame) -> None:
        self._modify_save_args_dtype()
        try:
            data.to_sql(**self._save_args)
        except ImportError as import_error:
            raise _get_missing_module_error(import_error) from import_error
        except NoSuchModuleError as exc:
            raise _get_sql_alchemy_missing_error() from exc

    def _modify_save_args_dtype(self) -> None:
        new_dtype = {}
        if self._save_args == None:
            return

        dtype = self._save_args.get('dtype')

        if dtype == None:
            return

        for key, value in list(dtype.items()):
            mod_list = value.split('.')
            mod_name = ".".join(mod_list[:-1])
            class_name = "".join(mod_list[-1:])

            module = importlib.import_module(mod_name)
            actual_class = getattr(module, class_name)
            new_dtype[key] = actual_class

        self._save_args['dtype'] = new_dtype
