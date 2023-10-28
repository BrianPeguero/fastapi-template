FROM python:3.12-bullseye

WORKDIR /usr/src/app

COPY requirements.lock.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]