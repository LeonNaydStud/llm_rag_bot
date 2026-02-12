FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости (если нужны для beautifulsoup4/lxml)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Копируем файлы зависимостей сначала для кэширования
COPY pyproject.toml poetry.lock* ./

RUN ls -la

# Устанавливаем зависимости без установки проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root




# Теперь копируем остальной код
COPY . .

RUN poetry add --no-interaction beautifulsoup4


RUN echo '#!/bin/sh\n\
set -e\n\
echo "Запуск RAG ingestion..."\n\
python ingestion/rag_data.py\n\
echo "Запуск FastAPI сервера..."\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]