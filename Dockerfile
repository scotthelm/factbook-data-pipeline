FROM python:3.8.11-buster as builder

ENV PROJECT_NAME factbook_data_pipeline
ENV PROJECT_PATH src/${PROJECT_NAME}

COPY requirements.txt /tmp/requirements.txt

RUN \
  pip install -r /tmp/requirements.txt && \
  rm -f /tmp/requirements.txt

WORKDIR /usr/src/app

# COPY in files required by `kedro` to trick it into thinking we have a
# complete project
COPY pyproject.toml .
COPY ${PROJECT_PATH}/cli.py ${PROJECT_PATH}/
# existence this file is required by `kedro` but when the actual
# file is used we have to COPY more and more project contents
RUN touch ${PROJECT_PATH}/settings.py

# install project dependencies
COPY src/requirements.* src/

RUN kedro install

COPY . .

EXPOSE 8888

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["kedro", "run"]

