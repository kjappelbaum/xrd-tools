
FROM python:3.8-slim-buster

COPY install_packages.sh .
RUN ./install_packages.sh

RUN useradd cheminfo

WORKDIR /home/cheminfo

COPY requirements.txt .

COPY xrd_tools ./xrd_tools

COPY README.md .
COPY logging_config.ini .

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn xrd_tools.xrd_app:app --host=0.0.0.0 --port=$PORT --workers=$WORKERS --loop="uvloop" --http="httptools" --log-config=logging_config.ini --limit-concurrency=$CONCURRENCY_LIMIT
