# легкий официальный образ Python
FROM python:3.13-slim

# чтобы вывод не буферизировался
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# системные либы для lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# рабочая директория внутри контейнера
WORKDIR /app

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем проект (папку f6ops и файлы в корне)
COPY . .

# команда по умолчанию — просто показать помощь
CMD ["python", "-m", "f6ops.process_phones"]