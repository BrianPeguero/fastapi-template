FROM python3.12

RUN pip install --upgrade pip

WORKDIR /home/app

COPY ./requirements.txt /home/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /home/app/

EXPOSE 8080

CMD ["gunicorn", "--log-config", "app/utils/logging.ini", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "main:app"]