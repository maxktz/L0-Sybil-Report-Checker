FROM python:3.12

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock /app/
WORKDIR /app

RUN poetry install --without dev
COPY . /app
CMD ["poetry", "run", "python", "main.py"]