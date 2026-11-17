FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Отключаем создание pyc-файлов
ENV PYTHONDONTWRITEBYTECODE=1

# Показываем логи сразу
ENV PYTHONUNBUFFERED=1

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Порт Django
EXPOSE 8000

# Запуск Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]