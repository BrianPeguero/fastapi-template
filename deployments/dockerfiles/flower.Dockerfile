FROM python:3.12

RUN pip install --upgrade pip

WORKDIR /home/app

COPY ./requirements.txt /home/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /home/app/

EXPOSE 5555

CMD ["celery", "-A", "app.utils.celery", "flower", "port=5555", "url_prefix=flower"]