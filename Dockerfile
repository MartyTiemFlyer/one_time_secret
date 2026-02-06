FROM python:3.11-slim-bookworm
WORKDIR /secret_app
COPY requirements.txt .
# Устанавливаем все нужные библиотеки из requirements.txt
# Флаг --no-cache-dir говорит не сохранять временные файлы установки
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



