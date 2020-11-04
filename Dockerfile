
FROM python:3.8-slim-buster

COPY install_packages.sh .
RUN ./install_packages.sh

RUN useradd cheminfo

WORKDIR /home/cheminfo

COPY requirements.txt .

COPY xrd_tools ./xrd_tools

COPY README.md .

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 2 --backlog 16 xrd_tools.xrd_app:app -b 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker
