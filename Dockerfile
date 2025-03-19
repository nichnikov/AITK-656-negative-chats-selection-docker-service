# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app


# Устанавливаем зависимости проекта
RUN export HTTP_PROXY=http://proxy.dev.aservices.tech:8080 && export HTTPS_PROXY=http://proxy.dev.aservices.tech:8080
RUN pip install --proxy=http://proxy.dev.aservices.tech:8080 --upgrade pip
RUN pip install --proxy=http://proxy.dev.aservices.tech:8080 --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app

# Открываем порт для FastAPI
# EXPOSE 8000

# Команда для запуска FastAPI приложения
CMD ["app.main"]
