FROM python:3.10

# Set default version
ARG POETRY_VERSION=1.8.1

ENV PATH="/root/.local/bin:$PATH" \ 
    POETRY_VIRTUALENVS_CREATE=false

# Installs poetry and adds to path
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}