FROM python:3.10

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

ARG PROJECT_NAME=PROJECT_NAME

ENV PROJECT_NAME=$PROJECT_NAME

RUN poetry new $PROJECT_NAME