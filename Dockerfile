FROM python:3.11.4-alpine3.18

ENV PYTHONBUFFERED=1

WORKDIR ./

RUN apk update && apk upgrade
RUN apk add postgresql12-client

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

COPY ./ ./

EXPOSE 8000

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "loanpro.wsgi", "-b", "0.0.0.0:8000"]
