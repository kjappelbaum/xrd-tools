
FROM python:3.7-slim-buster

COPY install_packages.sh .
RUN ./install_packages.sh

RUN useradd lsmoler

WORKDIR /home/lsmoler

COPY requirements.txt .

COPY app.py .

COPY README.md .

COPY gunicorn_conf.py .

RUN pip install --no-cache-dir -r requirements.txt

USER lsmoler

CMD gunicorn -b 0.0.0.0:$PORT -c gunicorn_conf.py --log-level debug --capture-output --enable-stdio-inheritance app:app
