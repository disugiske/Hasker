FROM python:3.9

RUN /usr/local/bin/python -m pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD ./source /app
WORKDIR /app