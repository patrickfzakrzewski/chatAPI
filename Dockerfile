FROM python:3.9

WORKDIR /chatAPI-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/__main__.py"]