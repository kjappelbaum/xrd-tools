
FROM python:3.7-slim-buster

COPY install_packages.sh .
RUN ./install_packages.sh

RUN useradd cheminfo

WORKDIR /home/cheminfo

COPY requirements.txt .

COPY xrd-tools ./xrd-tools

COPY README.md .

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 4 xrd-tools.xrd-tools:app -b 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker
