FROM python:3.12

RUN python3 -m pip install poetry

COPY pyproject.toml /app/pyproject.toml
WORKDIR /app
RUN poetry install
RUN poetry shell

COPY . /app
CMD ["python3", "main.py"]