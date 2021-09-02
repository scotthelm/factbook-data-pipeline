#! /usr/bin/env bash

# deal with `nib` inserting itself here (e.g. shell history)
args="$(echo "${@}" | tail -n 2 | sed -z '$ s/\n$//' | xargs)"

if [ "${args}" = 'viz' ]; then
  args="viz --host 0.0.0.0"
elif [ "${args}" = 'jupyter' ]; then
  args="jupyter lab --ip 0.0.0.0 --allow-root --no-browser --LabApp.token=token"
elif [ "${args}" = 'bash' ]; then
  exec /bin/bash
  exit 0
fi

echo "Running: kedro ${args}"

exec kedro ${args}
