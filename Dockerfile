FROM public.ecr.aws/lambda/python:3.11

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

COPY src/ ${LAMBDA_TASK_ROOT}
COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}
# Install python packages
RUN poetry install --no-root

# CMD [ "resize.handler" ]