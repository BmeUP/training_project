FROM python:3.11

WORKDIR /app

COPY main.py settings.py requirements.txt /app/
COPY /src /app/src
COPY /tests /app/tests
COPY entrypoint.sh /usr/local/bin

RUN pip install -r requirements.txt
ENTRYPOINT ["entrypoint.sh"]