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

"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
from factbook_data_pipeline.pipelines import pre_data_processing as pdp
from factbook_data_pipeline.pipelines import data_fetching as df
from factbook_data_pipeline.pipelines import data_processing_intermediate as dpi
from factbook_data_pipeline.pipelines import data_processing_bronze as dpb
from factbook_data_pipeline.utils import load_geo_codes

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    pre_data_processing_pipeline = pdp.create_pipeline()
    data_fetching_pipeline = df.create_pipeline()
    data_processing_intermediate_pipeline = dpi.create_pipeline()
    data_processing_bronze_pipeline = dpb.create_pipeline()
    data_processing_pipeline = Pipeline(
        [
            pipeline(data_fetching_pipeline, outputs=fetching_outputs()),
            pipeline(data_processing_intermediate_pipeline, inputs=fetching_outputs(), outputs=intermediate_outputs()),
            pipeline(data_processing_bronze_pipeline, inputs=intermediate_outputs())
        ]
    )

    return {
        "__default__": data_processing_pipeline,
        "pdp": pre_data_processing_pipeline,
        "df": data_fetching_pipeline,
        "dpi": data_processing_intermediate_pipeline,
        "dpb": data_processing_bronze_pipeline,
    }

def intermediate_outputs() -> list:
    inputs = []
    for _index, row in load_geo_codes().iterrows():
        inputs.append(
            f'{row["code"]}_intermediate_csv_dataset'
        )
    return inputs

def fetching_outputs() -> list:
    inputs = []
    for _index, row in load_geo_codes().iterrows():
        inputs.append(
            f'{row["code"]}_json_dataset'
        )
    return inputs
