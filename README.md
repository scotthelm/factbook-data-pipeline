# Rate My World Leader

## Prerequisites

* Docker
* Docker Compose
* nib

## Setup

```sh
nib build --pull
```

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
