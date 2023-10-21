FROM python:3.9.6-slim-buster

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    curl

WORKDIR /app
COPY ./ ./
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
