FROM python:3.12-slim

WORKDIR /

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./
COPY . .


# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --no-root


CMD ["python", "main.py"]