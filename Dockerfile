FROM python:3.7.3-stretch

WORKDIR /app

ADD . /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python","app.py"]