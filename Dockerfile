FROM python:3.9-bullseye

WORKDIR app
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-dev

COPY . .

EXPOSE 8000
ENTRYPOINT poetry run alembic upgrade head && poetry run uvicorn app:create_app --factory --host 0.0.0.0 --port 8000
