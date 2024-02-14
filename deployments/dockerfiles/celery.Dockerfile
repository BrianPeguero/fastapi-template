FROM python3.12

RUN pip install --upgrade pip

WORKDIR /home/app

COPY ./requirements.txt /home/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /home/app/

CMD ["celery", "-A", "celery_worker", "worker", "--loglevel=info"]