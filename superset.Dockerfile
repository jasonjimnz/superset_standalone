FROM python:3.11.12-bullseye

WORKDIR /opt/app

ENV SUPERSET_SECRET_KEY="YOUR-SECRET-KEY"
ENV FLASK_APP=superset
ENV CONTAINER_VERSION="1.1"

RUN pip install uv && \
    uv pip install apache_superset --system && \
    uv pip install psycopg2-binary flask==2.0.3 werkzeug==2.3.0 jinja2==3.0.1 marshmallow==3.26.1 --system

RUN superset db upgrade
RUN superset fab create-admin --username admin --firstname admin --lastname admin --email admin@test.org --password admin
RUN superset init

EXPOSE 8008
CMD ["flask", "run", "--host", "0.0.0.0", "-p", "8008", "--with-threads", "--reload", "--debugger"]