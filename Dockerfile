FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

EXPOSE 3000

CMD ["poetry", "run", "gunicorn", "-w", "5", "-b", "0.0.0.0:8080", "page_analyzer:app"]
