FROM python:3.12

RUN pip install poetry==1.8.3
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . /app
CMD ["poetry", "run", "python", "main.py"]