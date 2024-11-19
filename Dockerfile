# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости для работы с PostgreSQL и другие необходимые пакеты
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt /app/

# Устанавливаем все зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

CMD ["python", "main.py"]