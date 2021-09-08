# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project hooks."""
from typing import Any, Dict, Iterable, Optional
from typing_extensions import ParamSpec
import pandas as pd
import os.path

from kedro.config import ConfigLoader
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.versioning import Journal
from kedro.pipeline.node import Node
from kedro.pipeline import Pipeline
from kedro.extras.datasets.api import APIDataSet
from kedro.extras.datasets.json import JSONDataSet
from kedro.extras.datasets.pandas import CSVDataSet

from rate_my_world_leader.pipelines.pre_data_processing.nodes import convert_api_to_json


class ProjectHooks:
    @hook_impl
    def register_config_loader(
        self, conf_paths: Iterable[str], env: str, extra_params: Dict[str, Any],
    ) -> ConfigLoader:
        return ConfigLoader(conf_paths)

    @hook_impl
    def register_catalog(
        self,
        catalog: Optional[Dict[str, Dict[str, Any]]],
        credentials: Dict[str, Dict[str, Any]],
        load_versions: Dict[str, str],
        save_version: str,
        journal: Journal,
    ) -> DataCatalog:
        the_catalog = DataCatalog.from_config(
            catalog, credentials, load_versions, save_version, journal
        )
        geo_codes = self.load_geo_codes()
        self.create_datasets(geo_codes, the_catalog)
        return the_catalog

    def say_hello(self, node: Node):
        """An extra behaviour for a node to say hello before running.
        """
        print(f"Hello from {node.name}")

    @hook_impl
    def before_node_run(self, node: Node):
        self.say_hello(node=node)

    def load_geo_codes(self):
        if os.path.isfile('conf/local/factbook_codes_normalized.csv'):
            df = pd.read_csv('conf/local/factbook_codes_normalized.csv')
        else:
            df = pd.DataFrame()
        return df

    def create_datasets(self, geo_codes: pd.DataFrame, catalog: DataCatalog):
        for _index, row in geo_codes.iterrows():
            catalog.add(
                f'{row["code"]}_api_dataset',
                APIDataSet(url=row['github_url'])
            )
            catalog.add(
                f'{row["code"]}_json_dataset',
                JSONDataSet(filepath=f'data/01_raw/{row["code"]}_data.json')
            )
            catalog.add(
                f'{row["code"]}_intermediate_csv_dataset',
                CSVDataSet(filepath=f'data/02_intermediate/{row["code"]}_intermediate.csv')
            )

    # @hook_impl
    # def before_pipeline_run(self, pipeline: Pipeline):
    #     print(pipeline.data_sets())