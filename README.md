# Factbook Data Pipeline

This repository is for collecting, normalizing, cleaning, and standardizing CIA World Factbook data.

The data that is processed in this pipeline is sourced from the [factbook.json](https://github.com/factbook/factbook.json)
 project. Their work is invaluable in this process. Every week, they produce a new set of data that is sourced from the CIA World Factbook site (which is a difficult datasource to pull from)

The goal of the pipelines is to create a dataset that has been cleaned to allow quantitative analysis of country data.

The origin of this project is as a learning exercise for myself. I wanted to learn how to use kedro to collect data, and make that data available for further refinement/model building/model execution. This particular dataset perhaps does not lend itself well to predictive analytics or machine learning, as the volume is low. However, the exercise of gathering data from various sources and synthesizing it into another form is instructive for me.

## Prerequisites

* Docker
* Docker Compose
* nib

## Setup

```sh
# build the image locally
nib build --pull
# set up the database and fetch/create config data
nib up -d db && \
sleep 2 && \
psql postgresql://postgres:docker@localhost:54323/postgres \
    -c 'create database factbook_data' && \
nib run kedro run --pipeline=pdp
```

## Pipelines

The following pipelines

* __default__ - dfp + dpi + dpb
* pdp - pre_data_processing
  * fetches country code data 
  * builds links to factbook data
  * stores configuration in conf/local
* dfp - data_fetching_pipeline
  * fetches raw data using configured links
  * stores country json files in data/01_primary
* dpi - data_processing_intermediate_pipeline
  * creates csv files of flattened json
* dpb - data_processing_bronze
  * combines individual country datasets in to a single dataset
  * creates column analysis file
  * shortens and renames columns for storage in sql
  * writes data to a postgres table


## Usage Examples

```sh
# kedro cli help
nib run kedro -h

# run a jupyter lab server: http://127.0.0.1:8888/lab?token=token
nib run --service-ports kedro jupyter

# run the kedro visualizer: http://localhost:4141/
nib run --service-ports kedro viz

# start an ipython session
nib run kedro ipython

# start a bash session
nib shell kedro

# run the test suite
nib run kedro test
```

## Debugging

To add a "break-point" for interactive debugging (say when running the test suite) add the following to a function where you would like to start your interactive session.

```python
import ipdb; ipdb.set_trace()
```

## Adding a Library

Add new library dependencies to `src/requirements.in` then run the following commands.

```sh
nib run kedro build-reqs && nib build --pull
```

## Packaging a Pipeline

```sh
pipeline_name="curate_repos" # ex. curate_repos
nib run kedro pipeline package $pipeline_name
```
