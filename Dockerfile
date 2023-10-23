FROM python:3.9-alpine3.12

WORKDIR /app
COPY . /app

RUN apk update

RUN apk add --no-cache --virtual .build-rundeps \
    linux-headers \
    build-base \
    mariadb-connector-c-dev \
    libxml2-dev \
    libxslt-dev

RUN  apk add --no-cache --virtual .libreoffice-rundeps \
    libreoffice \
    libreoffice-base \
    libreoffice-lang-ja \
    font-noto-cjk

COPY requirements.txt .
RUN pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
