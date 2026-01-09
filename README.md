# Python FAQ RAG Bot

**Описание:**  
Локальная система RAG (Retrieval-Augmented Generation) для работы с FAQ по Python. Позволяет задавать вопросы на естественном языке и получать ответы на основе локальной документации и векторного хранилища. Использует FastAPI для API и Hugging Face модели для генерации текстов на CPU.

---

## Содержание

- [Особенности](#особенности)  
- [Структура проекта](#структура-проекта)  
- [Требования](#требования)  
- [Установка](#установка)  
- [Подготовка данных и векторного хранилища](#подготовка-данных-и-векторного-хранилища)  
- [Запуск приложения](#запуск-приложения)  
- [Использование API](#использование-api)  
- [Конфигурация](#конфигурация)  
- [Используемые модели](#используемые-модели)  
- [Лицензия](#лицензия)  

---

## Особенности

- Генерация ответов на вопросы по Python FAQ с использованием RAG  
- Локальная instruction-модель на CPU  
- Векторное хранилище с Chroma и эмбеддингами Hugging Face  
- FastAPI сервер с `/ask` endpoint для запросов  
- Три режима работы:
  - **Простой** — возвращает наиболее релевантный фрагмент  
  - **Полный** — использует LLM для генерации ответа  
  - **Интерактивный** — возможность задавать вопросы через консоль  

---

## Структура проекта

```

llm_rag_bot/
├─ app/
│  ├─ main.py             # FastAPI приложение
│  ├─ api/
│  │  └─ v1/
│  │     └─ endpoints.py  # API endpoints
│  ├─ core/
│  │  └─ config.py        # Конфигурации проекта
│  ├─ services/
│  │  ├─ rag_service.py   # Логика RAG и LLM
│  │  └─ vectorstore.py   # Инициализация и загрузка vectorstore
├─ rag_data.py             # Сбор и подготовка данных для vectorstore
├─ query_rag.py            # Консольная версия RAG
├─ chroma_db/              # Локальное хранилище эмбеддингов (не коммитить)
├─ pyproject.toml          # Управление зависимостями через Poetry
└─ README.md

````

---

## Требования

- Python 3.12+  
- Poetry для управления зависимостями  
- Поддержка CPU для локальной генерации  

**Ключевые библиотеки:**

- `fastapi`, `uvicorn`
- `langchain`, `langchain_community`
- `transformers`, `torch`
- `chromadb`
- `pydantic-settings`
- `beautifulsoup4`
- `requests`

---

## Установка

1. Клонировать репозиторий:

```bash
git clone <repo_url>
cd llm_rag_bot
````

2. Установить зависимости через Poetry:

```bash
poetry install
poetry shell
```

3. Создать `.env` файл (при необходимости):

```env
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

---

## Подготовка данных и векторного хранилища

1. Запустить `rag_data.py` для загрузки FAQ:

```bash
python rag_data.py
```

* Скрипт автоматически:

  * Загружает страницы Python FAQ
  * Преобразует их в текстовые документы
  * Делит на чанки
  * Создаёт локальное векторное хранилище `chroma_db/` с эмбеддингами

2. Проверить, что файлы создались в `chroma_db/`.

---

## Запуск приложения

Запустить FastAPI сервер:

```bash
uvicorn app.main:app --reload
```

* Сервер будет доступен на: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`
* Redoc документация: `http://127.0.0.1:8000/redoc`

Остановить сервер: `CTRL + C`

---

## Использование API

### Endpoint: `/ask` (POST)

**Request Body:**

```json
{
  "question": "What is Python?"
}
```

**Response:**

```json
{
  "answer": "Python is an interpreted, interactive, object-oriented programming language..."
}
```

### Пример запроса через curl

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question":"What is Python?"}'
```

---

## Конфигурация

Все настройки проекта в `app/core/config.py`:

* `USER_AGENT` для парсинга документации
* Пути к локальному vectorstore (`chroma_db/`)
* Настройки LLM и Hugging Face моделей

Для Pydantic 2.x используется `pydantic-settings`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    persist_dir: str = "./chroma_db"

settings = Settings()
```

---

## Используемые модели

- **Эмбеддинги:** настраиваются через `settings.embedding_model` (по умолчанию:  
  `"sentence-transformers/all-MiniLM-L6-v2"`). Используются для построения векторного хранилища и поиска релевантных документов.  

- **LLM (языковая модель):** настраивается через `settings.llm_model` (по умолчанию:  
  `"google/flan-t5-base"`). Модель используется для генерации ответа на основе найденного контекста.  

> Любые изменения моделей можно сделать напрямую в `app/core/config.py`.

---

**Примечание:**
Проект полностью автономен на CPU, не требует внешних API ключей и может использоваться локально.

