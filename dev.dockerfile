FROM python:3.8
LABEL maintainer="Hossam Hammady <github@hammady.net>"

WORKDIR /home

COPY ./requirements-dev.txt /home/requirements.txt
RUN pip install -r requirements.txt

COPY . /home
CMD [ "python", "app.py" ]

EXPOSE 5000
