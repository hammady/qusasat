FROM python:3.8
LABEL maintainer="Hossam Hammady <github@hammady.net>"

WORKDIR /home

COPY ./requirements.txt /home/requirements.txt
RUN pip install -r requirements.txt

COPY . /home

CMD [ \
    "gunicorn", \
    "wsgi:app", \
    "--max-requests", \
    "10000", \
    "--timeout", \
    "5", \
    "--keep-alive", \
    "5", \
    "--log-level", \
    "info" \
]

EXPOSE 5000
