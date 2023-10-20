FROM python:3.11-alpine

RUN apk upgrade --update
RUN apk add --no-cache \
    libffi-dev \
    git \
    vim \
    curl \
    bash \
    build-base

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
