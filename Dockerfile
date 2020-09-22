
FROM python:3.7-slim-buster

WORKDIR /home/lsmoler

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER lsmoler

CMD gunicorn -b 0.0.0.0:$PORT -c gunicorn_conf.py --log-level debug --capture-output --enable-stdio-inheritance run_app:server

